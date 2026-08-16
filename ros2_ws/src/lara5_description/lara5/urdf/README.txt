# lara5

- lara5_macro.xacro : macro that contains structure of robot
- lara5_limits : contains information about joint limits, joint velocity limits and joint effort lara5_limits
- lara5_kinematic_parameters_nomial : contains the nominal kinematic parameters 
- lara5_dynamic_parameters_nominal : contains the nominal dynamic parameters

exchange these files after calibration and recreate description files (urdf, sdf, ...)

to create the urdf :

xacro lara5.urdf.xacro > lara5.urdf




# Moveit Setup Assistant
URDF is loaded — work through the **left panel top to bottom**, then generate the package.

## 1. Self-Collisions
- Click **Generate Collision Matrix**
- Disable pairs that are **always touching** (adjacent links)
- Keep pairs that could collide during motion
- **Save**

## 2. Virtual Joints
- **Add Virtual Joint**
- Parent: `world` → Child: `lara5_root_link` (or your base link name)
- Type: **fixed**
- **Save**

## 3. Planning Groups
- **Add Group** → name: `arm`
- Kinematics: **KDL** (default is fine)
- Add the **6 arm joints**: `lara5_joint1` … `lara5_joint6` (use “Add Kin. Chain” from base to tool if offered)
- **Save**

The URDF mounts an SO-101 follower gripper (meshes from so101_follower.urdf.xacro) on link6.
Run once: `bash src/lara5_description/scripts/fetch_so101_gripper_meshes.sh`
Joint `lara5_gripper_finger_joint` is the SO-101 revolute jaw (closed=-0.174533 rad, open=1.74533 rad).
Use `gripper_joint_bridge` + `/command_gripper` for open/close.

## 4. Robot Poses
Add poses you already use (from teach pendant / `poses.py`), e.g.:
- `home` — safe idle
- `stand`
- `ready` — pre-grasp

Enter joint values in **radians** if the UI expects radians (teach pendant often shows degrees — convert).

- **Save**

## 5. End Effectors
- If there is a tool link (e.g. `lara5_gripper` or `lara5_flange`): add end effector on that link, group `arm`
- Otherwise **skip**
- **Save**

## 6. Passive Joints
- Leave empty unless the URDF has passive joints
- **Save**

## 7. ROS 2 Control
For **planning + RViz** (real arm still uses NeuraPy `move_joints`):

- Add controller: **FollowJointTrajectory**
- Joints: all 6 arm joints
- **Save**

You will wire real execution to `move_joints` later; this step is for MoveIt’s planner and demo.

## 8. MoveIt Controllers
- Map group **`arm`** → the **FollowJointTrajectory** controller
- **Save**

## 9. Perception
- **Skip** for now
- **Save**

## 10. Launch Files (last)
- **Configuration Package Path**:  
  `/ros2_ws/src/lara5_moveit_config`  
  (create that name; must be under `src/`)
- Enable **Generate Launch Files**
- **Generate Package** → **Finish**

---

## After MSA (in Docker)

```bash
cd /ros2_ws
colcon build --packages-select lara5_moveit_config
source install/setup.bash
ros2 launch lara5_moveit_config demo.launch.py
```

(XLaunch running for RViz.)

---

## Lara-specific reminders

| Topic | Your setup |
|--------|------------|
| Joint states | `/lara/joint_states` — may need a relay to `/joint_states` with URDF names |
| Real motion | `move_joints` / NeuraPy, not `ros2_control` yet |
| Gripper | `gripper_node` + `robot_gripper.py`, not MoveIt (for now) |

---

**Order:** Self-Collisions → Virtual Joint → Planning Group `arm` → Poses → (End Effector) → ROS 2 Control → Controllers → **Generate** under `/ros2_ws/src/lara5_moveit_config`.

If a step shows red errors, note the message (often joint name mismatch) and we can fix that step.