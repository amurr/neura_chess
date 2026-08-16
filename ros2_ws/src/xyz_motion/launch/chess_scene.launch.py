from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def _is_true(value: str) -> bool:
    return value.strip().lower() in ('1', 'true', 'yes', 'on')


def _launch_setup(context, *args, **kwargs):
    pkg_share = get_package_share_directory('xyz_motion')
    params_file_arg = LaunchConfiguration('params_file').perform(context)
    use_cylinders = _is_true(LaunchConfiguration('use_cylinder_collision').perform(context))
    planning_scene_only = _is_true(LaunchConfiguration('planning_scene_only').perform(context))

    if params_file_arg.strip():
        params_path = params_file_arg
    elif use_cylinders and planning_scene_only:
        params_path = os.path.join(pkg_share, 'config', 'chess_scene_cylinders_mtc.yaml')
    elif use_cylinders:
        params_path = os.path.join(pkg_share, 'config', 'chess_scene_cylinders.yaml')
    else:
        params_path = os.path.join(pkg_share, 'config', 'chess_scene.yaml')

    publish_initial_pieces = LaunchConfiguration('publish_initial_pieces')

    return [
        Node(
            package='xyz_motion',
            executable='chess_scene',
            name='chess_scene',
            output='screen',
            parameters=[
                params_path,
                {'publish_initial_pieces': publish_initial_pieces},
            ],
        )
    ]


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription(
        [
            DeclareLaunchArgument(
                'params_file',
                default_value='',
                description='Override params YAML (empty = auto from other args)',
            ),
            DeclareLaunchArgument(
                'use_cylinder_collision',
                default_value='false',
                description='Use cylinder collision primitives (recommended for MTC)',
            ),
            DeclareLaunchArgument(
                'planning_scene_only',
                default_value='false',
                description='No MarkerArray topics; collision via /planning_scene only (MTC/RViz)',
            ),
            DeclareLaunchArgument('publish_initial_pieces', default_value='true'),
            OpaqueFunction(function=_launch_setup),
        ]
    )
