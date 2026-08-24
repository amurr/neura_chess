"""Republish Isaac joint states for MoveIt with wall-clock stamps.

Isaac ROS2PublishJointState stamps with simulation time (tens of seconds).
MoveIt CurrentStateMonitor uses wall time when use_sim_time is false, so a
sim-time stamp looks hours stale and execution aborts with
'couldn't receive full current joint state within 1s'.
"""

from __future__ import annotations

import rclpy
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, HistoryPolicy, QoSProfile, ReliabilityPolicy
from sensor_msgs.msg import JointState

IN_TOPIC = '/isaac_joint_states'
OUT_TOPIC = '/joint_states'


def wall_stamp_joint_state(msg: JointState, stamp) -> JointState:
    """Copy ``msg`` and replace the header stamp (MoveIt needs a current clock)."""
    out = JointState()
    out.header.stamp = stamp
    out.header.frame_id = msg.header.frame_id
    out.name = list(msg.name)
    out.position = list(msg.position)
    out.velocity = list(msg.velocity)
    out.effort = list(msg.effort)
    return out


class RelayIsaacJointStates(Node):
    """Relay /isaac_joint_states onto /joint_states with Node.get_clock() stamps."""

    def __init__(self) -> None:
        super().__init__('isaac_joint_state_relay')
        inn = str(self.declare_parameter('in_topic', IN_TOPIC).value)
        out = str(self.declare_parameter('out_topic', OUT_TOPIC).value)
        sensor_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.VOLATILE,
            history=HistoryPolicy.KEEP_LAST,
            depth=5,
        )
        isaac_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.VOLATILE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10,
        )
        self._pub = self.create_publisher(JointState, out, sensor_qos)
        self.create_subscription(JointState, inn, self._on_msg, isaac_qos)
        self.get_logger().info(f'relay {inn} → {out} (wall-clock stamp)')

    def _on_msg(self, msg: JointState) -> None:
        self._pub.publish(wall_stamp_joint_state(msg, self.get_clock().now().to_msg()))


def main() -> None:
    """Spin the Isaac joint-state relay."""
    rclpy.init()
    node = RelayIsaacJointStates()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
