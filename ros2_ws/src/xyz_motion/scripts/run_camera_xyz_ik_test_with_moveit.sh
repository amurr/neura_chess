#!/bin/bash
# Starts headless MoveIt if /compute_ik is missing, then runs the IK integration test.
set -eo pipefail
export ROS_DOMAIN_ID=0
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
export ROS_LOCALHOST_ONLY=1
export CYCLONEDDS_URI=file:///etc/cyclonedds.localhost.xml
source /opt/ros/humble/setup.bash
source /ros2_ws/install/setup.bash

MOVEIT_PID=""
cleanup() {
  if [[ -n "${MOVEIT_PID}" ]]; then
    kill "${MOVEIT_PID}" 2>/dev/null || true
  fi
}
trap cleanup EXIT

if ! ros2 service list 2>/dev/null | grep -q '/compute_ik'; then
  echo "=== Starting moveit_ik_headless ==="
  ros2 launch lara5_moveit_config moveit_ik_headless.launch.py &
  MOVEIT_PID=$!
  for _ in $(seq 1 30); do
    if ros2 service list 2>/dev/null | grep -q '/compute_ik'; then
      echo "=== /compute_ik ready ==="
      break
    fi
    sleep 1
  done
  if ! ros2 service list 2>/dev/null | grep -q '/compute_ik'; then
    echo "ERROR: /compute_ik never appeared"
    exit 1
  fi
fi

exec bash /ros2_ws/src/xyz_motion/scripts/run_camera_xyz_ik_test.sh
