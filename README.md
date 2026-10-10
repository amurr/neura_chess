# docker container starting

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


# lara5 neura_chess pipeline
- is run with tmux started inside the docker container

## startup (inside the container: /ros2_ws/neura_chess/_tmux/tmux_start_ws.sh [board:=big] [use_fake_hardware:=false])
1. description: robot_state_publisher publishes /robot_description + TF; use_fake_hardware:=true (default) puts mock_components/GenericSystem into the URDF as the ros2_control hardware
2. control: ros2_control_node + joint_state_broadcaster, arm_controller (FollowJointTrajectory), gripper_controller (GripperCommand); mock: echoes the commands back as /joint_states; real: drives the motors (no real LARA5 hardware plugin exists yet)
3. moveit: move_group loads URDF + SRDF (stand, mid_move, {square}_hover, open/close) and serves /move_action, /execute_trajectory, /compute_cartesian_path, /get_planning_scene, /apply_planning_scene
4. rviz: RViz with the MotionPlanning panel
5. app: chess_scene_collisions adds the board (64 board_sq_*) + 32 pieces (piece_<square>) to the PlanningScene; moveit_master starts /moveit_master/execute_sequence
6. by hand in the cli pane: ros2 run articulation_orchestrator chess_board_server -> waits for moveit_master + move_group, syncs the 32 pieces from initial_fen, starts /chess_board

## PIPELINE: receiving chess_interfaces/action/ChessBoard on /chess_board (from the CV / Stockfish node or the CLI)
1. chess_board_server: one goal at a time; target board = goal fen (or the board + to_pick -> to_place)
2. change_status active (move already happened on the real board): PlanningSceneUpdater makes the PlanningScene pieces equal to the target board through /apply_planning_scene; done
3. change_status passive (robot moves): checks piece_type against its board, splits the move into transfers (captured pieces -> discard first, then moves; castling = 2 transfers)
4. per transfer, ArticulationOrchestrator builds the MotionSteps (objects_dictionary.yaml: lower_distance, lift_distance, gripper positions per piece type) and sends them to /moveit_master/execute_sequence:
   stand -> mid_move -> src_hover -> open -> allow collision piece/gripper -> down -> close -> attach -> up -> dst_hover -> down -> open -> detach -> up -> stand
5. moveit_master runs the steps through MoveGroupInterface: move_group plans, the trajectories go to arm_controller / gripper_controller (mock or real), the attached piece moves with the gripper in the PlanningScene
6. after each transfer chess_board_server updates its board and the PlanningScene (piece_<src> removed, piece_<dst> added at the square centre)
7. result: success, message, fen of the board now held; on failure moveit_master undoes its scene changes and chess_board_server asks for an active goal with the real board's FEN




# ros2_ws components and roles

## ArticulationOrchestrator
- builds a hard-coded sequence of MotionSteps (arm pose / arm named state / gripper named state / wait)
- outputs it + velocity_scaling to moveit_master as goal moveit_master/action/ExecuteSequence (MotionStep[] steps) on action /moveit_master/execute_sequence
- takes the result (success, failed_step, message) from /moveit_master/execute_sequence and logs it
to do:
- takes all objects from the PlanningScene (moveit_msgs/srv/GetPlanningScene, service /get_planning_scene)
- retrieves the specified one
- retrieves its 3d pose, type (=name in dictionary)
- retireves specifications to pick and place it correctly from db
- injects this data as MotionSteps into moveit_master (moveit_master/action/ExecuteSequence, action /moveit_master/execute_sequence)


## planning_scene_update, planning_scene_updater (articulation_orchestrator)
- planning_scene_update: once on startup adds CollisionObjects (chess_board.obj + pawn.stl on the board top) to PlanningScene of move_group through /planning_scene topic (moveit_msgs/msg/PlanningScene, is_diff, transient_local)
- planning_scene_updater: adds / moves / removes CollisionObjects (box, cylinder, mesh) in PlanningScene of move_group through /apply_planning_scene service (moveit_msgs/srv/ApplyPlanningScene), returns only after move_group applied the diff; main() is a demo (add board + pawn, move pawn, remove pawn)

## moveit_master
- takes MotionStep[] + velocity_scaling as goal moveit_master/action/ExecuteSequence on action server /moveit_master/execute_sequence (one goal at a time, others rejected), outputs feedback current_step and result success / failed_step / message
- sends Targets (pose / SRDF named state) of groups arm, gripper to move_group through MoveGroupInterface: plan via action /move_action (moveit_msgs/action/MoveGroup), execute via action /execute_trajectory (moveit_msgs/action/ExecuteTrajectory)


## chess_scene_collisions, fake_controllers, teach_board, moveit_master (lara5_moveit), lara5_moveit_config
- srdf (lara5_moveit_config): groups arm, gripper; named states stand, a1_hover…h8_hover, a1_grasp…h8_grasp, gripper open / close
- chess_scene_collisions (executables chess_scene_collisions = small board, chess_scene_big = big board): posting static objects of the scene (board + 32 pieces, no table) in the PlanningScene through /planning_scene topic (moveit_msgs/msg/PlanningScene); outputs RViz markers on /chess_board_markers, /chess_piece_markers (visualization_msgs/msg/MarkerArray); takes /chess_occupancy (std_msgs/msg/String, JSON) to move / remove pieces; service ~/reset_scene (std_srvs/srv/Trigger)
- fake_controllers: takes trajectories from move_group on action servers /arm_controller/follow_joint_trajectory_safe (control_msgs/action/FollowJointTrajectory), /gripper_controller/gripper_cmd (control_msgs/action/GripperCommand); outputs replayed joints on /joint_states (sensor_msgs/msg/JointState)
- teach_board: takes /joint_states (sensor_msgs/msg/JointState), saves the taught hover, fills hover joints for all 64 squares, writes them to YAML
- moveit_master (lara5_moveit): empty placeholder, only prints a message


