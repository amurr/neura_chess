"""MoveIt IK helpers shared by chess motion nodes."""

from __future__ import annotations

import math
import time
from typing import Sequence

from geometry_msgs.msg import Pose, PoseStamped
from moveit_msgs.msg import MoveItErrorCodes, PositionIKRequest, RobotState
from moveit_msgs.srv import GetPositionIK
from rclpy.node import Node
from sensor_msgs.msg import JointState

_LARA5_JOINTS = [f'lara5_joint{i}' for i in range(1, 7)]


def rpy_to_quaternion(roll: float, pitch: float, yaw: float) -> tuple[float, float, float, float]:
    cr, sr = math.cos(roll * 0.5), math.sin(roll * 0.5)
    cp, sp = math.cos(pitch * 0.5), math.sin(pitch * 0.5)
    cy, sy = math.cos(yaw * 0.5), math.sin(yaw * 0.5)
    qw = cr * cp * cy + sr * sp * sy
    qx = sr * cp * cy - cr * sp * sy
    qy = cr * sp * cy + sr * cp * sy
    qz = cr * cp * sy - sr * sp * cy
    return qx, qy, qz, qw


def pose6_to_pose_stamped(
    pose6: Sequence[float],
    frame_id: str,
    stamp=None,
) -> PoseStamped:
    if len(pose6) != 6:
        raise ValueError(f'pose6 must have 6 values, got {len(pose6)}')
    x, y, z, roll, pitch, yaw = [float(v) for v in pose6]
    qx, qy, qz, qw = rpy_to_quaternion(roll, pitch, yaw)
    msg = PoseStamped()
    msg.header.frame_id = frame_id
    if stamp is not None:
        msg.header.stamp = stamp
    msg.pose.position.x = x
    msg.pose.position.y = y
    msg.pose.position.z = z
    msg.pose.orientation.x = qx
    msg.pose.orientation.y = qy
    msg.pose.orientation.z = qz
    msg.pose.orientation.w = qw
    return msg


def pose6_with_z_offset(pose6: Sequence[float], dz: float) -> list[float]:
    out = [float(v) for v in pose6]
    out[2] += float(dz)
    return out


def joint_state_to_ordered_positions(
    joint_state: JointState,
    joint_names: Sequence[str],
) -> list[float] | None:
    if not joint_state.name or not joint_state.position:
        return None
    name_to_pos = dict(zip(joint_state.name, joint_state.position))
    ordered: list[float] = []
    for name in joint_names:
        if name not in name_to_pos:
            return None
        ordered.append(float(name_to_pos[name]))
    return ordered


def joint_positions_rad_to_deg(positions_rad: Sequence[float]) -> list[float]:
    return [math.degrees(float(v)) for v in positions_rad]


class MoveItIkSolver:
    """Thin wrapper around move_group /compute_ik."""

    def __init__(
        self,
        node: Node,
        *,
        ik_service_name: str = '/compute_ik',
        move_group_name: str = 'arm',
        planning_frame: str = 'world',
        joint_names: Sequence[str] | None = None,
        avoid_collisions: bool = False,
        ik_timeout_sec: float = 10.0,
    ) -> None:
        self._node = node
        self._ik_service = ik_service_name
        self._move_group = move_group_name
        self._planning_frame = planning_frame
        self._joint_names = list(joint_names or _LARA5_JOINTS)
        self._avoid_collisions = avoid_collisions
        self._ik_timeout = float(ik_timeout_sec)
        self._client = node.create_client(GetPositionIK, ik_service_name)
        self._last_seed_rad: list[float] | None = None

    @property
    def planning_frame(self) -> str:
        return self._planning_frame

    def service_is_ready(self) -> bool:
        return self._client.service_is_ready()

    def wait_for_service(self, timeout_sec: float = 5.0) -> bool:
        return self._client.wait_for_service(timeout_sec=timeout_sec)

    def set_seed_from_joint_state(self, msg: JointState) -> None:
        ordered = joint_state_to_ordered_positions(msg, self._joint_names)
        if ordered is not None:
            self._last_seed_rad = ordered

    def seed_positions_rad(self, fallback: Sequence[float] | None = None) -> list[float]:
        if self._last_seed_rad is not None:
            return list(self._last_seed_rad)
        if fallback is not None:
            return [float(v) for v in fallback]
        return [0.0] * len(self._joint_names)

    def solve_pose6(
        self,
        pose6: Sequence[float],
        seed_rad: Sequence[float] | None = None,
    ) -> list[float] | None:
        """Return arm joint positions in degrees, or None on failure."""
        if not self._client.service_is_ready():
            self._node.get_logger().warning(f'MoveIt IK service {self._ik_service!r} not ready')
            return None

        stamp = self._node.get_clock().now().to_msg()
        target = pose6_to_pose_stamped(pose6, self._planning_frame, stamp=stamp)
        seed = list(seed_rad) if seed_rad is not None else self.seed_positions_rad()

        req = GetPositionIK.Request()
        req.ik_request = PositionIKRequest()
        req.ik_request.group_name = self._move_group
        req.ik_request.avoid_collisions = self._avoid_collisions
        req.ik_request.pose_stamped = target
        req.ik_request.robot_state = RobotState()
        req.ik_request.robot_state.joint_state = JointState(
            name=list(self._joint_names),
            position=seed,
        )

        future = self._client.call_async(req)
        deadline = time.monotonic() + self._ik_timeout
        while not future.done():
            if time.monotonic() >= deadline:
                self._node.get_logger().error('MoveIt IK call timed out')
                return None
            time.sleep(0.01)

        try:
            response = future.result()
        except Exception as exc:
            self._node.get_logger().error(f'MoveIt IK call failed: {exc}')
            return None

        if response is None or response.error_code.val != MoveItErrorCodes.SUCCESS:
            code = response.error_code.val if response is not None else 'no response'
            self._node.get_logger().warning(f'MoveIt IK failed, error_code={code}')
            return None

        solution = response.solution.joint_state
        ordered = joint_state_to_ordered_positions(solution, self._joint_names)
        if ordered is None:
            self._node.get_logger().warning('MoveIt IK succeeded but joint names did not match')
            return None

        self._last_seed_rad = ordered
        return joint_positions_rad_to_deg(ordered)
