#!/usr/bin/env python3
"""chess_board_server: action server /chess_board (chess_interfaces/action/ChessBoard).

Receives board changes from the chess CV node and moves to make from the Stockfish node:
- change_status = active:  the move already happened on the real board
                           -> PlanningSceneUpdater updates the PlanningScene
- change_status = passive: the robot must make the move
                           -> ArticulationOrchestrator runs one pick-and-place sequence per
                              piece to move (captured pieces first) on MoveItMaster, then the
                              PlanningScene is updated

Chess pieces positions on the board: {square: FEN letter}, e.g. {"e2": "P", "e7": "p"}
(upper case = white). The PlanningScene pieces are kept equal to it: ids "piece_<square>",
geometry and board calibration from lara5_moveit (the same as chess_scene_collisions).
"""
import math
import os
import threading

import yaml
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from ament_index_python.packages import get_package_share_directory

from chess_interfaces.action import ChessBoard
from lara5_moveit.chess_scene_collisions import (
    board_square_object_id, board_surface_z, default_piece_mesh_library, load_board_calibration,
    piece_collision_object, piece_dimensions, piece_object_id, square_center_world)

from articulation_orchestrator.articulation_orchestrator import ArticulationOrchestrator
from articulation_orchestrator.planning_scene_updater import PlanningSceneUpdater

START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
TYPES = {"p": "pawn", "n": "knight", "b": "bishop", "r": "rook", "q": "queen", "k": "king"}
FILES = "abcdefgh"


# ---------- board <-> FEN ----------
def fen_to_board(fen: str) -> dict[str, str]:
    """FEN (piece-placement field is enough) -> {"e2": "P", ...}."""
    rows = fen.split()[0].split("/")
    if len(rows) != 8:
        raise ValueError(f"bad FEN {fen!r}")
    board = {}
    for i, row in enumerate(rows):
        f = 0
        for c in row:
            if c.isdigit():
                f += int(c)
            elif c.lower() in TYPES and f < 8:
                board[f"{FILES[f]}{8 - i}"] = c
                f += 1
            else:
                raise ValueError(f"bad FEN {fen!r}")
        if f != 8:
            raise ValueError(f"bad FEN {fen!r}")
    return board


def board_to_fen(board: dict[str, str]) -> str:
    rows = []
    for rank in range(8, 0, -1):
        row, empty = "", 0
        for f in FILES:
            p = board.get(f"{f}{rank}")
            if p is None:
                empty += 1
            else:
                row, empty = row + (str(empty) if empty else "") + p, 0
        rows.append(row + (str(empty) if empty else ""))
    return "/".join(rows)


# ---------- board changes ----------
def apply_move(board, to_pick, to_place) -> dict[str, str]:
    """Board after a plain move / capture (castling, en passant, promotion need a FEN)."""
    if to_pick not in board:
        raise ValueError(f"no piece on {to_pick!r}")
    target = dict(board)
    target[to_place] = target.pop(to_pick)
    return target


def plan_transfers(board, target, to_pick="") -> list[tuple[str, str | None]]:
    """Physical moves turning `board` into `target`: [(from, to)], to=None -> discard.

    Captured pieces come first (frees the target square). Covers moves, captures,
    en passant and castling. Promotion: the pawn is moved and has to be swapped by hand.
    """
    gone = {sq: p for sq, p in board.items() if target.get(sq) != p}
    new = {sq: p for sq, p in target.items() if board.get(sq) != p}
    moves = []
    for promotion in (False, True):
        for dst, p in sorted(new.items()):
            want = ("P" if p.isupper() else "p") if promotion else p
            if promotion and dst[1] not in "18":
                continue
            src = next((sq for sq in sorted(gone, key=lambda s: s != to_pick) if gone[sq] == want), None)
            if src is not None:
                del gone[src], new[dst]
                moves.append((src, dst))
    if new:
        raise ValueError(f"no piece on the board can get to {sorted(new)}")
    return [(sq, None) for sq in sorted(gone)] + moves


# ---------- server ----------
class ChessBoardServer(Node):
    def __init__(self, orchestrator: ArticulationOrchestrator, scene: PlanningSceneUpdater):
        super().__init__("chess_board_server")
        self.orchestrator, self.scene = orchestrator, scene

        self.declare_parameter("chess_scene_config", os.path.join(
            get_package_share_directory("lara5_moveit"), "config", "chess_scene.yaml"))
        self.declare_parameter("hover_pose_format", "{square}_hover")   # big board: "{square}_hover_big"
        self.declare_parameter("velocity_scaling", 0.2)
        self.declare_parameter("initial_fen", START_FEN)
        self._load_board_geometry()

        self.board = fen_to_board(self.get_parameter("initial_fen").value)
        self._scene_board = {}          # pieces last sent to the PlanningScene
        self._scene_ok = False          # False -> next sync re-adds every piece
        self._busy = threading.Lock()

    def start(self):
        """Call once move_group and moveit_master are up."""
        self.sync_scene(self.board)
        self._server = ActionServer(self, ChessBoard, "chess_board", self.execute,
                                    goal_callback=self._on_goal,
                                    callback_group=ReentrantCallbackGroup())
        self.get_logger().info(f"chess_board ready, board {board_to_fen(self.board)}")

    # ---------- action ----------
    def _on_goal(self, _goal):
        return GoalResponse.ACCEPT if self._busy.acquire(blocking=False) else GoalResponse.REJECT

    def execute(self, goal_handle):
        try:
            ok, msg = True, self._run(goal_handle.request, goal_handle)
            goal_handle.succeed()
        except (ValueError, KeyError, RuntimeError) as e:
            ok, msg = False, str(e)
            goal_handle.abort()
        finally:
            self._busy.release()
        self.get_logger().info(f"{'done' if ok else 'FAILED'}: {msg}")
        return ChessBoard.Result(success=ok, message=msg, fen=board_to_fen(self.board))

    def _run(self, g, goal_handle) -> str:
        to_pick, to_place = g.to_pick.strip().lower(), g.to_place.strip().lower()
        target = fen_to_board(g.fen) if g.fen else apply_move(self.board, to_pick, to_place)

        if g.change_status == ChessBoard.Goal.ACTIVE:
            self._feedback(goal_handle, "planning scene sync")
            self.board = target
            if not self.sync_scene(target):
                raise RuntimeError("planning scene sync failed")
            return "planning scene updated"

        if g.change_status != ChessBoard.Goal.PASSIVE:
            raise ValueError(f"change_status must be '{ChessBoard.Goal.ACTIVE}' or "
                             f"'{ChessBoard.Goal.PASSIVE}', got {g.change_status!r}")
        held = TYPES.get(self.board.get(to_pick, "?").lower())
        if to_pick and g.piece_type and held != g.piece_type:
            raise ValueError(f"goal moves a {g.piece_type} from {to_pick}, board has {held}: "
                             "send an active goal with the FEN to re-sync first")

        for src, dst in plan_transfers(self.board, target, to_pick):
            stage = f"move {src} -> {dst}" if dst else f"capture {src} -> discard"
            self._feedback(goal_handle, stage)
            after_pick = {sq: p for sq, p in self.board.items() if sq != src}
            steps = self.orchestrator.transfer_steps(
                piece_object_id(src), TYPES[self.board[src].lower()],
                self._hover(src), self._support(src),
                dst and self._hover(dst), dst and self._support(dst),
                pick_neighbours=self._neighbours(src, self.board),
                place_neighbours=self._neighbours(dst, after_pick) if dst else ())
            ok, msg = self.orchestrator.run_sequence(
                steps, velocity_scaling=self.get_parameter("velocity_scaling").value)
            if not ok:
                self._scene_ok = False
                raise RuntimeError(f"{stage}: {msg}. Clear the arm, then send an active goal "
                                   "with the FEN of the real board")
            new = dict(self.board)
            piece = new.pop(src)
            if dst:
                new[dst] = piece
            self.board = new
            if not self.sync_scene(new):
                raise RuntimeError(f"{stage}: moved, but planning scene sync failed")

        if self.board != target:
            diff = sorted(sq for sq in self.board.keys() | target.keys()
                          if self.board.get(sq) != target.get(sq))
            return f"moved; board differs from FEN on {diff} (promotion: swap the piece by hand)"
        return "moved"

    def _feedback(self, goal_handle, stage):
        self.get_logger().info(stage)
        goal_handle.publish_feedback(ChessBoard.Feedback(stage=stage))

    def _hover(self, square) -> str:
        return self.get_parameter("hover_pose_format").value.format(square=square)

    def _neighbours(self, square, board) -> list[tuple[float, float, tuple]]:
        """Pieces on the squares around `square`: (dx, dy, profile), world offsets from its
        centre and the piece's radius profile ((z, max radius at or above z), ...) for the
        orchestrator's check against the gripper's wrist block."""
        out = []
        centre = self._centre(square)
        f, r = FILES.index(square[0]), int(square[1])
        for ff in range(max(0, f - 1), min(8, f + 2)):
            for rr in range(max(1, r - 1), min(9, r + 2)):
                sq = f"{FILES[ff]}{rr}"
                if sq == square or sq not in board:
                    continue
                c = self._centre(sq)
                out.append((c[0] - centre[0], c[1] - centre[1],
                             self._profile(TYPES[board[sq].lower()])))
        return out

    def _profile(self, ptype) -> tuple:
        """((z, max radius of the piece at or above z), ...) every 1 mm, z from the board."""
        if ptype not in self._profiles:
            if self._meshes is not None:
                pts = [(v.x, v.y, v.z) for v in self._meshes.get(ptype).mesh.vertices]
            else:
                diameter, height = piece_dimensions(ptype, self._dims)
                pts = [(diameter / 2.0, 0.0, 0.0), (diameter / 2.0, 0.0, height)]
            top = max(p[2] for p in pts)
            zs = [i * 0.001 for i in range(int(top / 0.001) + 1)]
            self._profiles[ptype] = tuple(
                (z, max(math.hypot(x, y) for x, y, pz in pts if pz >= z)) for z in zs)
        return self._profiles[ptype]

    def _centre(self, square):
        g = self._geo
        return square_center_world(self._calib, square, square_size=g["square_size"],
                                   board_layout=g["board_layout"],
                                   file_mirror=g["board_file_mirror"])

    @staticmethod
    def _support(square) -> list[str]:
        """Board squares a lifted / placed piece may touch: the square and its neighbours (the
        piece is pressed onto the board and may sit a few mm off-centre in the gripper)."""
        f, r = FILES.index(square[0]), int(square[1])
        return [board_square_object_id(f"{FILES[ff]}{rr}")
                for ff in range(max(0, f - 1), min(8, f + 2))
                for rr in range(max(1, r - 1), min(9, r + 2))]

    # ---------- planning scene ----------
    def sync_scene(self, board) -> bool:
        """Make the PlanningScene pieces equal `board`: only changed / missing pieces are sent."""
        present = self.scene.object_ids()
        if present is None:
            self._scene_ok = False
            return False
        wanted = {piece_object_id(sq): sq for sq in board}
        objects = [self.scene.make_remove(i) for i in present
                   if i.startswith("piece_") and i not in wanted]
        objects += [self._piece(sq, board[sq]) for i, sq in wanted.items()
                    if not self._scene_ok or i not in present or self._scene_board.get(sq) != board[sq]]
        self._scene_ok = not objects or self.scene.apply(objects)   # ADD replaces existing ids
        self._scene_board = dict(board)
        return self._scene_ok

    def _piece(self, square, letter):
        ptype, g = TYPES[letter.lower()], self._geo
        xyz = square_center_world(self._calib, square, square_size=g["square_size"],
                                  z_board=self._piece_z, board_layout=g["board_layout"],
                                  file_mirror=g["board_file_mirror"])
        diameter, height = piece_dimensions(ptype, self._dims)
        return piece_collision_object(
            square, xyz, frame_id=g["planning_frame"], piece_type=ptype,
            camp="white" if letter.isupper() else "black", diameter=diameter, height=height,
            mesh_library=self._meshes, calib=self._calib, board_layout=g["board_layout"])

    def _load_board_geometry(self):
        """Board calibration from lara5_moveit chess_scene.yaml; each value can be overridden as a
        parameter of this node (e.g. square_size, board_a1/b1/a2 for the big board)."""
        with open(self.get_parameter("chess_scene_config").value) as f:
            cfg = yaml.safe_load(f)["chess_scene_collisions"]["ros__parameters"]
        keys = ("planning_frame", "square_size", "board_thickness", "initial_piece_z", "board_layout",
                "board_file_mirror", "board_a1", "board_b1", "board_a2", "use_convex_hull_collision")
        g = self._geo = {k: self.declare_parameter(k, cfg[k]).value for k in keys}
        self._calib = load_board_calibration(g["board_a1"], g["board_b1"], g["board_a2"], g["square_size"])
        self._piece_z = g["initial_piece_z"] if g["initial_piece_z"] > 0 else board_surface_z(g["board_thickness"])
        meshes = default_piece_mesh_library()
        self._meshes = meshes if g["use_convex_hull_collision"] and meshes.available() else None
        self._dims = cfg.get("piece_dims")
        self._profiles = {}


def main():
    rclpy.init()
    orchestrator, scene = ArticulationOrchestrator(), PlanningSceneUpdater()
    server = ChessBoardServer(orchestrator, scene)
    executor = MultiThreadedExecutor()
    for node in (orchestrator, scene, server):
        executor.add_node(node)
    spinner = threading.Thread(target=executor.spin, daemon=True)
    spinner.start()

    orchestrator.wait_for_master()
    scene.wait_for_move_group()
    server.start()
    try:
        spinner.join()
    except KeyboardInterrupt:
        pass
    rclpy.shutdown()


if __name__ == "__main__":
    main()
