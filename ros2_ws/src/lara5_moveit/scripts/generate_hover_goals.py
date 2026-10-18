#!/usr/bin/env python3
"""Generate 64 hover joint goals from the taught h1_hover pose."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import yaml

from lara5_moveit.board_ik import (
    ARM_JOINTS, HOVER_TIP_Z, JAW_AXIS_YAW, JAW_AXIS_YAW_ALT, TIP_LINK, ArmModel, fill_hover_joints)

H1_Q = np.array(
    [-0.453786, -0.122173, 2.251475, 0.0, 0.977384, 0.069813],
    dtype=float,
)
ROOT = Path(__file__).resolve().parents[2]  # ros2_ws/src
URDF = ROOT / 'lara5_description' / 'lara5' / 'urdf' / 'lara5.urdf'
YAML_OUT = Path(__file__).resolve().parents[1] / 'config' / 'board_hover_joints.yaml'
SRDF = ROOT / 'lara5_moveit_config' / 'config' / 'lara5.srdf'
# 'discard' state (orchestrator discard_pose): captured pieces are dropped here, TCP at hover
# orientation beside the board (board y = -0.16 .. 0.16), 8 cm above the floor.
DISCARD_XYZ = (0.40, -0.25, 0.08)


def _group_state(name: str, q: list[float]) -> str:
    lines = [f'    <group_state name="{name}" group="arm">']
    for joint, val in zip(ARM_JOINTS, q):
        lines.append(f'        <joint name="{joint}" value="{val:.6f}"/>')
    lines.append('    </group_state>')
    return '\n'.join(lines)


def main() -> None:
    model = ArmModel(str(URDF))
    packed = fill_hover_joints(H1_Q, model, z_override=HOVER_TIP_Z, jaw_yaw=JAW_AXIS_YAW)
    # h1 is re-solved too: the taught joints (integer-degree sliders, ~6 mm per degree of
    # joint1) only give the seed, hover height and orientation.
    squares = packed['squares']

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
        'eef': TIP_LINK,
        'seed_square': 'h1',
        'seed_q': [float(v) for v in H1_Q],
        'hover_z': packed['hover_z'],
        'tcp': packed['tcp'],
        'tool_z_world': packed['tool_z_world'],
        'ik_ok': {sq: bool(rec['ok']) for sq, rec in squares.items()},
        'hover': hover,
        'hover_deg': {sq: [float(np.degrees(v)) for v in q] for sq, q in hover.items()},
    }
    YAML_OUT.write_text(yaml.safe_dump(payload, sort_keys=False), encoding='utf-8')
    print('wrote', YAML_OUT)

    text = SRDF.read_text(encoding='utf-8')
    # replace only the *_hover block (the *_grasp block after it is kept)
    start = text.index('    <!-- Hover goals: ')
    end = text.index('    <!-- Grasp goals: ', start)
    block = [
        '    <!-- Hover goals: grasp TCP above each square centre, IK at taught h1 z and R. -->',
    ]
    for sq, q in hover.items():
        block.append(_group_state(f'{sq}_hover', q))
    block.append('')
    # alternative jaw direction (orchestrator fallback when the wrist would hit a neighbour)
    alt = fill_hover_joints(H1_Q, model, z_override=HOVER_TIP_Z, jaw_yaw=JAW_AXIS_YAW_ALT)
    weak_alt = [sq for sq, rec in alt['squares'].items() if not rec['ok']]
    print(f'alt jaw yaw: ok={64 - len(weak_alt)}/64', ('weak: ' + ' '.join(weak_alt)) if weak_alt else '')
    block.append('    <!-- Hover goals, alternative jaw direction (board_ik.JAW_AXIS_YAW_ALT). -->')
    for sq, rec in alt['squares'].items():
        if rec['ok']:
            block.append(_group_state(f'{sq}_hover_alt', rec['q']))
    block.append('')
    text = text[:start] + '\n'.join(block) + '\n' + text[end:]

    # discard: IK from the h1 hover with the hover orientation
    t_h1 = model.fk(np.array(hover['h1']))
    ok, q, pe, oe = model.ik(np.array(DISCARD_XYZ), t_h1[:3, :3], np.array(hover['h1']),
                             pos_tol=0.001, ori_tol=0.01)
    if not ok:
        raise RuntimeError(f'discard IK failed: {pe * 1000:.1f} mm, {oe:.3f} rad')
    discard = _group_state('discard', [float(v) for v in q])
    if '<group_state name="discard"' in text:
        a = text.index('    <group_state name="discard"')
        b = text.index('</group_state>', a) + len('</group_state>')
        text = text[:a] + discard + text[b:]
    else:
        text = text.replace('    <!-- Hover goals: ', discard + '\n    <!-- Hover goals: ', 1)
    print('discard', [round(v, 4) for v in q])

    SRDF.write_text(text, encoding='utf-8')
    print('updated', SRDF)


if __name__ == '__main__':
    main()
