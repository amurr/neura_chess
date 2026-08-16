#!/usr/bin/env python3
"""MTC chess pick-and-place — world-frame pick/place XYZ + gripper open/close.

For planning-scene pieces use ``lara5_chess_mtc_pick_place.py`` (Pick/Place).
See GRIPPER_INTEGRATION below and lara5.srdf states ``open`` / ``close``.

Run (with mtc_demo.launch.py in another terminal):
  ros2 launch lara5_moveit_config mtc_run.launch.py \\
    package:=lara5_moveit_config exe:=lara5_chess_pick_place.py

Tune poses to match your board (chess_scene_node board_a1/b1/a2 calibration).
"""

from __future__ import annotations

import math
import time
from typing import Sequence

import rclcpp
from geometry_msgs.msg import Point, Pose, PoseStamped, Quaternion, Vector3, Vector3Stamped
from moveit.task_constructor import core, stages
from std_msgs.msg import Header


rclcpp.init()
node = rclcpp.Node('lara5_mtc_chess_pick_place')

ARM = 'arm'
GRIPPER = 'gripper'
EEF_LINK = 'lara5_gripper'
WORLD = 'world'
HOME_POSE = 'stand'
SEED_POSE = 'pre_pick'  # arm over workspace; use mid_move if pre_pick fails
SEED_STAGE = 'seed pre_pick'
# Wait for MoveIt's planning scene monitor (move_group) to be available.
# If you run this without `mtc_demo.launch.py` (move_group + ros2_control), CurrentState will fail.
PLANNING_SCENE_TIMEOUT_S = 30.0

# Tune here (mirrors lara5_mtc_config.yaml keys for documentation).
# rclcpp.Node cannot declare_parameter; edit values or switch to an rclpy wrapper later.
pick_xyz = [0.30, 0.08, 0.12]
place_xyz = [0.30, 0.22, 0.12]
pick_rpy = [0.0, math.pi / 2.0, 0.0]  # default top-down; avoids many self-collisions vs roll=pi
place_rpy = [0.0, math.pi / 2.0, 0.0]
approach_m = 0.08
lift_m = 0.08
place_descent_m = 0.04
hover_z = 0.0
extra_hover_candidates_m = [0.00, 0.04, 0.08, 0.12]  # try higher hover to avoid self-collision

# Tool orientations to try for hover IK (roll=pi often hits link4 vs gripper_body).
pick_rpy_candidates = [
    pick_rpy,
    [0.0, math.pi / 2.0, math.pi / 2.0],
    [0.0, math.pi / 2.0, -math.pi / 2.0],
    [math.pi, 0.0, 0.0],
]
place_rpy_candidates = [
    place_rpy,
    [0.0, math.pi / 2.0, math.pi / 2.0],
    [0.0, math.pi / 2.0, -math.pi / 2.0],
]

jointspace = core.JointInterpolationPlanner()
cartesian = core.CartesianPath()
pipeline = core.PipelinePlanner(node)
pipeline.planner = 'RRTConnectkConfigDefault'
planners = [(ARM, pipeline)]


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


def world_pose_stamped(
    xyz: Sequence[float],
    rpy: Sequence[float],
    *,
    frame_id: str = WORLD,
) -> PoseStamped:
    x, y, z = float(xyz[0]), float(xyz[1]), float(xyz[2])
    qx, qy, qz, qw = euler_to_quaternion(float(rpy[0]), float(rpy[1]), float(rpy[2]))
    msg = PoseStamped()
    msg.header.frame_id = frame_id
    msg.pose = Pose(
        position=Point(x=x, y=y, z=z),
        orientation=Quaternion(x=qx, y=qy, z=qz, w=qw),
    )
    return msg


def add_connect(task: core.Task, name: str) -> None:
    connect = stages.Connect(name, planners)
    connect.properties.configureInitFrom(core.Stage.PropertyInitializerSource.PARENT)
    task.add(connect)


def add_move_to_named(task: core.Task, name: str, goal: str) -> None:
    move = stages.MoveTo(name, jointspace)
    move.group = ARM
    move.setGoal(goal)
    task.add(move)


def add_move_gripper(task: core.Task, name: str, goal: str) -> None:
    move = stages.MoveTo(name, jointspace)
    move.group = GRIPPER
    move.setGoal(goal)
    task.add(move)


def add_compute_ik_to_world_pose(
    task: core.Task,
    name: str,
    monitored_stage,
    target: PoseStamped,
) -> None:
    """Plan arm joints so ``EEF_LINK`` reaches ``target`` (world-frame goal)."""
    generator = stages.GeneratePose(f'{name} pose')
    generator.setMonitoredStage(monitored_stage)
    generator.pose = target

    ik = stages.ComputeIK(name, generator)
    ik.group = ARM
    ik.ik_frame = PoseStamped(header=Header(frame_id=EEF_LINK))
    ik.max_ik_solutions = 8
    props = ik.properties
    props.configureInitFrom(
        core.Stage.PropertyInitializerSource.INTERFACE, ['target_pose']
    )
    task.add(ik)


def add_compute_ik_alternatives(
    task: core.Task,
    name: str,
    monitored_stage,
    *,
    xyz: Sequence[float],
    rpy_candidates: Sequence[Sequence[float]],
    extra_hover_candidates: Sequence[float],
) -> None:
    """Try multiple IK targets (orientation/height) and let MTC pick a valid one."""
    alternatives = core.Alternatives(name)

    for dz in extra_hover_candidates:
        for idx, rpy in enumerate(rpy_candidates):
            target = world_pose_stamped(
                [xyz[0], xyz[1], xyz[2] + float(dz)],
                rpy,
            )
            stage_name = f'{name} dz={dz:.2f} rpy#{idx}'
            generator = stages.GeneratePose(f'{stage_name} pose')
            generator.setMonitoredStage(monitored_stage)
            generator.pose = target

            ik = stages.ComputeIK(stage_name, generator)
            ik.group = ARM
            ik.ik_frame = PoseStamped(header=Header(frame_id=EEF_LINK))
            ik.max_ik_solutions = 8
            props = ik.properties
            props.configureInitFrom(
                core.Stage.PropertyInitializerSource.INTERFACE, ['target_pose']
            )
            alternatives.insert(ik)

    task.add(alternatives)


def add_world_relative_z(task: core.Task, name: str, delta_z: float) -> None:
    move = stages.MoveRelative(name, cartesian)
    move.group = ARM
    move.setDirection(
        Vector3Stamped(
            header=Header(frame_id=WORLD),
            vector=Vector3(x=0.0, y=0.0, z=float(delta_z)),
        )
    )
    task.add(move)


# --- Build task tree (arm only) ---
task = core.Task()
task.name = 'lara5_chess_pick_place'
task.loadRobotModel(node)

current = stages.CurrentState('current state')
current.timeout = PLANNING_SCENE_TIMEOUT_S
task.add(current)

add_move_gripper(task, 'open gripper', 'open')

# Seed near the board, then Connect (MTC needs this before ComputeIK — see compute_ik demo).
add_move_to_named(task, SEED_STAGE, SEED_POSE)
add_connect(task, 'connect to pick hover')

# --- Pick sequence: try IK candidates until one plans (Fallback, not Alternatives) ---
pick_hover_xyz = [pick_xyz[0], pick_xyz[1], pick_xyz[2] + approach_m + hover_z]
pick_ik = core.Fallbacks('IK pick hover')
for dz in extra_hover_candidates_m:
    for idx, rpy in enumerate(pick_rpy_candidates):
        target = world_pose_stamped(
            [pick_hover_xyz[0], pick_hover_xyz[1], pick_hover_xyz[2] + float(dz)],
            rpy,
        )
        stage_name = f'pick IK dz={dz:.2f} rpy#{idx}'
        generator = stages.GeneratePose(f'{stage_name} pose')
        # MTC demos monitor a state stage (e.g. current), not the Connect stage before IK.
        generator.setMonitoredStage(task[SEED_STAGE])
        generator.pose = target
        ik = stages.ComputeIK(stage_name, generator)
        ik.group = ARM
        ik.ik_frame = PoseStamped(header=Header(frame_id=EEF_LINK))
        ik.max_ik_solutions = 8
        ik.properties.configureInitFrom(
            core.Stage.PropertyInitializerSource.INTERFACE, ['target_pose']
        )
        pick_ik.insert(ik)
task.add(pick_ik)

add_world_relative_z(task, 'approach pick (world -Z)', -approach_m)
add_move_gripper(task, 'close gripper', 'close')

add_world_relative_z(task, 'lift from pick (world +Z)', lift_m)

# --- Place sequence ---
add_connect(task, 'connect to place hover')
place_hover_xyz = [place_xyz[0], place_xyz[1], place_xyz[2] + place_descent_m + hover_z]
place_ik = core.Fallbacks('IK place hover')
for dz in extra_hover_candidates_m:
    for idx, rpy in enumerate(place_rpy_candidates):
        target = world_pose_stamped(
            [place_hover_xyz[0], place_hover_xyz[1], place_hover_xyz[2] + float(dz)],
            rpy,
        )
        stage_name = f'place IK dz={dz:.2f} rpy#{idx}'
        generator = stages.GeneratePose(f'{stage_name} pose')
        generator.setMonitoredStage(task['lift from pick (world +Z)'])
        generator.pose = target
        ik = stages.ComputeIK(stage_name, generator)
        ik.group = ARM
        ik.ik_frame = PoseStamped(header=Header(frame_id=EEF_LINK))
        ik.max_ik_solutions = 8
        ik.properties.configureInitFrom(
            core.Stage.PropertyInitializerSource.INTERFACE, ['target_pose']
        )
        place_ik.insert(ik)
task.add(place_ik)

add_world_relative_z(task, 'descend place (world -Z)', -place_descent_m)
add_move_gripper(task, 'open gripper', 'open')

add_world_relative_z(task, 'retreat after place (world +Z)', place_descent_m + 0.02)

# --- Return home (joint-space goal; no Connect — avoids interface mismatch) ---
add_move_to_named(task, 'move to stand', HOME_POSE)

print(
    f'pick_xyz={pick_xyz} place_xyz={place_xyz} '
    f'approach_m={approach_m} lift_m={lift_m}',
    flush=True,
)

if task.plan():
    task.publish(task.solutions[0])
    print(
        'Planning succeeded — expand stages in RViz, then Execute the root solution',
        flush=True,
    )
else:
    print('Planning failed — check terminal for failing stage name', flush=True)

time.sleep(100)
