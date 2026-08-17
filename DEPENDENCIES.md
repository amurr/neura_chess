# Dependencies

See `dependencies.txt` (checked by `scripts/setup/check_dependencies.sh`).

After a pod relaunch only `/workspace` survives. Reinstall system packages with:

```bash
./scripts/setup/install_dependencies.sh
source /opt/ros/humble/setup.bash
source ros2_ws/install/setup.bash
```

## Required to **plan** the MTC tree

- ROS 2 Humble (`ros2`, `colcon`)
- MoveIt 2 + MoveIt Task Constructor (`moveit_core`, `moveit_task_constructor_core`)
- `tf2_ros`, `geometry_msgs`, `rclcpp` / `rclpy`, `nlohmann_json`
- Python 3: `numpy`, `pytest`, `yaml`

Workspace packages: `xyz_motion`, `lara5_mtc`, `lara5_moveit_config`, `lara5_description`.

## Optional (execute in Isaac)

- `topic_based_ros2_control` (`sudo apt install ros-humble-topic-based-ros2-control`)
- Isaac Sim with `isaacsim.ros2.bridge` (`scripts/setup/setup_isaac_ros_env.sh`, `scripts/launch/launch_world.sh`)
- Same `RMW_IMPLEMENTATION` (default `rmw_fastrtps_cpp`) and `ROS_DOMAIN_ID` (default `0`) as Kit

Launch: `scripts/launch/launch_moveit_isaac.sh` then chess_scene / MTC with `isaac:=true`.

Isaac is **not** required for `scripts/test/run_mtc_tf_plan_test.sh`.
