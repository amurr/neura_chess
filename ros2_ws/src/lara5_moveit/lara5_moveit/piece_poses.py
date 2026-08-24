"""Read chess-piece world poses from the Isaac Sim RigidPrim snapshot."""

from __future__ import annotations

import json
import math
import time
from pathlib import Path
from typing import Any, Mapping

PIECES_REQUEST = Path('/tmp/neura_chess_pieces.request')
PIECES_DONE = Path('/tmp/neura_chess_pieces.done')
PIECES_READY = Path('/tmp/neura_chess_pieces.ready')
PIECES_JSON = Path('/tmp/neura_chess_pieces.json')

SQUARE_M = 0.04
BOARD_CENTER_X = 0.41
BOARD_CENTER_Y = 0.0
BOARD_ORIGIN = -4 * SQUARE_M
FILE_MIRROR = True

# Top-down EEF, same as lara5_chess_pick_place.py.
DOWN_RPY = (0.0, math.pi / 2.0, 0.0)
APPROACH_M = 0.08
GRASP_Z_OFFSET = 0.03


def normalize_square(square: str) -> str:
    """Return algebraic square in lowercase (e.g. 'e2')."""
    key = square.strip().lower()
    if len(key) != 2 or key[0] not in 'abcdefgh' or key[1] not in '12345678':
        raise ValueError(f'invalid chess square {square!r}')
    return key


def load_snapshot(path: str | Path) -> dict[str, Any]:
    """Load a Kit piece-pose JSON snapshot."""
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    if not isinstance(data, dict):
        raise ValueError('piece snapshot must be a JSON object')
    return data


def fetch_isaac_snapshot(
    *,
    timeout_s: float = 5.0,
    ready: Path = PIECES_READY,
    request: Path = PIECES_REQUEST,
    done: Path = PIECES_DONE,
    json_out: Path = PIECES_JSON,
) -> dict[str, Any]:
    """Ask the running world for a RigidPrim snapshot, then load it."""
    if not ready.is_file():
        raise FileNotFoundError(
            f'Kit piece-pose listener missing ({ready}). '
            'Start ./scripts/launch/launch_world.sh first.'
        )
    try:
        done.unlink(missing_ok=True)
    except TypeError:
        if done.exists():
            done.unlink()
    request.write_text('1\n', encoding='utf-8')
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        if done.is_file():
            return load_snapshot(json_out)
        time.sleep(0.02)
    raise TimeoutError(f'Kit did not write {done} in {timeout_s:.1f}s')


def _record(square: str, rec: Mapping[str, Any]) -> dict[str, Any]:
    return {
        'square': square,
        'name': rec.get('name', ''),
        'type': rec.get('type', 'pawn'),
        'color': rec.get('color'),
        'x': float(rec['x']),
        'y': float(rec['y']),
        'z': float(rec['z']),
        'qx': float(rec['qx']) if 'qx' in rec else 0.0,
        'qy': float(rec['qy']) if 'qy' in rec else 0.0,
        'qz': float(rec['qz']) if 'qz' in rec else 0.0,
        'qw': float(rec['qw']) if 'qw' in rec else 1.0,
    }


def piece_at_square(
    snapshot: Mapping[str, Any],
    square: str,
    piece_type: str | None = None,
) -> dict[str, Any]:
    """Return the piece occupying ``square`` from an Isaac snapshot."""
    sq = normalize_square(square)
    wanted = None if piece_type is None else piece_type.strip().lower()
    occupancy = snapshot.get('occupancy') or {}
    rec = occupancy.get(sq)
    if isinstance(rec, Mapping) and 'x' in rec:
        if wanted and str(rec.get('type', '')).lower() != wanted:
            raise ValueError(f'{sq} has type {rec.get("type")!r}, not {wanted!r}')
        return _record(sq, rec)
    for piece in snapshot.get('pieces') or []:
        if not isinstance(piece, Mapping):
            continue
        if str(piece.get('square', '')).lower() != sq:
            continue
        if wanted and str(piece.get('type', '')).lower() != wanted:
            continue
        return _record(sq, piece)
    raise KeyError(f'no piece on {sq} in Isaac snapshot')


def square_xy(square: str) -> tuple[float, float]:
    """Return world XY of a square center on the Isaac board."""
    sq = normalize_square(square)
    file_i = ord(sq[0]) - ord('a')
    rank_i = int(sq[1]) - 1
    row = 7 - file_i if FILE_MIRROR else file_i
    col = rank_i
    x = BOARD_CENTER_X + BOARD_ORIGIN + (col + 0.5) * SQUARE_M
    y = BOARD_CENTER_Y + BOARD_ORIGIN + (row + 0.5) * SQUARE_M
    return x, y


def rpy_to_quaternion(
    roll: float, pitch: float, yaw: float
) -> tuple[float, float, float, float]:
    """Return quaternion (x, y, z, w) from roll-pitch-yaw."""
    cr, sr = math.cos(roll * 0.5), math.sin(roll * 0.5)
    cp, sp = math.cos(pitch * 0.5), math.sin(pitch * 0.5)
    cy, sy = math.cos(yaw * 0.5), math.sin(yaw * 0.5)
    return (
        sr * cp * cy - cr * sp * sy,
        cr * sp * cy + sr * cp * sy,
        cr * cp * sy - sr * sp * cy,
        cr * cp * cy + sr * sp * sy,
    )


def eef_targets(
    piece: Mapping[str, Any],
    *,
    approach_m: float = APPROACH_M,
    grasp_z_offset: float = GRASP_Z_OFFSET,
    place_square: str | None = None,
    snapshot: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build hover/grasp XYZ and a downward EEF quaternion from a piece pose."""
    x, y, z = float(piece['x']), float(piece['y']), float(piece['z'])
    grasp_z = z + float(grasp_z_offset)
    hover_z = grasp_z + float(approach_m)
    qx, qy, qz, qw = rpy_to_quaternion(*DOWN_RPY)
    out: dict[str, Any] = {
        'pick_grasp': (x, y, grasp_z),
        'pick_hover': (x, y, hover_z),
        'orientation_xyzw': (qx, qy, qz, qw),
        'square': piece.get('square'),
        'type': piece.get('type'),
        'name': piece.get('name'),
    }
    if not place_square:
        return out
    dest_sq = normalize_square(place_square)
    dest_xy = None
    if snapshot is not None:
        rec = (snapshot.get('occupancy') or {}).get(dest_sq)
        if isinstance(rec, Mapping) and 'x' in rec:
            dest_xy = (float(rec['x']), float(rec['y']))
    if dest_xy is None:
        dest_xy = square_xy(dest_sq)
    out['place_grasp'] = (dest_xy[0], dest_xy[1], grasp_z)
    out['place_hover'] = (dest_xy[0], dest_xy[1], hover_z)
    out['place_square'] = dest_sq
    return out
