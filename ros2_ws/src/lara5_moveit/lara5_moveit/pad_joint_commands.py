"""Pad JointState so Isaac ROS2SubscribeJointState.checkValid() accepts it.

topic_based_ros2_control publishes positions only. Isaac requires name, position,
velocity, and effort to be the same length. Pad omitted velocity/effort with NaN
so ArticulationController leaves those targets unchanged (zeros would freeze the arm).
"""

from __future__ import annotations

import math

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

NAN = math.nan
IN_TOPIC = '/isaac_hw_joint_commands'
OUT_TOPIC = '/isaac_joint_commands'


def pad_joint_state(msg: JointState) -> JointState:
    """Copy positions; fill velocity/effort to len(name) with NaN when omitted."""
    n = len(msg.name)
    out = JointState()
    out.header = msg.header
    out.name = list(msg.name)
    pos = list(msg.position[:n])
    if len(pos) < n:
        pos.extend([0.0] * (n - len(pos)))
    out.position = pos
    vel = list(msg.velocity)
    eff = list(msg.effort)
    out.velocity = vel if len(vel) == n else [NAN] * n
    out.effort = eff if len(eff) == n else [NAN] * n
    return out


class PadJointCommands(Node):
    """Relay hardware JointState onto the Isaac command topic with padded arrays."""

    def __init__(self) -> None:
        super().__init__('isaac_joint_command_pad')
        inn = str(self.declare_parameter('in_topic', IN_TOPIC).value)
        out = str(self.declare_parameter('out_topic', OUT_TOPIC).value)
        self._pub = self.create_publisher(JointState, out, 10)
        self.create_subscription(JointState, inn, self._on_msg, 10)
        self.get_logger().info(f'pad {inn} → {out} (NaN velocity/effort)')

    def _on_msg(self, msg: JointState) -> None:
        self._pub.publish(pad_joint_state(msg))


def main() -> None:
    """Spin the JointState pad relay."""
    rclpy.init()
    node = PadJointCommands()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
