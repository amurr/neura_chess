#!/usr/bin/env bash
# Source before launching Isaac via python.sh so isaacsim.ros2.* can load.
# python.sh does NOT call setup_ros_env.sh (only isaac-sim.sh does).
#
# Uses Isaac Sim's bundled Humble libs only — do not overlay host / ros2_ws.
set -euo pipefail

ISAAC_SIM_ROOT="${ISAAC_SIM_ROOT:-/workspace/isaacsim}"
ROS_CORE_EXT="${ISAAC_SIM_ROOT}/exts/isaacsim.ros2.core"

if [[ ! -d "$ROS_CORE_EXT" ]]; then
  echo "ERROR: ROS2 core extension not found at $ROS_CORE_EXT" >&2
  return 1 2>/dev/null || exit 1
fi

export ROS_DISTRO="${NEURA_ROS_DISTRO:-humble}"

LIB_DIR="${ROS_CORE_EXT}/${ROS_DISTRO}/lib"
if [[ ! -d "$LIB_DIR" ]]; then
  echo "ERROR: Internal ROS libs missing: $LIB_DIR" >&2
  echo "  Set NEURA_ROS_DISTRO=jazzy or humble to match available bridge libs." >&2
  return 1 2>/dev/null || exit 1
fi

export ROS_DOMAIN_ID="${ROS_DOMAIN_ID:-0}"
export RMW_IMPLEMENTATION="${RMW_IMPLEMENTATION:-rmw_fastrtps_cpp}"
BIN_DIR="${ROS_CORE_EXT}/bin"
export LD_LIBRARY_PATH="${LIB_DIR}${BIN_DIR:+:$BIN_DIR}${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"

PY_SITE="${ROS_CORE_EXT}/${ROS_DISTRO}/rclpy"
if [[ -d "$PY_SITE" ]]; then
  export PYTHONPATH="${PY_SITE}${PYTHONPATH:+:$PYTHONPATH}"
fi

if [[ -n "${AMENT_PREFIX_PATH:-}" ]]; then
  echo "WARNING: AMENT_PREFIX_PATH is set; Isaac should use internal bridge libs only." >&2
  echo "         Unset host ROS in this shell if the bridge fails to load." >&2
fi

echo "Isaac ROS2 env: ROS_DISTRO=$ROS_DISTRO RMW=$RMW_IMPLEMENTATION DOMAIN=${ROS_DOMAIN_ID}"
echo "  LD_LIBRARY_PATH includes $LIB_DIR"
if [[ -d "$BIN_DIR" ]]; then
  echo "  plugin bin: $BIN_DIR"
fi
if [[ ! -f "${BIN_DIR}/libisaacsim.ros2.core.${ROS_DISTRO}.so" ]]; then
  echo "WARNING: ${BIN_DIR}/libisaacsim.ros2.core.${ROS_DISTRO}.so not found;" >&2
  echo "         native isaacsim.ros2.core may log 'Create Factory Failed'." >&2
fi
