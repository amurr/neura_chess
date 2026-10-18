"""Relay Isaac joint states with velocities from the position change.

Isaac's joint velocities are solver values: a jaw squeezing a chess piece reads 0.07-2.8 rad/s
while its position does not change, so the gripper controller never detects the stall and the
arm controller's stopped-velocity check is noisy. topic_based_ros2_control reads this relay
instead: positions and efforts as published by Isaac, velocity = d(position)/dt, low-passed.
"""

from __future__ import annotations

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

IN_TOPIC = '/isaac_joint_states'
OUT_TOPIC = '/isaac_hw_joint_states'


class IsaacStateVelocity(Node):
    def __init__(self) -> None:
        super().__init__('isaac_state_velocity')
        inn = str(self.declare_parameter('in_topic', IN_TOPIC).value)
        out = str(self.declare_parameter('out_topic', OUT_TOPIC).value)
        # weight of the newest finite difference (1.0 = no filtering)
        self._alpha = float(self.declare_parameter('alpha', 0.5).value)
        self._prev: dict[str, tuple[float, float]] = {}  # name -> (t, position)
        self._vel: dict[str, float] = {}
        self._pub = self.create_publisher(JointState, out, 10)
        self.create_subscription(JointState, inn, self._on_msg, 10)
        self.get_logger().info(f'{inn} -> {out} (velocity from position, alpha={self._alpha})')

    def _stamp(self, msg: JointState) -> float:
        t = msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9
        return t if t > 0.0 else self.get_clock().now().nanoseconds * 1e-9

    def _on_msg(self, msg: JointState) -> None:
        t = self._stamp(msg)
        out = JointState()
        out.header = msg.header
        out.name = list(msg.name)
        out.position = list(msg.position)
        out.effort = list(msg.effort)
        vel = []
        for name, pos in zip(msg.name, msg.position):
            prev = self._prev.get(name)
            v = self._vel.get(name, 0.0)
            if prev is not None and t > prev[0]:
                v += self._alpha * ((pos - prev[1]) / (t - prev[0]) - v)
            if prev is None or t > prev[0]:
                self._prev[name] = (t, pos)
            self._vel[name] = v
            vel.append(v)
        out.velocity = vel
        self._pub.publish(out)


def main() -> None:
    rclpy.init()
    node = IsaacStateVelocity()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
