"""Board calibration utilities (no ROS).

The board frame is defined such that:
- X increases along files (a->b->...->h)
- Y increases along ranks (1->2->...->8)
- Z is the right-handed normal.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

import numpy as np


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

