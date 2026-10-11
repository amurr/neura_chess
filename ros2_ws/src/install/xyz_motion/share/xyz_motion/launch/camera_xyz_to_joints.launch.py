from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description() -> LaunchDescription:
    config_default = os.path.join(
        get_package_share_directory('xyz_motion'),
        'config',
        'camera_xyz_to_joints.yaml',
    )

    params_file = LaunchConfiguration('params_file')
    assume_base_frame = LaunchConfiguration('assume_base_frame')
    publish_test_static_tf = LaunchConfiguration('publish_test_static_tf')

    return LaunchDescription(
        [
            DeclareLaunchArgument('params_file', default_value=config_default),
            DeclareLaunchArgument('assume_base_frame', default_value='false'),
            DeclareLaunchArgument('publish_test_static_tf', default_value='false'),
            Node(
                package='tf2_ros',
                executable='static_transform_publisher',
                name='camera_to_base_static_tf',
                output='screen',
                condition=IfCondition(publish_test_static_tf),
                arguments=[
                    '--x', '0.0',
                    '--y', '0.0',
                    '--z', '0.0',
                    '--roll', '0.0',
                    '--pitch', '0.0',
                    '--yaw', '0.0',
                    '--frame-id', 'lara5_link0',
                    '--child-frame-id', 'camera_optical_frame',
                ],
            ),
            Node(
                package='xyz_motion',
                executable='camera_xyz_to_joints',
                name='camera_xyz_to_joints',
                output='screen',
                parameters=[
                    params_file,
                    {'assume_base_frame': assume_base_frame},
                ],
            ),
        ]
    )
