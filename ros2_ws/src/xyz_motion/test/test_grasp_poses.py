"""Unit tests for perpendicular chess grasp poses (no ROS)."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from xyz_motion.board_calibration import compute_board_calibration
from xyz_motion.chess_scene import board_surface_z, piece_dimensions
from xyz_motion.grasp_poses import (
    build_board_grasps,
    build_square_grasp,
    eef_z_world,
    frame_name,
    grasp_height_along_normal,
    isaac_square_name,
    perpendicular_eef_quaternion,
)


def _calib():
    return compute_board_calibration(
        a1=[0.27, -0.16, 0.02],
        b1=[0.31, -0.16, 0.02],
        a2=[0.27, -0.12, 0.02],
        square_size=0.04,
    )


def test_normal_is_world_plus_z():
    calib = _calib()
    assert pytest.approx(calib.z_axis, abs=1e-6) == [0.0, 0.0, 1.0]


def test_eef_z_points_into_board():
    q = perpendicular_eef_quaternion([0.0, 0.0, 1.0])
    tool_z = eef_z_world(q)
    assert pytest.approx(tool_z, abs=1e-6) == [0.0, 0.0, -1.0]


def test_tilted_board_normal_alignment():
    # 45° tilt about Y: a2 raised.
    calib = compute_board_calibration(
        a1=[0.0, 0.0, 0.0],
        b1=[0.04, 0.0, 0.0],
        a2=[0.0, 0.04, 0.04],
        square_size=0.04,
    )
    q = perpendicular_eef_quaternion(calib.z_axis)
    tool_z = eef_z_world(q)
    expected = -np.array(calib.z_axis) / np.linalg.norm(calib.z_axis)
    assert pytest.approx(tool_z, abs=1e-6) == expected.tolist()


def test_detected_z_is_piece_top():
    z = grasp_height_along_normal(
        occupancy_z=0.08,
        piece_height=0.034,
        grasp_clearance=0.015,
        gripper_z_offset=-0.01,
        z_is_piece_top=True,
        board_surface_z_world=0.03,
    )
    assert z == pytest.approx(0.07)


def test_occupancy_z_is_board_surface_plus_piece():
    z = grasp_height_along_normal(
        occupancy_z=0.03,
        piece_height=0.034,
        grasp_clearance=0.015,
        gripper_z_offset=0.0,
        z_is_piece_top=False,
        board_surface_z_world=0.03,
    )
    assert z == pytest.approx(0.079)


def test_king_grasp_higher_than_pawn():
    calib = _calib()
    pawn = build_square_grasp(
        calib, 'e2', square_size=0.04, surface_z_board=0.01, approach_m=0.08, piece_type='pawn'
    )
    king = build_square_grasp(
        calib, 'e2', square_size=0.04, surface_z_board=0.01, approach_m=0.08, piece_type='king'
    )
    assert king.grasp_xyz[2] > pawn.grasp_xyz[2]
    _, pawn_h = piece_dimensions('pawn')
    _, king_h = piece_dimensions('king')
    assert king.grasp_xyz[2] - pawn.grasp_xyz[2] == pytest.approx(king_h - pawn_h)


def test_hover_is_approach_along_normal():
    calib = _calib()
    g = build_square_grasp(
        calib, 'e4', square_size=0.04, surface_z_board=0.01, approach_m=0.08, piece_type='pawn'
    )
    assert g.hover_xyz[2] - g.grasp_xyz[2] == pytest.approx(0.08)
    assert g.hover_xyz[0] == pytest.approx(g.grasp_xyz[0])
    assert g.hover_xyz[1] == pytest.approx(g.grasp_xyz[1])


def test_occupancy_overrides_z():
    calib = _calib()
    occ = {
        'source': 'e2',
        'target': 'e4',
        'squares': {
            'e2': {'x': 0.33, 'y': -0.02, 'z': 0.05, 'type': 'pawn', 'color': 'white'},
            'e4': {'x': 0.41, 'y': -0.02, 'z': 0.03},
        },
    }
    grasps = build_board_grasps(
        calib,
        square_size=0.04,
        surface_z_board=board_surface_z(0.02),
        approach_m=0.08,
        occupancy=occ,
        grasp_clearance=0.015,
        z_is_piece_top=False,
        board_layout='ranks_x_files_y',
        file_mirror=True,
        squares=['e2', 'e4'],
    )
    assert grasps['e2'].used_occupancy_z
    assert grasps['e2'].grasp_xyz[0] == pytest.approx(0.33)
    assert grasps['e2'].grasp_xyz[2] == pytest.approx(0.05 + 0.034 + 0.015)
    # Empty destination uses moving pawn height on the calibrated surface (world z≈0.03).
    assert not grasps['e4'].used_occupancy_z
    assert grasps['e4'].piece_type == 'pawn'
    assert grasps['e4'].grasp_xyz[2] == pytest.approx(0.03 + 0.034 + 0.015)


def test_e2_to_e4_example_file():
    path = Path(__file__).resolve().parents[1] / 'config' / 'examples' / 'e2_to_e4.json'
    occ = json.loads(path.read_text(encoding='utf-8'))
    calib = _calib()
    grasps = build_board_grasps(
        calib,
        square_size=0.04,
        surface_z_board=0.01,
        approach_m=0.08,
        occupancy=occ,
        grasp_clearance=0.015,
        board_layout='ranks_x_files_y',
        file_mirror=True,
        squares=['e2', 'e4'],
    )
    assert frame_name('grasp', 'e2') == 'grasp/e2'
    assert grasps['e2'].grasp_xyz[2] == pytest.approx(0.03 + 0.034 + 0.015)


def test_isaac_square_names():
    assert isaac_square_name(0, 0, file_mirror=False) == 'a1'
    assert isaac_square_name(0, 3, file_mirror=False) == 'a4'
    assert isaac_square_name(4, 1, file_mirror=False) == 'e2'
    assert isaac_square_name(0, 0, file_mirror=True) == 'h1'
