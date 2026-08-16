"""Attach/detach chess pieces to the gripper in the MoveIt planning scene."""

from __future__ import annotations

from typing import Sequence

from geometry_msgs.msg import Pose
from moveit_msgs.msg import AttachedCollisionObject, CollisionObject, PlanningScene
from rclpy.node import Node
from rclpy.publisher import Publisher

from xyz_motion.chess_scene import (
    _occupancy_piece_types,
    piece_collision_height,
    piece_collision_object,
    piece_dimensions,
    piece_object_id,
    piece_removal_object,
)
from xyz_motion.chess_xyz import chess_occupancy_to_pose6


class GripperPlanningScene:
    """Publish planning-scene updates to attach chess pieces to lara5_gripper."""

    def __init__(
        self,
        node: Node,
        *,
        planning_scene_topic: str = '/planning_scene',
        planning_frame: str = 'world',
        ee_link: str = 'lara5_gripper',
        grasp_offset_xyz: Sequence[float] = (0.0, -0.052, 0.0),
        piece_diameter: float = 0.035,
        piece_height: float = 0.05,
        mesh_library=None,
    ) -> None:
        self._node = node
        self._frame = planning_frame
        self._ee_link = ee_link
        self._grasp_offset = [float(v) for v in grasp_offset_xyz]
        self._piece_diameter = float(piece_diameter)
        self._piece_height = float(piece_height)
        self._mesh_library = mesh_library
        self._pub: Publisher = node.create_publisher(PlanningScene, planning_scene_topic, 10)
        self._attached_square: str | None = None

    def _piece_height(self, piece_type: str) -> float:
        return piece_collision_height(
            piece_type,
            mesh_library=self._mesh_library,
            default_diameter=self._piece_diameter,
            default_height=self._piece_height,
        )

    def _attach_pose(self, piece_type: str) -> Pose:
        height = self._piece_height(piece_type)
        pose = Pose()
        pose.position.x = self._grasp_offset[0]
        pose.position.y = self._grasp_offset[1]
        if self._mesh_library is not None:
            pose.position.z = self._grasp_offset[2]
        else:
            pose.position.z = self._grasp_offset[2] + float(height) / 2.0
        pose.orientation.w = 1.0
        return pose

    def attach_piece_from_occupancy(self, square: str, occ: dict) -> None:
        """Remove world piece and attach to the end-effector."""
        square = square.strip().lower()
        poses = chess_occupancy_to_pose6(occ)
        if square not in poses:
            self._node.get_logger().warning(
                f'[attach] no XYZ for square {square!r} in occupancy'
            )
            return
        types = _occupancy_piece_types(occ)
        piece_type = types.get(square, 'pawn')
        diameter, height = piece_dimensions(
            piece_type,
            default_diameter=self._piece_diameter,
            default_height=self._piece_height,
        )
        world_piece = piece_collision_object(
            square,
            poses[square][:3],
            frame_id=self._frame,
            piece_type=piece_type,
            diameter=diameter,
            height=height,
            mesh_library=self._mesh_library,
        )
        attached = AttachedCollisionObject()
        attached.link_name = self._ee_link
        attached.touch_links = [
            self._ee_link,
            'lara5_gripper_body',
            'lara5_gripper_jaw',
            'lara5_gripper_adapter',
        ]
        attached.object = world_piece
        attached.object.header.frame_id = self._ee_link
        attached.object.operation = CollisionObject.ADD
        attach_pose = self._attach_pose(piece_type)
        if self._mesh_library is not None:
            attached.object.mesh_poses = [attach_pose]
            attached.object.primitives = []
            attached.object.primitive_poses = []
        else:
            attached.object.primitive_poses = [attach_pose]

        scene = PlanningScene()
        scene.is_diff = True
        scene.robot_state.is_diff = True
        scene.world.collision_objects.append(piece_removal_object(square, frame_id=self._frame))
        scene.robot_state.attached_collision_objects.append(attached)
        self._pub.publish(scene)
        self._attached_square = square
        self._node.get_logger().info(f'[attach] piece {piece_object_id(square)} -> {self._ee_link}')

    def detach_piece_to_square(self, square: str, occ: dict) -> None:
        """Detach from gripper and place piece at square XYZ in the world scene."""
        square = square.strip().lower()
        poses = chess_occupancy_to_pose6(occ)
        if square not in poses:
            self._node.get_logger().warning(
                f'[detach] no XYZ for square {square!r} in occupancy'
            )
            return
        types = _occupancy_piece_types(occ)
        piece_type = types.get(square, 'pawn')
        diameter, height = piece_dimensions(
            piece_type,
            default_diameter=self._piece_diameter,
            default_height=self._piece_height,
        )

        detach = AttachedCollisionObject()
        detach.link_name = self._ee_link
        detach.object.id = piece_object_id(self._attached_square or square)
        detach.object.operation = CollisionObject.REMOVE

        world_piece = piece_collision_object(
            square,
            poses[square][:3],
            frame_id=self._frame,
            piece_type=piece_type,
            diameter=diameter,
            height=height,
            mesh_library=self._mesh_library,
        )

        scene = PlanningScene()
        scene.is_diff = True
        scene.robot_state.is_diff = True
        scene.robot_state.attached_collision_objects.append(detach)
        scene.world.collision_objects.append(world_piece)
        self._pub.publish(scene)
        self._attached_square = None
        self._node.get_logger().info(f'[detach] piece -> world at {square!r}')
