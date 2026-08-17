"""DDS env that matches isaacsim.ros2.bridge (FastRTPS, domain from ROS_DOMAIN_ID).

Include this instead of localhost_dds_env.launch.py when talking to Isaac.
Do not set ROS_LOCALHOST_ONLY or CycloneDDS — Kit defaults to rmw_fastrtps_cpp.
"""

import os

from launch import LaunchDescription
from launch.actions import SetEnvironmentVariable


def generate_launch_description():
    return LaunchDescription(
        [
            SetEnvironmentVariable(
                'ROS_DOMAIN_ID', os.environ.get('ROS_DOMAIN_ID', '0')
            ),
            SetEnvironmentVariable(
                'RMW_IMPLEMENTATION',
                os.environ.get('RMW_IMPLEMENTATION', 'rmw_fastrtps_cpp'),
            ),
            SetEnvironmentVariable('ROS_LOCALHOST_ONLY', '0'),
        ]
    )
