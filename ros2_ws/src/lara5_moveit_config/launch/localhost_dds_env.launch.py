"""Set CycloneDDS localhost env (include first in multi-node launches)."""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import SetEnvironmentVariable


def generate_launch_description():
    cyclone = os.path.join(
        get_package_share_directory('lara5_moveit_config'),
        'config',
        'cyclonedds.localhost.xml',
    )
    return LaunchDescription(
        [
            SetEnvironmentVariable('ROS_DOMAIN_ID', '0'),
            SetEnvironmentVariable('RMW_IMPLEMENTATION', 'rmw_cyclonedds_cpp'),
            SetEnvironmentVariable('ROS_LOCALHOST_ONLY', '1'),
            SetEnvironmentVariable('CYCLONEDDS_URI', f'file://{cyclone}'),
        ]
    )
