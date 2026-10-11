from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def _is_true(value: str) -> bool:
    return value.strip().lower() in ('1', 'true', 'yes', 'on')


def _cyclone_env():
    try:
        moveit_share = get_package_share_directory('lara5_moveit_config')
    except Exception:
        return []
    cyclone = os.path.join(moveit_share, 'config', 'cyclonedds.localhost.xml')
    if not os.path.isfile(cyclone):
        return []
    return [
        SetEnvironmentVariable('ROS_DOMAIN_ID', os.environ.get('ROS_DOMAIN_ID', '0')),
        SetEnvironmentVariable('RMW_IMPLEMENTATION', 'rmw_cyclonedds_cpp'),
        SetEnvironmentVariable('ROS_LOCALHOST_ONLY', '1'),
        SetEnvironmentVariable('CYCLONEDDS_URI', f'file://{cyclone}'),
    ]


def _isaac_dds():
    return {
        'RMW_IMPLEMENTATION': os.environ.get('RMW_IMPLEMENTATION', 'rmw_fastrtps_cpp'),
        'ROS_LOCALHOST_ONLY': '0',
        'ROS_DOMAIN_ID': os.environ.get('ROS_DOMAIN_ID', '0'),
    }


def _cyclone_dds():
    env = {
        'RMW_IMPLEMENTATION': os.environ.get('RMW_IMPLEMENTATION', 'rmw_cyclonedds_cpp'),
        'ROS_LOCALHOST_ONLY': os.environ.get('ROS_LOCALHOST_ONLY', '1'),
        'ROS_DOMAIN_ID': os.environ.get('ROS_DOMAIN_ID', '0'),
    }
    if os.environ.get('CYCLONEDDS_URI'):
        env['CYCLONEDDS_URI'] = os.environ['CYCLONEDDS_URI']
    return env


def _launch_setup(context, *args, **kwargs):
    pkg_share = get_package_share_directory('xyz_motion')
    params_file_arg = LaunchConfiguration('params_file').perform(context)
    use_cylinders = _is_true(LaunchConfiguration('use_cylinder_collision').perform(context))
    planning_scene_only = _is_true(LaunchConfiguration('planning_scene_only').perform(context))
    isaac = _is_true(LaunchConfiguration('isaac').perform(context))

    if params_file_arg.strip():
        params_path = params_file_arg
    elif use_cylinders and planning_scene_only:
        params_path = os.path.join(pkg_share, 'config', 'chess_scene_cylinders_mtc.yaml')
    elif use_cylinders:
        params_path = os.path.join(pkg_share, 'config', 'chess_scene_cylinders.yaml')
    else:
        params_path = os.path.join(pkg_share, 'config', 'chess_scene.yaml')

    if isaac:
        dds = _isaac_dds()
        env_actions = [SetEnvironmentVariable(k, v) for k, v in dds.items()]
    else:
        dds = _cyclone_dds()
        env_actions = _cyclone_env()

    publish_initial_pieces = LaunchConfiguration('publish_initial_pieces')
    return env_actions + [
        Node(
            package='xyz_motion',
            executable='chess_scene',
            name='chess_scene',
            output='screen',
            additional_env=dds,
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
                'isaac',
                default_value='false',
                description='Match isaacsim.ros2.bridge (FastRTPS). Skip Cyclone localhost.',
            ),
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
