"""Stage 4: RViz with the MoveIt MotionPlanning plugin.

Reuses build_moveit_config() from moveit.launch.py, so RViz gets exactly the
same robot description, SRDF, kinematics and planning pipelines as move_group.

RViz is optional and nothing depends on it, so it is not gated on anything.
config/lara5.rviz shows RobotModel, MotionPlanning and the ChessBoard / ChessPieces
markers published by lara5_moveit/chess_scene_collisions (app.launch.py).

Usage:
  ros2 launch lara5_bringup rviz.launch.py
  ros2 launch lara5_bringup rviz.launch.py rviz_config:=/path/to/other.rviz
"""

import importlib.util
import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def load_sibling_launch_module(file_name: str, module_name: str):
    """Load another launch file from this directory as a Python module.

    Launch files are not on sys.path, so a plain `import` does not work.
    __file__ points to the installed copy in share/lara5_bringup/launch.
    """
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def launch_setup(context, *args, **kwargs):
    use_fake_hardware = LaunchConfiguration("use_fake_hardware").perform(context)
    hardware = LaunchConfiguration("hardware").perform(context)
    use_sim_time = LaunchConfiguration("use_sim_time").perform(context).lower() == "true"
    rviz_config = LaunchConfiguration("rviz_config").perform(context)

    moveit_launch = load_sibling_launch_module("moveit.launch.py", "lara5_moveit_launch")
    moveit_config = moveit_launch.build_moveit_config(use_fake_hardware, hardware)

    rviz = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="log",  # RViz is noisy; keep its output out of the main console
        arguments=["-d", rviz_config],
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.robot_description_kinematics,
            moveit_config.planning_pipelines,
            moveit_config.joint_limits,
            {"use_sim_time": use_sim_time},
        ],
    )

    return [rviz]


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
            "rviz_config",
            default_value=PathJoinSubstitution(
                [FindPackageShare("lara5_bringup"), "config", "lara5.rviz"]
            ),
            description="Full path to the RViz config file.",
        ),
    ]

    return LaunchDescription(declared_arguments + [OpaqueFunction(function=launch_setup)])