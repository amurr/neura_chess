#!/usr/bin/env python3
"""Generate config/examples/*.json board snapshots (ranks_x_files_y + board calibration)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

_PKG_ROOT = Path(__file__).resolve().parents[1]
if str(_PKG_ROOT) not in sys.path:
    sys.path.insert(0, str(_PKG_ROOT))

from xyz_motion.board_calibration import compute_board_calibration, square_center_base, square_name_to_indices

FILES = 'abcdefgh'
BACK = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
BOARD_THICKNESS = 0.02
PIECE_Z = BOARD_THICKNESS / 2.0
CALIB = compute_board_calibration(
    [0.27, -0.16, 0.02],
    [0.31, -0.16, 0.02],
    [0.27, -0.12, 0.02],
    0.04,
)
LAYOUT = 'ranks_x_files_y'
FILE_MIRROR = True
OUT = _PKG_ROOT / 'config' / 'examples'


def standard_types() -> dict[str, str]:
    types: dict[str, str] = {}
    for i, file in enumerate(FILES):
        back = BACK[i]
        types[f'{file}1'] = back
        types[f'{file}2'] = 'pawn'
        types[f'{file}7'] = 'pawn'
        types[f'{file}8'] = back
    return types


def camp(square: str) -> str:
    _, rank_i = square_name_to_indices(square)
    if rank_i <= 1:
        return 'white'
    if rank_i >= 6:
        return 'black'
    return 'white'


def apply_moves(types: dict[str, str], moves: list[tuple]) -> dict[str, str]:
    out = dict(types)
    for move in moves:
        src, dst = move[0], move[1]
        piece_type = move[2] if len(move) > 2 else out.get(src, 'pawn')
        out.pop(src, None)
        out[dst] = piece_type
    return out


def to_payload(
    types: dict[str, str],
    *,
    turn: str,
    source: str | None = None,
    target: str | None = None,
    note: str = '',
) -> dict:
    squares: dict = {}
    for square in sorted(types.keys()):
        center = square_center_base(
            CALIB, square, z=PIECE_Z, square_size=0.04, layout=LAYOUT, file_mirror=FILE_MIRROR
        )
        squares[square] = {
            'x': round(center[0], 4),
            'y': round(center[1], 4),
            'z': round(center[2], 4),
            'type': types[square],
            'color': camp(square),
        }
    payload: dict = {'turn': turn, 'squares': squares}
    if source:
        payload['source'] = source
    if target:
        payload['target'] = target
    if note:
        payload['note'] = note
    return payload


POSITIONS = [
    ('standard_start.json', standard_types(), 'white', None, None, 'Initial position (32 pieces)'),
    (
        'full_board_after_e4_e5.json',
        apply_moves(standard_types(), [('e2', 'e4'), ('e7', 'e5')]),
        'white',
        'e2',
        'e4',
        '1. e4 e5',
    ),
    (
        'full_board_after_d4_d5.json',
        apply_moves(standard_types(), [('d2', 'd4'), ('d7', 'd5')]),
        'white',
        'd2',
        'd4',
        '1. d4 d5',
    ),
    (
        'full_board_after_d2d3.json',
        apply_moves(standard_types(), [('d2', 'd3')]),
        'black',
        'd2',
        'd3',
        '1. d2 d3',
    ),
    (
        'full_board_after_nf3_nc6.json',
        apply_moves(
            standard_types(),
            [
                ('e2', 'e4'),
                ('e7', 'e5'),
                ('g1', 'f3', 'knight'),
                ('b8', 'c6', 'knight'),
            ],
        ),
        'white',
        'g1',
        'f3',
        '1. e4 e5 2. Nf3 Nc6',
    ),
    (
        'full_board_after_italian.json',
        apply_moves(
            standard_types(),
            [
                ('e2', 'e4'),
                ('e7', 'e5'),
                ('g1', 'f3', 'knight'),
                ('b8', 'c6', 'knight'),
                ('f1', 'c4', 'bishop'),
                ('f8', 'c5', 'bishop'),
            ],
        ),
        'white',
        'f1',
        'c4',
        'Italian: 1. e4 e5 2. Nf3 Nc6 3. Bc4 Bc5',
    ),
    (
        'full_board_after_e4_c5_sicilian.json',
        apply_moves(standard_types(), [('e2', 'e4'), ('c7', 'c5')]),
        'white',
        'c7',
        'c5',
        '1. e4 c5 Sicilian',
    ),
    (
        'full_board_after_queens_gambit.json',
        apply_moves(standard_types(), [('d2', 'd4'), ('d7', 'd5'), ('c2', 'c4')]),
        'black',
        'c2',
        'c4',
        "Queen's Gambit: 1. d4 d5 2. c4",
    ),
    (
        'full_board_after_london_attack.json',
        apply_moves(
            standard_types(),
            [
                ('d2', 'd4'),
                ('d7', 'd5'),
                ('c1', 'f4', 'bishop'),
                ('g8', 'f6', 'knight'),
                ('e2', 'e3'),
                ('e7', 'e6'),
                ('g1', 'f3', 'knight'),
                ('f8', 'd6', 'bishop'),
            ],
        ),
        'white',
        'c1',
        'f4',
        'London Attack: 1. d4 d5 2. Bf4 Nf6 3. e3 e6 4. Nf3 Bd6',
    ),
]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for fname, types, turn, src, tgt, note in POSITIONS:
        path = OUT / fname
        path.write_text(
            json.dumps(to_payload(types, turn=turn, source=src, target=tgt, note=note), indent=2)
            + '\n',
            encoding='utf-8',
        )
        print(f'wrote {fname} ({len(types)} pieces)')


if __name__ == '__main__':
    main()
