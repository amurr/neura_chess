# Sourced inside the rosh container by every lara5 tmux pane (START_WS.MD section 1).
# Also used as --rcfile for the interactive shells the panes end in.

if [[ $- == *i* ]] && [ -f ~/.bashrc ]; then
  source ~/.bashrc
fi

source /opt/ros/humble/setup.bash
source /ros2_ws/neura_chess/ros2_ws/install/setup.bash
export ROS_LOCALHOST_ONLY=1 QT_QPA_PLATFORM=xcb   # same env as bringup.launch.py sets

# START_WS.MD check / drive commands, one line each. Up arrow in any pane recalls them.
LARA5_COMMANDS=(
  'ros2 control list_controllers'
  'ros2 topic hz /joint_states'
  'ros2 action list'
  'ros2 node list'
  'ros2 action send_goal /arm_controller/follow_joint_trajectory control_msgs/action/FollowJointTrajectory "{trajectory: {joint_names: [lara5_joint1,lara5_joint2,lara5_joint3,lara5_joint4,lara5_joint5,lara5_joint6], points: [{positions: [0.3,-0.3,0.6,0.0,0.4,0.0], time_from_start: {sec: 3}}]}}"'
  'ros2 action send_goal /gripper_controller/gripper_cmd control_msgs/action/GripperCommand "{command: {position: 1.0, max_effort: 0.0}}"'
  'ros2 run articulation_orchestrator planning_scene_updater'
  'ros2 run articulation_orchestrator articulation_orchestrator'
  'ros2 service call /chess_scene_collisions/reset_scene std_srvs/srv/Trigger'
  'ros2 action send_goal /moveit_master/execute_sequence moveit_master/action/ExecuteSequence "{steps: [{type: 1, named_target: e4_hover}, {type: 2, named_target: open}, {type: 3, duration: 1.0}, {type: 2, named_target: close}, {type: 1, named_target: stand}], velocity_scaling: 0.5}" --feedback'
)

lara5_help() {
  printf '%s\n' "${LARA5_COMMANDS[@]}"
}

# Bash loads ~/.bash_history after the rcfile, so seed the history on the first
# prompt instead. LARA5_LAST_CMD (set by stage.sh) goes last: Up = rerun the stage.
_lara5_seed_history() {
  local c
  for c in "${LARA5_COMMANDS[@]}"; do history -s "$c"; done
  [ -n "$LARA5_LAST_CMD" ] && history -s "$LARA5_LAST_CMD"
  PROMPT_COMMAND=$_LARA5_PROMPT_COMMAND
}

if [[ $- == *i* ]]; then
  HISTCONTROL=ignoredups:erasedups
  _LARA5_PROMPT_COMMAND=$PROMPT_COMMAND
  PROMPT_COMMAND=_lara5_seed_history
fi
