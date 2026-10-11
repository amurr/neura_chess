"""Broadcast chess grasp / hover TF frames for MTC."""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    pkg_share = get_package_share_directory('xyz_motion')
    default_params = os.path.join(pkg_share, 'config', 'grasp_tf.yaml')

    return LaunchDescription(
        [
            DeclareLaunchArgument('params_file', default_value=default_params),
            DeclareLaunchArgument('occupancy_file', default_value=''),
            DeclareLaunchArgument(
                'z_is_piece_top',
                default_value='false',
                description='true when occupancy/detection z is the piece top',
            ),
            Node(
                package='xyz_motion',
                executable='publish_grasp_tf',
                name='publish_grasp_tf',
                output='screen',
                parameters=[
                    LaunchConfiguration('params_file'),
                    {
                        'occupancy_file': LaunchConfiguration('occupancy_file'),
                        'z_is_piece_top': LaunchConfiguration('z_is_piece_top'),
                    },
                ],
            ),
        ]
    )
