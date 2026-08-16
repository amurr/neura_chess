#!/usr/bin/env bash
# Launch the neura chess PhysX world into the existing VNC display (:1).
# Same method as supermarket_world: Isaac python.sh on DISPLAY=:1, no vglrun.
# Isolated runtime/log/prims. Only one Kit instance can run on this GPU.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORLD_SCRIPT="${ROOT}/neura_chess_world.py"
LOCAL_ROOT="${NEURA_CHESS_WORLD_LOCAL_ROOT:-/tmp/neura_chess_world_runtime}"
ISAAC_SIM_ROOT="${ISAAC_SIM_ROOT:-/workspace/isaacsim}"
LOG="/tmp/neura_chess_world.log"

export DISPLAY="${DISPLAY:-:1}"
export ACCEPT_EULA="${ACCEPT_EULA:-Y}"
export PRIVACY_CONSENT="${PRIVACY_CONSENT:-Y}"
export OMNI_KIT_ALLOW_ROOT=1
export OMNI_KIT_ACCEPT_EULA=YES
export OMNI_SERVER="${OMNI_SERVER:-https://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Isaac/6.0}"
export NVIDIA_DRIVER_CAPABILITIES="${NVIDIA_DRIVER_CAPABILITIES:-all,graphics,utility,compute,display,video}"
export PYTHONUNBUFFERED=1

# Do not inherit chess / supermarket / host MoveIt overlays into this Kit process.
# Isaac ROS libs come from setup_isaac_ros_env.sh (bundled Humble), not ros2_ws.
unset AMENT_PREFIX_PATH COLCON_PREFIX_PATH CMAKE_PREFIX_PATH
unset ROS_DISTRO ROS_VERSION ROS_PYTHON_VERSION RMW_IMPLEMENTATION
unset PIPER_CHESS_ROOT PIPER_CHESS_LOCAL_ROOT MTC_FEEDBACK_LOGS PIPER_ROS_DISTRO
unset SUPERMARKET_WORLD_ROOT SUPERMARKET_WORLD_LOCAL_ROOT
unset VGL_DISPLAY

if [[ -z "${XAUTHORITY:-}" ]]; then
  if [[ -f /home/ubuntu/.Xauthority ]]; then
    cp -f /home/ubuntu/.Xauthority /root/.Xauthority
    chmod 600 /root/.Xauthority
    export XAUTHORITY=/root/.Xauthority
  elif [[ -f "${HOME}/.Xauthority" ]]; then
    export XAUTHORITY="${HOME}/.Xauthority"
  fi
fi
if command -v xhost >/dev/null 2>&1; then
  DISPLAY="$DISPLAY" XAUTHORITY="${XAUTHORITY:-}" xhost +local:root >/dev/null 2>&1 || true
  DISPLAY="$DISPLAY" XAUTHORITY="${XAUTHORITY:-}" xhost +SI:localuser:root >/dev/null 2>&1 || true
fi

chmod a+rw /dev/dri/card* /dev/dri/renderD* 2>/dev/null || true
if [[ ! -e /dev/dri/renderD128 ]]; then
  for n in 130 135 129 131 132 133 134; do
    if [[ -e "/dev/dri/renderD${n}" ]]; then
      ln -sf "/dev/dri/renderD${n}" /dev/dri/renderD128 || true
      break
    fi
  done
fi

echo "Stopping any previous Isaac Kit processes..."
mapfile -t KIT_PIDS < <(
  pgrep -f '/workspace/isaacsim/kit/kit ' || true
  pgrep -f '/workspace/isaacsim/kit/python/bin/python3 .*/neura_chess_world\\.py' || true
  pgrep -f '/workspace/neura_chess/neura_chess_world\\.py' || true
  pgrep -f '/tmp/neura_chess_world_runtime/neura_chess_world\\.py' || true
  pgrep -f '/workspace/isaacsim/kit/python/bin/python3 .*/supermarket_world\\.py' || true
  pgrep -f '/tmp/supermarket_world_runtime/supermarket_world\\.py' || true
  pgrep -f '/workspace/isaacsim/kit/python/bin/python3 .*/piper_chess_world\\.py' || true
  pgrep -f '/tmp/piper_chess_runtime/piper_chess_world\\.py' || true
  pgrep -f '/workspace/isaacsim/isaac-sim\\.sh' || true
)
declare -A SEEN=()
KILL_LIST=()
for pid in "${KIT_PIDS[@]}"; do
  [[ -z "$pid" ]] && continue
  [[ "$pid" == "$$" || "$pid" == "$PPID" ]] && continue
  [[ -n "${SEEN[$pid]:-}" ]] && continue
  SEEN[$pid]=1
  KILL_LIST+=("$pid")
done
if ((${#KILL_LIST[@]})); then
  echo "Killing: ${KILL_LIST[*]}"
  kill -9 "${KILL_LIST[@]}" 2>/dev/null || true
fi
sleep 2

echo "Syncing project to local cache: $LOCAL_ROOT"
mkdir -p "$LOCAL_ROOT"
if command -v rsync >/dev/null 2>&1; then
  rsync -a --exclude '.git' --exclude '__pycache__' --exclude '.kit_portable' \
    --exclude 'ros2_ws' \
    "$ROOT/" "$LOCAL_ROOT/"
else
  rm -rf "$LOCAL_ROOT"
  mkdir -p "$LOCAL_ROOT"
  cp -a "$ROOT/." "$LOCAL_ROOT/"
  rm -rf "$LOCAL_ROOT/.git" "$LOCAL_ROOT/.kit_portable" "$LOCAL_ROOT/ros2_ws"
fi
WORLD_SCRIPT="${LOCAL_ROOT}/neura_chess_world.py"
export NEURA_CHESS_WORLD_ROOT="$LOCAL_ROOT"
export PYTHONPATH="${LOCAL_ROOT}${PYTHONPATH:+:$PYTHONPATH}"
# shellcheck source=/dev/null
source "${ROOT}/scripts/setup_isaac_ros_env.sh"

rm -f "$LOG"

echo "Launching neura chess world on DISPLAY=$DISPLAY"
echo "Isaac: $ISAAC_SIM_ROOT"
echo "Script: $WORLD_SCRIPT"
echo "Log: $LOG"
echo "Launcher: ${ISAAC_SIM_ROOT}/python.sh (no vglrun)"
echo "Args: $*"

LAUNCH_CMD=("${ISAAC_SIM_ROOT}/python.sh" "$WORLD_SCRIPT" "$@")

nohup "${LAUNCH_CMD[@]}" >"$LOG" 2>&1 &
PID=$!
echo "PID $PID"
sleep 8
if ! kill -0 "$PID" 2>/dev/null; then
  echo "Process exited early — last log lines:"
  tail -n 80 "$LOG" || true
  exit 1
fi
echo "---- log ----"
tail -n 40 "$LOG" || true
echo "----"
echo "Follow with: tail -f $LOG"
echo "Isaac window is on VNC DISPLAY=$DISPLAY (first viewport can take 1–2 min)."
