#!/usr/bin/env bash
# Verify commands, ROS packages, and Python modules from dependencies.txt.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEPS="${ROOT}/dependencies.txt"
FAIL=0

set +u
if [[ -f /opt/ros/humble/setup.bash ]]; then
  # shellcheck source=/dev/null
  source /opt/ros/humble/setup.bash
fi
if [[ -f "${ROS2_WS:-${ROOT}/ros2_ws}/install/setup.bash" ]]; then
  # shellcheck source=/dev/null
  source "${ROS2_WS:-${ROOT}/ros2_ws}/install/setup.bash" || true
fi
set -u

echo "Checking dependencies from $DEPS"
echo "ROS_DISTRO=${ROS_DISTRO:-unset}"

while read -r kind name extra; do
  [[ -z "${kind:-}" || "$kind" =~ ^# ]] && continue
  case "$kind" in
    cmd)
      if command -v "$name" >/dev/null 2>&1; then
        echo "  OK  cmd  $name ($(command -v "$name"))"
      else
        echo "  MISSING cmd  $name"
        FAIL=1
      fi
      ;;
    deb)
      if dpkg -s "$name" >/dev/null 2>&1; then
        echo "  OK  deb  $name"
      else
        echo "  MISSING deb  $name"
        FAIL=1
      fi
      ;;
    ros_pkg)
      if ros2 pkg prefix "$name" >/dev/null 2>&1; then
        echo "  OK  ros  $name  $(ros2 pkg prefix "$name")"
      else
        echo "  MISSING ros  $name"
        FAIL=1
      fi
      ;;
    python)
      if python3 -c "import $name" >/dev/null 2>&1; then
        echo "  OK  py   $name"
      else
        echo "  MISSING py   $name"
        FAIL=1
      fi
      ;;
    *)
      echo "  SKIP unknown kind $kind"
      ;;
  esac
done < <(grep -v '^[[:space:]]*$' "$DEPS" | grep -v '^#')

if [[ "$FAIL" -ne 0 ]]; then
  echo "FAIL: one or more dependencies are missing."
  exit 1
fi
echo "OK: all listed dependencies are installed."
