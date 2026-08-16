"""Run an moveit_task_constructor_demo executable against the Lara5 MoveIt config."""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder


def generate_launch_description():
    moveit_config = (
        MoveItConfigsBuilder('lara5', package_name='lara5_moveit_config')
        .planning_pipelines(pipelines=['ompl'])
        .to_moveit_configs()
    )

    pkg_share = get_package_share_directory('lara5_moveit_config')
    lara5_mtc_config = os.path.join(pkg_share, 'config', 'lara5_mtc_config.yaml')

    demo_node = Node(
        package=LaunchConfiguration('package'),
        executable=LaunchConfiguration('exe'),
        output='screen',
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.robot_description_kinematics,
            moveit_config.joint_limits,
            moveit_config.planning_pipelines,
            lara5_mtc_config,
        ],
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                name='package',
                default_value='moveit_task_constructor_demo',
                description='Package providing the MTC demo script',
            ),
            DeclareLaunchArgument(
                name='exe',
                default_value='current_state.py',
                description='Demo script (e.g. current_state.py or lara5_cartesian.py)',
            ),
            demo_node,
        ]
    )
