#!/usr/bin/env bash
# Restore Isaac chess board + pieces + Lara joints to the authored start (no Kit relaunch).
# Requires a running world built from current neura_chess_world.py (SceneRestore).
set -euo pipefail
# shellcheck source=/dev/null
source "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/_repo_root.sh"
if [[ -f /opt/ros/humble/setup.bash ]]; then
  # shellcheck source=/dev/null
  set +u
  source /opt/ros/humble/setup.bash
  set -u
fi
if [[ -f "${ROOT}/ros2_ws/install/setup.bash" ]]; then
  # shellcheck source=/dev/null
  set +u
  source "${ROOT}/ros2_ws/install/setup.bash"
  set -u
fi
export ROS_DOMAIN_ID="${ROS_DOMAIN_ID:-0}"
export RMW_IMPLEMENTATION="${RMW_IMPLEMENTATION:-rmw_fastrtps_cpp}"
export ROS_LOCALHOST_ONLY="${ROS_LOCALHOST_ONLY:-0}"
unset CYCLONEDDS_URI || true
exec python3 "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/chess_scene_restore.py" "$@"
