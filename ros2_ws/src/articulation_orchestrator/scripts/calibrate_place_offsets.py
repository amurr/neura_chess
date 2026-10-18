#!/usr/bin/env python3
"""Correct the place offsets from where the pieces really landed in Isaac.

For every move in the execution logs (execution_logger with Isaac piece recording) that put the
piece upright on its target square, take the final piece position minus the target square
centre, in the TCP axes at the place, and add the median per piece type to the offset the moves
used (objects.<type>.place_offset, else [grasp_offset, 0]):

  objects.<type>.place_offset: [x, y]   (m, TCP frame; the place shifts the TCP by -place_offset)

The runs must have been made with the current objects_dictionary.yaml (the offsets used are read
from it). Repeat: run moves, calibrate, run moves again to check.

  python3 scripts/calibrate_place_offsets.py [execution_logs dirs ...]   (default: all)
  python3 scripts/calibrate_place_offsets.py --dry-run
"""

from __future__ import annotations

import argparse
import bisect
import csv
import json
import math
import re
import statistics
from pathlib import Path

import yaml

PKG = Path(__file__).resolve().parents[1]
LOGS = PKG / 'execution_logs'
OBJECTS_YAML = PKG / 'assets' / 'objects_dictionary.yaml'
MAX_ERROR = 0.015    # m, larger: the move failed, not an offset
MAX_TILT_DEG = 10.0  # the piece must stand upright


def quat_x_axis(wxyz) -> tuple[float, float]:
    w, x, y, z = wxyz
    cx, cy = 1 - 2 * (y * y + z * z), 2 * (x * y + w * z)
    n = math.hypot(cx, cy)
    return cx / n, cy / n


def measure(run: Path) -> list[tuple[str, float, float]]:
    """[(piece type, x, y)]: final position - target centre, TCP frame, per move of a run."""
    steps_csv, arm, pieces = run / 'steps.csv', run / 'arm.jsonl', run / 'isaac_pieces.jsonl'
    if not (steps_csv.is_file() and arm.is_file() and pieces.is_file()):
        return []
    samples = [json.loads(line) for line in arm.open()]
    samples = [s for s in samples if s.get('type') == 'sample' and 'lara5_tcp' in s.get('links', {})]
    snaps = [json.loads(line) for line in pieces.open()]
    if not samples or not snaps:
        return []
    times = [s['t'] for s in samples]

    out = []
    for row in csv.DictReader(steps_csv.open()):
        dst = row['dst']
        if row['label'] != f'ARM_NAMED {dst}_hover' or not row['ps_square_x']:
            continue
        start = next((p for p in snaps[0]['pieces'] if p.get('square') == row['src']), None)
        if start is None:
            continue
        final = next(p for p in snaps[-1]['pieces'] if p['name'] == start['name'])
        ex = final['x'] - float(row['ps_square_x'])
        ey = final['y'] - float(row['ps_square_y'])
        if (math.hypot(ex, ey) > MAX_ERROR or final.get('square') != dst
                or (final.get('tilt_deg') or 0.0) > MAX_TILT_DEG):
            continue
        i = max(0, bisect.bisect(times, float(row['t_end'])) - 1)
        cx, cy = quat_x_axis(samples[i]['links']['lara5_tcp']['wxyz'])
        # TCP y axis = z x x (z ~ world up at the hover poses)
        out.append((start['type'], ex * cx + ey * cy, -ex * cy + ey * cx))
    return out


def write(offsets: dict[str, tuple[float, float]]) -> None:
    text = OBJECTS_YAML.read_text(encoding='utf-8')
    for kind, (x, y) in offsets.items():
        # "  <kind>:   # comment" then "    {tip_height: .., grasp_offset: .., ..." (preferred level)
        pat = re.compile(rf'^(  {kind}:[^\n]*\n    \{{tip_height: [-0-9.]+, grasp_offset: [-0-9.]+)'
                         rf'(, place_offset: \[[^\]]*\])?', re.MULTILINE)
        text, n = pat.subn(rf'\g<1>, place_offset: [{x:.4f}, {y:.4f}]', text)
        if n != 1:
            raise RuntimeError(f'{OBJECTS_YAML}: no line for {kind!r}')
    OBJECTS_YAML.write_text(text, encoding='utf-8')


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('runs', nargs='*', type=Path, help='execution log directories (default: all)')
    ap.add_argument('--types', nargs='*', help='only these piece types')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    objects = yaml.safe_load(OBJECTS_YAML.read_text(encoding='utf-8'))['objects']
    runs = args.runs or sorted(p for p in LOGS.iterdir() if p.is_dir())
    errors: dict[str, list[tuple[float, float]]] = {}
    for run in runs:
        for kind, x, y in measure(run):
            if not args.types or kind in args.types:
                errors.setdefault(kind, []).append((x, y))
    offsets = {}
    for kind, vals in sorted(errors.items()):
        ex = statistics.median(v[0] for v in vals)
        ey = statistics.median(v[1] for v in vals)
        spread = max(math.hypot(v[0] - ex, v[1] - ey) for v in vals)
        used = objects[kind].get('place_offset', (objects[kind]['grasp_offset'], 0.0))
        offsets[kind] = (used[0] + ex, used[1] + ey)
        print(f'{kind:7s} n={len(vals):2d} error=[{ex * 1000:+.1f}, {ey * 1000:+.1f}] mm '
              f'(spread {spread * 1000:.1f} mm) -> place_offset=[{offsets[kind][0]:.4f}, '
              f'{offsets[kind][1]:.4f}]')
    if offsets and not args.dry_run:
        write(offsets)
        print('updated', OBJECTS_YAML)


if __name__ == '__main__':
    main()
