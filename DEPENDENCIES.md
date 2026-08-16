# Dependencies

See `dependencies.txt` (checked by `scripts/check_dependencies.sh`).

## Required to **plan** the MTC tree

- ROS 2 Humble (`ros2`, `colcon`)
- MoveIt 2 + MoveIt Task Constructor (`moveit_core`, `moveit_task_constructor_core`)
- `tf2_ros`, `geometry_msgs`, `rclcpp` / `rclpy`, `nlohmann_json`
- Python 3: `numpy`, `pytest`, `yaml`

Workspace packages: `xyz_motion`, `lara5_mtc`, `lara5_moveit_config`, `lara5_description`.

## Optional (later **execute** in Isaac)

- Isaac Sim with `isaacsim.ros2.bridge` (`scripts/setup_isaac_ros_env.sh`, `scripts/launch_world.sh`)
- Compatible RMW / `ROS_DOMAIN_ID` between Isaac and this workspace so `/isaac_joint_commands` reaches the arm

Isaac is **not** required for `scripts/run_mtc_tf_plan_test.sh`.
