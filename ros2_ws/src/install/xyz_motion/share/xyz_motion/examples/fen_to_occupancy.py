#!/usr/bin/env python3
"""Build chess_occupancy JSON from FEN (same XYZ grid as full_board examples)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from xyz_motion.board_calibration import compute_board_calibration, square_center_base

# Matches ranks_x_files_y + board_file_mirror in config/chess_scene.yaml
CALIB = compute_board_calibration(
    [0.27, -0.16, 0.02],
    [0.31, -0.16, 0.02],
    [0.27, -0.12, 0.02],
    0.04,
)
LAYOUT = 'ranks_x_files_y'
FILE_MIRROR = True
PIECE_Z = 0.01  # board-frame Z; world Z = board origin Z + 0.01 = 0.03
SQUARE_SIZE = 0.04

FEN_TYPE = {
    'p': 'pawn',
    'n': 'knight',
    'b': 'bishop',
    'r': 'rook',
    'q': 'queen',
    'k': 'king',
}


def square_to_xyz(square: str) -> tuple[float, float, float]:
    center = square_center_base(
        CALIB, square, z=PIECE_Z, square_size=SQUARE_SIZE, layout=LAYOUT, file_mirror=FILE_MIRROR
    )
    return round(center[0], 2), round(center[1], 2), round(center[2], 2)


def fen_to_occupancy(
    fen: str,
    *,
    turn: str,
    source: str = '',
    target: str = '',
    note: str = '',
) -> dict:
    board_part = fen.split()[0]
    squares: dict[str, dict] = {}
    for rank_idx, rank_str in enumerate(reversed(board_part.split('/'))):
        rank = rank_idx + 1
        file_i = 0
        for ch in rank_str:
            if ch.isdigit():
                file_i += int(ch)
                continue
            square = f'{chr(ord("a") + file_i)}{rank}'
            color = 'white' if ch.isupper() else 'black'
            x, y, z = square_to_xyz(square)
            squares[square] = {
                'x': x,
                'y': y,
                'z': z,
                'type': FEN_TYPE[ch.lower()],
                'color': color,
            }
            file_i += 1

    payload: dict = {'turn': turn, 'squares': squares}
    if source:
        payload['source'] = source
    if target:
        payload['target'] = target
    if note:
        payload['note'] = note
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('fen', help='FEN board position (first field only is used)')
    parser.add_argument('-o', '--output', type=Path, help='write JSON to this path')
    parser.add_argument('--turn', default='white', choices=('white', 'black'))
    parser.add_argument('--source', default='')
    parser.add_argument('--target', default='')
    parser.add_argument('--note', default='')
    args = parser.parse_args()

    payload = fen_to_occupancy(
        args.fen,
        turn=args.turn,
        source=args.source,
        target=args.target,
        note=args.note,
    )
    text = json.dumps(payload, indent=2) + '\n'
    if args.output:
        args.output.write_text(text, encoding='utf-8')
        print(f'wrote {args.output} ({len(payload["squares"])} squares)')
    else:
        print(text, end='')


if __name__ == '__main__':
    main()
