# Poses library
/home/artem/robotics/neura_chess/ros2_ws/src/lara5_moveit_config/config/lara5.srdf stores memorized joint-space positions of the arms


# Hardware is abstraction
/home/artem/robotics/neura_chess/ros2_ws/src/lara5_bringup/config/moveit_controllers.yaml


# lara5 neura_chess pipeline: When one chess move runs, `moveit_master.cpp` does this:

- **Startup:** it opens `MoveGroupInterface` for the `arm` and `gripper` groups, collects the gripper links (`lara5_gripper` and every link below it, e.g. the jaw), connects to `/get_planning_scene`, and offers the action `/moveit_master/execute_sequence`.
- **Goal arrives:** it accepts one goal at a time (others are rejected while busy) and runs `execute()` in a separate thread.
- **`execute()`:** it sets the speed scaling (default 0.2), clears its record of scene changes, and runs the `MotionStep`s in order, sending feedback with `current_step` each time.
- **`runStep()` for each step type:**
  - `ARM_NAMED` (stand, mid_move, e2_hover, …): sets the named target, then plans and executes through move_group.
  - `ARM_CARTESIAN` (down/up): reads the current gripper pose, adds the offset, plans a straight path with `computeCartesianPath` and fails if less than 100% of it is possible. It then re-times the path to the speed scaling and executes it.
  - `GRIPPER_JOINT` (0.25 open, close value): sets the jaw joint angle, then plans and executes.
  - `ALLOW_COLLISION`: fetches the current collision-allowance table, allows or removes contact between the piece and the gripper links plus the board square, then applies it.
  - `ATTACH` / `DETACH`: moves the piece from the world onto the gripper link (touch allowed for the gripper links), or puts it back into the world where it was released.
  - `WAIT` sleeps. `ARM_POSE` and `GRIPPER_NAMED` still work as before.
- **Step fails:** it stops and returns `failed_step` plus an error text. It then undoes its scene changes: detaches the attached piece and removes the collision allowances it added.
- **Cancel request:** it stops the arm and gripper, the step loop exits, and the same rollback runs.
- **End:** the result is `success` with `"done"`, or an abort or cancel with the failing step, and it's free for the next goal.
