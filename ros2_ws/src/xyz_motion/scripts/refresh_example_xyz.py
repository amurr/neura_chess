#!/usr/bin/env python3
"""Recompute x/y/z in config/examples/*.json from square names (ranks_x_files_y)."""

from __future__ import annotations

import json
from pathlib import Path

from xyz_motion.board_calibration import compute_board_calibration, square_center_base

CALIB = compute_board_calibration(
    [0.27, -0.16, 0.02],
    [0.31, -0.16, 0.02],
    [0.27, -0.12, 0.02],
    0.04,
)
LAYOUT = 'ranks_x_files_y'
FILE_MIRROR = True
PIECE_Z = 0.01  # board-frame Z; world Z = board origin Z + 0.01 = 0.03
EXAMPLES = Path(__file__).resolve().parents[1] / 'config' / 'examples'


def refresh_square_xyz(square: str) -> dict[str, float]:
    center = square_center_base(
        CALIB, square, z=PIECE_Z, square_size=0.04, layout=LAYOUT, file_mirror=FILE_MIRROR
    )
    return {
        'x': round(center[0], 4),
        'y': round(center[1], 4),
        'z': round(center[2], 4),
    }


def refresh_payload(payload: dict) -> dict:
    squares = payload.get('squares')
    if not isinstance(squares, dict):
        return payload
    for square, entry in squares.items():
        if not isinstance(entry, dict):
            continue
        xyz = refresh_square_xyz(str(square))
        entry['x'] = xyz['x']
        entry['y'] = xyz['y']
        entry['z'] = xyz['z']
    return payload


def main() -> None:
    for path in sorted(EXAMPLES.glob('*.json')):
        payload = json.loads(path.read_text(encoding='utf-8'))
        refreshed = refresh_payload(payload)
        path.write_text(json.dumps(refreshed, indent=2) + '\n', encoding='utf-8')
        n = len(refreshed.get('squares', {}))
        print(f'refreshed {path.name} ({n} squares)')


if __name__ == '__main__':
    main()
