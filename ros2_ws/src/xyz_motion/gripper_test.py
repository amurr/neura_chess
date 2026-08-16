"""Gripper tests via /command_gripper (requires gripper_node + robot_gripper on :5000).

For close_until_object(), deploy src/xyz_motion/robot_gripper_server.py to the robot as
/home/hrg/Robotum/robot_gripper.py and restart the gripper bridge.
"""
import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

CMD_OPEN = "open"
CMD_CLOSE = "close"
CMD_CLOSE_UNTIL_STALL = "close_until_stall"


def send_gripper(pub, cmd: str) -> None:
    pub.publish(String(data=cmd))


def open_gripper(pub, node, wait_sec: float = 1.0) -> None:
    send_gripper(pub, CMD_OPEN)
    rclpy.spin_once(node, timeout_sec=wait_sec)


def close_gripper(pub, node, wait_sec: float = 1.0) -> None:
    send_gripper(pub, CMD_CLOSE)
    rclpy.spin_once(node, timeout_sec=wait_sec)


def close_until_object(pub, node, wait_sec: float = 15.0) -> None:
    """Close until the fingers stall on an object (unknown width).

    Sends close_until_stall to the robot TCP server, which steps the servo closed
    and stops when load rises or position stops changing.
    """
    send_gripper(pub, CMD_CLOSE_UNTIL_STALL)
    rclpy.spin_once(node, timeout_sec=wait_sec)


def main():
    rclpy.init()
    node = Node("grip_test")
    pub = node.create_publisher(String, "command_gripper", 10)
    rclpy.spin_once(node, timeout_sec=0.5)

    open_gripper(pub, node)
    time.sleep(0.3)
    close_until_object(pub, node)
    # hold grasp; add arm motion here before opening
    time.sleep(1.0)
    open_gripper(pub, node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
