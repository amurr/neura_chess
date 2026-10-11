#!/usr/bin/env python3
"""execution_logger: record the arm in the world frame while /chess_board goals run.

Starts a run when a /chess_board goal starts executing and closes it when the goal
ends. Each run is a directory <out_dir>/<YYYYmmdd_HHMMSS>/ with:

- arm.jsonl           samples at rate_hz: joint positions + world-frame pose of every
                      link in `links`, tagged with the chess stage and the moveit_master
                      step; plus event records (goal start/end, stage, step changes)
- scene.json          PlanningScene world objects (board_sq_*, piece_*, ...) at run start,
                      poses in their header frame (world)
- isaac_pieces.jsonl  Isaac (PhysX) piece poses recorded by Kit during the run
                      (neura_chess_piece_positions record mode, isaac_pieces_hz)
- steps.csv           one row per moveit_master step, taken when the step ended:
                      gripper / jaw position vs the moved piece (PlanningScene and Isaac)
                      and vs the target square, so MoveIt targets (hover poses,
                      lower_distance, gripper positions) can be corrected

Step labels come from ArticulationOrchestrator.transfer_steps, so they follow the
real sequence. Usage (next to chess_board_server, same ROS env):

  ros2 run articulation_orchestrator execution_logger
  ros2 run articulation_orchestrator execution_logger --ros-args -p out_dir:=/tmp/runs -p rate_hz:=50
"""
import csv
import json
import re
import shutil
import time
from pathlib import Path

import rclpy
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, QoSProfile, ReliabilityPolicy
from rclpy.time import Time
from tf2_ros import Buffer, TransformListener
from action_msgs.msg import GoalStatus, GoalStatusArray
from sensor_msgs.msg import JointState
from moveit_msgs.msg import PlanningSceneComponents
from moveit_msgs.srv import GetPlanningScene

from chess_interfaces.action import ChessBoard
from moveit_master.action import ExecuteSequence
from moveit_master.msg import MotionStep
from articulation_orchestrator.articulation_orchestrator import ArticulationOrchestrator

# Kit record mode (neura_chess_piece_positions.py): Kit appends a snapshot to
# PIECES_JSONL at the rate written into PIECES_RECORD while that file exists.
PIECES_JSONL = Path("/tmp/neura_chess_pieces.jsonl")
PIECES_RECORD = Path("/tmp/neura_chess_pieces.record")

DEFAULT_LINKS = [
    "lara5_link1", "lara5_link2", "lara5_link3", "lara5_link4", "lara5_link5", "lara5_link6",
    "lara5_gripper", "lara5_gripper_body", "lara5_gripper_jaw",
]
STAGE_RE = re.compile(r"^(move|capture) ([a-h][1-8]) -> ([a-h][1-8]|discard)$")
TERMINAL = {GoalStatus.STATUS_SUCCEEDED: "succeeded", GoalStatus.STATUS_CANCELED: "canceled",
            GoalStatus.STATUS_ABORTED: "aborted"}
STEP_TYPES = {v: k for k, v in vars(MotionStep).items() if k.isupper() and isinstance(v, int)}
OPEN, CLOSE = 1.0, -1.0     # sentinel gripper values used only to label steps


# ---------- small math ----------
def quat_mul(a, b):
    aw, ax, ay, az = a
    bw, bx, by, bz = b
    return (aw * bw - ax * bx - ay * by - az * bz, aw * bx + ax * bw + ay * bz - az * by,
            aw * by - ax * bz + ay * bw + az * bx, aw * bz + ax * by - ay * bx + az * bw)


def quat_rotate(q, v):
    w, x, y, z = q
    p = quat_mul(quat_mul(q, (0.0, *v)), (w, -x, -y, -z))
    return p[1:]


def pose_tuple(p):
    return ((p.position.x, p.position.y, p.position.z),
            (p.orientation.w, p.orientation.x, p.orientation.y, p.orientation.z))


def compose(a, b):
    """a * b for (xyz, wxyz) poses."""
    t = quat_rotate(a[1], b[0])
    return (tuple(a[0][i] + t[i] for i in range(3)), quat_mul(a[1], b[1]))


def rnd(v, n=5):
    return [round(float(x), n) for x in v]


# ---------- step labels ----------
class _StepStub:
    """Stands in for ArticulationOrchestrator so transfer_steps() can be called offline."""

    def __init__(self, params):
        self._params = params

    def _param(self, name):
        return self._params[name]

    def object_spec(self, _obj_type):
        return {"lower_distance": 1.0, "lift_distance": 1.0,
                "gripper_open_position": OPEN, "gripper_close_position": CLOSE}


def step_label(s) -> str:
    kind = STEP_TYPES.get(s.type, str(s.type))
    if s.type in (MotionStep.ARM_NAMED, MotionStep.GRIPPER_NAMED):
        return f"{kind} {s.named_target}"
    if s.type == MotionStep.GRIPPER_JOINT:
        return f"{kind} {'open' if s.joint_value == OPEN else 'close'}"
    if s.type == MotionStep.ARM_CARTESIAN:
        return f"{kind} {'down' if s.offset.z < 0 else 'up'}"
    if s.type == MotionStep.ALLOW_COLLISION:
        return f"{kind} {s.object_id} {'allow' if s.allow else 'forbid'}"
    if s.type in (MotionStep.ATTACH, MotionStep.DETACH):
        return f"{kind} {s.object_id}"
    return kind


class ExecutionLogger(Node):
    def __init__(self):
        super().__init__("execution_logger")
        self.declare_parameter("out_dir", "/tmp/neura_chess_exec_logs")
        self.declare_parameter("rate_hz", 20.0)
        self.declare_parameter("world_frame", "world")
        self.declare_parameter("links", DEFAULT_LINKS)
        self.declare_parameter("eef_link", "lara5_gripper")
        self.declare_parameter("jaw_link", "lara5_gripper_jaw")
        self.declare_parameter("isaac_pieces_hz", 10.0)   # 0 = do not record Isaac pieces
        # Must match chess_board_server / ArticulationOrchestrator.
        self.declare_parameter("hover_pose_format", "{square}_hover")
        self.declare_parameter("home_pose", "stand")
        self.declare_parameter("mid_pose", "mid_move")
        self.declare_parameter("discard_pose", "discard")

        self.tf = Buffer()
        self._tf_listener = TransformListener(self.tf, self)
        self.joints = {}
        self.run = None

        status_qos = QoSProfile(depth=1, reliability=ReliabilityPolicy.RELIABLE,
                                durability=DurabilityPolicy.TRANSIENT_LOCAL)
        self.create_subscription(JointState, "/joint_states", self._on_joints, 50)
        self.create_subscription(GoalStatusArray, "/chess_board/_action/status",
                                 self._on_status, status_qos)
        self.create_subscription(ChessBoard.Impl.FeedbackMessage, "/chess_board/_action/feedback",
                                 self._on_stage, 10)
        self.create_subscription(ExecuteSequence.Impl.FeedbackMessage,
                                 "/moveit_master/execute_sequence/_action/feedback",
                                 self._on_step, 10)
        self._scene_client = self.create_client(GetPlanningScene, "/get_planning_scene")
        self.create_timer(1.0 / max(self._p("rate_hz"), 1.0), self._sample)
        self.get_logger().info(f"execution_logger ready, runs go to {self._p('out_dir')}")

    def _p(self, name):
        return self.get_parameter(name).value

    # ---------- inputs ----------
    def _on_joints(self, msg):
        self.joints.update(zip(msg.name, msg.position))

    def _on_status(self, msg):
        for st in msg.status_list:
            gid = bytes(st.goal_info.goal_id.uuid).hex()
            if self.run is None and st.status == GoalStatus.STATUS_EXECUTING:
                self._start(gid)
            elif self.run and self.run["goal"] == gid and st.status in TERMINAL:
                self._finish(TERMINAL[st.status])

    def _on_stage(self, msg):
        if not self.run:
            return
        stage = msg.feedback.stage
        r = self.run
        r["stage"], r["step"], r["step_start"] = stage, None, None
        m = STAGE_RE.match(stage)
        r["transfer"] = None
        if m:
            r["transfer_n"] += 1
            src, dst = m.group(2), (None if m.group(3) == "discard" else m.group(3))
            r["transfer"] = {"n": r["transfer_n"], "src": src, "dst": dst,
                             "labels": self._labels(src, dst), "isaac_piece": None}
        self._event("stage", stage=stage,
                    steps=r["transfer"]["labels"] if r["transfer"] else None)

    def _on_step(self, msg):
        if not self.run:
            return
        self._close_step()
        r = self.run
        r["step"] = int(msg.feedback.current_step)
        r["step_start"] = time.time()
        self._event("step", step=r["step"], label=self._label(r["step"]))

    # ---------- run lifecycle ----------
    def _start(self, gid):
        d = Path(self._p("out_dir")) / time.strftime("%Y%m%d_%H%M%S")
        d.mkdir(parents=True, exist_ok=True)
        self.run = {"goal": gid, "dir": d, "t0": time.time(), "stage": "", "step": None,
                    "step_start": None, "transfer": None, "transfer_n": 0, "rows": [],
                    "scene": None, "arm": (d / "arm.jsonl").open("w")}
        self._event("goal_start", goal_id=gid)
        self._request_scene()
        self._isaac_record(True)
        self.get_logger().info(f"recording goal {gid[:8]} -> {d}")

    def _finish(self, outcome):
        self._close_step()
        self._event("goal_end", outcome=outcome)
        r, self.run = self.run, None
        r["arm"].close()
        isaac = self._isaac_record(False, r)
        self._write_steps(r, isaac)
        self.get_logger().info(f"goal {outcome}: {r['dir']} ({len(r['rows'])} steps)")

    # ---------- sampling ----------
    def _link_poses(self):
        out, world = {}, self._p("world_frame")
        for link in self._p("links"):
            try:
                t = self.tf.lookup_transform(world, link, Time()).transform
            except Exception:
                continue
            out[link] = {"xyz": rnd((t.translation.x, t.translation.y, t.translation.z)),
                         "wxyz": rnd((t.rotation.w, t.rotation.x, t.rotation.y, t.rotation.z))}
        return out

    def _sample(self):
        if not self.run:
            return
        r = self.run
        self._write({"type": "sample", "t": round(time.time(), 4), "stage": r["stage"],
                     "step": r["step"], "label": self._label(r["step"]),
                     "joints": {k: round(v, 5) for k, v in sorted(self.joints.items())},
                     "links": self._link_poses()})

    def _event(self, kind, **data):
        self._write({"type": "event", "event": kind, "t": round(time.time(), 4), **data})

    def _write(self, rec):
        self.run["arm"].write(json.dumps(rec) + "\n")
        self.run["arm"].flush()

    def _close_step(self):
        """Store where the gripper is at the end of the running step (for steps.csv)."""
        r = self.run
        if not r or r["step"] is None:
            return
        links, tr = self._link_poses(), r["transfer"] or {}
        r["rows"].append({
            "t_end": time.time(), "t_start": r["step_start"], "stage": r["stage"],
            "transfer": tr.get("n"), "src": tr.get("src"), "dst": tr.get("dst"),
            "step": r["step"], "label": self._label(r["step"]),
            "finger": self.joints.get("lara5_gripper_finger_joint"),
            "eef": links.get(self._p("eef_link"), {}).get("xyz"),
            "jaw": links.get(self._p("jaw_link"), {}).get("xyz"),
        })
        r["step"] = None

    def _labels(self, src, dst):
        stub = _StepStub({k: self._p(k) for k in ("home_pose", "mid_pose", "discard_pose")})
        fmt = self._p("hover_pose_format")
        steps = ArticulationOrchestrator.transfer_steps(
            stub, f"piece_{src}", "piece", fmt.format(square=src), f"board_sq_{src}",
            dst and fmt.format(square=dst), dst and f"board_sq_{dst}")
        return [step_label(s) for s in steps]

    def _label(self, i):
        tr = self.run and self.run["transfer"]
        if i is None or not tr or i >= len(tr["labels"]):
            return None
        return tr["labels"][i]

    # ---------- PlanningScene ----------
    def _request_scene(self):
        if not self._scene_client.service_is_ready():
            self.get_logger().warn("/get_planning_scene not available, scene.json skipped")
            return
        req = GetPlanningScene.Request()
        req.components.components = (PlanningSceneComponents.WORLD_OBJECT_NAMES
                                     | PlanningSceneComponents.WORLD_OBJECT_GEOMETRY)
        run = self.run
        self._scene_client.call_async(req).add_done_callback(lambda f: self._on_scene(run, f))

    def _on_scene(self, run, future):
        try:
            objects = future.result().scene.world.collision_objects
        except Exception as e:
            self.get_logger().warn(f"get_planning_scene failed: {e}")
            return
        scene = {}
        for o in objects:
            base = pose_tuple(o.pose)
            shapes = [(f"primitive:{p.type}", list(p.dimensions), pp)
                      for p, pp in zip(o.primitives, o.primitive_poses)]
            shapes += [("mesh", [], mp) for mp in o.mesh_poses]
            world = [compose(base, pose_tuple(pp)) for _, _, pp in shapes]
            scene[o.id] = {
                "frame": o.header.frame_id,
                "pose": {"xyz": rnd(base[0]), "wxyz": rnd(base[1])},
                "shapes": [{"kind": k, "dimensions": rnd(dims), "xyz": rnd(w[0]),
                            "wxyz": rnd(w[1])} for (k, dims, _), w in zip(shapes, world)],
            }
        run["scene"] = scene
        (run["dir"] / "scene.json").write_text(json.dumps(scene, indent=1))

    # ---------- Isaac pieces (Kit record mode) ----------
    def _isaac_record(self, on, run=None):
        hz = float(self._p("isaac_pieces_hz"))
        if hz <= 0:
            return []
        try:
            if on:
                PIECES_JSONL.write_text("")
                PIECES_RECORD.write_text(f"{hz:.6f}\n")
                return []
            PIECES_RECORD.unlink(missing_ok=True)
            time.sleep(0.2)     # let Kit finish its last write
            if PIECES_JSONL.is_file():
                shutil.copyfile(PIECES_JSONL, run["dir"] / "isaac_pieces.jsonl")
                return [json.loads(line) for line in PIECES_JSONL.read_text().splitlines()
                        if line.strip()]
        except (OSError, ValueError) as e:
            self.get_logger().warn(f"Isaac piece recording: {e}")
        return []

    # ---------- summary ----------
    def _write_steps(self, r, isaac):
        scene = r["scene"] or {}

        def scene_xyz(obj_id):
            o = scene.get(obj_id)
            return o["shapes"][0]["xyz"] if o and o["shapes"] else (o or {}).get("pose", {}).get("xyz")

        def isaac_at(t):
            return min(isaac, key=lambda s: abs(s.get("t_unix", 0.0) - t)) if isaac else None

        tracked = {}    # transfer n -> Isaac prim name of the moved piece
        placing = set()     # transfers that reached the target-square hover
        fmt = self._p("hover_pose_format")
        cols = ["transfer", "src", "dst", "step", "label", "t_start", "t_end", "finger",
                "eef_x", "eef_y", "eef_z", "jaw_x", "jaw_y", "jaw_z",
                "ps_piece_x", "ps_piece_y", "ps_piece_z",
                "isaac_piece_x", "isaac_piece_y", "isaac_piece_z", "isaac_piece_square",
                "eef_minus_isaac_x", "eef_minus_isaac_y", "eef_minus_isaac_z",
                "target_square", "ps_square_x", "ps_square_y", "ps_square_z",
                "eef_minus_square_x", "eef_minus_square_y", "eef_minus_square_z"]
        with (r["dir"] / "steps.csv").open("w", newline="") as f:
            w = csv.writer(f)
            w.writerow(cols)
            for row in r["rows"]:
                src, dst, eef = row["src"], row["dst"], row["eef"]
                if dst and row["label"] == f"ARM_NAMED {fmt.format(square=dst)}":
                    placing.add(row["transfer"])
                target_sq = dst if row["transfer"] in placing else src
                ps_piece = scene_xyz(f"piece_{src}") if src else None
                ps_sq = scene_xyz(f"board_sq_{target_sq}") if target_sq else None
                ip, isq = None, None
                snap = isaac_at(row["t_end"])
                if snap and src:
                    if row["transfer"] not in tracked:
                        first = isaac_at(row["t_start"] or row["t_end"])
                        tracked[row["transfer"]] = next(
                            (p["name"] for p in first.get("pieces", []) if p.get("square") == src), None)
                    p = next((p for p in snap.get("pieces", [])
                              if p.get("name") == tracked[row["transfer"]]), None)
                    if p:
                        ip, isq = (p["x"], p["y"], p["z"]), p.get("square")

                def diff(a, b):
                    return rnd([a[i] - b[i] for i in range(3)]) if a and b else [None] * 3

                w.writerow([row["transfer"], src, dst, row["step"], row["label"],
                            round(row["t_start"] or 0.0, 3), round(row["t_end"], 3),
                            None if row["finger"] is None else round(row["finger"], 4),
                            *(eef or [None] * 3), *(row["jaw"] or [None] * 3),
                            *(ps_piece or [None] * 3), *(rnd(ip) if ip else [None] * 3), isq,
                            *diff(eef, ip), target_sq, *(ps_sq or [None] * 3), *diff(eef, ps_sq)])

    def destroy_node(self):
        if self.run:
            self._finish("logger stopped")
        super().destroy_node()


def main():
    rclpy.init()
    node = ExecutionLogger()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
