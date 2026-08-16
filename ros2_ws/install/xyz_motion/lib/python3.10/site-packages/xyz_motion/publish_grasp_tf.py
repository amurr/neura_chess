#!/usr/bin/env python3
"""Broadcast perpendicular chess grasp / hover TF frames.

MTC looks up ``grasp/<square>`` and ``hover/<square>``. Occupancy supplies
detected piece Z (and XY); board calibration supplies the surface normal.
"""

from __future__ import annotations

import json
from pathlib import Path

import rclpy
from geometry_msgs.msg import TransformStamped
from rclpy.node import Node
from std_msgs.msg import String
from tf2_ros import TransformBroadcaster, StaticTransformBroadcaster

from xyz_motion.board_calibration import compute_board_calibration
from xyz_motion.chess_scene import board_surface_z, normalize_board_layout
from xyz_motion.chess_xyz import CHESS_OCCUPANCY_TOPIC
from xyz_motion.grasp_poses import (
    SquareGrasp,
    board_origin_pose,
    build_board_grasps,
    frame_name,
)


def _as_float_list(value, expected: int) -> list[float]:
    out = [float(v) for v in value]
    if len(out) != expected:
        raise ValueError(f'expected {expected} values, got {len(out)}')
    return out


def _stamp_tf(
    stamp,
    parent: str,
    child: str,
    xyz: tuple[float, float, float] | list[float],
    quat_xyzw: tuple[float, float, float, float],
) -> TransformStamped:
    msg = TransformStamped()
    msg.header.stamp = stamp
    msg.header.frame_id = parent
    msg.child_frame_id = child
    msg.transform.translation.x = float(xyz[0])
    msg.transform.translation.y = float(xyz[1])
    msg.transform.translation.z = float(xyz[2])
    msg.transform.rotation.x = float(quat_xyzw[0])
    msg.transform.rotation.y = float(quat_xyzw[1])
    msg.transform.rotation.z = float(quat_xyzw[2])
    msg.transform.rotation.w = float(quat_xyzw[3])
    return msg


class GraspTfPublisher(Node):
    def __init__(self) -> None:
        super().__init__('publish_grasp_tf')

        self.declare_parameter('planning_frame', 'world')
        self.declare_parameter('board_frame', 'board')
        self.declare_parameter('square_frame_prefix', 'square')
        self.declare_parameter('grasp_frame_prefix', 'grasp')
        self.declare_parameter('hover_frame_prefix', 'hover')
        self.declare_parameter('board_a1', [0.27, -0.16, 0.02])
        self.declare_parameter('board_b1', [0.31, -0.16, 0.02])
        self.declare_parameter('board_a2', [0.27, -0.12, 0.02])
        self.declare_parameter('square_size', 0.04)
        self.declare_parameter('board_thickness', 0.02)
        self.declare_parameter('board_layout', 'ranks_x_files_y')
        self.declare_parameter('board_file_mirror', True)
        self.declare_parameter('chess_occupancy_topic', CHESS_OCCUPANCY_TOPIC)
        self.declare_parameter('occupancy_file', '')
        self.declare_parameter('approach_m', 0.08)
        self.declare_parameter('grasp_clearance_m', 0.015)
        self.declare_parameter('gripper_z_offset_m', 0.0)
        self.declare_parameter('z_is_piece_top', False)
        self.declare_parameter('grasp_yaw_rad', 0.0)
        self.declare_parameter('publish_rate_hz', 20.0)
        self.declare_parameter('broadcast_all_squares', True)
        self.declare_parameter('piece_dims.pawn', [0.018, 0.034])
        self.declare_parameter('piece_dims.bishop', [0.022, 0.047])
        self.declare_parameter('piece_dims.knight', [0.024, 0.049])
        self.declare_parameter('piece_dims.rook', [0.026, 0.044])
        self.declare_parameter('piece_dims.queen', [0.027, 0.058])
        self.declare_parameter('piece_dims.king', [0.029, 0.066])

        self._world = str(self.get_parameter('planning_frame').value)
        self._board_frame = str(self.get_parameter('board_frame').value)
        self._square_prefix = str(self.get_parameter('square_frame_prefix').value)
        self._grasp_prefix = str(self.get_parameter('grasp_frame_prefix').value)
        self._hover_prefix = str(self.get_parameter('hover_frame_prefix').value)
        self._square_size = float(self.get_parameter('square_size').value)
        self._layout = normalize_board_layout(str(self.get_parameter('board_layout').value))
        self._file_mirror = bool(self.get_parameter('board_file_mirror').value)
        self._approach_m = float(self.get_parameter('approach_m').value)
        self._clearance = float(self.get_parameter('grasp_clearance_m').value)
        self._gripper_z_offset = float(self.get_parameter('gripper_z_offset_m').value)
        self._z_is_piece_top = bool(self.get_parameter('z_is_piece_top').value)
        self._yaw = float(self.get_parameter('grasp_yaw_rad').value)
        self._broadcast_all = bool(self.get_parameter('broadcast_all_squares').value)
        thickness = float(self.get_parameter('board_thickness').value)
        self._surface_z_board = board_surface_z(thickness)

        self._calib = compute_board_calibration(
            _as_float_list(self.get_parameter('board_a1').value, 3),
            _as_float_list(self.get_parameter('board_b1').value, 3),
            _as_float_list(self.get_parameter('board_a2').value, 3),
            square_size=self._square_size,
        )
        self._piece_dims = {
            'pawn': _as_float_list(self.get_parameter('piece_dims.pawn').value, 2),
            'bishop': _as_float_list(self.get_parameter('piece_dims.bishop').value, 2),
            'knight': _as_float_list(self.get_parameter('piece_dims.knight').value, 2),
            'rook': _as_float_list(self.get_parameter('piece_dims.rook').value, 2),
            'queen': _as_float_list(self.get_parameter('piece_dims.queen').value, 2),
            'king': _as_float_list(self.get_parameter('piece_dims.king').value, 2),
        }

        self._occupancy: dict = {}
        occ_file = str(self.get_parameter('occupancy_file').value).strip()
        if occ_file:
            self._occupancy = json.loads(Path(occ_file).read_text(encoding='utf-8'))
            self.get_logger().info(f'loaded occupancy file {occ_file}')

        occ_topic = str(self.get_parameter('chess_occupancy_topic').value)
        self.create_subscription(String, occ_topic, self._on_occupancy, 10)

        self._tf = TransformBroadcaster(self)
        self._static_tf = StaticTransformBroadcaster(self)
        self._grasps: dict[str, SquareGrasp] = {}
        self._rebuild()
        self._publish_static_board()

        rate = float(self.get_parameter('publish_rate_hz').value)
        period = 1.0 / max(rate, 1.0)
        self.create_timer(period, self._on_timer)
        self.get_logger().info(
            f'grasp TF ready frame={self._world}->{self._board_frame} '
            f'normal=({self._calib.z_axis[0]:.3f},{self._calib.z_axis[1]:.3f},{self._calib.z_axis[2]:.3f}) '
            f'z_is_piece_top={self._z_is_piece_top} squares={len(self._grasps)}'
        )

    def _on_occupancy(self, msg: String) -> None:
        try:
            data = json.loads(msg.data)
        except json.JSONDecodeError as exc:
            self.get_logger().error(f'occupancy JSON invalid: {exc}')
            return
        if not isinstance(data, dict):
            self.get_logger().error('occupancy JSON must be an object')
            return
        self._occupancy = data
        self._rebuild()

    def _rebuild(self) -> None:
        squares = None if self._broadcast_all else None
        self._grasps = build_board_grasps(
            self._calib,
            square_size=self._square_size,
            surface_z_board=self._surface_z_board,
            approach_m=self._approach_m,
            occupancy=self._occupancy,
            grasp_clearance=self._clearance,
            gripper_z_offset=self._gripper_z_offset,
            z_is_piece_top=self._z_is_piece_top,
            board_layout=self._layout,
            file_mirror=self._file_mirror,
            piece_dims=self._piece_dims,
            yaw_about_approach=self._yaw,
            squares=squares,
        )

    def _publish_static_board(self) -> None:
        xyz, quat = board_origin_pose(self._calib)
        stamp = self.get_clock().now().to_msg()
        self._static_tf.sendTransform(
            [_stamp_tf(stamp, self._world, self._board_frame, xyz, quat)]
        )

    def _on_timer(self) -> None:
        stamp = self.get_clock().now().to_msg()
        msgs: list[TransformStamped] = []
        identity = (0.0, 0.0, 0.0, 1.0)
        for grasp in self._grasps.values():
            sq_child = frame_name(self._square_prefix, grasp.square)
            grasp_child = frame_name(self._grasp_prefix, grasp.square)
            hover_child = frame_name(self._hover_prefix, grasp.square)
            msgs.append(_stamp_tf(stamp, self._world, sq_child, grasp.square_xyz, identity))
            msgs.append(_stamp_tf(stamp, self._world, grasp_child, grasp.grasp_xyz, grasp.orientation_xyzw))
            msgs.append(_stamp_tf(stamp, self._world, hover_child, grasp.hover_xyz, grasp.orientation_xyzw))
        if msgs:
            self._tf.sendTransform(msgs)


def main(args=None) -> None:
    rclpy.init(args=args)
    node = GraspTfPublisher()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
