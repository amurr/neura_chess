"""Stage 5: application nodes.

Startup order:
  1. wait_for_system (optional gate): a short-lived process that exits once
     move_group (/get_planning_scene service) and the arm trajectory controller
     (FollowJointTrajectory action server) are available.
  2. after the gate:
     - chess_scene_collisions (lara5_moveit)   board:=small|big|none, long-running
     - moveit_master (moveit_master, C++)      /moveit_master/execute_sequence, long-running
     - planning_scene_updater                  scene_demo:=true, one-shot demo, exits
     - articulation_orchestrator               orchestrator:=true, one-shot demo, exits;
                                               started once moveit_master's process is up

If the gate times out, the application nodes are not started and an error is logged.

The gate is a safety net, not a replacement: the nodes themselves should still
wait for the services, actions and TF frames they use (see earlier recommendations).

Usage:
  ros2 launch lara5_bringup app.launch.py
  ros2 launch lara5_bringup app.launch.py board:=big pieces:=false
  ros2 launch lara5_bringup app.launch.py orchestrator:=true
  ros2 launch lara5_bringup app.launch.py wait_for_system:=false
  ros2 launch lara5_bringup app.launch.py app_params_file:=/path/to/moveit_master.yaml
"""

import importlib.util
import os
import sys

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    ExecuteProcess,
    LogInfo,
    OpaqueFunction,
    RegisterEventHandler,
)
from launch.event_handlers import OnProcessExit, OnProcessStart
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


# Runs in a separate Python process. Exit code 0 = system ready, 1 = timeout.
WAIT_FOR_SYSTEM_SCRIPT = r"""
import sys
import time

import rclpy
from rclpy.action import ActionClient
from moveit_msgs.srv import GetPlanningScene
from control_msgs.action import FollowJointTrajectory

timeout = float(sys.argv[1])
trajectory_action = sys.argv[2] if len(sys.argv) > 2 else ""

rclpy.init()
node = rclpy.create_node("wait_for_system")
log = node.get_logger()
deadline = time.monotonic() + timeout


def remaining():
    return max(0.1, deadline - time.monotonic())


log.info("Waiting for move_group (/get_planning_scene) ...")
ok = node.create_client(GetPlanningScene, "/get_planning_scene").wait_for_service(
    timeout_sec=remaining()
)

if ok and trajectory_action:
    log.info(f"Waiting for trajectory controller ({trajectory_action}) ...")
    ok = ActionClient(node, FollowJointTrajectory, trajectory_action).wait_for_server(
        timeout_sec=remaining()
    )

if ok:
    log.info("System ready, starting application nodes.")
else:
    log.error(f"System not ready after {timeout:.0f} s.")

node.destroy_node()
rclpy.shutdown()
sys.exit(0 if ok else 1)
"""


def load_sibling_launch_module(file_name: str, module_name: str):
    """Load another launch file from this directory as a Python module."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def launch_setup(context, *args, **kwargs):
    use_fake_hardware = LaunchConfiguration("use_fake_hardware").perform(context)
    hardware = LaunchConfiguration("hardware").perform(context)
    use_sim_time = LaunchConfiguration("use_sim_time").perform(context).lower() == "true"
    app_params_file = LaunchConfiguration("app_params_file").perform(context)
    board = LaunchConfiguration("board").perform(context)
    pieces = LaunchConfiguration("pieces").perform(context).lower() == "true"
    scene_demo = LaunchConfiguration("scene_demo").perform(context).lower() == "true"
    orchestrator = LaunchConfiguration("orchestrator").perform(context).lower() == "true"
    wait_for_system = LaunchConfiguration("wait_for_system").perform(context).lower() == "true"
    wait_timeout = LaunchConfiguration("wait_timeout").perform(context)
    trajectory_action = LaunchConfiguration("trajectory_action").perform(context)

    moveit_launch = load_sibling_launch_module("moveit.launch.py", "lara5_moveit_launch")
    moveit_config = moveit_launch.build_moveit_config(use_fake_hardware, hardware)

    sim_time = {"use_sim_time": use_sim_time}

    # MoveGroupInterface in moveit_master needs the description, the SRDF and
    # kinematics as its own parameters; later entries override earlier ones.
    moveit_master_parameters = [
        moveit_config.robot_description,
        moveit_config.robot_description_semantic,
        moveit_config.robot_description_kinematics,
        moveit_config.joint_limits,
        sim_time,
    ]
    if app_params_file:
        moveit_master_parameters.append(app_params_file)

    # Chess board + 32 pieces -> /planning_scene, markers -> /chess_*_markers.
    # Same node name for both boards, so only one runs. The big board must not get
    # chess_scene.yaml: it would overwrite square_size / a1 with the small-board values.
    chess_scene = []
    if board in ("small", "big"):
        chess_parameters = [{"publish_initial_pieces": pieces}, sim_time]
        if board == "small":
            chess_parameters.insert(0, os.path.join(
                get_package_share_directory("lara5_moveit"), "config", "chess_scene.yaml"))
        chess_scene.append(Node(
            package="lara5_moveit",
            executable="chess_scene_collisions" if board == "small" else "chess_scene_big",
            name="chess_scene_collisions",
            output="screen",
            parameters=chess_parameters,
            respawn=True,
            respawn_delay=1.0,
        ))

    # One-shot demo: add board + pawn via /apply_planning_scene, move the pawn, remove it.
    planning_scene_updater = Node(
        package="articulation_orchestrator",
        executable="planning_scene_updater",
        name="planning_scene_updater",
        output="screen",
        parameters=[sim_time],
    )

    moveit_master = Node(
        package="moveit_master",
        executable="moveit_master",
        name="moveit_master",
        output="screen",
        parameters=moveit_master_parameters,
    )

    # One-shot demo: sends its hard-coded MotionStep sequence to
    # /moveit_master/execute_sequence. It waits for that action server itself.
    articulation_orchestrator = Node(
        package="articulation_orchestrator",
        executable="articulation_orchestrator",
        name="articulation_orchestrator",
        output="screen",
        parameters=[sim_time],
    )

    app_actions = chess_scene + [moveit_master]
    if scene_demo:
        app_actions.append(planning_scene_updater)
    if orchestrator:
        # Note: OnProcessStart means "process launched", not "node ready".
        app_actions.append(RegisterEventHandler(
            OnProcessStart(target_action=moveit_master, on_start=[articulation_orchestrator])
        ))

    if not wait_for_system:
        return app_actions

    wait_for_system_process = ExecuteProcess(
        cmd=[sys.executable, "-c", WAIT_FOR_SYSTEM_SCRIPT, wait_timeout, trajectory_action],
        name="wait_for_system",
        output="screen",
    )

    def on_gate_exit(event, context):
        if event.returncode == 0:
            return app_actions
        return [
            LogInfo(
                msg="[app.launch.py] move_group or the trajectory controller did not come up "
                "in time. Application nodes were NOT started."
            )
        ]

    start_app_when_ready = RegisterEventHandler(
        OnProcessExit(target_action=wait_for_system_process, on_exit=on_gate_exit)
    )

    return [wait_for_system_process, start_app_when_ready]


def generate_launch_description():
    declared_arguments = [
        DeclareLaunchArgument(
            "use_fake_hardware",
            default_value="true",
            description="Must match the value used in description.launch.py.",
        ),
        DeclareLaunchArgument(
            "hardware",
            default_value="mock",
            description="Must match the value used in description.launch.py.",
        ),
        DeclareLaunchArgument(
            "use_sim_time",
            default_value="false",
            description="Use /clock from a simulator.",
        ),
        DeclareLaunchArgument(
            "app_params_file",
            default_value="",
            description="Optional YAML with extra parameters for moveit_master.",
        ),
        DeclareLaunchArgument(
            "board",
            default_value="small",
            description="Chess scene: 'small' (4 cm squares), 'big' (7.2 cm, max reach) or 'none'.",
        ),
        DeclareLaunchArgument(
            "pieces",
            default_value="true",
            description="Publish the 32 starting pieces into the planning scene.",
        ),
        DeclareLaunchArgument(
            "scene_demo",
            default_value="false",
            description="Run the planning_scene_updater demo (add/move/remove a pawn).",
        ),
        DeclareLaunchArgument(
            "orchestrator",
            default_value="false",
            description="Run articulation_orchestrator's demo sequence through moveit_master.",
        ),
        DeclareLaunchArgument(
            "wait_for_system",
            default_value="true",
            description="Wait for move_group and the trajectory controller before starting the nodes.",
        ),
        DeclareLaunchArgument(
            "wait_timeout",
            default_value="60.0",
            description="Seconds to wait for the system before giving up.",
        ),
        DeclareLaunchArgument(
            "trajectory_action",
            default_value="/arm_controller/follow_joint_trajectory",
            description="FollowJointTrajectory action to wait for. Empty string to skip.",
        ),
    ]

    return LaunchDescription(declared_arguments + [OpaqueFunction(function=launch_setup)])