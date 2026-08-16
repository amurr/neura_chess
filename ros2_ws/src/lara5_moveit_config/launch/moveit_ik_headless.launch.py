"""Minimal MoveIt stack for IK in Docker: robot_state_publisher + move_group only (no RViz, no ros2_control)."""

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description() -> LaunchDescription:
    pkg_share = get_package_share_directory('lara5_moveit_config')
    rsp_launch = os.path.join(pkg_share, 'launch', 'rsp.launch.py')
    move_group_launch = os.path.join(pkg_share, 'launch', 'move_group.launch.py')

    rsp = IncludeLaunchDescription(PythonLaunchDescriptionSource(rsp_launch))
    move_group = IncludeLaunchDescription(PythonLaunchDescriptionSource(move_group_launch))

    return LaunchDescription(
        [
            rsp,
            TimerAction(period=2.0, actions=[move_group]),
        ]
    )
