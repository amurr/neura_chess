#!/usr/bin/env bash
# Run in superbloom_ros2:
#   bash /ros2_ws/src/lara5_description/scripts/setup_so101_gripper.sh
set -eo pipefail
WS="/ros2_ws"
MESH_DIR="${WS}/src/lara5_description/lara5/meshes/so101"
URDF_DIR="${WS}/src/lara5_description/lara5/urdf"
BASE="https://raw.githubusercontent.com/TheRobotStudio/SO-ARM100/main/STL/SO101/Individual"

mkdir -p "${MESH_DIR}"
if [[ -f "${MESH_DIR}/moving_jaw_so101_v1.stl" && -f "${MESH_DIR}/wrist_roll_follower_so101_v1.stl" ]]; then
  echo "==> SO-101 meshes already present"
else
  echo "==> Downloading SO-101 gripper meshes ..."
  curl -fsSL -o "${MESH_DIR}/moving_jaw_so101_v1.stl" "${BASE}/Moving_Jaw_SO101.stl"
  curl -fsSL -o "${MESH_DIR}/wrist_roll_follower_so101_v1.stl" "${BASE}/Wrist_Roll_Follower_SO101.stl"
fi
ls -la "${MESH_DIR}"

source /opt/ros/humble/setup.bash
echo "==> Regenerating lara5.urdf ..."
xacro "${URDF_DIR}/lara5.urdf.xacro" -o "${URDF_DIR}/lara5.urdf"
grep -E "gripper_jaw|wrist_roll_follower" "${URDF_DIR}/lara5.urdf" | head -6

echo "==> colcon build ..."
cd "${WS}"
colcon build --packages-select lara5_description lara5_moveit_config xyz_motion
echo "==> OK. Run: source ${WS}/install/setup.bash"
