#!/usr/bin/env python3
"""Neura Lara5 PhysX world + isaacsim.ros2.bridge.

Imports the Lara5 URDF (from ros2_ws/lara5_description, copied under assets/)
and drives it with OmniGraph + a Kit JointState subscriber:
  /isaac_joint_commands → position targets → /isaac_joint_states
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any, Optional

ROOT = Path(os.environ.get("NEURA_CHESS_WORLD_ROOT", Path(__file__).resolve().parent))
ASSETS = ROOT / "assets"

LARA_DESC = ASSETS / "neura_lara5"
LARA_URDF = LARA_DESC / "urdf" / "lara5.urdf"
LARA_URDF_REL = LARA_DESC / "urdf" / "lara5_relmeshes.urdf"

WORLD = "/World/NeuraChess"
LARA_PRIM_PATH = f"{WORLD}/lara5"
CHESS_PRIM_PATH = f"{WORLD}/ChessSet"
GROUND_PATH = f"{WORLD}/Ground"
PHYSICS_SCENE = "/physicsScene"

CHESS_PIECE_DIR = ASSETS / "OpenChessSet" / "assets"
CHESS_PIECE_USDS = {
    "pawn": CHESS_PIECE_DIR / "Pawn" / "Pawn.usd",
    "rook": CHESS_PIECE_DIR / "Rook" / "Rook.usd",
    "knight": CHESS_PIECE_DIR / "Knight" / "Knight.usd",
    "bishop": CHESS_PIECE_DIR / "Bishop" / "Bishop.usd",
    "queen": CHESS_PIECE_DIR / "Queen" / "Queen.usd",
    "king": CHESS_PIECE_DIR / "King" / "King.usd",
}
# OpenChessSet is authored for ~62.5 mm squares; scale to this board.
CHESS_PIECE_NATIVE_SQUARE_M = 0.0625
# In front of Lara: ranks along +X (white near the base), files along +Y.
# Matches ros2_ws chess_scene.yaml: board_a1 (0.27, -0.16, 0.02) is the a1 *corner* on the
# board top, 40 mm squares, centred on the arm in y.
SQUARE = 0.04
BOARD_THICKNESS = 0.02
BOARD_HALF_M = 4 * SQUARE
BOARD_CENTER_X = 0.27 + 4 * SQUARE  # 0.43 m
BOARD_CENTER_Y = 0.0
CHESS_PIECE_MASS_KG = {
    "king": 0.016,
    "queen": 0.014,
    "rook": 0.010,
    "bishop": 0.008,
    "knight": 0.008,
    "pawn": 0.0055,
}
BOARD_DENSITY_KG_M3 = 650.0
BOARD_STATIC_FRICTION = 0.45
BOARD_DYNAMIC_FRICTION = 0.35
BOARD_RESTITUTION = 0.04
PIECE_STATIC_FRICTION = 0.40
PIECE_DYNAMIC_FRICTION = 0.30
PIECE_RESTITUTION = 0.06
PIECE_TORSIONAL_PATCH_RADIUS = 0.003  # m
PIECE_MAX_DEPENETRATION_VELOCITY = 0.1  # m/s
HULL_VERTEX_LIMIT = 255  # PhysX convex hull vertices (pieces and robot meshes; default 64)
# Pad on the static finger (gripper body): pieces stay put against it while carried. The moving
# jaw keeps the default material: it needs friction too (a frictionless jaw lets the piece turn
# about the pad contact and fall out), but a pad on it drags placed pieces along its opening arc.
GRIPPER_PAD_FRICTION = 1.0
GRIPPER_PAD_LINKS = ("lara5_gripper_body",)

# USD angular drives: N*m/deg and N*m*s/deg. Stiff arm drives keep the gravity sag well below
# 1 mm at the TCP; the damping stays ~2.5x critical.
JOINT_STIFFNESS = 2000.0
JOINT_DAMPING = 40.0
# Jaw: soft spring, so a position target past the contact squeezes the piece with
# ~stiffness * overshoot: the close position (objects_dictionary.yaml) is ~0.3 rad past the
# predicted contact (up to ~1.2 N*m, ~15 N at the fingertips). Stiffer drives (0.2 and
# 0.5 N*m/deg tried) knock light pieces (pawns) over or push them away instead of gripping.
# Damping: time constant ~0.3 s, the jaw does not slam into (and tip over) the piece.
GRIPPER_STIFFNESS = 0.07  # N*m/deg (~4 N*m/rad)
GRIPPER_DAMPING = 0.02    # N*m*s/deg
GRIPPER_MAX_FORCE = 1.5   # N*m, safety cap
ARM_JOINT_NAMES = (
    "lara5_joint1",
    "lara5_joint2",
    "lara5_joint3",
    "lara5_joint4",
    "lara5_joint5",
    "lara5_joint6",
)
GRIPPER_JOINT_NAMES = ("lara5_gripper_finger_joint",)
ALL_DOF_JOINT_NAMES = ARM_JOINT_NAMES + GRIPPER_JOINT_NAMES

JOINT_COMMANDS_TOPIC = "isaac_joint_commands"
JOINT_STATES_TOPIC = "isaac_joint_states"
# Fast IPC for scripts/scene/chess_scene_restore.sh (no extra ROS node in Kit).
RESTORE_REQUEST = Path("/tmp/neura_chess_restore.request")
RESTORE_DONE = Path("/tmp/neura_chess_restore.done")
RESTORE_READY = Path("/tmp/neura_chess_restore.ready")
RESTORE_ROS_SERVICE = "/neura_chess/restore_scene"


def log(msg: str) -> None:
    print(f"[neura_chess] {msg}", flush=True)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Neura Lara5 PhysX + ROS2 bridge world")
    p.add_argument("--headless", action="store_true")
    p.add_argument("--ros", action="store_true", default=True, help=argparse.SUPPRESS)
    p.add_argument("--physics", action="store_true", default=True, help=argparse.SUPPRESS)
    p.add_argument("--no-ros", action="store_true", help="Skip isaacsim.ros2.bridge")
    return p.parse_args()


def ensure_relative_urdf() -> Path:
    if not LARA_URDF.is_file():
        raise FileNotFoundError(f"Missing Lara5 URDF: {LARA_URDF}")
    text = LARA_URDF.read_text(encoding="utf-8")
    text = text.replace("package://lara5_description/lara5/meshes/", "../meshes/")
    text = text.replace("package://lara5_description/lara5/collision/", "../collision/")
    # Isaac fix_base authors Physics/root_joint; drop the URDF world mount.
    text = re.sub(
        r'\s*<link name="world"/>\s*<joint name="world_joint"[^>]*>.*?</joint>',
        "\n",
        text,
        count=1,
        flags=re.DOTALL,
    )
    LARA_URDF_REL.parent.mkdir(parents=True, exist_ok=True)
    LARA_URDF_REL.write_text(text, encoding="utf-8")
    return LARA_URDF_REL


def _strip_articulation_root_schemas(prim) -> None:
    from pxr import UsdPhysics

    try:
        if prim.HasAPI(UsdPhysics.ArticulationRootAPI):
            prim.RemoveAPI(UsdPhysics.ArticulationRootAPI)
    except Exception:
        pass
    for schema in (
        "PhysxArticulationAPI",
        "PhysicsArticulationRootAPI",
        "NewtonArticulationRootAPI",
    ):
        try:
            prim.RemoveAppliedSchema(schema)
        except Exception:
            pass


def _force_physx(stage) -> None:
    """Isaac Sim 6 can default to Newton, which has no PhysX Articulation GUI panel."""
    try:
        from isaacsim.core.simulation_manager import SimulationManager

        SimulationManager.switch_physics_engine("physx", verbose=True)
        log(f"Physics engine={SimulationManager.get_active_physics_engine()}")
    except Exception as e:
        log(f"WARNING: could not switch physics engine to PhysX: {e}")
    try:
        from pxr import PhysxSchema

        scene = stage.GetPrimAtPath(PHYSICS_SCENE)
        if scene.IsValid():
            PhysxSchema.PhysxSceneAPI.Apply(scene)
    except Exception as e:
        log(f"WARNING: PhysxSceneAPI: {e}")


def apply_joint_drives(stage, robot_root: str) -> None:
    """Position drives strong enough for ROS joint commands (URDF import stores ~7)."""
    from pxr import Usd, UsdPhysics

    robot = stage.GetPrimAtPath(robot_root)
    if not robot.IsValid():
        return
    n = n_gripper = 0
    for prim in Usd.PrimRange(robot):
        if prim.IsA(UsdPhysics.RevoluteJoint):
            axis = "angular"
        elif prim.IsA(UsdPhysics.PrismaticJoint):
            axis = "linear"
        else:
            continue
        gripper = prim.GetName() in GRIPPER_JOINT_NAMES
        drive = UsdPhysics.DriveAPI.Apply(prim, axis)
        drive.CreateStiffnessAttr().Set(float(GRIPPER_STIFFNESS if gripper else JOINT_STIFFNESS))
        drive.CreateDampingAttr().Set(float(GRIPPER_DAMPING if gripper else JOINT_DAMPING))
        drive.CreateTypeAttr().Set("force")
        if gripper:
            drive.CreateMaxForceAttr().Set(float(GRIPPER_MAX_FORCE))
            n_gripper += 1
        n += 1
    log(f"Joint drives stiffness={JOINT_STIFFNESS} damping={JOINT_DAMPING} on {n} joints, "
        f"{n_gripper} gripper: stiffness={GRIPPER_STIFFNESS} damping={GRIPPER_DAMPING} "
        f"max_force={GRIPPER_MAX_FORCE}")


def apply_gripper_pads(stage, robot_root: str) -> None:
    """High-friction physics material on the static finger (gripper body)."""
    from pxr import PhysxSchema, Usd, UsdPhysics, UsdShade

    material = UsdShade.Material.Define(stage, f"{robot_root}/Looks/PhysicsGripperPad")
    api = UsdPhysics.MaterialAPI.Apply(material.GetPrim())
    api.CreateStaticFrictionAttr(GRIPPER_PAD_FRICTION)
    api.CreateDynamicFrictionAttr(GRIPPER_PAD_FRICTION)
    api.CreateRestitutionAttr(0.0)
    PhysxSchema.PhysxMaterialAPI.Apply(material.GetPrim()).CreateFrictionCombineModeAttr("max")
    n = 0
    for prim in Usd.PrimRange(stage.GetPrimAtPath(robot_root)):
        if prim.GetName() in GRIPPER_PAD_LINKS:
            UsdShade.MaterialBindingAPI.Apply(prim).Bind(
                material, UsdShade.Tokens.weakerThanDescendants, "physics")
            n += 1
    log(f"Gripper pad friction={GRIPPER_PAD_FRICTION} (max combine) on {n} links")


def ensure_physx_articulation(simulation_app: Any, robot_root: str) -> str:
    """Put ArticulationRootAPI on the instance prim the Stage tree selects.

    The URDF importer authors PhysicsArticulationRootAPI on Geometry/lara5_root_link.
    Selecting /World/NeuraChess/lara5 then shows no Articulation panel, and
    IsaacArticulationController may not drive the referenced payload.
    """
    import omni.usd
    from pxr import PhysxSchema, Usd, UsdPhysics

    stage = omni.usd.get_context().get_stage()
    _force_physx(stage)
    root = stage.GetPrimAtPath(robot_root)
    if not root.IsValid():
        raise RuntimeError(f"Robot root missing: {robot_root}")

    stripped: list[str] = []
    for p in list(Usd.PrimRange(root)):
        if p == root or not p.HasAPI(UsdPhysics.ArticulationRootAPI):
            continue
        stripped.append(str(p.GetPath()))
        _strip_articulation_root_schemas(p)

    UsdPhysics.ArticulationRootAPI.Apply(root)
    try:
        # A fresh PhysxArticulationAPI enables self-collisions (the importer's
        # allow_self_collision=False sat on the stripped root): the jaw hub overlaps the
        # link6 convex hull, so PhysX would keep pushing the jaw shut.
        PhysxSchema.PhysxArticulationAPI.Apply(root).CreateEnabledSelfCollisionsAttr().Set(False)
    except Exception as e:
        log(f"PhysxArticulationAPI note: {e}")

    if stripped:
        log(f"Moved ArticulationRootAPI from {stripped} → {robot_root}")

    roots = [
        str(p.GetPath())
        for p in Usd.PrimRange(root)
        if p.HasAPI(UsdPhysics.ArticulationRootAPI)
    ]
    if roots != [robot_root]:
        log(f"WARNING: ArticulationRootAPI prims under {robot_root}: {roots}")
    else:
        log(f"ArticulationRootAPI on {robot_root} (select this prim for the Articulation panel)")
    apply_joint_drives(stage, robot_root)
    apply_gripper_pads(stage, robot_root)
    n_hull = 0
    for p in Usd.PrimRange(root):
        if p.HasAPI(UsdPhysics.MeshCollisionAPI):
            PhysxSchema.PhysxConvexHullCollisionAPI.Apply(p).CreateHullVertexLimitAttr(
                HULL_VERTEX_LIMIT)
            n_hull += 1
    log(f"Convex hull vertex limit {HULL_VERTEX_LIMIT} on {n_hull} robot collision meshes")
    for _ in range(3):
        simulation_app.update()
    return robot_root


def _log_live_articulation(robot_path: str) -> None:
    try:
        from isaacsim.core.experimental.prims import Articulation
        from isaacsim.core.simulation_manager import SimulationManager

        art = Articulation(robot_path)
        log(
            f"Live articulation engine={SimulationManager.get_active_physics_engine()} "
            f"path={robot_path} dofs={art.num_dofs} names={art.dof_names}"
        )
    except Exception as e:
        log(f"WARNING: live articulation probe failed: {e}")


class JointCommandApplier:
    """Apply /isaac_joint_commands positions onto the live articulation.

    Isaac ROS2SubscribeJointState.checkValid() requires name, position, velocity,
    and effort arrays to be the same length. topic_based_ros2_control publishes
    positions only (empty velocity/effort), so OmniGraph drops every command.
    Connecting those empty arrays as zeros would also pin velocity targets at 0.
    """

    def __init__(self, robot_path: str) -> None:
        self._path = robot_path
        self._art = None
        self._node = None
        self._latest = None
        self._applied = 0
        self._fails = 0

    def attach_ros(self) -> None:
        try:
            import rclpy
            from sensor_msgs.msg import JointState
        except Exception as e:
            log(f"JointCommandApplier ROS skipped: {e}")
            return
        try:
            if not rclpy.ok():
                rclpy.init()
            self._node = rclpy.create_node("neura_chess_joint_commands")
            self._node.create_subscription(JointState, f"/{JOINT_COMMANDS_TOPIC}", self._on_cmd, 10)
            log(f"JointCommandApplier sub=/{JOINT_COMMANDS_TOPIC} robot={self._path}")
        except Exception as e:
            log(f"WARNING: JointCommandApplier ROS failed: {e}")
            self._node = None

    def _on_cmd(self, msg) -> None:
        self._latest = msg

    def _ensure_art(self) -> bool:
        if self._art is not None:
            try:
                if self._art.valid:
                    return True
            except Exception:
                self._art = None
        try:
            from isaacsim.core.experimental.prims import Articulation

            self._art = Articulation(self._path)
            return bool(self._art.valid)
        except Exception as e:
            self._art = None
            self._fails += 1
            if self._fails <= 3 or self._fails % 200 == 0:
                log(f"WARNING: JointCommandApplier Articulation({self._path}): {e}")
            return False

    def _apply(self, msg) -> None:
        import numpy as np

        n = min(len(msg.name), len(msg.position))
        if n == 0 or not self._ensure_art():
            return
        names = list(msg.name[:n])
        pos = np.asarray(msg.position[:n], dtype=np.float64)
        indices = self._art.get_dof_indices(names).numpy().flatten()
        self._art.set_dof_position_targets(pos, dof_indices=indices)
        self._applied += 1
        if self._applied == 1 or self._applied % 500 == 0:
            log(
                f"JointCommandApplier applied={self._applied} n={n} "
                f"{names[0]}={float(pos[0]):.4f}"
            )

    def poll(self) -> None:
        node = self._node
        if node is None:
            return
        try:
            import rclpy

            for _ in range(32):
                rclpy.spin_once(node, timeout_sec=0.0)
        except Exception:
            return
        msg = self._latest
        self._latest = None
        if msg is None:
            return
        try:
            self._apply(msg)
        except Exception as e:
            self._art = None
            self._fails += 1
            if self._fails <= 3 or self._fails % 200 == 0:
                log(f"WARNING: JointCommandApplier: {e}")


def add_simple_chess(stage, parent_path: str = CHESS_PRIM_PATH) -> None:
    """Procedural board + OpenChessSet pieces, white near the Lara base (−X of board)."""
    from pxr import Gf, Sdf, Usd, UsdGeom, UsdShade

    root = stage.DefinePrim(parent_path, "Xform")
    xf = UsdGeom.Xformable(root)
    xf.ClearXformOpOrder()
    xf.AddTranslateOp().Set(Gf.Vec3d(BOARD_CENTER_X, BOARD_CENTER_Y, 0.0))

    light = (0.92, 0.85, 0.70)
    dark = (0.25, 0.18, 0.12)
    origin = -4 * SQUARE

    def make_cube(path, translate, scale, color):
        cube = UsdGeom.Cube.Define(stage, Sdf.Path(path))
        cube.CreateSizeAttr(1.0)
        cx = UsdGeom.Xformable(cube.GetPrim())
        cx.ClearXformOpOrder()
        cx.AddTranslateOp().Set(Gf.Vec3d(*translate))
        cx.AddScaleOp().Set(Gf.Vec3f(*scale))
        cube.CreateDisplayColorAttr([Gf.Vec3f(*color)])

    for row in range(8):
        for col in range(8):
            is_dark = (row + col) % 2 == 1
            x = origin + (col + 0.5) * SQUARE
            y = origin + (row + 0.5) * SQUARE
            make_cube(
                f"{parent_path}/sq_{row}_{col}",
                (x, y, BOARD_THICKNESS * 0.5),
                (SQUARE * 0.98, SQUARE * 0.98, BOARD_THICKNESS),
                dark if is_dark else light,
            )

    piece_scale = SQUARE / CHESS_PIECE_NATIVE_SQUARE_M
    for kind, usd_path in CHESS_PIECE_USDS.items():
        if not usd_path.is_file():
            raise FileNotFoundError(f"Missing chess piece USD ({kind}): {usd_path}")
    log("Referencing OpenChessSet USDs (first MDL compile can take several minutes)...")

    stage.DefinePrim(f"{parent_path}/Looks", "Scope")
    preview_mats: dict[tuple[str, bool], UsdShade.Material] = {}
    piece_albedo = {
        "king": (
            CHESS_PIECE_USDS["king"].parent / "tex" / "king_white_base_color.jpg",
            CHESS_PIECE_USDS["king"].parent / "tex" / "king_black_base_color.jpg",
        ),
        "queen": (
            CHESS_PIECE_USDS["queen"].parent / "tex" / "queen_white_base_color.jpg",
            CHESS_PIECE_USDS["queen"].parent / "tex" / "queen_black_base_color.jpg",
        ),
    }

    def preview_material(kind: str, white: bool) -> UsdShade.Material:
        key = (kind, white)
        if key in preview_mats:
            return preview_mats[key]
        side = "W" if white else "B"
        mat_path = f"{parent_path}/Looks/M_{kind}_{side}"
        material = UsdShade.Material.Define(stage, mat_path)
        shader = UsdShade.Shader.Define(stage, f"{mat_path}/PreviewSurface")
        shader.CreateIdAttr("UsdPreviewSurface")
        shader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.45)
        shader.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(0.0)
        tex_path = piece_albedo[kind][0 if white else 1]
        if tex_path.is_file():
            tex = UsdShade.Shader.Define(stage, f"{mat_path}/AlbedoTex")
            tex.CreateIdAttr("UsdUVTexture")
            tex.CreateInput("file", Sdf.ValueTypeNames.Asset).Set(str(tex_path))
            tex.CreateInput("sourceColorSpace", Sdf.ValueTypeNames.Token).Set("sRGB")
            tex.CreateOutput("rgb", Sdf.ValueTypeNames.Float3)
            shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).ConnectToSource(
                tex.ConnectableAPI(), "rgb"
            )
        else:
            rgb = Gf.Vec3f(0.93, 0.90, 0.82) if white else Gf.Vec3f(0.06, 0.06, 0.06)
            shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set(rgb)
        material.CreateSurfaceOutput().ConnectToSource(shader.ConnectableAPI(), "surface")
        preview_mats[key] = material
        return material

    def bind_preview_color(piece_prim, kind: str, *, white: bool) -> None:
        material = preview_material(kind, white)
        for child in Usd.PrimRange(piece_prim):
            if child.GetName() != "Render" and not child.IsA(UsdGeom.Mesh):
                continue
            api = UsdShade.MaterialBindingAPI.Apply(child)
            api.Bind(material, UsdShade.Tokens.strongerThanDescendants)

    white_back = -3.5 * SQUARE
    white_pawn = -2.5 * SQUARE
    black_pawn = 2.5 * SQUARE
    black_back = 3.5 * SQUARE
    # sq row 0 (-Y) is the h-file (ROS board_file_mirror): h..a -> king on e, queen on d
    back_order = ["rook", "knight", "bishop", "king", "queen", "bishop", "knight", "rook"]

    def place_piece(kind: str, prim_path: str, x_row: float, y: float, *, white: bool) -> None:
        usd_path = CHESS_PIECE_USDS[kind]
        prim = stage.DefinePrim(prim_path, "Xform")
        prim.GetReferences().AddReference(str(usd_path))
        vset = prim.GetVariantSet("shadingVariant")
        selection = "White" if white else "Black"
        if vset:
            vset.SetVariantSelection(selection)
        prim_spec = stage.GetRootLayer().GetPrimAtPath(prim.GetPath())
        if prim_spec is not None:
            prim_spec.variantSelections["shadingVariant"] = selection

        yaw_deg = 0.0 if white else 180.0
        px = UsdGeom.Xformable(prim)
        px.ClearXformOpOrder()
        t_op = px.AddTranslateOp()
        t_op.Set(Gf.Vec3d(x_row, y, 0.0))
        px.AddRotateZOp().Set(yaw_deg)
        px.AddRotateXOp().Set(90.0)
        px.AddScaleOp().Set(Gf.Vec3f(piece_scale, piece_scale, piece_scale))

        bbox_cache = UsdGeom.BBoxCache(Usd.TimeCode.Default(), [UsdGeom.Tokens.default_])
        bound = bbox_cache.ComputeLocalBound(prim)
        if bound.GetRange().IsEmpty():
            extents = {
                "pawn": 0.014926995,
                "rook": 0.0008221504,
                "knight": 0.01870833,
                "bishop": 0.018705152,
                "queen": 0.018983757,
                "king": 0.006083087,
            }
            z_min = piece_scale * extents[kind]
        else:
            z_min = bound.GetRange().GetMin()[2]
        t_op.Set(Gf.Vec3d(x_row, y, BOARD_THICKNESS - z_min))

        if kind in ("king", "queen"):
            bind_preview_color(prim, kind, white=white)

    def place_row(kind_row, x_row, *, white: bool, prefix: str) -> None:
        for col, kind in enumerate(kind_row):
            y = origin + (col + 0.5) * SQUARE
            place_piece(
                kind,
                f"{parent_path}/{prefix}_{kind}_{col}",
                x_row,
                y,
                white=white,
            )

    place_row(back_order, white_back, white=True, prefix="W")
    place_row(["pawn"] * 8, white_pawn, white=True, prefix="Wp")
    place_row(["pawn"] * 8, black_pawn, white=False, prefix="Bp")
    place_row(back_order, black_back, white=False, prefix="B")
    log(
        f"OpenChessSet on board at ({BOARD_CENTER_X:.2f}, {BOARD_CENTER_Y:.2f}), "
        f"square={SQUARE:.3f} m, white near arm"
    )


def _piece_kind_from_prim_name(name: str) -> Optional[str]:
    lower = name.lower()
    for kind in sorted(CHESS_PIECE_MASS_KG, key=len, reverse=True):
        if kind in lower:
            return kind
    return None


def isaac_square_algebraic(row: int, col: int, *, file_mirror: bool = False) -> str:
    """Map procedural ``sq_{row}_{col}`` (row→+Y/file, col→+X/rank) to algebraic."""
    files = "abcdefgh"
    ranks = "12345678"
    rank_i = int(col)
    file_i = 7 - int(row) if file_mirror else int(row)
    return f"{files[file_i]}{ranks[rank_i]}"


def log_chess_board_frames(stage, parent_path: str = CHESS_PRIM_PATH) -> None:
    """Log board normal and a1/e2/e4 world poses for TF alignment with ROS grasp_tf."""
    from pxr import Usd, UsdGeom

    root = stage.GetPrimAtPath(parent_path)
    if not root.IsValid():
        return
    xform = UsdGeom.Xformable(root)
    world_tf = xform.ComputeLocalToWorldTransform(Usd.TimeCode.Default())
    rot = world_tf.ExtractRotationQuat()
    # Gf.Quatd: GetReal/GetImaginary; rotate local +Z into world.
    try:
        from pxr import Gf

        local_z = Gf.Vec3d(0, 0, 1)
        normal = Gf.Rotation(rot).TransformDir(local_z)
    except Exception:
        normal = (0.0, 0.0, 1.0)
    log(f"ChessSet world origin={tuple(world_tf.ExtractTranslation())} normal={tuple(normal)}")
    for name in ("sq_0_0", "sq_4_1", "sq_4_3"):  # a1, e2, e4 when file_mirror=false
        prim = stage.GetPrimAtPath(f"{parent_path}/{name}")
        if not prim.IsValid():
            continue
        xf = UsdGeom.Xformable(prim)
        tf = xf.ComputeLocalToWorldTransform(Usd.TimeCode.Default())
        pos = tf.ExtractTranslation()
        row_col = name.replace("sq_", "").split("_")
        square = isaac_square_algebraic(int(row_col[0]), int(row_col[1]))
        log(f"  {name} → {square} world=({pos[0]:.3f}, {pos[1]:.3f}, {pos[2]:.3f})")
    log("ROS grasp TF is published by xyz_motion/publish_grasp_tf (not Isaac).")


def apply_chess_physics(stage, parent_path: str = CHESS_PRIM_PATH) -> None:
    """Static board squares + dynamic piece rigid bodies."""
    from pxr import PhysxSchema, Usd, UsdGeom, UsdPhysics, UsdShade

    root = stage.GetPrimAtPath(parent_path)
    if not root.IsValid():
        raise RuntimeError(f"Chess root missing for physics: {parent_path}")

    stage.DefinePrim(f"{parent_path}/Looks", "Scope")

    def make_physics_material(
        name: str,
        *,
        static_friction: float,
        dynamic_friction: float,
        restitution: float,
    ) -> UsdShade.Material:
        mat_path = f"{parent_path}/Looks/{name}"
        material = UsdShade.Material.Define(stage, mat_path)
        api = UsdPhysics.MaterialAPI.Apply(material.GetPrim())
        api.CreateStaticFrictionAttr(static_friction)
        api.CreateDynamicFrictionAttr(dynamic_friction)
        api.CreateRestitutionAttr(restitution)
        try:
            physx_mat = PhysxSchema.PhysxMaterialAPI.Apply(material.GetPrim())
            physx_mat.CreateFrictionCombineModeAttr("average")
            physx_mat.CreateRestitutionCombineModeAttr("min")
        except Exception as e:
            log(f"PhysxMaterialAPI note ({name}): {e}")
        return material

    board_mat = make_physics_material(
        "PhysicsBoardWood",
        static_friction=BOARD_STATIC_FRICTION,
        dynamic_friction=BOARD_DYNAMIC_FRICTION,
        restitution=BOARD_RESTITUTION,
    )
    piece_mat = make_physics_material(
        "PhysicsPiece",
        static_friction=PIECE_STATIC_FRICTION,
        dynamic_friction=PIECE_DYNAMIC_FRICTION,
        restitution=PIECE_RESTITUTION,
    )

    def bind_physics_material(prim, material: UsdShade.Material) -> None:
        binding = UsdShade.MaterialBindingAPI.Apply(prim)
        binding.Bind(material, UsdShade.Tokens.weakerThanDescendants, "physics")

    n_squares = 0
    n_pieces = 0
    for child in root.GetChildren():
        name = child.GetName()
        if name == "Looks":
            continue
        if name.startswith("sq_"):
            if not child.HasAPI(UsdPhysics.CollisionAPI):
                UsdPhysics.CollisionAPI.Apply(child)
            try:
                if not child.HasAPI(PhysxSchema.PhysxCollisionAPI):
                    PhysxSchema.PhysxCollisionAPI.Apply(child)
                PhysxSchema.PhysxCollisionAPI(child).CreateContactOffsetAttr(0.002)
                PhysxSchema.PhysxCollisionAPI(child).CreateRestOffsetAttr(0.0)
            except Exception as e:
                log(f"PhysxCollisionAPI on {child.GetPath()} note: {e}")
            bind_physics_material(child, board_mat)
            n_squares += 1
            continue

        kind = _piece_kind_from_prim_name(name)
        if kind is None:
            continue

        if not child.HasAPI(UsdPhysics.RigidBodyAPI):
            UsdPhysics.RigidBodyAPI.Apply(child)
        mass_api = UsdPhysics.MassAPI.Apply(child)
        mass_api.CreateMassAttr(CHESS_PIECE_MASS_KG[kind])
        mass_api.CreateDensityAttr(800.0)
        try:
            if not child.HasAPI(PhysxSchema.PhysxRigidBodyAPI):
                PhysxSchema.PhysxRigidBodyAPI.Apply(child)
            prb = PhysxSchema.PhysxRigidBodyAPI(child)
            prb.CreateLinearDampingAttr(0.8)
            prb.CreateAngularDampingAttr(1.5)
            prb.CreateEnableCCDAttr(True)
            prb.CreateSolverPositionIterationCountAttr(16)
            # a piece released from a slightly overlapping grip must not be shot away
            prb.CreateMaxDepenetrationVelocityAttr(PIECE_MAX_DEPENETRATION_VELOCITY)
            prb.CreateSolverVelocityIterationCountAttr(4)
        except Exception as e:
            log(f"PhysxRigidBodyAPI on {child.GetPath()} note: {e}")
        bind_physics_material(child, piece_mat)

        mesh_n = 0
        for prim in Usd.PrimRange(child):
            if not prim.IsA(UsdGeom.Mesh):
                continue
            if not prim.HasAPI(UsdPhysics.CollisionAPI):
                UsdPhysics.CollisionAPI.Apply(prim)
            UsdPhysics.MeshCollisionAPI.Apply(prim).CreateApproximationAttr("convexHull")
            # PhysX limits hulls to 64 vertices by default: that shaves the pawn's neck and head
            # (the jaw closed ~10 mm further than the hull of the mesh says)
            PhysxSchema.PhysxConvexHullCollisionAPI.Apply(prim).CreateHullVertexLimitAttr(
                HULL_VERTEX_LIMIT)
            try:
                if not prim.HasAPI(PhysxSchema.PhysxCollisionAPI):
                    PhysxSchema.PhysxCollisionAPI.Apply(prim)
                pcol = PhysxSchema.PhysxCollisionAPI(prim)
                pcol.CreateContactOffsetAttr(0.0015)
                pcol.CreateRestOffsetAttr(0.0)
                # Finger pads have area: torsional friction about the contact normal keeps
                # a gripped piece from swinging about the axis between the two fingers.
                pcol.CreateTorsionalPatchRadiusAttr(PIECE_TORSIONAL_PATCH_RADIUS)
                pcol.CreateMinTorsionalPatchRadiusAttr(PIECE_TORSIONAL_PATCH_RADIUS)
            except Exception as e:
                log(f"PhysxCollisionAPI on mesh {prim.GetPath()} note: {e}")
            bind_physics_material(prim, piece_mat)
            mesh_n += 1
        if mesh_n == 0 and not child.HasAPI(UsdPhysics.CollisionAPI):
            UsdPhysics.CollisionAPI.Apply(child)
        n_pieces += 1

    n_reset = _promote_piece_xforms_to_world(stage, parent_path)
    log(
        f"Chess PhysX: {n_squares} static squares, {n_pieces} dynamic pieces "
        f"(resetXformStack={n_reset})"
    )


def _promote_piece_xforms_to_world(stage, parent_path: str = CHESS_PRIM_PATH) -> int:
    """Bake ChessSet parent into piece translates and ignore the parent xform.

    PhysX writes the actor *world* pose back into xformOp:translate. Pieces live
    under ChessSet (0.43 m), so that writeback double-applies the board origin
    unless resetXformStack is set and the translate is already world-frame.
    """
    from pxr import Gf, Usd, UsdGeom, UsdPhysics

    root = stage.GetPrimAtPath(parent_path)
    if not root.IsValid():
        return 0
    n = 0
    sample = None
    for child in root.GetChildren():
        if not child.HasAPI(UsdPhysics.RigidBodyAPI):
            continue
        xf = UsdGeom.Xformable(child)
        world_tf = xf.ComputeLocalToWorldTransform(Usd.TimeCode.Default())
        world_t = world_tf.ExtractTranslation()
        if not xf.GetResetXformStack():
            for op in xf.GetOrderedXformOps():
                if op.GetOpType() == UsdGeom.XformOp.TypeTranslate:
                    op.Set(Gf.Vec3d(float(world_t[0]), float(world_t[1]), float(world_t[2])))
                    break
            xf.SetResetXformStack(True)
        n += 1
        if sample is None:
            sample = (child.GetName(), tuple(float(v) for v in world_t))
    if sample is not None:
        log(f"Piece xforms are world-frame (resetXformStack): {sample[0]} world={sample[1]}")
    return n


class SceneRestore:
    """Snapshot ChessSet (board + pieces) and joint starts; restore without rebuilding USD.

    Piece rigid bodies use resetXformStack with world-frame translates (PhysX writeback
    is world-space). Restore rewrites those authored ops, reloads PhysX from USD, and
    holds bodies kinematic for a few play frames. Do not RigidPrim.set_world_poses:
    that path double-applies ChessSet when tensor fallback writes USD.
    """

    _SETTLE_FRAMES = 3

    def __init__(self) -> None:
        self.xform_ops: list[tuple[str, list[tuple[str, Any]], bool]] = []
        self.rb_paths: list[str] = []
        self.joint_targets: list[tuple[str, str, float]] = []  # path, drive_type, position
        self.n_squares = 0
        self.n_pieces = 0
        self.ready = False
        self._pending_frames = 0
        self._physx_status = "skipped"
        self._usd_reload_status = "skipped"
        self._ros_node: Any = None
        self._ros_queued = False
        self.busy = False

    @staticmethod
    def _iter_chess_prims(stage):
        from pxr import UsdGeom

        root = stage.GetPrimAtPath(CHESS_PRIM_PATH)
        if not root.IsValid():
            return
        yield root
        for child in root.GetChildren():
            name = child.GetName()
            if name == "Looks":
                continue
            if not child.IsA(UsdGeom.Xformable):
                continue
            yield child

    @staticmethod
    def _snapshot_xform_ops(prim) -> list[tuple[str, Any]]:
        from pxr import UsdGeom

        xf = UsdGeom.Xformable(prim)
        ops: list[tuple[str, Any]] = []
        for op in xf.GetOrderedXformOps():
            try:
                ops.append((op.GetOpName(), op.Get()))
            except Exception:
                continue
        return ops

    def capture(self, stage, robot_path: str) -> None:
        from pxr import Usd, UsdGeom, UsdPhysics

        self.xform_ops = []
        self.rb_paths = []
        self.n_squares = 0
        self.n_pieces = 0
        for prim in self._iter_chess_prims(stage):
            path = str(prim.GetPath())
            xf = UsdGeom.Xformable(prim)
            reset = bool(xf.GetResetXformStack())
            self.xform_ops.append((path, self._snapshot_xform_ops(prim), reset))
            name = prim.GetName()
            if name.startswith("sq_"):
                self.n_squares += 1
            if prim.HasAPI(UsdPhysics.RigidBodyAPI):
                self.rb_paths.append(path)
                if _piece_kind_from_prim_name(name) is not None:
                    self.n_pieces += 1

        self.joint_targets = []
        seen_joints: set[str] = set()
        for root_path in (robot_path, LARA_PRIM_PATH):
            robot = stage.GetPrimAtPath(root_path)
            if not robot.IsValid():
                continue
            for prim in Usd.PrimRange(robot):
                if prim.IsA(UsdPhysics.PrismaticJoint):
                    drive_type = "linear"
                elif prim.IsA(UsdPhysics.RevoluteJoint):
                    drive_type = "angular"
                else:
                    continue
                path = str(prim.GetPath())
                if path in seen_joints:
                    continue
                seen_joints.add(path)
                pos = 0.0
                name = prim.GetName()
                if name == "lara5_gripper_finger_joint" or name.endswith("gripper_finger_joint"):
                    pos = -0.174533
                self.joint_targets.append((path, drive_type, pos))

        self.ready = True
        ready = (
            f"squares={self.n_squares} pieces={self.n_pieces} "
            f"rigid={len(self.rb_paths)} joints={len(self.joint_targets)}\n"
        )
        try:
            RESTORE_READY.write_text(ready, encoding="utf-8")
        except OSError as e:
            log(f"WARNING: could not write restore ready: {e}")
        log(
            f"Scene restore snapshot: ChessSet + {self.n_squares} squares + "
            f"{self.n_pieces} pieces ({len(self.rb_paths)} rigid), "
            f"{len(self.joint_targets)} joints, "
            f"resetXformStack={sum(1 for _p, _o, r in self.xform_ops if r)}"
        )

    _XFORM_OP_TYPES = None

    @classmethod
    def _xform_op_type_map(cls):
        if cls._XFORM_OP_TYPES is None:
            from pxr import UsdGeom

            cls._XFORM_OP_TYPES = {
                "translate": UsdGeom.XformOp.TypeTranslate,
                "scale": UsdGeom.XformOp.TypeScale,
                "rotateX": UsdGeom.XformOp.TypeRotateX,
                "rotateY": UsdGeom.XformOp.TypeRotateY,
                "rotateZ": UsdGeom.XformOp.TypeRotateZ,
                "rotateXYZ": UsdGeom.XformOp.TypeRotateXYZ,
                "orient": UsdGeom.XformOp.TypeOrient,
                "transform": UsdGeom.XformOp.TypeTransform,
            }
        return cls._XFORM_OP_TYPES

    def _apply_usd_xforms(self, stage) -> int:
        """Rewrite authored local xform ops. Never write world-frame xyz into translate."""
        from pxr import UsdGeom

        n = 0
        type_map = self._xform_op_type_map()
        for path, ops, reset in self.xform_ops:
            prim = stage.GetPrimAtPath(path)
            if not prim.IsValid():
                continue
            xf = UsdGeom.Xformable(prim)
            by_name = {op.GetOpName(): op for op in xf.GetOrderedXformOps()}
            missing = [name for name, val in ops if val is not None and name not in by_name]
            if missing:
                xf.ClearXformOpOrder()
                by_name = {}
                for name, val in ops:
                    if val is None:
                        continue
                    rest = name[8:] if name.startswith("xformOp:") else name
                    parts = rest.split(":")
                    op_type = type_map.get(parts[0])
                    if op_type is None:
                        continue
                    suffix = parts[1] if len(parts) > 1 else ""
                    try:
                        op = xf.AddXformOp(op_type, UsdGeom.XformOp.PrecisionDouble, suffix)
                    except Exception:
                        continue
                    op.Set(val)
                    by_name[name] = op
            else:
                for name, val in ops:
                    op = by_name.get(name)
                    if op is not None and val is not None:
                        op.Set(val)
            try:
                xf.SetResetXformStack(bool(reset))
            except Exception:
                pass
            n += 1
        _promote_piece_xforms_to_world(stage, CHESS_PRIM_PATH)
        return n

    def _iter_rb_prims(self, stage):
        from pxr import UsdPhysics

        for path in self.rb_paths:
            prim = stage.GetPrimAtPath(path)
            if prim.IsValid() and prim.HasAPI(UsdPhysics.RigidBodyAPI):
                yield prim

    def _zero_rb_velocities(self, stage) -> None:
        from pxr import Gf, UsdPhysics

        for prim in self._iter_rb_prims(stage):
            rb = UsdPhysics.RigidBodyAPI(prim)
            try:
                rb.CreateVelocityAttr().Set(Gf.Vec3f(0.0, 0.0, 0.0))
                rb.CreateAngularVelocityAttr().Set(Gf.Vec3f(0.0, 0.0, 0.0))
            except Exception:
                pass

    def _set_rb_enabled(self, stage, enabled: bool) -> None:
        from pxr import UsdPhysics

        for prim in self._iter_rb_prims(stage):
            try:
                UsdPhysics.RigidBodyAPI(prim).CreateRigidBodyEnabledAttr().Set(bool(enabled))
            except Exception:
                pass

    def _set_rb_kinematic(self, stage, kinematic: bool) -> None:
        from pxr import UsdPhysics

        for prim in self._iter_rb_prims(stage):
            try:
                UsdPhysics.RigidBodyAPI(prim).CreateKinematicEnabledAttr().Set(bool(kinematic))
            except Exception:
                pass

    def _restore_joints(self, stage) -> None:
        from pxr import UsdPhysics

        for path, drive_type, pos in self.joint_targets:
            prim = stage.GetPrimAtPath(path)
            if not prim.IsValid():
                continue
            try:
                drive = UsdPhysics.DriveAPI.Get(prim, drive_type)
                if drive:
                    drive.CreateTargetPositionAttr().Set(float(pos))
            except Exception:
                pass
            try:
                from pxr import PhysxSchema

                state = PhysxSchema.JointStateAPI.Apply(prim, drive_type)
                state.CreatePositionAttr().Set(float(pos))
                state.CreateVelocityAttr().Set(0.0)
            except Exception:
                pass

    def attach_ros(self) -> None:
        """Optional Trigger service; PhysX work still runs on the Kit main loop."""
        try:
            import rclpy
            from std_srvs.srv import Trigger
        except Exception as e:
            log(f"Scene restore ROS service skipped: {e}")
            return
        try:
            if not rclpy.ok():
                rclpy.init()
            self._ros_node = rclpy.create_node("neura_chess_restore")

            def _on_restore(_req, resp):
                self._ros_queued = True
                resp.success = True
                resp.message = "queued"
                return resp

            self._ros_node.create_service(Trigger, RESTORE_ROS_SERVICE, _on_restore)
            log(f"Scene restore ROS: {RESTORE_ROS_SERVICE}")
        except Exception as e:
            log(f"WARNING: scene restore ROS service failed: {e}")
            self._ros_node = None

    def _spin_ros(self) -> None:
        node = self._ros_node
        if node is None:
            return
        try:
            import rclpy

            rclpy.spin_once(node, timeout_sec=0.0)
        except Exception:
            pass

    def _reload_physx_from_usd(self) -> str:
        try:
            from omni.physx import get_physx_interface

            physx = get_physx_interface()
            physx.release_physics_objects()
            physx.force_load_physics_from_usd()
            return "ok"
        except Exception as e:
            log(f"WARNING: PhysX reload from USD failed: {e}")
            return f"fail:{e}"

    def _log_sample_world_poses(self, stage) -> None:
        from pxr import Usd, UsdGeom

        for name in ("W_rook_0", "Wp_pawn_0", "Bp_pawn_0", "B_king_4"):
            prim = stage.GetPrimAtPath(f"{CHESS_PRIM_PATH}/{name}")
            if not prim.IsValid():
                continue
            t = UsdGeom.Xformable(prim).ComputeLocalToWorldTransform(Usd.TimeCode.Default()).ExtractTranslation()
            xf = UsdGeom.Xformable(prim)
            reset = xf.GetResetXformStack()
            local_t = None
            for op in xf.GetOrderedXformOps():
                if op.GetOpType() == UsdGeom.XformOp.TypeTranslate:
                    local_t = op.Get()
                    break
            log(
                f"  restore sample {name} world=({float(t[0]):.3f}, {float(t[1]):.3f}, {float(t[2]):.3f}) "
                f"translate={local_t} resetXformStack={reset}"
            )

    def _begin_restore(self, stage, timeline: Any) -> None:
        if timeline is not None and timeline.is_playing():
            timeline.stop()
        self._set_rb_enabled(stage, False)
        n = self._apply_usd_xforms(stage)
        self._zero_rb_velocities(stage)
        self._set_rb_kinematic(stage, True)
        self._restore_joints(stage)
        self._set_rb_enabled(stage, True)
        self._usd_reload_status = self._reload_physx_from_usd()
        self._apply_usd_xforms(stage)
        if timeline is not None:
            timeline.play()
        log(
            f"Scene restore USD applied ({n} chess prims: ChessSet + "
            f"{self.n_squares} squares + {self.n_pieces} pieces); "
            f"physx_usd={self._usd_reload_status}; kinematic settle"
        )

    def _finish_restore(self, stage) -> None:
        self._apply_usd_xforms(stage)
        self._zero_rb_velocities(stage)
        self._set_rb_kinematic(stage, False)
        self._zero_rb_velocities(stage)
        self._physx_status = "ok" if self._usd_reload_status == "ok" else self._usd_reload_status
        try:
            self._log_sample_world_poses(stage)
        except Exception as e:
            log(f"WARNING: restore sample poses skipped: {e}")
        log(
            f"Scene restore PhysX from USD={self._physx_status} "
            f"(squares={self.n_squares}, pieces={self.n_pieces}, joints={len(self.joint_targets)})"
        )

    def _clear_done(self) -> None:
        try:
            RESTORE_DONE.unlink(missing_ok=True)
        except TypeError:
            if RESTORE_DONE.exists():
                RESTORE_DONE.unlink()
        except OSError:
            pass

    def _write_done(self) -> None:
        body = (
            f"ok squares={self.n_squares} pieces={self.n_pieces} "
            f"rigid={len(self.rb_paths)} joints={len(self.joint_targets)} "
            f"physx={self._physx_status} usd_reload={self._usd_reload_status}\n"
        )
        try:
            RESTORE_DONE.write_text(body, encoding="utf-8")
        except OSError as e:
            log(f"WARNING: could not write restore done: {e}")

    def poll(self, stage, timeline: Any) -> None:
        try:
            self._spin_ros()
            triggered = bool(self._ros_queued)
            self._ros_queued = False
            if RESTORE_REQUEST.is_file():
                try:
                    RESTORE_REQUEST.unlink()
                    triggered = True
                except OSError:
                    pass
            if triggered:
                if self.busy:
                    return
                self._clear_done()
                if not self.ready:
                    log("WARNING: scene restore requested before snapshot")
                    self._physx_status = "not_ready"
                    self._write_done()
                    self.busy = False
                    self._pending_frames = 0
                    return
                self.busy = True
                self._begin_restore(stage, timeline)
                self._pending_frames = self._SETTLE_FRAMES
                return

            if self._pending_frames <= 0:
                return
            self._apply_usd_xforms(stage)
            self._zero_rb_velocities(stage)
            self._pending_frames -= 1
            if self._pending_frames > 0:
                return
            self._finish_restore(stage)
            self.busy = False
            self._write_done()
        except Exception as e:
            import traceback

            log(f"ERROR: scene restore crashed: {e}\n{traceback.format_exc()}")
            self.busy = False
            self._pending_frames = 0
            self._physx_status = f"crash:{e}"
            self._write_done()


def build_stage(stage) -> None:
    from pxr import Gf, Sdf, UsdGeom, UsdLux, UsdPhysics

    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)
    UsdGeom.SetStageMetersPerUnit(stage, 1.0)

    if not stage.GetPrimAtPath("/World").IsValid():
        stage.DefinePrim("/World", "Xform")
    stage.SetDefaultPrim(stage.GetPrimAtPath("/World"))
    stage.DefinePrim(WORLD, "Xform")

    if not stage.GetPrimAtPath(PHYSICS_SCENE).IsValid():
        scene = UsdPhysics.Scene.Define(stage, Sdf.Path(PHYSICS_SCENE))
        scene.CreateGravityDirectionAttr().Set(Gf.Vec3f(0, 0, -1))
        scene.CreateGravityMagnitudeAttr().Set(9.81)

    ground = UsdGeom.Cube.Define(stage, Sdf.Path(GROUND_PATH))
    ground.CreateSizeAttr(1.0)
    xf = UsdGeom.Xformable(ground.GetPrim())
    xf.ClearXformOpOrder()
    xf.AddTranslateOp().Set(Gf.Vec3d(0.0, 0.0, -0.04))
    xf.AddScaleOp().Set(Gf.Vec3f(4.0, 4.0, 0.08))
    ground.CreateDisplayColorAttr([Gf.Vec3f(0.35, 0.38, 0.36)])
    UsdPhysics.CollisionAPI.Apply(ground.GetPrim())

    fill = UsdLux.DomeLight.Define(stage, Sdf.Path(f"{WORLD}/DomeLight"))
    fill.CreateIntensityAttr(800.0)
    distant = UsdLux.DistantLight.Define(stage, Sdf.Path(f"{WORLD}/DistantLight"))
    distant.CreateIntensityAttr(2500.0)
    distant.CreateAngleAttr(1.0)
    dx = UsdGeom.Xformable(distant.GetPrim())
    dx.ClearXformOpOrder()
    dx.AddRotateXYZOp().Set(Gf.Vec3f(-45.0, 30.0, 0.0))


def import_lara(simulation_app: Any) -> str:
    import omni.usd
    from isaacsim.core.utils import extensions
    from isaacsim.core.utils.stage import add_reference_to_stage
    from isaacsim.asset.importer.urdf import URDFImporter, URDFImporterConfig
    from pxr import Usd, UsdGeom

    log("Enabling URDF importer...")
    extensions.enable_extension("isaacsim.asset.importer.urdf")
    simulation_app.update()

    urdf_path = ensure_relative_urdf()
    log(f"Using URDF: {urdf_path}")

    usd_cache = Path(tempfile.mkdtemp(prefix="lara5_urdf_"))
    import_config = URDFImporterConfig(
        urdf_path=str(urdf_path),
        usd_path=str(usd_cache),
        fix_base=True,
        merge_fixed_joints=False,
        collision_from_visuals=False,
        collision_type="Convex Hull",
        allow_self_collision=False,
        joint_target_type="position",
        override_joint_stiffness=JOINT_STIFFNESS,
        override_joint_damping=JOINT_DAMPING,
        run_asset_transformer=False,
    )
    output_usd = URDFImporter(import_config).import_urdf()
    log(f"Lara5 USD generated: {output_usd}")
    add_reference_to_stage(str(output_usd), LARA_PRIM_PATH)
    simulation_app.update()

    stage = omni.usd.get_context().get_stage()
    lara_prim = stage.GetPrimAtPath(LARA_PRIM_PATH)
    if not lara_prim.IsValid():
        raise RuntimeError(f"Lara5 prim missing after URDF import: {LARA_PRIM_PATH}")

    xf = UsdGeom.Xformable(lara_prim)
    try:
        xf.AddTranslateOp().Set((0.0, 0.0, 0.0))
    except Exception:
        xf.ClearXformOpOrder()
        xf.AddTranslateOp().Set((0.0, 0.0, 0.0))
        xf.AddRotateZOp().Set(0.0)

    for prim in Usd.PrimRange(lara_prim):
        if prim.IsA(UsdGeom.Imageable):
            try:
                UsdGeom.Imageable(prim).MakeVisible()
            except Exception:
                pass
    simulation_app.update()

    mesh_n = sum(1 for p in Usd.PrimRange(lara_prim) if p.IsA(UsdGeom.Mesh))
    log(f"Lara5 meshes under {LARA_PRIM_PATH}: {mesh_n}")
    return LARA_PRIM_PATH


def setup_ros_bridge(simulation_app: Any, robot_path: str) -> str:
    """OnPlaybackTick → SubscribeJointState.execOut → ArticulationController + PublishJointState.

    Only joint names + positions are wired. topic_based_ros2_control leaves
    velocity/effort empty; connecting those outputs as zeros freezes the arm.
    """
    import omni.graph.core as og
    import usdrt.Sdf
    from isaacsim.core.utils import extensions

    log("Enabling isaacsim.ros2 bridge stack...")
    for ext in ("isaacsim.ros2.core", "isaacsim.ros2.bridge"):
        extensions.enable_extension(ext)
    for _ in range(10):
        simulation_app.update()

    graph_path = f"{WORLD}/ActionGraph"
    tick_node = "OnPlaybackTick"
    tick_out = f"{tick_node}.outputs:tick"

    try:
        og.Controller.edit(
            {"graph_path": graph_path, "evaluator_name": "execution"},
            {
                og.Controller.Keys.CREATE_NODES: [
                    (tick_node, "omni.graph.action.OnPlaybackTick"),
                    ("ReadSimTime", "isaacsim.core.nodes.IsaacReadSimulationTime"),
                    ("Context", "isaacsim.ros2.bridge.ROS2Context"),
                    ("PublishJointState", "isaacsim.ros2.bridge.ROS2PublishJointState"),
                    ("SubscribeJointState", "isaacsim.ros2.bridge.ROS2SubscribeJointState"),
                    ("ArticulationController", "isaacsim.core.nodes.IsaacArticulationController"),
                    ("PublishClock", "isaacsim.ros2.bridge.ROS2PublishClock"),
                ],
                og.Controller.Keys.CONNECT: [
                    (tick_out, "PublishJointState.inputs:execIn"),
                    (tick_out, "SubscribeJointState.inputs:execIn"),
                    (tick_out, "PublishClock.inputs:execIn"),
                    (
                        "SubscribeJointState.outputs:execOut",
                        "ArticulationController.inputs:execIn",
                    ),
                    ("Context.outputs:context", "PublishJointState.inputs:context"),
                    ("Context.outputs:context", "SubscribeJointState.inputs:context"),
                    ("Context.outputs:context", "PublishClock.inputs:context"),
                    ("ReadSimTime.outputs:simulationTime", "PublishJointState.inputs:timeStamp"),
                    ("ReadSimTime.outputs:simulationTime", "PublishClock.inputs:timeStamp"),
                    ("SubscribeJointState.outputs:jointNames", "ArticulationController.inputs:jointNames"),
                    (
                        "SubscribeJointState.outputs:positionCommand",
                        "ArticulationController.inputs:positionCommand",
                    ),
                ],
                og.Controller.Keys.SET_VALUES: [
                    ("ArticulationController.inputs:robotPath", robot_path),
                    ("ArticulationController.inputs:targetPrim", [usdrt.Sdf.Path(robot_path)]),
                    ("PublishJointState.inputs:topicName", JOINT_STATES_TOPIC),
                    ("SubscribeJointState.inputs:topicName", JOINT_COMMANDS_TOPIC),
                    ("PublishJointState.inputs:targetPrim", [usdrt.Sdf.Path(robot_path)]),
                    ("Context.inputs:useDomainIDEnvVar", True),
                ],
            },
        )
    except Exception as e:
        log(f"ActionGraph create note: {e}")

    simulation_app.update()
    log(
        f"OmniGraph ROS2 bridge ready: sub=/{JOINT_COMMANDS_TOPIC} "
        f"pub=/{JOINT_STATES_TOPIC} robot={robot_path} joints={list(ALL_DOF_JOINT_NAMES)}"
    )
    return graph_path


def _frame_scene_camera(app, eye, target) -> None:
    """Point the active viewport at the Lara + board layout. Never raises."""
    try:
        from isaacsim.core.utils import viewports
        from omni.kit.viewport.utility import get_active_viewport

        viewport = None
        for _ in range(20):
            viewport = get_active_viewport()
            if viewport is not None:
                break
            app.update()
        if viewport is None:
            log("WARNING: no active viewport yet; camera not framed")
            return
        viewports.set_camera_view(eye=eye, target=target, viewport_api=viewport)
        for _ in range(3):
            app.update()
        viewports.set_camera_view(eye=eye, target=target, viewport_api=viewport)
        log(f"Camera framed eye={tuple(float(x) for x in eye)} target={tuple(float(x) for x in target)}")
    except Exception as e:
        log(f"WARNING: camera frame failed: {e}")


def run(app, *, headless: bool, enable_ros: bool) -> None:
    import carb
    import numpy as np
    import omni.timeline
    import omni.usd
    from isaacsim.core.utils import extensions

    log("Enabling PhysX")
    for ext in ("omni.physx", "omni.physx.bundle"):
        extensions.enable_extension(ext)
    app.update()

    stage = omni.usd.get_context().get_stage()
    build_stage(stage)
    _force_physx(stage)
    app.update()

    import_lara(app)
    articulation_path = ensure_physx_articulation(app, LARA_PRIM_PATH)

    cam_eye = np.array([1.15, -1.15, 0.85])
    cam_target = np.array([BOARD_CENTER_X * 0.5, 0.0, 0.12])
    _frame_scene_camera(app, cam_eye, cam_target)

    stage = omni.usd.get_context().get_stage()
    log("Building chessboard + OpenChessSet pieces in front of Lara...")
    add_simple_chess(stage, CHESS_PRIM_PATH)
    app.update()
    apply_chess_physics(stage, CHESS_PRIM_PATH)
    app.update()
    try:
        log_chess_board_frames(stage, CHESS_PRIM_PATH)
    except Exception as e:
        log(f"WARNING: chess frame log skipped: {e}")

    _frame_scene_camera(app, cam_eye, cam_target)

    restorer = SceneRestore()
    restorer.capture(stage, articulation_path)

    if enable_ros:
        setup_ros_bridge(app, articulation_path)
        app.update()
        restorer.attach_ros()

    timeline = omni.timeline.get_timeline_interface()
    carb.settings.get_settings().set("/app/player/playSimulations", True)
    timeline.play()
    for _ in range(10):
        app.update()
    _log_live_articulation(articulation_path)

    try:
        from neura_chess_piece_positions import PiecePositionsRigidPrim
    except ImportError:
        sys.path.insert(0, str(ROOT))
        from neura_chess_piece_positions import PiecePositionsRigidPrim

    piece_poses = PiecePositionsRigidPrim()
    piece_poses.bind(stage)
    joint_cmds = JointCommandApplier(articulation_path)
    if enable_ros:
        piece_poses.attach_ros()
        joint_cmds.attach_ros()

    try:
        if RESTORE_REQUEST.exists():
            RESTORE_REQUEST.unlink()
        if RESTORE_DONE.exists():
            RESTORE_DONE.unlink()
        from neura_chess_piece_positions import PIECES_REQUEST, PIECES_DONE

        if PIECES_REQUEST.exists():
            PIECES_REQUEST.unlink()
        if PIECES_DONE.exists():
            PIECES_DONE.unlink()
    except OSError:
        pass
    log(f"Scene restore: ./scripts/scene/chess_scene_restore.sh  (ready file {RESTORE_READY})")
    log("Piece poses: ./scripts/scene/pieces_positions_RigidPrim.sh")

    if enable_ros:
        log("Ready for topic_based_ros2_control")
        log(
            f"  /{JOINT_COMMANDS_TOPIC} → JointCommandApplier + ArticulationController "
            f"→ /{JOINT_STATES_TOPIC}"
        )
    else:
        log("Ready (PhysX playing, ROS bridge skipped)")

    while app.is_running():
        restorer.poll(stage, timeline)
        piece_poses.poll(stage)
        joint_cmds.poll()
        if not restorer.busy and not timeline.is_playing():
            timeline.play()
        app.update()
        if headless:
            break

    timeline.stop()


def _check_ros_env() -> None:
    lib = os.environ.get("LD_LIBRARY_PATH", "")
    if "isaacsim.ros2.core" not in lib and not os.environ.get("ROS_DISTRO"):
        log(
            "WARNING: Isaac ROS env may be unset. Source scripts/setup/setup_isaac_ros_env.sh "
            "before launch (scripts/launch/launch_world.sh does this)."
        )


def main() -> int:
    args = parse_args()
    os.environ.setdefault("OMNI_KIT_ALLOW_ROOT", "1")
    log(f"ROOT={ROOT}")
    enable_ros = bool(args.ros) and not args.no_ros
    if enable_ros:
        _check_ros_env()

    from isaacsim import SimulationApp

    # GUI: keep the viewport painting while OpenChessSet MDL compiles (several minutes).
    # Headless: wait for loads so physics sees complete meshes.
    launch_config = {
        "renderer": "RaytracedLighting",
        "headless": args.headless,
        "width": 1280,
        "height": 720,
        "sync_loads": bool(args.headless),
        "multi_gpu": False,
    }
    if not args.headless:
        launch_config["hide_ui"] = False
    app = SimulationApp(launch_config)
    try:
        run(app, headless=args.headless, enable_ros=enable_ros)
    except Exception as e:
        import traceback

        log(f"ERROR: {e}\n{traceback.format_exc()}")
        raise
    finally:
        app.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
