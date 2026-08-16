# SO-101 gripper meshes

Required for RViz / Gazebo (from `so101_follower.urdf.xacro` / TheRobotStudio SO-ARM100).

**One-shot setup inside Docker** (recommended):

```bash
bash /ros2_ws/src/lara5_description/scripts/setup_so101_gripper.sh
source /ros2_ws/install/setup.bash
```

Or download only:

```bash
bash /ros2_ws/src/lara5_description/scripts/fetch_so101_gripper_meshes.sh
```

Windows:

```powershell
powershell -ExecutionPolicy Bypass -File src\lara5_description\scripts\fetch_so101_gripper_meshes.ps1
```

**Alternative:** if `so101_follower_description` is in your workspace, build with:

```bash
xacro lara5.urdf.xacro so101_mesh_uri:=package://so101_follower_description/meshes
```

Files in this folder:

- `moving_jaw_so101_v1.stl`
- `wrist_roll_follower_so101_v1.stl`
