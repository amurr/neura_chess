# _tmux

`./start.sh` — brings up the containers and runs the lara5 stack in a tmux session,
following [START_WS.MD](../ros2_ws/src/lara5_bringup/START_WS.MD).

Run it **on the host**, not inside `rosh`.

```bash
./start.sh                           # staged: stages 1-5, one pane each, in order
./start.sh board:=big orchestrator:=true   # launch args go to every stage
./start.sh all                       # bringup.launch.py in one pane
./start.sh model                     # URDF check: joint_state_publisher_gui + RViz
./start.sh build                     # colcon build inside rosh (no tmux)
./start.sh stop                      # Ctrl-C every stage, last first, close the session
```

## From inside the container: `tmux_start_ws.sh`

Same modes and panes, but tmux runs inside the container. For a container started with:

```bash
xhost +local:docker
docker run --rm -it --net=host --ipc=host -e DISPLAY -e QT_X11_NO_MITSHM=1 \
  -v /home/artem/robotics:/ros2_ws:rw -v /tmp/.X11-unix:/tmp/.X11-unix:rw rosh
```

```bash
/ros2_ws/neura_chess/_tmux/tmux_start_ws.sh                 # staged
/ros2_ws/neura_chess/_tmux/tmux_start_ws.sh all board:=big
/ros2_ws/neura_chess/_tmux/tmux_start_ws.sh stop
```

- Installs tmux on first use (the image has none, and `--rm` drops it again on exit).
- Mouse is on: click a pane to focus it, scroll to read its output.
- Exiting the container shell (`--rm`) ends the whole stack.

## One stack at a time

Both scripts refuse to start while another lara5 stack (`/move_group`, `/controller_manager`, ...)
is on the ROS graph. Containers with `--ipc=host` see each other through Fast DDS shared memory
even in different networks, so the compose `rosh` stack and a `docker run --net=host` stack
collide: two `/joint_states`, two controller managers, two planning-scene writers.
Stop the other one first, or pass `--force` after the mode (`./start.sh staged --force`).

## Panes (staged)

| pane | stage | starts when |
|---|---|---|
| 1 | `description.launch.py` | immediately |
| 2 | `control.launch.py` | `/robot_description` has a publisher |
| 3 | `moveit.launch.py` | joint_state_broadcaster, arm_controller, gripper_controller active |
| 4 | `rviz.launch.py` | `/get_planning_scene` (move_group) is up |
| 5 | `app.launch.py` | `/get_planning_scene` (move_group) is up |
| 0 | cli shell | immediately, prints the check commands |

- Ctrl-C in a pane that is still waiting cancels that stage.
- When a launch exits, its pane stays as a shell. **Up arrow** = the same launch command again.
- In every pane, the START_WS check commands (list_controllers, direct FJT / gripper goals,
  moveit_master sequence, reset_scene, ...) are in the shell history; `lara5_help` lists them.

## Files

| file | runs | role |
|---|---|---|
| `start.sh` | host | containers, X access, tmux layout, stop |
| `stage.sh` | rosh | one stage per pane: wait for the previous stage, launch, leave a shell |
| `tmux_start_ws.sh` | rosh | same as `start.sh`, but tmux runs inside the container |
| `stage.sh` `graph-free` | rosh | exit 1 if another lara5 stack is on the ROS graph |
| `rosh_env.sh` | rosh | ROS env (START_WS section 1) + history of check commands |

## Notes

- X11 goes through the bind-mounted `/tmp/.X11-unix` socket, so the script runs
  `xhost +local:`. Nothing is exposed over TCP.
- `staged`, `all` and `model` force-recreate the `ros` service. It shares the tailscale
  container's network namespace, and if tailscale restarts, `ros` is stranded in
  the dead namespace — no DNS, no network. It also kills any ROS processes left over
  from an earlier run. `build` does not recreate.
- Sourced install space is `/ros2_ws/neura_chess/ros2_ws/install`.
- Detach `C-b d`, reattach `tmux attach -t lara5`, stop `./start.sh stop`.
