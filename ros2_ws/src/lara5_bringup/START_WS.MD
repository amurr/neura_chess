# START_WS — staged startup of ros2_ws

## 0. Host (Ubuntu, not in the container)

```bash
xhost +local:
docker compose -f /home/artem/robotics/docker-compose.yml up -d
docker exec -it -e DISPLAY=$DISPLAY rosh bash        # one per terminal
```

## 1. Every terminal inside `rosh`

```bash
source /opt/ros/humble/setup.bash
source /ros2_ws/neura_chess/ros2_ws/install/setup.bash
export ROS_LOCALHOST_ONLY=1 QT_QPA_PLATFORM=xcb      # same env as bringup.launch.py sets
```

## 2. Build (once / after changes)

```bash
cd /ros2_ws/neura_chess/ros2_ws
pip3 install -r src/articulation_orchestrator/requirements.txt   # trimesh, once
colcon build
source install/setup.bash
```

## 3. Staged start — one terminal per stage, in this order

Stop `lara5_moveit_config rviz_moveit.launch.py` first.

### Stage 1 — description (robot_state_publisher, /robot_description, TF)

```bash
ros2 launch lara5_bringup description.launch.py
```

```bash
ros2 topic echo /robot_description --once | head -3
```

Model-only check, without stages 2–5:

```bash
ros2 launch lara5_bringup description.launch.py use_joint_state_publisher:=true
ros2 launch lara5_bringup rviz.launch.py
```

### Stage 2 — ros2_control (mock hardware, joint_state_broadcaster, arm + gripper controllers)

```bash
ros2 launch lara5_bringup control.launch.py
```

```bash
ros2 control list_controllers                    # 3 x active
ros2 topic hz /joint_states                      # ~100 Hz
ros2 action list | grep -E "follow|gripper"
```

Drive the controllers directly, no MoveIt:

```bash
ros2 action send_goal /arm_controller/follow_joint_trajectory control_msgs/action/FollowJointTrajectory \
  "{trajectory: {joint_names: [lara5_joint1,lara5_joint2,lara5_joint3,lara5_joint4,lara5_joint5,lara5_joint6],
    points: [{positions: [0.3,-0.3,0.6,0.0,0.4,0.0], time_from_start: {sec: 3}}]}}"
ros2 action send_goal /gripper_controller/gripper_cmd control_msgs/action/GripperCommand \
  "{command: {position: 1.0, max_effort: 0.0}}"
```

### Stage 3 — MoveIt (move_group)

```bash
ros2 launch lara5_bringup moveit.launch.py
```

```bash
ros2 action list | grep -E "move_action|execute_trajectory"
ros2 service list | grep get_planning_scene
```

### Stage 4 — RViz (optional)

```bash
ros2 launch lara5_bringup rviz.launch.py
```

### Stage 5 — application (chess scene + moveit_master; waits for stages 2+3)

```bash
ros2 launch lara5_bringup app.launch.py                         # small board, 32 pieces
ros2 launch lara5_bringup app.launch.py board:=big pieces:=false
ros2 launch lara5_bringup app.launch.py scene_demo:=true        # + planning_scene_updater demo
ros2 launch lara5_bringup app.launch.py orchestrator:=true      # + articulation_orchestrator demo
```

```bash
ros2 node list | grep -E "moveit_master|chess_scene"
ros2 action list | grep execute_sequence
```

Send a sequence to moveit_master (type: 0 pose, 1 arm named, 2 gripper named, 3 wait):

```bash
ros2 action send_goal /moveit_master/execute_sequence moveit_master/action/ExecuteSequence \
  "{steps: [{type: 1, named_target: e4_hover}, {type: 2, named_target: open},
            {type: 3, duration: 1.0}, {type: 2, named_target: close},
            {type: 1, named_target: stand}], velocity_scaling: 0.5}" --feedback
```

Run the app nodes by hand instead of via the launch file:

```bash
ros2 run articulation_orchestrator planning_scene_updater
ros2 run articulation_orchestrator articulation_orchestrator
ros2 service call /chess_scene_collisions/reset_scene std_srvs/srv/Trigger
```

## 4. All stages at once

```bash
ros2 launch lara5_bringup bringup.launch.py
ros2 launch lara5_bringup bringup.launch.py board:=big
ros2 launch lara5_bringup bringup.launch.py orchestrator:=true
ros2 launch lara5_bringup bringup.launch.py use_rviz:=false
ros2 launch lara5_bringup bringup.launch.py launch_app:=false                                # stages 1–4
ros2 launch lara5_bringup bringup.launch.py use_fake_hardware:=false launch_control:=false   # external driver
ros2 launch lara5_bringup bringup.launch.py use_sim_time:=true launch_control:=false         # simulator
ros2 launch lara5_bringup bringup.launch.py --show-args
```

## 5. Stop

```bash
# Ctrl-C in each terminal, last stage first
ros2 node list                                   # empty when everything is down
```
