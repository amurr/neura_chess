#!/usr/bin/env python3
"""Generate board=big hover and grasp SRDF states from taught h1_hover.

Keeps the existing small-board *_hover / *_grasp group states. New names are
{square}_hover_big and {square}_grasp_big.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import yaml

from lara5_moveit.board_ik import ARM_JOINTS, ArmModel, fill_hover_joints

# Same geometry as lara5_moveit/chess_scene_big.py
A1 = (0.15, -0.16, 0.02)
S = 0.072

ROOT = Path(__file__).resolve().parents[2]
URDF = ROOT / 'lara5_description' / 'lara5' / 'urdf' / 'lara5.urdf'
HOVER_YAML = Path(__file__).resolve().parents[1] / 'config' / 'board_hover_joints_big.yaml'
GRASP_YAML = Path(__file__).resolve().parents[1] / 'config' / 'board_grasp_joints_big.yaml'
SRDF = ROOT / 'lara5_moveit_config' / 'config' / 'lara5.srdf'

# Taught in RViz Joints tab (integer degrees) with board:=big, square h1.
H1_Q = np.deg2rad(np.array([-34.0, -26.0, 142.0, 0.0, 63.0, 4.0]))

# Same taught hover→grasp pair as generate_grasp_goals.py (world-frame tendency).
H1_HOVER_TENDENCY = np.array([-0.453786, -0.122173, 2.251475, 0.0, 0.977384, 0.069813])
H1_GRASP_TENDENCY = np.radians(np.array([-27.0, 1.0, 132.0, 0.0, 45.0, 3.0]))

BIG_HOVER_MARKER = '    <!-- Hover goals (board=big):'
END_EE_MARKER = '    <!--END EFFECTOR:'


def _group_state(name: str, q: list[float]) -> str:
    lines = [f'    <group_state name="{name}" group="arm">']
    for joint, val in zip(ARM_JOINTS, q):
        lines.append(f'        <joint name="{joint}" value="{val:.6f}"/>')
    lines.append('    </group_state>')
    return '\n'.join(lines)


def _hover_squares(model: ArmModel) -> tuple[dict, dict]:
    packed = fill_hover_joints(
        H1_Q,
        model,
        a1=tuple(A1),
        square_size=S,
    )
    squares = packed['squares']
    t_h1 = model.fk(H1_Q)
    squares['h1']['q'] = [float(v) for v in H1_Q]
    squares['h1']['ok'] = True
    squares['h1']['pos_err_m'] = 0.0
    squares['h1']['ori_err_rad'] = 0.0
    squares['h1']['xyz'] = [float(v) for v in t_h1[:3, 3]]
    return packed, squares


def _write_hover_yaml(packed: dict, squares: dict) -> dict[str, list[float]]:
    hover = {sq: rec['q'] for sq, rec in squares.items()}
    HOVER_YAML.parent.mkdir(parents=True, exist_ok=True)
    HOVER_YAML.write_text(
        yaml.safe_dump(
            {
                'board': 'big',
                'units': 'radians',
                'joints': list(ARM_JOINTS),
                'eef': 'lara5_gripper',
                'seed_square': 'h1',
                'seed_q': [float(v) for v in H1_Q],
                'seed_q_deg': [float(v) for v in np.degrees(H1_Q)],
                'a1': [float(v) for v in A1],
                'square_size': float(S),
                'hover_z': packed['hover_z'],
                'tool_z_world': packed['tool_z_world'],
                'ik_ok': {sq: bool(rec['ok']) for sq, rec in squares.items()},
                'hover': hover,
                'hover_deg': {sq: [float(np.degrees(v)) for v in q] for sq, q in hover.items()},
            },
            sort_keys=False,
        ),
        encoding='utf-8',
    )
    print('wrote', HOVER_YAML)
    return hover


def _grasps_from_hover(model: ArmModel, hover: dict[str, list[float]]) -> tuple[dict, dict, list[str], np.ndarray, np.ndarray]:
    t_h = model.fk(H1_HOVER_TENDENCY)
    t_g = model.fk(H1_GRASP_TENDENCY)
    dp = t_g[:3, 3] - t_h[:3, 3]
    dR = t_g[:3, :3] @ t_h[:3, :3].T
    dq = H1_GRASP_TENDENCY - H1_HOVER_TENDENCY

    grasps: dict[str, list[float]] = {}
    ok_map: dict[str, bool] = {}
    weak: list[str] = []
    seed_prev = None
    for square, q_h in hover.items():
        q_h = np.array(q_h, dtype=float)
        t_sq = model.fk(q_h)
        target_p = t_sq[:3, 3] + dp
        target_r = dR @ t_sq[:3, :3]
        seed = np.clip(q_h + dq, model.lower, model.upper)
        ok, q, pe, oe = model.ik(target_p, target_r, seed)
        if not ok and seed_prev is not None:
            ok, q, pe, oe = model.ik(target_p, target_r, seed_prev)
        if not ok:
            ok, q, pe, oe = model.ik(target_p, target_r, q_h)
        grasps[square] = [float(v) for v in q]
        ok_map[square] = bool(ok)
        if ok:
            seed_prev = q
        else:
            weak.append(f'{square}({pe * 1000:.1f}mm,{np.degrees(oe):.1f}deg)')
    return grasps, ok_map, weak, dp, dq


def _write_grasp_yaml(
    grasps: dict[str, list[float]],
    ok_map: dict[str, bool],
    dp: np.ndarray,
    dq: np.ndarray,
) -> None:
    GRASP_YAML.write_text(
        yaml.safe_dump(
            {
                'board': 'big',
                'units': 'radians',
                'joints': list(ARM_JOINTS),
                'eef': 'lara5_gripper',
                'seed_square': 'h1',
                'tendency_dq_rad': [float(v) for v in dq],
                'tendency_dq_deg': [float(v) for v in np.degrees(dq)],
                'tendency_dp_m': [float(v) for v in dp],
                'ik_ok': ok_map,
                'grasp': grasps,
                'grasp_deg': {k: [float(np.degrees(v)) for v in q] for k, q in grasps.items()},
            },
            sort_keys=False,
        ),
        encoding='utf-8',
    )
    print('wrote', GRASP_YAML)


def _update_srdf(hover: dict[str, list[float]], grasps: dict[str, list[float]]) -> None:
    text = SRDF.read_text(encoding='utf-8')
    if END_EE_MARKER not in text:
        raise RuntimeError(f'{SRDF}: missing {END_EE_MARKER!r}')
    if BIG_HOVER_MARKER in text:
        text = text[: text.index(BIG_HOVER_MARKER)] + text[text.index(END_EE_MARKER) :]
    block = [
        '    <!-- Hover goals (board=big): h1 taught in RViz; other squares IK at same z and R. -->',
    ]
    for square, q in hover.items():
        block.append(_group_state(f'{square}_hover_big', q))
    block.append('')
    block.append(
        '    <!-- Grasp goals (board=big): hover TCP + h1 dp/dR, seed q_hover+dq. -->'
    )
    for square, q in grasps.items():
        block.append(_group_state(f'{square}_grasp_big', q))
    block.append('')
    text = text.replace(END_EE_MARKER, '\n'.join(block) + '\n' + END_EE_MARKER, 1)
    SRDF.write_text(text, encoding='utf-8')
    print('updated', SRDF)


def main() -> None:
    model = ArmModel(str(URDF))
    packed, squares = _hover_squares(model)
    n_ok = sum(1 for rec in squares.values() if rec['ok'])
    weak_hover = [s for s, rec in squares.items() if not rec['ok']]
    t_h1 = model.fk(H1_Q)
    print(
        f'board=big a1={A1} square={S:.3f} hover_z={packed["hover_z"]:.4f} '
        f'toolZ={packed["tool_z_world"]} ok={n_ok}/64'
    )
    print('taught h1 TCP xyz', np.round(t_h1[:3, 3], 4).tolist())
    if weak_hover:
        print('weak hover IK:', ' '.join(weak_hover))
        for square in weak_hover:
            rec = squares[square]
            print(f'  {square} pe={rec["pos_err_m"] * 1000:.1f}mm oe={rec["ori_err_rad"]:.3f}')

    hover = _write_hover_yaml(packed, squares)
    grasps, ok_map, weak_grasp, dp, dq = _grasps_from_hover(model, hover)
    n_grasp = sum(ok_map.values())
    print('tendency hover→grasp dp m', np.round(dp, 4).tolist())
    print(f'grasp IK {n_grasp}/64')
    if weak_grasp:
        print('weak grasp:', ' '.join(weak_grasp))
    _write_grasp_yaml(grasps, ok_map, dp, dq)
    _update_srdf(hover, grasps)


if __name__ == '__main__':
    main()
