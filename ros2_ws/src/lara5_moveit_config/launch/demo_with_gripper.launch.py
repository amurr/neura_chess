"""MoveIt demo plus gripper_joint_bridge (starts after controllers are up)."""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    pkg_moveit = get_package_share_directory('lara5_moveit_config')
    demo_launch = os.path.join(pkg_moveit, 'launch', 'demo.launch.py')
    bridge_config = os.path.join(
        get_package_share_directory('xyz_motion'),
        'config',
        'gripper_bridge.yaml',
    )

    gripper_bridge = Node(
        package='xyz_motion',
        executable='gripper_joint_bridge',
        name='gripper_joint_bridge',
        output='screen',
        parameters=[bridge_config, {'forward_to_robot': False}],
    )

    return LaunchDescription(
        [
            IncludeLaunchDescription(PythonLaunchDescriptionSource(demo_launch)),
            TimerAction(period=8.0, actions=[gripper_bridge]),
        ]
    )
