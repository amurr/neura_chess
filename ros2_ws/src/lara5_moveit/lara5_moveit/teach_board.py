#!/usr/bin/env python3
"""Capture / generate hover joints for all 64 squares without topic-echo paste.

Workflow (fast):
  1. Launch orient.launch.py and teleop *once* to a good hover
     (EEF perpendicular, height you want above the pieces).
  2. In this node:  fill
  3. write         — YAML dict for later MoveIt pick/place.

Optional: save a1 (or any square) after a manual nudge to overwrite that entry.

  ros2 run lara5_moveit teach_board
"""

from __future__ import annotations

import threading
from pathlib import Path

import numpy as np
import rclpy
import yaml
from rclpy.node import Node
from sensor_msgs.msg import JointState

from lara5_moveit.board_ik import (
    ARM_JOINTS, TIP_LINK, ArmModel, all_squares, default_urdf, fill_hover_joints)


class TeachBoard(Node):
    def __init__(self) -> None:
        super().__init__('teach_board')
        self.declare_parameter('out', str(Path.cwd() / 'board_hover_joints.yaml'))
        self.declare_parameter('urdf', default_urdf())
        self._q: np.ndarray | None = None
        self._saved: dict[str, list[float]] = {}
        self._filled: dict[str, dict[str, object]] | None = None
        self._meta: dict[str, object] = {}
        self._model = ArmModel(str(self.get_parameter('urdf').value))
        self.create_subscription(JointState, '/joint_states', self._on_js, 10)
        self.get_logger().info(
            f'teach_board ready urdf={self.get_parameter("urdf").value} '
            f'out={self.get_parameter("out").value}'
        )

    def _on_js(self, msg: JointState) -> None:
        by_name = {n: p for n, p in zip(msg.name, msg.position)}
        if all(n in by_name for n in ARM_JOINTS):
            self._q = np.array([by_name[n] for n in ARM_JOINTS], dtype=float)

    def current_q(self) -> np.ndarray:
        if self._q is None:
            raise RuntimeError('no /joint_states yet — is orient.launch running?')
        return self._q.copy()

    def save(self, square: str) -> list[float]:
        q = [float(v) for v in self.current_q()]
        self._saved[square.strip().lower()] = q
        return q

    def fill(self) -> dict[str, object]:
        try:
            seed = self.current_q()
        except RuntimeError:
            if not self._saved:
                raise
            seed = np.array(next(reversed(self._saved.values())), dtype=float)
        packed = fill_hover_joints(seed, self._model)
        self._filled = packed['squares']  # type: ignore[assignment]
        self._meta = {
            'hover_z': packed['hover_z'],
            'tool_z_world': packed['tool_z_world'],
            'seed_q': [float(v) for v in seed],
        }
        return packed

    def joints_for(self, square: str) -> list[float] | None:
        key = square.strip().lower()
        if key in self._saved:
            return self._saved[key]
        if self._filled and key in self._filled:
            return list(self._filled[key]['q'])  # type: ignore[index]
        return None

    def write(self, path: str | None = None) -> Path:
        dest = Path(path or str(self.get_parameter('out').value))
        squares: dict[str, list[float]] = {}
        if self._filled:
            for sq, rec in self._filled.items():
                squares[sq] = list(rec['q'])  # type: ignore[index]
        squares.update(self._saved)
        payload = {
            'units': 'radians',
            'joints': list(ARM_JOINTS),
            'eef': TIP_LINK,
            **self._meta,
            'hover': squares,
            'hover_deg': {k: [float(np.degrees(v)) for v in q] for k, q in squares.items()},
        }
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(yaml.safe_dump(payload, sort_keys=False), encoding='utf-8')
        return dest


def _fmt(q: list[float]) -> str:
    return '[' + ', '.join(f'{v:.6f}' for v in q) + ']'


def _repl(node: TeachBoard) -> None:
    squares = all_squares()
    idx = 0
    print(
        'teach_board  commands: show | save [sq] | fill | goto <sq> | write [path] | list | quit\n'
        'Fast path: teleop to one hover, then  fill  then  write'
    )
    while rclpy.ok():
        try:
            line = input(f'[{squares[idx]}] > ').strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not line:
            continue
        cmd, *rest = line.split()
        try:
            if cmd in ('q', 'quit', 'exit'):
                break
            if cmd in ('h', 'help'):
                print('show | save [sq] | fill | goto <sq> | write [path] | list | quit')
            elif cmd == 'show':
                q = node.current_q()
                t = node._model.fk(q)
                print('q rad', _fmt(q.tolist()))
                print('q deg', _fmt(np.degrees(q).tolist()))
                print('tcp', _fmt(t[:3, 3].tolist()), 'toolZ', _fmt((t[:3, :3] @ [0, 0, 1]).tolist()))
            elif cmd == 'save':
                sq = rest[0] if rest else squares[idx]
                q = node.save(sq)
                print(f'saved {sq} {_fmt(q)}')
                if sq in squares:
                    idx = (squares.index(sq) + 1) % 64
            elif cmd == 'fill':
                packed = node.fill()
                squares_rec = packed['squares']
                n_ok = sum(1 for r in squares_rec.values() if r['ok'])
                tz = packed['tool_z_world']
                print(
                    f'filled {n_ok}/64  hover_z={packed["hover_z"]:.4f} m  '
                    f'toolZ=[{tz[0]:.2f}, {tz[1]:.2f}, {tz[2]:.2f}]  '
                    '(want ≈ [0, 0, -1] for perpendicular)'
                )
                bad = [s for s, r in squares_rec.items() if not r['ok']]
                if bad:
                    print('IK weak:', ' '.join(bad))
            elif cmd == 'goto':
                if not rest:
                    print('goto <square>')
                    continue
                q = node.joints_for(rest[0])
                if q is None:
                    print('unknown square — fill or save first')
                else:
                    print(rest[0], 'rad', _fmt(q))
                    print(rest[0], 'deg', _fmt([float(np.degrees(v)) for v in q]))
            elif cmd == 'write':
                dest = node.write(rest[0] if rest else None)
                n = len(node._saved) + (len(node._filled) if node._filled else 0)
                print(f'wrote {n} poses -> {dest}')
            elif cmd == 'list':
                keys = sorted(node._saved)
                print('saved', keys or '(none)')
                if node._filled:
                    print('filled 64 (save overrides fill on write)')
            else:
                print('unknown command')
        except Exception as exc:  # noqa: BLE001 — REPL should stay up
            print('error:', exc)


def main(args: list[str] | None = None) -> None:
    rclpy.init(args=args)
    node = TeachBoard()
    spinner = threading.Thread(target=rclpy.spin, args=(node,), daemon=True)
    spinner.start()
    try:
        _repl(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
