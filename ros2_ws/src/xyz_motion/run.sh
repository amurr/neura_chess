#!/usr/bin/env bash
# Run ROS scripts from a second docker exec shell (must match bringup DDS settings).
# chess / 2.py:  ros2 run xyz_motion chess_move   (after colcon build + source install)
set -eo pipefail
export ROS_DOMAIN_ID=0
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
export ROS_LOCALHOST_ONLY=1
export CYCLONEDDS_URI=file:///etc/cyclonedds.localhost.xml
source /opt/ros/humble/setup.bash
source /ros2_ws/install/setup.bash
cd "$(dirname "$0")"
exec env \
  ROS_DOMAIN_ID="${ROS_DOMAIN_ID}" \
  RMW_IMPLEMENTATION="${RMW_IMPLEMENTATION}" \
  ROS_LOCALHOST_ONLY="${ROS_LOCALHOST_ONLY}" \
  CYCLONEDDS_URI="${CYCLONEDDS_URI}" \
  python3 "$@"
