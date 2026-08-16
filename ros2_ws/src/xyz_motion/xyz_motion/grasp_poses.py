"""Perpendicular EEF grasp / hover poses for chess squares.

All orientation math lives here (and in the TF publisher). MTC only looks up frames.

Board frame: origin at the a1 *corner*, +X/+Y from calibration, +Z = surface normal.
Grasp frame: same origin offset along the normal; EEF +Z aligned to -normal (into the board).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence

import numpy as np

from xyz_motion.board_calibration import BoardCalibration, board_to_base
from xyz_motion.chess_scene import (
    extract_pieces_from_occupancy,
    extract_square_xyz_from_occupancy,
    iter_board_squares,
    normalize_piece_type,
    normalize_square_name,
    piece_dimensions,
    square_center_world,
)

FILES = 'abcdefgh'
RANKS = '12345678'


def _v3(xyz: Sequence[float]) -> np.ndarray:
    arr = np.asarray(xyz, dtype=float).reshape(3)
    return arr


def _norm(v: np.ndarray) -> np.ndarray:
    n = float(np.linalg.norm(v))
    if n < 1e-12:
        raise ValueError('cannot normalize near-zero vector')
    return v / n


def rotation_matrix_to_quaternion(rotation: np.ndarray) -> tuple[float, float, float, float]:
    """Return (x, y, z, w) from a 3x3 rotation matrix."""
    m = np.asarray(rotation, dtype=float).reshape(3, 3)
    trace = float(m[0, 0] + m[1, 1] + m[2, 2])
    if trace > 0.0:
        s = np.sqrt(trace + 1.0) * 2.0
        qw = 0.25 * s
        qx = (m[2, 1] - m[1, 2]) / s
        qy = (m[0, 2] - m[2, 0]) / s
        qz = (m[1, 0] - m[0, 1]) / s
    elif m[0, 0] > m[1, 1] and m[0, 0] > m[2, 2]:
        s = np.sqrt(1.0 + m[0, 0] - m[1, 1] - m[2, 2]) * 2.0
        qw = (m[2, 1] - m[1, 2]) / s
        qx = 0.25 * s
        qy = (m[0, 1] + m[1, 0]) / s
        qz = (m[0, 2] + m[2, 0]) / s
    elif m[1, 1] > m[2, 2]:
        s = np.sqrt(1.0 + m[1, 1] - m[0, 0] - m[2, 2]) * 2.0
        qw = (m[0, 2] - m[2, 0]) / s
        qx = (m[0, 1] + m[1, 0]) / s
        qy = 0.25 * s
        qz = (m[1, 2] + m[2, 1]) / s
    else:
        s = np.sqrt(1.0 + m[2, 2] - m[0, 0] - m[1, 1]) * 2.0
        qw = (m[1, 0] - m[0, 1]) / s
        qx = (m[0, 2] + m[2, 0]) / s
        qy = (m[1, 2] + m[2, 1]) / s
        qz = 0.25 * s
    return float(qx), float(qy), float(qz), float(qw)


def quaternion_to_rotation_matrix(quat_xyzw: Sequence[float]) -> np.ndarray:
    x, y, z, w = (float(v) for v in quat_xyzw)
    return np.array(
        [
            [1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
            [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
            [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)],
        ],
        dtype=float,
    )


def eef_z_world(quat_xyzw: Sequence[float]) -> np.ndarray:
    """World-frame direction of the EEF +Z axis."""
    return quaternion_to_rotation_matrix(quat_xyzw) @ np.array([0.0, 0.0, 1.0])


def rotation_aligning_eef_z(approach_world: Sequence[float], yaw_about_approach: float = 0.0) -> np.ndarray:
    """Rotation whose columns are EEF axes in world: +Z maps to ``approach_world``."""
    z_axis = _norm(_v3(approach_world))
    helper = np.array([1.0, 0.0, 0.0]) if abs(float(z_axis[0])) < 0.9 else np.array([0.0, 1.0, 0.0])
    x_axis = _norm(np.cross(helper, z_axis))
    y_axis = np.cross(z_axis, x_axis)
    rot = np.column_stack((x_axis, y_axis, z_axis))
    yaw = float(yaw_about_approach)
    if abs(yaw) > 1e-12:
        c, s = float(np.cos(yaw)), float(np.sin(yaw))
        rot = rot @ np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]], dtype=float)
    return rot


def perpendicular_eef_quaternion(
    board_normal_world: Sequence[float],
    *,
    yaw_about_approach: float = 0.0,
) -> tuple[float, float, float, float]:
    """EEF +Z aligned to -normal (into the board). Returns (x, y, z, w)."""
    approach = -_norm(_v3(board_normal_world))
    rot = rotation_aligning_eef_z(approach, yaw_about_approach)
    return rotation_matrix_to_quaternion(rot)


def board_origin_pose(calib: BoardCalibration) -> tuple[list[float], tuple[float, float, float, float]]:
    rot = np.column_stack(
        (
            _v3(calib.x_axis),
            _v3(calib.y_axis),
            _v3(calib.z_axis),
        )
    )
    return list(calib.origin), rotation_matrix_to_quaternion(rot)


def square_center_on_surface(
    calib: BoardCalibration,
    square: str,
    *,
    square_size: float,
    surface_z_board: float,
    board_layout: str = 'ranks_x_files_y',
    file_mirror: bool = False,
) -> list[float]:
    return square_center_world(
        calib,
        square,
        square_size=square_size,
        z_board=surface_z_board,
        board_layout=board_layout,
        file_mirror=file_mirror,
    )


def grasp_height_along_normal(
    *,
    occupancy_z: float | None,
    piece_height: float,
    grasp_clearance: float,
    gripper_z_offset: float,
    z_is_piece_top: bool,
    board_surface_z_world: float,
) -> float:
    """World-frame height along +Z for a level board; callers offset along the normal."""
    if occupancy_z is None:
        base = float(board_surface_z_world)
        if z_is_piece_top:
            return base + float(piece_height) + float(gripper_z_offset)
        return base + float(piece_height) + float(grasp_clearance)

    z = float(occupancy_z)
    if z_is_piece_top:
        return z + float(gripper_z_offset)
    return z + float(piece_height) + float(grasp_clearance)


@dataclass(frozen=True)
class SquareGrasp:
    square: str
    square_xyz: tuple[float, float, float]
    grasp_xyz: tuple[float, float, float]
    hover_xyz: tuple[float, float, float]
    orientation_xyzw: tuple[float, float, float, float]
    piece_type: str
    used_occupancy_z: bool


def offset_along_normal(point: Sequence[float], normal: Sequence[float], distance: float) -> list[float]:
    p = _v3(point) + _norm(_v3(normal)) * float(distance)
    return p.tolist()


def build_square_grasp(
    calib: BoardCalibration,
    square: str,
    *,
    square_size: float,
    surface_z_board: float,
    approach_m: float,
    piece_type: str = 'pawn',
    occupancy_xyz: Sequence[float] | None = None,
    grasp_clearance: float = 0.015,
    gripper_z_offset: float = 0.0,
    z_is_piece_top: bool = False,
    board_layout: str = 'ranks_x_files_y',
    file_mirror: bool = False,
    piece_dims: Mapping[str, Sequence[float]] | None = None,
    yaw_about_approach: float = 0.0,
) -> SquareGrasp:
    """One square: surface center, grasp pose, hover pose, perpendicular orientation."""
    sq = normalize_square_name(square)
    ptype = normalize_piece_type(piece_type)
    _, height = piece_dimensions(ptype, piece_dims)
    normal = _v3(calib.z_axis)
    orientation = perpendicular_eef_quaternion(normal, yaw_about_approach=yaw_about_approach)

    square_xyz = square_center_on_surface(
        calib,
        sq,
        square_size=square_size,
        surface_z_board=surface_z_board,
        board_layout=board_layout,
        file_mirror=file_mirror,
    )
    used_z = occupancy_xyz is not None
    if occupancy_xyz is not None:
        xy_z = _v3(occupancy_xyz)
        # Keep detected / occupancy XY; Z is interpreted per z_is_piece_top.
        board_surface_world = float(xy_z[2]) if z_is_piece_top else float(xy_z[2])
        grasp_z = grasp_height_along_normal(
            occupancy_z=float(xy_z[2]),
            piece_height=height,
            grasp_clearance=grasp_clearance,
            gripper_z_offset=gripper_z_offset,
            z_is_piece_top=z_is_piece_top,
            board_surface_z_world=board_surface_world,
        )
        # Offset from occupancy XY along the normal by (grasp_z - occupancy_z) when the
        # board is level this equals world Z; when tilted, occupancy_z is the point's
        # world Z and we still add the remaining height along the normal.
        delta = grasp_z - float(xy_z[2])
        grasp_xyz = offset_along_normal(xy_z, normal, delta)
        square_xyz = [float(xy_z[0]), float(xy_z[1]), float(xy_z[2])]
    else:
        origin_z = float(board_to_base(calib, [0.0, 0.0, surface_z_board])[2])
        grasp_z = grasp_height_along_normal(
            occupancy_z=None,
            piece_height=height,
            grasp_clearance=grasp_clearance,
            gripper_z_offset=gripper_z_offset,
            z_is_piece_top=z_is_piece_top,
            board_surface_z_world=origin_z,
        )
        delta = grasp_z - float(square_xyz[2])
        grasp_xyz = offset_along_normal(square_xyz, normal, delta)

    hover_xyz = offset_along_normal(grasp_xyz, normal, approach_m)
    return SquareGrasp(
        square=sq,
        square_xyz=(float(square_xyz[0]), float(square_xyz[1]), float(square_xyz[2])),
        grasp_xyz=(float(grasp_xyz[0]), float(grasp_xyz[1]), float(grasp_xyz[2])),
        hover_xyz=(float(hover_xyz[0]), float(hover_xyz[1]), float(hover_xyz[2])),
        orientation_xyzw=orientation,
        piece_type=ptype,
        used_occupancy_z=used_z,
    )


def occupancy_source_target(data: Mapping) -> tuple[str | None, str | None]:
    def _first(*keys: str) -> str | None:
        for key in keys:
            value = data.get(key)
            if isinstance(value, str) and value.strip():
                try:
                    return normalize_square_name(value)
                except ValueError:
                    continue
        return None

    source = _first('source', 'from', 'from_square')
    target = _first('target', 'to', 'to_square', 'destination')
    return source, target


def build_board_grasps(
    calib: BoardCalibration,
    *,
    square_size: float,
    surface_z_board: float,
    approach_m: float,
    occupancy: Mapping | None = None,
    grasp_clearance: float = 0.015,
    gripper_z_offset: float = 0.0,
    z_is_piece_top: bool = False,
    board_layout: str = 'ranks_x_files_y',
    file_mirror: bool = False,
    piece_dims: Mapping[str, Sequence[float]] | None = None,
    yaw_about_approach: float = 0.0,
    squares: Iterable[str] | None = None,
    default_piece_type: str = 'pawn',
) -> dict[str, SquareGrasp]:
    """Build grasp/hover poses for 64 squares (or ``squares``).

    Occupied squares use occupancy XYZ (detected Z). Empty destination squares use
    the moving piece's height when source/target are present in occupancy.
    """
    occ = dict(occupancy) if occupancy else {}
    occ_xyz = extract_square_xyz_from_occupancy(occ) if occ else {}
    occ_pieces = extract_pieces_from_occupancy(occ) if occ else {}
    source, target = occupancy_source_target(occ)

    moving_type = default_piece_type
    if source and source in occ_pieces:
        moving_type = occ_pieces[source].piece_type

    wanted = [normalize_square_name(s) for s in squares] if squares is not None else list(iter_board_squares())
    out: dict[str, SquareGrasp] = {}
    for square in wanted:
        occ_pt = occ_xyz.get(square)
        if square in occ_pieces:
            ptype = occ_pieces[square].piece_type
        elif target is not None and square == target:
            ptype = moving_type
        else:
            ptype = default_piece_type
        xyz = occ_pt
        # Empty destination: keep calibrated XY, apply moving-piece height (no occupancy Z).
        if target is not None and square == target and square not in occ_pieces:
            xyz = None
        out[square] = build_square_grasp(
            calib,
            square,
            square_size=square_size,
            surface_z_board=surface_z_board,
            approach_m=approach_m,
            piece_type=ptype,
            occupancy_xyz=xyz,
            grasp_clearance=grasp_clearance,
            gripper_z_offset=gripper_z_offset,
            z_is_piece_top=z_is_piece_top,
            board_layout=board_layout,
            file_mirror=file_mirror,
            piece_dims=piece_dims,
            yaw_about_approach=yaw_about_approach,
        )
    return out


def frame_name(prefix: str, square: str) -> str:
    return f'{prefix.strip("/")}/{normalize_square_name(square)}'


def isaac_square_name(
    row: int,
    col: int,
    *,
    file_mirror: bool = False,
) -> str:
    """Map Isaac ``sq_{row}_{col}`` (row→Y/file, col→X/rank) to algebraic.

    ``neura_chess_world.py``: ranks along +X (col), files along +Y (row), white at low X.
    """
    rank_i = int(col)
    file_i = 7 - int(row) if file_mirror else int(row)
    if not (0 <= file_i <= 7 and 0 <= rank_i <= 7):
        raise ValueError(f'invalid Isaac square row={row} col={col}')
    return f'{FILES[file_i]}{RANKS[rank_i]}'
