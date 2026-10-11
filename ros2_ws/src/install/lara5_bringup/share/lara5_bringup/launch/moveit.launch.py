"""Stage 3: MoveIt (move_group).

Builds the MoveIt configuration with MoveItConfigsBuilder and starts move_group.
The builder runs in plain Python, so launch arguments are resolved first inside
an OpaqueFunction and then passed to xacro as mappings.

SRDF, kinematics, joint limits and Pilz limits come from lara5_moveit_config.
The URDF (config/lara5.urdf.xacro) and the controller mapping
(config/moveit_controllers.yaml) come from this package, so move_group,
robot_state_publisher and ros2_control all see the same robot.

Usage:
  ros2 launch lara5_bringup moveit.launch.py
  ros2 launch lara5_bringup moveit.launch.py use_fake_hardware:=false
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder


def build_moveit_config(use_fake_hardware: str):
    """Shared MoveIt config. Import and reuse this in rviz.launch.py and app.launch.py."""
    bringup_share = get_package_share_directory("lara5_bringup")
    return (
        MoveItConfigsBuilder("lara5", package_name="lara5_moveit_config")
        # Absolute paths: URDF and controller mapping live in lara5_bringup, not in the MoveIt config.
        .robot_description(
            file_path=os.path.join(bringup_share, "config", "lara5.urdf.xacro"),
            mappings={"use_fake_hardware": use_fake_hardware},
        )
        .robot_description_semantic(file_path="config/lara5.srdf")
        .robot_description_kinematics(file_path="config/kinematics.yaml")
        .joint_limits(file_path="config/joint_limits.yaml")
        .trajectory_execution(
            file_path=os.path.join(bringup_share, "config", "moveit_controllers.yaml")
        )
        .planning_scene_monitor(
            publish_robot_description=True,
            publish_robot_description_semantic=True,
        )
        .planning_pipelines(pipelines=["ompl", "pilz_industrial_motion_planner"])
        .pilz_cartesian_limits(file_path="config/pilz_cartesian_limits.yaml")
        .to_moveit_configs()
    )


def launch_setup(context, *args, **kwargs):
    # Resolve launch arguments to plain strings for the builder.
    use_fake_hardware = LaunchConfiguration("use_fake_hardware").perform(context)
    use_sim_time = LaunchConfiguration("use_sim_time").perform(context).lower() == "true"

    moveit_config = build_moveit_config(use_fake_hardware)

    # Humble's to_dict() does not include capabilities. ExecuteTaskSolutionCapability
    # serves /execute_task_solution for MTC task.execute() (lara5_mtc).
    move_group_capabilities = {"capabilities": "move_group/ExecuteTaskSolutionCapability"}

    move_group = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[
            moveit_config.to_dict(),
            move_group_capabilities,
            {"use_sim_time": use_sim_time},
        ],
    )

    return [move_group]


def generate_launch_description():
    declared_arguments = [
        DeclareLaunchArgument(
            "use_fake_hardware",
            default_value="true",
            description="Must match the value used in description.launch.py.",
        ),
        DeclareLaunchArgument(
            "use_sim_time",
            default_value="false",
            description="Use /clock from a simulator.",
        ),
    ]

    return LaunchDescription(declared_arguments + [OpaqueFunction(function=launch_setup)])
