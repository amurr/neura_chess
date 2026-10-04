#!/usr/bin/env python3
"""articulation_orchestrator: high-level logic.

Decides WHAT the robot should do, builds a list of MotionSteps and sends it to
moveit_master (C++) via the action "moveit_master/execute_sequence".
"""
import math
import threading

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.executors import MultiThreadedExecutor
from geometry_msgs.msg import Pose

from moveit_master.action import ExecuteSequence
from moveit_master.msg import MotionStep


# ---------- step builders ----------
def make_pose(x, y, z, roll, pitch, yaw) -> Pose:
    cr, sr = math.cos(roll / 2), math.sin(roll / 2)
    cp, sp = math.cos(pitch / 2), math.sin(pitch / 2)
    cy, sy = math.cos(yaw / 2), math.sin(yaw / 2)
    p = Pose()
    p.position.x, p.position.y, p.position.z = x, y, z
    p.orientation.x = sr * cp * cy - cr * sp * sy
    p.orientation.y = cr * sp * cy + sr * cp * sy
    p.orientation.z = cr * cp * sy - sr * sp * cy
    p.orientation.w = cr * cp * cy + sr * sp * sy
    return p


def arm_pose(x, y, z, roll, pitch, yaw) -> MotionStep:
    return MotionStep(type=MotionStep.ARM_POSE, pose=make_pose(x, y, z, roll, pitch, yaw))


def arm_named(name) -> MotionStep:
    return MotionStep(type=MotionStep.ARM_NAMED, named_target=name)


def gripper(name) -> MotionStep:
    return MotionStep(type=MotionStep.GRIPPER_NAMED, named_target=name)


def wait(seconds) -> MotionStep:
    return MotionStep(type=MotionStep.WAIT, duration=float(seconds))


# ---------- client ----------
def _wait_future(future):
    done = threading.Event()
    future.add_done_callback(lambda _: done.set())
    done.wait()
    return future.result()


class ArticulationOrchestrator(Node):
    def __init__(self):
        super().__init__("articulation_orchestrator")
        self._client = ActionClient(self, ExecuteSequence, "moveit_master/execute_sequence")

    def wait_for_master(self):
        self.get_logger().info("waiting for moveit_master ...")
        self._client.wait_for_server()

    def run_sequence(self, steps, velocity_scaling=0.0):
        """Blocking: returns (success, message)."""
        goal = ExecuteSequence.Goal(steps=steps, velocity_scaling=velocity_scaling)
        handle = _wait_future(self._client.send_goal_async(goal))
        if not handle.accepted:
            return False, "rejected (moveit_master busy)"
        res = _wait_future(handle.get_result_async()).result
        if not res.success:
            return False, f"step {res.failed_step}: {res.message}"
        return True, res.message


def main():
    rclpy.init()
    node = ArticulationOrchestrator()
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    threading.Thread(target=executor.spin, daemon=True).start()

    node.wait_for_master()

    # Same sequence as the old hard-coded moveit_master.cpp, now defined here.
    sequence = [
        arm_named("home"),
        arm_pose(0.5, 0.1, 0.6, 3.14, 0.0, 0.0),
        arm_pose(0.5, 0.1, 0.3, 3.14, 0.0, 0.0),
        gripper("gripper_open"),
        wait(1.0),
        arm_pose(0.5, -0.1, 0.3, 3.14, 0.0, 0.0),
        gripper("gripper_closed"),
        wait(1.0),
        arm_named("home"),
        gripper("gripper_open"),
        wait(1.0),
    ]

    #velocity_scaling sets how fast the robot moves, as a fraction of its maximum joint speeds
    ok, msg = node.run_sequence(sequence, velocity_scaling=0.2)
    node.get_logger().info(f"sequence {'succeeded' if ok else 'failed'}: {msg}")

    rclpy.shutdown()


if __name__ == "__main__":
    main()