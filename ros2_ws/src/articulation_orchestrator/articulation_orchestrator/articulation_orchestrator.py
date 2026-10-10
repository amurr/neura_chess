#!/usr/bin/env python3
"""articulation_orchestrator: high-level logic.

Decides WHAT the robot should do, builds a list of MotionSteps and sends it to
moveit_master (C++) via the action "moveit_master/execute_sequence".
"""
import math
import os
import threading

import yaml
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.executors import MultiThreadedExecutor
from ament_index_python.packages import get_package_share_directory
from geometry_msgs.msg import Pose, Vector3

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


def gripper_joint(value) -> MotionStep:
    return MotionStep(type=MotionStep.GRIPPER_JOINT, joint_value=float(value))


def cartesian(dx=0.0, dy=0.0, dz=0.0) -> MotionStep:
    """Straight-line EEF move by (dx, dy, dz) in the planning frame (world)."""
    return MotionStep(type=MotionStep.ARM_CARTESIAN,
                      offset=Vector3(x=float(dx), y=float(dy), z=float(dz)))


def attach(obj_id) -> MotionStep:
    return MotionStep(type=MotionStep.ATTACH, object_id=obj_id)


def detach(obj_id) -> MotionStep:
    return MotionStep(type=MotionStep.DETACH, object_id=obj_id)


def allow_collision(obj_id, touch=(), allow=True) -> MotionStep:
    """allow: obj may touch the gripper links + `touch` (e.g. the board square under it)."""
    return MotionStep(type=MotionStep.ALLOW_COLLISION, object_id=obj_id,
                      touch_links=list(touch), allow=allow)


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

        share = get_package_share_directory("articulation_orchestrator")
        self.declare_parameter("objects_dictionary", os.path.join(share, "assets", "objects_dictionary.yaml"))
        self.declare_parameter("home_pose", "stand")        # SRDF named states of group "arm"
        self.declare_parameter("mid_pose", "mid_move")
        self.declare_parameter("discard_pose", "discard")   # where captured pieces are dropped

    def _param(self, name):
        return self.get_parameter(name).value

    # ---------- objects dictionary ----------
    def object_spec(self, obj_type) -> dict:
        """defaults + objects[obj_type] from objects_dictionary.yaml (re-read every call)."""
        with open(self._param("objects_dictionary")) as f:
            d = yaml.safe_load(f)
        if obj_type not in d["objects"]:
            raise KeyError(f"'{obj_type}' not in objects_dictionary.yaml")
        spec = {**d.get("defaults", {}), **(d["objects"][obj_type] or {})}
        spec.setdefault("lift_distance", spec["lower_distance"])
        return spec

    # ---------- sequences ----------
    def transfer_steps(self, obj_id, obj_type, pick_hover, pick_support,
                       place_hover=None, place_support=None) -> list:
        """Pick `obj_id` below SRDF pose `pick_hover`, place it below `place_hover`.

        *_support: collision object the piece stands on (allowed to touch it while it is
        lifted off / set down). place_hover=None: drop the piece at `discard_pose` (capture).
        """
        o = self.object_spec(obj_type)
        down, up = o["lower_distance"], o["lift_distance"]
        steps = [
            arm_named(self._param("home_pose")),            # 0. start from home
            arm_named(self._param("mid_pose")),             # 1.
            arm_named(pick_hover),                          # 2. hover over the piece
            gripper_joint(o["gripper_open_position"]),      # 3.
            allow_collision(obj_id, [pick_support]),        #    fingers may touch the piece
            cartesian(dz=-down),                            # 4. straight down
            gripper_joint(o["gripper_close_position"]),     # 5. grasp
            attach(obj_id),                                 #    piece now moves with the EEF
            cartesian(dz=up),                               # 6. straight up
            allow_collision(obj_id, [pick_support], allow=False),
        ]
        if place_hover is None:                             # captured piece -> discard
            return steps + [
                arm_named(self._param("discard_pose")),
                gripper_joint(o["gripper_open_position"]),
                allow_collision(obj_id),                    # stays allowed until the arm left
                detach(obj_id),
                arm_named(self._param("home_pose")),
                allow_collision(obj_id, allow=False),
            ]
        return steps + [
            arm_named(place_hover),                         # 7. hover over the target square
            allow_collision(obj_id, [place_support]),
            cartesian(dz=-down),                            # 8. straight down
            gripper_joint(o["gripper_open_position"]),      # 9. release
            detach(obj_id),                                 #    piece back in the world
            cartesian(dz=down),                             # 10. back to hover
            allow_collision(obj_id, [place_support], allow=False),
            arm_named(self._param("home_pose")),            # 11. home
        ]

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