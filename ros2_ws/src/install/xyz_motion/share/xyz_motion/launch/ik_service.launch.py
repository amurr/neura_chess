from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description() -> LaunchDescription:
    config_default = os.path.join(
        get_package_share_directory('xyz_motion'),
        'config',
        'ik_service.yaml',
    )

    params_file = LaunchConfiguration('params_file')
    urdf_path = LaunchConfiguration('urdf_path')
    base_link = LaunchConfiguration('base_link')
    tip_link = LaunchConfiguration('tip_link')
    service_name = LaunchConfiguration('service_name')

    return LaunchDescription(
        [
            DeclareLaunchArgument('params_file', default_value=config_default),
            DeclareLaunchArgument('urdf_path', default_value=''),
            DeclareLaunchArgument('base_link', default_value='lara5_link0'),
            DeclareLaunchArgument('tip_link', default_value='lara5_gripper'),
            DeclareLaunchArgument('service_name', default_value='compute_ik'),
            Node(
                package='xyz_motion',
                executable='ik_service',
                name='ik_service',
                output='screen',
                parameters=[
                    params_file,
                    {
                        'urdf_path': urdf_path,
                        'base_link': base_link,
                        'tip_link': tip_link,
                        'service_name': service_name,
                    },
                ],
            ),
        ]
    )
