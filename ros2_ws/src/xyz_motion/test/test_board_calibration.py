"""Unit tests for board calibration utilities (no ROS)."""

from __future__ import annotations

import pytest

from xyz_motion.board_calibration import (
    board_to_base,
    compute_board_calibration,
    square_center_base,
    square_center_board,
    square_name_to_indices,
)


def test_square_name_to_indices():
    assert square_name_to_indices('a1') == (0, 0)
    assert square_name_to_indices('h8') == (7, 7)
    assert square_name_to_indices('E4') == (4, 3)


def test_square_name_to_indices_rejects_invalid():
    with pytest.raises(ValueError, match='invalid square'):
        square_name_to_indices('a9')
    with pytest.raises(ValueError, match='invalid square'):
        square_name_to_indices('abc')


def test_square_center_board():
    p = square_center_board('a1', square_size=0.04)
    assert p == [0.02, 0.02, 0.0]
    p = square_center_board('h8', square_size=0.04, z=0.01)
    assert p == [0.3, 0.3, 0.01]


def test_square_center_board_ranks_layout():
    assert square_center_board('b1', 0.04, layout='ranks_x_files_y') == [0.02, 0.06, 0.0]
    assert square_center_board('a2', 0.04, layout='ranks_x_files_y') == [0.06, 0.02, 0.0]


def test_square_center_board_file_mirror():
    assert square_center_board('b1', 0.04, layout='ranks_x_files_y', file_mirror=True) == [
        0.02,
        0.26,
        0.0,
    ]
    assert square_center_board('g1', 0.04, layout='ranks_x_files_y', file_mirror=True) == [
        0.02,
        0.06,
        0.0,
    ]


def test_compute_calibration_identity_axes():
    # Base frame already aligned with board frame.
    a1 = [1.0, 2.0, 3.0]
    b1 = [1.04, 2.0, 3.0]
    a2 = [1.0, 2.04, 3.0]
    calib = compute_board_calibration(a1, b1, a2, square_size=0.04)

    assert calib.origin == a1
    assert pytest.approx(calib.x_axis, rel=1e-6, abs=1e-6) == [1.0, 0.0, 0.0]
    assert pytest.approx(calib.y_axis, rel=1e-6, abs=1e-6) == [0.0, 1.0, 0.0]
    assert pytest.approx(calib.z_axis, rel=1e-6, abs=1e-6) == [0.0, 0.0, 1.0]


def test_square_center_base_matches_expected_translation():
    a1 = [0.5, -0.2, 0.3]
    b1 = [0.54, -0.2, 0.3]
    a2 = [0.5, -0.16, 0.3]
    calib = compute_board_calibration(a1, b1, a2, square_size=0.04)

    # e4 => file=4, rank=3 => board [0.18, 0.14, 0.0] with files_x_ranks_y
    p = square_center_base(calib, 'e4', z=0.0, layout='files_x_ranks_y')
    assert pytest.approx(p, rel=1e-6, abs=1e-6) == [0.68, -0.06, 0.3]


def test_board_to_base_uses_axes():
    # Rotated board: x along +Y, y along -X.
    calib = compute_board_calibration(
        a1=[1.0, 1.0, 0.5],
        b1=[1.0, 1.04, 0.5],  # x-axis
        a2=[0.96, 1.0, 0.5],  # y-axis direction
        square_size=0.04,
    )
    p_base = board_to_base(calib, [0.04, 0.0, 0.0])
    assert pytest.approx(p_base, rel=1e-6, abs=1e-6) == [1.0, 1.04, 0.5]

