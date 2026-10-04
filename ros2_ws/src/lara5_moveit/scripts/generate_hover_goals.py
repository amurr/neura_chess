#!/usr/bin/env python3
"""Generate 64 hover joint goals from the taught h1_hover pose."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import yaml

from lara5_moveit.board_ik import ARM_JOINTS, ArmModel, fill_hover_joints

H1_Q = np.array(
    [-0.453786, -0.122173, 2.251475, 0.0, 0.977384, 0.069813],
    dtype=float,
)
ROOT = Path(__file__).resolve().parents[2]  # ros2_ws/src
URDF = ROOT / 'lara5_description' / 'lara5' / 'urdf' / 'lara5.urdf'
YAML_OUT = Path(__file__).resolve().parents[1] / 'config' / 'board_hover_joints.yaml'
SRDF = ROOT / 'lara5_moveit_config' / 'config' / 'lara5.srdf'


def _group_state(name: str, q: list[float]) -> str:
    lines = [f'    <group_state name="{name}" group="arm">']
    for joint, val in zip(ARM_JOINTS, q):
        lines.append(f'        <joint name="{joint}" value="{val:.6f}"/>')
    lines.append('    </group_state>')
    return '\n'.join(lines)


def main() -> None:
    model = ArmModel(str(URDF))
    packed = fill_hover_joints(H1_Q, model)
    squares = packed['squares']
    # Keep the taught h1 joints exactly (do not replace with re-IK).
    t_h1 = model.fk(H1_Q)
    squares['h1']['q'] = [float(v) for v in H1_Q]
    squares['h1']['ok'] = True
    squares['h1']['pos_err_m'] = 0.0
    squares['h1']['ori_err_rad'] = 0.0
    squares['h1']['xyz'] = [float(v) for v in t_h1[:3, 3]]

    n_ok = sum(1 for rec in squares.values() if rec['ok'])
    weak = [s for s, rec in squares.items() if not rec['ok']]
    print(f'hover_z={packed["hover_z"]:.4f} toolZ={packed["tool_z_world"]} ok={n_ok}/64')
    if weak:
        print('weak IK:', ' '.join(weak))
        for s in weak:
            rec = squares[s]
            print(f'  {s} pe={rec["pos_err_m"]*1000:.1f}mm oe={rec["ori_err_rad"]:.3f}')

    hover = {sq: rec['q'] for sq, rec in squares.items()}
    YAML_OUT.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        'units': 'radians',
        'joints': list(ARM_JOINTS),
        'eef': 'lara5_gripper',
        'seed_square': 'h1',
        'seed_q': [float(v) for v in H1_Q],
        'hover_z': packed['hover_z'],
        'tool_z_world': packed['tool_z_world'],
        'ik_ok': {sq: bool(rec['ok']) for sq, rec in squares.items()},
        'hover': hover,
        'hover_deg': {sq: [float(np.degrees(v)) for v in q] for sq, q in hover.items()},
    }
    YAML_OUT.write_text(yaml.safe_dump(payload, sort_keys=False), encoding='utf-8')
    print('wrote', YAML_OUT)

    text = SRDF.read_text(encoding='utf-8')
    start = text.index('    <!-- Taught in RViz: hover above h1 (goal sliders). -->')
    end = text.index('    <group_state name="close" group="gripper">')
    block = [
        '    <!-- Hover goals: h1 taught in RViz; other squares IK at same z and R. -->',
    ]
    for sq, q in hover.items():
        block.append(_group_state(f'{sq}_hover', q))
    block.append('')
    SRDF.write_text(text[:start] + '\n'.join(block) + '\n' + text[end:], encoding='utf-8')
    print('updated', SRDF)


if __name__ == '__main__':
    main()
