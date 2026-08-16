#!/usr/bin/env bash
# Build, unit-test, and plan the TF-backed MTC chess pick-place tree (no execute).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WS="${ROS2_WS:-${ROOT}/ros2_ws}"
LOG="${MTC_TF_TEST_LOG:-/tmp/mtc_tf_pick_place}"
OCC="${WS}/src/xyz_motion/config/examples/e2_to_e4.json"

mkdir -p "$LOG"
# shellcheck source=/dev/null
set +u
source /opt/ros/humble/setup.bash
set -u

echo "== dependencies =="
"${ROOT}/scripts/check_dependencies.sh"

echo "== build =="
cd "$WS"
colcon build --packages-select xyz_motion lara5_mtc lara5_moveit_config lara5_description --symlink-install
# shellcheck source=/dev/null
set +u
source "${WS}/install/setup.bash"
set -u

echo "== unit tests =="
python3 -m pytest "${WS}/src/xyz_motion/test" -q --tb=short

echo "== stop leftover ROS nodes =="
# Match executable paths, not this script's source text.
for exe in move_group chess_scene ros2_control_node publish_grasp_tf \
           lara5_mtc_chess_cylinders robot_state_publisher; do
  pkill -9 -x "$exe" 2>/dev/null || true
  pkill -9 -f "/$exe " 2>/dev/null || true
  pkill -9 -f "/$exe$" 2>/dev/null || true
done
pkill -9 -f mtc_demo_headless.launch.py 2>/dev/null || true
pkill -9 -f chess_scene.launch.py 2>/dev/null || true
pkill -9 -f mtc_chess_cylinders_pick_place.launch.py 2>/dev/null || true
rm -f /dev/shm/cyclonedds* /dev/shm/fastrtps* 2>/dev/null || true
sleep 3
: >"$LOG/move_group.log"
: >"$LOG/chess_scene.log"
: >"$LOG/mtc.log"
cleanup_ros() {
  pkill -9 -f "/move_group " 2>/dev/null || true
  pkill -9 -f "/ros2_control_node " 2>/dev/null || true
  pkill -9 -f "/chess_scene " 2>/dev/null || true
  pkill -9 -f "/publish_grasp_tf " 2>/dev/null || true
  pkill -9 -f "/lara5_mtc_chess_cylinders_pick_place " 2>/dev/null || true
}
trap cleanup_ros EXIT

export ROS_LOCALHOST_ONLY="${ROS_LOCALHOST_ONLY:-1}"
export ROS_DOMAIN_ID="${ROS_DOMAIN_ID:-42}"
CYCLONE_XML="${WS}/src/lara5_moveit_config/config/cyclonedds.localhost.xml"
if [[ -f "$CYCLONE_XML" ]]; then
  export CYCLONEDDS_URI="file://${CYCLONE_XML}"
  export RMW_IMPLEMENTATION="${RMW_IMPLEMENTATION:-rmw_cyclonedds_cpp}"
elif [[ -f /etc/cyclonedds.localhost.xml ]]; then
  export CYCLONEDDS_URI=file:///etc/cyclonedds.localhost.xml
  export RMW_IMPLEMENTATION="${RMW_IMPLEMENTATION:-rmw_cyclonedds_cpp}"
fi

echo "== move_group (headless) =="
ros2 launch lara5_moveit_config mtc_demo_headless.launch.py >"$LOG/move_group.log" 2>&1 &
for _ in $(seq 1 90); do
  if grep -q "You can start planning now" "$LOG/move_group.log" 2>/dev/null; then
    break
  fi
  sleep 1
done
if ! grep -q "You can start planning now" "$LOG/move_group.log" 2>/dev/null; then
  echo "FAIL: move_group did not start"
  tail -n 80 "$LOG/move_group.log" || true
  exit 1
fi

echo "== chess_scene =="
ros2 launch xyz_motion chess_scene.launch.py use_cylinder_collision:=true planning_scene_only:=true \
  >"$LOG/chess_scene.log" 2>&1 &
for _ in $(seq 1 30); do
  if grep -q "published initial pieces" "$LOG/chess_scene.log" 2>/dev/null; then
    break
  fi
  sleep 1
done
if ! grep -q "published initial pieces" "$LOG/chess_scene.log" 2>/dev/null; then
  echo "FAIL: chess_scene did not publish pieces"
  tail -n 40 "$LOG/chess_scene.log" || true
  exit 1
fi
for _ in $(seq 1 15); do
  if grep -q "Republished board" "$LOG/chess_scene.log" 2>/dev/null; then
    break
  fi
  sleep 1
done
sleep 2
# Do not publish the 2-square e2_to_e4 occupancy onto /chess_occupancy — that
# replaces the 32-piece start with 1 object and can empty the MoveIt scene.
# MTC and grasp_tf load the same JSON from occupancy_file.

echo "== MTC plan (auto_execute=false keep_alive_s=0) =="
export CHESS_OCCUPANCY_FILE="$OCC"
export CHESS_SOURCE=e2
export CHESS_TARGET=e4
export CHESS_SEED_POSE=pre_pick
export AUTO_EXECUTE=false
export KEEP_ALIVE_S=0
set +e
timeout 180 ros2 launch lara5_mtc mtc_chess_cylinders_pick_place.launch.py \
  occupancy_file:="$OCC" source:=e2 target:=e4 seed_pose:=pre_pick \
  auto_execute:=false keep_alive_s:=0 \
  >"$LOG/mtc.log" 2>&1
MTC_RC=$?
set -e
tee -a "$LOG/mtc.tail" <"$LOG/mtc.log" >/dev/null
grep -E "Planning succeeded|Planning failed|Plan OK|TF lookup failed|Task initialization failed|pick hover pose unreachable" "$LOG/mtc.log" || true

if grep -q "Planning succeeded" "$LOG/mtc.log" && grep -q "Plan OK" "$LOG/mtc.log"; then
  echo "TEST_OK: MTC tree planned successfully and is ready to execute (auto_execute=false)."
  exit 0
fi
echo "FAIL: MTC plan did not succeed (launch rc=$MTC_RC). Last log:"
tail -n 120 "$LOG/mtc.log" || true
exit 1
