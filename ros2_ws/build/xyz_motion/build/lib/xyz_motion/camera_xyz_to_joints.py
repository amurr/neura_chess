#!/usr/bin/env python3
"""
Camera-frame object XYZ -> base-frame TCP pose -> MoveIt IK -> joint solution.

Subscribes to geometry_msgs/PointStamped (metres). Transforms the point into the
robot base frame via TF2, attaches a fixed tool orientation, calls MoveIt
GetPositionIK, and publishes the joint solution.

Requires (separate terminals / launch):
  - robot_state_publisher + joint_states (or MoveIt demo)
  - TF: camera_frame -> base_frame (unless assume_base_frame is true)
  - move_group with /compute_ik (ros2 launch lara5_moveit_config move_group.launch.py)
"""

from __future__ import annotations

import math
import time
from typing import Sequence

import rclpy
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from geometry_msgs.msg import PointStamped, PoseStamped
from moveit_msgs.msg import MoveItErrorCodes, PositionIKRequest, RobotState
from moveit_msgs.srv import GetPositionIK
from rclpy.duration import Duration
from rclpy.node import Node
from rclpy.time import Time
from sensor_msgs.msg import JointState
from tf2_geometry_msgs import do_transform_point
from tf2_ros import Buffer, TransformException, TransformListener

from xyz_motion.poses import DEFAULT_VIEW_RPY

_LARA5_JOINTS = [f'lara5_joint{i}' for i in range(1, 7)]


def _rpy_to_quaternion(roll: float, pitch: float, yaw: float) -> tuple[float, float, float, float]:
    cr, sr = math.cos(roll * 0.5), math.sin(roll * 0.5)
    cp, sp = math.cos(pitch * 0.5), math.sin(pitch * 0.5)
    cy, sy = math.cos(yaw * 0.5), math.sin(yaw * 0.5)
    qw = cr * cp * cy + sr * sp * sy
    qx = sr * cp * cy - cr * sp * sy
    qy = cr * sp * cy + sr * cp * sy
    qz = cr * cp * sy - sr * sp * cy
    return qx, qy, qz, qw


class CameraXyzToJointsNode(Node):
    def __init__(self) -> None:
        super().__init__('camera_xyz_to_joints')

        self.declare_parameter('object_xyz_topic', '/object_xyz')
        self.declare_parameter('base_frame', 'lara5_link0')
        self.declare_parameter('camera_frame', 'camera_optical_frame')
        self.declare_parameter('assume_base_frame', False)
        self.declare_parameter('ik_service_name', '/compute_ik')
        self.declare_parameter('move_group_name', 'arm')
        self.declare_parameter('joint_states_topic', '/joint_states')
        self.declare_parameter('joint_names', _LARA5_JOINTS)
        self.declare_parameter('view_roll', float(DEFAULT_VIEW_RPY[0]))
        self.declare_parameter('view_pitch', float(DEFAULT_VIEW_RPY[1]))
        self.declare_parameter('view_yaw', float(DEFAULT_VIEW_RPY[2]))
        self.declare_parameter('approach_z_offset', 0.0)
        self.declare_parameter('avoid_collisions', False)
        self.declare_parameter('ik_call_timeout_sec', 10.0)
        self.declare_parameter('tf_lookup_timeout_sec', 1.0)
        self.declare_parameter('use_last_ik_as_seed', True)

        self._base_frame = str(self.get_parameter('base_frame').value)
        self._camera_frame = str(self.get_parameter('camera_frame').value)
        self._assume_base = bool(self.get_parameter('assume_base_frame').value)
        self._ik_service = str(self.get_parameter('ik_service_name').value)
        self._move_group = str(self.get_parameter('move_group_name').value)
        self._joint_names = [str(v) for v in self.get_parameter('joint_names').value]
        self._view_rpy = (
            float(self.get_parameter('view_roll').value),
            float(self.get_parameter('view_pitch').value),
            float(self.get_parameter('view_yaw').value),
        )
        self._z_offset = float(self.get_parameter('approach_z_offset').value)
        self._avoid_collisions = bool(self.get_parameter('avoid_collisions').value)
        self._ik_timeout = float(self.get_parameter('ik_call_timeout_sec').value)
        self._tf_timeout = Duration(seconds=float(self.get_parameter('tf_lookup_timeout_sec').value))
        self._use_last_seed = bool(self.get_parameter('use_last_ik_as_seed').value)

        self._latest_joint_positions: list[float] | None = None
        self._last_ik_seed: list[float] | None = None

        self._tf_buffer = Buffer()
        self._tf_listener = TransformListener(self._tf_buffer, self)

        # Reentrant group: service calls from subscription callbacks must not deadlock spin.
        self._cb_group = ReentrantCallbackGroup()
        self._ik_client = self.create_client(
            GetPositionIK, self._ik_service, callback_group=self._cb_group
        )

        object_topic = str(self.get_parameter('object_xyz_topic').value)
        joint_topic = str(self.get_parameter('joint_states_topic').value)

        self.create_subscription(
            PointStamped, object_topic, self._on_object_xyz, 10, callback_group=self._cb_group
        )
        self.create_subscription(
            JointState, joint_topic, self._on_joint_states, 10, callback_group=self._cb_group
        )

        self._target_pose_pub = self.create_publisher(PoseStamped, 'target_pose_base', 10)
        self._ik_solution_pub = self.create_publisher(JointState, 'ik_solution', 10)

        self.get_logger().info(
            f'Listening on {object_topic!r}; base={self._base_frame!r}, '
            f'camera={self._camera_frame!r}, assume_base={self._assume_base}, '
            f'IK service={self._ik_service!r}'
        )

    def _on_joint_states(self, msg: JointState) -> None:
        if not msg.name or not msg.position:
            return
        name_to_pos = dict(zip(msg.name, msg.position))
        positions: list[float] = []
        for name in self._joint_names:
            if name not in name_to_pos:
                return
            positions.append(float(name_to_pos[name]))
        self._latest_joint_positions = positions

    def _seed_positions(self) -> list[float]:
        if self._use_last_seed and self._last_ik_seed is not None:
            return list(self._last_ik_seed)
        if self._latest_joint_positions is not None:
            return list(self._latest_joint_positions)
        return [0.0] * len(self._joint_names)

    @staticmethod
    def _tf_lookup_time_for_point(msg: PointStamped) -> Time:
        """
        Prefer the measurement timestamp from the incoming PointStamped header.
        Fall back to "latest available" TF when stamp is missing/zero.
        """
        try:
            if msg.header.stamp.sec != 0 or msg.header.stamp.nanosec != 0:
                return Time.from_msg(msg.header.stamp)
        except Exception:
            # Defensive: if header/stamp is malformed, fall back to latest.
            pass
        return Time()

    def _point_in_base_frame(self, msg: PointStamped) -> tuple[float, float, float] | None:
        src_frame = msg.header.frame_id.strip() if msg.header.frame_id else self._camera_frame
        if self._assume_base or src_frame == self._base_frame:
            return float(msg.point.x), float(msg.point.y), float(msg.point.z)

        pt = PointStamped()
        pt.header = msg.header
        if not pt.header.frame_id:
            pt.header.frame_id = self._camera_frame
        pt.point = msg.point

        try:
            transform = self._tf_buffer.lookup_transform(
                self._base_frame,
                pt.header.frame_id,
                self._tf_lookup_time_for_point(pt),
                timeout=self._tf_timeout,
            )
        except TransformException as exc:
            self.get_logger().warning(
                f'TF {pt.header.frame_id!r} -> {self._base_frame!r} failed: {exc}'
            )
            return None

        pt_base = do_transform_point(pt, transform)
        return float(pt_base.point.x), float(pt_base.point.y), float(pt_base.point.z)

    def _build_target_pose(self, x: float, y: float, z: float) -> PoseStamped:
        z += self._z_offset
        qx, qy, qz, qw = _rpy_to_quaternion(*self._view_rpy)
        pose = PoseStamped()
        pose.header.frame_id = self._base_frame
        pose.header.stamp = self.get_clock().now().to_msg()
        pose.pose.position.x = x
        pose.pose.position.y = y
        pose.pose.position.z = z
        pose.pose.orientation.x = qx
        pose.pose.orientation.y = qy
        pose.pose.orientation.z = qz
        pose.pose.orientation.w = qw
        return pose

    def _call_moveit_ik(self, target: PoseStamped, seed: Sequence[float]) -> GetPositionIK.Response | None:
        if not self._ik_client.service_is_ready():
            self.get_logger().warning(f'MoveIt IK service {self._ik_service!r} not ready')
            return None

        req = GetPositionIK.Request()
        req.ik_request = PositionIKRequest()
        req.ik_request.group_name = self._move_group
        req.ik_request.avoid_collisions = self._avoid_collisions
        req.ik_request.pose_stamped = target
        req.ik_request.robot_state = RobotState()
        req.ik_request.robot_state.joint_state = JointState(
            name=list(self._joint_names),
            position=[float(v) for v in seed],
        )

        future = self._ik_client.call_async(req)
        deadline = time.monotonic() + self._ik_timeout
        while not future.done():
            if time.monotonic() >= deadline:
                self.get_logger().error('MoveIt IK call timed out')
                return None
            time.sleep(0.01)
        try:
            return future.result()
        except Exception as exc:
            self.get_logger().error(f'MoveIt IK call failed: {exc}')
            return None

    def _on_object_xyz(self, msg: PointStamped) -> None:
        if not all(math.isfinite(v) for v in (msg.point.x, msg.point.y, msg.point.z)):
            self.get_logger().warning('Ignoring object_xyz with non-finite coordinates')
            return

        src_frame = msg.header.frame_id.strip() if msg.header.frame_id else self._camera_frame
        base_xyz = self._point_in_base_frame(msg)
        if base_xyz is None:
            return

        self.get_logger().info(
            f'TF OK {src_frame!r} ({msg.point.x:.3f}, {msg.point.y:.3f}, {msg.point.z:.3f}) '
            f'-> {self._base_frame!r} ({base_xyz[0]:.3f}, {base_xyz[1]:.3f}, {base_xyz[2]:.3f})'
        )

        target = self._build_target_pose(*base_xyz)
        self._target_pose_pub.publish(target)

        seed = self._seed_positions()
        response = self._call_moveit_ik(target, seed)
        if response is None:
            return

        if response.error_code.val != MoveItErrorCodes.SUCCESS:
            self.get_logger().warning(f'MoveIt IK failed, error_code={response.error_code.val}')
            return

        solution = response.solution.joint_state
        if not solution.name or not solution.position:
            self.get_logger().warning('MoveIt IK succeeded but returned empty joint_state')
            return

        out = JointState()
        out.header.stamp = self.get_clock().now().to_msg()
        out.name = list(solution.name)
        out.position = [float(v) for v in solution.position]
        self._ik_solution_pub.publish(out)

        if self._use_last_seed:
            ordered = []
            name_to_pos = dict(zip(out.name, out.position))
            for jn in self._joint_names:
                if jn in name_to_pos:
                    ordered.append(float(name_to_pos[jn]))
            if len(ordered) == len(self._joint_names):
                self._last_ik_seed = ordered

        deg = [math.degrees(v) for v in out.position]
        self.get_logger().info(
            f'IK OK base_xyz=({base_xyz[0]:.3f}, {base_xyz[1]:.3f}, {base_xyz[2]:.3f}) '
            f'joints_deg={[round(d, 2) for d in deg]}'
        )


def main() -> None:
    rclpy.init()
    node = CameraXyzToJointsNode()
    executor = MultiThreadedExecutor(num_threads=4)
    executor.add_node(node)
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
