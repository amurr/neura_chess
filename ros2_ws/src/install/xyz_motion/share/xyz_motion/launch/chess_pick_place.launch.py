"""Chess planning scene node (start move_group and chess_move separately)."""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description() -> LaunchDescription:
    pkg_share = get_package_share_directory('xyz_motion')
    scene_launch = os.path.join(pkg_share, 'launch', 'chess_scene.launch.py')

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                'scene_params_file',
                default_value=os.path.join(pkg_share, 'config', 'chess_scene.yaml'),
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(scene_launch),
                launch_arguments={'params_file': LaunchConfiguration('scene_params_file')}.items(),
            ),
        ]
    )
