#!/usr/bin/env python3
"""Neura Lara5 PhysX world + isaacsim.ros2.bridge.

Imports the Lara5 URDF (from ros2_ws/lara5_description, copied under assets/)
and drives it with OmniGraph:
  /isaac_joint_commands → ArticulationController → /isaac_joint_states
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
# Matches ros2_ws chess_scene a1≈(0.27, −0.16) at 40 mm, centered on the arm.
SQUARE = 0.04
BOARD_THICKNESS = 0.02
BOARD_HALF_M = 4 * SQUARE
BOARD_CENTER_X = 0.27 + 3.5 * SQUARE  # 0.41 m
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

JOINT_STIFFNESS = 400.0
JOINT_DAMPING = 80.0
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


def ensure_physx_articulation(simulation_app: Any, robot_root: str) -> str:
    """Single fixed-base ArticulationRootAPI for PhysX + OmniGraph."""
    import omni.usd
    from pxr import PhysxSchema, Usd, UsdPhysics

    stage = omni.usd.get_context().get_stage()
    root = stage.GetPrimAtPath(robot_root)
    if not root.IsValid():
        raise RuntimeError(f"Robot root missing: {robot_root}")

    try:
        from isaacsim.asset.importer.utils.impl import asset_utils

        relocated = asset_utils.fix_articulation_root_for_fixed_base(stage)
        if relocated:
            log(f"fix_articulation_root_for_fixed_base relocated {relocated} root(s)")
    except Exception as e:
        log(f"fix_articulation_root_for_fixed_base note: {e}")

    root_joint = stage.GetPrimAtPath(f"{robot_root}/Physics/root_joint")
    if not root_joint.IsValid():
        for cand in (
            f"{robot_root}/Physics/root_to_base",
            f"{robot_root}/fix_base_joint",
        ):
            p = stage.GetPrimAtPath(cand)
            if p.IsValid():
                root_joint = p
                break

    keep = None
    if root_joint.IsValid():
        keep = root_joint
    else:
        for p in Usd.PrimRange(root):
            if p.HasAPI(UsdPhysics.ArticulationRootAPI) and not p.HasAPI(UsdPhysics.RigidBodyAPI):
                keep = p
                break
    if keep is None:
        keep = root

    stripped: list[str] = []
    for p in list(Usd.PrimRange(root)):
        if not p.HasAPI(UsdPhysics.ArticulationRootAPI):
            continue
        if p == keep:
            continue
        stripped.append(str(p.GetPath()))
        _strip_articulation_root_schemas(p)

    if not keep.HasAPI(UsdPhysics.ArticulationRootAPI):
        UsdPhysics.ArticulationRootAPI.Apply(keep)
        log(f"Applied ArticulationRootAPI on {keep.GetPath()}")
    try:
        if not keep.HasAPI(PhysxSchema.PhysxArticulationAPI):
            PhysxSchema.PhysxArticulationAPI.Apply(keep)
        try:
            keep.ApplyAPI("NewtonArticulationRootAPI")
        except Exception:
            pass
    except Exception as e:
        log(f"PhysxArticulationAPI note: {e}")

    if stripped:
        log(f"Removed duplicate ArticulationRootAPI from: {stripped}")

    roots = [
        str(p.GetPath())
        for p in Usd.PrimRange(root)
        if p.HasAPI(UsdPhysics.ArticulationRootAPI)
    ]
    art_path = str(keep.GetPath())
    if len(roots) != 1:
        log(f"WARNING: expected 1 ArticulationRootAPI under {robot_root}, found {len(roots)}: {roots}")
    else:
        log(f"Fixed-base ArticulationRootAPI at {roots[0]}; OmniGraph robotPath={art_path}")
    for _ in range(3):
        simulation_app.update()
    return art_path


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
    back_order = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]

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
    from pxr import UsdGeom

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
            try:
                if not prim.HasAPI(PhysxSchema.PhysxCollisionAPI):
                    PhysxSchema.PhysxCollisionAPI.Apply(prim)
                pcol = PhysxSchema.PhysxCollisionAPI(prim)
                pcol.CreateContactOffsetAttr(0.0015)
                pcol.CreateRestOffsetAttr(0.0)
            except Exception as e:
                log(f"PhysxCollisionAPI on mesh {prim.GetPath()} note: {e}")
            bind_physics_material(prim, piece_mat)
            mesh_n += 1
        if mesh_n == 0 and not child.HasAPI(UsdPhysics.CollisionAPI):
            UsdPhysics.CollisionAPI.Apply(child)
        n_pieces += 1

    log(f"Chess PhysX: {n_squares} static squares, {n_pieces} dynamic pieces")


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
    """OnPlaybackTick → SubscribeJointState → ArticulationController + PublishJointState."""
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
                    (tick_out, "ArticulationController.inputs:execIn"),
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
                    (
                        "SubscribeJointState.outputs:velocityCommand",
                        "ArticulationController.inputs:velocityCommand",
                    ),
                    (
                        "SubscribeJointState.outputs:effortCommand",
                        "ArticulationController.inputs:effortCommand",
                    ),
                ],
                og.Controller.Keys.SET_VALUES: [
                    ("ArticulationController.inputs:robotPath", robot_path),
                    ("PublishJointState.inputs:topicName", JOINT_STATES_TOPIC),
                    ("SubscribeJointState.inputs:topicName", JOINT_COMMANDS_TOPIC),
                    ("PublishJointState.inputs:targetPrim", [usdrt.Sdf.Path(robot_path)]),
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


def run(app, *, headless: bool, enable_ros: bool) -> None:
    import carb
    import numpy as np
    import omni.timeline
    import omni.usd
    from isaacsim.core.utils import extensions, viewports

    log("Enabling PhysX")
    for ext in ("omni.physx", "omni.physx.bundle"):
        extensions.enable_extension(ext)
    app.update()

    build_stage(omni.usd.get_context().get_stage())
    app.update()

    import_lara(app)
    articulation_path = ensure_physx_articulation(app, LARA_PRIM_PATH)

    stage = omni.usd.get_context().get_stage()
    log("Building chessboard + OpenChessSet pieces in front of Lara...")
    add_simple_chess(stage, CHESS_PRIM_PATH)
    app.update()
    apply_chess_physics(stage, CHESS_PRIM_PATH)
    app.update()
    log_chess_board_frames(stage, CHESS_PRIM_PATH)

    cam_eye = np.array([1.15, -1.15, 0.85])
    cam_target = np.array([BOARD_CENTER_X * 0.5, 0.0, 0.12])
    viewports.set_camera_view(eye=cam_eye, target=cam_target)
    for _ in range(5):
        app.update()
    viewports.set_camera_view(eye=cam_eye, target=cam_target)
    app.update()

    if enable_ros:
        setup_ros_bridge(app, articulation_path)
        app.update()

    timeline = omni.timeline.get_timeline_interface()
    carb.settings.get_settings().set("/app/player/playSimulations", True)
    timeline.play()
    for _ in range(10):
        app.update()

    if enable_ros:
        log("Ready for topic_based_ros2_control")
        log(f"  /{JOINT_COMMANDS_TOPIC} → ArticulationController → /{JOINT_STATES_TOPIC}")
    else:
        log("Ready (PhysX playing, ROS bridge skipped)")

    while app.is_running():
        if not timeline.is_playing():
            timeline.play()
        app.update()
        if headless:
            break

    timeline.stop()


def _check_ros_env() -> None:
    lib = os.environ.get("LD_LIBRARY_PATH", "")
    if "isaacsim.ros2.core" not in lib and not os.environ.get("ROS_DISTRO"):
        log(
            "WARNING: Isaac ROS env may be unset. Source scripts/setup_isaac_ros_env.sh "
            "before launch (launch_world.sh does this)."
        )


def main() -> int:
    args = parse_args()
    os.environ.setdefault("OMNI_KIT_ALLOW_ROOT", "1")
    log(f"ROOT={ROOT}")
    enable_ros = bool(args.ros) and not args.no_ros
    if enable_ros:
        _check_ros_env()

    from isaacsim import SimulationApp

    app = SimulationApp(
        {"renderer": "RaytracedLighting", "headless": args.headless, "width": 1280, "height": 720}
    )
    try:
        run(app, headless=args.headless, enable_ros=enable_ros)
    except Exception as e:
        log(f"ERROR: {e}")
        raise
    finally:
        app.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
