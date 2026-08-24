#!/usr/bin/env python3
"""Pick a chess piece using Isaac Sim poses and MoveIt trajectories."""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Mapping, Sequence

from lara5_moveit.piece_poses import (
    DOWN_RPY,
    eef_targets,
    fetch_isaac_snapshot,
    load_snapshot,
    piece_at_square,
)


ARM = 'arm'
EEF_LINK = 'lara5_gripper'
WORLD = 'world'
HOME_POSE = 'stand'
SEED_POSE = 'pre_pick'

ARM_JOINTS = (
    'lara5_joint1',
    'lara5_joint2',
    'lara5_joint3',
    'lara5_joint4',
    'lara5_joint5',
    'lara5_joint6',
)
NAMED_ARM = {
    'stand': (0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
    'pre_pick': (0.55, 0.35, 1.25, 0.0, 1.05, 0.0),
    'mid_move': (0.0, 0.0, 1.5, 0.0, 1.5, 0.0),
}
GRIPPER_NAMED = {
    'open': 1.74533,
    'close': -0.174533,
}
GRIPPER_ACTION = '/gripper_controller/gripper_cmd'
MOVE_ACTION = '/move_action'
EXECUTE_ACTION = '/execute_trajectory'
IK_SERVICE = '/compute_ik'
CARTESIAN_SERVICE = '/compute_cartesian_path'

JOINT_TOL = 0.02
POSE_POS_TOL = 0.005
POSE_ORI_TOL = 0.1
CART_MAX_STEP = 0.01
CART_MIN_FRACTION = 0.9
VEL_SCALE = 0.25
ACC_SCALE = 0.25
PLAN_TIME_S = 10.0
PLAN_ATTEMPTS = 8
ACTION_WAIT_S = 20.0
MOVE_TIMEOUT_S = 90.0
GRIPPER_TIMEOUT_S = 15.0
GRIPPER_EFFORT = 20.0
HOVER_Z_TRIES = (0.0, 0.04, 0.08)


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


def motion_steps(targets: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Return the pick / place sequence as named MoveIt motions."""
    quat = tuple(targets['orientation_xyzw'])
    steps: list[dict[str, Any]] = [
        {'kind': 'gripper', 'name': 'open gripper', 'goal': 'open'},
        {'kind': 'named', 'name': f'seed {SEED_POSE}', 'goal': SEED_POSE},
        {'kind': 'pose', 'name': 'pick hover', 'xyz': targets['pick_hover'], 'quat': quat},
        {
            'kind': 'cartesian',
            'name': 'approach pick',
            'xyz': targets['pick_grasp'],
            'quat': quat,
        },
        {'kind': 'gripper', 'name': 'close gripper', 'goal': 'close'},
        {'kind': 'cartesian', 'name': 'lift', 'xyz': targets['pick_hover'], 'quat': quat},
    ]
    if 'place_hover' in targets:
        steps.extend(
            [
                {
                    'kind': 'pose',
                    'name': 'place hover',
                    'xyz': targets['place_hover'],
                    'quat': quat,
                },
                {
                    'kind': 'cartesian',
                    'name': 'descend place',
                    'xyz': targets['place_grasp'],
                    'quat': quat,
                },
                {'kind': 'gripper', 'name': 'open gripper place', 'goal': 'open'},
                {
                    'kind': 'cartesian',
                    'name': 'retreat',
                    'xyz': targets['place_hover'],
                    'quat': quat,
                },
            ]
        )
    steps.append({'kind': 'named', 'name': f'move to {HOME_POSE}', 'goal': HOME_POSE})
    return steps


def _ok(code: int) -> bool:
    return int(code) == 1


def _xyz_pose(xyz: Sequence[float], quat: Sequence[float]):
    from geometry_msgs.msg import Point, Pose, Quaternion

    return Pose(
        position=Point(x=float(xyz[0]), y=float(xyz[1]), z=float(xyz[2])),
        orientation=Quaternion(
            x=float(quat[0]), y=float(quat[1]), z=float(quat[2]), w=float(quat[3])
        ),
    )


def _stamp_pose(xyz: Sequence[float], quat: Sequence[float], frame: str = WORLD):
    from geometry_msgs.msg import PoseStamped
    from std_msgs.msg import Header

    msg = PoseStamped()
    msg.header = Header(frame_id=frame)
    msg.pose = _xyz_pose(xyz, quat)
    return msg


def _arm_positions(joint_state) -> list[float] | None:
    lookup = dict(zip(list(joint_state.name), list(joint_state.position)))
    try:
        return [float(lookup[name]) for name in ARM_JOINTS]
    except KeyError:
        return None


class MoveItTrajectories:
    """Sequential MoveIt client: named poses, IK pose goals, Cartesian paths."""

    def __init__(self, node, *, execute: bool) -> None:
        """Connect action and service clients on ``node``."""
        from control_msgs.action import GripperCommand
        from moveit_msgs.action import ExecuteTrajectory, MoveGroup
        from moveit_msgs.srv import GetCartesianPath, GetPositionIK
        from rclpy.action import ActionClient
        from rclpy.callback_groups import ReentrantCallbackGroup

        self._node = node
        self._execute = execute
        self._last_arm: list[float] | None = None
        cb = ReentrantCallbackGroup()
        self._move = ActionClient(node, MoveGroup, MOVE_ACTION, callback_group=cb)
        self._exec = ActionClient(
            node, ExecuteTrajectory, EXECUTE_ACTION, callback_group=cb
        )
        self._grip = ActionClient(
            node, GripperCommand, GRIPPER_ACTION, callback_group=cb
        )
        self._ik = node.create_client(GetPositionIK, IK_SERVICE, callback_group=cb)
        self._cart = node.create_client(
            GetCartesianPath, CARTESIAN_SERVICE, callback_group=cb
        )

    def wait_for_servers(self) -> None:
        """Block until move_group actions and services are available."""
        missing = 'missing. Start ./scripts/launch/launch_moveit_isaac.sh first.'
        actions = (
            (self._move, f'MoveGroup {MOVE_ACTION}'),
            (self._exec, f'ExecuteTrajectory {EXECUTE_ACTION}'),
        )
        if self._execute:
            actions += ((self._grip, f'Gripper {GRIPPER_ACTION}'),)
        for client, label in actions:
            if not client.wait_for_server(timeout_sec=ACTION_WAIT_S):
                raise TimeoutError(f'{label} {missing}')
        for client, label in (
            (self._ik, f'GetPositionIK {IK_SERVICE}'),
            (self._cart, f'GetCartesianPath {CARTESIAN_SERVICE}'),
        ):
            if not client.wait_for_service(timeout_sec=ACTION_WAIT_S):
                raise TimeoutError(f'{label} {missing}')

    def run(self, steps: Sequence[Mapping[str, Any]]) -> int:
        """Plan (and optionally execute) each motion in order."""
        for step in steps:
            kind = str(step['kind'])
            name = str(step['name'])
            print(f'{name}...', flush=True)
            if kind == 'gripper':
                if not self._gripper(str(step['goal'])):
                    print(f'{name} failed', flush=True)
                    return 1
            elif kind == 'named':
                if not self._named(str(step['goal'])):
                    print(f'{name} failed', flush=True)
                    return 1
            elif kind == 'pose':
                if not self._pose(step['xyz'], step['quat']):
                    print(f'{name} failed', flush=True)
                    return 1
            elif kind == 'cartesian':
                if not self._cartesian(step['xyz'], step['quat']):
                    print(f'{name} failed', flush=True)
                    return 1
            else:
                print(f'unknown step {kind!r}', flush=True)
                return 1
            print(f'{name} ok', flush=True)
        return 0

    def _spin(self, future, timeout_s: float):
        import rclpy

        rclpy.spin_until_future_complete(self._node, future, timeout_sec=timeout_s)
        if not future.done():
            raise TimeoutError(f'MoveIt call timed out after {timeout_s:.0f}s')
        return future.result()

    def _send_action(self, client, goal, timeout_s: float):
        handle = self._spin(client.send_goal_async(goal), timeout_s)
        if handle is None or not handle.accepted:
            raise RuntimeError('MoveIt goal rejected')
        wrap = self._spin(handle.get_result_async(), timeout_s)
        return wrap.result

    def _start_state(self):
        from moveit_msgs.msg import RobotState
        from sensor_msgs.msg import JointState

        state = RobotState()
        state.is_diff = True
        if self._last_arm is not None:
            state.joint_state = JointState(name=list(ARM_JOINTS), position=self._last_arm)
        return state

    def _remember_traj(self, trajectory) -> None:
        points = trajectory.joint_trajectory.points
        names = list(trajectory.joint_trajectory.joint_names)
        if not points or not names:
            return
        lookup = dict(zip(names, list(points[-1].positions)))
        try:
            self._last_arm = [float(lookup[name]) for name in ARM_JOINTS]
        except KeyError:
            return

    def _named(self, goal: str) -> bool:
        if goal not in NAMED_ARM:
            print(f'unknown named pose {goal!r}', flush=True)
            return False
        return self._joint_goal(list(NAMED_ARM[goal]))

    def _joint_goal(self, positions: Sequence[float]) -> bool:
        from moveit_msgs.action import MoveGroup
        from moveit_msgs.msg import (
            Constraints,
            JointConstraint,
            MotionPlanRequest,
            PlanningOptions,
        )

        request = MotionPlanRequest()
        request.group_name = ARM
        request.num_planning_attempts = PLAN_ATTEMPTS
        request.allowed_planning_time = PLAN_TIME_S
        request.max_velocity_scaling_factor = VEL_SCALE
        request.max_acceleration_scaling_factor = ACC_SCALE
        request.pipeline_id = 'ompl'
        request.start_state = self._start_state()
        constraints = Constraints(name='joints')
        for name, position in zip(ARM_JOINTS, positions):
            constraints.joint_constraints.append(
                JointConstraint(
                    joint_name=name,
                    position=float(position),
                    tolerance_above=JOINT_TOL,
                    tolerance_below=JOINT_TOL,
                    weight=1.0,
                )
            )
        request.goal_constraints.append(constraints)
        goal = MoveGroup.Goal()
        goal.request = request
        goal.planning_options = PlanningOptions(
            plan_only=not self._execute,
            replan=self._execute,
            replan_attempts=3,
            replan_delay=0.1,
        )
        result = self._send_action(self._move, goal, MOVE_TIMEOUT_S)
        if not _ok(result.error_code.val):
            print(f'MoveGroup error_code={result.error_code.val}', flush=True)
            return False
        self._remember_traj(result.planned_trajectory)
        return True

    def _pose(self, xyz: Sequence[float], quat: Sequence[float]) -> bool:
        ik = self._solve_ik(xyz, quat)
        if ik is not None:
            return self._joint_goal(ik)
        print('IK failed, falling back to pose goal', flush=True)
        return self._pose_goal(xyz, quat)

    def _solve_ik(self, xyz: Sequence[float], quat: Sequence[float]) -> list[float] | None:
        from builtin_interfaces.msg import Duration
        from moveit_msgs.msg import PositionIKRequest
        from moveit_msgs.srv import GetPositionIK

        for dz in HOVER_Z_TRIES:
            req = GetPositionIK.Request()
            req.ik_request = PositionIKRequest()
            req.ik_request.group_name = ARM
            req.ik_request.ik_link_name = EEF_LINK
            req.ik_request.avoid_collisions = True
            req.ik_request.timeout = Duration(sec=1)
            req.ik_request.robot_state = self._start_state()
            req.ik_request.pose_stamped = _stamp_pose(
                (xyz[0], xyz[1], xyz[2] + dz), quat
            )
            resp = self._spin(self._ik.call_async(req), PLAN_TIME_S)
            if resp is None or not _ok(resp.error_code.val):
                continue
            positions = _arm_positions(resp.solution.joint_state)
            if positions is not None:
                if dz:
                    print(f'IK ok with dz={dz:.2f}', flush=True)
                return positions
        return None

    def _pose_goal(self, xyz: Sequence[float], quat: Sequence[float]) -> bool:
        from geometry_msgs.msg import Pose, Quaternion
        from moveit_msgs.action import MoveGroup
        from moveit_msgs.msg import (
            BoundingVolume,
            Constraints,
            MotionPlanRequest,
            OrientationConstraint,
            PlanningOptions,
            PositionConstraint,
        )
        from shape_msgs.msg import SolidPrimitive
        from std_msgs.msg import Header

        request = MotionPlanRequest()
        request.group_name = ARM
        request.num_planning_attempts = PLAN_ATTEMPTS
        request.allowed_planning_time = PLAN_TIME_S
        request.max_velocity_scaling_factor = VEL_SCALE
        request.max_acceleration_scaling_factor = ACC_SCALE
        request.pipeline_id = 'ompl'
        request.start_state = self._start_state()
        header = Header(frame_id=WORLD)
        sphere = SolidPrimitive(type=SolidPrimitive.SPHERE, dimensions=[POSE_POS_TOL])
        region = BoundingVolume(
            primitives=[sphere],
            primitive_poses=[Pose(orientation=Quaternion(w=1.0))],
        )
        region.primitive_poses[0].position.x = float(xyz[0])
        region.primitive_poses[0].position.y = float(xyz[1])
        region.primitive_poses[0].position.z = float(xyz[2])
        pos = PositionConstraint(
            header=header,
            link_name=EEF_LINK,
            constraint_region=region,
            weight=1.0,
        )
        ori = OrientationConstraint(
            header=header,
            link_name=EEF_LINK,
            orientation=Quaternion(
                x=float(quat[0]), y=float(quat[1]), z=float(quat[2]), w=float(quat[3])
            ),
            absolute_x_axis_tolerance=POSE_ORI_TOL,
            absolute_y_axis_tolerance=POSE_ORI_TOL,
            absolute_z_axis_tolerance=POSE_ORI_TOL,
            weight=1.0,
        )
        request.goal_constraints.append(
            Constraints(
                name='eef',
                position_constraints=[pos],
                orientation_constraints=[ori],
            )
        )
        goal = MoveGroup.Goal()
        goal.request = request
        goal.planning_options = PlanningOptions(
            plan_only=not self._execute,
            replan=self._execute,
            replan_attempts=3,
            replan_delay=0.1,
        )
        result = self._send_action(self._move, goal, MOVE_TIMEOUT_S)
        if not _ok(result.error_code.val):
            print(f'pose MoveGroup error_code={result.error_code.val}', flush=True)
            return False
        self._remember_traj(result.planned_trajectory)
        return True

    def _cartesian(self, xyz: Sequence[float], quat: Sequence[float]) -> bool:
        from moveit_msgs.action import ExecuteTrajectory
        from moveit_msgs.srv import GetCartesianPath
        from std_msgs.msg import Header

        from lara5_moveit.sanitize_trajectory import sanitize_joint_trajectory

        for avoid in (True, False):
            req = GetCartesianPath.Request()
            req.header = Header(frame_id=WORLD)
            req.start_state = self._start_state()
            req.group_name = ARM
            req.link_name = EEF_LINK
            req.waypoints = [_xyz_pose(xyz, quat)]
            req.max_step = CART_MAX_STEP
            req.jump_threshold = 0.0
            req.avoid_collisions = avoid
            resp = self._spin(self._cart.call_async(req), PLAN_TIME_S)
            if resp is None or not _ok(resp.error_code.val):
                continue
            if float(resp.fraction) < CART_MIN_FRACTION:
                print(
                    f'cartesian fraction={resp.fraction:.2f} avoid={avoid}',
                    flush=True,
                )
                continue
            traj = resp.solution
            traj.joint_trajectory = sanitize_joint_trajectory(traj.joint_trajectory)
            if not traj.joint_trajectory.points:
                continue
            if self._execute:
                goal = ExecuteTrajectory.Goal()
                goal.trajectory = traj
                result = self._send_action(self._exec, goal, MOVE_TIMEOUT_S)
                if not _ok(result.error_code.val):
                    print(
                        f'execute_trajectory error_code={result.error_code.val}',
                        flush=True,
                    )
                    return False
            self._remember_traj(traj)
            return True
        return False

    def _gripper(self, goal: str) -> bool:
        from control_msgs.action import GripperCommand

        if goal not in GRIPPER_NAMED:
            print(f'unknown gripper goal {goal!r}', flush=True)
            return False
        if not self._execute:
            return True
        msg = GripperCommand.Goal()
        msg.command.position = float(GRIPPER_NAMED[goal])
        msg.command.max_effort = GRIPPER_EFFORT
        try:
            result = self._send_action(self._grip, msg, GRIPPER_TIMEOUT_S)
        except (RuntimeError, TimeoutError) as exc:
            print(f'gripper {goal} warning: {exc}', flush=True)
            return True
        reached = bool(getattr(result, 'reached_goal', True))
        stalled = bool(getattr(result, 'stalled', False))
        if not reached and not stalled:
            print(f'gripper {goal} did not reach goal', flush=True)
        return True


def run_moveit(targets: dict[str, Any], *, execute: bool) -> int:
    """Plan (and optionally execute) pick / place as MoveIt trajectories."""
    try:
        import rclpy
        from rclpy.node import Node
    except ImportError as exc:
        print(
            f'ERROR: rclpy missing ({exc}). Source ROS 2 Humble + the workspace.',
            flush=True,
        )
        return 1

    steps = motion_steps(targets)
    print(
        f'pick={targets.get("square")} {targets["pick_grasp"]} '
        f'place={targets.get("place_square")} rpy={DOWN_RPY} '
        f'steps={len(steps)} execute={execute}',
        flush=True,
    )

    rclpy.init()
    node = Node('moveit_chess')
    try:
        client = MoveItTrajectories(node, execute=execute)
        client.wait_for_servers()
        rc = client.run(steps)
        if rc == 0:
            label = 'Planning succeeded' if not execute else 'Execution succeeded'
            print(label, flush=True)
        else:
            print('Planning failed' if not execute else 'Execution failed', flush=True)
        return rc
    except (TimeoutError, RuntimeError) as exc:
        print(f'ERROR: {exc}', flush=True)
        return 1
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


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
    return run_moveit(targets, execute=execute)


if __name__ == '__main__':
    sys.exit(main())
