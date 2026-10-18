# RunPod.io GPU-powered Pods to run Isaac Sim
Pod is a docker container with mounted S3 bucket
- 4090 gpu, 24 gb vram, 64 cpu cores, 64 gb ram
- 100 gb SSD (not persistent files storage): ros2 installation, builds
- 100 gb S3 bucket: isaac sim, workspaces files, assets

pod image: runpod/base:1.0.3-ubuntu2204

prerequisites:
- isaac sim 6.0.1 installation in S3 bucket
  /workspace/isaacsim
- ubuntu 22.04


## system check
cat /etc/os-release
nvidia-smi


# SSH tunnel to Pod
1. Runpod web panel: 'Connect to your Pod using a terminal directly in your browser'

2. add ssh key
cat ~/.ssh/id_ed25519.pub

echo 'ssh-ed25519 THE_KEY' >> ~/.ssh/authorized_keys

## XRDP connection inside SSH tunnel
3. bash ./workspace/neura_chess/scripts/pod_scripts/start_xrdp.sh

4. from pc terminal: 
ssh -N -L 13389:127.0.0.1:3389 -p <real port> root@<real IP>

5. from Remmina client: 
127.0.0.1:13389

  user     root
  pass     xrdp
  session  xvnc (select)

## vscode remote (optional)
6. from pc terminal:
micro /home/USER/.ssh/config
  redact port, ip:
```
Host runpod
    HostName 157.157.221.29
    Port 33193
    User root
    IdentityFile ~/.ssh/id_ed25519
    ServerAliveInterval 30
```
  ctrl s, ctrl q

code --remote ssh-remote+runpod /workspace/

# on Pod
## install ros2 humble
7. from pod terminal:
./neura_chess/scripts/ros2h_installation.sh


## Isaac Sim

8. from pod terminal:
start Isaac Sim with the chess scene (once; leave it running, timeline playing):
```
./neura_chess/scripts/launch/launch_world.sh
```

Wait until `/tmp/neura_chess_pieces.ready` exists and `/isaac_joint_states` is publishing.

Alt+Left to orbit camera
Right+D/A to move camera


## run ChessBoard.action pipeline 
- move_group sends FollowJointTrajectory.action goals to the arm_controller and gripper_controller configured for executing goals on Isaac Sim robot model (during local development arm_controller and gripper_controller executed goal with RViz mock_components/GenericSystem)

9. MoveIt + Isaac hardware (once; leave it running)

```bash
cd neura_chess
colcon build

source /opt/ros/humble/setup.bash
source /workspace/neura_chess/ros2_ws/install/setup.bash
export ROS_DOMAIN_ID=0 RMW_IMPLEMENTATION=rmw_fastrtps_cpp ROS_LOCALHOST_ONLY=0
./scripts/launch/launch_moveit_isaac.sh
```
This is `move_group`, `arm_controller`, and the `/isaac_joint_states` → `/joint_states` relay. Without it, planning can succeed and then you get `Failed to acquire current PlanningScene` or `Goal was aborted`.

10. run ChessBoardServer Node:

```
source /opt/ros/humble/setup.bash
source /workspace/neura_chess/ros2_ws/install/setup.bash
export ROS_DOMAIN_ID=0 RMW_IMPLEMENTATION=rmw_fastrtps_cpp ROS_LOCALHOST_ONLY=0
ros2 run articulation_orchestrator chess_board_server
```

actions pipeline is described in /workspace/neura_chess/ros2_ws/src/README.md

11. send a test move goal to ChessBoard action server Node
- change_status: passive is for arm to move a piece; active is for updating move_group PlanningScene (when opponent makes a move)

ros2 action list | grep chess_board # make sure the server is up

```
source /opt/ros/humble/setup.bash
source /workspace/neura_chess/ros2_ws/install/setup.bash
export ROS_DOMAIN_ID=0 RMW_IMPLEMENTATION=rmw_fastrtps_cpp ROS_LOCALHOST_ONLY=0

ros2 action send_goal --feedback /chess_board chess_interfaces/action/ChessBoard \
  "{change_status: passive, piece_type: pawn, to_pick: e2, to_place: e4}"
```

12. restore PlanningScene
```
ros2 action send_goal /chess_board chess_interfaces/action/ChessBoard \
  "{change_status: active, fen: 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'}"
```

## logging joint_state in world_frame to define better moveit targets
```
source /opt/ros/humble/setup.bash
source /workspace/neura_chess/ros2_ws/install/setup.bash
export ROS_DOMAIN_ID=0 RMW_IMPLEMENTATION=rmw_fastrtps_cpp ROS_LOCALHOST_ONLY=0
ros2 run articulation_orchestrator execution_logger --ros-args \
  -p out_dir:=/workspace/neura_chess/ros2_ws/src/articulation_orchestrator/execution_logs
```
options: --ros-args -p out_dir:=/path -p rate_hz:=50 -p isaac_pieces_hz:=10


# Controlling robot model in Isaac Sim scene

```
client ──FollowJointTrajectory──▶ /arm_controller/follow_joint_trajectory   (JTC, 100 Hz)
                                  /gripper_controller/gripper_cmd          (GripperActionController)
JTC ─▶ topic_based_ros2_control ─▶ /isaac_hw_joint_commands ─▶ pad ─▶ /isaac_joint_commands ─▶ Isaac
Isaac ─▶ /isaac_joint_states ─▶ topic_based_ros2_control (state feedback, tolerances, goal result)
```

arm_controller and gripper_controller are names used in ros2_controllers.yaml and moveit_controllers.yaml in lara5_moveit_config package

topic_based_ros2_control is a ROS 2 package for integrating the ros2_control with any system that uses topics to command the robot and publish its state.


pad step exists because Isaac's OmniGraph ROS2SubscribeJointState rejects messages that contain only positions


# Gripper control
- calibration is needed for controlling Lerobot gripper through ROS1 Node on Neura controller block
  - something is already in xyz_motion package; some notes are in creative robotics notion page

/workspace/neura_chess/ros2_ws/src/lara5_moveit_config/config/ros2_controllers.yaml
```
gripper_controller:
  ros__parameters:
    joint: lara5_gripper_finger_joint
    # Isaac jaw can oscillate at the URDF limit; don't block the whole MTC execute.
    allow_stalling: true
    stall_timeout: 1.0
    stall_velocity_threshold: 100.0
    goal_tolerance: 0.2
```

# Lerobot Gripper TCP

MoveIt plans for `lara5_tcp`: the tip of the static (fixed) SO-101 finger, on its inner gripping
face. It is a fixed link under the gripper mount `lara5_gripper`
([so101_gripper.xacro](ros2_ws/src/lara5_description/lara5/urdf/so101_gripper.xacro)), at
(−0.0079, 0, −0.1044) measured from `wrist_roll_follower_so101_v1.stl`, with the same axes:
+x from the static to the moving finger, +z back up the fingers. A piece pressed against the
static finger has its centre at (r, 0, 0) in this frame.

```
            lara5_gripper (wrist mount)
                  │  −z (finger direction)
                  ▼
   static finger │       │ moving finger (closes toward −x)
   inner face    │  (●)  │
                 ●───► +x
              lara5_tcp     piece centre at +r
```

- SRDF: the `arm` chain ends at `lara5_tcp`, and the end effector hangs from it. `moveit_master`
  uses it for `ARM_POSE`, `ARM_CARTESIAN` and `ATTACH`; the links allowed to touch a held piece
  are everything below `lara5_gripper` (parameter `gripper_root_link`).
- `ARM_CARTESIAN` takes `frame: "tcp"` to move along the TCP axes (the sideways shift onto a
  piece), otherwise the offset is in the planning frame.
- Hover poses (`{square}_hover` in the SRDF, `lara5_moveit/scripts/generate_hover_goals*.py`):
  TCP straight above the square centre at z = 0.150, TCP x axis at −45° in the world
  (`JAW_AXIS_YAW`, the fingers then point along a board diagonal, where the next piece is
  furthest away), plus a `discard` pose beside the board for captured pieces.
  `{square}_hover_alt`: the same with the x axis at −60° (`JAW_AXIS_YAW_ALT`), used when the
  wrist would hit a neighbour at −45° (e.g. the e2 pawn next to the king in the start position).


# Pick and place: where the numbers come from

All per-piece values are in
[objects_dictionary.yaml](ros2_ws/src/articulation_orchestrator/assets/objects_dictionary.yaml),
generated by `ros2_ws/src/lara5_moveit/scripts/compute_piece_grasps.py` from the Isaac pieces
(OpenChessSet, scaled to 40 mm squares, one PhysX convex hull per mesh) and the gripper collision
shapes in the URDF. The same script writes the MoveIt piece collision hulls
(`lara5_moveit/meshes/chess_pieces/collision_hulls`). Rerun it after changing the pieces, the
gripper geometry or the hover height (it needs `pxr`: `pip install --target /tmp/usdlib usd-core`,
then `PYTHONPATH=/tmp/usdlib:$PYTHONPATH python3 scripts/compute_piece_grasps.py`).

Per piece type:
- `tip_height`: fingertip height above the board at the grasp: knight 16 mm (not on its
  asymmetric head, which tips over), the rest 32 mm (king 35.6 mm, its height), above the
  centre of mass. The pawn's PhysX body hull is a cone: held on it (~22 mm) the closing jaw
  tips it over, at 32 mm (neck) it holds. `higher`: the same values at higher grips (4 mm steps) up to 35.6 mm,
  where the wrist above the fingers clears a king on a neighbouring square. The orchestrator
  checks the wrist boxes (`wrist` in the defaults) against the neighbouring pieces at the pick
  and the place square, for the default and then the alternative jaw direction, and takes the
  lowest level that clears both squares (one grip for the whole transfer).
- `grasp_offset`: piece centre − TCP along x when the piece touches the static finger. The pick
  shifts the TCP by −(grasp_offset + finger_clearance), the place by −place_offset.
- `place_offset`: corrected from where the pieces really landed in Isaac:
  `python3 ros2_ws/src/articulation_orchestrator/scripts/calibrate_place_offsets.py <log dirs>`
  reads the execution logs (`execution_logger` running) of moves made with the current
  dictionary, takes the final error of the pieces that stood upright on their target square
  and adds the median per type to the offset used. Run moves again afterwards to check.
- `gripper_open/close/release_position`: jaw angles from the hull geometry. The close position
  is ~0.3 rad past the predicted contact (at most the joint limit, −0.1745): the soft jaw
  drive in Isaac then squeezes with up to ~1.2 N·m and the gripper controller reports success
  on the stall.

Sequence (`ArticulationOrchestrator.transfer_steps`): hover → open → shift → down → close →
attach → up → target hover → shift → down (+1 mm) → release → detach → back off 2 mm → up → home.


# Isaac Sim settings that matter for grasping

In [neura_chess_world.py](neura_chess_world.py):
- Board: `BOARD_CENTER_X = 0.27 + 4*SQUARE` so that `board_a1` in
  [chess_scene.yaml](ros2_ws/src/lara5_moveit/chess_scene.yaml) is the a1 corner on the board
  top, as in the PlanningScene. Back rank h→a along +y, so kings stand on e, queens on d.
- Robot: self-collisions off (the jaw hub overlaps link6's convex hull). Arm drives
  2000 N·m/deg; the jaw is a soft spring (0.07 N·m/deg, max 1.5 N·m) that closes in ~0.3 s.
  The gripper body (static finger) has a high-friction pad (1.0); the moving jaw keeps the
  default friction.
- Gripper collisions are boxes fitted to the finger and wrist (URDF): the convex hull of the
  wrist mesh closes the gap between the fingers.
- Pieces: torsional patch friction (a gripped piece does not swing about the finger axis),
  capped depenetration velocity (released pieces are not shot away).

ROS side ([lara5_bringup](ros2_ws/src/lara5_bringup)):
- `isaac_state_velocity` relays `/isaac_joint_states` to `/isaac_hw_joint_states` with
  velocities from the position change. Isaac's own joint velocity reads up to ~3 rad/s for a jaw
  pressed still against a piece, so the gripper controller would never see the stall.
- `ros2_controllers_isaac.yaml`: arm goal tolerance 0.005 rad on joints 1–3 (0.015 on the wrist),
  so a pick or place step only starts once the arm really arrived.
- The first goal right after startup can abort on `mid_move` with CONTROL_FAILED (the Kit
  command subscriber is not connected yet). Send it again.


# TO DO next

- understand ArticulationOrchestrator and MoveItMaster responsibilities
- understand where to redact Targets

- the points that TCP achieves during MoveItMaster execution of ExecuteSequence.action are incorrect: they must be where the chess pieces optimal grasping areas are.
- define those areas based on position of chess pieces in world_frame in isaac sim scene
- compare these points with positions the TCP reaches when time of logged joint position = time of move_group target executed log
- redact Moveit targets, achieve working sequence



- paste:
# Expected terminal logs when pipeline (activated by ChessBoard.action) is running
ros2 topic list
ros2 action list
ros2 node list
ros2 control list_controllers