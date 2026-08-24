"""MoveIt + ros2_control driving the Lara5 in Isaac Sim.

Hardware is topic_based_ros2_control (not mock). JointTrajectoryController /
GripperActionController are unchanged; they write JointState positions to
/isaac_hw_joint_commands. pad_joint_commands fills velocity/effort (NaN) so
Isaac ROS2SubscribeJointState accepts the message on /isaac_joint_commands.

Prerequisites:
  scripts/launch/launch_world.sh   # timeline playing, bridge subscribed
  Same ROS_DOMAIN_ID and RMW as Kit (default domain 0, rmw_fastrtps_cpp).

Then:
  ros2 launch lara5_moveit_config mtc_demo_isaac.launch.py
  ros2 launch xyz_motion chess_scene.launch.py isaac:=true \\
      use_cylinder_collision:=true planning_scene_only:=true
  ros2 launch lara5_mtc mtc_chess_cylinders_pick_place.launch.py isaac:=true \\
      auto_execute:=true
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    SetEnvironmentVariable,
    TimerAction,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from moveit_configs_utils import MoveItConfigsBuilder


def _dds_env() -> dict:
    return {
        'ROS_DOMAIN_ID': os.environ.get('ROS_DOMAIN_ID', '0'),
        'RMW_IMPLEMENTATION': os.environ.get('RMW_IMPLEMENTATION', 'rmw_fastrtps_cpp'),
        'ROS_LOCALHOST_ONLY': '0',
    }


def _spawner(controller: str, dds_env: dict) -> Node:
    return Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            controller,
            '--controller-manager',
            '/controller_manager',
            '--controller-manager-timeout',
            '60',
        ],
        output='screen',
        additional_env=dds_env,
    )


def generate_launch_description():
    dds_env = _dds_env()
    pkg_share = get_package_share_directory('lara5_moveit_config')

    moveit_config = (
        MoveItConfigsBuilder('lara5', package_name='lara5_moveit_config')
        .robot_description(
            file_path='config/lara5.urdf.xacro',
            mappings={
                'ros2_control_name': 'IsaacTopicSystem',
                'ros2_control_hardware_plugin': 'topic_based_ros2_control/TopicBasedSystem',
                'use_topic_hw': 'true',
                'joint_commands_topic': '/isaac_hw_joint_commands',
                'joint_states_topic': '/isaac_joint_states',
            },
        )
        .planning_pipelines(pipelines=['ompl'])
        .to_moveit_configs()
    )

    use_sim_time = LaunchConfiguration('use_sim_time')
    sim_time_param = {'use_sim_time': ParameterValue(use_sim_time, value_type=bool)}

    move_group_node = Node(
        package='moveit_ros_move_group',
        executable='move_group',
        output='screen',
        additional_env=dds_env,
        parameters=[
            moveit_config.to_dict(),
            {'capabilities': 'move_group/ExecuteTaskSolutionCapability'},
            sim_time_param,
        ],
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='both',
        additional_env=dds_env,
        parameters=[moveit_config.robot_description, sim_time_param],
    )

    ros2_control_node = Node(
        package='controller_manager',
        executable='ros2_control_node',
        additional_env=dds_env,
        parameters=[
            moveit_config.robot_description,
            os.path.join(pkg_share, 'config', 'ros2_controllers.yaml'),
            sim_time_param,
        ],
        remappings=[('/joint_states', '/joint_states_ros2_control')],
        output='both',
    )

    pad_joint_commands = Node(
        package='lara5_moveit',
        executable='pad_joint_commands',
        name='isaac_joint_command_pad',
        output='screen',
        additional_env=dds_env,
        parameters=[
            {'in_topic': '/isaac_hw_joint_commands'},
            {'out_topic': '/isaac_joint_commands'},
        ],
    )

    # MoveIt CurrentStateMonitor is BEST_EFFORT + wall clock. Isaac stamps sim
    # time; joint_state_broadcaster is RELIABLE/TRANSIENT_LOCAL and often idle.
    relay_isaac_joint_states = Node(
        package='lara5_moveit',
        executable='relay_isaac_joint_states',
        name='isaac_joint_state_relay',
        output='screen',
        additional_env=dds_env,
        parameters=[
            {'in_topic': '/isaac_joint_states'},
            {'out_topic': '/joint_states'},
        ],
    )

    sanitize_follow_joint_trajectory = Node(
        package='lara5_moveit',
        executable='sanitize_follow_joint_trajectory',
        name='sanitize_follow_joint_trajectory',
        output='screen',
        additional_env=dds_env,
        parameters=[
            {'in_action': '/arm_controller/follow_joint_trajectory_safe'},
            {'out_action': '/arm_controller/follow_joint_trajectory'},
        ],
    )

    static_virtual_joint_tfs = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_share, 'launch', 'static_virtual_joint_tfs.launch.py')
        ),
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                'use_sim_time',
                default_value='false',
                description='Follow Isaac /clock (only if the bridge clock is received)',
            ),
            SetEnvironmentVariable('ROS_DOMAIN_ID', dds_env['ROS_DOMAIN_ID']),
            SetEnvironmentVariable('RMW_IMPLEMENTATION', dds_env['RMW_IMPLEMENTATION']),
            SetEnvironmentVariable('ROS_LOCALHOST_ONLY', '0'),
            robot_state_publisher,
            static_virtual_joint_tfs,
            ros2_control_node,
            pad_joint_commands,
            relay_isaac_joint_states,
            sanitize_follow_joint_trajectory,
            move_group_node,
            TimerAction(period=3.0, actions=[_spawner('joint_state_broadcaster', dds_env)]),
            TimerAction(
                period=5.0,
                actions=[
                    _spawner('arm_controller', dds_env),
                    _spawner('gripper_controller', dds_env),
                ],
            ),
            TimerAction(
                period=7.0,
                actions=[
                    Node(
                        package='lara5_moveit',
                        executable='activate_controllers',
                        name='activate_controllers',
                        output='screen',
                        additional_env=dds_env,
                        parameters=[{'timeout_s': 60.0}],
                    )
                ],
            ),
        ]
    )
