"""Lara5 MTC demo without RViz: mock ros2_control, move_group + MTC capability."""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder


def _dds_env(cyclonedds_config: str) -> dict:
    return {
        'ROS_DOMAIN_ID': os.environ.get('ROS_DOMAIN_ID', '0'),
        'RMW_IMPLEMENTATION': 'rmw_cyclonedds_cpp',
        'ROS_LOCALHOST_ONLY': '1',
        'CYCLONEDDS_URI': f'file://{cyclonedds_config}',
    }


def _spawner(controller: str, dds_env: dict) -> Node:
    return Node(
        package='controller_manager',
        executable='spawner',
        arguments=[controller, '--controller-manager', '/controller_manager'],
        output='screen',
        additional_env=dds_env,
    )


def generate_launch_description():
    moveit_config = (
        MoveItConfigsBuilder('lara5', package_name='lara5_moveit_config')
        .planning_pipelines(pipelines=['ompl'])
        .to_moveit_configs()
    )

    move_group_capabilities = {
        'capabilities': 'move_group/ExecuteTaskSolutionCapability',
    }

    pkg_share = get_package_share_directory('lara5_moveit_config')
    cyclonedds_config = os.path.join(pkg_share, 'config', 'cyclonedds.localhost.xml')
    dds_env = _dds_env(cyclonedds_config)

    move_group_node = Node(
        package='moveit_ros_move_group',
        executable='move_group',
        output='screen',
        additional_env=dds_env,
        parameters=[
            moveit_config.to_dict(),
            move_group_capabilities,
        ],
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='both',
        additional_env=dds_env,
        parameters=[moveit_config.robot_description],
    )

    ros2_controllers_path = os.path.join(pkg_share, 'config', 'ros2_controllers.yaml')

    ros2_control_node = Node(
        package='controller_manager',
        executable='ros2_control_node',
        additional_env=dds_env,
        parameters=[moveit_config.robot_description, ros2_controllers_path],
        output='both',
    )

    static_virtual_joint_tfs = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_share, 'launch', 'static_virtual_joint_tfs.launch.py')
        ),
    )

    return LaunchDescription(
        [
            SetEnvironmentVariable('ROS_DOMAIN_ID', dds_env['ROS_DOMAIN_ID']),
            SetEnvironmentVariable('RMW_IMPLEMENTATION', dds_env['RMW_IMPLEMENTATION']),
            SetEnvironmentVariable('ROS_LOCALHOST_ONLY', '1'),
            SetEnvironmentVariable('CYCLONEDDS_URI', dds_env['CYCLONEDDS_URI']),
            robot_state_publisher,
            static_virtual_joint_tfs,
            ros2_control_node,
            move_group_node,
            TimerAction(period=2.0, actions=[_spawner('joint_state_broadcaster', dds_env)]),
            TimerAction(
                period=3.0,
                actions=[
                    _spawner('arm_controller', dds_env),
                    _spawner('gripper_controller', dds_env),
                ],
            ),
        ]
    )
