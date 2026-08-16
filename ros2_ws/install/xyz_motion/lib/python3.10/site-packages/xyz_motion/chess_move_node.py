"""Orchestrate chess pick-and-place via MoveIt IK or taught joint poses."""

from __future__ import annotations

import json
import threading
import time
from collections.abc import Callable

import rclpy
from lara_interfaces.srv import MoveJoints
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import String

from xyz_motion.chess_xyz import CHESS_OCCUPANCY_TOPIC, chess_occupancy_to_pose6
from xyz_motion.chess_piece_meshes import PieceMeshLibrary
from xyz_motion.gripper_planning_scene import GripperPlanningScene
from xyz_motion.moveit_ik import MoveItIkSolver, pose6_with_z_offset
from xyz_motion.poses import JOINT_POSES

_latest_chess_occupancy: dict | None = None
_latest_pose6_from_chess: dict[str, list[float]] | None = None


DEFAULT_MOVE_SPEED = 20.0
DEFAULT_MOVE_ACCELERATION = 20.0
DEFAULT_ENABLE_SAFETY = True
DEFAULT_GRIPPER_PAUSE_SEC = 0.8
DEFAULT_CAMERA_SETTLE_SEC = 0.5
DEFAULT_APPROACH_Z_OFFSET = 0.08


def _resolve_square_name(occ: dict, keys: tuple[str, ...]) -> str | None:
    for key in keys:
        value = occ.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip().lower()
    return None


def _first_joint_pose(keys: list[str]) -> tuple[str, list[float]] | None:
    for key in keys:
        pose = JOINT_POSES.get(key)
        if pose is not None:
            return key, list(pose)
    return None


def _source_approach_keys(square: str) -> list[str]:
    return [f'{square}_approach', f'approach_{square}', f'{square}_pre', square]


def _source_pick_keys(square: str) -> list[str]:
    return [f'{square}_pick', f'pick_{square}', f'{square}_grasp', f'grasp_{square}', square]


def _target_approach_keys(square: str) -> list[str]:
    return [f'{square}_approach', f'approach_{square}', f'{square}_pre', square]


def _target_place_keys(square: str) -> list[str]:
    return [f'{square}_place', f'place_{square}', square]


def _update_pose6_cache(node: Node, data: dict) -> None:
    global _latest_pose6_from_chess
    try:
        poses = chess_occupancy_to_pose6(data)
        _latest_pose6_from_chess = poses if poses else None
    except (TypeError, ValueError) as exc:
        _latest_pose6_from_chess = None
        node.get_logger().warning(f'chess occupancy pose6 parse skipped: {exc}')


def listen_chess_occupancy(node: Node, on_update: Callable[[dict], None] | None = None) -> None:
    """Subscribe to chess occupancy JSON and cache latest command payload."""

    def _on_chess_occupancy(msg: String) -> None:
        global _latest_chess_occupancy
        try:
            data = json.loads(msg.data)
            if not isinstance(data, dict):
                node.get_logger().error('chess_occupancy JSON must be an object')
                return
        except json.JSONDecodeError as exc:
            node.get_logger().error(f'chess_occupancy bad JSON: {exc}')
            return

        _latest_chess_occupancy = data
        _update_pose6_cache(node, data)

        source_square = _resolve_square_name(data, ('source', 'from', 'from_square'))
        target_square = _resolve_square_name(data, ('target', 'to', 'to_square', 'destination'))
        if source_square and target_square:
            node.get_logger().info(
                f'chess command received: {source_square} -> {target_square}'
            )
        else:
            node.get_logger().info(
                'chess command received (waiting for source/target keys)'
            )

        if on_update is not None:
            on_update(data)

    node.create_subscription(String, CHESS_OCCUPANCY_TOPIC, _on_chess_occupancy, 10)
    node.get_logger().info(
        f'listening on {CHESS_OCCUPANCY_TOPIC!r} '
        '(std_msgs/String, JSON with source/target and optional square XYZ)'
    )


def get_latest_chess_occupancy() -> dict | None:
    return _latest_chess_occupancy


def get_latest_pose6_from_chess() -> dict[str, list[float]] | None:
    return _latest_pose6_from_chess


def get_latest_poses_from_chess() -> dict[str, list[float]] | None:
    return _latest_pose6_from_chess


class ChessMoveOrchestrator:
    """Run chess pick-and-place from chess_occupancy (IK when XYZ available)."""

    def __init__(
        self,
        node: Node,
        client,
        executor: MultiThreadedExecutor,
        *,
        ik_solver: MoveItIkSolver | None = None,
        approach_z_offset: float = DEFAULT_APPROACH_Z_OFFSET,
        scene_helper: GripperPlanningScene | None = None,
    ):
        self.node = node
        self.client = client
        self.executor = executor
        self.executor_running = False
        self.gripper_pub = node.create_publisher(String, 'command_gripper', 10)
        self._ik = ik_solver
        self._approach_z_offset = float(approach_z_offset)
        self._scene = scene_helper
        self._busy = False
        self._busy_lock = threading.Lock()

    def start_from_message(self, occ: dict) -> None:
        with self._busy_lock:
            if self._busy:
                self.node.get_logger().warning(
                    'workflow already running; ignoring new chess command'
                )
                return
            self._busy = True
        worker = threading.Thread(target=self._run_workflow, args=(dict(occ),), daemon=True)
        worker.start()

    def _run_workflow(self, occ: dict) -> None:
        try:
            self.execute_from_latest(occ)
        finally:
            with self._busy_lock:
                self._busy = False

    def _move_joints(self, joints_deg: list[float], label: str) -> bool:
        req = MoveJoints.Request()
        req.point_name = ''
        req.target_joint = list(joints_deg)
        if hasattr(req, 'target_pose'):
            req.target_pose = []
        req.speed = DEFAULT_MOVE_SPEED
        req.acceleration = DEFAULT_MOVE_ACCELERATION
        req.enable_safety = DEFAULT_ENABLE_SAFETY
        self.node.get_logger().info(f'[{label}] move_joints')
        future = self.client.call_async(req)
        if not self.executor_running:
            self.executor.spin_until_future_complete(future, timeout_sec=60.0)
            if not future.done():
                self.node.get_logger().error(f'[{label}] timeout waiting move_joints response')
                return False
            try:
                result = future.result()
            except Exception as exc:
                self.node.get_logger().error(f'[{label}] move_joints call failed: {exc}')
                return False
            if result is None:
                self.node.get_logger().error(f'[{label}] no response from move_joints')
                return False
            if not result.success:
                self.node.get_logger().error(f'[{label}] failed: {result.message}')
                return False
            self.node.get_logger().info(f'[{label}] OK: {result.message}')
            return True

        deadline = time.monotonic() + 60.0
        while rclpy.ok() and not future.done():
            if time.monotonic() > deadline:
                self.node.get_logger().error(f'[{label}] timeout waiting move_joints response')
                return False
            time.sleep(0.01)
        if not future.done():
            self.node.get_logger().error(f'[{label}] interrupted before move_joints response')
            return False
        try:
            result = future.result()
        except Exception as exc:
            self.node.get_logger().error(f'[{label}] move_joints call failed: {exc}')
            return False
        if result is None:
            self.node.get_logger().error(f'[{label}] no response from move_joints')
            return False
        if not result.success:
            self.node.get_logger().error(f'[{label}] failed: {result.message}')
            return False
        self.node.get_logger().info(f'[{label}] OK: {result.message}')
        return True

    def _move_to_pose6(self, pose6: list[float], label: str) -> bool:
        if self._ik is None:
            self.node.get_logger().error(f'[{label}] MoveIt IK solver not configured')
            return False
        joints_deg = self._ik.solve_pose6(pose6)
        if joints_deg is None:
            self.node.get_logger().error(f'[{label}] MoveIt IK failed')
            return False
        return self._move_joints(joints_deg, label)

    def _send_gripper(self, cmd: str, pause_sec: float) -> None:
        self.gripper_pub.publish(String(data=cmd))
        self.node.get_logger().info(f'[gripper] {cmd!r} (pause {pause_sec:.2f}s)')
        time.sleep(pause_sec)

    def _extract_move(self, occ: dict) -> tuple[str, str] | None:
        source = _resolve_square_name(occ, ('source', 'from', 'from_square'))
        target = _resolve_square_name(occ, ('target', 'to', 'to_square', 'destination'))
        if not source or not target:
            self.node.get_logger().info(
                'chess_occupancy needs source+target keys (e.g. {"source":"e2","target":"e4"})'
            )
            return None
        return source, target

    def _require_joint_pose(self, keys: list[str], label: str) -> list[float] | None:
        match = _first_joint_pose(keys)
        if match is None:
            self.node.get_logger().error(
                f'[{label}] missing JOINT_POSES entry. Tried keys: {", ".join(keys)}'
            )
            return None
        key, pose = match
        self.node.get_logger().info(f'[{label}] using JOINT_POSES[{key!r}]')
        return pose

    def _can_use_ik_for_move(self, occ: dict, source_square: str, target_square: str) -> bool:
        if self._ik is None or not self._ik.service_is_ready():
            return False
        try:
            poses = chess_occupancy_to_pose6(occ)
        except (TypeError, ValueError):
            return False
        return source_square in poses and target_square in poses

    def execute_from_latest(self, occ: dict) -> None:
        move = self._extract_move(occ)
        if move is None:
            return
        source_square, target_square = move

        if self._can_use_ik_for_move(occ, source_square, target_square):
            self._execute_ik_workflow(occ, source_square, target_square)
        else:
            self._execute_joint_workflow(occ, source_square, target_square)

    def _workflow_timing_and_gripper(self, occ: dict) -> tuple[float, float, str, str] | None:
        try:
            gripper_pause_sec = float(occ.get('gripper_pause_sec', DEFAULT_GRIPPER_PAUSE_SEC))
            camera_settle_sec = float(occ.get('camera_settle_sec', DEFAULT_CAMERA_SETTLE_SEC))
        except (TypeError, ValueError):
            self.node.get_logger().error('invalid gripper_pause_sec/camera_settle_sec in command')
            return None
        close_cmd = str(occ.get('close_cmd', 'close_until_stall')).strip() or 'close_until_stall'
        open_cmd = str(occ.get('open_cmd', 'open')).strip() or 'open'
        return gripper_pause_sec, camera_settle_sec, close_cmd, open_cmd

    def _execute_ik_workflow(self, occ: dict, source_square: str, target_square: str) -> None:
        timing = self._workflow_timing_and_gripper(occ)
        if timing is None:
            return
        gripper_pause_sec, camera_settle_sec, close_cmd, open_cmd = timing

        poses = chess_occupancy_to_pose6(occ)
        source_pose = poses[source_square]
        target_pose = poses[target_square]
        source_approach = pose6_with_z_offset(source_pose, self._approach_z_offset)
        target_approach = pose6_with_z_offset(target_pose, self._approach_z_offset)

        self.node.get_logger().info(
            f'MoveIt IK workflow start: {source_square} -> {target_square}'
        )

        if not self._move_joints(list(JOINT_POSES['image_1']), 'image_1'):
            return
        time.sleep(camera_settle_sec)

        if not self._move_to_pose6(source_approach, 'source_approach'):
            return
        if not self._move_to_pose6(source_pose, 'source_pick'):
            return

        self._send_gripper(close_cmd, gripper_pause_sec)
        if self._scene is not None:
            self._scene.attach_piece_from_occupancy(source_square, occ)

        if not self._move_to_pose6(source_approach, 'source_retreat'):
            return
        if not self._move_to_pose6(target_approach, 'target_approach'):
            return
        if not self._move_to_pose6(target_pose, 'target_place'):
            return

        self._send_gripper(open_cmd, gripper_pause_sec)
        if self._scene is not None:
            self._scene.detach_piece_to_square(target_square, occ)
        if not self._move_to_pose6(target_approach, 'target_retreat'):
            return
        self._move_joints(list(JOINT_POSES['stand']), 'stand')
        self.node.get_logger().info(f'IK workflow completed: {source_square} -> {target_square}')

    def _execute_joint_workflow(self, occ: dict, source_square: str, target_square: str) -> None:
        timing = self._workflow_timing_and_gripper(occ)
        if timing is None:
            return
        gripper_pause_sec, camera_settle_sec, close_cmd, open_cmd = timing

        source_approach = self._require_joint_pose(
            _source_approach_keys(source_square), 'source_approach'
        )
        if source_approach is None:
            return
        source_pick = self._require_joint_pose(_source_pick_keys(source_square), 'source_pick')
        if source_pick is None:
            return
        target_approach = self._require_joint_pose(
            _target_approach_keys(target_square), 'target_approach'
        )
        if target_approach is None:
            return
        target_place = self._require_joint_pose(_target_place_keys(target_square), 'target_place')
        if target_place is None:
            return

        self.node.get_logger().info(
            f'joint-space workflow start: {source_square} -> {target_square}'
        )

        if not self._move_joints(list(JOINT_POSES['image_1']), 'image_1'):
            return
        time.sleep(camera_settle_sec)

        if not self._move_joints(source_approach, 'source_approach'):
            return
        if not self._move_joints(source_pick, 'source_pick'):
            return

        self._send_gripper(close_cmd, gripper_pause_sec)
        if self._scene is not None:
            self._scene.attach_piece_from_occupancy(source_square, occ)

        if not self._move_joints(source_approach, 'source_retreat'):
            return
        if not self._move_joints(target_approach, 'target_approach'):
            return
        if not self._move_joints(target_place, 'target_place'):
            return

        self._send_gripper(open_cmd, gripper_pause_sec)
        if self._scene is not None:
            self._scene.detach_piece_to_square(target_square, occ)
        if not self._move_joints(target_approach, 'target_retreat'):
            return
        self._move_joints(list(JOINT_POSES['stand']), 'stand')
        self.node.get_logger().info(f'workflow completed: {source_square} -> {target_square}')


def main(args=None):
    rclpy.init(args=args)
    node = Node('chess_move')
    executor = MultiThreadedExecutor()
    executor.add_node(node)

    node.declare_parameter('use_moveit_ik', True)
    node.declare_parameter('ik_service_name', '/compute_ik')
    node.declare_parameter('move_group_name', 'arm')
    node.declare_parameter('planning_frame', 'world')
    node.declare_parameter('joint_states_topic', '/joint_states')
    node.declare_parameter('approach_z_offset', DEFAULT_APPROACH_Z_OFFSET)
    node.declare_parameter('avoid_collisions', False)
    node.declare_parameter('ik_call_timeout_sec', 10.0)
    node.declare_parameter('attach_piece_in_scene', True)
    node.declare_parameter('planning_scene_topic', '/planning_scene')
    node.declare_parameter('planning_frame', 'world')
    node.declare_parameter('ee_link', 'lara5_gripper')
    node.declare_parameter('piece_diameter', 0.035)
    node.declare_parameter('piece_height', 0.05)
    node.declare_parameter('use_convex_hull_collision', True)

    client = node.create_client(MoveJoints, 'move_joints')
    if not client.wait_for_service(timeout_sec=15.0):
        node.get_logger().error(
            'No move_joints — start bringup, then: ros2 run xyz_motion chess_move'
        )
        rclpy.shutdown()
        return

    ik_solver = None
    if bool(node.get_parameter('use_moveit_ik').value):
        ik_solver = MoveItIkSolver(
            node,
            ik_service_name=str(node.get_parameter('ik_service_name').value),
            move_group_name=str(node.get_parameter('move_group_name').value),
            planning_frame=str(node.get_parameter('planning_frame').value),
            avoid_collisions=bool(node.get_parameter('avoid_collisions').value),
            ik_timeout_sec=float(node.get_parameter('ik_call_timeout_sec').value),
        )
        if ik_solver.wait_for_service(timeout_sec=8.0):
            joint_topic = str(node.get_parameter('joint_states_topic').value)

            def _on_joint_state(msg: JointState) -> None:
                ik_solver.set_seed_from_joint_state(msg)

            node.create_subscription(JointState, joint_topic, _on_joint_state, 10)
            node.get_logger().info('MoveIt IK enabled for chess moves with square XYZ')
        else:
            node.get_logger().warning(
                'MoveIt IK service not available — using JOINT_POSES fallback only'
            )
            ik_solver = None

    scene_helper = None
    if bool(node.get_parameter('attach_piece_in_scene').value):
        mesh_library = None
        if bool(node.get_parameter('use_convex_hull_collision').value):
            library = PieceMeshLibrary()
            if library.available():
                mesh_library = library
                node.get_logger().info(f'gripper scene convex hulls from {library.mesh_dir}')
            else:
                node.get_logger().warning(
                    f'convex hull meshes missing in {library.mesh_dir}; using cylinders'
                )
        scene_helper = GripperPlanningScene(
            node,
            planning_scene_topic=str(node.get_parameter('planning_scene_topic').value),
            planning_frame=str(node.get_parameter('planning_frame').value),
            ee_link=str(node.get_parameter('ee_link').value),
            piece_diameter=float(node.get_parameter('piece_diameter').value),
            piece_height=float(node.get_parameter('piece_height').value),
            mesh_library=mesh_library,
        )

    orchestrator = ChessMoveOrchestrator(
        node=node,
        client=client,
        executor=executor,
        ik_solver=ik_solver,
        approach_z_offset=float(node.get_parameter('approach_z_offset').value),
        scene_helper=scene_helper,
    )
    listen_chess_occupancy(node, on_update=orchestrator.start_from_message)

    if not orchestrator._move_joints(list(JOINT_POSES['stand']), 'startup_stand'):
        rclpy.shutdown()
        return

    node.get_logger().info(
        'stand move done — publish /chess_occupancy with source, target, and square XYZ in world frame'
    )
    try:
        orchestrator.executor_running = True
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
