"""Lara5 MTC demo with RViz — primary dev workflow (WSLg / local GUI)."""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder


def _spawner(controller: str) -> Node:
    return Node(
        package='controller_manager',
        executable='spawner',
        arguments=[controller, '--controller-manager', '/controller_manager'],
        output='screen',
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

    move_group_node = Node(
        package='moveit_ros_move_group',
        executable='move_group',
        output='screen',
        parameters=[
            moveit_config.to_dict(),
            move_group_capabilities,
        ],
    )

    pkg_share = get_package_share_directory('lara5_moveit_config')
    rviz_config = os.path.join(pkg_share, 'config', 'mtc.rviz')
    cyclonedds_config = os.path.join(pkg_share, 'config', 'cyclonedds.localhost.xml')

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        output='screen',
        arguments=['-d', rviz_config],
        parameters=[moveit_config.to_dict()],
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='both',
        parameters=[moveit_config.robot_description],
    )

    ros2_controllers_path = os.path.join(pkg_share, 'config', 'ros2_controllers.yaml')

    ros2_control_node = Node(
        package='controller_manager',
        executable='ros2_control_node',
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
            SetEnvironmentVariable('ROS_DOMAIN_ID', '0'),
            SetEnvironmentVariable('RMW_IMPLEMENTATION', 'rmw_cyclonedds_cpp'),
            SetEnvironmentVariable('ROS_LOCALHOST_ONLY', '1'),
            SetEnvironmentVariable('CYCLONEDDS_URI', f'file://{cyclonedds_config}'),
            SetEnvironmentVariable('QT_QPA_PLATFORM', 'xcb'),
            SetEnvironmentVariable('OGRE_RTT_MODE', 'Copy'),
            robot_state_publisher,
            static_virtual_joint_tfs,
            ros2_control_node,
            move_group_node,
            # joint_state_broadcaster must be active before RViz — it publishes /joint_states
            # so robot_state_publisher can broadcast the arm chain to camera_optical_frame.
            TimerAction(period=2.0, actions=[_spawner('joint_state_broadcaster')]),
            TimerAction(
                period=3.0,
                actions=[
                    _spawner('arm_controller'),
                    _spawner('gripper_controller'),
                ],
            ),
            TimerAction(period=8.0, actions=[rviz_node]),
        ]
    )
