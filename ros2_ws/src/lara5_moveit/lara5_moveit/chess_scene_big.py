#!/usr/bin/env python3
"""Same planning-scene chess set as chess_scene_collisions, but the largest 8x8
that still has perpendicular hover IK on all 64 squares (board_ik DLS sweep).

  square 7.2 cm, board 57.6 cm, a1 at (0.15, -0.16, 0.02) in front of the base.
"""

import rclpy
from rclpy.parameter import Parameter

from lara5_moveit.chess_scene_collisions import ChessSceneCollisions

S = 0.072
A1 = [0.15, -0.16, 0.02]


def main(args=None) -> None:
    rclpy.init(args=args)
    node = ChessSceneCollisions(
        parameter_overrides=[
            Parameter('square_size', Parameter.Type.DOUBLE, S),
            Parameter('board_a1', Parameter.Type.DOUBLE_ARRAY, A1),
            Parameter('board_b1', Parameter.Type.DOUBLE_ARRAY, [A1[0] + S, A1[1], A1[2]]),
            Parameter('board_a2', Parameter.Type.DOUBLE_ARRAY, [A1[0], A1[1] + S, A1[2]]),
        ]
    )
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    if rclpy.ok():
        rclpy.shutdown()


if __name__ == '__main__':
    main()
