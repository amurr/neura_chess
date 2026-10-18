#!/usr/bin/env python3
"""Build {square}_grasp goals from taught h1 hover → h1 grasp tendency."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import yaml

from lara5_moveit.board_ik import ARM_JOINTS, TIP_LINK, ArmModel

ROOT = Path(__file__).resolve().parents[2]
URDF = ROOT / 'lara5_description' / 'lara5' / 'urdf' / 'lara5.urdf'
HOVER_YAML = Path(__file__).resolve().parents[1] / 'config' / 'board_hover_joints.yaml'
GRASP_YAML = Path(__file__).resolve().parents[1] / 'config' / 'board_grasp_joints.yaml'
SRDF = ROOT / 'lara5_moveit_config' / 'config' / 'lara5.srdf'

# Taught in RViz (integer degrees on the Joints sliders).
H1_HOVER = np.array([-0.453786, -0.122173, 2.251475, 0.0, 0.977384, 0.069813])
H1_GRASP = np.radians(np.array([-27.0, 1.0, 132.0, 0.0, 45.0, 3.0]))


def _group_state(name: str, q: list[float]) -> str:
    lines = [f'    <group_state name="{name}" group="arm">']
    for joint, val in zip(ARM_JOINTS, q):
        lines.append(f'        <joint name="{joint}" value="{val:.6f}"/>')
    lines.append('    </group_state>')
    return '\n'.join(lines)


def main() -> None:
    model = ArmModel(str(URDF))
    hover_doc = yaml.safe_load(HOVER_YAML.read_text(encoding='utf-8'))
    hover = {k: np.array(v, dtype=float) for k, v in hover_doc['hover'].items()}

    t_h = model.fk(H1_HOVER)
    t_g = model.fk(H1_GRASP)
    dp = t_g[:3, 3] - t_h[:3, 3]
    dR = t_g[:3, :3] @ t_h[:3, :3].T
    dq = H1_GRASP - H1_HOVER

    print('tendency hover→grasp')
    print('  dq deg', np.round(np.degrees(dq), 2).tolist())
    print('  dp m  ', np.round(dp, 4).tolist())

    grasps: dict[str, list[float]] = {}
    ok_map: dict[str, bool] = {}
    weak: list[str] = []
    seed_prev = H1_GRASP.copy()

    for square, q_h in hover.items():
        if square == 'h1':
            grasps[square] = [float(v) for v in H1_GRASP]
            ok_map[square] = True
            seed_prev = H1_GRASP.copy()
            continue
        t_sq = model.fk(q_h)
        target_p = t_sq[:3, 3] + dp
        target_r = dR @ t_sq[:3, :3]
        seed = np.clip(q_h + dq, model.lower, model.upper)
        ok, q, pe, oe = model.ik(target_p, target_r, seed)
        if not ok:
            ok, q, pe, oe = model.ik(target_p, target_r, seed_prev)
        if not ok:
            ok, q, pe, oe = model.ik(target_p, target_r, H1_GRASP)
        grasps[square] = [float(v) for v in q]
        ok_map[square] = bool(ok)
        if ok:
            seed_prev = q
        else:
            weak.append(f'{square}({pe*1000:.1f}mm,{np.degrees(oe):.1f}deg)')

    n_ok = sum(ok_map.values())
    print(f'grasp IK {n_ok}/64')
    if weak:
        print('weak:', ' '.join(weak))

    GRASP_YAML.write_text(
        yaml.safe_dump(
            {
                'units': 'radians',
                'joints': list(ARM_JOINTS),
                'eef': TIP_LINK,
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

    text = SRDF.read_text(encoding='utf-8')
    marker = '    <group_state name="close" group="gripper">'
    if 'name="a1_grasp"' in text:
        start = text.index('    <!-- Grasp goals:')
        text = text[:start] + text[text.index(marker) :]
    block = ['    <!-- Grasp goals: h1 taught; others = hover TCP + h1 dp/dR, seed q_hover+dq. -->']
    for square, q in grasps.items():
        block.append(_group_state(f'{square}_grasp', q))
    block.append('')
    SRDF.write_text(text.replace(marker, '\n'.join(block) + '\n' + marker, 1), encoding='utf-8')
    print('updated', SRDF)


if __name__ == '__main__':
    main()
