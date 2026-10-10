#!/usr/bin/env bash
# Start the lara5 stack in tmux, following ros2_ws/src/lara5_bringup/START_WS.MD.
# Run this on the Ubuntu 22 host, NOT inside the container.
#
#   ./start.sh [staged] [launch args]   stages 1-5, one pane each, started in order (default)
#   ./start.sh all [launch args]        bringup.launch.py in one pane
#   ./start.sh model                    URDF check: joint_state_publisher_gui + RViz
#   ./start.sh build [colcon args]      colcon build inside rosh, no tmux
#   ./start.sh stop                     Ctrl-C every stage, last first, close the session
#
# Launch args go to every launch file, e.g. ./start.sh board:=big orchestrator:=true
# --force (after the mode) skips the check for another lara5 stack on the ROS graph.
set -e

SESSION=lara5
COMPOSE=/home/artem/robotics/docker-compose.yml
# This directory as seen from inside rosh (/home/artem/robotics -> /ros2_ws).
STAGE=/ros2_ws/neura_chess/_tmux/stage.sh

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

containers_up() {
  # Let the container draw on the host X display. The X socket is bind-mounted
  # by compose (/tmp/.X11-unix), so "local:" is the connection type to allow.
  xhost +local: >/dev/null || echo "xhost failed: RViz will not open (no X display?)" >&2

  # The ros container shares the tailscale container's network namespace. If
  # tailscale ever restarted, ros is left in the old dead namespace with no DNS
  # and no network. Recreating ros re-joins the live one. It is just a
  # sleep-infinity container, so this is cheap and safe (it also kills any
  # ROS processes left over from an earlier run).
  docker compose -f "$COMPOSE" up -d
  docker compose -f "$COMPOSE" up -d --force-recreate ros

  # A stack in a `docker run --ipc=host` container is still visible from here.
  if [ -z "$FORCE" ]; then
    echo "checking the ROS graph for a running lara5 stack ..."
    docker exec rosh bash "$STAGE" graph-free
  fi
}

# Command for a pane: stage.sh in the rosh container, display passed through.
rosh_cmd() {
  printf 'docker exec -it -e DISPLAY=%q rosh bash %q' "$DISPLAY" "$STAGE"
  printf ' %q' "$@"
}

# new_pane <stage number> <stage.sh args...>
# The stage number orders the shutdown in stop(); 0 = never Ctrl-C'd.
new_pane() {
  local n=$1 id
  shift
  if tmux has-session -t "$SESSION" 2>/dev/null; then
    id=$(tmux split-window -t "$SESSION:lara5" -P -F '#{pane_id}' "$(rosh_cmd "$@")")
  else
    id=$(tmux new-session -d -s "$SESSION" -n lara5 -x "$COLS" -y "$ROWS" \
      -P -F '#{pane_id}' "$(rosh_cmd "$@")")
    tmux set-option -t "$SESSION" remain-on-exit on       # keep docker exec errors visible
    tmux set-option -t "$SESSION" pane-border-status top
    tmux set-option -t "$SESSION" pane-border-format ' #{@label} '
  fi
  tmux set-option -p -t "$id" @stage "$n"
  tmux set-option -p -t "$id" @label "$n $1"
  tmux select-layout -t "$SESSION:lara5" tiled >/dev/null
  echo "$id"
}

stop() {
  tmux has-session -t "$SESSION" 2>/dev/null || return 0
  echo "stopping $SESSION, last stage first ..."
  tmux list-panes -s -t "$SESSION" -F '#{@stage} #{pane_id}' | sort -rn |
    while read -r n id; do
      [ "$n" -gt 0 ] || continue
      tmux send-keys -t "$id" C-c
      sleep 2
    done
  # docker exec leaves the container-side shell running when its pane is killed,
  # so end every shell first.
  tmux list-panes -s -t "$SESSION" -F '#{pane_id}' |
    while read -r id; do tmux send-keys -t "$id" C-u exit Enter; done
  sleep 1
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

case $mode in
  staged)
    stop
    containers_up
    new_pane 1 description "$@" >/dev/null
    new_pane 2 control "$@" >/dev/null
    new_pane 3 moveit "$@" >/dev/null
    new_pane 4 rviz "$@" >/dev/null
    new_pane 5 app "$@" >/dev/null
    attach "$(new_pane 0 cli)"
    ;;
  all)
    stop
    containers_up
    new_pane 1 all "$@" >/dev/null
    attach "$(new_pane 0 cli)"
    ;;
  model)
    stop
    containers_up
    new_pane 1 model-description "$@" >/dev/null
    new_pane 2 model-rviz "$@" >/dev/null
    attach "$(new_pane 0 cli)"
    ;;
  build)
    # No --force-recreate: a running stack keeps running while you build.
    xhost +local: >/dev/null 2>&1 || true
    docker compose -f "$COMPOSE" up -d
    docker exec -it rosh bash "$STAGE" build "$@"
    ;;
  stop)
    stop
    ;;
  *)
    sed -n '2,13p' "$0"
    exit 1
    ;;
esac
