Use **three terminals**. Do **not** use `ros2 run lara5_moveit moveit_chess` — that node has no SRDF / `robot_description_semantic` and dies immediately.

**1. Isaac world** (once; leave it running, timeline playing)

```bash
./scripts/launch/launch_world.sh
```

Wait until `/tmp/neura_chess_pieces.ready` exists and `/isaac_joint_states` is publishing.

**2. MoveIt + Isaac hardware** (once; leave it running)

```bash
source /opt/ros/humble/setup.bash
source /workspace/neura_chess/ros2_ws/install/setup.bash
export ROS_DOMAIN_ID=0 RMW_IMPLEMENTATION=rmw_fastrtps_cpp ROS_LOCALHOST_ONLY=0
./scripts/launch/launch_moveit_isaac.sh
```

This is `move_group`, `arm_controller`, and the `/isaac_joint_states` → `/joint_states` relay. Without it, planning can succeed and then you get `Failed to acquire current PlanningScene` or `Goal was aborted`.

**3. Run d2 → d3** (new terminal each attempt)

```bash
source /opt/ros/humble/setup.bash
source /workspace/neura_chess/ros2_ws/install/setup.bash
export ROS_DOMAIN_ID=0 RMW_IMPLEMENTATION=rmw_fastrtps_cpp ROS_LOCALHOST_ONLY=0

ros2 launch lara5_moveit_config mtc_run.launch.py \
  package:=lara5_moveit exe:=moveit_chess square:=d2 to:=d3
```

Success looks like `Planning succeeded` then `Execution succeeded`. If a previous run already moved the pawn, reset the board first:

```bash
./scripts/scene/chess_scene_restore.sh
```

**Sanity checks before execute**

List pieces (Kit handshake, no MoveIt):

```bash
ros2 launch lara5_moveit_config mtc_run.launch.py \
  package:=lara5_moveit exe:=moveit_chess list:=true
```

Print grasp targets only:

```bash
ros2 launch lara5_moveit_config mtc_run.launch.py \
  package:=lara5_moveit exe:=moveit_chess square:=d2 to:=d3 print_only:=true
```

Plan without sending trajectories:

```bash
ros2 launch lara5_moveit_config mtc_run.launch.py \
  package:=lara5_moveit exe:=moveit_chess square:=d2 to:=d3 plan_only:=true
```