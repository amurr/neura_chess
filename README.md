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
1. connect through web terminal
2. add ssh key
cat ~/.ssh/id_ed25519.pub

echo 'ssh-ed25519 THE_KEY' >> ~/.ssh/authorized_keys

## XRDP connection inside SSH tunnel
3. ./workspace/lara/pod_scripts/start_xrdp.sh
4. from pc terminal: 
ssh -N -L 13389:127.0.0.1:3389 -p <real port> root@<real IP>

5. from Remmina client: 
127.0.0.1:13389

  user     root
  pass     xrdp
  session  xvnc (select)

## vscode remote
6. from pc terminal:
micro /home/USER/.ssh/config
code --remote ssh-remote+runpod /workspace/

## install ros2 humble
7. from pod terminal:
/workspace/neura_chess/scripts/ros2h_installation.sh


## Isaac Sim

8. from pod terminal:
start Isaac Sim with the chess scene (once; leave it running, timeline playing)
./scripts/launch/launch_world.sh

Wait until `/tmp/neura_chess_pieces.ready` exists and `/isaac_joint_states` is publishing.

Alt+Left to orbit camera
Right+D/A to move camera


## run ChessBoard.action pipeline 
- move_group sends FollowJointTrajectory.action goals to the arm_controller and gripper_controller configured for executing goals on Isaac Sim robot model (during local development arm_controller and gripper_controller executed goal with RViz mock_components/GenericSystem)

9. MoveIt + Isaac hardware (once; leave it running)

```bash
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

```
source /opt/ros/humble/setup.bash
source /workspace/neura_chess/ros2_ws/install/setup.bash
export ROS_DOMAIN_ID=0 RMW_IMPLEMENTATION=rmw_fastrtps_cpp ROS_LOCALHOST_ONLY=0

#ros2 action list | grep chess_board # make sure the server is up

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
# options: --ros-args -p out_dir:=/path -p rate_hz:=50 -p isaac_pieces_hz:=10
```


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
Lerobot gripper TCP is near the static finger

TCP to use is about (−0.008 + r_piece, 0, −0.095) in lara5_gripper, where r_piece is the radius of the piece where the fingers grip it. For a pawn neck of radius about 5–6 mm, that's x ≈ −0.003.

```
            lara5_gripper (wrist mount, origin)
                  │
                  │  −z  (finger direction)
                  ▼
   fixed finger │     │ moving finger  ← closes toward −x
   inner face   │ (●) │
   x = −0.008   │  ↑  │
                 centre of piece = −0.008 + r   at z ≈ −0.095

```


# TO DO

[] start with step 1, change the board position and height in `neura_chess_world.py`; Isaac would then need a restart to pick it up.

`ArticulationOrchestrator` controls the up/down distances and the gripper positions. Where the gripper sits over each square comes from the SRDF hover poses, and those only work if the Isaac board sits where the PlanningScene says it does. It doesn't yet.

From most to least important:

**1. Put the Isaac board where the PlanningScene board is.** [chess_scene.yaml](ros2_ws/src/lara5_moveit/chess_scene.yaml) sets `board_a1: [0.27, -0.16, 0.02]` as the **corner** of a1, so the a1 square's centre is at x = 0.29 and the board top is at z = 0.02. [neura_chess_world.py](neura_chess_world.py) treats (0.27, −0.16) as the **centre** of a1 (`BOARD_CENTER_X = 0.27 + 3.5*SQUARE`). Two consequences:
- **x:** the Isaac board is 2 cm (half a square) closer to the robot. That's the 0.310 vs 0.330 seen in the logs.
- **z:** the Isaac board top appears to be at about 0.01, against 0.02 in the PlanningScene. The Isaac pawn's origin is at z = 0.0105.

The fix belongs in the Isaac world, since the hover poses were taught against `chess_scene.yaml`: `BOARD_CENTER_X = 0.27 + 4*SQUARE` (0.43) and a board top at 0.02. Without this, no orchestrator setting will make the grasps work.

**2. Make the arm reach its targets in Isaac.** The tolerance and `goal_time` changes in `ros2_controllers_isaac.yaml` are already done. Better still: stiffer or less damped joint drives in `neura_chess_world.py`.

**3. Hover poses over each square:** the `{square}_hover` entries in [lara5.srdf](ros2_ws/src/lara5_moveit_config/config/lara5.srdf), which `teach_board` generates. These decide x and y over the square. Only re-teach or shift them if step 2 in `steps.csv` still shows the fingers missing the piece sideways once 1 and 2 are fixed. Remember that `lara5_gripper` is the wrist mount: the grip point is about 9.5 cm below it, offset toward the fixed finger.

**4. Orchestrator parameters**, in [objects_dictionary.yaml](ros2_ws/src/articulation_orchestrator/assets/objects_dictionary.yaml). This is the part you tune per piece type, and it's re-read on every move, so no rebuild is needed:
- `lower_distance` / `lift_distance`: how far to go down from the hover. The grip point should end up about halfway up the piece's neck. Check the "down" row in `steps.csv`: the `lara5_gripper` z minus about 0.095 should equal the board top plus about half the piece's height.
- `gripper_open_position`: open enough to clear the piece. At 0.25 the fingertip gap is about 34 mm.
- `gripper_close_position`: at 0.0 there's still a gap of about 16 mm, wider than a pawn neck (the pawn diameter in `chess_scene.yaml` is 18 mm, and the neck is narrower). Close tighter, for example −0.1, and let the gripper's stall detection report success when it hits the piece.
- `home_pose`, `mid_pose` and `discard_pose` are ROS parameters of the orchestrator, but they're only names of SRDF poses, so you don't need to change them.

**5. Piece sizes in the PlanningScene:** `piece_dims` in `chess_scene.yaml` should match the scaled Isaac pieces. If they don't, MoveIt's collision checks during "down" won't match what happens in Isaac.


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