# _tmux

`./start.sh` — brings up the containers and opens the lara5 stack in a tmux session.

Run it **on the host**, not inside `rosh`.

## Panes

| pane | what |
|---|---|
| 0 | `rviz_moveit.launch.py` — move_group, rviz2, robot_state_publisher, fake_controllers, chess scene |
| 1 | idle shell, prints the MTC command to run |
| 2 | spare shell |

`ros2 launch lara5_moveit_config rviz_moveit.launch.py` starts both MoveIt and RViz;
they are not separate panes.

Useful args: `board:=big`, `fake_controllers:=false`.

## Notes

- X11 goes through the bind-mounted `/tmp/.X11-unix` socket, so the script runs
  `xhost +local:`. Nothing is exposed over TCP.
- The script force-recreates the `ros` service every time. It shares the tailscale
  container's network namespace, and if tailscale restarts, `ros` is stranded in
  the dead namespace — no DNS, no network, `apt-get` fails to resolve anything.
- Sourced install space is `/ros2_ws/neura_chess/install` (the top-level one).
  There are also stale install trees at `ros2_ws/install` and `ros2_ws/src/install`;
  the top-level one is the only one with all packages including `lara5_mtc`.
- Detach `C-b d`, reattach `tmux attach -t lara5`, kill `tmux kill-session -t lara5`.
