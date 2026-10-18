# Local docker container to run ChessBoard.action pipeline in RViz (instead of running in Isaac Sim described in README)
Local container is the same as the Pod (Pod is a docker container too), but without Isaac Sim:
- arm_controller and gripper_controller execute goals with mock_components/GenericSystem (use_fake_hardware:=true, hardware:=mock, the defaults); RViz shows the result
- /home/artem/r on the host is mounted as /ros2_ws in the container, so the workspace is /ros2_ws/neura_chess/ros2_ws (on the Pod: /workspace/neura_chess/ros2_ws)

image: rosh (ROS 2 Humble + MoveIt 2, built from neura_chess/Dockerfile)

prerequisites:
- ubuntu 22.04 host with X display
- `rosh` docker image
- no other lara5 stack on the ROS graph (compose `rosh` container, another `docker run`): `--ipc=host` containers see each other through Fast DDS shared memory


## system check
docker images | grep rosh
echo $DISPLAY


# docker container
1. from pc terminal: allow the container to draw on the host X display, run container

```
xhost +local:docker
docker run --rm -it \
  --name rosh \
  --net=host \
  --ipc=host \
  -e DISPLAY="$DISPLAY" \
  -e XAUTHORITY=/tmp/.Xauthority \
  -v "${XAUTHORITY:-$HOME/.Xauthority}":/tmp/.Xauthority:ro \
  -e QT_QPA_PLATFORM=xcb \
  -e XDG_RUNTIME_DIR=/tmp/runtime-root \
  --device /dev/dri \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v /home/artem/r:/ros2_ws:rw \
  rosh
```

second terminal into the same container (optional)
```
docker exec -it -e DISPLAY="$DISPLAY" rosh bash
```


## run ChessBoard.action pipeline
- move_group sends FollowJointTrajectory.action goals to the arm_controller and gripper_controller, which are configured for executing goals with RViz mock_components/GenericSystem (on the Pod they execute goals on the Isaac Sim robot model)

5. ros2 stack with tmux (once; leave it running)

```
cd /ros2_ws/neura_chess/_tmux
./tmux_start_ws.sh
```
  options: ./tmux_start_ws.sh board:=big   |   ./tmux_start_ws.sh all   |   --force

Panes start in order, each waits for the one before:

| pane | stage | starts when |
|---|---|---|
| 1 | `description.launch.py`: robot_state_publisher, /robot_description, TF | immediately |
| 2 | `control.launch.py`: ros2_control_node (mock), joint_state_broadcaster, arm_controller, gripper_controller | `/robot_description` has a publisher |
| 3 | `moveit.launch.py`: move_group | 3 controllers active |
| 4 | `rviz.launch.py`: RViz with the MotionPlanning panel | `/get_planning_scene` is up |
| 5 | `app.launch.py`: chess_scene_collisions (board + 32 pieces in the PlanningScene), moveit_master (/moveit_master/execute_sequence) | `/get_planning_scene` is up |
| 0 | cli shell, ROS env already sourced | immediately |

This replaces Pod steps 8 and 9 (`launch_world.sh` + `launch_moveit_isaac.sh`). Without stage 5, chess_board_server waits forever for moveit_master.

Wait until RViz shows the robot, the board and the 32 pieces.

6. check the stack, from pane 0 (cli):
```
ros2 control list_controllers      # joint_state_broadcaster, arm_controller, gripper_controller: active
ros2 topic hz /joint_states        # ~100 Hz
ros2 action list                   # /arm_controller/follow_joint_trajectory, /gripper_controller/gripper_cmd, /move_action, /execute_trajectory, /moveit_master/execute_sequence
ros2 node list                     # /move_group, /controller_manager, /moveit_master, /chess_scene_collisions
```

7. run ChessBoardServer Node, from pane 0 (cli) or a `docker exec` terminal:

```
source /opt/ros/humble/setup.bash
source /ros2_ws/neura_chess/ros2_ws/install/setup.bash
export ROS_LOCALHOST_ONLY=1 QT_QPA_PLATFORM=xcb

ros2 run articulation_orchestrator chess_board_server
```
  options: big board: --ros-args -p hover_pose_format:={square}_hover_big

It waits for moveit_master + move_group, syncs the 32 pieces from initial_fen, starts /chess_board.

actions pipeline is described in /ros2_ws/neura_chess/ros2_ws/src/README.md

8. send a test move goal to ChessBoard action server Node, from another terminal (tmux: `C-b "` splits the cli pane; or `docker exec`)
- change_status: passive is for arm to move a piece; active is for updating move_group PlanningScene (when opponent makes a move)

```
source /opt/ros/humble/setup.bash
source /ros2_ws/neura_chess/ros2_ws/install/setup.bash
export ROS_LOCALHOST_ONLY=1

#ros2 action list | grep chess_board # make sure the server is up

ros2 action send_goal --feedback /chess_board chess_interfaces/action/ChessBoard \
  "{change_status: passive, piece_type: pawn, to_pick: e2, to_place: e4}"
```
In RViz: stand -> mid_move -> e2_hover -> open -> down -> close -> attach -> up -> e4_hover -> down -> open -> detach -> up -> stand; the attached pawn moves with the gripper.

9. restore PlanningScene
```
ros2 action send_goal /chess_board chess_interfaces/action/ChessBoard \
  "{change_status: active, fen: 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'}"
```
or reset the whole chess scene:
```
ros2 service call /chess_scene_collisions/reset_scene std_srvs/srv/Trigger
```

10. stop the stack
```
/ros2_ws/neura_chess/_tmux/tmux_start_ws.sh stop
```
Ctrl-C every stage, last first, close the session. Detach `C-b d`, reattach `tmux attach -t lara5`. Exiting the container shell (`--rm`) ends everything, tmux included.


## logging joint_state in world_frame to define better moveit targets
```
source /opt/ros/humble/setup.bash
source /ros2_ws/neura_chess/ros2_ws/install/setup.bash
export ROS_LOCALHOST_ONLY=1
ros2 run articulation_orchestrator execution_logger --ros-args \
  -p out_dir:=/ros2_ws/neura_chess/ros2_ws/src/articulation_orchestrator/execution_logs
# options: --ros-args -p out_dir:=/path -p rate_hz:=50
# no Isaac locally, so there are no Isaac piece poses to log
```


# Differences from the Pod

| | Pod | local container |
|---|---|---|
| workspace | /workspace/neura_chess/ros2_ws | /ros2_ws/neura_chess/ros2_ws |
| robot | Isaac Sim (`hardware:=isaac`, topic_based_ros2_control, ros2_controllers_isaac.yaml) | mock_components/GenericSystem (`hardware:=mock`, default) |
| start | `launch_world.sh` + `launch_moveit_isaac.sh` (bringup.launch.py in one process) | `tmux_start_ws.sh` (same launch files, one pane per stage) |
| ROS env | `ROS_LOCALHOST_ONLY=0` (Kit runs without it) | `ROS_LOCALHOST_ONLY=1` (set by `rosh_env.sh`) |
| display | XRDP inside SSH tunnel | host X display through /tmp/.X11-unix |

Mock hardware reaches every target exactly, so a move that works here can still miss the piece in Isaac (see TO DO in README.md).
