#!/usr/bin/env bash
# Starts the full chess pipeline in one tmux session, one pane per step:
#   1. world      - install ROS 2 Humble, then launch the Isaac world
#   2. moveit     - colcon build, then launch MoveIt for Isaac
#   3. server     - chess_board action server        (waits for build)
#   4. goal       - send a test move e2 -> e4         (waits for server)
#   5. logger     - execution_logger, logs positions  (waits for build)
# Usage: bash pod_tmux_auto.sh   (re-running replaces the old session)
set -euo pipefail

SESSION=chess
ROOT=/workspace/neura_chess
WS=$ROOT/ros2_ws
ENV="source /opt/ros/humble/setup.bash && source $WS/install/setup.bash && \
export ROS_DOMAIN_ID=0 RMW_IMPLEMENTATION=rmw_fastrtps_cpp ROS_LOCALHOST_ONLY=0"
WAIT_BUILD="tmux wait-for ${SESSION}_built"   # released by pane 2 after colcon build

run() { tmux send-keys -t "$SESSION:0.$1" "$2" C-m; }

tmux kill-session -t "$SESSION" 2>/dev/null || true
tmux new-session -d -s "$SESSION" -c /workspace
for _ in 1 2 3 4; do tmux split-window -t "$SESSION:0" -c "$ROOT"; tmux select-layout -t "$SESSION:0" tiled; done

# 1. Install ROS 2, then launch the world in the same pane
run 0 "bash $ROOT/scripts/ros2h_installation.sh && bash $ROOT/scripts/launch/launch_world.sh"

# 2. Build the workspace, signal the other panes, launch MoveIt
run 1 "source /opt/ros/humble/setup.bash && (cd $WS && colcon build) && tmux wait-for -S ${SESSION}_built && $ENV && ./scripts/launch/launch_moveit_isaac.sh"

# 3. Chess board action server
run 2 "$WAIT_BUILD && $ENV && ros2 run articulation_orchestrator chess_board_server"

# 4. Test goal: move pawn e2 -> e4, once the server is up
run 3 "$WAIT_BUILD && $ENV && until ros2 action list | grep -q /chess_board; do sleep 2; done && \
ros2 action send_goal --feedback /chess_board chess_interfaces/action/ChessBoard \
'{change_status: passive, piece_type: pawn, to_pick: e2, to_place: e4}'"

# 5. Log executed positions
run 4 "$WAIT_BUILD && $ENV && ros2 run articulation_orchestrator execution_logger --ros-args \
-p out_dir:=$WS/src/articulation_orchestrator/execution_logs"

tmux attach -t "$SESSION"
