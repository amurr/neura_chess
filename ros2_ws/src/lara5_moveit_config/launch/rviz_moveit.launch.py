"""Lara5 + MoveIt + RViz + chess board. No hardware.

  source /opt/ros/humble/setup.bash
  source /ros2_ws/neura_chess/install/setup.bash
  ros2 launch lara5_moveit_config rviz_moveit.launch.py
  ros2 launch lara5_moveit_config rviz_moveit.launch.py board:=big

fake_controllers:=true (default) serves the actions in moveit_controllers.yaml with
lara5_moveit/fake_controllers, so Execute and MTC task.execute() move the model.
fake_controllers:=false gives joint_state_publisher_gui sliders instead; nothing
executes then. The two cannot run together, both publish /joint_states.
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    SetEnvironmentVariable,
)
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder


def generate_launch_description():
    moveit_config = (
        MoveItConfigsBuilder('lara5', package_name='lara5_moveit_config')
        .planning_pipelines(pipelines=['ompl'])
        .to_moveit_configs()
    )

    # Humble's MoveItConfigs.to_dict() does not include capabilities, so pass
    # this extra dict to move_group. Needed for MTC task.execute()
    # (/execute_task_solution). Appended to the default capability set.
    move_group_capabilities = {
        'capabilities': 'move_group/ExecuteTaskSolutionCapability',
    }

    pkg_share = get_package_share_directory('lara5_moveit_config')
    moveit_share = get_package_share_directory('lara5_moveit')
    rviz_config = os.path.join(pkg_share, 'config', 'orient.rviz')
    chess_params = os.path.join(moveit_share, 'config', 'chess_scene.yaml')
    board = LaunchConfiguration('board')

    rmw = os.environ.get('RMW_IMPLEMENTATION', 'rmw_fastrtps_cpp')
    domain = os.environ.get('ROS_DOMAIN_ID', '0')

    robot_description = moveit_config.robot_description

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[robot_description],
    )

    use_fake_controllers = LaunchConfiguration('fake_controllers')

    joint_state_publisher_gui = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        output='screen',
        parameters=[robot_description],
        condition=UnlessCondition(use_fake_controllers),
    )

    fake_controllers = Node(
        package='lara5_moveit',
        executable='fake_controllers',
        name='fake_controllers',
        output='screen',
        respawn=True,
        respawn_delay=1.0,
        condition=IfCondition(use_fake_controllers),
    )

    static_virtual_joint_tfs = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_share, 'launch', 'static_virtual_joint_tfs.launch.py')
        ),
    )

    move_group = Node(
        package='moveit_ros_move_group',
        executable='move_group',
        output='screen',
        parameters=[
            moveit_config.to_dict(),
            move_group_capabilities,
        ],
    )

    chess_scene_small = Node(
        package='lara5_moveit',
        executable='chess_scene_collisions',
        name='chess_scene_collisions',
        output='screen',
        parameters=[chess_params],
        respawn=True,
        respawn_delay=1.0,
        condition=IfCondition(PythonExpression(["'", board, "' == 'small'"])),
    )

    # Max perpendicular-reachable 8x8 (7.2 cm squares, 57.6 cm board). Do not pass
    # chess_scene.yaml: it would overwrite square_size / a1 with the small-board values.
    chess_scene_big = Node(
        package='lara5_moveit',
        executable='chess_scene_big',
        name='chess_scene_collisions',
        output='screen',
        respawn=True,
        respawn_delay=1.0,
        condition=IfCondition(PythonExpression(["'", board, "' == 'big'"])),
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        output='screen',
        arguments=['-d', rviz_config],
        parameters=[moveit_config.to_dict()],
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                'board',
                default_value='small',
                description="Chess scene: 'small' (4 cm squares) or 'big' (7.2 cm, max reach).",
            ),
            DeclareLaunchArgument(
                'fake_controllers',
                default_value='true',
                description='Serve MoveIt controller actions with lara5_moveit/fake_controllers '
                'instead of joint_state_publisher_gui sliders.',
            ),
            SetEnvironmentVariable('RMW_IMPLEMENTATION', rmw),
            SetEnvironmentVariable('ROS_DOMAIN_ID', domain),
            SetEnvironmentVariable('ROS_LOCALHOST_ONLY', '1'),
            SetEnvironmentVariable('QT_QPA_PLATFORM', 'xcb'),
            robot_state_publisher,
            static_virtual_joint_tfs,
            joint_state_publisher_gui,
            fake_controllers,
            move_group,
            chess_scene_small,
            chess_scene_big,
            rviz,
        ]
    )
