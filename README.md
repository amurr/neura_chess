# Neura Chess — Lara5 pick-and-place

Two-phase control stack:

- **Phase A** — `xyz_motion/publish_grasp_tf` computes a perpendicular EEF pose per square and broadcasts TF (`world → grasp/e2`, `hover/e2`, …).
- **Phase B** — `lara5_mtc` builds a **parametrized** MTC tree from two frame names (`grasp/<src>`, `grasp/<tgt>`), plans, and is ready to execute.

Isaac Sim (`neura_chess_world.py`) is **not** required to plan. Execution sends joint-space position commands through `topic_based_ros2_control` → `isaacsim.ros2.bridge` (`/isaac_joint_commands` → ArticulationController → `/isaac_joint_states`).

Repo scripts live under `scripts/` by job:

| Dir | Role |
|---|---|
| `scripts/setup/` | apt deps, Isaac ROS env |
| `scripts/launch/` | Kit world, MoveIt-on-Isaac |
| `scripts/scene/` | restore board/pieces, RigidPrim poses |
| `scripts/test/` | MTC plan CI |
| `scripts/vnc/` | display |

## Inputs

Every input the stack consumes. Defaults match the 40 mm board in front of Lara (`chess_scene` / `grasp_tf` YAML).

### 1. Chess move (occupancy JSON)

Published on `/chess_occupancy` or loaded from a file. Selects **which** piece moves. Pose orientation is **not** read from this message.

| Field | Required | Meaning |
|---|---|---|
| `source` / `from` / `from_square` | if not passed as ROS param | Pick square, e.g. `"e2"` |
| `target` / `to` / `to_square` | if not passed as ROS param | Place square, e.g. `"e4"` |
| `squares.<sq>.x,y,z` | for occupied squares | Square / piece position in **planning frame** (metres) |
| `squares.<sq>.type` | recommended | `pawn` `knight` `bishop` `rook` `queen` `king` — sets grasp height |
| `squares.<sq>.color` / `camp` | optional | `white` / `black` |
| `z` meaning | via `z_is_piece_top` | **false** (default): `z` is board/square surface. Grasp = `z + piece_height + grasp_clearance_m`. **true**: `z` is **detected piece top**. Grasp = `z + gripper_z_offset_m`. Empty destination squares never use a piece-top Z; they use board surface + the moving piece’s height. |

Example: `ros2_ws/src/xyz_motion/config/examples/e2_to_e4.json`.

### 2. Board calibration (Phase A)

Used by `publish_grasp_tf` and `chess_scene`. Must agree so collision objects and TF line up.

| Parameter | Default | Meaning |
|---|---|---|
| `planning_frame` | `world` | TF parent / MoveIt planning frame |
| `board_a1` | `[0.27, -0.16, 0.02]` | a1 **corner** in planning frame (m) |
| `board_b1` | `[0.31, -0.16, 0.02]` | one file-step from a1 |
| `board_a2` | `[0.27, -0.12, 0.02]` | one rank-step from a1 |
| `square_size` | `0.04` | Square width (m) |
| `board_thickness` | `0.02` | Used for surface Z = thickness/2 in the board frame |
| `board_layout` | `ranks_x_files_y` | Ranks along board +X (white near the arm) |
| `board_file_mirror` | `true` | Flip files a↔h to match this occupancy set |

Surface **normal** = calibrated +Z. EEF +Z is aligned to **−normal** (into the board).

### 3. Grasp TF publisher (`publish_grasp_tf`)

| Parameter | Default | Meaning |
|---|---|---|
| `board_frame` | `board` | Child of `world` at the a1 corner |
| `square_frame_prefix` | `square` | Frames `square/a1` … `square/h8` (square centers) |
| `grasp_frame_prefix` | `grasp` | Frames MTC looks up (`grasp/e2`) |
| `hover_frame_prefix` | `hover` | Grasp translated `approach_m` along +normal |
| `chess_occupancy_topic` | `/chess_occupancy` | Live XYZ / Z updates |
| `occupancy_file` | `""` | Optional JSON loaded at start |
| `approach_m` | `0.08` | Hover offset along the board normal (m) |
| `grasp_clearance_m` | `0.015` | Added when `z_is_piece_top` is false |
| `gripper_z_offset_m` | `0.0` | Added when `z_is_piece_top` is true (usually ≤ 0) |
| `z_is_piece_top` | `false` | How to interpret occupancy / detected Z |
| `grasp_yaw_rad` | `0.0` | Extra rotation about the approach axis (finger alignment) |
| `publish_rate_hz` | `20.0` | Dynamic TF rate |
| `broadcast_all_squares` | `true` | 64 squares each cycle |
| `piece_dims.<type>` | see YAML | `[diameter_m, height_m]` per piece |

**TF tree (all in `world` for MTC):**

- `world → board`
- `world → square/<sq>`
- `world → grasp/<sq>`  ← pick/place goal (position + perpendicular orientation)
- `world → hover/<sq>`

### 4. MTC task (`lara5_mtc_chess_cylinders_pick_place`)

| Parameter | Default | Meaning |
|---|---|---|
| `chess_source_square` | `e2` | Or env `CHESS_SOURCE` |
| `chess_target_square` | `e4` | Or env `CHESS_TARGET` |
| `chess_occupancy_file` | example JSON | Or env `CHESS_OCCUPANCY_FILE` — **move identity only** |
| `chess_pick_frame` | `""` → `grasp/<source>` | Override pick TF child |
| `chess_place_frame` | `""` → `grasp/<target>` | Override place TF child |
| `chess_grasp_frame_prefix` | `grasp` | Prefix when pick/place frames are empty |
| `chess_world_frame` | `world` | TF lookup parent |
| `chess_tf_timeout_s` | `10.0` | How long to wait for grasp frames |
| `chess_seed_pose` | `pre_pick` | SRDF named state before the hover |
| `chess_approach_m` | `0.08` | Cartesian approach / retreat distance |
| `chess_lift_m` | `0.08` | Lift after grasp |
| `chess_hover_mode` | `cartesian` | `cartesian`: XYZ from seed (CI-proven). `pose`: `MoveTo` TF hover (applies TF orientation; use with a tilted board). |
| `chess_approach_frame` | `world` | `world`: ±Z. `eef`: tool +Z (into the board once orientation is TF). |
| `auto_execute` | `false` | If true, `task.execute` after a successful plan |
| `keep_alive_s` | `-1` | `0` = exit after plan (CI). `-1` = stay up for RViz Execute |
| `planning_scene_timeout_s` | `30` | Wait for `piece_<source>` in the planning scene |

Factory (called once per chess move):

```text
createPickPlaceTask(pick_frame, place_frame, object_id)
  current → open gripper → seed
  → collision allows
  → pick hover → approach → close → attach → lift
  → place hover → descend → detach → retreat → open
  → stand
```

The tree is **planned** (`task.plan`). Execution uses the same MoveIt controllers (`arm_controller`, `gripper_controller`). With Isaac, those controllers sit on `topic_based_ros2_control` and publish `/isaac_joint_commands`.

### 5. Planning scene (`chess_scene`)

Same board corners as grasp TF. Cylinder collision (`use_cylinder_collision:=true`) is required for this MTC tree. Object ids: `piece_e2`, `board_sq_e2`, …

### 6. Isaac execution

MoveIt controllers are unchanged (`arm_controller` FollowJointTrajectory, `gripper_controller` GripperCommand). The **hardware plugin** is what talks to Kit.

| Input | Topic / item | Meaning |
|---|---|---|
| Joint position commands | `/isaac_joint_commands` (`sensor_msgs/JointState`) | Drive Lara5 DoF |
| Joint states | `/isaac_joint_states` | Feedback into `ros2_control` / MoveIt |
| Clock | `/clock` | Sim time (optional `use_sim_time:=true`) |

```bash
# 1) Isaac world (bridge + ArticulationController). Default domain 0, FastRTPS.
./scripts/launch/launch_world.sh

# 2) MoveIt with topic_based hardware (waits for /isaac_joint_states)
./scripts/launch/launch_moveit_isaac.sh

# 3) Planning scene + MTC execute (same RMW / domain as Kit — isaac:=true)
source /opt/ros/humble/setup.bash
source ros2_ws/install/setup.bash
export ROS_DOMAIN_ID=0 RMW_IMPLEMENTATION=rmw_fastrtps_cpp ROS_LOCALHOST_ONLY=0
ros2 launch xyz_motion chess_scene.launch.py isaac:=true \
  use_cylinder_collision:=true planning_scene_only:=true
ros2 launch lara5_mtc mtc_chess_cylinders_pick_place.launch.py isaac:=true \
  occupancy_file:=ros2_ws/src/xyz_motion/config/examples/e2_to_e4.json \
  auto_execute:=true
```

Between MTC runs, do **not** relaunch Kit. Restore the chess board, all 32 pieces, and Lara joints:

```bash
./scripts/scene/chess_scene_restore.sh
```

Dump **PhysX** piece poses (RigidPrim, not occupancy / MoveIt) at the current sim step:

```bash
./scripts/scene/pieces_positions_RigidPrim.sh
./scripts/scene/pieces_positions_RigidPrim.sh --out /tmp/after_mtc.json
./scripts/scene/pieces_positions_RigidPrim.sh --record 10   # JSONL while MTC runs
./scripts/scene/pieces_positions_RigidPrim.sh --stop
```

Restart `./scripts/launch/launch_world.sh` once after a `neura_chess_world.py` change so Kit loads SceneRestore and PiecePositions. Wait until the log shows `Scene restore snapshot` and `PiecePositions RigidPrim` (`/tmp/neura_chess_restore.ready` and `/tmp/neura_chess_pieces.ready`). Then restore homes the arm, reloads PhysX from authored USD, and republishes the MoveIt planning scene.

Plan-only / CI still uses mock hardware: `mtc_demo_headless.launch.py` (CycloneDDS localhost). Do not mix that launch with Isaac.

Install the hardware plugin: `sudo apt install ros-humble-topic-based-ros2-control`.

## Run (plan only)

```bash
# After a pod relaunch (only /workspace persists):
./scripts/setup/install_dependencies.sh

# 1) dependencies
./scripts/setup/check_dependencies.sh

# 2) build + unit tests + MTC plan (keep_alive_s=0, auto_execute=false)
./scripts/test/run_mtc_tf_plan_test.sh
```

Manual:

```bash
source /opt/ros/humble/setup.bash
source ros2_ws/install/setup.bash
ros2 launch lara5_moveit_config mtc_demo_headless.launch.py
ros2 launch xyz_motion chess_scene.launch.py use_cylinder_collision:=true planning_scene_only:=true
ros2 run xyz_motion publish_chess_occupancy -- ros2_ws/src/xyz_motion/config/examples/e2_to_e4.json
ros2 launch lara5_mtc mtc_chess_cylinders_pick_place.launch.py \
  occupancy_file:=.../e2_to_e4.json keep_alive_s:=0 auto_execute:=false
```

Success log: `Planning succeeded` and `Plan OK (keep_alive_s=0 — exiting)`.

## Real board

Set `z_is_piece_top:=true` and publish detected piece XYZ (base/world) on `/chess_occupancy`. Keep `board_a1/b1/a2` from calibration so the **normal** (approach direction) is correct. Empty place squares need no piece Z.
