"""MTC pose sequence: mid_move -> hover -> open gripper -> down -> close gripper -> up.

  ros2 launch lara5_mtc mtc_pose_sequence.launch.py
  ros2 launch lara5_mtc mtc_pose_sequence.launch.py hover_pose:=e4
  ros2 launch lara5_mtc mtc_pose_sequence.launch.py hover_pose:=e4_hover
  ros2 launch lara5_mtc mtc_pose_sequence.launch.py lower_distance:=0.03 lift_distance:=0.08
  ros2 launch lara5_mtc mtc_pose_sequence.launch.py gripper_close_position:=0.2
  ros2 launch lara5_mtc mtc_pose_sequence.launch.py gripper_open_position:=0.25

hover_pose is an SRDF arm state (a1_hover … h8_hover) or a square (e4 → e4_hover).
Distances are in metres. Gripper angles are jaw joint radians (URDF allows -0.174533 shut
to 1.74533 wide open). Changing any of them needs no rebuild.

gripper rad to cm openness (inner-pad gap from the SO-101 meshes):
  rad      deg    open cm
  -0.175   -10    0.3     SRDF close / URDF lower
   0.0       0    1.6
   0.2      11    3.3
   0.4      23    4.9
   0.6      34    6.4
   0.8      46    7.8
   0.9      52    8.4
   1.0      57    8.9
   1.2      69    9.9
   1.4      80   10.5
   1.745   100   10.9     URDF open
  Up to ~0.6 rad: open_cm ≈ 0.3 + 8.0 * (q + 0.175). Pawn is 1.8 cm across.
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder


def launch_setup(context, *args, **kwargs):
    moveit_config = (
        MoveItConfigsBuilder("lara5", package_name="lara5_moveit_config")
        .to_moveit_configs()
    )

    def arg(name):
        return LaunchConfiguration(name).perform(context)

    params = {
        "hover_pose": arg("hover_pose"),
        "lower_distance": float(arg("lower_distance")),
        "lift_distance": float(arg("lift_distance")),
        "gripper_open_position": float(arg("gripper_open_position")),
    }
    # Left empty, the node falls back to the SRDF-named state "close".
    if arg("gripper_close_position"):
        params["gripper_close_position"] = float(arg("gripper_close_position"))

    return [
        Node(
            package="lara5_mtc",
            executable="mtc_pose_sequence",
            output="screen",
            parameters=[moveit_config.to_dict(), params],
        )
    ]


def generate_launch_description():
    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "hover_pose",
                default_value="a1_hover",
                description="SRDF arm state after mid_move, e.g. e4_hover or e4.",
            ),
            DeclareLaunchArgument(
                "lower_distance",
                default_value="0.05",
                description="Metres the EEF moves down (-Z) after reaching hover.",
            ),
            DeclareLaunchArgument(
                "lift_distance",
                default_value="0.05",
                description="Metres the EEF moves back up (+Z) after closing the gripper.",
            ),
            DeclareLaunchArgument(
                "gripper_open_position",
                default_value="0.25",
                description="Jaw joint angle in radians at hover, before descending.",
            ),
            DeclareLaunchArgument(
                "gripper_close_position",
                default_value="",
                description="Jaw joint angle in radians after descending. Empty: SRDF state 'close'.",
            ),
            OpaqueFunction(function=launch_setup),
        ]
    )
