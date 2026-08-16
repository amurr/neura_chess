#!/usr/bin/env bash
# Download SO-101 gripper STL meshes into lara5_description (TheRobotStudio/SO-ARM100).
set -eo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MESH_DIR="$(cd "${SCRIPT_DIR}/../lara5/meshes/so101" && pwd)"
BASE="https://raw.githubusercontent.com/TheRobotStudio/SO-ARM100/main/STL/SO101/Individual"
mkdir -p "${MESH_DIR}"
curl -fsSL -o "${MESH_DIR}/moving_jaw_so101_v1.stl" "${BASE}/Moving_Jaw_SO101.stl"
curl -fsSL -o "${MESH_DIR}/wrist_roll_follower_so101_v1.stl" "${BASE}/Wrist_Roll_Follower_SO101.stl"
# STS3215 servo mesh (shared SO-100 part; used on gripper housing in onshape URDF)
curl -fsSL -o "${MESH_DIR}/sts3215_03a_v1.stl" \
  "https://raw.githubusercontent.com/TheRobotStudio/SO-ARM100/main/STL/SO100/Individual/STS3215_03a_v1.stl" \
  || curl -fsSL -o "${MESH_DIR}/sts3215_03a_v1.stl" \
  "https://raw.githubusercontent.com/TheRobotStudio/SO-ARM100/main/STL/SO100/Individual/STS3215_03a.stl"
echo "Installed SO-101 gripper meshes in ${MESH_DIR}"
