# MTC Chess Cylinder Pick-Place — Optimization Plan

Knowledge base for `lara5_mtc_chess_cylinders_pick_place.cpp`.

## Problem

End effector approached the board **parallel** (horizontal) instead of **perpendicular** (top-down grasp). RViz stage tree was slow due to heavy planning scene and bulk collision stages.

## MTC goal representation (reference)

| Stage type | Goal input | Space | C++ type |
|---|---|---|---|
| `MoveTo` | SRDF name or world pose | Joint / Cartesian | `std::string` or `geometry_msgs::msg::PoseStamped` |
| `Connect` | *(none)* | Config / joint | OMPL via `GroupPlannerVector` |
| `MoveRelative` | axis + distance | Cartesian | `geometry_msgs::msg::Vector3Stamped` |
| `ModifyPlanningScene` | allow/attach/detach | Scene diff | object/link names |

Planned result: `Solution` → `SubTrajectory` → `robot_trajectory::RobotTrajectory` → `RobotState` waypoints.

## Root cause (orientation)

Top-down was only enforced inside `Pick`/`Place` via `setIKFrame`. **`Connect`** and **`pre_pick`** moved in joint space with **no orientation constraint**.

## Final tree (16 stages — verified planning + execution)

```
current state
→ open gripper
→ allow collision (gripper, piece_<src>)
→ allow gripper on board_sq_<src>
→ allow gripper on board_sq_<tgt>
→ pick hover          [MoveTo PoseStamped, top-down RPY]
→ approach pick       [MoveRelative world −Z]
→ close gripper
→ attach piece
→ lift from pick      [MoveRelative world +Z]
→ place hover         [MoveTo PoseStamped, top-down RPY]
→ descend place       [MoveRelative world −Z]
→ allow release collisions
→ detach piece
→ retreat after place [MoveRelative world +Z]
→ open gripper after place
→ move to stand
```

**Removed vs baseline:** both `Connect` stages, `Pick`/`Place` containers, seed `pre_pick`, bulk 64-square / 64-piece / 31-piece collision loops.

## Snapshots

| File | Status |
|---|---|
| `v0_baseline.cpp` | Pick/Place + Connect + bulk collision — plans OK |
| `v1_compute_ik_no_connect.cpp` | ComputeIK attempt — **init failed** (interface mismatch) |
| `v2_flat_topdown_tree.cpp` | Flat tree draft |
| `v3_flat_topdown_planning_ok.cpp` | **Final — planning + execution OK** |

## Test command (WSL)

```bash
bash /mnt/d/dev/superbloom/lara_superbloom-lucas-le_robot_gripper/lara_superbloom-lucas-le_robot_gripper/scripts/wsl-mtc-cpp-test.sh
```

## Insights log

### Phase 0 — baseline (v0)

- Headless test: **Planning succeeded** with old Pick/Place tree (~8.7 s OMPL).
- Node stayed alive after plan → test script timed out; fixed with `rclcpp::shutdown()` when `auto_execute=false`.

### Phase 1 — ComputeIK hovers (v1, failed init)

- `GeneratePose` + `ComputeIK` after `MoveTo` seed caused **interface mismatch** (`← →` vs `→ →`).
- MTC tutorial wraps ComputeIK after **`Connect`**, not directly after propagators.
- **Fix:** use `MoveTo(PoseStamped)` for hovers instead of ComputeIK wrapper.

### Phase 1b — Pick container after hover (failed init)

- `Pick`/`SimpleGrasp` internal ComputeIK still failed when `Connect` removed.
- **Fix:** drop Pick/Place containers entirely; use flat sequence from `lara5_chess_pick_place.py`.

### Phase 2 — flat top-down tree (v2 → v3)

- **`pick hover` / `place hover`**: `MoveTo` with `top_down_orientation` `(roll=0, pitch=π/2, yaw=0)` in `world` frame — enforces perpendicular EEF before approach.
- **`approach pick` Cartesian failed in RViz** (5 mm of 80 mm, ~6% fraction): vertical descent hits other pieces on full `chess_scene`. Headless test passed due to luckier arm config / timing.
- **Fix:** replace `approach pick` / `descend place` Cartesian with **`MoveTo pick grasp` / `MoveTo place grasp`** (OMPL, top-down pose at grasp height). Re-add **`allow arm on other pieces`** for transit.
- **`open gripper after place`**: failed at board height (self-collision). **Fix:** order `detach → retreat → open gripper` (open at safe height).
- **Minimal collision:** 3 `ModifyPlanningScene` stages (piece + 2 board squares) vs 3×64 loops — faster RViz introspection.

### Phase 3 — verification

- `auto_execute=false`: **Planning succeeded (1 solution)** — TEST_OK (headless)
- `auto_execute=true` in headless: planning OK, execution aborts (error 99999) — use `mtc_demo.launch.py` + RViz Execute for motion
- Uses `publishSolution(front())` instead of `publishAllSolutions`.

## Top-down RPY tuning

If jaw still looks parallel in RViz, calibrate `kTopDownRoll/Pitch/Yaw` against actual `lara5_gripper` frame (adapter joints: `rpy="0 1.57 0"` + `rpy="1.57 0 π"`). Candidates from Python script:

- `(0, π/2, 0)` — default
- `(0, π/2, ±π/2)`
- `(π, 0, 0)`

## Optional next steps

- Single `board` collision mesh instead of 64 `board_sq_*` in chess_scene (scene-side).
- RPY fallback `Alternatives` stage if hover IK fails on other squares.
- Slim `mtc_debug.rviz` (disable duplicate PlanningScene / MarkerArray during stage scrub).
