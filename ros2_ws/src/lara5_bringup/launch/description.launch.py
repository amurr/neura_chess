"""Stage 1: robot description.

Starts robot_state_publisher with the URDF generated from
lara5_bringup/config/lara5.urdf.xacro (lara5_description + <ros2_control> block).
Optionally starts joint_state_publisher_gui for checking the URDF on its own
(leave it off when ros2_control is running, it publishes /joint_states itself).

The world -> lara5_root_link joint is part of the URDF, so robot_state_publisher
already publishes it; static_virtual_joint_tfs from lara5_moveit_config is not needed.

Usage:
  ros2 launch lara5_bringup description.launch.py
  ros2 launch lara5_bringup description.launch.py use_joint_state_publisher:=true
  ros2 launch lara5_bringup description.launch.py hardware:=isaac
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    use_fake_hardware = LaunchConfiguration("use_fake_hardware")
    hardware = LaunchConfiguration("hardware")
    use_sim_time = LaunchConfiguration("use_sim_time")
    use_joint_state_publisher = LaunchConfiguration("use_joint_state_publisher")

    declared_arguments = [
        DeclareLaunchArgument(
            "use_fake_hardware",
            default_value="true",
            description="Use mock_components/GenericSystem instead of the real hardware plugin.",
        ),
        DeclareLaunchArgument(
            "hardware",
            default_value="mock",
            description="ros2_control hardware: 'mock' (GenericSystem) or 'isaac' (topic_based_ros2_control).",
        ),
        DeclareLaunchArgument(
            "use_sim_time",
            default_value="false",
            description="Use /clock from a simulator.",
        ),
        DeclareLaunchArgument(
            "use_joint_state_publisher",
            default_value="false",
            description="Start joint_state_publisher_gui (only for viewing the URDF without ros2_control).",
        ),
    ]

    # Generate the URDF from xacro. Command handles launch arguments natively,
    # so the hardware switch is passed straight through as a xacro argument.
    robot_description_content = Command(
        [
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            PathJoinSubstitution(
                [FindPackageShare("lara5_bringup"), "config", "lara5.urdf.xacro"]
            ),
            " use_fake_hardware:=",
            use_fake_hardware,
            " hardware:=",
            hardware,
        ]
    )
    robot_description = {
        "robot_description": ParameterValue(robot_description_content, value_type=str)
    }

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[robot_description, {"use_sim_time": use_sim_time}],
    )

    joint_state_publisher_gui = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        output="screen",
        parameters=[robot_description, {"use_sim_time": use_sim_time}],
        condition=IfCondition(use_joint_state_publisher),
    )

    return LaunchDescription(
        declared_arguments + [robot_state_publisher, joint_state_publisher_gui]
    )
