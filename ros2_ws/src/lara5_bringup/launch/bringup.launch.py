"""Top-level bringup: includes all stages with shared arguments.

Stages and how their order is enforced:
  1. description.launch.py  robot_state_publisher          (started immediately)
  2. control.launch.py      controller_manager + spawners  (spawners chained with OnProcessExit)
  3. moveit.launch.py       move_group                     (started immediately, finds controllers on use)
  4. rviz.launch.py         RViz                           (optional, no dependencies)
  5. app.launch.py          chess scene, moveit_master     (gated on move_group + trajectory controller)

use_fake_hardware and use_sim_time are passed to every stage, so all nodes
load the same robot model and use the same clock.

Do not run together with lara5_moveit_config/rviz_moveit.launch.py: both start
their own move_group and publish /joint_states.

Usage:
  ros2 launch lara5_bringup bringup.launch.py
  ros2 launch lara5_bringup bringup.launch.py board:=big
  ros2 launch lara5_bringup bringup.launch.py use_rviz:=false launch_app:=false
  ros2 launch lara5_bringup bringup.launch.py orchestrator:=true
  ros2 launch lara5_bringup bringup.launch.py use_fake_hardware:=false launch_control:=false  # external driver
  ros2 launch lara5_bringup bringup.launch.py use_sim_time:=true launch_control:=false        # simulator
"""

import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def include(file_name: str, launch_arguments: dict, condition=None):
    return IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([FindPackageShare("lara5_bringup"), "launch", file_name])
        ),
        launch_arguments=launch_arguments.items(),
        condition=condition,
    )


def generate_launch_description():
    use_fake_hardware = LaunchConfiguration("use_fake_hardware")
    use_sim_time = LaunchConfiguration("use_sim_time")
    use_rviz = LaunchConfiguration("use_rviz")
    launch_control = LaunchConfiguration("launch_control")
    launch_app = LaunchConfiguration("launch_app")
    controllers_file = LaunchConfiguration("controllers_file")
    app_params_file = LaunchConfiguration("app_params_file")
    board = LaunchConfiguration("board")
    pieces = LaunchConfiguration("pieces")
    scene_demo = LaunchConfiguration("scene_demo")
    orchestrator = LaunchConfiguration("orchestrator")

    declared_arguments = [
        DeclareLaunchArgument(
            "use_fake_hardware",
            default_value="true",
            description="Use mock_components/GenericSystem instead of the real hardware plugin.",
        ),
        DeclareLaunchArgument(
            "use_sim_time",
            default_value="false",
            description="Use /clock from a simulator.",
        ),
        DeclareLaunchArgument(
            "use_rviz",
            default_value="true",
            description="Start RViz.",
        ),
        DeclareLaunchArgument(
            "launch_control",
            default_value="true",
            description="Start ros2_control. Set false when a simulator or robot driver serves the controllers.",
        ),
        DeclareLaunchArgument(
            "launch_app",
            default_value="true",
            description="Start the application nodes (chess scene, moveit_master).",
        ),
        DeclareLaunchArgument(
            "controllers_file",
            default_value=PathJoinSubstitution(
                [FindPackageShare("lara5_bringup"), "config", "ros2_controllers.yaml"]
            ),
            description="Full path to the ros2_control controllers YAML.",
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
    ]

    # Docker with a bind-mounted X socket: same environment as the other Lara5
    # launch files, so every stage's nodes discover each other and RViz can draw.
    environment = [
        SetEnvironmentVariable("RMW_IMPLEMENTATION", os.environ.get("RMW_IMPLEMENTATION", "rmw_fastrtps_cpp")),
        SetEnvironmentVariable("ROS_DOMAIN_ID", os.environ.get("ROS_DOMAIN_ID", "0")),
        SetEnvironmentVariable("ROS_LOCALHOST_ONLY", "1"),
        SetEnvironmentVariable("QT_QPA_PLATFORM", "xcb"),
    ]

    common = {"use_fake_hardware": use_fake_hardware, "use_sim_time": use_sim_time}

    description = include("description.launch.py", common)

    control = include(
        "control.launch.py",
        {"use_sim_time": use_sim_time, "controllers_file": controllers_file},
        condition=IfCondition(launch_control),
    )

    moveit = include("moveit.launch.py", common)

    rviz = include("rviz.launch.py", common, condition=IfCondition(use_rviz))

    app = include(
        "app.launch.py",
        {
            **common,
            "app_params_file": app_params_file,
            "board": board,
            "pieces": pieces,
            "scene_demo": scene_demo,
            "orchestrator": orchestrator,
        },
        condition=IfCondition(launch_app),
    )

    return LaunchDescription(
        declared_arguments + environment + [description, control, moveit, rviz, app]
    )
