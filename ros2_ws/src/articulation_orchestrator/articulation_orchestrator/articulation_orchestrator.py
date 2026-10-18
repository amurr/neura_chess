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

from lara5_moveit.board_ik import JAW_AXIS_YAW, JAW_AXIS_YAW_ALT
from moveit_master.action import ExecuteSequence
from moveit_master.msg import MotionStep

WRIST_MARGIN = 0.002  # m, wrist - neighbouring piece (horizontal and vertical)


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


def cartesian(dx=0.0, dy=0.0, dz=0.0, frame="") -> MotionStep:
    """Straight-line TCP move by (dx, dy, dz) in the planning frame (world), or in the TCP
    axes with frame="tcp" (x: static -> moving finger)."""
    return MotionStep(type=MotionStep.ARM_CARTESIAN, frame=frame,
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
        # SRDF hover poses with the alternative jaw direction: hover name + suffix ("" = none)
        self.declare_parameter("alt_hover_suffix", "_alt")

    def _param(self, name):
        return self.get_parameter(name).value

    # ---------- objects dictionary ----------
    def object_spec(self, obj_type) -> dict:
        """defaults + objects[obj_type] from objects_dictionary.yaml (re-read every call)."""
        with open(self._param("objects_dictionary")) as f:
            d = yaml.safe_load(f)
        if obj_type not in d["objects"]:
            raise KeyError(f"'{obj_type}' not in objects_dictionary.yaml")
        return {**d.get("defaults", {}), **(d["objects"][obj_type] or {})}

    @staticmethod
    def _wrist_clear(spec, neighbours, tcp_offset, jaw_yaw=JAW_AXIS_YAW) -> bool:
        """True if the wrist (objects_dictionary `wrist` boxes, TCP frame) clears the pieces in
        `neighbours` [(dx, dy, profile)]: world offsets from the square centre and
        ((z, radius at or above z), ...) from the board. tcp_offset: TCP - square centre.
        jaw_yaw: world yaw of the TCP x axis (hover poses)."""
        cx, cy = math.cos(jaw_yaw), math.sin(jaw_yaw)
        for dx, dy, profile in neighbours:
            # neighbour centre in the TCP frame
            px = dx * cx + dy * cy - tcp_offset[0]
            py = -dx * cy + dy * cx - tcp_offset[1]
            for box in spec["wrist"]:
                bottom = spec["tip_height"] + box["z"][0] - WRIST_MARGIN
                if profile[-1][0] < bottom:
                    continue                            # the piece ends below this box
                # radius of the piece from the box bottom up (last profile step at or below it)
                radius = [r for z, r in profile if z <= max(bottom, 0.0)][-1]
                qx = min(max(px, box["x"][0]), box["x"][1])
                qy = min(max(py, box["y"][0]), box["y"][1])
                if math.hypot(px - qx, py - qy) < radius + WRIST_MARGIN:
                    return False
        return True

    def grasp_level(self, spec, pick_neighbours=(), place_neighbours=(), alt_jaw=True) -> dict:
        """The lowest grasp level (objects_dictionary: preferred, then `higher`) whose wrist
        clears the neighbouring pieces at the pick and at the place (one grip for both), with
        the default jaw direction or else (alt_jaw) the alternative one: `jaw_alt` in the result.
        """
        levels = [spec] + [{**spec, **h} for h in spec.get("higher", [])]
        jaws = [(False, JAW_AXIS_YAW)] + ([(True, JAW_AXIS_YAW_ALT)] if alt_jaw else [])
        for level in levels:
            if level is not spec:
                level.pop("place_offset", None)     # measured for the preferred level only
            pick = (-(level["grasp_offset"] + level["finger_clearance"]), 0.0)
            place = tuple(-v for v in level.get("place_offset", (level["grasp_offset"], 0.0)))
            clear = [alt for alt, yaw in jaws
                     if self._wrist_clear(level, pick_neighbours, pick, yaw)
                     and self._wrist_clear(level, place_neighbours, place, yaw)]
            if clear:
                break
        level = dict(level, jaw_alt=bool(clear) and clear[0])
        level.pop("higher", None)
        level.setdefault("lift_distance", level["lower_distance"])
        return level

    # ---------- sequences ----------
    def transfer_steps(self, obj_id, obj_type, pick_hover, pick_support,
                       place_hover=None, place_support=None,
                       pick_neighbours=(), place_neighbours=()) -> list:
        """Pick `obj_id` below SRDF pose `pick_hover`, place it below `place_hover`.

        *_support: collision object(s) the piece stands on (allowed to touch them while it is
        lifted off / set down). place_hover=None: drop the piece at `discard_pose` (capture).
        *_neighbours: pieces around the square [(dx, dy, radius profile)] (chess_board_server):
        the grip is taken higher when the wrist would hit one of them.
        """
        alt_suffix = self._param("alt_hover_suffix")
        o = self.grasp_level(self.object_spec(obj_type), pick_neighbours, place_neighbours,
                             alt_jaw=bool(alt_suffix))
        if o["jaw_alt"]:                                    # alternative jaw direction
            pick_hover = pick_hover + alt_suffix
            place_hover = place_hover and place_hover + alt_suffix
        down, up = o["lower_distance"], o["lift_distance"]
        pick_support = [pick_support] if isinstance(pick_support, str) else list(pick_support)
        place_support = ([place_support] if isinstance(place_support, str)
                         else list(place_support or []))
        # The hover puts the TCP (static finger tip) above the square centre. Shift it so the
        # piece centre is at +grasp_offset along the TCP x axis: that is where the closing jaw
        # pushes the piece against the static finger, so the same shift centres it when placed.
        pick_shift = -(o["grasp_offset"] + o["finger_clearance"])
        steps = [
            arm_named(self._param("home_pose")),            # 0. start from home
            arm_named(self._param("mid_pose")),             # 1.
            arm_named(pick_hover),                          # 2. hover over the piece
            gripper_joint(o["gripper_open_position"]),      # 3.
            cartesian(dx=pick_shift, frame="tcp"),          #    static finger next to the piece
            allow_collision(obj_id, pick_support),          #    fingers may touch the piece
            cartesian(dz=-down),                            # 4. straight down
            gripper_joint(o["gripper_close_position"]),     # 5. grasp
            attach(obj_id),                                 #    piece now moves with the EEF
            cartesian(dz=up),                               # 6. straight up
            allow_collision(obj_id, pick_support, allow=False),
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
        # Where the piece sits in the TCP frame while carried: measured in Isaac when calibrated
        # (place_offset, scripts/calibrate_place_offsets.py), else the geometric grasp_offset.
        px, py = o.get("place_offset", (o["grasp_offset"], 0.0))
        press = o["place_press"]     # a slightly tilted piece is set down onto its base
        return steps + [
            arm_named(place_hover),                         # 7. hover over the target square
            cartesian(dx=-px, dy=-py, frame="tcp"),         #    piece centre above the square
            allow_collision(obj_id, place_support),
            cartesian(dz=-(down + press)),                  # 8. straight down
            gripper_joint(o["gripper_release_position"]),   # 9. release
            detach(obj_id),                                 #    piece back in the world
            cartesian(dx=-o["release_retreat"], frame="tcp"),  # static finger off the piece
            cartesian(dz=down + press),                     # 10. back to hover height
            allow_collision(obj_id, place_support, allow=False),
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