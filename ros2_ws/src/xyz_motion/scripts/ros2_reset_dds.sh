#!/bin/bash
# DDS reset (mounted in container at /ros2_ws/src/xyz_motion/scripts/).
set -eo pipefail
if [[ -x /docker/ros2-cleanup.sh ]]; then
  bash /docker/ros2-cleanup.sh
else
  pkill -9 -f 'ros2 launch' 2>/dev/null || true
  pkill -9 -f 'ros2 run' 2>/dev/null || true
  pkill -9 -f move_group 2>/dev/null || true
  pkill -9 -f robot_state_publisher 2>/dev/null || true
  pkill -9 -f ros2_control_node 2>/dev/null || true
  pkill -9 -f rviz2 2>/dev/null || true
  pkill -9 -f camera_xyz_to_joints 2>/dev/null || true
  rm -rf /dev/shm/cyclonedds* /dev/shm/iceoryx* 2>/dev/null || true
  export ROS_DOMAIN_ID=0
  export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
  export CYCLONEDDS_URI="${CYCLONEDDS_URI:-file:///etc/cyclonedds.localhost.xml}"
  source /opt/ros/humble/setup.bash 2>/dev/null || true
  ros2 daemon stop 2>/dev/null || true
  sleep 2
  echo "ROS processes cleaned."
fi
export ROS_DOMAIN_ID=0
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
export ROS_LOCALHOST_ONLY=1
export CYCLONEDDS_URI=file:///etc/cyclonedds.localhost.xml
source /opt/ros/humble/setup.bash
source /ros2_ws/install/setup.bash 2>/dev/null || true
if ros2 service list 2>/dev/null | head -1 >/dev/null; then
  echo "DDS OK — you can launch MoveIt now."
else
  echo "DDS still broken — run: docker restart superbloom_ros2"
  exit 1
fi
