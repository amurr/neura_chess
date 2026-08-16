#!/usr/bin/env python3
"""Mock move_joints service for testing without a real robot."""

import rclpy
from lara_interfaces.srv import MoveJoints
from rclpy.node import Node


class MockMoveJoints(Node):
    def __init__(self):
        super().__init__('mock_move_joints')
        self.last_target_pose: list[float] = []
        self.last_target_joint: list[float] = []
        self.calls = 0
        self.create_service(MoveJoints, 'move_joints', self.cb)
        self.get_logger().info('mock move_joints ready')

    def cb(self, request, response):
        self.calls += 1
        self.last_target_pose = list(getattr(request, 'target_pose', []))
        self.last_target_joint = list(request.target_joint)
        response.success = True
        response.message = 'mock OK (no robot)'
        if len(self.last_target_pose) == 6:
            self.get_logger().info(f'mock move pose6={self.last_target_pose}')
        else:
            self.get_logger().info(f'mock move joints={self.last_target_joint}')
        return response


def main(args=None):
    rclpy.init(args=args)
    node = MockMoveJoints()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
