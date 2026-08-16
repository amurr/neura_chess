"""Unit tests for chess XYZ -> pose6 translation (no ROS)."""

from __future__ import annotations

import pytest

from xyz_motion.chess_xyz import chess_occupancy_to_pose6, xyz_to_pose6
from xyz_motion.poses import DEFAULT_VIEW_RPY

CUSTOM_RPY = [1.0, 0.5, -0.25]


class TestXyzToPose6:
    def test_uses_default_view_rpy(self):
        pose = xyz_to_pose6(0.4, 0.0, 0.35)
        assert pose[:3] == [0.4, 0.0, 0.35]
        assert pose[3:] == DEFAULT_VIEW_RPY

    def test_custom_fixed_rpy(self):
        pose = xyz_to_pose6(1.0, 2.0, 3.0, fixed_rpy=CUSTOM_RPY)
        assert pose == [1.0, 2.0, 3.0, *CUSTOM_RPY]

    def test_invalid_rpy_length(self):
        with pytest.raises(ValueError, match='fixed_rpy must have 3'):
            xyz_to_pose6(0.0, 0.0, 0.0, fixed_rpy=[0.0, 0.0])

    def test_coerces_numeric_strings_via_float(self):
        pose = xyz_to_pose6(0.4, 0.0, 0.35)
        assert all(isinstance(v, float) for v in pose)


class TestChessOccupancyToPose6:
    def test_squares_dict_xyz(self):
        data = {
            'squares': {
                'e4': {'x': 0.4, 'y': 0.0, 'z': 0.35},
                'e5': {'x': 0.41, 'y': 0.01, 'z': 0.35},
            },
            'turn': 'white',
        }
        poses = chess_occupancy_to_pose6(data)
        assert set(poses.keys()) == {'e4', 'e5'}
        assert poses['e4'][:3] == [0.4, 0.0, 0.35]
        assert poses['e4'][3:] == DEFAULT_VIEW_RPY
        assert poses['e5'][:3] == [0.41, 0.01, 0.35]

    def test_squares_list_xyz(self):
        data = {'squares': {'a1': [0.30, -0.20, 0.32]}}
        poses = chess_occupancy_to_pose6(data)
        assert poses['a1'][:3] == [0.30, -0.20, 0.32]
        assert poses['a1'][3:] == DEFAULT_VIEW_RPY

    def test_poses_key_alias(self):
        data = {'poses': {'d4': [0.38, 0.0, 0.34]}}
        poses = chess_occupancy_to_pose6(data)
        assert 'd4' in poses

    def test_top_level_square_keys(self):
        data = {
            'e4': [0.4, 0.0, 0.35],
            'turn': 'white',
            'fen': 'startpos',
        }
        poses = chess_occupancy_to_pose6(data)
        assert list(poses.keys()) == ['e4']

    def test_merges_squares_and_top_level(self):
        data = {
            'squares': {'e4': [0.4, 0.0, 0.35]},
            'e5': [0.41, 0.01, 0.35],
        }
        poses = chess_occupancy_to_pose6(data)
        assert set(poses.keys()) == {'e4', 'e5'}

    def test_custom_fixed_rpy_parameter(self):
        data = {'e4': [0.4, 0.0, 0.35]}
        poses = chess_occupancy_to_pose6(data, fixed_rpy=CUSTOM_RPY)
        assert poses['e4'][3:] == CUSTOM_RPY

    def test_empty_message(self):
        assert chess_occupancy_to_pose6({}) == {}

    def test_negative_coordinates(self):
        data = {'b2': [-0.1, 0.2, 0.25]}
        poses = chess_occupancy_to_pose6(data)
        assert poses['b2'][:3] == [-0.1, 0.2, 0.25]

    def test_rejects_joint_array_len6(self):
        with pytest.raises(ValueError, match='expected xyz'):
            chess_occupancy_to_pose6({'e4': [1, 2, 3, 4, 5, 6]})

    def test_rejects_string_square_reference(self):
        with pytest.raises(ValueError, match='string references'):
            chess_occupancy_to_pose6({'e4': 'stand'})

    def test_rejects_xyz_dict_missing_key(self):
        with pytest.raises(ValueError, match='x, y, z'):
            chess_occupancy_to_pose6({'e4': {'x': 1.0, 'y': 2.0}})

    def test_rejects_invalid_xyz_length(self):
        with pytest.raises(ValueError, match='expected 3 xyz'):
            chess_occupancy_to_pose6({'e4': [1.0, 2.0]})

    def test_rejects_non_object_json(self):
        with pytest.raises(TypeError, match='must be an object'):
            chess_occupancy_to_pose6([])  # type: ignore[arg-type]

    def test_rejects_invalid_square_name(self):
        with pytest.raises(ValueError, match='invalid square name'):
            chess_occupancy_to_pose6({'': [0.1, 0.2, 0.3]})

    def test_ignores_metadata_keys(self):
        data = {
            'turn': 'black',
            'target': 'e4',
            'board': [[None] * 8] * 8,
            'occupancy': {'e4': 'pawn'},
            'timestamp': 123,
            'fen': '...',
        }
        assert chess_occupancy_to_pose6(data) == {}

    def test_ignores_note_field(self):
        data = {
            'note': '1. e4 c5 Sicilian',
            'squares': {'e4': {'x': 0.45, 'y': -0.06, 'z': 0.03}},
        }
        poses = chess_occupancy_to_pose6(data)
        assert list(poses.keys()) == ['e4']

    def test_rpy_not_read_from_message(self):
        """Chess module must not supply rpy; fixed orientation is always applied."""
        data = {
            'e4': {
                'x': 0.4,
                'y': 0.0,
                'z': 0.35,
                'roll': 0.1,
                'pitch': 0.2,
                'yaw': 0.3,
            },
        }
        poses = chess_occupancy_to_pose6(data)
        assert poses['e4'][3:] == DEFAULT_VIEW_RPY
