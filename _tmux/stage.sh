#!/usr/bin/env bash
# Runs INSIDE the rosh container, one tmux pane per call (started by start.sh).
#
#   stage.sh <stage> [launch args...]
#
# stages (START_WS.MD sections 2-4):
#   description control moveit rviz app   staged start, each waits for the one before
#   all                                   bringup.launch.py
#   model-description model-rviz          URDF check: joint_state_publisher_gui + RViz
#   cli                                   shell only, check commands in history
#   build                                 colcon build [colcon args...]
#   graph-free                            exit 1 if another lara5 stack is on the ROS graph
#
# After the launch file exits (Ctrl-C), the pane stays as an interactive shell;
# Up arrow gives the same launch command again.

HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
WS=/ros2_ws/neura_chess/ros2_ws

stage=$1
shift
args=("$@")

if [ "$stage" = build ]; then
  # Underlay only: sourcing the workspace's own install space before building it
  # makes colcon warn about overriding packages.
  source /opt/ros/humble/setup.bash
  cd "$WS" || exit 1
  python3 -c 'import trimesh' 2>/dev/null || pip3 install -r src/articulation_orchestrator/requirements.txt
  colcon build "${args[@]}"
  exit $?
fi

source "$HERE/rosh_env.sh"

# Exit 1 if another lara5 stack is already on this ROS graph. Containers started
# with --ipc=host see each other through Fast DDS shared memory even in different
# network namespaces (compose rosh + docker run --net=host), and two stacks fight
# over /joint_states, /controller_manager and the planning scene.
if [ "$stage" = graph-free ]; then
  found=$(ros2 node list --no-daemon --spin-time 3 2>/dev/null |
    grep -xE '/(move_group|controller_manager|robot_state_publisher|moveit_master|chess_scene_collisions)')
  [ -z "$found" ] && exit 0
  echo "another lara5 stack is already running on this ROS graph:" >&2
  echo "$found" | sed 's/^/  /' >&2
  echo "stop it first (host: _tmux/start.sh stop, container: tmux_start_ws.sh stop)" >&2
  echo "or start anyway with --force." >&2
  exit 1
fi

# Ctrl-C while waiting cancels the stage. Ctrl-C while the launch runs stops the
# launch (it gets the default SIGINT handling) but not this script.
CANCEL=
trap 'CANCEL=1' INT

# ---------- readiness checks ----------
robot_description_up() {
  ros2 topic info /robot_description 2>/dev/null | grep -q 'Publisher count: [1-9]'
}

controllers_up() {
  local list c
  list=$(timeout 5 ros2 control list_controllers 2>/dev/null | sed 's/\x1b\[[0-9;]*m//g')
  for c in joint_state_broadcaster arm_controller gripper_controller; do
    grep -Eq "^$c +.* active\s*$" <<<"$list" || return 1
  done
}

move_group_up() {
  ros2 service list 2>/dev/null | grep -qx /get_planning_scene
}

wait_for() {  # wait_for <description> <check function>
  echo "[lara5] waiting for $1 ..."
  until "$2"; do
    [ -n "$CANCEL" ] && { echo "[lara5] canceled"; return 1; }
    sleep 1
  done
  echo "[lara5] $1 is up"
}

# ---------- stages ----------
cmd=()
case $stage in
  description)
    cmd=(ros2 launch lara5_bringup description.launch.py) ;;
  control)
    wait_for "stage 1: /robot_description" robot_description_up &&
      cmd=(ros2 launch lara5_bringup control.launch.py) ;;
  moveit)
    wait_for "stage 2: joint_state_broadcaster, arm_controller, gripper_controller" controllers_up &&
      cmd=(ros2 launch lara5_bringup moveit.launch.py) ;;
  rviz)
    wait_for "stage 3: move_group" move_group_up &&
      cmd=(ros2 launch lara5_bringup rviz.launch.py) ;;
  app)
    wait_for "stage 3: move_group" move_group_up &&
      cmd=(ros2 launch lara5_bringup app.launch.py) ;;
  all)
    cmd=(ros2 launch lara5_bringup bringup.launch.py) ;;
  model-description)
    cmd=(ros2 launch lara5_bringup description.launch.py use_joint_state_publisher:=true) ;;
  model-rviz)
    wait_for "/robot_description" robot_description_up &&
      cmd=(ros2 launch lara5_bringup rviz.launch.py) ;;
  cli)
    lara5_help ;;
  *)
    echo "unknown stage '$stage'" >&2 ;;
esac

if [ ${#cmd[@]} -gt 0 ]; then
  cmd+=("${args[@]}")
  export LARA5_LAST_CMD="${cmd[*]}"
  echo "[lara5] $LARA5_LAST_CMD"
  "${cmd[@]}"
fi

trap - INT
exec bash --rcfile "$HERE/rosh_env.sh" -i
