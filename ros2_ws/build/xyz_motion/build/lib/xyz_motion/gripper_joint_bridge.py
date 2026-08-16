"""Bridge /command_gripper to ros2_control and optional robot TCP gripper."""

from __future__ import annotations

import socket
import threading

import rclpy
from control_msgs.action import GripperCommand
from rclpy.action import ActionClient
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray, String

CMD_OPEN = 'open'
CMD_CLOSE = 'close'
CMD_CLOSE_UNTIL_STALL = 'close_until_stall'


class GripperJointBridge(Node):
    def __init__(self) -> None:
        super().__init__('gripper_joint_bridge')
        self.declare_parameter('finger_joint_name', 'lara5_gripper_finger_joint')
        self.declare_parameter('open_position', 1.74533)
        self.declare_parameter('close_position', -0.174533)
        self.declare_parameter('gripper_commands_topic', 'gripper_controller/commands')
        self.declare_parameter('gripper_action_name', 'gripper_controller/gripper_cmd')
        self.declare_parameter('use_forward_command', True)
        self.declare_parameter('use_gripper_action', False)
        self.declare_parameter('forward_to_robot', False)
        self.declare_parameter('robot_host', '192.168.2.13')
        self.declare_parameter('robot_port', 5000)
        self.declare_parameter('controller_wait_sec', 15.0)
        self.declare_parameter('dynamixel_open', 1500)
        self.declare_parameter('dynamixel_close', 600)
        self.declare_parameter('use_dynamixel_ticks', True)

        self._open_pos = float(self.get_parameter('open_position').value)
        self._close_pos = float(self.get_parameter('close_position').value)
        self._dxl_open = int(self.get_parameter('dynamixel_open').value)
        self._dxl_close = int(self.get_parameter('dynamixel_close').value)
        self._use_dxl = bool(self.get_parameter('use_dynamixel_ticks').value)
        self._use_forward = bool(self.get_parameter('use_forward_command').value)
        self._use_action = bool(self.get_parameter('use_gripper_action').value)
        self._forward = bool(self.get_parameter('forward_to_robot').value)
        self._robot_host = str(self.get_parameter('robot_host').value)
        self._robot_port = int(self.get_parameter('robot_port').value)
        self._wait_sec = float(self.get_parameter('controller_wait_sec').value)

        self._cmd_pub = None
        if self._use_forward:
            topic = str(self.get_parameter('gripper_commands_topic').value)
            self._cmd_pub = self.create_publisher(Float64MultiArray, topic, 10)

        self._action_client: ActionClient | None = None
        if self._use_action:
            action_name = str(self.get_parameter('gripper_action_name').value)
            self._action_client = ActionClient(self, GripperCommand, action_name)

        self._sock: socket.socket | None = None
        self._sock_lock = threading.Lock()
        if self._forward:
            self._connect_robot()

        self.create_subscription(String, 'command_gripper', self._on_command, 10)
        self.get_logger().info(
            'gripper_joint_bridge ready '
            f'(forward_cmd={self._use_forward}, action={self._use_action}, tcp={self._forward})'
        )

    def _connect_robot(self) -> None:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5.0)
            sock.connect((self._robot_host, self._robot_port))
            sock.settimeout(None)
            self._sock = sock
            self.get_logger().info(
                f'connected to robot gripper at {self._robot_host}:{self._robot_port}'
            )
        except OSError as exc:
            self.get_logger().warning(f'robot gripper TCP not connected: {exc}')

    def _send_tcp(self, cmd: str) -> None:
        if not self._forward:
            return
        with self._sock_lock:
            if self._sock is None:
                self._connect_robot()
            if self._sock is None:
                return
            try:
                self._sock.sendall(cmd.encode())
            except OSError as exc:
                self.get_logger().warning(f'TCP gripper send failed: {exc}')
                self._sock = None

    def _ticks_to_joint(self, ticks: float) -> float:
        lo, hi = self._dxl_close, self._dxl_open
        if hi == lo:
            return self._close_pos
        t = max(lo, min(hi, ticks))
        alpha = (t - lo) / (hi - lo)
        return self._close_pos + alpha * (self._open_pos - self._close_pos)

    def _command_to_position(self, cmd: str) -> float | None:
        c = cmd.strip().lower()
        if c in (CMD_OPEN,):
            return self._open_pos
        if c in (CMD_CLOSE, CMD_CLOSE_UNTIL_STALL):
            return self._close_pos
        try:
            value = float(c)
            # Legacy prismatic commands (0=closed, ~0.016=open) map to revolute range
            if 0.0 <= value <= 0.05:
                span = self._open_pos - self._close_pos
                return self._close_pos + (value / 0.016) * span
            # Dynamixel goal position (ticks), e.g. 600=closed, 1500=open
            if self._use_dxl and value >= 100.0:
                return self._ticks_to_joint(value)
            return max(self._close_pos, min(self._open_pos, value))
        except ValueError:
            self.get_logger().warning(f'unknown gripper command: {cmd!r}')
            return None

    def _command_to_tcp(self, cmd: str) -> str:
        """Payload for robot TCP: named commands or raw Dynamixel goal ticks."""
        c = cmd.strip().lower()
        if c in (CMD_OPEN, CMD_CLOSE, CMD_CLOSE_UNTIL_STALL):
            if self._use_dxl and c in (CMD_OPEN, CMD_CLOSE):
                tick = self._dxl_open if c == CMD_OPEN else self._dxl_close
                return str(tick)
            return c
        try:
            value = float(c)
            if self._use_dxl and value >= 100.0:
                lo, hi = self._dxl_close, self._dxl_open
                tick = int(max(lo, min(hi, round(value))))
                return str(tick)
        except ValueError:
            pass
        return c

    def _send_forward_command(self, position: float) -> bool:
        if self._cmd_pub is None:
            return False
        deadline = self.get_clock().now().nanoseconds + int(self._wait_sec * 1e9)
        while self._cmd_pub.get_subscription_count() == 0:
            if self.get_clock().now().nanoseconds > deadline:
                self.get_logger().warning(
                    'gripper_controller commands topic has no subscribers — '
                    'is gripper_controller spawned? (relaunch demo_with_gripper)'
                )
                return False
            rclpy.spin_once(self, timeout_sec=0.2)
        msg = Float64MultiArray()
        msg.data = [float(position)]
        self._cmd_pub.publish(msg)
        return True

    def _send_gripper_action(self, position: float) -> bool:
        if self._action_client is None:
            return False
        if not self._action_client.wait_for_server(timeout_sec=self._wait_sec):
            self.get_logger().warning('gripper_controller action server not available')
            return False
        goal = GripperCommand.Goal()
        goal.command.position = float(position)
        goal.command.max_effort = 20.0
        send_future = self._action_client.send_goal_async(goal)
        rclpy.spin_until_future_complete(self, send_future, timeout_sec=self._wait_sec)
        return True

    def _apply_position(self, position: float) -> None:
        ok = False
        if self._use_forward:
            ok = self._send_forward_command(position) or ok
        if self._use_action:
            ok = self._send_gripper_action(position) or ok

    def _on_command(self, msg: String) -> None:
        cmd = msg.data.strip().lower()
        if not cmd:
            return
        position = self._command_to_position(cmd)
        tcp_cmd = self._command_to_tcp(msg.data.strip())
        self.get_logger().info(f'[gripper_bridge] {cmd!r} -> tcp {tcp_cmd!r}')
        self._send_tcp(tcp_cmd)
        if position is not None:
            self._apply_position(position)


def main(args=None) -> None:
    rclpy.init(args=args)
    node = GripperJointBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
