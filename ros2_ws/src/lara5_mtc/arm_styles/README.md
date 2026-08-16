# Lara5 arm style library

Named **configuration families** for MTC and LLM task control. Styles point at SRDF `group_state` entries; they do not duplicate the full joint-space solution set for every board square.

## Layout

| File | Purpose |
|------|---------|
| `catalog.yaml` | Style ids, SRDF mapping, semantics, joint summaries |
| `selection_rules.yaml` | Aliases, region hints, retry order, LLM read/write fields |
| `schema/task_request.schema.json` | JSON Schema for high-level task requests |
| `examples/*.json` | Sample LLM outputs |

## Usage

**LLM / task builder (write):** pick `arm_style` + chess squares + approach params — see `examples/e2_to_e4_default.json`.

**Planner / MTC (today):** set ROS param `chess_seed_pose` to the style’s `srdf_state` (e.g. `pre_pick` for `pre_pick_over_board`). C++ loader from this catalog is not implemented yet.

**Debug (read only):** joint values per stage in `log/solution_latest.json` — do not feed back as goals unless adding a new SRDF state.

## Adding a style

1. Add `group_state` to `lara5_moveit_config/config/lara5.srdf`.
2. Add entry under `styles:` in `catalog.yaml`.
3. Optionally update `selection_rules.yaml` and remove from `planned_styles`.

## Install path

After `colcon build`:

```
install/lara5_mtc/share/lara5_mtc/arm_styles/
```
