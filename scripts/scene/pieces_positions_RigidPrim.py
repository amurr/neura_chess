#!/usr/bin/env python3
"""Ask Kit for current chess-piece PhysX poses (RigidPrim.get_world_poses).

Kit writes /tmp/neura_chess_pieces.json. Use after (or during) an MTC execute
to see where pieces actually are vs the intended occupancy.

  ./scripts/scene/pieces_positions_RigidPrim.sh
  ./scripts/scene/pieces_positions_RigidPrim.sh --json
  ./scripts/scene/pieces_positions_RigidPrim.sh --out /tmp/after_e2e4.json
  ./scripts/scene/pieces_positions_RigidPrim.sh --record 10   # Kit JSONL at 10 Hz
  ./scripts/scene/pieces_positions_RigidPrim.sh --stop
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import time
from pathlib import Path

REQUEST = Path("/tmp/neura_chess_pieces.request")
DONE = Path("/tmp/neura_chess_pieces.done")
READY = Path("/tmp/neura_chess_pieces.ready")
JSON_OUT = Path("/tmp/neura_chess_pieces.json")
JSONL = Path("/tmp/neura_chess_pieces.jsonl")
RECORD = Path("/tmp/neura_chess_pieces.record")
ROS_SERVICE = "/neura_chess/piece_poses"


def _wait_ready(timeout_s: float) -> bool:
    if not READY.is_file():
        print(
            f"waiting up to {timeout_s:.0f}s for Kit piece-pose listener ({READY}) ...",
            flush=True,
        )
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        if READY.is_file():
            print(f"Kit piece poses: {READY.read_text(encoding='utf-8').strip()}", flush=True)
            return True
        time.sleep(0.1)
    print(
        f"ERROR: Kit has no piece-pose listener ({READY} missing). "
        "Restart ./scripts/launch/launch_world.sh and wait for 'PiecePositions RigidPrim' "
        "in /tmp/neura_chess_world.log, then rerun this script.",
        flush=True,
    )
    return False


def _call_ros(timeout_s: float) -> bool:
    try:
        import rclpy
        from std_srvs.srv import Trigger
    except Exception:
        return False
    if not rclpy.ok():
        rclpy.init()
    node = rclpy.create_node("pieces_positions_rigidprim_srv")
    try:
        client = node.create_client(Trigger, ROS_SERVICE)
        if not client.wait_for_service(timeout_sec=min(0.6, timeout_s)):
            return False
        fut = client.call_async(Trigger.Request())
        rclpy.spin_until_future_complete(node, fut, timeout_sec=timeout_s)
        res = fut.result()
        return bool(res is not None and res.success)
    except Exception:
        return False
    finally:
        node.destroy_node()


def _poke(timeout_s: float) -> bool:
    try:
        DONE.unlink(missing_ok=True)
    except TypeError:
        if DONE.exists():
            DONE.unlink()
    REQUEST.write_text("1\n", encoding="utf-8")
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        if DONE.is_file():
            print(f"Isaac pieces: {DONE.read_text(encoding='utf-8').strip()}", flush=True)
            return True
        time.sleep(0.02)
    leftover = REQUEST.is_file()
    print(
        f"ERROR: Kit did not ack {DONE} in {timeout_s:.1f}s. "
        + (
            "World has no PiecePositions poll — restart ./scripts/launch/launch_world.sh."
            if leftover
            else "Check /tmp/neura_chess_world.log and retry with --timeout 15."
        ),
        flush=True,
    )
    return False


def _print_table(snap: dict) -> None:
    pieces = snap.get("pieces") or []
    print(
        f"backend={snap.get('backend')} t_sim={snap.get('t_sim')} n={len(pieces)} "
        f"occupancy={len(snap.get('occupancy') or {})} displaced={len(snap.get('displaced') or [])}",
        flush=True,
    )
    hdr = f"{'name':<16} {'ros':<4} {'raw':<4} {'x':>7} {'y':>7} {'z':>7} {'err_mm':>7} {'tilt':>6} {'ok':<4}"
    print(hdr, flush=True)
    for p in pieces:
        sq = p.get("square") or "--"
        raw = p.get("square_unmirrored") or "--"
        err = 1000.0 * float(p.get("xy_err_m") or 0.0)
        tilt = p.get("tilt_deg")
        tilt_s = f"{tilt:5.1f}" if tilt is not None else "  n/a"
        ok = "yes" if p.get("on_square") and p.get("upright") is not False else "no"
        print(
            f"{p.get('name', ''):<16} {sq:<4} {raw:<4} {p['x']:7.3f} {p['y']:7.3f} {p['z']:7.3f} "
            f"{err:7.1f} {tilt_s:>6} {ok:<4}",
            flush=True,
        )
    displaced = snap.get("displaced") or []
    if displaced:
        print(f"displaced: {', '.join(displaced)}", flush=True)
    conflicts = snap.get("conflicts") or {}
    if conflicts:
        print(f"conflicts: {conflicts}", flush=True)


def _snapshot(timeout_s: float, *, use_ros: bool) -> dict | None:
    if use_ros:
        _call_ros(timeout_s=min(1.0, timeout_s))
    if not _poke(timeout_s):
        return None
    if not JSON_OUT.is_file():
        print(f"ERROR: Kit ack but {JSON_OUT} missing", flush=True)
        return None
    return json.loads(JSON_OUT.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser(
        description="Dump Isaac chess piece poses from RigidPrim (PhysX)"
    )
    p.add_argument("--timeout", type=float, default=5.0)
    p.add_argument("--json", action="store_true", help="Print full JSON instead of a table")
    p.add_argument("--out", type=Path, default=None, help="Copy snapshot JSON to this path")
    p.add_argument("--no-ros", action="store_true", help="File IPC only")
    p.add_argument(
        "--record",
        type=float,
        nargs="?",
        const=10.0,
        metavar="HZ",
        help="Start Kit JSONL recording at HZ (0 = every frame). Writes /tmp/neura_chess_pieces.jsonl",
    )
    p.add_argument("--stop", action="store_true", help="Stop Kit JSONL recording")
    p.add_argument(
        "--watch",
        type=float,
        metavar="HZ",
        help="Repeated snapshots at HZ until Ctrl+C",
    )
    args = p.parse_args()

    if args.stop:
        try:
            RECORD.unlink(missing_ok=True)
        except TypeError:
            if RECORD.exists():
                RECORD.unlink()
        print(f"stopped recording ({JSONL})", flush=True)
        return 0

    if not _wait_ready(timeout_s=max(args.timeout, 90.0)):
        return 1

    if args.record is not None:
        try:
            JSONL.write_text("", encoding="utf-8")
        except OSError:
            pass
        RECORD.write_text(f"{float(args.record):.6f}\n", encoding="utf-8")
        print(
            f"recording {args.record:g} Hz → {JSONL}  (stop with --stop)",
            flush=True,
        )
        return 0

    def once() -> int:
        snap = _snapshot(args.timeout, use_ros=not args.no_ros)
        if snap is None:
            return 1
        if args.out is not None:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(JSON_OUT, args.out)
            print(f"wrote {args.out}", flush=True)
        if args.json:
            print(json.dumps(snap, indent=2), flush=True)
        else:
            _print_table(snap)
            print(f"json: {JSON_OUT}", flush=True)
        return 0

    if args.watch is not None:
        period = 1.0 / max(1e-3, float(args.watch))
        try:
            while True:
                rc = once()
                if rc != 0:
                    return rc
                time.sleep(period)
        except KeyboardInterrupt:
            return 0

    return once()


if __name__ == "__main__":
    sys.exit(main())
