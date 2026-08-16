#!/usr/bin/env python3
"""MTC chess pick-and-place using Pick/Place containers and planning-scene pieces.

Requires ``chess_scene`` publishing ``piece_<square>`` collision objects and
``mtc_demo_headless.launch.py`` (move_group + ros2_control).

Environment (optional):
  CHESS_SOURCE / CHESS_TARGET     squares, default e2 / e4
  CHESS_OCCUPANCY_FILE            path to occupancy JSON (else standard_start.json)
  CHESS_SEED_POSE                 arm seed state, default pre_pick (try mid_move)
  CHESS_GRASP_CLEARANCE_M         metres above pawn top for top-down IK, default 0.015
  CHESS_PUBLISH_OCCUPANCY=1       publish updated /chess_occupancy after successful plan

Run:
  ros2 launch xyz_motion chess_scene.launch.py
  ros2 launch lara5_moveit_config mtc_demo_headless.launch.py
  ros2 launch lara5_moveit_config mtc_run.launch.py \\
    package:=lara5_moveit_config exe:=lara5_chess_mtc_pick_place.py
"""

from __future__ import annotations

import copy
import json
import math
import os
import time

import rclcpp
from ament_index_python.packages import get_package_share_directory
from geometry_msgs.msg import Point, Pose, PoseStamped, Quaternion, Twist, TwistStamped
from moveit.task_constructor import core, stages
from std_msgs.msg import Header, String

try:
    from xyz_motion.chess_scene import (
        board_square_object_id,
        iter_board_squares,
        piece_dimensions,
        piece_object_id,
    )
    from xyz_motion.chess_xyz import chess_occupancy_to_pose6
except ImportError:  # fallback when xyz_motion not on PYTHONPATH

    def piece_object_id(square: str) -> str:
        return f'piece_{square.strip().lower()}'

    def board_square_object_id(square: str) -> str:
        return f'board_sq_{square.strip().lower()}'

    def iter_board_squares():
        for rank in '12345678':
            for file in 'abcdefgh':
                yield f'{file}{rank}'

    def chess_occupancy_to_pose6(data: dict, **_kwargs) -> dict[str, list[float]]:
        out: dict[str, list[float]] = {}
        squares = data.get('squares', {})
        if isinstance(squares, dict):
            for name, val in squares.items():
                if isinstance(val, dict) and all(k in val for k in ('x', 'y', 'z')):
                    out[name.lower()] = [
                        float(val['x']),
                        float(val['y']),
                        float(val['z']),
                        0.0,
                        0.0,
                        0.0,
                    ]
        return out

    def piece_dimensions(  # type: ignore[misc]
        piece_type: str,
        overrides=None,
        *,
        default_diameter: float = 0.035,
        default_height: float = 0.05,
    ) -> tuple[float, float]:
        _FALLBACK = {
            'pawn': (0.018, 0.034),
            'bishop': (0.022, 0.047),
            'knight': (0.024, 0.049),
            'rook': (0.026, 0.044),
            'queen': (0.027, 0.058),
            'king': (0.029, 0.066),
        }
        ptype = str(piece_type).strip().lower()
        if overrides and ptype in overrides and len(overrides[ptype]) >= 2:
            return float(overrides[ptype][0]), float(overrides[ptype][1])
        return _FALLBACK.get(ptype, (default_diameter, default_height))


rclcpp.init()
node = rclcpp.Node('lara5_mtc_chess_pick_place')

ARM = 'arm'
GRIPPER = 'gripper'
EEF = 'lerobot_gripper'
EEF_LINK = 'lara5_gripper'
WORLD = 'world'
HOME_POSE = 'stand'
SEED_POSE = os.environ.get('CHESS_SEED_POSE', 'pre_pick').strip() or 'pre_pick'
SEED_STAGE = f'seed {SEED_POSE}'
CURRENT_STAGE = 'current state'
PLANNING_SCENE_TIMEOUT_S = 30.0

# Top-down grasp: tool Z perpendicular to board, approach along world -Z.
TOP_DOWN_RPY = (0.0, math.pi / 2.0, 0.0)
PAWN_TOP_DOWN_ANGLE_DELTA = 2.0 * math.pi  # one yaw sample (symmetric cylinder)
DEFAULT_GRASP_ANGLE_DELTA = math.pi / 6.0

# Approach / lift distances (metres).
APPROACH_MIN = 0.03
APPROACH_MAX = 0.10
PAWN_APPROACH_MIN = 0.05
PAWN_APPROACH_MAX = 0.12
LIFT_MIN = 0.02
LIFT_MAX = 0.12
PLACE_MIN = 0.02
PLACE_MAX = 0.05
RETRACT_MIN = 0.02
RETRACT_MAX = 0.05
GRASP_CLEARANCE_M = 0.015

jointspace = core.JointInterpolationPlanner()
pipeline = core.PipelinePlanner(node)
pipeline.planner = 'RRTConnectkConfigDefault'
planners = [(ARM, pipeline)]


def load_occupancy() -> dict:
    path = os.environ.get('CHESS_OCCUPANCY_FILE', '').strip()
    if not path:
        share = get_package_share_directory('xyz_motion')
        path = os.path.join(share, 'examples', 'standard_start.json')
    with open(path, encoding='utf-8') as fh:
        return json.load(fh)


def resolve_move(occ: dict) -> tuple[str, str, dict]:
    source = (
        os.environ.get('CHESS_SOURCE')
        or occ.get('source')
        or occ.get('from')
        or occ.get('from_square')
        or 'e2'
    )
    target = (
        os.environ.get('CHESS_TARGET')
        or occ.get('target')
        or occ.get('to')
        or occ.get('to_square')
        or 'e4'
    )
    return str(source).strip().lower(), str(target).strip().lower(), occ


def resolve_piece_type(occ: dict, square: str) -> str:
    squares = occ.get('squares')
    if isinstance(squares, dict):
        entry = squares.get(square.strip().lower())
        if isinstance(entry, dict):
            ptype = entry.get('type')
            if ptype:
                return str(ptype).strip().lower()
    return 'pawn'


def euler_to_quaternion(roll: float, pitch: float, yaw: float) -> tuple[float, float, float, float]:
    cr, sr = math.cos(roll * 0.5), math.sin(roll * 0.5)
    cp, sp = math.cos(pitch * 0.5), math.sin(pitch * 0.5)
    cy, sy = math.cos(yaw * 0.5), math.sin(yaw * 0.5)
    return (
        sr * cp * cy - cr * sp * sy,
        cr * sp * cy + sr * cp * sy,
        cr * cp * sy - sr * sp * cy,
        cr * cp * cy + sr * sp * sy,
    )


def cylinder_center_z(surface_z: float, height: float) -> float:
    """Match chess_scene cylinder collision (center = board top + height/2)."""
    return float(surface_z) + float(height) / 2.0


def world_pose_with_rpy(
    x: float,
    y: float,
    z: float,
    rpy: tuple[float, float, float],
) -> PoseStamped:
    qx, qy, qz, qw = euler_to_quaternion(*rpy)
    msg = PoseStamped()
    msg.header.frame_id = WORLD
    msg.pose = Pose(
        position=Point(x=x, y=y, z=z),
        orientation=Quaternion(x=qx, y=qy, z=qz, w=qw),
    )
    return msg


def make_top_down_ik_frame(*, piece_height: float, piece_type: str) -> PoseStamped:
    """EEF offset for vertical pick on a cylinder collision object."""
    clearance = float(os.environ.get('CHESS_GRASP_CLEARANCE_M', str(GRASP_CLEARANCE_M)))
    if piece_type == 'pawn':
        # Grasp above pawn top; collision cylinder center is at height/2 above board.
        z_offset = piece_height / 2.0 + clearance
    else:
        z_offset = float(os.environ.get('CHESS_GRASP_Z_OFFSET_M', '0.03'))

    ik_frame = PoseStamped()
    ik_frame.header.frame_id = EEF_LINK
    qx, qy, qz, qw = euler_to_quaternion(*TOP_DOWN_RPY)
    ik_frame.pose.orientation = Quaternion(x=qx, y=qy, z=qz, w=qw)
    ik_frame.pose.position.z = z_offset
    return ik_frame


def infer_square_xyz(occ: dict, square: str, *, from_square: str | None = None) -> tuple[float, float, float]:
    """Infer empty-square XYZ from a neighbour (board step 0.04 m, ranks along +X)."""
    poses = chess_occupancy_to_pose6(occ)
    sq = square.strip().lower()
    if sq in poses:
        return float(poses[sq][0]), float(poses[sq][1]), float(poses[sq][2])
    ref = (from_square or '').strip().lower()
    if ref not in poses:
        raise RuntimeError(f'cannot infer {sq!r}: reference square {ref!r} has no XYZ')
    sx, sy, sz = (float(poses[ref][i]) for i in range(3))
    step = float(os.environ.get('CHESS_SQUARE_SIZE_M', '0.04'))
    df = ord(sq[0]) - ord(ref[0])
    dr = int(sq[1]) - int(ref[1])
    return sx + dr * step, sy + df * step, sz


def square_pose_stamped(
    occ: dict,
    square: str,
    *,
    from_square: str | None = None,
    piece_type: str = 'pawn',
) -> PoseStamped:
    sq = square.strip().lower()
    x, y, z = infer_square_xyz(occ, sq, from_square=from_square)
    diameter, height = piece_dimensions(piece_type)
    z_center = cylinder_center_z(z, height)
    return world_pose_with_rpy(x, y, z_center, TOP_DOWN_RPY)


def add_allow_gripper_target_collision(task: core.Task, object_id: str) -> None:
    """Allow gripper vs the picked piece during grasp IK (cylinder top-down)."""
    mps = stages.ModifyPlanningScene(f'allow gripper on {object_id}')
    gripper_links = (
        EEF_LINK,
        'lara5_gripper_body',
        'lara5_gripper_jaw',
        'lara5_gripper_adapter',
    )
    mps.allowCollisions(object_id, True)
    for link in gripper_links:
        mps.allowCollisions(object_id, link, True)
    task.add(mps)


def build_pick_stage(
    task: core.Task,
    object_id: str,
    *,
    piece_type: str,
    piece_height: float,
) -> stages.Pick:
    grasp_generator = stages.GenerateGraspPose('generate grasp')
    if piece_type == 'pawn':
        # Single top-down orientation; cylinder is rotation-symmetric in XY.
        grasp_generator.angle_delta = PAWN_TOP_DOWN_ANGLE_DELTA
    else:
        grasp_generator.angle_delta = DEFAULT_GRASP_ANGLE_DELTA
    if hasattr(grasp_generator, 'rotation_axis'):
        grasp_generator.rotation_axis = (0.0, 0.0, 1.0)
    grasp_generator.pregrasp = 'open'
    grasp_generator.grasp = 'close'
    grasp_generator.setMonitoredStage(task[SEED_STAGE])

    simple_grasp = stages.SimpleGrasp(grasp_generator, 'grasp')
    simple_grasp.setIKFrame(
        make_top_down_ik_frame(piece_height=piece_height, piece_type=piece_type)
    )

    pick = stages.Pick(simple_grasp, 'pick')
    pick.eef = EEF
    pick.object = object_id

    approach = TwistStamped()
    approach.header.frame_id = WORLD
    approach.twist.linear.z = -1.0
    if piece_type == 'pawn':
        pick.setApproachMotion(approach, PAWN_APPROACH_MIN, PAWN_APPROACH_MAX)
    else:
        pick.setApproachMotion(approach, APPROACH_MIN, APPROACH_MAX)

    lift = TwistStamped()
    lift.header.frame_id = WORLD
    lift.twist.linear.z = 1.0
    pick.setLiftMotion(lift, LIFT_MIN, LIFT_MAX)
    return pick


def apply_move_to_occupancy(occ: dict, source: str, target: str) -> dict:
    """Build occupancy JSON after moving piece source → target."""
    updated = copy.deepcopy(occ)
    source = source.lower()
    target = target.lower()
    updated['source'] = source
    updated['target'] = target

    squares = updated.get('squares')
    if not isinstance(squares, dict):
        squares = {}
        for key, val in list(updated.items()):
            if key in {
                'turn', 'fen', 'source', 'target', 'from', 'to',
                'from_square', 'to_square',
            }:
                continue
            if isinstance(key, str) and len(key) == 2 and key[0].isalpha():
                squares[key] = val
        updated['squares'] = squares

    piece = squares.pop(source, None)
    if piece is None:
        raise RuntimeError(f'square {source!r} not in occupancy squares')
    if target in squares:
        squares.pop(target, None)  # capture
    if isinstance(piece, dict):
        piece = copy.deepcopy(piece)
        tx, ty, tz = infer_square_xyz(updated, target, from_square=source)
        piece['x'] = tx
        piece['y'] = ty
        piece['z'] = tz
    squares[target] = piece
    return updated


def move_gripper(name: str, goal: str) -> stages.MoveTo:
    stage = stages.MoveTo(name, jointspace)
    stage.group = GRIPPER
    stage.setGoal(goal)
    return stage


def add_connect(task: core.Task, name: str) -> None:
    connect = stages.Connect(name, planners)
    connect.properties.configureInitFrom(core.Stage.PropertyInitializerSource.PARENT)
    task.add(connect)


def add_move_arm_named(task: core.Task, name: str, goal: str) -> None:
    move = stages.MoveTo(name, jointspace)
    move.group = ARM
    move.setGoal(goal)
    task.add(move)


def add_allow_gripper_board_collisions(task: core.Task) -> None:
    """Board square collision boxes block grasp IK; allow gripper vs board_sq_*."""
    mps = stages.ModifyPlanningScene('allow gripper on board squares')
    gripper_links = (
        EEF_LINK,
        'lara5_gripper_body',
        'lara5_gripper_jaw',
        'lara5_gripper_adapter',
    )
    for square in iter_board_squares():
        obj = board_square_object_id(square)
        mps.allowCollisions(obj, True)
        for link in gripper_links:
            mps.allowCollisions(obj, link, True)
    task.add(mps)


def build_place_stage(
    task: core.Task,
    object_id: str,
    place_pose: PoseStamped,
) -> stages.Place:
    place_generator = stages.GeneratePlacePose('generate place')
    place_generator.setMonitoredStage(task['pick'])
    place_generator.object = object_id
    place_generator.pose = place_pose

    simple_ungrasp = stages.SimpleUnGrasp(place_generator, 'ungrasp')
    place = stages.Place(simple_ungrasp, 'place')
    place.eef = EEF
    place.object = object_id
    place.eef_frame = EEF_LINK

    place_motion = TwistStamped()
    place_motion.header.frame_id = EEF_LINK
    place_motion.twist.linear.z = -1.0
    place.setPlaceMotion(place_motion, PLACE_MIN, PLACE_MAX)

    retract = TwistStamped()
    retract.header.frame_id = WORLD
    retract.twist.linear.z = 1.0
    place.setRetractMotion(retract, RETRACT_MIN, RETRACT_MAX)
    return place


def publish_occupancy(occ: dict) -> None:
    pub = node.create_publisher(String, '/chess_occupancy', 10)
    deadline = time.time() + 5.0
    while pub.get_subscription_count() == 0 and time.time() < deadline:
        rclcpp.spin_once(node, timeout_sec=0.1)
    msg = String()
    msg.data = json.dumps(occ)
    pub.publish(msg)
    print(f'Published /chess_occupancy ({len(msg.data)} bytes)', flush=True)


# --- Load move ---
occupancy = load_occupancy()
source_square, target_square, occupancy = resolve_move(occupancy)
piece_type = resolve_piece_type(occupancy, source_square)
piece_diameter, piece_height = piece_dimensions(piece_type)
object_id = piece_object_id(source_square)
place_pose = square_pose_stamped(
    occupancy,
    target_square,
    from_square=source_square,
    piece_type=piece_type,
)

print(
    f'Move {source_square} -> {target_square}  type={piece_type}  '
    f'cylinder(d={piece_diameter:.3f}, h={piece_height:.3f})  '
    f'object={object_id}  '
    f'place=({place_pose.pose.position.x:.3f}, '
    f'{place_pose.pose.position.y:.3f}, {place_pose.pose.position.z:.3f})  '
    f'seed={SEED_POSE}',
    flush=True,
)

# --- Task tree ---
task = core.Task()
task.name = 'lara5_chess_mtc_pick_place'
task.loadRobotModel(node)

current = stages.CurrentState(CURRENT_STAGE)
current.timeout = PLANNING_SCENE_TIMEOUT_S
task.add(current)

add_allow_gripper_board_collisions(task)
task.add(move_gripper('open gripper', 'open'))
add_move_arm_named(task, SEED_STAGE, SEED_POSE)
add_allow_gripper_target_collision(task, object_id)
add_connect(task, 'connect to pick')
task.add(
    build_pick_stage(
        task,
        object_id,
        piece_type=piece_type,
        piece_height=piece_height,
    )
)
add_connect(task, 'connect to place')
task.add(build_place_stage(task, object_id, place_pose))
add_move_arm_named(task, 'move to stand', HOME_POSE)

if task.plan():
    task.publish(task.solutions[0])
    print('Planning succeeded', flush=True)
    auto_execute = os.environ.get('AUTO_EXECUTE', '').strip().lower() in ('1', 'true', 'yes')
    if auto_execute:
        result = task.execute(task.solutions[0])
        if result.val != 1:
            print(f'Execution failed (error code {result.val})', flush=True)
        else:
            print('Execution succeeded — watch motion in RViz', flush=True)
    else:
        print('Set AUTO_EXECUTE=true to execute, or use auto_execute:=true on launch', flush=True)
    if os.environ.get('CHESS_PUBLISH_OCCUPANCY', '').strip() in ('1', 'true', 'yes'):
        try:
            publish_occupancy(apply_move_to_occupancy(occupancy, source_square, target_square))
        except Exception as exc:
            print(f'Could not publish occupancy update: {exc}', flush=True)
else:
    print('Planning failed — ensure chess_scene is running and piece is in the scene', flush=True)

time.sleep(100)
