#!/usr/bin/env bash
# Bring up the lara5_bringup stack (ros2_control with topic_based_ros2_control,
# MoveIt, RViz, chess app nodes) against a running Isaac world.
# Does not start Kit — run scripts/launch/launch_world.sh first (timeline playing).
# Extra args go to bringup.launch.py, e.g. use_rviz:=false orchestrator:=true.
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
# Kit runs without ROS_LOCALHOST_ONLY; bringup.launch.py would default it to 1.
export ROS_LOCALHOST_ONLY="${ROS_LOCALHOST_ONLY:-0}"
unset CYCLONEDDS_URI || true

if ! python3 -c "import moveit_configs_utils" >/dev/null 2>&1; then
  echo "ERROR: moveit_configs_utils missing. Run ./scripts/ros2h_installation.sh" >&2
  echo "  then: source /opt/ros/humble/setup.bash && source ros2_ws/install/setup.bash" >&2
  exit 1
fi

echo "MoveIt Isaac: domain=$ROS_DOMAIN_ID rmw=$RMW_IMPLEMENTATION"
# Wait before starting the controllers: until topic_based_ros2_control receives
# Isaac's state it reports 0.0 for every joint, and the arm would be sent there.
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

CONTROLLERS="$(ros2 pkg prefix lara5_bringup)/share/lara5_bringup/config/ros2_controllers_isaac.yaml"
echo "Launching lara5_bringup bringup.launch.py hardware:=isaac"
exec ros2 launch lara5_bringup bringup.launch.py hardware:=isaac \
  controllers_file:="$CONTROLLERS" "$@"
