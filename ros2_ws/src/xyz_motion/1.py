import rclpy
from rclpy.node import Node
from lara_interfaces.srv import MoveJoints

from xyz_motion.poses import POSES


def main():
    rclpy.init()
    node = Node('move_once')

    client = node.create_client(MoveJoints, 'move_joints')
    if not client.wait_for_service(timeout_sec=15.0):
        node.get_logger().error(
            'No move_joints — start bringup in another shell, then run: '
            'bash /ros2_ws/src/xyz_motion/run.sh 1.py'
        )
        return

    req = MoveJoints.Request()
    req.point_name = ""
    req.target_joint = list(POSES["stand"])  # A1..A6 degrees
    req.speed = 20.0
    req.acceleration = 20.0
    req.enable_safety = True

    future = client.call_async(req)
    rclpy.spin_until_future_complete(node, future)
    result = future.result()
    print('success:', result.success, 'message:', result.message)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()