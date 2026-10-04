#!/usr/bin/env bash
# Start the lara5 stack in tmux. Run this on the Ubuntu 22 host, NOT inside the container.
set -e

SESSION=lara5
COMPOSE=/home/artem/robotics/docker-compose.yml
SETUP='source /opt/ros/humble/setup.bash; source /ros2_ws/neura_chess/install/setup.bash'

# Let the container draw on the host X display. The X socket is bind-mounted
# by compose (/tmp/.X11-unix), so "local:" is the connection type to allow.
xhost +local: >/dev/null

# The ros container shares the tailscale container's network namespace. If
# tailscale ever restarted, ros is left in the old dead namespace with no DNS
# and no network. Recreating ros re-joins the live one. It is just a
# sleep-infinity container, so this is cheap and always safe.
docker compose -f "$COMPOSE" up -d
docker compose -f "$COMPOSE" up -d --force-recreate ros

# A shell in the rosh container with ROS sourced and the display passed through.
in_rosh() {
  echo "docker exec -it -e DISPLAY=$DISPLAY rosh bash -c '$SETUP; $1'"
}

tmux kill-session -t $SESSION 2>/dev/null || true

# pane 0: move_group + rviz + chess scene (all from this one launch file)
tmux new-session -d -s $SESSION -n main \
  "$(in_rosh 'ros2 launch lara5_moveit_config rviz_moveit.launch.py')"

# pane 1: MTC, left for you to start once rviz is up
tmux split-window -h -t $SESSION \
  "$(in_rosh 'echo \"run: ros2 launch lara5_mtc mtc_pose_sequence.launch.py\"; exec bash')"

# pane 2: spare shell for ros2 topic//node poking
tmux split-window -v -t $SESSION "$(in_rosh 'exec bash')"

tmux select-layout -t $SESSION tiled
tmux select-pane -t $SESSION.1
tmux attach -t $SESSION
