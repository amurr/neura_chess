#!/usr/bin/env bash
set -eo pipefail
source /opt/ros/humble/setup.bash
source /ros2_ws/install/setup.bash
export ROS_LOCALHOST_ONLY=1
export CYCLONEDDS_URI=file:///etc/cyclonedds.localhost.xml
LOG=/tmp/mtc_cylinder_test
mkdir -p "$LOG"
pkill -9 -f 'ros2 launch' 2>/dev/null || true
pkill -9 -f move_group 2>/dev/null || true
pkill -9 -f rviz 2>/dev/null || true
pkill -9 -f controller_manager 2>/dev/null || true
pkill -9 -f chess_scene 2>/dev/null || true
pkill -9 -f lara5_chess_mtc 2>/dev/null || true
sleep 3
cd /ros2_ws
colcon build --packages-select xyz_motion lara5_moveit_config --symlink-install
source install/setup.bash
ros2 launch lara5_moveit_config mtc_demo_headless.launch.py >"$LOG/t1.log" 2>&1 &
for i in $(seq 1 90); do
  ros2 node list 2>/dev/null | grep -q move_group && break
  sleep 1
done
for i in $(seq 1 30); do
  ros2 control list_controllers 2>/dev/null | grep -q joint_state_broadcaster && break
  sleep 1
done
ros2 control list_controllers 2>/dev/null | grep joint_state || {
  echo "WARN: joint_state_broadcaster missing — RViz TF errors likely"
  ros2 run controller_manager spawner joint_state_broadcaster || true
  sleep 2
}
ros2 launch xyz_motion chess_scene.launch.py use_cylinder_collision:=true >"$LOG/t2.log" 2>&1 &
for i in $(seq 1 30); do
  ros2 node list 2>/dev/null | grep -q chess_scene && break
  sleep 1
done
grep collision "$LOG/t2.log" | tail -1 || true
ros2 run xyz_motion publish_chess_occupancy -- /ros2_ws/src/xyz_motion/config/examples/e2_to_e4.json
sleep 2
export CHESS_OCCUPANCY_FILE=/ros2_ws/src/xyz_motion/config/examples/e2_to_e4.json
export CHESS_SOURCE=e2 CHESS_TARGET=e4 CHESS_SEED_POSE=mid_move
timeout 180 ros2 launch lara5_moveit_config mtc_run.launch.py \
  package:=lara5_moveit_config exe:=lara5_chess_mtc_pick_place.py 2>&1 | tee "$LOG/t3.log"
grep -E "Planning succeeded|Planning failed|Failing stage" "$LOG/t3.log" || true
