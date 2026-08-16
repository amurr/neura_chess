from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description() -> LaunchDescription:
    pkg_share = get_package_share_directory('xyz_motion')
    config_default = os.path.join(pkg_share, 'config', 'gripper_bridge.yaml')

    return LaunchDescription(
        [
            DeclareLaunchArgument('params_file', default_value=config_default),
            DeclareLaunchArgument('forward_to_robot', default_value='false'),
            Node(
                package='xyz_motion',
                executable='gripper_joint_bridge',
                name='gripper_joint_bridge',
                output='screen',
                parameters=[
                    LaunchConfiguration('params_file'),
                    {'forward_to_robot': LaunchConfiguration('forward_to_robot')},
                ],
            ),
        ]
    )
