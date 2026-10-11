#!/usr/bin/env python3
"""
this file publishes the chessboard and the 32 pieces into MoveIt’s planning scene so the arm treats them as obstacles, and it draws the same board and pieces in RViz. Board pose and piece sizes come from chess_scene.yaml; occupancy updates on /chess_occupancy can move or remove pieces.

Started by orient.launch.py:

    ros2 run lara5_moveit chess_scene_collisions
"""

from __future__ import annotations

import json
import math
import re
import struct
import time
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Iterable, Mapping, Sequence

import numpy as np
import rclpy
from geometry_msgs.msg import Point, Pose
from moveit_msgs.msg import CollisionObject, PlanningScene
from rcl_interfaces.msg import ParameterDescriptor
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, QoSProfile
from shape_msgs.msg import Mesh, MeshTriangle, SolidPrimitive
from std_msgs.msg import ColorRGBA, String
from std_srvs.srv import Trigger
from visualization_msgs.msg import Marker, MarkerArray

CHESS_OCCUPANCY_TOPIC = '/chess_occupancy'
_PKG = 'lara5_moveit'
_HULL_SUBDIR = Path('meshes') / 'chess_pieces' / 'collision_hulls'


def _v3(xyz: Sequence[float]) -> np.ndarray:
    if len(xyz) != 3:
        raise ValueError("expected 3 elements for xyz")
    return np.array([float(xyz[0]), float(xyz[1]), float(xyz[2])], dtype=float)


def _norm(v: np.ndarray) -> np.ndarray:
    n = float(np.linalg.norm(v))
    if n == 0.0:
        raise ValueError("cannot normalize zero vector")
    return v / n


@dataclass(frozen=True)
class BoardCalibration:
    origin: list[float]
    x_axis: list[float]
    y_axis: list[float]
    z_axis: list[float]


def square_name_to_indices(square: str) -> tuple[int, int]:
    s = (square or "").strip().lower()
    if len(s) != 2:
        raise ValueError(f"invalid square {square!r}")
    file_c, rank_c = s[0], s[1]
    if file_c < "a" or file_c > "h" or rank_c < "1" or rank_c > "8":
        raise ValueError(f"invalid square {square!r}")
    file_i = ord(file_c) - ord("a")
    rank_i = ord(rank_c) - ord("1")
    return file_i, rank_i


def square_center_board(
    square: str,
    square_size: float,
    z: float = 0.0,
    *,
    layout: str = 'ranks_x_files_y',
    file_mirror: bool = False,
) -> list[float]:
    """Board-frame square centre.

    layouts:
      files_x_ranks_y — file index along board X, rank along board Y (classic).
      ranks_x_files_y — rank along board X (arm faces rank 1 at low X), file along board Y.

    file_mirror: flip the file axis (a↔h). Use when square labels on the physical board
    run opposite to the calibrated +Y file direction.
    """
    file_i, rank_i = square_name_to_indices(square)
    s = float(square_size)
    if file_mirror:
        file_i = 7 - file_i
    if layout == 'ranks_x_files_y':
        return [(rank_i + 0.5) * s, (file_i + 0.5) * s, float(z)]
    return [(file_i + 0.5) * s, (rank_i + 0.5) * s, float(z)]


def compute_board_calibration(
    a1: Sequence[float],
    b1: Sequence[float],
    a2: Sequence[float],
    square_size: float,
) -> BoardCalibration:
    origin = _v3(a1)
    x_vec = _v3(b1) - origin
    y_vec = _v3(a2) - origin

    # Axes in base frame. We treat the provided points as a single-square step.
    x_axis = _norm(x_vec / float(square_size))
    y_axis_raw = _norm(y_vec / float(square_size))
    z_axis = _norm(np.cross(x_axis, y_axis_raw))
    y_axis = _norm(np.cross(z_axis, x_axis))

    return BoardCalibration(
        origin=origin.tolist(),
        x_axis=x_axis.tolist(),
        y_axis=y_axis.tolist(),
        z_axis=z_axis.tolist(),
    )


def board_to_base(calib: BoardCalibration, p_board: Sequence[float]) -> list[float]:
    p = _v3(p_board)
    o = _v3(calib.origin)
    x = _v3(calib.x_axis)
    y = _v3(calib.y_axis)
    z = _v3(calib.z_axis)
    out = o + x * p[0] + y * p[1] + z * p[2]
    return out.tolist()


def square_center_base(
    calib: BoardCalibration,
    square: str,
    z: float = 0.0,
    square_size: float = 0.04,
    *,
    layout: str = 'ranks_x_files_y',
    file_mirror: bool = False,
) -> list[float]:
    p_board = square_center_board(
        square, square_size=square_size, z=z, layout=layout, file_mirror=file_mirror
    )
    return board_to_base(calib, p_board)



PIECE_MESH_TYPES = frozenset({'pawn', 'rook', 'knight', 'bishop', 'queen', 'king'})


@dataclass(frozen=True)
class PieceMeshInfo:
    piece_type: str
    mesh: Mesh
    height_m: float
    base_diameter_m: float


def _package_mesh_dir() -> Path | None:
    try:
        from ament_index_python.packages import get_package_share_directory

        return Path(get_package_share_directory(_PKG)) / _HULL_SUBDIR
    except Exception:
        return None


def _source_mesh_dir() -> Path:
    installed = _package_mesh_dir()
    if installed is not None and installed.is_dir():
        return installed
    return Path(__file__).resolve().parent.parent / _HULL_SUBDIR


def load_binary_stl(path: Path) -> tuple[list[tuple[float, float, float]], list[tuple[int, int, int]]]:
    data = path.read_bytes()
    tri_count = struct.unpack_from('<I', data, 80)[0]
    raw_verts: list[tuple[float, float, float]] = []
    offset = 84
    for _ in range(tri_count):
        offset += 12
        tri: list[int] = []
        for __ in range(3):
            x, y, z = struct.unpack_from('<fff', data, offset)
            raw_verts.append((x, y, z))
            tri.append(len(raw_verts) - 1)
            offset += 12
        offset += 2
    return raw_verts, [(tri[0], tri[1], tri[2])]


def stl_to_shape_mesh(path: Path) -> Mesh:
    vertices, triangles = load_binary_stl(path)
    mesh = Mesh()
    mesh.vertices = [Point(x=float(x), y=float(y), z=float(z)) for x, y, z in vertices]
    mesh.triangles = [
        MeshTriangle(vertex_indices=[int(a), int(b), int(c)]) for a, b, c in triangles
    ]
    return mesh


def _mesh_height(mesh: Mesh) -> float:
    if not mesh.vertices:
        return 0.0
    return max(float(v.z) for v in mesh.vertices)


def _mesh_base_diameter(mesh: Mesh) -> float:
    if not mesh.vertices:
        return 0.0
    xs = [float(v.x) for v in mesh.vertices]
    ys = [float(v.y) for v in mesh.vertices]
    return max(max(xs) - min(xs), max(ys) - min(ys))


class PieceMeshLibrary:
    """Cached convex-hull meshes keyed by piece type."""

    def __init__(self, mesh_dir: Path | None = None) -> None:
        self._mesh_dir = mesh_dir if mesh_dir is not None else _source_mesh_dir()

    @property
    def mesh_dir(self) -> Path:
        return self._mesh_dir

    def available(self) -> bool:
        return all((self._mesh_dir / f'{ptype}.stl').is_file() for ptype in PIECE_MESH_TYPES)

    @lru_cache(maxsize=len(PIECE_MESH_TYPES))
    def get(self, piece_type: str) -> PieceMeshInfo:
        ptype = piece_type.strip().lower()
        if ptype not in PIECE_MESH_TYPES:
            raise ValueError(f'unknown piece type {piece_type!r}')
        path = self._mesh_dir / f'{ptype}.stl'
        if not path.is_file():
            raise FileNotFoundError(f'collision hull missing: {path}')
        mesh = stl_to_shape_mesh(path)
        return PieceMeshInfo(
            piece_type=ptype,
            mesh=mesh,
            height_m=_mesh_height(mesh),
            base_diameter_m=_mesh_base_diameter(mesh),
        )

    def piece_height(self, piece_type: str) -> float:
        return self.get(piece_type).height_m

    def mesh_resource_uri(self, piece_type: str) -> str:
        ptype = piece_type.strip().lower()
        if ptype not in PIECE_MESH_TYPES:
            raise ValueError(f'unknown piece type {piece_type!r}')
        return f'package://{_PKG}/meshes/chess_pieces/collision_hulls/{ptype}.stl'


@lru_cache(maxsize=1)
def default_piece_mesh_library() -> PieceMeshLibrary:
    return PieceMeshLibrary()

_CHESS_SQUARE_RE = re.compile(r'^[a-h][1-8]$', re.IGNORECASE)
_BOARD_ID = 'chess_board'
_BOARD_SQ_PREFIX = 'board_sq_'
_BOARD_MARKER_NS = 'chess_board'
_PIECE_MARKER_NS = 'chess_pieces'
_FILES = 'abcdefgh'
_RANKS = '12345678'
BOARD_LAYOUTS = frozenset({'files_x_ranks_y', 'ranks_x_files_y'})

_COLOR_LIGHT = ColorRGBA(r=0.95, g=0.82, b=0.20, a=1.0)
_COLOR_DARK = ColorRGBA(r=0.08, g=0.08, b=0.08, a=1.0)
_COLOR_PIECE_WHITE = ColorRGBA(r=0.93, g=0.93, b=0.88, a=1.0)
_COLOR_PIECE_BLACK = ColorRGBA(r=0.12, g=0.12, b=0.14, a=1.0)

PIECE_TYPES = frozenset({'pawn', 'rook', 'knight', 'bishop', 'queen', 'king'})
PIECE_TYPE_ALIASES = {
    'horse': 'knight',
    'knights': 'knight',
    'horses': 'knight',
    'kn': 'knight',
    'n': 'knight',
    'b': 'bishop',
    'r': 'rook',
    'q': 'queen',
    'k': 'king',
    'p': 'pawn',
}

# Default collision sizes (metres) for ~4 cm squares (conservative / planning-friendly).
DEFAULT_PIECE_DIMENSIONS: dict[str, tuple[float, float]] = {
    'pawn': (0.018, 0.034),
    'bishop': (0.022, 0.047),
    'knight': (0.024, 0.049),
    'rook': (0.026, 0.044),
    'queen': (0.027, 0.058),
    'king': (0.029, 0.066),
}

_BACK_RANK_TYPES = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']


@dataclass(frozen=True)
class PieceState:
    xyz: tuple[float, float, float]
    piece_type: str = 'pawn'
    camp: str = 'white'


def normalize_board_layout(layout: str) -> str:
    key = (layout or 'ranks_x_files_y').strip().lower()
    if key not in BOARD_LAYOUTS:
        raise ValueError(f'invalid board_layout {layout!r}; use {sorted(BOARD_LAYOUTS)}')
    return key


def camp_for_square(square: str, camp: str | None = None) -> str:
    if camp is not None and str(camp).strip():
        c = str(camp).strip().lower()
        if c in ('white', 'black'):
            return c
    _, rank_i = square_name_to_indices(square)
    if rank_i <= 1:
        return 'white'
    if rank_i >= 6:
        return 'black'
    return 'white'


def piece_color(camp: str) -> ColorRGBA:
    return _COLOR_PIECE_WHITE if camp == 'white' else _COLOR_PIECE_BLACK


def normalize_piece_type(value: str | None, default: str = 'pawn') -> str:
    if not value or not str(value).strip():
        return default
    key = str(value).strip().lower()
    key = PIECE_TYPE_ALIASES.get(key, key)
    if key not in PIECE_TYPES:
        raise ValueError(f'invalid piece type {value!r}; expected one of {sorted(PIECE_TYPES)}')
    return key


def piece_dimensions(
    piece_type: str,
    overrides: Mapping[str, Sequence[float]] | None = None,
    *,
    default_diameter: float = 0.035,
    default_height: float = 0.05,
) -> tuple[float, float]:
    """Return (diameter, height) for a piece type."""
    ptype = normalize_piece_type(piece_type)
    if overrides and ptype in overrides:
        vals = overrides[ptype]
        if len(vals) >= 2:
            return float(vals[0]), float(vals[1])
    if ptype in DEFAULT_PIECE_DIMENSIONS:
        return DEFAULT_PIECE_DIMENSIONS[ptype]
    return float(default_diameter), float(default_height)


def standard_start_piece_types() -> dict[str, str]:
    """Standard chess start: ranks 1, 2, 7, 8 (32 pieces)."""
    types: dict[str, str] = {}
    for i, file in enumerate(_FILES):
        back = _BACK_RANK_TYPES[i]
        types[f'{file}1'] = back
        types[f'{file}2'] = 'pawn'
        types[f'{file}7'] = 'pawn'
        types[f'{file}8'] = back
    return types


def build_standard_start_pieces(
    calib: BoardCalibration,
    *,
    square_size: float = 0.04,
    piece_z: float | None = None,
    board_thickness: float = 0.02,
    board_layout: str = 'ranks_x_files_y',
    file_mirror: bool = False,
) -> dict[str, PieceState]:
    """Square -> piece state for the standard initial chess layout."""
    layout = normalize_board_layout(board_layout)
    if piece_z is None:
        piece_z = board_surface_z(board_thickness)
    start_types = standard_start_piece_types()
    pieces: dict[str, PieceState] = {}
    for square, piece_type in start_types.items():
        center = square_center_world(
            calib,
            square,
            square_size=square_size,
            z_board=piece_z,
            board_layout=layout,
            file_mirror=file_mirror,
        )
        pieces[square] = PieceState(
            xyz=(center[0], center[1], center[2]),
            piece_type=piece_type,
            camp=camp_for_square(square),
        )
    return pieces


def is_chess_square_name(name: str) -> bool:
    return bool(_CHESS_SQUARE_RE.match((name or '').strip()))


def normalize_square_name(name: str) -> str:
    s = (name or '').strip().lower()
    if not is_chess_square_name(s):
        raise ValueError(f'invalid chess square name: {name!r}')
    square_name_to_indices(s)
    return s


def load_board_calibration(
    a1: Sequence[float],
    b1: Sequence[float],
    a2: Sequence[float],
    square_size: float,
) -> BoardCalibration:
    return compute_board_calibration(a1, b1, a2, square_size=square_size)


def rotation_matrix_to_quaternion(rotation: np.ndarray) -> tuple[float, float, float, float]:
    m = np.asarray(rotation, dtype=float).reshape(3, 3)
    trace = float(m[0, 0] + m[1, 1] + m[2, 2])
    if trace > 0.0:
        s = math.sqrt(trace + 1.0) * 2.0
        qw = 0.25 * s
        qx = (m[2, 1] - m[1, 2]) / s
        qy = (m[0, 2] - m[2, 0]) / s
        qz = (m[1, 0] - m[0, 1]) / s
    elif m[0, 0] > m[1, 1] and m[0, 0] > m[2, 2]:
        s = math.sqrt(1.0 + m[0, 0] - m[1, 1] - m[2, 2]) * 2.0
        qw = (m[2, 1] - m[1, 2]) / s
        qx = 0.25 * s
        qy = (m[0, 1] + m[1, 0]) / s
        qz = (m[0, 2] + m[2, 0]) / s
    elif m[1, 1] > m[2, 2]:
        s = math.sqrt(1.0 + m[1, 1] - m[0, 0] - m[2, 2]) * 2.0
        qw = (m[0, 2] - m[2, 0]) / s
        qx = (m[0, 1] + m[1, 0]) / s
        qy = 0.25 * s
        qz = (m[1, 2] + m[2, 1]) / s
    else:
        s = math.sqrt(1.0 + m[2, 2] - m[0, 0] - m[1, 1]) * 2.0
        qw = (m[1, 0] - m[0, 1]) / s
        qx = (m[0, 2] + m[2, 0]) / s
        qy = (m[1, 2] + m[2, 1]) / s
        qz = 0.25 * s
    return float(qx), float(qy), float(qz), float(qw)


def calib_to_pose(calib: BoardCalibration, position: Sequence[float]) -> Pose:
    rot = np.column_stack(
        [
            np.array(calib.x_axis, dtype=float),
            np.array(calib.y_axis, dtype=float),
            np.array(calib.z_axis, dtype=float),
        ]
    )
    qx, qy, qz, qw = rotation_matrix_to_quaternion(rot)
    pose = Pose()
    pose.position.x = float(position[0])
    pose.position.y = float(position[1])
    pose.position.z = float(position[2])
    pose.orientation.x = qx
    pose.orientation.y = qy
    pose.orientation.z = qz
    pose.orientation.w = qw
    return pose


def board_surface_z(board_thickness: float) -> float:
    """Board-frame Z of the top playing surface (matches RViz square markers)."""
    return float(board_thickness) / 2.0


def piece_board_yaw(
    piece_type: str,
    camp: str,
    *,
    board_layout: str = 'ranks_x_files_y',
) -> float:
    """Yaw (rad) about board +Z; mesh knights default facing +board Y."""
    if normalize_piece_type(piece_type) != 'knight':
        return 0.0
    layout = normalize_board_layout(board_layout)
    c = camp_for_square('a1', camp)
    if layout == 'ranks_x_files_y':
        # White faces +board X (toward black); black faces -board X; +π flips mesh default.
        base = -math.pi / 2.0 if c == 'white' else math.pi / 2.0
        return base + math.pi
    base = 0.0 if c == 'white' else math.pi
    return base + math.pi


def piece_pose_on_board(
    calib: BoardCalibration,
    xyz: Sequence[float],
    *,
    piece_type: str,
    camp: str,
    board_layout: str = 'ranks_x_files_y',
) -> Pose:
    """Piece pose aligned to the board with optional per-type yaw (knights)."""
    rot = np.column_stack(
        [
            np.array(calib.x_axis, dtype=float),
            np.array(calib.y_axis, dtype=float),
            np.array(calib.z_axis, dtype=float),
        ]
    )
    yaw = piece_board_yaw(piece_type, camp, board_layout=board_layout)
    if abs(yaw) > 1e-12:
        c, s = math.cos(yaw), math.sin(yaw)
        rot = rot @ np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]], dtype=float)
    qx, qy, qz, qw = rotation_matrix_to_quaternion(rot)
    pose = Pose()
    pose.position.x = float(xyz[0])
    pose.position.y = float(xyz[1])
    pose.position.z = float(xyz[2])
    pose.orientation.x = qx
    pose.orientation.y = qy
    pose.orientation.z = qz
    pose.orientation.w = qw
    return pose


def is_light_square(file_i: int, rank_i: int, *, file_mirror: bool = False) -> bool:
    """True for yellow/light squares; a1 (0, 0) is dark."""
    if file_mirror:
        file_i = 7 - int(file_i)
    return (int(file_i) + int(rank_i)) % 2 == 1


def square_color(file_i: int, rank_i: int, *, file_mirror: bool = False) -> ColorRGBA:
    return _COLOR_LIGHT if is_light_square(file_i, rank_i, file_mirror=file_mirror) else _COLOR_DARK


def board_square_object_id(square: str) -> str:
    return f'{_BOARD_SQ_PREFIX}{normalize_square_name(square)}'


def square_center_world(
    calib: BoardCalibration,
    square: str,
    *,
    square_size: float,
    z_board: float = 0.0,
    board_layout: str = 'ranks_x_files_y',
    file_mirror: bool = False,
) -> list[float]:
    layout = normalize_board_layout(board_layout)
    p_board = square_center_board(
        square, square_size, z_board, layout=layout, file_mirror=file_mirror
    )
    return board_to_base(calib, p_board)


def iter_board_squares() -> Iterable[str]:
    for rank in _RANKS:
        for file in _FILES:
            yield f'{file}{rank}'


def board_collision_object(
    calib: BoardCalibration,
    *,
    frame_id: str,
    square_size: float = 0.04,
    thickness: float = 0.02,
    object_id: str = _BOARD_ID,
) -> CollisionObject:
    """Legacy single-plate board collision (prefer board_collision_squares)."""
    s = float(square_size)
    t = float(thickness)
    center_board = [4.0 * s, 4.0 * s, -t / 2.0]
    center_world = board_to_base(calib, center_board)

    box = SolidPrimitive()
    box.type = SolidPrimitive.BOX
    box.dimensions = [8.0 * s, 8.0 * s, t]

    co = CollisionObject()
    co.header.frame_id = frame_id
    co.id = object_id
    co.operation = CollisionObject.ADD
    co.primitives.append(box)
    co.primitive_poses.append(calib_to_pose(calib, center_world))
    return co


def legacy_board_removal(frame_id: str) -> CollisionObject:
    co = CollisionObject()
    co.header.frame_id = frame_id
    co.id = _BOARD_ID
    co.operation = CollisionObject.REMOVE
    return co


def board_collision_squares(
    calib: BoardCalibration,
    *,
    frame_id: str,
    square_size: float = 0.04,
    thickness: float = 0.02,
    board_layout: str = 'ranks_x_files_y',
    file_mirror: bool = False,
) -> list[CollisionObject]:
    """One thin box per square for collision (64 objects)."""
    layout = normalize_board_layout(board_layout)
    s = float(square_size)
    t = float(thickness)
    z_center = -t / 2.0
    objects: list[CollisionObject] = []

    for square in iter_board_squares():
        file_i, rank_i = square_name_to_indices(square)
        center_world = square_center_world(
            calib,
            square,
            square_size=s,
            z_board=z_center,
            board_layout=layout,
            file_mirror=file_mirror,
        )
        box = SolidPrimitive()
        box.type = SolidPrimitive.BOX
        box.dimensions = [s, s, t]

        co = CollisionObject()
        co.header.frame_id = frame_id
        co.id = board_square_object_id(square)
        co.operation = CollisionObject.ADD
        co.primitives.append(box)
        co.primitive_poses.append(calib_to_pose(calib, center_world))
        objects.append(co)

    return objects


def build_board_marker_array(
    calib: BoardCalibration,
    *,
    frame_id: str,
    square_size: float = 0.04,
    thickness: float = 0.02,
    board_layout: str = 'ranks_x_files_y',
    file_mirror: bool = False,
    stamp=None,
) -> MarkerArray:
    """Colored 8x8 board for RViz (yellow / black squares)."""
    layout = normalize_board_layout(board_layout)
    s = float(square_size)
    t = float(thickness)
    array = MarkerArray()

    clear = Marker()
    clear.header.frame_id = frame_id
    if stamp is not None:
        clear.header.stamp = stamp
    clear.ns = _BOARD_MARKER_NS
    clear.id = 0
    clear.action = Marker.DELETEALL
    array.markers.append(clear)

    marker_id = 1
    for square in iter_board_squares():
        file_i, rank_i = square_name_to_indices(square)
        center_world = square_center_world(
            calib,
            square,
            square_size=s,
            z_board=0.0,
            board_layout=layout,
            file_mirror=file_mirror,
        )

        marker = Marker()
        marker.header.frame_id = frame_id
        if stamp is not None:
            marker.header.stamp = stamp
        marker.ns = _BOARD_MARKER_NS
        marker.id = marker_id
        marker_id += 1
        marker.type = Marker.CUBE
        marker.action = Marker.ADD
        marker.pose = calib_to_pose(calib, center_world)
        marker.scale.x = s
        marker.scale.y = s
        marker.scale.z = t
        marker.color = square_color(file_i, rank_i, file_mirror=file_mirror)
        array.markers.append(marker)

    return array


def piece_object_id(square: str) -> str:
    return f'piece_{normalize_square_name(square)}'


def _copy_shape_mesh(mesh: Mesh) -> Mesh:
    out = Mesh()
    out.vertices = list(mesh.vertices)
    out.triangles = list(mesh.triangles)
    return out


def piece_mesh_collision_object(
    square: str,
    xyz: Sequence[float],
    piece_type: str,
    mesh_library,
    *,
    frame_id: str,
    camp: str = 'white',
    calib: BoardCalibration | None = None,
    board_layout: str = 'ranks_x_files_y',
    operation: int = CollisionObject.ADD,
) -> CollisionObject:
    """Convex-hull collision object; mesh base centred in XY with Z on board surface."""
    info = mesh_library.get(normalize_piece_type(piece_type))

    if calib is not None:
        pose = piece_pose_on_board(
            calib,
            xyz,
            piece_type=piece_type,
            camp=camp,
            board_layout=board_layout,
        )
    else:
        pose = Pose()
        pose.position.x = float(xyz[0])
        pose.position.y = float(xyz[1])
        pose.position.z = float(xyz[2])
        pose.orientation.w = 1.0

    co = CollisionObject()
    co.header.frame_id = frame_id
    co.id = piece_object_id(square)
    co.operation = operation
    co.meshes.append(_copy_shape_mesh(info.mesh))
    co.mesh_poses.append(pose)
    return co


def piece_collision_height(
    piece_type: str,
    *,
    mesh_library=None,
    dimension_overrides: Mapping[str, Sequence[float]] | None = None,
    default_diameter: float = 0.035,
    default_height: float = 0.05,
) -> float:
    """Vertical extent used for attach offsets and RViz markers."""
    if mesh_library is not None:
        return float(mesh_library.piece_height(normalize_piece_type(piece_type)))
    _, height = piece_dimensions(
        piece_type,
        dimension_overrides,
        default_diameter=default_diameter,
        default_height=default_height,
    )
    return float(height)


def piece_collision_object(
    square: str,
    xyz: Sequence[float],
    *,
    frame_id: str,
    piece_type: str = 'pawn',
    camp: str = 'white',
    diameter: float = 0.035,
    height: float = 0.05,
    operation: int = CollisionObject.ADD,
    mesh_library=None,
    calib: BoardCalibration | None = None,
    board_layout: str = 'ranks_x_files_y',
) -> CollisionObject:
    if mesh_library is not None:
        return piece_mesh_collision_object(
            square,
            xyz,
            piece_type,
            mesh_library,
            frame_id=frame_id,
            camp=camp,
            calib=calib,
            board_layout=board_layout,
            operation=operation,
        )

    cylinder = SolidPrimitive()
    cylinder.type = SolidPrimitive.CYLINDER
    cylinder.dimensions = [float(height), float(diameter) / 2.0]

    pose = Pose()
    pose.position.x = float(xyz[0])
    pose.position.y = float(xyz[1])
    pose.position.z = float(xyz[2]) + float(height) / 2.0
    pose.orientation.w = 1.0

    co = CollisionObject()
    co.header.frame_id = frame_id
    co.id = piece_object_id(square)
    co.operation = operation
    co.primitives.append(cylinder)
    co.primitive_poses.append(pose)
    return co


def piece_removal_object(square: str, *, frame_id: str) -> CollisionObject:
    co = CollisionObject()
    co.header.frame_id = frame_id
    co.id = piece_object_id(square)
    co.operation = CollisionObject.REMOVE
    return co


_RESERVED_OCCUPANCY_KEYS = frozenset({
    'turn', 'fen', 'timestamp', 'note', 'comment', 'description',
    'occupancy', 'board', 'poses', 'squares',
    'target', 'source', 'from', 'from_square', 'to', 'to_square', 'destination',
    'speed', 'acceleration', 'enable_safety',
    'close_cmd', 'open_cmd', 'gripper_pause_sec', 'camera_settle_sec',
})


def _xyz_from_value(value: object) -> tuple[float, float, float] | None:
    if isinstance(value, dict) and all(k in value for k in ('x', 'y', 'z')):
        return float(value['x']), float(value['y']), float(value['z'])
    if isinstance(value, (list, tuple)) and len(value) >= 3:
        return float(value[0]), float(value[1]), float(value[2])
    return None


def _occupancy_xyz(data: dict) -> dict[str, tuple[float, float, float]]:
    """Square name → (x, y, z) from occupancy JSON."""
    out: dict[str, tuple[float, float, float]] = {}

    def ingest(mapping: dict) -> None:
        for name, value in mapping.items():
            key = str(name)
            if key in _RESERVED_OCCUPANCY_KEYS or not is_chess_square_name(key):
                continue
            xyz = _xyz_from_value(value)
            if xyz is not None:
                out[normalize_square_name(key)] = xyz

    for section in ('squares', 'occupancy', 'board', 'poses'):
        if isinstance(data.get(section), dict):
            ingest(data[section])
    ingest(data)
    return out


def extract_pieces_from_occupancy(data: dict) -> dict[str, PieceState]:
    """Parse occupied squares with XYZ and optional piece type from chess_occupancy."""
    squares = data.get('squares')
    xyzs = _occupancy_xyz(data)
    known_types = _occupancy_piece_types(data)
    known_camps = _occupancy_camps(data)
    out: dict[str, PieceState] = {}
    for name, xyz in xyzs.items():
        square = normalize_square_name(name)
        if isinstance(squares, dict):
            entry = squares.get(square) or squares.get(name)
            if entry is not None and not _square_entry_is_piece(entry):
                continue
        piece_type = known_types.get(square, 'pawn')
        camp = known_camps.get(square)
        out[square] = PieceState(
            xyz=xyz,
            piece_type=piece_type,
            camp=camp_for_square(square, camp),
        )
    return out


def extract_square_xyz_from_occupancy(data: dict) -> dict[str, tuple[float, float, float]]:
    """Parse square XYZ from occupancy (includes coords-only entries without piece type)."""
    return dict(_occupancy_xyz(data))


def _occupancy_piece_types(data: dict) -> dict[str, str]:
    """Read optional piece types from squares/occupancy/board sections."""
    types: dict[str, str] = {}

    def ingest_mapping(mapping: dict) -> None:
        for name, value in mapping.items():
            if not is_chess_square_name(str(name)):
                continue
            square = normalize_square_name(str(name))
            if isinstance(value, dict):
                for key in ('type', 'piece', 'piece_type'):
                    if key in value:
                        types[square] = normalize_piece_type(str(value[key]))
                        break
            elif isinstance(value, str) and value.strip() and not _looks_like_xyz_container(value):
                try:
                    types[square] = normalize_piece_type(value)
                except ValueError:
                    pass

    if isinstance(data.get('squares'), dict):
        ingest_mapping(data['squares'])
    if isinstance(data.get('occupancy'), dict):
        ingest_mapping(data['occupancy'])
    if isinstance(data.get('board'), dict):
        ingest_mapping(data['board'])

    return types


def _occupancy_camps(data: dict) -> dict[str, str]:
    """Read optional camp (white/black) from squares/occupancy/board sections."""
    camps: dict[str, str] = {}

    def ingest_mapping(mapping: dict) -> None:
        for name, value in mapping.items():
            if not is_chess_square_name(str(name)):
                continue
            square = normalize_square_name(str(name))
            if isinstance(value, dict):
                for key in ('camp', 'color', 'side'):
                    if key in value:
                        c = str(value[key]).strip().lower()
                        if c in ('white', 'black'):
                            camps[square] = c
                        break

    if isinstance(data.get('squares'), dict):
        ingest_mapping(data['squares'])
    if isinstance(data.get('occupancy'), dict):
        ingest_mapping(data['occupancy'])
    if isinstance(data.get('board'), dict):
        ingest_mapping(data['board'])

    return camps


def _looks_like_xyz_container(value: str) -> bool:
    return value.strip().startswith('[') or value.strip().startswith('{')


def _square_entry_is_piece(value: object) -> bool:
    """True when a squares[] entry describes a piece (not coords-only for an empty square)."""
    if not isinstance(value, dict):
        return False
    return any(key in value for key in ('type', 'piece', 'piece_type', 'color', 'camp'))


def occupancy_move_source(data: dict) -> str | None:
    """Return source square from a move message (d2-d3 etc.), if present."""
    for key in ('source', 'from', 'from_square'):
        val = data.get(key)
        if isinstance(val, str) and is_chess_square_name(val):
            return normalize_square_name(val)
    return None


def strip_move_source_from_active(data: dict, active: dict[str, PieceState]) -> None:
    """Drop a stale source square after a completed move (piece already left source)."""
    src = occupancy_move_source(data)
    if src is None or src in active:
        return
    active.pop(src, None)


def should_rebuild_piece_snapshot(
    active_pieces: Mapping[str, PieceState],
    previous_pieces: Mapping[str, PieceState],
    *,
    full_snapshot_min_squares: int,
) -> bool:
    """
    Decide between incremental diff vs remove-all-then-add.

    MoveIt often drops ADD/MOVE updates when a diff carries many REMOVEs in
    separate batched messages (crowded board → sparse endgame). Prefer a full
    rebuild whenever the new message is a large position refresh.
    """
    if len(active_pieces) >= max(1, full_snapshot_min_squares):
        return True
    prev_keys = set(previous_pieces.keys())
    active_keys = set(active_pieces.keys())
    removed = len(prev_keys - active_keys)
    if removed > len(active_pieces):
        return True
    type_changes = sum(
        1
        for sq in active_keys & prev_keys
        if previous_pieces[sq].piece_type != active_pieces[sq].piece_type
    )
    return type_changes > 4


def build_full_piece_snapshot_objects(
    active_pieces: Mapping[str, PieceState],
    previous_pieces: Mapping[str, PieceState],
    *,
    frame_id: str,
    dimension_overrides: Mapping[str, Sequence[float]] | None = None,
    default_diameter: float = 0.035,
    default_height: float = 0.05,
    mesh_library=None,
    calib: BoardCalibration | None = None,
    board_layout: str = 'ranks_x_files_y',
) -> list[CollisionObject]:
    """Remove every previous piece, then ADD the full active set (no ghost squares)."""
    objects: list[CollisionObject] = []
    for square in sorted(previous_pieces.keys()):
        objects.append(piece_removal_object(square, frame_id=frame_id))
    objects.extend(
        build_piece_collision_objects(
            active_pieces,
            frame_id=frame_id,
            dimension_overrides=dimension_overrides,
            default_diameter=default_diameter,
            default_height=default_height,
            mesh_library=mesh_library,
            calib=calib,
            board_layout=board_layout,
        )
    )
    return objects


def build_piece_scene_diff(
    active_pieces: Mapping[str, PieceState],
    previous_pieces: Mapping[str, PieceState],
    *,
    frame_id: str,
    dimension_overrides: Mapping[str, Sequence[float]] | None = None,
    default_diameter: float = 0.035,
    default_height: float = 0.05,
    mesh_library=None,
    calib: BoardCalibration | None = None,
    board_layout: str = 'ranks_x_files_y',
) -> tuple[list[CollisionObject], dict[str, PieceState]]:
    """Return collision objects to apply and the new active piece map."""
    prev = dict(previous_pieces)
    new_set = set(active_pieces.keys())
    objects: list[CollisionObject] = []

    for square in sorted(set(prev.keys()) - new_set):
        objects.append(piece_removal_object(square, frame_id=frame_id))

    for square in sorted(active_pieces.keys()):
        piece = active_pieces[square]
        diameter, height = piece_dimensions(
            piece.piece_type,
            dimension_overrides,
            default_diameter=default_diameter,
            default_height=default_height,
        )
        prev_piece = prev.get(square)
        if prev_piece is None:
            op = CollisionObject.ADD
        elif prev_piece.piece_type != piece.piece_type:
            objects.append(piece_removal_object(square, frame_id=frame_id))
            op = CollisionObject.ADD
        else:
            op = CollisionObject.MOVE

        objects.append(
            piece_collision_object(
                square,
                piece.xyz,
                frame_id=frame_id,
                piece_type=piece.piece_type,
                camp=piece.camp,
                diameter=diameter,
                height=height,
                operation=op,
                mesh_library=mesh_library,
                calib=calib,
                board_layout=board_layout,
            )
        )

    return objects, dict(active_pieces)


def build_piece_collision_objects(
    pieces: Mapping[str, PieceState],
    *,
    frame_id: str,
    dimension_overrides: Mapping[str, Sequence[float]] | None = None,
    default_diameter: float = 0.035,
    default_height: float = 0.05,
    mesh_library=None,
    calib: BoardCalibration | None = None,
    board_layout: str = 'ranks_x_files_y',
) -> list[CollisionObject]:
    """ADD collision objects for all pieces (startup / full refresh)."""
    objects: list[CollisionObject] = []
    for square in sorted(pieces.keys()):
        piece = pieces[square]
        diameter, height = piece_dimensions(
            piece.piece_type,
            dimension_overrides,
            default_diameter=default_diameter,
            default_height=default_height,
        )
        objects.append(
            piece_collision_object(
                square,
                piece.xyz,
                frame_id=frame_id,
                piece_type=piece.piece_type,
                camp=piece.camp,
                diameter=diameter,
                height=height,
                operation=CollisionObject.ADD,
                mesh_library=mesh_library,
                calib=calib,
                board_layout=board_layout,
            )
        )
    return objects


def build_piece_marker_array(
    pieces: Mapping[str, PieceState],
    *,
    frame_id: str,
    dimension_overrides: Mapping[str, Sequence[float]] | None = None,
    default_diameter: float = 0.035,
    default_height: float = 0.05,
    stamp=None,
    mesh_library=None,
    calib: BoardCalibration | None = None,
    board_layout: str = 'ranks_x_files_y',
) -> MarkerArray:
    """Colored piece markers for RViz (mesh hulls or fallback cylinders)."""
    array = MarkerArray()

    clear = Marker()
    clear.header.frame_id = frame_id
    if stamp is not None:
        clear.header.stamp = stamp
    clear.ns = _PIECE_MARKER_NS
    clear.id = 0
    clear.action = Marker.DELETEALL
    array.markers.append(clear)

    marker_id = 1
    for square in sorted(pieces.keys()):
        piece = pieces[square]
        diameter, height = piece_dimensions(
            piece.piece_type,
            dimension_overrides,
            default_diameter=default_diameter,
            default_height=default_height,
        )
        use_mesh = mesh_library is not None
        if use_mesh:
            height = piece_collision_height(
                piece.piece_type,
                mesh_library=mesh_library,
                dimension_overrides=dimension_overrides,
                default_diameter=default_diameter,
                default_height=default_height,
            )
        marker = Marker()
        marker.header.frame_id = frame_id
        if stamp is not None:
            marker.header.stamp = stamp
        marker.ns = _PIECE_MARKER_NS
        marker.id = marker_id
        marker_id += 1
        marker.action = Marker.ADD
        if use_mesh and calib is not None:
            marker.type = Marker.MESH_RESOURCE
            marker.mesh_resource = mesh_library.mesh_resource_uri(piece.piece_type)
            marker.mesh_use_embedded_materials = False
            pose = piece_pose_on_board(
                calib,
                piece.xyz,
                piece_type=piece.piece_type,
                camp=piece.camp,
                board_layout=board_layout,
            )
            marker.pose = pose
            marker.scale.x = 1.0
            marker.scale.y = 1.0
            marker.scale.z = 1.0
        elif use_mesh:
            marker.type = Marker.MESH_RESOURCE
            marker.mesh_resource = mesh_library.mesh_resource_uri(piece.piece_type)
            marker.mesh_use_embedded_materials = False
            marker.pose.position.x = float(piece.xyz[0])
            marker.pose.position.y = float(piece.xyz[1])
            marker.pose.position.z = float(piece.xyz[2])
            marker.pose.orientation.w = 1.0
            marker.scale.x = 1.0
            marker.scale.y = 1.0
            marker.scale.z = 1.0
        else:
            marker.type = Marker.CYLINDER
            marker.pose.position.x = float(piece.xyz[0])
            marker.pose.position.y = float(piece.xyz[1])
            marker.pose.position.z = float(piece.xyz[2]) + float(height) / 2.0
            marker.pose.orientation.w = 1.0
            marker.scale.x = float(diameter)
            marker.scale.y = float(diameter)
            marker.scale.z = float(height)
        marker.color = piece_color(piece.camp)
        array.markers.append(marker)

    return array


def make_planning_scene_diff(collision_objects: Iterable[CollisionObject]) -> PlanningScene:
    scene = PlanningScene()
    scene.is_diff = True
    scene.world.collision_objects.extend(collision_objects)
    return scene


class ChessSceneCollisions(Node):
    def __init__(self, **kwargs) -> None:
        super().__init__('chess_scene_collisions', **kwargs)

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
            f'chess_scene_collisions ready frame={self._frame_id!r} topic={scene_topic!r} '
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
                    'true to clear, or restart chess_scene_collisions to restore initial layout.'
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
    node = ChessSceneCollisions()
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
