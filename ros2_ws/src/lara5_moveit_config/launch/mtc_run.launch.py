"""Run an MTC executable against the Lara5 MoveIt config.

Loads robot_description / SRDF onto the node. ``ros2 run`` cannot do that.

Chess pick (Isaac poses):
  ros2 launch lara5_moveit_config mtc_run.launch.py \\
    package:=lara5_moveit exe:=moveit_chess square:=d2 to:=d3
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder


def _dds_env() -> dict:
    return {
        'ROS_DOMAIN_ID': os.environ.get('ROS_DOMAIN_ID', '0'),
        'RMW_IMPLEMENTATION': os.environ.get('RMW_IMPLEMENTATION', 'rmw_fastrtps_cpp'),
        'ROS_LOCALHOST_ONLY': '0',
    }


def _truthy(value: str) -> bool:
    return value.strip().lower() in ('1', 'true', 'yes')


def _demo_node(context, *args, **kwargs):
    moveit_config = (
        MoveItConfigsBuilder('lara5', package_name='lara5_moveit_config')
        .planning_pipelines(pipelines=['ompl'])
        .to_moveit_configs()
    )
    pkg_share = get_package_share_directory('lara5_moveit_config')
    lara5_mtc_config = os.path.join(pkg_share, 'config', 'lara5_mtc_config.yaml')

    extra = []
    square = LaunchConfiguration('square').perform(context)
    dest = LaunchConfiguration('to').perform(context)
    if square:
        extra += ['--square', square]
    if dest:
        extra += ['--to', dest]
    if _truthy(LaunchConfiguration('plan_only').perform(context)):
        extra.append('--plan-only')
    if _truthy(LaunchConfiguration('print_only').perform(context)):
        extra.append('--print-only')
    if _truthy(LaunchConfiguration('list').perform(context)):
        extra.append('--list')

    return [
        Node(
            package=LaunchConfiguration('package'),
            executable=LaunchConfiguration('exe'),
            output='screen',
            additional_env=_dds_env(),
            arguments=extra,
            parameters=[
                moveit_config.robot_description,
                moveit_config.robot_description_semantic,
                moveit_config.robot_description_kinematics,
                moveit_config.joint_limits,
                moveit_config.planning_pipelines,
                lara5_mtc_config,
            ],
        )
    ]


def generate_launch_description():
    dds = _dds_env()
    return LaunchDescription(
        [
            SetEnvironmentVariable('ROS_DOMAIN_ID', dds['ROS_DOMAIN_ID']),
            SetEnvironmentVariable('RMW_IMPLEMENTATION', dds['RMW_IMPLEMENTATION']),
            SetEnvironmentVariable('ROS_LOCALHOST_ONLY', '0'),
            DeclareLaunchArgument(
                name='package',
                default_value='moveit_task_constructor_demo',
                description='Package providing the MTC demo script',
            ),
            DeclareLaunchArgument(
                name='exe',
                default_value='current_state.py',
                description='Demo script (e.g. current_state.py or moveit_chess)',
            ),
            DeclareLaunchArgument(
                name='square',
                default_value='',
                description='Pick square for moveit_chess (e.g. d2)',
            ),
            DeclareLaunchArgument(
                name='to',
                default_value='',
                description='Place square for moveit_chess (e.g. d3)',
            ),
            DeclareLaunchArgument(
                name='plan_only',
                default_value='false',
                description='Plan moveit_chess but do not execute',
            ),
            DeclareLaunchArgument(
                name='print_only',
                default_value='false',
                description='Print grasp targets and exit',
            ),
            DeclareLaunchArgument(
                name='list',
                default_value='false',
                description='List Isaac piece poses and exit',
            ),
            OpaqueFunction(function=_demo_node),
        ]
    )
