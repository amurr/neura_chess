#!/usr/bin/env bash
# Bring up MoveIt + topic_based_ros2_control against a running Isaac world.
# Does not start Kit — run scripts/launch/launch_world.sh first (timeline playing).
set -euo pipefail
# shellcheck source=/dev/null
source "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/_repo_root.sh"
WS="${ROS2_WS:-${ROOT}/ros2_ws}"

if [[ -f /opt/ros/humble/setup.bash ]]; then
  # shellcheck source=/dev/null
  set +u
  source /opt/ros/humble/setup.bash
  set -u
fi
if [[ -f "${WS}/install/setup.bash" ]]; then
  # shellcheck source=/dev/null
  set +u
  source "${WS}/install/setup.bash"
  set -u
fi

export ROS_DOMAIN_ID="${ROS_DOMAIN_ID:-0}"
export RMW_IMPLEMENTATION="${RMW_IMPLEMENTATION:-rmw_fastrtps_cpp}"
export ROS_LOCALHOST_ONLY="${ROS_LOCALHOST_ONLY:-0}"
unset CYCLONEDDS_URI || true

echo "MoveIt Isaac: domain=$ROS_DOMAIN_ID rmw=$RMW_IMPLEMENTATION"
echo "Waiting for /isaac_joint_states (Isaac world must be playing)..."
ok=0
for _ in $(seq 1 60); do
  if ros2 topic info /isaac_joint_states >/dev/null 2>&1; then
    ok=1
    break
  fi
  sleep 1
done
if [[ "$ok" -ne 1 ]]; then
  echo "ERROR: /isaac_joint_states not found. Start scripts/launch/launch_world.sh first." >&2
  exit 1
fi

echo "Launching mtc_demo_isaac.launch.py"
exec ros2 launch lara5_moveit_config mtc_demo_isaac.launch.py "$@"
