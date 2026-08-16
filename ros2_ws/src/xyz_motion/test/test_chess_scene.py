"""Unit tests for chess planning scene builders (no ROS)."""

from __future__ import annotations

import math

from moveit_msgs.msg import CollisionObject
from visualization_msgs.msg import Marker

from xyz_motion.board_calibration import compute_board_calibration
from xyz_motion.chess_scene import (
    PieceState,
    _COLOR_DARK,
    _COLOR_LIGHT,
    _COLOR_PIECE_BLACK,
    _COLOR_PIECE_WHITE,
    board_collision_object,
    board_collision_squares,
    build_board_marker_array,
    build_piece_marker_array,
    build_piece_scene_diff,
    build_standard_start_pieces,
    should_rebuild_piece_snapshot,
    camp_for_square,
    extract_pieces_from_occupancy,
    extract_square_xyz_from_occupancy,
    is_chess_square_name,
    is_light_square,
    normalize_piece_type,
    piece_color,
    piece_dimensions,
    piece_board_yaw,
    piece_object_id,
    piece_removal_object,
    square_center_world,
    standard_start_piece_types,
)


def _example_calib():
    return compute_board_calibration(
        a1=[0.27, -0.16, 0.02],
        b1=[0.31, -0.16, 0.02],
        a2=[0.27, -0.12, 0.02],
        square_size=0.04,
    )


class TestChessSquareNames:
    def test_valid_square(self):
        assert is_chess_square_name('e4')
        assert piece_object_id('E4') == 'piece_e4'

    def test_invalid_square(self):
        assert not is_chess_square_name('image_1')


class TestPieceTypes:
    def test_normalize_aliases(self):
        assert normalize_piece_type('horse') == 'knight'
        assert normalize_piece_type('KNIGHT') == 'knight'

    def test_king_taller_than_pawn(self):
        _, pawn_h = piece_dimensions('pawn')
        _, king_h = piece_dimensions('king')
        assert king_h > pawn_h

    def test_standard_start_has_32_pieces(self):
        assert len(standard_start_piece_types()) == 32
        assert standard_start_piece_types()['e1'] == 'king'
        assert standard_start_piece_types()['e2'] == 'pawn'
        assert standard_start_piece_types()['e8'] == 'king'


class TestStandardStartPieces:
    def test_build_from_calibration(self):
        pieces = build_standard_start_pieces(_example_calib(), square_size=0.04, piece_z=0.01)
        assert len(pieces) == 32
        assert pieces['e1'].piece_type == 'king'
        assert pieces['b1'].piece_type == 'knight'
        assert pieces['e2'].piece_type == 'pawn'
        assert len(pieces['e1'].xyz) == 3

    def test_start_pieces_have_white_and_black_camps(self):
        pieces = build_standard_start_pieces(_example_calib(), square_size=0.04, piece_z=0.01)
        assert pieces['a1'].camp == 'white'
        assert pieces['a8'].camp == 'black'

    def test_ranks_layout_swaps_file_and_rank_steps(self):
        calib = _example_calib()
        classic_b1 = square_center_world(
            calib, 'b1', square_size=0.04, z_board=0.0, board_layout='files_x_ranks_y'
        )
        classic_a2 = square_center_world(
            calib, 'a2', square_size=0.04, z_board=0.0, board_layout='files_x_ranks_y'
        )
        ranks_b1 = square_center_world(
            calib, 'b1', square_size=0.04, z_board=0.0, board_layout='ranks_x_files_y'
        )
        ranks_a2 = square_center_world(
            calib, 'a2', square_size=0.04, z_board=0.0, board_layout='ranks_x_files_y'
        )
        assert ranks_b1 == classic_a2
        assert ranks_a2 == classic_b1


class TestSquareColors:
    def test_a1_dark_b1_light(self):
        assert not is_light_square(0, 0)
        assert is_light_square(1, 0)


class TestBoardCollisionObject:
    def test_legacy_plate_dimensions(self):
        co = board_collision_object(_example_calib(), frame_id='world')
        assert co.id == 'chess_board'
        assert list(co.primitives[0].dimensions) == [0.32, 0.32, 0.02]

    def test_per_square_collision_grid(self):
        squares = board_collision_squares(_example_calib(), frame_id='world')
        assert len(squares) == 64
        assert squares[0].id == 'board_sq_a1'


class TestBoardMarkers:
    def test_marker_array_has_64_squares_plus_clear(self):
        array = build_board_marker_array(_example_calib(), frame_id='world')
        assert array.markers[0].action == Marker.DELETEALL
        cubes = [m for m in array.markers if m.type == Marker.CUBE]
        assert len(cubes) == 64

    def test_a1_black_b1_yellow(self):
        array = build_board_marker_array(_example_calib(), frame_id='world')
        cubes = [m for m in array.markers if m.type == Marker.CUBE]
        assert cubes[0].color.r == _COLOR_DARK.r
        assert cubes[1].color.r == _COLOR_LIGHT.r


class TestShouldRebuildPieceSnapshot:
    def test_sparse_endgame_from_crowded_board(self):
        prev = {f'a{i}': PieceState((0.0, 0.0, 0.03), 'pawn') for i in range(1, 30)}
        active = {
            'e1': PieceState((0.29, 0.02, 0.03), 'king'),
            'e8': PieceState((0.57, 0.02, 0.03), 'king'),
        }
        assert should_rebuild_piece_snapshot(active, prev, full_snapshot_min_squares=16)

    def test_small_incremental_capture_uses_diff(self):
        prev = {
            'e1': PieceState((0.29, 0.02, 0.03), 'king'),
            'e2': PieceState((0.33, 0.02, 0.03), 'pawn'),
            'e8': PieceState((0.57, 0.02, 0.03), 'king'),
        }
        active = {
            'e1': PieceState((0.29, 0.02, 0.03), 'king'),
            'e4': PieceState((0.41, 0.02, 0.03), 'pawn'),
            'e8': PieceState((0.57, 0.02, 0.03), 'king'),
        }
        assert not should_rebuild_piece_snapshot(active, prev, full_snapshot_min_squares=16)


class TestPieceSceneDiff:
    def test_add_and_remove_pieces(self):
        frame = 'world'
        active = {
            'e2': PieceState((0.45, -0.10, 0.03), 'pawn'),
            'e4': PieceState((0.45, -0.06, 0.03), 'pawn'),
        }
        objects, new_map = build_piece_scene_diff(active, {}, frame_id=frame)
        assert set(new_map.keys()) == {'e2', 'e4'}
        assert len(objects) == 2
        assert all(co.operation == CollisionObject.ADD for co in objects)

        objects2, new_map2 = build_piece_scene_diff(
            {'e4': active['e4']}, new_map, frame_id=frame
        )
        assert set(new_map2.keys()) == {'e4'}
        assert CollisionObject.REMOVE in [co.operation for co in objects2]

    def test_king_taller_cylinder_than_pawn(self):
        active = {
            'e1': PieceState((0.45, -0.14, 0.03), 'king'),
            'e2': PieceState((0.45, -0.10, 0.03), 'pawn'),
        }
        objects, _ = build_piece_scene_diff(active, {}, frame_id='world')
        by_id = {co.id: co for co in objects}
        king_h = list(by_id['piece_e1'].primitives[0].dimensions)[0]
        pawn_h = list(by_id['piece_e2'].primitives[0].dimensions)[0]
        assert king_h > pawn_h

    def test_convex_hull_collision_objects(self):
        from xyz_motion.chess_piece_meshes import PieceMeshLibrary
        from visualization_msgs.msg import Marker

        library = PieceMeshLibrary()
        if not library.available():
            return
        active = {
            'e1': PieceState((0.45, -0.14, 0.01), 'king'),
            'e2': PieceState((0.45, -0.10, 0.01), 'pawn'),
        }
        objects, _ = build_piece_scene_diff(
            active, {}, frame_id='world', mesh_library=library, calib=_example_calib()
        )
        by_id = {co.id: co for co in objects}
        assert by_id['piece_e1'].meshes
        assert not by_id['piece_e1'].primitives
        assert abs(by_id['piece_e1'].mesh_poses[0].position.z - 0.01) < 0.005
        king_h = library.piece_height('king')
        pawn_h = library.piece_height('pawn')
        assert king_h > pawn_h

        markers = build_piece_marker_array(
            active, frame_id='world', mesh_library=library, calib=_example_calib()
        )
        meshes = [m for m in markers.markers if m.type == Marker.MESH_RESOURCE]
        assert len(meshes) == 2
        assert 'package://xyz_motion' in meshes[0].mesh_resource

    def test_knight_yaw_faces_opponent(self):
        calib = _example_calib()
        assert piece_board_yaw('knight', 'white', board_layout='ranks_x_files_y') == math.pi / 2
        assert piece_board_yaw('knight', 'black', board_layout='ranks_x_files_y') == 3 * math.pi / 2
        assert piece_board_yaw('pawn', 'white', board_layout='ranks_x_files_y') == 0.0

    def test_piece_type_change_remove_and_add(self):
        prev = {'e1': PieceState((0.45, -0.14, 0.03), 'pawn')}
        active = {'e1': PieceState((0.45, -0.14, 0.03), 'queen')}
        objects, _ = build_piece_scene_diff(active, prev, frame_id='world')
        ops = [co.operation for co in objects if co.id == 'piece_e1']
        assert CollisionObject.REMOVE in ops
        assert CollisionObject.ADD in ops


class TestPieceColors:
    def test_camp_from_rank(self):
        assert camp_for_square('a1') == 'white'
        assert camp_for_square('a8') == 'black'

    def test_piece_marker_colors(self):
        pieces = {
            'e1': PieceState((0.0, 0.0, 0.03), 'king', 'white'),
            'e8': PieceState((0.1, 0.1, 0.03), 'king', 'black'),
        }
        array = build_piece_marker_array(pieces, frame_id='world')
        cylinders = [m for m in array.markers if m.type == Marker.CYLINDER]
        assert len(cylinders) == 2
        assert cylinders[0].color.r == _COLOR_PIECE_WHITE.r
        assert cylinders[1].color.r == _COLOR_PIECE_BLACK.r
        assert piece_color('white').g == _COLOR_PIECE_WHITE.g


class TestExtractPieces:
    def test_from_squares_dict_with_type(self):
        data = {
            'squares': {
                'e2': {'x': 0.45, 'y': -0.10, 'z': 0.03, 'type': 'pawn'},
                'e1': {'x': 0.45, 'y': -0.14, 'z': 0.03, 'piece': 'king'},
            },
        }
        pieces = extract_pieces_from_occupancy(data)
        assert pieces['e2'].piece_type == 'pawn'
        assert pieces['e1'].piece_type == 'king'

    def test_camp_from_occupancy(self):
        data = {
            'squares': {
                'e2': {'x': 0.45, 'y': -0.10, 'z': 0.03, 'color': 'white'},
                'e7': {'x': 0.45, 'y': 0.10, 'z': 0.03, 'camp': 'black'},
            },
        }
        pieces = extract_pieces_from_occupancy(data)
        assert pieces['e2'].camp == 'white'
        assert pieces['e7'].camp == 'black'

    def test_xyz_helper_backward_compatible(self):
        data = {'squares': {'e2': {'x': 0.45, 'y': -0.10, 'z': 0.03}}}
        out = extract_square_xyz_from_occupancy(data)
        assert out['e2'] == (0.45, -0.10, 0.03)

    def test_e2_to_e4_pending_move_keeps_source_piece(self):
        """MTC planning files list source+target; piece must stay on source until picked."""
        from xyz_motion.chess_scene import strip_move_source_from_active

        data = {
            'source': 'e2',
            'target': 'e4',
            'squares': {
                'e2': {'x': 0.33, 'y': -0.02, 'z': 0.03, 'type': 'pawn', 'color': 'white'},
                'e4': {'x': 0.41, 'y': -0.02, 'z': 0.03},
            },
        }
        pieces = extract_pieces_from_occupancy(data)
        assert set(pieces.keys()) == {'e2'}
        strip_move_source_from_active(data, pieces)
        assert 'e2' in pieces

    def test_piece_removal_object(self):
        co = piece_removal_object('e2', frame_id='world')
        assert co.id == 'piece_e2'
        assert co.operation == CollisionObject.REMOVE
