"""
Translate chess_occupancy JSON (XYZ only) into TCP pose6 targets.

High-level chess module publishes square positions in metres; roll/pitch/yaw are
always taken from DEFAULT_VIEW_RPY (not from the message).
"""

from __future__ import annotations

from xyz_motion.poses import DEFAULT_VIEW_RPY

CHESS_OCCUPANCY_TOPIC = '/chess_occupancy'

_RESERVED_JSON_KEYS = frozenset({
    'turn', 'fen', 'timestamp', 'note', 'comment', 'description',
    'occupancy', 'board', 'poses', 'squares',
    'target', 'source', 'from', 'from_square', 'to', 'to_square', 'destination',
    'speed', 'acceleration', 'enable_safety',
    'close_cmd', 'open_cmd', 'gripper_pause_sec', 'camera_settle_sec',
})


def xyz_to_pose6(
    x: float,
    y: float,
    z: float,
    fixed_rpy: list[float] | None = None,
) -> list[float]:
    """Build [x, y, z, roll, pitch, yaw] with fixed orientation (m, rad)."""
    rpy = list(fixed_rpy if fixed_rpy is not None else DEFAULT_VIEW_RPY)
    if len(rpy) != 3:
        raise ValueError(f'fixed_rpy must have 3 values, got {len(rpy)}')
    return [float(x), float(y), float(z), float(rpy[0]), float(rpy[1]), float(rpy[2])]


def _xyz_from_value(value) -> tuple[float, float, float]:
    """Parse chess square value -> (x, y, z) in metres."""
    if isinstance(value, dict):
        keys = ('x', 'y', 'z')
        if not all(k in value for k in keys):
            raise ValueError('xyz object must contain x, y, z keys')
        return float(value['x']), float(value['y']), float(value['z'])
    if isinstance(value, (list, tuple)):
        if len(value) == 3:
            return float(value[0]), float(value[1]), float(value[2])
        if len(value) == 6:
            raise ValueError(
                'expected xyz [x, y, z]; got 6 values — '
                'use joint poses only via move_joints stand, not chess JSON'
            )
        raise ValueError(f'expected 3 xyz values, got {len(value)}')
    raise ValueError(f'unsupported xyz value type: {type(value).__name__}')


def chess_occupancy_to_pose6(
    data: dict,
    fixed_rpy: list[float] | None = None,
) -> dict[str, list[float]]:
    """
    Translate chess_occupancy JSON into name -> [x, y, z, roll, pitch, yaw].

    Supported JSON (chess module sends XYZ only):
      {"squares": {"e4": {"x": 0.4, "y": 0.0, "z": 0.35}, "e5": [0.41, 0.01, 0.35]}}
      {"poses": {"e4": [0.4, 0.0, 0.35]}}
      {"e4": {"x": 0.4, "y": 0.0, "z": 0.35}}

    Metadata keys (turn, fen, board, target, ...) are ignored.
    """
    if not isinstance(data, dict):
        raise TypeError('chess_occupancy JSON must be an object')

    result: dict[str, list[float]] = {}

    def merge_mapping(mapping: dict) -> None:
        for name, value in mapping.items():
            if not isinstance(name, str) or not name:
                raise ValueError(f'invalid square name: {name!r}')
            if isinstance(value, str):
                raise ValueError(
                    f'square {name!r}: string references are not supported; send x,y,z'
                )
            x, y, z = _xyz_from_value(value)
            result[name] = xyz_to_pose6(x, y, z, fixed_rpy=fixed_rpy)

    if isinstance(data.get('squares'), dict):
        merge_mapping(data['squares'])
    if isinstance(data.get('poses'), dict):
        merge_mapping(data['poses'])

    for key, value in data.items():
        if key in _RESERVED_JSON_KEYS:
            continue
        if not isinstance(key, str) or not key:
            raise ValueError(f'invalid square name: {key!r}')
        if isinstance(value, str):
            raise ValueError(
                f'square {key!r}: string references are not supported; send x,y,z'
            )
        if isinstance(value, (list, tuple, dict)):
            x, y, z = _xyz_from_value(value)
            result[key] = xyz_to_pose6(x, y, z, fixed_rpy=fixed_rpy)

    return result
