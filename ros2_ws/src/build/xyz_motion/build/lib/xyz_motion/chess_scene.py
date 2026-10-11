"""Build MoveIt planning-scene collision objects and RViz markers for chess."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence

import numpy as np
from geometry_msgs.msg import Pose
from moveit_msgs.msg import CollisionObject, PlanningScene
from shape_msgs.msg import Mesh, SolidPrimitive
from std_msgs.msg import ColorRGBA
from visualization_msgs.msg import Marker, MarkerArray

from xyz_motion.board_calibration import (
    BoardCalibration,
    board_to_base,
    compute_board_calibration,
    square_center_board,
    square_name_to_indices,
)

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


def extract_pieces_from_occupancy(data: dict) -> dict[str, PieceState]:
    """Parse occupied squares with XYZ and optional piece type from chess_occupancy."""
    from xyz_motion.chess_xyz import chess_occupancy_to_pose6

    squares = data.get('squares')
    poses6 = chess_occupancy_to_pose6(data)
    known_types = _occupancy_piece_types(data)
    known_camps = _occupancy_camps(data)
    out: dict[str, PieceState] = {}
    for name, pose6 in poses6.items():
        if not is_chess_square_name(name):
            continue
        square = normalize_square_name(name)
        if isinstance(squares, dict):
            entry = squares.get(square) or squares.get(name)
            if entry is not None and not _square_entry_is_piece(entry):
                continue
        piece_type = known_types.get(square, 'pawn')
        camp = known_camps.get(square)
        out[square] = PieceState(
            xyz=(pose6[0], pose6[1], pose6[2]),
            piece_type=piece_type,
            camp=camp_for_square(square, camp),
        )
    return out


def extract_square_xyz_from_occupancy(data: dict) -> dict[str, tuple[float, float, float]]:
    """Parse square XYZ from occupancy (includes coords-only entries without piece type)."""
    from xyz_motion.chess_xyz import chess_occupancy_to_pose6

    out: dict[str, tuple[float, float, float]] = {}
    for name, pose6 in chess_occupancy_to_pose6(data).items():
        if not is_chess_square_name(name):
            continue
        square = normalize_square_name(name)
        out[square] = (float(pose6[0]), float(pose6[1]), float(pose6[2]))
    return out


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
