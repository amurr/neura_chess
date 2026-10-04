"""FK/IK and chess-square XY for hover-joint teaching (no ROS)."""

from __future__ import annotations

import math
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np

ARM_JOINTS = (
    'lara5_joint1',
    'lara5_joint2',
    'lara5_joint3',
    'lara5_joint4',
    'lara5_joint5',
    'lara5_joint6',
)
FILES = 'abcdefgh'
RANKS = '12345678'


def all_squares() -> list[str]:
    return [f'{f}{r}' for f in FILES for r in RANKS]


def square_xy(
    square: str,
    *,
    a1: tuple[float, float, float] = (0.27, -0.16, 0.02),
    square_size: float = 0.04,
    layout: str = 'ranks_x_files_y',
    file_mirror: bool = True,
) -> np.ndarray:
    """World XY of a square centre (matches lara5_moveit/chess_scene.yaml)."""
    key = square.strip().lower()
    file_i = ord(key[0]) - ord('a')
    rank_i = int(key[1]) - 1
    if file_mirror:
        file_i = 7 - file_i
    s = float(square_size)
    if layout == 'ranks_x_files_y':
        pb = np.array([(rank_i + 0.5) * s, (file_i + 0.5) * s])
    else:
        pb = np.array([(file_i + 0.5) * s, (rank_i + 0.5) * s])
    return np.array([a1[0], a1[1]], dtype=float) + pb


def rpy_to_matrix(roll: float, pitch: float, yaw: float) -> np.ndarray:
    cr, sr = math.cos(roll), math.sin(roll)
    cp, sp = math.cos(pitch), math.sin(pitch)
    cy, sy = math.cos(yaw), math.sin(yaw)
    return np.array(
        [
            [cy * cp, cy * sp * sr - sy * cr, cy * sp * cr + sy * sr],
            [sy * cp, sy * sp * sr + cy * cr, sy * sp * cr - cy * sr],
            [-sp, cp * sr, cp * cr],
        ]
    )


def _axis_angle(axis: np.ndarray, angle: float) -> np.ndarray:
    axis = axis / np.linalg.norm(axis)
    x, y, z = axis
    c, s = math.cos(angle), math.sin(angle)
    c1 = 1.0 - c
    return np.array(
        [
            [c + x * x * c1, x * y * c1 - z * s, x * z * c1 + y * s],
            [y * x * c1 + z * s, c + y * y * c1, y * z * c1 - x * s],
            [z * x * c1 - y * s, z * y * c1 + x * s, c + z * z * c1],
        ]
    )


def _homog(rot: np.ndarray, xyz: np.ndarray) -> np.ndarray:
    out = np.eye(4)
    out[:3, :3] = rot
    out[:3, 3] = xyz
    return out


def _rotvec(rot: np.ndarray) -> np.ndarray:
    tr = float(np.trace(rot))
    ca = max(-1.0, min(1.0, 0.5 * (tr - 1.0)))
    ang = math.acos(ca)
    if ang < 1e-9:
        return np.zeros(3)
    denom = 2.0 * math.sin(ang)
    return (
        np.array([rot[2, 1] - rot[1, 2], rot[0, 2] - rot[2, 0], rot[1, 0] - rot[0, 1]])
        / denom
        * ang
    )


class _Joint:
    def __init__(self, **kwargs: object) -> None:
        self.__dict__.update(kwargs)


class ArmModel:
    def __init__(self, urdf_path: str, base: str = 'world', tip: str = 'lara5_gripper') -> None:
        self.chain, self.active = self._parse(urdf_path, base, tip)
        self.lower = np.array([j.lo for j in self.active], dtype=float)
        self.upper = np.array([j.hi for j in self.active], dtype=float)

    @staticmethod
    def _parse(path: str, base: str, tip: str) -> tuple[list[_Joint], list[_Joint]]:
        root = ET.parse(path).getroot()
        joints: list[_Joint] = []
        for node in root.findall('joint'):
            origin = node.find('origin')
            axis_n = node.find('axis')
            limit = node.find('limit')
            xyz = (
                [0.0, 0.0, 0.0]
                if origin is None or 'xyz' not in origin.attrib
                else [float(v) for v in origin.attrib['xyz'].split()]
            )
            rpy = (
                [0.0, 0.0, 0.0]
                if origin is None or 'rpy' not in origin.attrib
                else [float(v) for v in origin.attrib['rpy'].split()]
            )
            axis = (
                [1.0, 0.0, 0.0]
                if axis_n is None
                else [float(v) for v in axis_n.attrib.get('xyz', '1 0 0').split()]
            )
            lo, hi = -math.pi, math.pi
            if limit is not None:
                lo = float(limit.attrib.get('lower', lo))
                hi = float(limit.attrib.get('upper', hi))
            parent = node.find('parent')
            child = node.find('child')
            if parent is None or child is None:
                continue
            joints.append(
                _Joint(
                    name=node.attrib['name'],
                    parent=parent.attrib['link'],
                    child=child.attrib['link'],
                    xyz=np.array(xyz, float),
                    rpy=np.array(rpy, float),
                    axis=np.array(axis, float) / np.linalg.norm(axis),
                    lo=lo,
                    hi=hi,
                )
            )
        child_to = {j.child: j for j in joints}
        chain: list[_Joint] = []
        cur = tip
        while cur != base:
            joint = child_to[cur]
            chain.append(joint)
            cur = joint.parent
        chain.reverse()
        active = [j for j in chain if j.name in ARM_JOINTS]
        return chain, active

    def fk(self, q: np.ndarray) -> np.ndarray:
        qmap = {name: float(val) for name, val in zip(ARM_JOINTS, q)}
        t = np.eye(4)
        for joint in self.chain:
            t = t @ _homog(rpy_to_matrix(*joint.rpy), joint.xyz)
            if joint.name in qmap:
                t = t @ _homog(_axis_angle(joint.axis, qmap[joint.name]), np.zeros(3))
        return t

    def jacobian(self, q: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        qmap = {name: float(val) for name, val in zip(ARM_JOINTS, q)}
        t = np.eye(4)
        pos, axes = [], []
        for joint in self.chain:
            t = t @ _homog(rpy_to_matrix(*joint.rpy), joint.xyz)
            if joint.name in qmap:
                pos.append(t[:3, 3].copy())
                axes.append(t[:3, :3] @ joint.axis)
                t = t @ _homog(_axis_angle(joint.axis, qmap[joint.name]), np.zeros(3))
        p_ee = t[:3, 3]
        jac = np.zeros((6, 6))
        for i, (p_i, z_i) in enumerate(zip(pos, axes)):
            jac[:3, i] = np.cross(z_i, p_ee - p_i)
            jac[3:, i] = z_i
        return jac, t

    def ik(
        self,
        target_pos: np.ndarray,
        target_rot: np.ndarray,
        seed: np.ndarray,
        *,
        pos_tol: float = 0.002,
        ori_tol: float = 0.03,
    ) -> tuple[bool, np.ndarray, float, float]:
        q = np.clip(np.array(seed, dtype=float), self.lower, self.upper)
        best = (float('inf'), float('inf'), q.copy())
        for _ in range(280):
            jac, t = self.jacobian(q)
            pos_err = target_pos - t[:3, 3]
            ori_err = _rotvec(target_rot @ t[:3, :3].T)
            pe, oe = float(np.linalg.norm(pos_err)), float(np.linalg.norm(ori_err))
            if pe + oe < best[0] + best[1]:
                best = (pe, oe, q.copy())
            if pe <= pos_tol and oe <= ori_tol:
                return True, q, pe, oe
            err = np.concatenate((pos_err, 0.8 * ori_err))
            weighted = np.vstack((jac[:3], 0.8 * jac[3:]))
            dq = weighted.T @ np.linalg.solve(
                weighted @ weighted.T + 0.04**2 * np.eye(6), err
            )
            q = np.clip(q + np.clip(dq, -0.2, 0.2), self.lower, self.upper)
        return False, best[2], best[0], best[1]


def default_urdf() -> str:
    try:
        from ament_index_python.packages import get_package_share_directory

        return str(
            Path(get_package_share_directory('lara5_description'))
            / 'lara5'
            / 'urdf'
            / 'lara5.urdf'
        )
    except Exception:
        here = Path(__file__).resolve()
        return str(
            here.parents[2] / 'lara5_description' / 'lara5' / 'urdf' / 'lara5.urdf'
        )


def fill_hover_joints(
    seed_q: np.ndarray,
    model: ArmModel,
    *,
    a1: tuple[float, float, float] = (0.27, -0.16, 0.02),
    square_size: float = 0.04,
    layout: str = 'ranks_x_files_y',
    file_mirror: bool = True,
    z_override: float | None = None,
) -> dict[str, dict[str, object]]:
    """IK every square at the seed pose's height and orientation."""
    t0 = model.fk(seed_q)
    rot = t0[:3, :3]
    hover_z = float(t0[2, 3] if z_override is None else z_override)
    tool_z = rot @ np.array([0.0, 0.0, 1.0])
    out: dict[str, dict[str, object]] = {}
    seed = np.array(seed_q, dtype=float)
    for square in all_squares():
        xy = square_xy(
            square, a1=a1, square_size=square_size, layout=layout, file_mirror=file_mirror
        )
        target = np.array([xy[0], xy[1], hover_z])
        ok, q, pe, oe = model.ik(target, rot, seed)
        out[square] = {
            'ok': ok,
            'q': [float(v) for v in q],
            'pos_err_m': pe,
            'ori_err_rad': oe,
            'xyz': [float(xy[0]), float(xy[1]), hover_z],
        }
        if not ok:
            ok, q, pe, oe = model.ik(target, rot, seed_q)
            out[square] = {
                'ok': ok,
                'q': [float(v) for v in q],
                'pos_err_m': pe,
                'ori_err_rad': oe,
                'xyz': [float(xy[0]), float(xy[1]), hover_z],
            }
        if out[square]['ok']:
            seed = np.array(out[square]['q'], dtype=float)
    return {
        'hover_z': hover_z,
        'tool_z_world': [float(v) for v in tool_z],
        'squares': out,
    }
