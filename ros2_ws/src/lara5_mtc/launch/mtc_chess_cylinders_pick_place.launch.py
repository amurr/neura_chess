"""Run lara5_mtc_chess_cylinders_pick_place (TF grasp frames + parametrized MTC tree).

Prerequisites (plan / mock):
  ros2 launch lara5_moveit_config mtc_demo.launch.py
    (or mtc_demo_headless.launch.py when no display)
  ros2 launch xyz_motion chess_scene.launch.py use_cylinder_collision:=true planning_scene_only:=true

Prerequisites (Isaac execute):
  scripts/launch/launch_world.sh
  ros2 launch lara5_moveit_config mtc_demo_isaac.launch.py
  ros2 launch xyz_motion chess_scene.launch.py isaac:=true use_cylinder_collision:=true planning_scene_only:=true
  this launch with isaac:=true auto_execute:=true

Optional:
  source:=e2 target:=e4 occupancy_file:=<path> auto_execute:=true keep_alive_s:=0
  hover_mode:=pose approach_frame:=eef isaac:=true
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from moveit_configs_utils import MoveItConfigsBuilder


def _is_true(value: str) -> bool:
    return value.strip().lower() in ('1', 'true', 'yes', 'on')


def _setup(context, *args, **kwargs):
    xyz_share = get_package_share_directory('xyz_motion')
    lara5_mtc_share = get_package_share_directory('lara5_mtc')
    moveit_share = get_package_share_directory('lara5_moveit_config')

    mtc_params = os.path.join(lara5_mtc_share, 'config', 'lara5_mtc_chess_cylinders.yaml')
    lara5_mtc_config = os.path.join(moveit_share, 'config', 'lara5_mtc_config.yaml')
    grasp_tf_params = os.path.join(xyz_share, 'config', 'grasp_tf.yaml')
    cyclone = os.path.join(moveit_share, 'config', 'cyclonedds.localhost.xml')

    moveit_config = (
        MoveItConfigsBuilder('lara5', package_name='lara5_moveit_config')
        .planning_pipelines(pipelines=['ompl'])
        .to_moveit_configs()
    )

    isaac = _is_true(LaunchConfiguration('isaac').perform(context))
    source = LaunchConfiguration('source')
    target = LaunchConfiguration('target')
    occupancy_file = LaunchConfiguration('occupancy_file')
    seed_pose = LaunchConfiguration('seed_pose')
    auto_execute = LaunchConfiguration('auto_execute')
    keep_alive_s = LaunchConfiguration('keep_alive_s')
    hover_mode = LaunchConfiguration('hover_mode')
    approach_frame = LaunchConfiguration('approach_frame')

    if isaac:
        dds = {
            'ROS_DOMAIN_ID': os.environ.get('ROS_DOMAIN_ID', '0'),
            'RMW_IMPLEMENTATION': os.environ.get('RMW_IMPLEMENTATION', 'rmw_fastrtps_cpp'),
            'ROS_LOCALHOST_ONLY': '0',
        }
        env_actions = [SetEnvironmentVariable(k, v) for k, v in dds.items()]
    else:
        dds = {
            'ROS_DOMAIN_ID': os.environ.get('ROS_DOMAIN_ID', '0'),
            'RMW_IMPLEMENTATION': 'rmw_cyclonedds_cpp',
            'ROS_LOCALHOST_ONLY': '1',
            'CYCLONEDDS_URI': f'file://{cyclone}',
        }
        env_actions = [SetEnvironmentVariable(k, v) for k, v in dds.items()]

    return env_actions + [
        SetEnvironmentVariable('CHESS_SOURCE', source),
        SetEnvironmentVariable('CHESS_TARGET', target),
        SetEnvironmentVariable('CHESS_OCCUPANCY_FILE', occupancy_file),
        SetEnvironmentVariable('CHESS_SEED_POSE', seed_pose),
        SetEnvironmentVariable('AUTO_EXECUTE', auto_execute),
        SetEnvironmentVariable('KEEP_ALIVE_S', keep_alive_s),
        Node(
            package='xyz_motion',
            executable='publish_grasp_tf',
            name='publish_grasp_tf',
            output='screen',
            additional_env=dds,
            parameters=[
                grasp_tf_params,
                {'occupancy_file': occupancy_file},
            ],
        ),
        Node(
            package='lara5_mtc',
            executable='lara5_mtc_chess_cylinders_pick_place',
            output='screen',
            additional_env=dds,
            parameters=[
                moveit_config.robot_description,
                moveit_config.robot_description_semantic,
                moveit_config.robot_description_kinematics,
                moveit_config.joint_limits,
                moveit_config.planning_pipelines,
                lara5_mtc_config,
                mtc_params,
                {'auto_execute': ParameterValue(auto_execute, value_type=bool)},
                {'keep_alive_s': ParameterValue(keep_alive_s, value_type=float)},
                {'chess_hover_mode': hover_mode},
                {'chess_approach_frame': approach_frame},
            ],
        ),
    ]


def generate_launch_description():
    xyz_share = get_package_share_directory('xyz_motion')
    default_occ = os.path.join(xyz_share, 'examples', 'e2_to_e4.json')
    return LaunchDescription(
        [
            DeclareLaunchArgument('source', default_value='e2'),
            DeclareLaunchArgument('target', default_value='e4'),
            DeclareLaunchArgument('occupancy_file', default_value=default_occ),
            DeclareLaunchArgument('seed_pose', default_value='pre_pick'),
            DeclareLaunchArgument(
                'isaac',
                default_value='false',
                description='Match isaacsim.ros2.bridge (FastRTPS). Skip Cyclone localhost.',
            ),
            DeclareLaunchArgument(
                'hover_mode',
                default_value='cartesian',
                description='cartesian (XYZ from seed) or pose (MoveTo TF hover orientation)',
            ),
            DeclareLaunchArgument(
                'approach_frame',
                default_value='world',
                description='world (±Z) or eef (tool +Z, into the board)',
            ),
            DeclareLaunchArgument(
                'auto_execute',
                default_value='false',
                description='Execute the planned trajectory via move_group',
            ),
            DeclareLaunchArgument(
                'keep_alive_s',
                default_value='-1',
                description='After plan without auto_execute: -1=until Ctrl+C (RViz), 0=exit (CI)',
            ),
            OpaqueFunction(function=_setup),
        ]
    )
