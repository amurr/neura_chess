# 1. /_tmux

# articulation_orchestrator
to do:
- takes all objects from the PlanningScene
- retrieves the specified one
- retrieves its 3d pose, type (=name in dictionary)
- retireves specifications to pick and place it correctly from db
- injects this data as arguments into moveit_master.cpp


# 2. planning_scene_update
- adds CollisionObjects to PlanningScene of move_group through /planning_scene topic

# 3. moveit_sequence
- sends Targets to move_group through MoveGroupInterface




# 4. lara5_moveit , lara5_moveit_config
- srdf
- posting static objects of the scene (table, board) in the PlanningScene




# docker

xhost +local:docker
docker run --rm -it \
  --net=host \
  --ipc=host \
  -e DISPLAY \
  -e QT_X11_NO_MITSHM=1 \
  -v /home/artem/robotics:/ros2_ws:rw \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  rosh


docker ps -a

docker exec -it name_of_exect_container_running bash




## ros2

source /opt/ros/humble/setup.bash
source /ros2_ws/neura_chess/install/setup.bash
ros2 launch lara5_moveit_config rviz_moveit.launch.py

source /opt/ros/humble/setup.bash
source /ros2_ws/neura_chess/install/setup.bash
export PYTHONPATH=/ros2_ws/neura_chess/ros2_ws/src/orchestration:$PYTHONPATH
python3 -c "
from orchestration.master import params_from_json, run_mtc_pose_sequence
move = {'from': 'e2', 'to': 'e4', 'piece': 'pawn'}
for p in params_from_json(move):
    raise SystemExit(run_mtc_pose_sequence(**p))
"



master launch:
source /opt/ros/humble/setup.bash
source /ros2_ws/neura_chess/install/setup.bash
ros2 run orchestration master

run master.py without rebuild:
source /opt/ros/humble/setup.bash
source /ros2_ws/neura_chess/install/setup.bash
python3 -c "from orchestration.master import run_mtc_pose_sequence; raise SystemExit(run_mtc_pose_sequence(hover_pose='h1_hover_big'))"


direct launch file calling:
source /opt/ros/humble/setup.bash
source /ros2_ws/neura_chess/install/setup.bash
ros2 launch lara5_mtc mtc_pose_sequence.launch.py

ros2 launch lara5_mtc mtc_pose_sequence.launch.py \
  lower_distance:=0.055 \
  lift_distance:=0.055 \
  gripper_open_position:=0.2 \
  gripper_close_position:=-0.175




# launch files
generate_launch_description() is the entry point of the launch file. ROS 2 calls it when you run ros2 launch .... It must return a LaunchDescription — the list of things to start (nodes, included launches, env vars) and the launch arguments those things may use

# IK, chess board size
answer based on mathematical IK calculations: what is maximum size of chess board where the neura arm will be able to place EEF perpendicularly to all 64 squares?

[] increase the chess board size: more space between chess pieces



# mtc parameterizing
via launch file parameters
- x hover Pose
- n cm down/up by z-axis
- w gripper closing width




# neura_chess

Lara5 in MoveIt + RViz, with a chess board in the planning scene.

There is no Isaac Sim, no ros2_control, and no hardware. `fake_controllers` serves the two actions MoveIt expects and replays trajectories onto `/joint_states`, so Plan **and** Execute work on the model. Pass `fake_controllers:=false` for `joint_state_publisher_gui` sliders instead (nothing executes then).

```bash
source /opt/ros/humble/setup.bash
cd /ros2_ws/neura_chess          # or: cd /ros2_ws then source that overlay
colcon build
source install/setup.bash
ros2 launch lara5_moveit_config rviz_moveit.launch.py
```

That launch starts:

| Node | Role |
|------|------|
| `robot_state_publisher` | TF from URDF + `/joint_states` |
| `fake_controllers` | `arm_controller` / `gripper_controller` actions + `/joint_states` (default) |
| `joint_state_publisher_gui` | RViz joint sliders, `fake_controllers:=false` only |
| `static_virtual_joint_tfs` | `world` → `lara5_root_link` |
| `move_group` | MoveIt planning |
| `chess_scene_collisions` | Board + pieces as collision objects and markers |
| `rviz2` | RobotModel + MotionPlanning (`orient.rviz`) |

Named states `a1_hover`…`h8_hover` and `a1_grasp`…`h8_grasp` are in the SRDF. In RViz: MotionPlanning → Select Goal State.

Your node: `ros2 run lara5_moveit moveit_master` (empty — write it).

Sources live in `ros2_ws/src/`. Three packages:

```
orient.launch.py
 ├─ lara5_moveit_config     MoveIt config + this launch
 │    └─ lara5_description  URDF, meshes
 └─ lara5_moveit            chess_scene_collisions + board IK + moveit_master
```

---

## `lara5_description` — robot model

MoveIt does **not** load this package as `robot_description` by itself. `lara5_moveit_config/config/lara5.urdf.xacro` includes `lara5/urdf/lara5.urdf.xacro` from here.

| File | Role |
|------|------|
| `package.xml`, `CMakeLists.txt` | Installs the `lara5/` tree into the share directory |
| `lara5/urdf/lara5.urdf.xacro` | Entry xacro: macro + `world` → `lara5_root_link` |
| `lara5/urdf/lara5_macro.xacro` | Links, joints, visuals, collision, gripper |
| `lara5/urdf/lara5_kinematic_parameters_nominal.xacro` | Origins / DH |
| `lara5/urdf/lara5_dynamic_parameters_nominal.xacro` | Mass / inertia |
| `lara5/urdf/lara5_limits.xacro` | Joint position / velocity / effort limits |
| `lara5/urdf/so101_gripper.xacro` | Jaw on link6 (`lara5_gripper_finger_joint`) |
| `lara5/urdf/lara5.urdf` | Flattened snapshot of the xacro. `board_ik.py` parses this (no ROS). After xacro edits: `xacro lara5.urdf.xacro > lara5.urdf` |
| `lara5/urdf/README.txt` | Same chain, short |
| `lara5/meshes/*.stl` | Visual meshes (RViz) |
| `lara5/meshes/so101/*.stl` | Gripper body + jaw |
| `lara5/meshes/README.md`, `lara5/meshes/so101/README.md` | What the STL folders contain |
| `lara5/collision/Link*_body.stl` | Collision meshes used by the URDF |

---

## `lara5_moveit_config` — MoveIt + launch

`MoveItConfigsBuilder('lara5')` reads `config/` by convention.

| File | Role |
|------|------|
| `launch/orient.launch.py` | The only bringup you need |
| `launch/static_virtual_joint_tfs.launch.py` | Publishes the SRDF virtual joint as a static TF (included by orient) |
| `config/orient.rviz` | RViz layout: RobotModel, MotionPlanning, chess MarkerArrays |
| `config/lara5.urdf.xacro` | `robot_description`: includes `lara5_description` only |
| `config/lara5.srdf` | Groups (`arm`, `gripper`), collision matrix, named states (`stand`, `*_hover`, `*_grasp`, gripper `open`/`close`) |
| `config/kinematics.yaml` | KDL plugin for group `arm` |
| `config/joint_limits.yaml` | MoveIt velocity scaling (overrides / augments URDF) |
| `config/pilz_cartesian_limits.yaml` | Cartesian-path vel/acc (RViz “Use Cartesian Path”) |
| `config/moveit_controllers.yaml` | Controller names/action namespaces MoveIt executes through; served by `fake_controllers` |
| `package.xml`, `CMakeLists.txt` | Package metadata; installs `launch/` and `config/` |

---

## `lara5_moveit` — chess scene, IK fill, your node

| File | Role |
|------|------|
| `lara5_moveit/chess_scene_collisions.py` | **The chess node.** Board + pieces → `/planning_scene` and RViz markers. `ros2 run lara5_moveit chess_scene_collisions` |
| `chess_scene.yaml` | Board pose, square size, piece sizes (installed into `share/lara5_moveit/config/`) |
| `meshes/chess_pieces/collision_hulls/*.stl` | Convex-hull collision meshes per piece type |
| `lara5_moveit/fake_controllers.py` | **Fake controllers.** `follow_joint_trajectory_safe` + `gripper_cmd` action servers replaying onto `/joint_states`. `ros2 run lara5_moveit fake_controllers` |
| `lara5_moveit/moveit_master.py` | **Empty.** `ros2 run lara5_moveit moveit_master` |
| `lara5_moveit/board_ik.py` | FK/IK (Jacobian DLS, not MoveIt `/compute_ik`) + `square_xy()` |
| `lara5_moveit/teach_board.py` | `ros2 run lara5_moveit teach_board` — read `/joint_states`, `fill` other squares |
| `scripts/generate_hover_goals.py` | Taught h1 hover → 64 hovers → YAML + SRDF |
| `scripts/generate_grasp_goals.py` | Taught h1 hover→grasp tendency → 64 grasps → YAML + SRDF |
| `config/board_hover_joints.yaml` | Last generated hover joints |
| `config/board_grasp_joints.yaml` | Last generated grasp joints |
| `lara5_moveit/__init__.py` | Package marker |
| `package.xml`, `setup.py`, `setup.cfg`, `resource/lara5_moveit` | ament_python package |

Board XY used for hover IK matches `chess_scene.yaml`: `square_size=0.04`, `board_a1=[0.27,-0.16,0.02]`, `ranks_x_files_y`, `board_file_mirror=true`.

Lowering in RViz: start `e4_hover`, goal `e4_grasp`, **Use Cartesian Path** (do not only move j2/j5).

---

## Repo root

| File | Role |
|------|------|
| `README.md` | This map |
| `.gitignore` | `__pycache__` and colcon `build/` `install/` `log/` |

Build artifacts (`build/`, `install/`, `log/`) are generated; they are not source.
