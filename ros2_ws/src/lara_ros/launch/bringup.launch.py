from launch import LaunchDescription
from launch.actions import TimerAction, GroupAction, SetEnvironmentVariable
from launch_ros.actions import Node
import os

SOCKET_ADDRESS = os.getenv('SOCKET_ADDRESS', '192.168.2.13')

def node_bg(exe, name):
    return Node(
        package='lara_ros',
        executable=exe,
        name=name,
        output='screen',
        emulate_tty=True,
    )

def generate_launch_description():
    # Construct nodes dictionary so we don't reference names that may be commented out
    nodes = {
        'move_joint_service': node_bg('move_joint_service', 'move_joint_service'),
        'move_linear_service': node_bg('move_linear_service', 'move_linear_service'),
        'odom_publisher': node_bg('odom_publisher', 'odom_publisher'),
        'dance_node': node_bg('dance_node', 'dance_node'),
        'music_node': node_bg('music_node', 'music_node'),
        'toast_node': node_bg('toast_node', 'toast_node'),
        'gummy_bear_node': node_bg('gummy_bear_node', 'gummy_bear_node'),
        'gripper_node': node_bg('gripper_node', 'gripper_node'),
    }

    # Only enable the nodes that are safe to run in this environment.
    # Remove or add names in these lists as you enable/disable nodes.
    core_enabled = [
        'move_joint_service',
        'move_linear_service',
        'odom_publisher',
    ]
    apps_enabled = ['dance_node', 'toast_node', 'gummy_bear_node', 'gripper_node']

    ld = LaunchDescription([
        SetEnvironmentVariable('SOCKET_ADDRESS', SOCKET_ADDRESS),
    ])

    if core_enabled:
        core_actions = []
        for name in core_enabled:
            if name in nodes:
                core_actions.append(TimerAction(period=0.5, actions=[nodes[name]]))
        if core_actions:
            ld.add_action(GroupAction(core_actions))

    apps = [nodes[name] for name in apps_enabled if name in nodes]
    if apps:
        ld.add_action(GroupAction(apps))

    return ld
