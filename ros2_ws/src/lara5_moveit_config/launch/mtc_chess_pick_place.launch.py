"""Run lara5_chess_mtc_pick_place.py (Pick/Place on planning-scene piece).

Prerequisites (separate terminals):
  ros2 launch lara5_moveit_config mtc_demo.launch.py
  ros2 launch xyz_motion chess_scene.launch.py

Optional env before launch:
  CHESS_SOURCE=e2  CHESS_TARGET=e4
  CHESS_OCCUPANCY_FILE=<path to e2_to_e4.json or standard_start.json>
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder


def generate_launch_description():
    xyz_share = get_package_share_directory('xyz_motion')
    default_occ = os.path.join(xyz_share, 'examples', 'e2_to_e4.json')

    moveit_config = (
        MoveItConfigsBuilder('lara5', package_name='lara5_moveit_config')
        .planning_pipelines(pipelines=['ompl'])
        .to_moveit_configs()
    )

    pkg_share = get_package_share_directory('lara5_moveit_config')
    lara5_mtc_config = os.path.join(pkg_share, 'config', 'lara5_mtc_config.yaml')

    source = LaunchConfiguration('source')
    target = LaunchConfiguration('target')
    occupancy_file = LaunchConfiguration('occupancy_file')

    return LaunchDescription(
        [
            DeclareLaunchArgument('source', default_value='e2'),
            DeclareLaunchArgument('target', default_value='e4'),
            DeclareLaunchArgument('occupancy_file', default_value=default_occ),
            SetEnvironmentVariable('CHESS_SOURCE', source),
            SetEnvironmentVariable('CHESS_TARGET', target),
            SetEnvironmentVariable('CHESS_OCCUPANCY_FILE', occupancy_file),
            Node(
                package='lara5_moveit_config',
                executable='lara5_chess_mtc_pick_place.py',
                output='screen',
                parameters=[
                    moveit_config.robot_description,
                    moveit_config.robot_description_semantic,
                    moveit_config.robot_description_kinematics,
                    moveit_config.joint_limits,
                    moveit_config.planning_pipelines,
                    lara5_mtc_config,
                ],
            ),
        ]
    )
