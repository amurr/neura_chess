#!/bin/bash
# Test camera_frame -> output frame TF (before IK).
# Prerequisite: moveit_ik_headless in another shell (robot_state_publisher + move_group).
set -eo pipefail
export ROS_DOMAIN_ID=0
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
export ROS_LOCALHOST_ONLY=1
export CYCLONEDDS_URI=file:///etc/cyclonedds.localhost.xml
source /opt/ros/humble/setup.bash
source /ros2_ws/install/setup.bash

CAM_TX=0.1
CAM_TY=0.0
CAM_TZ=0.2
PT_X=0.0
PT_Y=0.0
PT_Z=0.1
OUT_FRAME="${1:-lara5_gripper}"

pkill -f '/xyz_motion/camera_xyz_to_joints' 2>/dev/null || true
pkill -f 'static_transform_publisher.*camera_optical_frame' 2>/dev/null || true
sleep 1

if ! ros2 service list --no-daemon 2>/dev/null | grep -q '/compute_ik'; then
  echo "ERROR: Start MoveIt first in another terminal:"
  echo "  bash /docker/ros2-moveit-ik.sh"
  exit 1
fi

if ! pgrep -f robot_state_publisher >/dev/null; then
  echo "ERROR: robot_state_publisher is not running (MoveIt launch incomplete)."
  exit 1
fi

wait_for_tf() {
  local target=$1
  local source=$2
  local i
  for i in $(seq 1 20); do
    if timeout 3 ros2 run tf2_ros tf2_echo "$target" "$source" 2>&1 | grep -q 'At time'; then
      echo "TF ready: ${target} <- ${source} (after ${i}s)"
      return 0
    fi
    sleep 1
  done
  echo "ERROR: TF not connected: ${target} <- ${source}"
  echo "  Ensure moveit_ik_headless is running and /joint_states was received."
  return 1
}

echo "=== 1) Seed /joint_states (robot TF chain) ==="
ros2 topic pub --once /joint_states sensor_msgs/msg/JointState \
  "{name: ['lara5_joint1','lara5_joint2','lara5_joint3','lara5_joint4','lara5_joint5','lara5_joint6'], position: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}"
sleep 3

echo "=== 2) Static TF lara5_link0 -> camera_optical_frame ==="
ros2 run tf2_ros static_transform_publisher \
  --x "$CAM_TX" --y "$CAM_TY" --z "$CAM_TZ" \
  --roll 0 --pitch 0 --yaw 0 \
  --frame-id lara5_link0 --child-frame-id camera_optical_frame &
STF_PID=$!
sleep 2

cleanup() {
  kill "$STF_PID" 2>/dev/null || true
  kill "$NODE_PID" 2>/dev/null || true
}
trap cleanup EXIT

echo "=== 3) Wait for full TF chain to ${OUT_FRAME} ==="
wait_for_tf "$OUT_FRAME" camera_optical_frame || exit 1

echo "=== 4) Start camera_xyz_to_joints (output frame ${OUT_FRAME}) ==="
ros2 run xyz_motion camera_xyz_to_joints --ros-args \
  -p assume_base_frame:=false \
  -p base_frame:="${OUT_FRAME}" \
  -p camera_frame:=camera_optical_frame \
  -p tf_lookup_timeout_sec:=5.0 &
NODE_PID=$!
sleep 4

echo "=== 5) Publish point in camera_optical_frame ==="
echo "    camera point: (${PT_X}, ${PT_Y}, ${PT_Z}) m"
ros2 topic pub --once /object_xyz geometry_msgs/msg/PointStamped \
  "{header: {frame_id: 'camera_optical_frame'}, point: {x: ${PT_X}, y: ${PT_Y}, z: ${PT_Z}}}"

echo "=== 6) Transformed position on target_pose_base ==="
sleep 2
timeout 8 ros2 topic echo --once /camera_xyz_to_joints/target_pose_base geometry_msgs/msg/PoseStamped --no-daemon 2>&1 || true

echo ""
echo "PASS if node log shows: TF OK 'camera_optical_frame' (...) -> '${OUT_FRAME}' (...)"
echo "Tip: test shorter chain first: bash $0 lara5_link0"
