#!/usr/bin/env python3
"""ROS2 IK service for 6-DOF arm targets in base frame."""

from __future__ import annotations

import math
import os
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass

import numpy as np
import rclpy
from ament_index_python.packages import PackageNotFoundError, get_package_share_directory
from geometry_msgs.msg import Pose
from lara_interfaces.srv import ComputeIK
from rclpy.exceptions import ParameterUninitializedException
from rclpy.node import Node


def _safe_float_list(text: str | None, expected_len: int, fallback: list[float]) -> list[float]:
    if text is None:
        return list(fallback)
    parts = text.split()
    if len(parts) != expected_len:
        return list(fallback)
    try:
        return [float(v) for v in parts]
    except ValueError:
        return list(fallback)


def _rpy_to_matrix(roll: float, pitch: float, yaw: float) -> np.ndarray:
    cr, sr = math.cos(roll), math.sin(roll)
    cp, sp = math.cos(pitch), math.sin(pitch)
    cy, sy = math.cos(yaw), math.sin(yaw)
    return np.array(
        [
            [cy * cp, cy * sp * sr - sy * cr, cy * sp * cr + sy * sr],
            [sy * cp, sy * sp * sr + cy * cr, sy * sp * cr - cy * sr],
            [-sp, cp * sr, cp * cr],
        ],
        dtype=float,
    )


def _axis_angle_matrix(axis: np.ndarray, angle: float) -> np.ndarray:
    axis_norm = float(np.linalg.norm(axis))
    if axis_norm < 1e-12:
        return np.eye(3, dtype=float)
    x, y, z = axis / axis_norm
    c = math.cos(angle)
    s = math.sin(angle)
    c1 = 1.0 - c
    return np.array(
        [
            [c + x * x * c1, x * y * c1 - z * s, x * z * c1 + y * s],
            [y * x * c1 + z * s, c + y * y * c1, y * z * c1 - x * s],
            [z * x * c1 - y * s, z * y * c1 + x * s, c + z * z * c1],
        ],
        dtype=float,
    )


def _homogeneous(rotation: np.ndarray, translation: np.ndarray) -> np.ndarray:
    out = np.eye(4, dtype=float)
    out[:3, :3] = rotation
    out[:3, 3] = translation
    return out


def _quat_to_matrix(x: float, y: float, z: float, w: float) -> np.ndarray:
    n = x * x + y * y + z * z + w * w
    if n < 1e-12:
        return np.eye(3, dtype=float)
    s = 2.0 / n
    xx, yy, zz = x * x * s, y * y * s, z * z * s
    xy, xz, yz = x * y * s, x * z * s, y * z * s
    wx, wy, wz = w * x * s, w * y * s, w * z * s
    return np.array(
        [
            [1.0 - (yy + zz), xy - wz, xz + wy],
            [xy + wz, 1.0 - (xx + zz), yz - wx],
            [xz - wy, yz + wx, 1.0 - (xx + yy)],
        ],
        dtype=float,
    )


def _rotation_vector_from_matrix(rot: np.ndarray) -> np.ndarray:
    tr = float(np.trace(rot))
    cos_angle = max(-1.0, min(1.0, 0.5 * (tr - 1.0)))
    angle = math.acos(cos_angle)
    if angle < 1e-9:
        return np.zeros(3, dtype=float)
    denom = 2.0 * math.sin(angle)
    if abs(denom) < 1e-9:
        axis = np.array(
            [
                math.sqrt(max(0.0, (rot[0, 0] + 1.0) * 0.5)),
                math.sqrt(max(0.0, (rot[1, 1] + 1.0) * 0.5)),
                math.sqrt(max(0.0, (rot[2, 2] + 1.0) * 0.5)),
            ],
            dtype=float,
        )
        return axis * angle
    axis = np.array(
        [
            (rot[2, 1] - rot[1, 2]) / denom,
            (rot[0, 2] - rot[2, 0]) / denom,
            (rot[1, 0] - rot[0, 1]) / denom,
        ],
        dtype=float,
    )
    return axis * angle


@dataclass
class JointModel:
    name: str
    joint_type: str
    parent_link: str
    child_link: str
    origin_xyz: np.ndarray
    origin_rpy: np.ndarray
    axis: np.ndarray
    lower: float
    upper: float


class UrdfChainModel:
    def __init__(self, urdf_path: str, base_link: str, tip_link: str, selected_joints: list[str]):
        self.urdf_path = urdf_path
        self.base_link = base_link
        self.tip_link = tip_link
        self._all_joints = self._parse_urdf(self.urdf_path)
        self.chain = self._build_chain(self._all_joints, self.base_link, self.tip_link)

        chain_revolute = [j for j in self.chain if j.joint_type in ('revolute', 'continuous')]
        if selected_joints:
            selected_set = set(selected_joints)
            by_name = {j.name: j for j in chain_revolute}
            for name in selected_joints:
                if name not in by_name:
                    raise ValueError(f'joint {name!r} is not part of chain {base_link}->{tip_link}')
            # Keep URDF chain order for stable FK/Jacobian indexing.
            self.active_joints = [j for j in chain_revolute if j.name in selected_set]
        else:
            self.active_joints = chain_revolute
        if len(self.active_joints) != 6:
            raise ValueError(
                f'expected 6 active joints, got {len(self.active_joints)}: '
                f'{[j.name for j in self.active_joints]}'
            )

        self.joint_names = [j.name for j in self.active_joints]
        self.lower = np.array([j.lower for j in self.active_joints], dtype=float)
        self.upper = np.array([j.upper for j in self.active_joints], dtype=float)

    @staticmethod
    def _parse_urdf(path: str) -> list[JointModel]:
        if not os.path.exists(path):
            raise FileNotFoundError(f'URDF file not found: {path}')
        root = ET.parse(path).getroot()
        joints: list[JointModel] = []
        for joint in root.findall('joint'):
            name = joint.attrib.get('name', '')
            joint_type = joint.attrib.get('type', 'fixed')
            parent_node = joint.find('parent')
            child_node = joint.find('child')
            if parent_node is None or child_node is None:
                continue
            parent_link = parent_node.attrib.get('link', '')
            child_link = child_node.attrib.get('link', '')
            origin_node = joint.find('origin')
            xyz = np.array(
                _safe_float_list(origin_node.attrib.get('xyz') if origin_node is not None else None, 3, [0.0, 0.0, 0.0]),
                dtype=float,
            )
            rpy = np.array(
                _safe_float_list(origin_node.attrib.get('rpy') if origin_node is not None else None, 3, [0.0, 0.0, 0.0]),
                dtype=float,
            )
            axis_node = joint.find('axis')
            axis = np.array(
                _safe_float_list(axis_node.attrib.get('xyz') if axis_node is not None else None, 3, [1.0, 0.0, 0.0]),
                dtype=float,
            )
            axis_norm = np.linalg.norm(axis)
            if axis_norm > 1e-12:
                axis = axis / axis_norm
            limit_node = joint.find('limit')
            lower = -math.pi
            upper = math.pi
            if joint_type == 'continuous':
                lower = -2.0 * math.pi
                upper = 2.0 * math.pi
            if limit_node is not None:
                lower = float(limit_node.attrib.get('lower', lower))
                upper = float(limit_node.attrib.get('upper', upper))
            joints.append(
                JointModel(
                    name=name,
                    joint_type=joint_type,
                    parent_link=parent_link,
                    child_link=child_link,
                    origin_xyz=xyz,
                    origin_rpy=rpy,
                    axis=axis,
                    lower=lower,
                    upper=upper,
                )
            )
        return joints

    @staticmethod
    def _build_chain(all_joints: list[JointModel], base_link: str, tip_link: str) -> list[JointModel]:
        child_to_joint = {j.child_link: j for j in all_joints}
        chain_rev: list[JointModel] = []
        current = tip_link
        visited: set[str] = set()
        while current != base_link:
            if current in visited:
                raise ValueError(f'loop detected while building chain from {base_link} to {tip_link}')
            visited.add(current)
            joint = child_to_joint.get(current)
            if joint is None:
                raise ValueError(f'no joint connects child link {current!r} toward base {base_link!r}')
            chain_rev.append(joint)
            current = joint.parent_link
        chain_rev.reverse()
        return chain_rev

    def forward_kinematics(self, q: np.ndarray) -> tuple[np.ndarray, list[np.ndarray], list[np.ndarray]]:
        q_map = {name: float(val) for name, val in zip(self.joint_names, q)}
        t = np.eye(4, dtype=float)
        joint_positions: list[np.ndarray] = []
        joint_axes_world: list[np.ndarray] = []
        for joint in self.chain:
            t = t @ _homogeneous(_rpy_to_matrix(*joint.origin_rpy), joint.origin_xyz)
            if joint.name in q_map:
                p = t[:3, 3].copy()
                z = t[:3, :3] @ joint.axis
                joint_positions.append(p)
                joint_axes_world.append(z)
                t = t @ _homogeneous(_axis_angle_matrix(joint.axis, q_map[joint.name]), np.zeros(3, dtype=float))
        return t, joint_positions, joint_axes_world

    def geometric_jacobian(self, q: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        t_ee, positions, axes = self.forward_kinematics(q)
        p_ee = t_ee[:3, 3]
        j = np.zeros((6, len(self.joint_names)), dtype=float)
        for i, (p_i, z_i) in enumerate(zip(positions, axes)):
            j[:3, i] = np.cross(z_i, p_ee - p_i)
            j[3:, i] = z_i
        return j, t_ee


class InverseKinematicsNode(Node):
    def __init__(self) -> None:
        super().__init__('ik_service')
        self.declare_parameter('service_name', 'compute_ik')
        self.declare_parameter('urdf_path', '')
        self.declare_parameter('base_link', 'lara5_link0')
        self.declare_parameter('tip_link', 'lara5_gripper')
        # Non-empty default avoids ROS2 Humble empty-array uninitialized edge case.
        self.declare_parameter('active_joint_names', [''])
        self.declare_parameter('default_seed', [0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        self.declare_parameter('solver.max_iterations', 250)
        self.declare_parameter('solver.damping', 0.05)
        self.declare_parameter('solver.step_scale', 1.0)
        self.declare_parameter('solver.max_step_rad', 0.25)
        self.declare_parameter('solver.position_weight', 1.0)
        self.declare_parameter('solver.orientation_weight', 0.6)
        self.declare_parameter('solver.position_tolerance', 0.003)
        self.declare_parameter('solver.orientation_tolerance', 0.04)
        self.declare_parameter('solver.timeout_sec', 0.2)
        self.declare_parameter('solver.random_restarts', 3)
        self.declare_parameter('solver.enforce_joint_limits', True)
        self.declare_parameter('solver.fail_on_outside_limits', False)

        urdf_path = str(self.get_parameter('urdf_path').value).strip()
        if not urdf_path:
            urdf_path = self._default_urdf_path()
        base_link = str(self.get_parameter('base_link').value)
        tip_link = str(self.get_parameter('tip_link').value)
        selected_joints = [
            str(v).strip()
            for v in self._get_param_list('active_joint_names', [''])
            if str(v).strip()
        ]
        self.default_seed = np.array([float(v) for v in self.get_parameter('default_seed').value], dtype=float)
        self.max_iterations = int(self.get_parameter('solver.max_iterations').value)
        self.damping = float(self.get_parameter('solver.damping').value)
        self.step_scale = float(self.get_parameter('solver.step_scale').value)
        self.max_step_rad = float(self.get_parameter('solver.max_step_rad').value)
        self.position_weight = float(self.get_parameter('solver.position_weight').value)
        self.orientation_weight = float(self.get_parameter('solver.orientation_weight').value)
        self.default_position_tolerance = float(self.get_parameter('solver.position_tolerance').value)
        self.default_orientation_tolerance = float(self.get_parameter('solver.orientation_tolerance').value)
        self.default_timeout_sec = float(self.get_parameter('solver.timeout_sec').value)
        self.random_restarts = int(self.get_parameter('solver.random_restarts').value)
        self.default_enforce_limits = bool(self.get_parameter('solver.enforce_joint_limits').value)
        self.fail_on_outside_limits = bool(self.get_parameter('solver.fail_on_outside_limits').value)

        self.model = UrdfChainModel(
            urdf_path=urdf_path,
            base_link=base_link,
            tip_link=tip_link,
            selected_joints=selected_joints,
        )
        if self.default_seed.shape[0] != len(self.model.joint_names):
            self.default_seed = np.zeros(len(self.model.joint_names), dtype=float)
        self.default_seed = np.clip(self.default_seed, self.model.lower, self.model.upper)

        service_name = str(self.get_parameter('service_name').value).strip() or 'compute_ik'
        self.create_service(ComputeIK, service_name, self._handle_ik)
        self.get_logger().info(
            f'IK service ready on {service_name!r}; base={base_link}, tip={tip_link}, '
            f'joints={self.model.joint_names}, urdf={urdf_path}'
        )

    def _get_param_list(self, name: str, fallback: list[str]) -> list[str]:
        try:
            value = self.get_parameter(name).value
        except ParameterUninitializedException:
            return list(fallback)
        if value is None:
            return list(fallback)
        if isinstance(value, (list, tuple)):
            return [str(v) for v in value]
        return list(fallback)

    def _default_urdf_path(self) -> str:
        try:
            share = get_package_share_directory('lara5_description')
            return os.path.join(share, 'lara5', 'urdf', 'lara5.urdf')
        except PackageNotFoundError:
            source_candidate = os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    '..',
                    '..',
                    'lara5_description',
                    'lara5',
                    'urdf',
                    'lara5.urdf',
                )
            )
            if os.path.exists(source_candidate):
                return source_candidate
            raise RuntimeError(
                'urdf_path parameter is empty and lara5_description was not resolved in '
                'installed share or source workspace; set urdf_path explicitly'
            )

    def _pose_to_target(self, pose: Pose) -> tuple[np.ndarray, np.ndarray]:
        p = np.array([pose.position.x, pose.position.y, pose.position.z], dtype=float)
        q = pose.orientation
        rot = _quat_to_matrix(q.x, q.y, q.z, q.w)
        return p, rot

    def _solve_once(
        self,
        seed: np.ndarray,
        target_pos: np.ndarray,
        target_rot: np.ndarray,
        pos_tol: float,
        ori_tol: float,
        timeout_sec: float,
        enforce_limits: bool,
    ) -> tuple[np.ndarray, float, float, int]:
        start = time.monotonic()
        q = np.array(seed, dtype=float)
        if enforce_limits:
            q = np.clip(q, self.model.lower, self.model.upper)

        best_q = q.copy()
        best_score = float('inf')
        best_pos_err = float('inf')
        best_ori_err = float('inf')
        best_iter = 0
        for i in range(1, self.max_iterations + 1):
            jacobian, t_now = self.model.geometric_jacobian(q)
            pos_now = t_now[:3, 3]
            rot_now = t_now[:3, :3]
            pos_err_vec = target_pos - pos_now
            rot_err = target_rot @ rot_now.T
            ori_err_vec = _rotation_vector_from_matrix(rot_err)
            pos_err = float(np.linalg.norm(pos_err_vec))
            ori_err = float(np.linalg.norm(ori_err_vec))
            score = self.position_weight * pos_err + self.orientation_weight * ori_err
            if score < best_score:
                best_score = score
                best_pos_err = pos_err
                best_ori_err = ori_err
                best_q = q.copy()
                best_iter = i
            if pos_err <= pos_tol and ori_err <= ori_tol:
                return q, pos_err, ori_err, i
            err = np.concatenate(
                (
                    self.position_weight * pos_err_vec,
                    self.orientation_weight * ori_err_vec,
                )
            )
            weighted_j = np.vstack(
                (
                    self.position_weight * jacobian[:3, :],
                    self.orientation_weight * jacobian[3:, :],
                )
            )
            jj_t = weighted_j @ weighted_j.T
            damp_mat = (self.damping ** 2) * np.eye(jj_t.shape[0], dtype=float)
            try:
                dq = weighted_j.T @ np.linalg.solve(jj_t + damp_mat, err)
            except np.linalg.LinAlgError:
                dq = weighted_j.T @ np.linalg.pinv(jj_t + damp_mat) @ err
            if self.max_step_rad > 0.0:
                dq = np.clip(dq, -self.max_step_rad, self.max_step_rad)
            q = q + self.step_scale * dq
            if enforce_limits:
                q = np.clip(q, self.model.lower, self.model.upper)
            if timeout_sec > 0.0 and time.monotonic() - start >= timeout_sec:
                break
        return best_q, best_pos_err, best_ori_err, best_iter

    def _choose_seeds(self, request_seed: list[float], enforce_limits: bool) -> list[np.ndarray]:
        seeds: list[np.ndarray] = []
        if len(request_seed) == len(self.model.joint_names):
            seed = np.array(request_seed, dtype=float)
            if enforce_limits:
                seed = np.clip(seed, self.model.lower, self.model.upper)
            seeds.append(seed)
        seeds.append(self.default_seed.copy())

        restarts = max(0, self.random_restarts)
        if restarts > 0:
            rng = np.random.default_rng()
            low = self.model.lower
            high = self.model.upper
            for _ in range(restarts):
                sample = rng.uniform(low=low, high=high)
                seeds.append(sample)
        return seeds

    def _handle_ik(self, request: ComputeIK.Request, response: ComputeIK.Response) -> ComputeIK.Response:
        target_pos, target_rot = self._pose_to_target(request.target_pose)
        pos_tol = float(request.position_tolerance) if request.position_tolerance > 0.0 else self.default_position_tolerance
        ori_tol = float(request.orientation_tolerance) if request.orientation_tolerance > 0.0 else self.default_orientation_tolerance
        timeout_sec = float(request.timeout_sec) if request.timeout_sec > 0.0 else self.default_timeout_sec
        if request.enforce_joint_limits_mode > 0:
            enforce_limits = True
        elif request.enforce_joint_limits_mode < 0:
            enforce_limits = False
        else:
            enforce_limits = self.default_enforce_limits

        best_q: np.ndarray | None = None
        best_pos_err = float('inf')
        best_ori_err = float('inf')
        best_iter = 0

        for seed in self._choose_seeds(list(request.seed_joint_positions), enforce_limits):
            q, pos_err, ori_err, iterations = self._solve_once(
                seed=seed,
                target_pos=target_pos,
                target_rot=target_rot,
                pos_tol=pos_tol,
                ori_tol=ori_tol,
                timeout_sec=timeout_sec,
                enforce_limits=enforce_limits,
            )
            if pos_err + ori_err < best_pos_err + best_ori_err:
                best_q = q
                best_pos_err = pos_err
                best_ori_err = ori_err
                best_iter = iterations
            if pos_err <= pos_tol and ori_err <= ori_tol:
                break

        response.joint_names = list(self.model.joint_names)
        response.position_error = float(best_pos_err)
        response.orientation_error = float(best_ori_err)
        response.iterations = int(best_iter)

        if best_q is None:
            response.success = False
            response.message = 'IK failed: no candidate solution generated'
            response.joint_positions = []
            return response

        if enforce_limits and self.fail_on_outside_limits:
            outside = np.logical_or(best_q < self.model.lower - 1e-8, best_q > self.model.upper + 1e-8)
            if np.any(outside):
                response.success = False
                response.message = 'IK failed: best solution outside joint limits'
                response.joint_positions = [float(v) for v in best_q]
                return response

        response.joint_positions = [float(v) for v in best_q]
        response.success = best_pos_err <= pos_tol and best_ori_err <= ori_tol
        if response.success:
            response.message = (
                f'IK converged (pos={best_pos_err:.5f} m, ori={best_ori_err:.5f} rad, '
                f'iterations={best_iter})'
            )
        else:
            response.message = (
                f'IK best effort only (pos={best_pos_err:.5f} m, ori={best_ori_err:.5f} rad, '
                f'tolerances={pos_tol:.5f}/{ori_tol:.5f})'
            )
        return response


def main(args=None) -> None:
    rclpy.init(args=args)
    node = InverseKinematicsNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
