#!/usr/bin/env python3
"""Publish static chess board and dynamic piece collision objects to MoveIt planning scene."""

from __future__ import annotations

import json
import time

import rclpy
from moveit_msgs.msg import PlanningScene
from rcl_interfaces.msg import ParameterDescriptor
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, QoSProfile
from std_msgs.msg import String
from std_srvs.srv import Trigger
from visualization_msgs.msg import MarkerArray

from xyz_motion.chess_piece_meshes import PieceMeshLibrary
from xyz_motion.chess_scene import (
    PieceState,
    board_collision_squares,
    build_board_marker_array,
    build_full_piece_snapshot_objects,
    build_piece_collision_objects,
    build_piece_marker_array,
    build_piece_scene_diff,
    build_standard_start_pieces,
    board_surface_z,
    should_rebuild_piece_snapshot,
    strip_move_source_from_active,
    normalize_board_layout,
    extract_pieces_from_occupancy,
    legacy_board_removal,
    load_board_calibration,
    make_planning_scene_diff,
)
from xyz_motion.chess_xyz import CHESS_OCCUPANCY_TOPIC


class ChessSceneNode(Node):
    def __init__(self) -> None:
        super().__init__('chess_scene')

        self.declare_parameter('planning_scene_topic', '/planning_scene')
        self.declare_parameter('planning_frame', 'world')
        self.declare_parameter('chess_occupancy_topic', CHESS_OCCUPANCY_TOPIC)
        self.declare_parameter('square_size', 0.04)
        self.declare_parameter('board_thickness', 0.02)
        self.declare_parameter('piece_diameter', 0.035)
        self.declare_parameter('piece_height', 0.05)
        self.declare_parameter('initial_piece_z', 0.0)
        self.declare_parameter('publish_board_on_startup', True)
        self.declare_parameter('publish_initial_pieces', True)
        self.declare_parameter('publish_board_markers', True)
        self.declare_parameter('board_markers_topic', '/chess_board_markers')
        self.declare_parameter('publish_piece_markers', True)
        self.declare_parameter('piece_markers_topic', '/chess_piece_markers')
        self.declare_parameter('board_markers_republish_hz', 1.0)
        self.declare_parameter('board_layout', 'ranks_x_files_y')
        self.declare_parameter('board_file_mirror', True)
        self.declare_parameter('allow_empty_occupancy', False)
        self.declare_parameter('planning_scene_batch_size', 8)
        self.declare_parameter('full_snapshot_min_squares', 16)
        self.declare_parameter('use_convex_hull_collision', True)

        self.declare_parameter('board_a1', [0.0, 0.0, 0.0])
        self.declare_parameter('board_b1', [0.04, 0.0, 0.0])
        self.declare_parameter('board_a2', [0.0, 0.04, 0.0])

        scene_topic = str(self.get_parameter('planning_scene_topic').value)
        occ_topic = str(self.get_parameter('chess_occupancy_topic').value)
        self._frame_id = str(self.get_parameter('planning_frame').value)
        self._square_size = float(self.get_parameter('square_size').value)
        self._board_thickness = float(self.get_parameter('board_thickness').value)
        self._default_diameter = float(self.get_parameter('piece_diameter').value)
        self._default_height = float(self.get_parameter('piece_height').value)
        self._initial_piece_z = float(self.get_parameter('initial_piece_z').value)
        if self._initial_piece_z <= 0.0:
            self._initial_piece_z = board_surface_z(self._board_thickness)
        self._dimension_overrides = self._load_dimension_overrides()
        self._board_layout = normalize_board_layout(
            str(self.get_parameter('board_layout').value)
        )
        self._file_mirror = bool(self.get_parameter('board_file_mirror').value)

        a1 = [float(v) for v in self.get_parameter('board_a1').value]
        b1 = [float(v) for v in self.get_parameter('board_b1').value]
        a2 = [float(v) for v in self.get_parameter('board_a2').value]
        self._board_calib = load_board_calibration(a1, b1, a2, self._square_size)
        self._mesh_library = self._load_mesh_library()
        self._visual_markers_enabled = (
            bool(self.get_parameter('publish_board_markers').value)
            or bool(self.get_parameter('publish_piece_markers').value)
        )

        self._scene_pub = self.create_publisher(PlanningScene, scene_topic, 10)
        self._active_pieces: dict[str, PieceState] = {}
        marker_qos = QoSProfile(
            depth=1,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
        )
        self._board_markers_pub = None
        if bool(self.get_parameter('publish_board_markers').value):
            marker_topic = str(self.get_parameter('board_markers_topic').value)
            self._board_markers_pub = self.create_publisher(
                MarkerArray, marker_topic, marker_qos
            )
        self._piece_markers_pub = None
        if bool(self.get_parameter('publish_piece_markers').value):
            piece_topic = str(self.get_parameter('piece_markers_topic').value)
            self._piece_markers_pub = self.create_publisher(
                MarkerArray, piece_topic, marker_qos
            )

        if bool(self.get_parameter('publish_board_on_startup').value):
            self._publish_board()

        if bool(self.get_parameter('publish_initial_pieces').value):
            self._publish_initial_pieces()

        republish_hz = float(self.get_parameter('board_markers_republish_hz').value)
        if republish_hz > 0.0 and (
            self._board_markers_pub is not None or self._piece_markers_pub is not None
        ):
            period = 1.0 / republish_hz
            self.create_timer(period, self._republish_visual_markers)

        self.create_subscription(String, occ_topic, self._on_chess_occupancy, 10)
        self.create_service(Trigger, '~/reset_scene', self._reset_scene)
        self._startup_republish_done = False
        self._startup_timer = self.create_timer(2.0, self._startup_republish_scene)
        self.get_logger().info(
            f'chess_scene ready frame={self._frame_id!r} topic={scene_topic!r} '
            f'occupancy={occ_topic!r} reset=~/reset_scene '
            f'collision={"convex_hull" if self._mesh_library else "cylinder"} '
            f'markers={"on" if self._visual_markers_enabled else "off (planning scene only)"}'
        )

    def _load_mesh_library(self) -> PieceMeshLibrary | None:
        if not bool(self.get_parameter('use_convex_hull_collision').value):
            return None
        library = PieceMeshLibrary()
        if library.available():
            self.get_logger().info(f'convex hull meshes from {library.mesh_dir}')
            return library
        self.get_logger().warning(
            f'use_convex_hull_collision enabled but meshes missing in {library.mesh_dir}; '
            'falling back to cylinder collision'
        )
        return None

    def _load_dimension_overrides(self) -> dict[str, list[float]]:
        self.declare_parameter(
            'piece_dims',
            descriptor=ParameterDescriptor(dynamic_typing=True),
        )
        overrides: dict[str, list[float]] = {}
        raw = self.get_parameter('piece_dims').value
        if isinstance(raw, dict):
            for ptype, vals in raw.items():
                if isinstance(vals, (list, tuple)) and len(vals) >= 2:
                    overrides[str(ptype)] = [float(vals[0]), float(vals[1])]
        return overrides

    def _piece_build_kwargs(self) -> dict:
        return {
            'frame_id': self._frame_id,
            'dimension_overrides': self._dimension_overrides or None,
            'default_diameter': self._default_diameter,
            'default_height': self._default_height,
            'mesh_library': self._mesh_library,
            'calib': self._board_calib,
            'board_layout': self._board_layout,
        }

    def _publish_scene_diff(self, objects) -> None:
        obj_list = list(objects)
        if not obj_list:
            return
        batch_size = int(self.get_parameter('planning_scene_batch_size').value)
        if batch_size <= 0:
            batch_size = len(obj_list)
        for start in range(0, len(obj_list), batch_size):
            chunk = obj_list[start : start + batch_size]
            self._scene_pub.publish(make_planning_scene_diff(chunk))
            if start + batch_size < len(obj_list):
                time.sleep(0.02)

    def _marker_stamp(self):
        return self.get_clock().now().to_msg()

    def _board_marker_array(self) -> MarkerArray:
        return build_board_marker_array(
            self._board_calib,
            frame_id=self._frame_id,
            square_size=self._square_size,
            thickness=self._board_thickness,
            board_layout=self._board_layout,
            file_mirror=self._file_mirror,
            stamp=self._marker_stamp(),
        )

    def _piece_marker_array(self) -> MarkerArray:
        return build_piece_marker_array(
            self._active_pieces,
            frame_id=self._frame_id,
            dimension_overrides=self._dimension_overrides or None,
            default_diameter=self._default_diameter,
            default_height=self._default_height,
            stamp=self._marker_stamp(),
            mesh_library=self._mesh_library,
            calib=self._board_calib,
            board_layout=self._board_layout,
        )

    def _publish_visual_markers(self) -> None:
        if self._board_markers_pub is not None:
            self._board_markers_pub.publish(self._board_marker_array())
        if self._piece_markers_pub is not None:
            self._piece_markers_pub.publish(self._piece_marker_array())

    def _republish_visual_markers(self) -> None:
        self._publish_visual_markers()

    def _publish_board(self) -> None:
        objects = [legacy_board_removal(self._frame_id)]
        objects.extend(
            board_collision_squares(
                self._board_calib,
                frame_id=self._frame_id,
                square_size=self._square_size,
                thickness=self._board_thickness,
                board_layout=self._board_layout,
                file_mirror=self._file_mirror,
            )
        )
        self._publish_scene_diff(objects)
        if self._visual_markers_enabled:
            self._publish_visual_markers()
        self.get_logger().info(
            'published 8x8 chess board (64 collision squares'
            + (' + colored RViz markers)' if self._visual_markers_enabled else ')')
        )

    def _publish_initial_pieces(self) -> None:
        pieces = build_standard_start_pieces(
            self._board_calib,
            square_size=self._square_size,
            piece_z=self._initial_piece_z,
            board_thickness=self._board_thickness,
            board_layout=self._board_layout,
            file_mirror=self._file_mirror,
        )
        objects = build_piece_collision_objects(pieces, **self._piece_build_kwargs())
        self._publish_scene_diff(objects)
        self._active_pieces = pieces
        if self._visual_markers_enabled:
            self._publish_visual_markers()
        type_counts: dict[str, int] = {}
        for piece in pieces.values():
            type_counts[piece.piece_type] = type_counts.get(piece.piece_type, 0) + 1
        self.get_logger().info(
            f'published initial pieces: {len(pieces)} total {type_counts}'
        )

    def _on_chess_occupancy(self, msg: String) -> None:
        try:
            data = json.loads(msg.data)
            if not isinstance(data, dict):
                self.get_logger().error('chess_occupancy JSON must be an object')
                return
        except json.JSONDecodeError as exc:
            self.get_logger().error(f'chess_occupancy bad JSON: {exc}')
            return

        try:
            active = extract_pieces_from_occupancy(data)
        except (TypeError, ValueError) as exc:
            self.get_logger().error(f'chess_occupancy parse failed: {exc}')
            return

        strip_move_source_from_active(data, active)

        if not active and not self._active_pieces:
            return

        if not active and self._active_pieces:
            if not bool(self.get_parameter('allow_empty_occupancy').value):
                self.get_logger().warning(
                    'chess_occupancy has no squares — ignored (would remove all '
                    f'{len(self._active_pieces)} pieces). Set allow_empty_occupancy '
                    'true to clear, or restart chess_scene to restore initial layout.'
                )
                return

        kwargs = self._piece_build_kwargs()
        prev = dict(self._active_pieces)
        min_full = int(self.get_parameter('full_snapshot_min_squares').value)
        if should_rebuild_piece_snapshot(active, prev, full_snapshot_min_squares=min_full):
            objects = build_full_piece_snapshot_objects(active, prev, **kwargs)
            self._active_pieces = dict(active)
            mode = 'full snapshot'
        else:
            objects, self._active_pieces = build_piece_scene_diff(active, prev, **kwargs)
            mode = 'diff'

        self._publish_scene_diff(objects)
        if self._visual_markers_enabled:
            self._publish_visual_markers()
        self.get_logger().info(
            f'planning scene pieces updated ({mode}): {len(self._active_pieces)} active, '
            f'layout={self._board_layout}'
        )

    def _startup_republish_scene(self) -> None:
        if self._startup_republish_done:
            return
        self._startup_republish_done = True
        try:
            self._startup_timer.cancel()
        except Exception:
            pass
        self._reset_scene(None, Trigger.Response())

    def _reset_scene(self, _request, response):
        """Re-publish board + standard 32-piece start (recovery)."""
        if bool(self.get_parameter('publish_board_on_startup').value):
            self._publish_board()
        if bool(self.get_parameter('publish_initial_pieces').value):
            self._publish_initial_pieces()
        else:
            if self._visual_markers_enabled:
                self._publish_visual_markers()
        response.success = True
        response.message = (
            f'Republished board and {len(self._active_pieces)} pieces '
            f'(layout={self._board_layout})'
        )
        self.get_logger().info(response.message)
        return response


def main(args=None) -> None:
    rclpy.init(args=args)
    node = ChessSceneNode()
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
