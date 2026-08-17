#!/usr/bin/env python3
"""Restore Isaac chess board/pieces/joints to the authored start (no Kit relaunch).

Kit must be running a world that wrote /tmp/neura_chess_restore.ready (SceneRestore).
SceneRestore rewrites *local* ChessSet xform ops and reloads PhysX from that USD.
It must not world-teleport: pieces are parented under ChessSet (x=0.41 m).
This client: homes ros2_control, pokes Kit (ROS + file), then republishes MoveIt chess scene.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

REQUEST = Path("/tmp/neura_chess_restore.request")
DONE = Path("/tmp/neura_chess_restore.done")
READY = Path("/tmp/neura_chess_restore.ready")
RESTORE_ROS_SERVICE = "/neura_chess/restore_scene"

ARM_JOINTS = [
    "lara5_joint1",
    "lara5_joint2",
    "lara5_joint3",
    "lara5_joint4",
    "lara5_joint5",
    "lara5_joint6",
]
HOME = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
GRIPPER_HOME = -0.174533


def _home_arm(timeout_s: float) -> None:
    try:
        import rclpy
        from builtin_interfaces.msg import Duration
        from control_msgs.action import FollowJointTrajectory, GripperCommand
        from rclpy.action import ActionClient
        from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
    except Exception as e:
        print(f"skip arm home (no ROS action libs): {e}", flush=True)
        return

    if not rclpy.ok():
        rclpy.init()
    node = rclpy.create_node("chess_scene_restore_arm")
    try:
        arm = ActionClient(node, FollowJointTrajectory, "/arm_controller/follow_joint_trajectory")
        if arm.wait_for_server(timeout_sec=min(1.5, timeout_s)):
            traj = JointTrajectory()
            traj.joint_names = list(ARM_JOINTS)
            pt = JointTrajectoryPoint()
            pt.positions = list(HOME)
            pt.time_from_start = Duration(sec=0, nanosec=150_000_000)
            traj.points = [pt]
            goal = FollowJointTrajectory.Goal()
            goal.trajectory = traj
            fut = arm.send_goal_async(goal)
            rclpy.spin_until_future_complete(node, fut, timeout_sec=timeout_s)
            gh = fut.result()
            if gh is not None and gh.accepted:
                rclpy.spin_until_future_complete(node, gh.get_result_async(), timeout_sec=timeout_s)
            print("arm home command sent", flush=True)
        else:
            print("arm_controller action not up — Kit will still reset joints/pieces", flush=True)

        grip = ActionClient(node, GripperCommand, "/gripper_controller/gripper_cmd")
        if grip.wait_for_server(timeout_sec=0.5):
            g = GripperCommand.Goal()
            g.command.position = GRIPPER_HOME
            g.command.max_effort = 20.0
            gf = grip.send_goal_async(g)
            rclpy.spin_until_future_complete(node, gf, timeout_sec=1.0)
            print("gripper home command sent", flush=True)
    finally:
        node.destroy_node()


def _reset_chess_scene(timeout_s: float) -> None:
    try:
        import rclpy
        from std_srvs.srv import Trigger
    except Exception as e:
        print(f"skip chess_scene reset: {e}", flush=True)
        return
    if not rclpy.ok():
        rclpy.init()
    node = rclpy.create_node("chess_scene_restore_scene")
    try:
        client = node.create_client(Trigger, "/chess_scene/reset_scene")
        if not client.wait_for_service(timeout_sec=min(1.0, timeout_s)):
            print("chess_scene reset service not up — skip", flush=True)
            return
        fut = client.call_async(Trigger.Request())
        rclpy.spin_until_future_complete(node, fut, timeout_sec=timeout_s)
        res = fut.result()
        if res is not None:
            print(f"chess_scene: {res.message}", flush=True)
    finally:
        node.destroy_node()


def _call_kit_ros(timeout_s: float) -> bool:
    try:
        import rclpy
        from std_srvs.srv import Trigger
    except Exception:
        return False
    if not rclpy.ok():
        rclpy.init()
    node = rclpy.create_node("chess_scene_restore_kit_srv")
    try:
        client = node.create_client(Trigger, RESTORE_ROS_SERVICE)
        if not client.wait_for_service(timeout_sec=min(0.8, timeout_s)):
            return False
        fut = client.call_async(Trigger.Request())
        rclpy.spin_until_future_complete(node, fut, timeout_sec=timeout_s)
        res = fut.result()
        if res is None:
            return False
        print(f"Kit ROS restore: {res.message}", flush=True)
        return bool(res.success)
    except Exception as e:
        print(f"Kit ROS restore skipped: {e}", flush=True)
        return False
    finally:
        node.destroy_node()


def _wait_ready(timeout_s: float) -> bool:
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        if READY.is_file():
            print(f"Kit restore listener: {READY.read_text(encoding='utf-8').strip()}", flush=True)
            return True
        time.sleep(0.1)
    print(
        f"ERROR: Kit has no restore listener ({READY} missing). "
        "The running world was launched before SceneRestore. "
        "Restart it: ./scripts/launch/launch_world.sh  then wait until the log shows "
        "'Scene restore snapshot' and run ./scripts/scene/chess_scene_restore.sh again.",
        flush=True,
    )
    return False


def _poke_kit(timeout_s: float) -> bool:
    try:
        DONE.unlink(missing_ok=True)
    except TypeError:
        if DONE.exists():
            DONE.unlink()
    REQUEST.write_text("1\n", encoding="utf-8")
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        if DONE.is_file():
            print(f"Isaac restore: {DONE.read_text(encoding='utf-8').strip()}", flush=True)
            return True
        time.sleep(0.02)
    leftover = REQUEST.is_file()
    print(
        f"ERROR: Isaac did not ack {DONE} in {timeout_s:.1f}s. "
        + (
            "Kit never consumed the request file — this world has no SceneRestore poll. "
            "Restart ./scripts/launch/launch_world.sh and wait for 'Scene restore snapshot'."
            if leftover
            else "Kit consumed the request but did not finish. Check /tmp/neura_chess_world.log "
            "and retry with --timeout 20."
        ),
        flush=True,
    )
    return False


def main() -> int:
    p = argparse.ArgumentParser(
        description="Restore Isaac chess board, pieces, and Lara joints to start"
    )
    p.add_argument("--timeout", type=float, default=8.0, help="Seconds to wait for Kit ack")
    p.add_argument("--skip-arm", action="store_true", help="Do not send ros2_control home")
    p.add_argument("--skip-scene", action="store_true", help="Do not call chess_scene/reset_scene")
    args = p.parse_args()

    t0 = time.perf_counter()
    if not _wait_ready(timeout_s=min(2.0, args.timeout)):
        return 1
    if not args.skip_arm:
        _home_arm(timeout_s=max(0.8, args.timeout))
    _call_kit_ros(timeout_s=1.0)
    ok = _poke_kit(timeout_s=args.timeout)
    if not args.skip_scene:
        _reset_chess_scene(timeout_s=1.0)
    print(
        f"chess_scene_restore done in {(time.perf_counter() - t0) * 1000.0:.0f} ms (kit_ok={ok})",
        flush=True,
    )
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
