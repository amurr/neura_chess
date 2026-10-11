"""Stage 2: ros2_control.

Starts the controller manager and spawns controllers in order:
  controller_manager -> joint_state_broadcaster -> arm_controller + gripper_controller

The arm/gripper spawners start only after the joint_state_broadcaster spawner
has exited (i.e. that controller is loaded and active), via OnProcessExit.

Requires robot_state_publisher to be running (description.launch.py): the
controller manager reads the URDF from the /robot_description topic (backported
to Humble controller_manager 2.x; passing it as a parameter is deprecated there).
Hardware comes from the URDF (config/lara5.urdf.xacro): mock_components/GenericSystem
by default, topic_based_ros2_control for Isaac Sim (hardware:=isaac in description.launch.py).
With hardware:=isaac this stage also starts pad_joint_commands: the plugin publishes
positions only on /isaac_hw_joint_commands, Isaac's ROS2SubscribeJointState only
accepts JointState with velocity/effort filled in on /isaac_joint_commands.

Usage:
  ros2 launch lara5_bringup control.launch.py
  ros2 launch lara5_bringup control.launch.py hardware:=isaac \
      controllers_file:=$(ros2 pkg prefix lara5_bringup)/share/lara5_bringup/config/ros2_controllers_isaac.yaml
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, RegisterEventHandler
from launch.conditions import LaunchConfigurationEquals
from launch.event_handlers import OnProcessExit
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    use_sim_time = LaunchConfiguration("use_sim_time")
    controllers_file = LaunchConfiguration("controllers_file")

    declared_arguments = [
        DeclareLaunchArgument(
            "hardware",
            default_value="mock",
            description="Must match the value used in description.launch.py.",
        ),
        DeclareLaunchArgument(
            "use_sim_time",
            default_value="false",
            description="Use /clock from a simulator.",
        ),
        DeclareLaunchArgument(
            "controllers_file",
            default_value=PathJoinSubstitution(
                [FindPackageShare("lara5_bringup"), "config", "ros2_controllers.yaml"]
            ),
            description="Full path to the ros2_control controllers YAML.",
        ),
    ]

    # Not started in simulation: Gazebo's ros2_control plugin runs its own controller manager.
    controller_manager = Node(
        package="controller_manager",
        executable="ros2_control_node",
        output="screen",
        parameters=[controllers_file, {"use_sim_time": use_sim_time}],
        remappings=[("~/robot_description", "/robot_description")],
    )

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        output="screen",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager", "/controller_manager",
            "--controller-manager-timeout", "30",
        ],
    )

    arm_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        output="screen",
        arguments=["arm_controller", "--controller-manager", "/controller_manager"],
    )

    gripper_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        output="screen",
        arguments=["gripper_controller", "--controller-manager", "/controller_manager"],
    )

    # Isaac only: topic_based_ros2_control -> /isaac_hw_joint_commands -> pad -> /isaac_joint_commands.
    pad_joint_commands = Node(
        package="lara5_moveit",
        executable="pad_joint_commands",
        name="isaac_joint_command_pad",
        output="screen",
        parameters=[
            {"in_topic": "/isaac_hw_joint_commands"},
            {"out_topic": "/isaac_joint_commands"},
        ],
        condition=LaunchConfigurationEquals("hardware", "isaac"),
    )

    # Stage the motion controllers after the joint_state_broadcaster is active.
    start_motion_controllers = RegisterEventHandler(
        OnProcessExit(
            target_action=joint_state_broadcaster_spawner,
            on_exit=[arm_controller_spawner, gripper_controller_spawner],
        )
    )

    return LaunchDescription(
        declared_arguments
        + [
            controller_manager,
            pad_joint_commands,
            joint_state_broadcaster_spawner,
            start_motion_controllers,
        ]
    )
