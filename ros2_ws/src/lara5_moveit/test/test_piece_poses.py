"""Unit tests for Isaac piece-pose lookup (no MoveIt / Isaac)."""

from __future__ import annotations

import json
import threading
import time
from pathlib import Path

import pytest

from lara5_moveit.moveit_chess import main, motion_steps
from lara5_moveit.piece_poses import (
    eef_targets,
    fetch_isaac_snapshot,
    load_snapshot,
    normalize_square,
    piece_at_square,
    square_xy,
)

SNAPSHOT = {
    'backend': 'test',
    'n': 2,
    'pieces': [
        {
            'name': 'Wp_pawn_4',
            'type': 'pawn',
            'color': 'white',
            'square': 'e2',
            'x': 0.31,
            'y': -0.02,
            'z': 0.02,
            'qw': 1.0,
            'qx': 0.0,
            'qy': 0.0,
            'qz': 0.0,
        },
        {
            'name': 'W_king_4',
            'type': 'king',
            'color': 'white',
            'square': 'e1',
            'x': 0.27,
            'y': -0.02,
            'z': 0.02,
            'qw': 1.0,
            'qx': 0.0,
            'qy': 0.0,
            'qz': 0.0,
        },
    ],
    'occupancy': {
        'e2': {
            'x': 0.31,
            'y': -0.02,
            'z': 0.02,
            'type': 'pawn',
            'color': 'white',
            'name': 'Wp_pawn_4',
        },
        'e1': {
            'x': 0.27,
            'y': -0.02,
            'z': 0.02,
            'type': 'king',
            'color': 'white',
            'name': 'W_king_4',
        },
    },
}


def test_normalize_square():
    assert normalize_square('E2') == 'e2'
    with pytest.raises(ValueError):
        normalize_square('e9')


def test_piece_at_square_from_occupancy():
    piece = piece_at_square(SNAPSHOT, 'e2')
    assert piece['type'] == 'pawn'
    assert piece['x'] == pytest.approx(0.31)
    assert piece['y'] == pytest.approx(-0.02)
    assert piece['z'] == pytest.approx(0.02)


def test_piece_at_square_type_filter():
    with pytest.raises(ValueError, match='not'):
        piece_at_square(SNAPSHOT, 'e2', piece_type='king')
    piece = piece_at_square(SNAPSHOT, 'e2', piece_type='pawn')
    assert piece['name'] == 'Wp_pawn_4'


def test_piece_at_square_missing():
    with pytest.raises(KeyError, match='e4'):
        piece_at_square(SNAPSHOT, 'e4')


def test_piece_from_pieces_list_without_occupancy():
    snap = {'pieces': SNAPSHOT['pieces']}
    piece = piece_at_square(snap, 'e1')
    assert piece['type'] == 'king'
    assert piece['qw'] == pytest.approx(1.0)


def test_square_xy_matches_isaac_board():
    x, y = square_xy('e2')
    assert x == pytest.approx(0.31)
    assert y == pytest.approx(-0.02)
    a1 = square_xy('a1')
    assert a1[0] == pytest.approx(0.27)


def test_eef_targets_pick_and_place():
    piece = piece_at_square(SNAPSHOT, 'e2')
    targets = eef_targets(piece, place_square='e4', snapshot=SNAPSHOT)
    assert targets['pick_grasp'][0] == pytest.approx(0.31)
    assert targets['pick_hover'][2] == pytest.approx(targets['pick_grasp'][2] + 0.08)
    assert targets['place_square'] == 'e4'
    assert targets['place_grasp'][0] == pytest.approx(0.39)
    assert targets['place_grasp'][1] == pytest.approx(-0.02)
    qx, qy, qz, qw = targets['orientation_xyzw']
    assert (qx * qx + qy * qy + qz * qz + qw * qw) == pytest.approx(1.0)


def test_load_snapshot_roundtrip(tmp_path: Path):
    path = tmp_path / 'pieces.json'
    path.write_text(json.dumps(SNAPSHOT), encoding='utf-8')
    loaded = load_snapshot(path)
    assert piece_at_square(loaded, 'e2')['name'] == 'Wp_pawn_4'


def test_fetch_isaac_snapshot(tmp_path: Path):
    ready = tmp_path / 'ready'
    request = tmp_path / 'request'
    done = tmp_path / 'done'
    json_out = tmp_path / 'pieces.json'
    ready.write_text('pieces=2\n', encoding='utf-8')

    def kit() -> None:
        deadline = time.time() + 2.0
        while time.time() < deadline:
            if request.is_file():
                json_out.write_text(json.dumps(SNAPSHOT), encoding='utf-8')
                done.write_text('ok n=2\n', encoding='utf-8')
                return
            time.sleep(0.01)
        raise AssertionError('request never appeared')

    worker = threading.Thread(target=kit, daemon=True)
    worker.start()
    snap = fetch_isaac_snapshot(
        timeout_s=2.0,
        ready=ready,
        request=request,
        done=done,
        json_out=json_out,
    )
    worker.join(timeout=2.0)
    assert piece_at_square(snap, 'e2')['type'] == 'pawn'


def test_fetch_isaac_snapshot_missing_kit(tmp_path: Path):
    with pytest.raises(FileNotFoundError, match='listener missing'):
        fetch_isaac_snapshot(
            timeout_s=0.1,
            ready=tmp_path / 'ready',
            request=tmp_path / 'request',
            done=tmp_path / 'done',
            json_out=tmp_path / 'out.json',
        )


def test_print_only_cli(tmp_path: Path, capsys):
    path = tmp_path / 'pieces.json'
    path.write_text(json.dumps(SNAPSHOT), encoding='utf-8')
    rc = main(['--poses-json', str(path), '--square', 'e2', '--to', 'e4', '--print-only'])
    assert rc == 0
    out = json.loads(capsys.readouterr().out)
    assert out['square'] == 'e2'
    assert out['place_square'] == 'e4'
    assert out['pick_grasp'][0] == pytest.approx(0.31)


def test_list_cli(tmp_path: Path, capsys):
    path = tmp_path / 'pieces.json'
    path.write_text(json.dumps(SNAPSHOT), encoding='utf-8')
    rc = main(['--poses-json', str(path), '--list'])
    assert rc == 0
    captured = capsys.readouterr().out
    assert 'Wp_pawn_4' in captured
    assert 'n=2' in captured


def test_missing_square_cli(tmp_path: Path, capsys, monkeypatch):
    monkeypatch.delenv('CHESS_SOURCE', raising=False)
    monkeypatch.delenv('CHESS_TARGET', raising=False)
    path = tmp_path / 'pieces.json'
    path.write_text(json.dumps(SNAPSHOT), encoding='utf-8')
    rc = main(['--poses-json', str(path), '--print-only'])
    assert rc == 1
    assert '--square' in capsys.readouterr().out


def test_motion_steps_pick_and_place():
    piece = piece_at_square(SNAPSHOT, 'e2')
    targets = eef_targets(piece, place_square='e4', snapshot=SNAPSHOT)
    steps = motion_steps(targets)
    kinds = [step['kind'] for step in steps]
    names = [step['name'] for step in steps]
    assert kinds[0] == 'gripper'
    assert 'named' in kinds
    assert 'pose' in kinds
    assert 'cartesian' in kinds
    assert 'pick hover' in names
    assert 'place hover' in names
    assert names[-1] == 'move to stand'
    assert steps[0]['goal'] == 'open'
    assert any(step.get('goal') == 'close' for step in steps)


def test_motion_steps_pick_only():
    piece = piece_at_square(SNAPSHOT, 'e2')
    targets = eef_targets(piece)
    names = [step['name'] for step in motion_steps(targets)]
    assert 'pick hover' in names
    assert 'place hover' not in names
    assert names[-1] == 'move to stand'
