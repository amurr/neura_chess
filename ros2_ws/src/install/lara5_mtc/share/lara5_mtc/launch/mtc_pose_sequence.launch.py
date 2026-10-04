from launch import LaunchDescription
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder


def generate_launch_description():
    moveit_config = (
        MoveItConfigsBuilder("lara5", package_name="lara5_moveit_config")
        .to_moveit_configs()
    )

    mtc_node = Node(
        package="lara5_mtc",
        executable="mtc_pose_sequence",
        output="screen",
        parameters=[
            moveit_config.to_dict(),
        ],
    )

    return LaunchDescription([mtc_node])