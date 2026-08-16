"""Spawn Lara5 in gz-sim with ros2_control (arm + gripper)."""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description() -> LaunchDescription:
    pkg_gazebo = get_package_share_directory('lara5_gazebo')
    pkg_moveit = get_package_share_directory('lara5_moveit_config')
    world_path = os.path.join(pkg_gazebo, 'worlds', 'empty.sdf')
    controllers_file = os.path.join(pkg_moveit, 'config', 'ros2_controllers.yaml')
    robot_xacro = os.path.join(pkg_gazebo, 'urdf', 'lara5_gz.urdf.xacro')

    robot_description = Command(['xacro ', robot_xacro])

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([FindPackageShare('ros_gz_sim'), 'launch', 'gz_sim.launch.py'])
        ),
        launch_arguments={'gz_args': f'-r {world_path}'}.items(),
    )

    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description}],
    )

    spawn = Node(
        package='ros_gz_sim',
        executable='create',
        output='screen',
        arguments=['-topic', 'robot_description', '-name', 'lara5', '-z', '0.0'],
    )

    controller_manager = Node(
        package='controller_manager',
        executable='ros2_control_node',
        parameters=[{'robot_description': robot_description}, controllers_file],
        output='screen',
    )

    joint_state_broadcaster = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster', '--controller-manager', '/controller_manager'],
    )
    arm_controller = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['arm_controller', '--controller-manager', '/controller_manager'],
    )
    gripper_controller = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['gripper_controller', '--controller-manager', '/controller_manager'],
    )

    gripper_bridge = Node(
        package='xyz_motion',
        executable='gripper_joint_bridge',
        name='gripper_joint_bridge',
        parameters=[
            os.path.join(get_package_share_directory('xyz_motion'), 'config', 'gripper_bridge.yaml'),
            {'forward_to_robot': False},
        ],
    )

    delay_arm = RegisterEventHandler(
        OnProcessExit(
            target_action=joint_state_broadcaster,
            on_exit=[arm_controller, gripper_controller, gripper_bridge],
        )
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument('world', default_value=world_path),
            gz_sim,
            rsp,
            controller_manager,
            spawn,
            joint_state_broadcaster,
            delay_arm,
        ]
    )
