"""Run lara5_mtc_chess_cylinders_pick_place (flat MTC tree, cylinder scene).

Prerequisites:
  ros2 launch lara5_moveit_config mtc_demo.launch.py
    (or mtc_demo_headless.launch.py when no display)
  ros2 launch xyz_motion chess_scene.launch.py use_cylinder_collision:=true planning_scene_only:=true

Optional:
  source:=e2 target:=e4 occupancy_file:=<path> auto_execute:=true keep_alive_s:=0
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from moveit_configs_utils import MoveItConfigsBuilder


def generate_launch_description():
    xyz_share = get_package_share_directory('xyz_motion')
    lara5_mtc_share = get_package_share_directory('lara5_mtc')
    moveit_share = get_package_share_directory('lara5_moveit_config')

    default_occ = os.path.join(xyz_share, 'examples', 'e2_to_e4.json')
    mtc_params = os.path.join(lara5_mtc_share, 'config', 'lara5_mtc_chess_cylinders.yaml')
    lara5_mtc_config = os.path.join(moveit_share, 'config', 'lara5_mtc_config.yaml')

    moveit_config = (
        MoveItConfigsBuilder('lara5', package_name='lara5_moveit_config')
        .planning_pipelines(pipelines=['ompl'])
        .to_moveit_configs()
    )

    source = LaunchConfiguration('source')
    target = LaunchConfiguration('target')
    occupancy_file = LaunchConfiguration('occupancy_file')
    seed_pose = LaunchConfiguration('seed_pose')
    auto_execute = LaunchConfiguration('auto_execute')
    keep_alive_s = LaunchConfiguration('keep_alive_s')

    top_down_roll = LaunchConfiguration('chess_top_down_roll')
    top_down_pitch = LaunchConfiguration('chess_top_down_pitch')
    top_down_yaw = LaunchConfiguration('chess_top_down_yaw')

    return LaunchDescription(
        [
            DeclareLaunchArgument('source', default_value='e2'),
            DeclareLaunchArgument('target', default_value='e4'),
            DeclareLaunchArgument('occupancy_file', default_value=default_occ),
            DeclareLaunchArgument('seed_pose', default_value='pre_pick'),
            DeclareLaunchArgument('chess_top_down_roll', default_value='0.0'),
            DeclareLaunchArgument('chess_top_down_pitch', default_value='1.5707963267948966'),
            DeclareLaunchArgument('chess_top_down_yaw', default_value='0.0'),
            DeclareLaunchArgument(
                'auto_execute',
                default_value='false',
                description='Execute the planned trajectory via move_group (watch in RViz)',
            ),
            DeclareLaunchArgument(
                'keep_alive_s',
                default_value='-1',
                description='After plan without auto_execute: -1=until Ctrl+C (RViz), 0=exit (CI)',
            ),
            SetEnvironmentVariable('CHESS_SOURCE', source),
            SetEnvironmentVariable('CHESS_TARGET', target),
            SetEnvironmentVariable('CHESS_OCCUPANCY_FILE', occupancy_file),
            SetEnvironmentVariable('CHESS_SEED_POSE', seed_pose),
            SetEnvironmentVariable('AUTO_EXECUTE', auto_execute),
            SetEnvironmentVariable('KEEP_ALIVE_S', keep_alive_s),
            Node(
                package='lara5_mtc',
                executable='lara5_mtc_chess_cylinders_pick_place',
                output='screen',
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
                    {'chess_top_down_roll': ParameterValue(top_down_roll, value_type=float)},
                    {'chess_top_down_pitch': ParameterValue(top_down_pitch, value_type=float)},
                    {'chess_top_down_yaw': ParameterValue(top_down_yaw, value_type=float)},
                ],
            ),
        ]
    )
