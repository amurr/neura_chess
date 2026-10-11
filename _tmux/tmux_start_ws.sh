#!/usr/bin/env bash
# Start the lara5 stack in tmux from INSIDE the rosh container, following
# ros2_ws/src/lara5_bringup/START_WS.MD. Container started on the host with:
#
#   xhost +local:docker
#   docker run --rm -it --net=host --ipc=host -e DISPLAY -e QT_X11_NO_MITSHM=1 \
#     -v /home/artem/robotics:/ros2_ws:rw -v /tmp/.X11-unix:/tmp/.X11-unix:rw rosh
#
# then, in the container:
#
#   /ros2_ws/neura_chess/_tmux/tmux_start_ws.sh [staged] [launch args]   stages 1-5, one pane each, in order (default)
#   /ros2_ws/neura_chess/_tmux/tmux_start_ws.sh all [launch args]        bringup.launch.py in one pane
#   /ros2_ws/neura_chess/_tmux/tmux_start_ws.sh model                    URDF check: joint_state_publisher_gui + RViz
#   /ros2_ws/neura_chess/_tmux/tmux_start_ws.sh build [colcon args]      colcon build, no tmux
#   /ros2_ws/neura_chess/_tmux/tmux_start_ws.sh stop                     Ctrl-C every stage, last first, close the session
#
# Launch args go to every launch file, e.g. tmux_start_ws.sh board:=big orchestrator:=true
# --force (after the mode) skips the check for another lara5 stack on the ROS graph.
set -e

SESSION=lara5
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
STAGE=$HERE/stage.sh

# Terminal size for the detached session (defaults to 80x24, too small for six panes).
read -r ROWS COLS < <(stty size 2>/dev/null </dev/tty || echo 50 200)

mode=staged
if [ $# -gt 0 ] && [[ $1 != *:=* ]] && [ "$1" != --force ]; then
  mode=$1
  shift
fi
FORCE=
if [ "$1" = --force ]; then
  FORCE=1
  shift
fi

# The rosh image has no tmux, and --rm drops anything installed at runtime,
# so this runs once per container.
ensure_tmux() {
  command -v tmux >/dev/null && return 0
  echo "installing tmux ..."
  apt-get update -qq && apt-get install -y -qq --no-install-recommends tmux >/dev/null
}

# Refuse to start a second stack on the same ROS graph (this container, another
# docker exec shell, or the compose rosh container: --ipc=host links them).
check_graph() {
  [ -n "$FORCE" ] && return 0
  echo "checking the ROS graph for a running lara5 stack ..."
  bash "$STAGE" graph-free
}

# new_pane <stage number> <stage.sh args...>
# The stage number orders the shutdown in stop(); 0 = never Ctrl-C'd.
new_pane() {
  local n=$1 cmd id
  shift
  cmd=$(printf 'bash %q' "$STAGE"; printf ' %q' "$@")
  if tmux has-session -t "$SESSION" 2>/dev/null; then
    id=$(tmux split-window -t "$SESSION:lara5" -P -F '#{pane_id}' "$cmd")
  else
    id=$(tmux new-session -d -s "$SESSION" -n lara5 -x "$COLS" -y "$ROWS" \
      -P -F '#{pane_id}' "$cmd")
    tmux set-option -t "$SESSION" remain-on-exit on       # keep errors visible
    tmux set-option -t "$SESSION" pane-border-status top
    tmux set-option -t "$SESSION" pane-border-format ' #{@label} '
    tmux set-option -t "$SESSION" mouse on                # click panes, scroll output
  fi
  tmux set-option -p -t "$id" @stage "$n"
  tmux set-option -p -t "$id" @label "$n $1"
  tmux select-layout -t "$SESSION:lara5" tiled >/dev/null
  echo "$id"
}

stop() {
  command -v tmux >/dev/null || return 0
  tmux has-session -t "$SESSION" 2>/dev/null || return 0
  echo "stopping $SESSION, last stage first ..."
  tmux list-panes -s -t "$SESSION" -F '#{@stage} #{pane_id}' | sort -rn |
    while read -r n id; do
      [ "$n" -gt 0 ] || continue
      tmux send-keys -t "$id" C-c
      sleep 2
    done
  tmux kill-session -t "$SESSION"
}

attach() {
  tmux select-pane -t "$1"
  if [ -n "$TMUX" ]; then
    tmux switch-client -t "$SESSION"
  else
    tmux attach -t "$SESSION"
  fi
}

start() {
  stop
  check_graph
  ensure_tmux
  [ -n "$DISPLAY" ] || echo "warning: DISPLAY is not set, RViz will not open (docker run -e DISPLAY)" >&2
}

case $mode in
  staged)
    start
    new_pane 1 description "$@" >/dev/null
    new_pane 2 control "$@" >/dev/null
    new_pane 3 moveit "$@" >/dev/null
    new_pane 4 rviz "$@" >/dev/null
    new_pane 5 app "$@" >/dev/null
    attach "$(new_pane 0 cli)"
    ;;
  all)
    start
    new_pane 1 all "$@" >/dev/null
    attach "$(new_pane 0 cli)"
    ;;
  model)
    start
    new_pane 1 model-description "$@" >/dev/null
    new_pane 2 model-rviz "$@" >/dev/null
    attach "$(new_pane 0 cli)"
    ;;
  build)
    bash "$STAGE" build "$@"
    ;;
  stop)
    stop
    ;;
  *)
    sed -n '2,18p' "$0"
    exit 1
    ;;
esac
