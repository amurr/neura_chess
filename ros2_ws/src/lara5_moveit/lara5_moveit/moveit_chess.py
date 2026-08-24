#!/usr/bin/env python3
"""Pick a chess piece using Isaac Sim poses and MoveIt."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from typing import Any, Sequence

from lara5_moveit.piece_poses import (
    APPROACH_M,
    DOWN_RPY,
    eef_targets,
    fetch_isaac_snapshot,
    load_snapshot,
    piece_at_square,
)


ARM = 'arm'
GRIPPER = 'gripper'
EEF_LINK = 'lara5_gripper'
WORLD = 'world'
HOME_POSE = 'stand'
SEED_POSE = 'pre_pick'


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        description='MoveIt chess pick using Isaac piece poses',
    )
    parser.add_argument(
        '--square',
        default=os.environ.get('CHESS_SOURCE', ''),
        help='Pick square (e.g. e2). Default: CHESS_SOURCE',
    )
    parser.add_argument(
        '--to',
        default=os.environ.get('CHESS_TARGET', ''),
        help='Optional place square (e.g. e4). Default: CHESS_TARGET',
    )
    parser.add_argument(
        '--piece',
        default='',
        help='Optional type filter (pawn, rook, …)',
    )
    parser.add_argument(
        '--poses-json',
        default='',
        help='Load snapshot JSON instead of poking Kit',
    )
    parser.add_argument('--timeout', type=float, default=5.0)
    parser.add_argument(
        '--list',
        action='store_true',
        help='Print every piece pose and exit',
    )
    parser.add_argument(
        '--print-only',
        action='store_true',
        help='Print grasp targets and exit (no MoveIt)',
    )
    parser.add_argument(
        '--plan-only',
        action='store_true',
        help='Plan but do not execute',
    )
    # Launch injects --ros-args / --params-file; rclcpp.init() still reads sys.argv.
    args, _unknown = parser.parse_known_args(argv)
    return args


def _snapshot(args: argparse.Namespace) -> dict[str, Any]:
    if args.poses_json:
        return load_snapshot(args.poses_json)
    return fetch_isaac_snapshot(timeout_s=args.timeout)


def _list_pieces(snapshot: dict[str, Any]) -> int:
    pieces = snapshot.get('pieces') or []
    print(json.dumps(pieces, indent=2), flush=True)
    print(f'n={len(pieces)} occupancy={len(snapshot.get("occupancy") or {})}', flush=True)
    return 0


def run_mtc(targets: dict[str, Any], *, execute: bool) -> int:
    """Plan (and optionally execute) a pick / place tree for Lara5."""
    try:
        import rclcpp
        from geometry_msgs.msg import Point, Pose, PoseStamped, Quaternion, Vector3, Vector3Stamped
        from moveit.task_constructor import core, stages
        from std_msgs.msg import Header
    except ImportError as exc:
        print(
            f'ERROR: MoveIt Python API missing ({exc}). '
            'Source ROS 2 Humble + the workspace after installing '
            'moveit_task_constructor.',
            flush=True,
        )
        return 1

    rclcpp.init()
    node = rclcpp.Node('moveit_chess')

    jointspace = core.JointInterpolationPlanner()
    cartesian = core.CartesianPath()
    pipeline = core.PipelinePlanner(node)
    pipeline.planner = 'RRTConnectkConfigDefault'

    def world_pose(xyz: Sequence[float]) -> PoseStamped:
        qx, qy, qz, qw = targets['orientation_xyzw']
        msg = PoseStamped()
        msg.header.frame_id = WORLD
        msg.pose = Pose(
            position=Point(x=float(xyz[0]), y=float(xyz[1]), z=float(xyz[2])),
            orientation=Quaternion(x=qx, y=qy, z=qz, w=qw),
        )
        return msg

    def add_named(task: core.Task, name: str, group: str, goal: str) -> None:
        move = stages.MoveTo(name, jointspace)
        move.group = group
        move.setGoal(goal)
        task.add(move)

    def add_ik(task: core.Task, name: str, monitored, xyz: Sequence[float]) -> None:
        generator = stages.GeneratePose(f'{name} pose')
        generator.setMonitoredStage(monitored)
        generator.pose = world_pose(xyz)
        ik = stages.ComputeIK(name, generator)
        ik.group = ARM
        ik.ik_frame = PoseStamped(header=Header(frame_id=EEF_LINK))
        ik.max_ik_solutions = 8
        ik.properties.configureInitFrom(
            core.Stage.PropertyInitializerSource.INTERFACE, ['target_pose']
        )
        task.add(ik)

    def add_dz(task: core.Task, name: str, delta_z: float) -> None:
        move = stages.MoveRelative(name, cartesian)
        move.group = ARM
        move.setDirection(
            Vector3Stamped(
                header=Header(frame_id=WORLD),
                vector=Vector3(x=0.0, y=0.0, z=float(delta_z)),
            )
        )
        task.add(move)

    task = core.Task()
    task.name = 'moveit_chess'
    task.loadRobotModel(node)

    current = stages.CurrentState('current state')
    current.timeout = 30.0
    task.add(current)
    add_named(task, 'open gripper', GRIPPER, 'open')
    add_named(task, 'seed pre_pick', ARM, SEED_POSE)

    connect = stages.Connect('connect to pick hover', [(ARM, pipeline)])
    connect.properties.configureInitFrom(core.Stage.PropertyInitializerSource.PARENT)
    task.add(connect)

    add_ik(task, 'pick hover', task['seed pre_pick'], targets['pick_hover'])
    add_dz(task, 'approach pick', -APPROACH_M)
    add_named(task, 'close gripper', GRIPPER, 'close')
    add_dz(task, 'lift', APPROACH_M)

    if 'place_hover' in targets:
        connect_place = stages.Connect('connect to place hover', [(ARM, pipeline)])
        connect_place.properties.configureInitFrom(
            core.Stage.PropertyInitializerSource.PARENT
        )
        task.add(connect_place)
        add_ik(task, 'place hover', task['lift'], targets['place_hover'])
        add_dz(task, 'descend place', -APPROACH_M)
        add_named(task, 'open gripper place', GRIPPER, 'open')
        add_dz(task, 'retreat', APPROACH_M)

    add_named(task, 'move to stand', ARM, HOME_POSE)

    print(
        f'pick={targets.get("square")} {targets["pick_grasp"]} '
        f'place={targets.get("place_square")} rpy={DOWN_RPY}',
        flush=True,
    )

    if not task.plan():
        print('Planning failed', flush=True)
        return 1
    task.publish(task.solutions[0])
    print('Planning succeeded', flush=True)
    if execute:
        result = task.execute(task.solutions[0])
        ok = getattr(result, 'val', 1) == 1
        print('Execution succeeded' if ok else f'Execution failed ({result})', flush=True)
        return 0 if ok else 1
    time.sleep(1.0)
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    """Fetch Isaac piece poses and run the MoveIt pick sequence."""
    args = parse_args(argv)
    try:
        snapshot = _snapshot(args)
    except (FileNotFoundError, TimeoutError, ValueError, OSError) as exc:
        print(f'ERROR: {exc}', flush=True)
        return 1

    if args.list:
        return _list_pieces(snapshot)

    if not args.square:
        print('ERROR: --square is required (or set CHESS_SOURCE)', flush=True)
        return 1

    piece_type = args.piece.strip() or None
    try:
        piece = piece_at_square(snapshot, args.square, piece_type)
    except (KeyError, ValueError) as exc:
        print(f'ERROR: {exc}', flush=True)
        return 1

    targets = eef_targets(
        piece,
        place_square=args.to.strip() or None,
        snapshot=snapshot,
    )
    if args.print_only:
        printable = {
            key: list(val) if isinstance(val, tuple) else val
            for key, val in targets.items()
        }
        print(json.dumps(printable, indent=2), flush=True)
        return 0

    execute = not args.plan_only
    if os.environ.get('AUTO_EXECUTE', '').strip().lower() in ('0', 'false', 'no'):
        execute = False
    return run_mtc(targets, execute=execute)


if __name__ == '__main__':
    sys.exit(main())
