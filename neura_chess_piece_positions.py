"""Kit-side RigidPrim snapshot of OpenChessSet piece poses.

Used by neura_chess_world.py. Client: scripts/scene/pieces_positions_RigidPrim.sh
"""

from __future__ import annotations

import json
import math
import time
from pathlib import Path
from typing import Any, Optional

CHESS_PRIM_PATH = "/World/NeuraChess/ChessSet"
SQUARE = 0.04
BOARD_CENTER_X = 0.43  # = neura_chess_world.BOARD_CENTER_X
BOARD_CENTER_Y = 0.0
BOARD_ORIGIN = -4 * SQUARE  # local XY of square corners
FILE_MIRROR = True
UPRIGHT_TILT_DEG = 25.0
ON_SQUARE_FRAC = 0.5  # residual < half a square

PIECES_REQUEST = Path("/tmp/neura_chess_pieces.request")
PIECES_DONE = Path("/tmp/neura_chess_pieces.done")
PIECES_READY = Path("/tmp/neura_chess_pieces.ready")
PIECES_JSON = Path("/tmp/neura_chess_pieces.json")
PIECES_JSONL = Path("/tmp/neura_chess_pieces.jsonl")
PIECES_RECORD = Path("/tmp/neura_chess_pieces.record")
PIECES_ROS_SERVICE = "/neura_chess/piece_poses"

_KINDS = ("king", "queen", "rook", "bishop", "knight", "pawn")


def log(msg: str) -> None:
    print(f"[neura_chess] {msg}", flush=True)


def _piece_kind(name: str) -> Optional[str]:
    lower = name.lower()
    for kind in _KINDS:
        if kind in lower:
            return kind
    return None


def _piece_color(name: str) -> Optional[str]:
    if name.startswith("W"):
        return "white"
    if name.startswith("B"):
        return "black"
    return None


def isaac_square_algebraic(row: int, col: int, *, file_mirror: bool = False) -> str:
    files = "abcdefgh"
    ranks = "12345678"
    rank_i = int(col)
    file_i = 7 - int(row) if file_mirror else int(row)
    if not (0 <= file_i <= 7 and 0 <= rank_i <= 7):
        raise ValueError(f"row={row} col={col}")
    return f"{files[file_i]}{ranks[rank_i]}"


def _to_numpy(arr: Any):
    import numpy as np

    if arr is None:
        return None
    if hasattr(arr, "numpy"):
        try:
            return arr.numpy()
        except Exception:
            pass
    return np.asarray(arr)


def _tilt_deg(q: Any, q_rest: Any) -> float:
    """Angle between the piece's up axis now and at rest (wxyz quaternions). Turning about the
    vertical (yaw) does not count: a piece spun in place is still upright."""
    import numpy as np

    def rot(qq: Any) -> Any:
        w, x, y, z = np.asarray(qq, dtype=np.float64).reshape(-1)[:4] / np.linalg.norm(qq)
        return np.array([
            [1 - 2 * (y * y + z * z), 2 * (x * y - w * z), 2 * (x * z + w * y)],
            [2 * (x * y + w * z), 1 - 2 * (x * x + z * z), 2 * (y * z - w * x)],
            [2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y)],
        ])

    up_local = rot(q_rest).T @ np.array([0.0, 0.0, 1.0])  # world z at rest, in the piece frame
    return float(np.degrees(math.acos(max(-1.0, min(1.0, float((rot(q) @ up_local)[2]))))))


def snap_board_xy(x: float, y: float) -> dict[str, Any]:
    """World XY → Isaac row/col + algebraic square (ROS file_mirror)."""
    lx = float(x) - BOARD_CENTER_X
    ly = float(y) - BOARD_CENTER_Y
    col_f = (lx - BOARD_ORIGIN) / SQUARE - 0.5
    row_f = (ly - BOARD_ORIGIN) / SQUARE - 0.5
    col = int(round(col_f))
    row = int(round(row_f))
    sx = BOARD_ORIGIN + (col + 0.5) * SQUARE
    sy = BOARD_ORIGIN + (row + 0.5) * SQUARE
    err = math.hypot(lx - sx, ly - sy)
    on_board = 0 <= row <= 7 and 0 <= col <= 7
    square = None
    square_raw = None
    if on_board:
        square = isaac_square_algebraic(row, col, file_mirror=FILE_MIRROR)
        square_raw = isaac_square_algebraic(row, col, file_mirror=False)
    return {
        "row": row,
        "col": col,
        "square": square,
        "square_unmirrored": square_raw,
        "xy_err_m": err,
        "on_board": on_board,
        "on_square": bool(on_board and err < ON_SQUARE_FRAC * SQUARE),
    }


class PiecePositionsRigidPrim:
    """Batched PhysX pose read for the 32 chess pieces."""

    def __init__(self) -> None:
        self._paths: list[str] = []
        self._view: Any = None
        self._rest_quat: dict[str, tuple[float, float, float, float]] = {}
        self._ros_node: Any = None
        self._ros_queued = False
        self._last_record_t = 0.0
        self.ready = False

    def bind(self, stage) -> None:
        from pxr import UsdPhysics

        root = stage.GetPrimAtPath(CHESS_PRIM_PATH)
        paths: list[str] = []
        if root.IsValid():
            for child in root.GetChildren():
                if child.HasAPI(UsdPhysics.RigidBodyAPI) and _piece_kind(child.GetName()):
                    paths.append(str(child.GetPath()))
        paths.sort()
        self._paths = paths
        self._view = None
        if paths:
            try:
                from isaacsim.core.experimental.prims import RigidPrim

                self._view = RigidPrim(paths, resolve_paths=False)
            except Exception as e:
                log(f"WARNING: RigidPrim bind failed (USD fallback): {e}")
        self.ready = True
        try:
            PIECES_READY.write_text(f"pieces={len(paths)}\n", encoding="utf-8")
        except OSError as e:
            log(f"WARNING: could not write pieces ready: {e}")
        log(f"PiecePositions RigidPrim: {len(paths)} pieces → {PIECES_JSON}")
        try:
            snap = self.snapshot(stage)
            for p in snap.get("pieces") or []:
                self._rest_quat[p["prim"]] = (p["qw"], p["qx"], p["qy"], p["qz"])
        except Exception as e:
            log(f"WARNING: rest-pose capture skipped: {e}")

    def attach_ros(self) -> None:
        try:
            import rclpy
            from std_srvs.srv import Trigger
        except Exception as e:
            log(f"PiecePositions ROS skipped: {e}")
            return
        try:
            if not rclpy.ok():
                rclpy.init()
            self._ros_node = rclpy.create_node("neura_chess_piece_poses")

            def _on_req(_req, resp):
                self._ros_queued = True
                resp.success = True
                resp.message = "queued"
                return resp

            self._ros_node.create_service(Trigger, PIECES_ROS_SERVICE, _on_req)
            log(f"PiecePositions ROS: {PIECES_ROS_SERVICE}")
        except Exception as e:
            log(f"WARNING: PiecePositions ROS failed: {e}")
            self._ros_node = None

    def _spin_ros(self) -> None:
        if self._ros_node is None:
            return
        try:
            import rclpy

            rclpy.spin_once(self._ros_node, timeout_sec=0.0)
        except Exception:
            pass

    def _read_poses(self, stage) -> tuple[str, list[str], Any, Any]:
        import numpy as np

        if self._view is not None:
            try:
                pos, quat = self._view.get_world_poses()
                paths = list(self._view.paths)
                return "tensor", paths, _to_numpy(pos), _to_numpy(quat)
            except Exception as e:
                log(f"WARNING: RigidPrim.get_world_poses failed, USD fallback: {e}")

        from pxr import Usd, UsdGeom

        n = len(self._paths)
        pos = np.zeros((n, 3), dtype=np.float64)
        quat = np.zeros((n, 4), dtype=np.float64)
        quat[:, 0] = 1.0
        for i, path in enumerate(self._paths):
            prim = stage.GetPrimAtPath(path)
            if not prim.IsValid():
                continue
            tf = UsdGeom.Xformable(prim).ComputeLocalToWorldTransform(Usd.TimeCode.Default())
            t = tf.ExtractTranslation()
            q = tf.ExtractRotationQuat()
            imag = q.GetImaginary()
            pos[i] = (float(t[0]), float(t[1]), float(t[2]))
            quat[i] = (float(q.GetReal()), float(imag[0]), float(imag[1]), float(imag[2]))
        return "usd", list(self._paths), pos, quat

    def snapshot(self, stage) -> dict[str, Any]:
        import numpy as np

        backend, paths, pos, quat = self._read_poses(stage)
        pos = np.asarray(pos, dtype=np.float64).reshape(-1, 3)
        quat = np.asarray(quat, dtype=np.float64).reshape(-1, 4)
        t_sim = None
        try:
            import omni.timeline

            t_sim = float(omni.timeline.get_timeline_interface().get_current_time())
        except Exception:
            pass

        pieces: list[dict[str, Any]] = []
        occupancy: dict[str, Any] = {}
        displaced: list[str] = []
        conflicts: dict[str, list[str]] = {}

        n = min(len(paths), pos.shape[0], quat.shape[0])
        for i in range(n):
            path = paths[i]
            name = path.rsplit("/", 1)[-1]
            x, y, z = (float(pos[i, 0]), float(pos[i, 1]), float(pos[i, 2]))
            qw, qx, qy, qz = (float(quat[i, 0]), float(quat[i, 1]), float(quat[i, 2]), float(quat[i, 3]))
            kind = _piece_kind(name) or "unknown"
            color = _piece_color(name)
            board = snap_board_xy(x, y)
            rest = self._rest_quat.get(path)
            tilt = _tilt_deg((qw, qx, qy, qz), rest) if rest is not None else None
            upright = None if tilt is None else bool(tilt < UPRIGHT_TILT_DEG)
            row = {
                "prim": path,
                "name": name,
                "type": kind,
                "color": color,
                "x": x,
                "y": y,
                "z": z,
                "qw": qw,
                "qx": qx,
                "qy": qy,
                "qz": qz,
                "tilt_deg": tilt,
                "upright": upright,
                **board,
            }
            pieces.append(row)
            sq = board["square"]
            ok = bool(board["on_square"] and upright is not False)
            if ok and sq:
                if sq in occupancy:
                    conflicts.setdefault(sq, [occupancy[sq]["name"]]).append(name)
                occupancy[sq] = {
                    "x": x,
                    "y": y,
                    "z": z,
                    "type": kind,
                    "color": color,
                    "name": name,
                }
            else:
                displaced.append(name)

        squares = {
            sq: {k: v for k, v in rec.items() if k != "name"}
            for sq, rec in occupancy.items()
        }
        return {
            "t_unix": time.time(),
            "t_sim": t_sim,
            "backend": backend,
            "n": len(pieces),
            "file_mirror": FILE_MIRROR,
            "pieces": pieces,
            "occupancy": occupancy,
            "squares": squares,
            "displaced": displaced,
            "conflicts": conflicts,
        }

    def write_snapshot(self, stage, *, jsonl: bool = False) -> dict[str, Any]:
        snap = self.snapshot(stage)
        text = json.dumps(snap, indent=2 if not jsonl else None)
        if jsonl:
            with PIECES_JSONL.open("a", encoding="utf-8") as f:
                f.write(json.dumps(snap, separators=(",", ":")) + "\n")
        tmp = PIECES_JSON.with_suffix(".json.tmp")
        tmp.write_text(text + "\n", encoding="utf-8")
        tmp.replace(PIECES_JSON)
        return snap

    def _write_done(self, snap: dict[str, Any]) -> None:
        n = int(snap.get("n") or 0)
        n_occ = len(snap.get("occupancy") or {})
        n_disp = len(snap.get("displaced") or [])
        body = (
            f"ok n={n} occupancy={n_occ} displaced={n_disp} "
            f"backend={snap.get('backend')} t_sim={snap.get('t_sim')}\n"
        )
        try:
            PIECES_DONE.write_text(body, encoding="utf-8")
        except OSError as e:
            log(f"WARNING: could not write pieces done: {e}")

    def poll(self, stage) -> None:
        if not self.ready:
            return
        try:
            self._spin_ros()
            if PIECES_RECORD.is_file():
                try:
                    hz = float(PIECES_RECORD.read_text(encoding="utf-8").strip() or "0")
                except ValueError:
                    hz = 0.0
                now = time.perf_counter()
                period = 0.0 if hz <= 0.0 else 1.0 / hz
                if now - self._last_record_t >= period:
                    self._last_record_t = now
                    self.write_snapshot(stage, jsonl=True)

            triggered = bool(self._ros_queued)
            self._ros_queued = False
            if PIECES_REQUEST.is_file():
                try:
                    PIECES_REQUEST.unlink()
                    triggered = True
                except OSError:
                    pass
            if not triggered:
                return
            try:
                PIECES_DONE.unlink(missing_ok=True)
            except TypeError:
                if PIECES_DONE.exists():
                    PIECES_DONE.unlink()
            except OSError:
                pass
            snap = self.write_snapshot(stage, jsonl=False)
            self._write_done(snap)
            log(
                f"PiecePositions n={snap['n']} occupancy={len(snap['occupancy'])} "
                f"displaced={len(snap['displaced'])} backend={snap['backend']}"
            )
        except Exception as e:
            import traceback

            log(f"ERROR: PiecePositions poll: {e}\n{traceback.format_exc()}")
            try:
                PIECES_DONE.write_text(f"error: {e}\n", encoding="utf-8")
            except OSError:
                pass
