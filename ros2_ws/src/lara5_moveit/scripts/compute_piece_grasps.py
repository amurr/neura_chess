#!/usr/bin/env python3
"""Piece collision hulls + per-type grasp parameters from the Isaac chess pieces.

Rebuilds what Isaac collides with (neura_chess_world.py: OpenChessSet USDs scaled to the
board, one PhysX convex hull per mesh prim) and solves, per piece type, how the SO-101
gripper grasps it with the TCP lara5_tcp (static finger tip, inner face):

  tip_height      fingertip height above the board top at the grasp
  grasp_offset    piece centre - TCP along the TCP x axis: the closing jaw pushes the piece
                  against the static finger, so its centre ends up here
  open / close    lara5_gripper_finger_joint for descending around the piece / squeezing it

Writes
  lara5_moveit/meshes/chess_pieces/collision_hulls/<type>.stl   MoveIt piece collision hulls
  articulation_orchestrator/assets/objects_dictionary.yaml      orchestrator parameters

Needs pxr (USD) and scipy. pxr is not in the ROS environment:
  pip install --target /tmp/usdlib usd-core
  PYTHONPATH=/tmp/usdlib:$PYTHONPATH python3 scripts/compute_piece_grasps.py
or run it with Isaac's python.sh.
"""

from __future__ import annotations

import argparse
import math
import struct
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
import yaml
from scipy.spatial import ConvexHull

from lara5_moveit.board_ik import HOVER_TIP_Z, ArmModel, rpy_to_matrix

SRC = Path(__file__).resolve().parents[2]  # ros2_ws/src
NEURA = SRC.parents[1]  # neura_chess
PIECES_DIR = NEURA / 'assets' / 'OpenChessSet' / 'assets'
URDF = SRC / 'lara5_description' / 'lara5' / 'urdf' / 'lara5.urdf'
JAW_STL = SRC / 'lara5_description' / 'lara5' / 'meshes' / 'so101' / 'moving_jaw_so101_v1.stl'
HULL_DIR = SRC / 'lara5_moveit' / 'meshes' / 'chess_pieces' / 'collision_hulls'
HOVER_YAML = SRC / 'lara5_moveit' / 'config' / 'board_hover_joints.yaml'
OBJECTS_YAML = SRC / 'articulation_orchestrator' / 'assets' / 'objects_dictionary.yaml'

TYPES = ('pawn', 'rook', 'knight', 'bishop', 'queen', 'king')
# neura_chess_world.py: OpenChessSet is authored for 62.5 mm squares
PIECE_SCALE = 0.04 / 0.0625

# Fingertip above the board top at the grasp. Each type gets its preferred level and, where that
# is lower, `higher` levels every LEVEL_STEP up to the one whose wrist (66 mm above the
# fingertip, 46 x 48 mm, wider than a square) clears the tallest piece (king, 97 mm) on any
# neighbouring square. The orchestrator takes the lowest level whose wrist clears the
# neighbouring pieces.
# Preferred levels: contacts above the centre of mass, not on the knight's asymmetric head (it
# tips over), and high enough to need little jaw opening. The pawn's PhysX body hull is a cone:
# held on it (~22 mm) the closing jaw tips it over; at 32 mm (neck) it held in Isaac.
MIN_TIP_HEIGHT = 0.032
TIP_HEIGHT: dict[str, float] = {'knight': 0.016}  # per piece type
LEVEL_STEP = 0.004
TOP_CLEARANCE = 0.005   # piece top below the lowest wrist collision
OPEN_CLEARANCE = 0.004  # moving jaw - piece while descending
FINGER_CLEARANCE = 0.0015  # static finger - piece while descending (arm tracking ~0.5 mm)
RELEASE_OPENING = 0.15  # rad past the contact to let go of a placed piece (small jaw sweep)
OPEN_MARGIN = 0.05      # rad added to the minimum open angle
SQUEEZE = 0.30          # rad past the predicted contact: squeeze set-point for the soft jaw
JAW_LOWER = -0.1745     # URDF lower limit of lara5_gripper_finger_joint


# ---------- geometry helpers ----------
def load_stl(path: Path) -> np.ndarray:
    data = path.read_bytes()
    n = struct.unpack('<I', data[80:84])[0]
    rec = np.frombuffer(data[84:84 + n * 50],
                        dtype=np.dtype([('n', '<3f4'), ('v', '<9f4'), ('a', '<u2')]))
    return rec['v'].reshape(-1, 3).astype(float)


def write_stl(path: Path, points: np.ndarray, hull: ConvexHull) -> None:
    centre = points.mean(axis=0)
    out = bytearray(b'convex hull from compute_piece_grasps.py'.ljust(80, b' '))
    out += struct.pack('<I', len(hull.simplices))
    for tri in hull.simplices:
        a, b, c = points[tri]
        normal = np.cross(b - a, c - a)
        if np.dot(normal, a - centre) < 0:  # outward winding
            b, c = c, b
            normal = -normal
        normal = normal / (np.linalg.norm(normal) or 1.0)
        out += struct.pack('<12fH', *normal, *a, *b, *c, 0)
    path.write_bytes(bytes(out))


def hull_edges(hull: ConvexHull) -> np.ndarray:
    """Unique vertex index pairs of the hull edges (Ex2)."""
    tri = hull.simplices
    e = np.vstack((tri[:, [0, 1]], tri[:, [1, 2]], tri[:, [2, 0]]))
    return np.unique(np.sort(e, axis=1), axis=0)


def hull_slice(points: np.ndarray, edges: np.ndarray, z: float) -> np.ndarray:
    """Polygon (Nx2 XY points) where the plane at height z cuts the hull."""
    a, b = points[edges[:, 0]], points[edges[:, 1]]
    za, zb = a[:, 2] - z, b[:, 2] - z
    cut = (za * zb <= 0.0) & (za != zb)
    t = (za[cut] / (za[cut] - zb[cut]))[:, None]
    return (a[cut] + (b[cut] - a[cut]) * t)[:, :2]


def rot_x(a: float) -> np.ndarray:
    c, s = math.cos(a), math.sin(a)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])


def rot_z(a: float) -> np.ndarray:
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


# ---------- Isaac pieces ----------
def isaac_piece_hulls(kind: str) -> list[np.ndarray]:
    """Vertices of each PhysX convex hull of a piece (white, yaw 0), metres, board top = 0,
    XY relative to the prim origin that Isaac puts on the square centre."""
    from pxr import Usd, UsdGeom

    stage = Usd.Stage.Open(str(PIECES_DIR / kind.capitalize() / f'{kind.capitalize()}.usd'))
    # place_piece(): rotateX(90) then uniform scale
    rot = rot_x(math.pi / 2)
    meshes = []
    for prim in stage.Traverse():
        if not prim.IsA(UsdGeom.Mesh):
            continue
        pts = np.array(UsdGeom.Mesh(prim).GetPointsAttr().Get() or [], dtype=float)
        if pts.size == 0:
            continue
        m = np.array(UsdGeom.Xformable(prim).ComputeLocalToWorldTransform(0)).T
        pts = (m[:3, :3] @ pts.T).T + m[:3, 3]
        meshes.append((rot @ pts.T).T * PIECE_SCALE)
    z0 = min(p[:, 2].min() for p in meshes)
    hulls = []
    for p in meshes:
        p = p - np.array([0.0, 0.0, z0])
        hulls.append(p[ConvexHull(p).vertices])
    return hulls


class PieceProfile:
    """Support of the piece hulls along a horizontal direction, per height."""

    def __init__(self, hulls: list[np.ndarray]) -> None:
        self.hulls = [(h, hull_edges(ConvexHull(h))) for h in hulls]
        self.height = max(h[:, 2].max() for h in hulls)

    def support(self, z: float, direction: np.ndarray) -> float:
        """max p . direction over the hull cross-sections at height z (0 if none)."""
        best = 0.0
        for pts, edges in self.hulls:
            sl = hull_slice(pts, edges, z)
            if len(sl):
                best = max(best, float((sl @ direction).max()))
        return best


# ---------- gripper (collision geometry, lara5_tcp frame) ----------
def _origin(node) -> tuple[np.ndarray, np.ndarray]:
    o = node.find('origin')
    xyz = [0.0, 0.0, 0.0] if o is None else [float(v) for v in o.get('xyz', '0 0 0').split()]
    rpy = [0.0, 0.0, 0.0] if o is None else [float(v) for v in o.get('rpy', '0 0 0').split()]
    return np.array(xyz), rpy_to_matrix(*rpy)


class Gripper:
    """Static finger boxes, wrist bottom and the moving jaw hull, in the lara5_tcp frame."""

    def __init__(self, urdf: Path) -> None:
        root = ET.parse(urdf).getroot()
        joints = {j.find('child').get('link'): j for j in root.findall('joint')}
        tcp_xyz, _ = _origin(joints['lara5_tcp'])  # lara5_gripper -> lara5_tcp, no rotation
        body_xyz, _ = _origin(joints['lara5_gripper_body'])
        self.offset = body_xyz - tcp_xyz  # body frame origin in the tcp frame

        body = next(l for l in root.findall('link') if l.get('name') == 'lara5_gripper_body')
        self.fingers, self.wrist = [], []  # (lo, hi) boxes in the tcp frame
        for col in body.findall('collision'):
            xyz, rot = _origin(col)
            box, cyl = col.find('geometry/box'), col.find('geometry/cylinder')
            if box is not None:
                size = np.array([float(v) for v in box.get('size').split()])
                corners = np.array([[sx, sy, sz] for sx in (-.5, .5) for sy in (-.5, .5)
                                    for sz in (-.5, .5)]) * size
            elif cyl is not None:
                r, length = float(cyl.get('radius')), float(cyl.get('length'))
                a = np.linspace(0, 2 * math.pi, 24, endpoint=False)
                corners = np.array([[r * math.cos(t), r * math.sin(t), hz]
                                    for t in a for hz in (-length / 2, length / 2)])
            else:
                continue
            pts = (rot @ corners.T).T + xyz + self.offset
            lo, hi = pts.min(axis=0), pts.max(axis=0)
            (self.fingers if 'finger' in col.get('name', '') else self.wrist).append((lo, hi))
        self.wrist_bottom = min(lo[2] for lo, _ in self.wrist)

        jaw_joint = joints['lara5_gripper_jaw']
        self.jaw_xyz, self.jaw_rot = _origin(jaw_joint)
        self.jaw_xyz = self.jaw_xyz + self.offset
        jaw_vis = next(l for l in root.findall('link') if l.get('name') == 'lara5_gripper_jaw')
        jxyz, _ = _origin(jaw_vis.find('collision'))
        pts = load_stl(JAW_STL) * 0.001 + jxyz
        self.jaw_pts = pts[ConvexHull(pts).vertices]
        self.jaw_edges = hull_edges(ConvexHull(self.jaw_pts))  # rotation keeps the hull

    def finger_inner_x(self, z: float) -> float:
        """Inner face x of the static finger at height z (tcp frame), -inf if no finger there."""
        xs = [hi[0] for lo, hi in self.fingers if lo[2] <= z <= hi[2]]
        return max(xs) if xs else -math.inf

    def jaw(self, q: float) -> np.ndarray:
        return (self.jaw_rot @ (rot_z(q) @ self.jaw_pts.T)).T + self.jaw_xyz

    def jaw_inner_x(self, q: float, z: float) -> float:
        sl = hull_slice(self.jaw(q), self.jaw_edges, z)
        return float(sl[:, 0].min()) if len(sl) else math.inf


# ---------- grasp solver ----------
def solve(kind: str, piece: PieceProfile, grip: Gripper, xdir: np.ndarray,
          tip: float | None = None) -> dict:
    """xdir: TCP x axis (static -> moving finger) in the piece frame, horizontal unit 2D.
    tip: fingertip height above the board (default: the preferred level of the type)."""
    h = piece.height
    tip = max(TIP_HEIGHT.get(kind, MIN_TIP_HEIGHT) if tip is None else tip,
              h - (grip.wrist_bottom - TOP_CLEARANCE))
    zs = np.linspace(0.0, h - tip, 60)  # heights above the fingertip covered by the piece
    # centre so that the static finger just touches the piece (support towards -x)
    offset = max(piece.support(tip + z, -xdir) + grip.finger_inner_x(z)
                 for z in zs if grip.finger_inner_x(z) > -math.inf)
    far = [(z, offset + piece.support(tip + z, xdir)) for z in zs]

    def gap(q: float) -> float:  # smallest moving jaw - piece distance
        return min(grip.jaw_inner_x(q, z) - x for z, x in far)

    def bisect(fn, lo, hi) -> float:  # fn(lo) < 0 <= fn(hi)
        for _ in range(40):
            mid = 0.5 * (lo + hi)
            lo, hi = (mid, hi) if fn(mid) < 0 else (lo, mid)
        return hi

    contact = bisect(gap, -0.5, 1.5)
    # while descending the piece is FINGER_CLEARANCE further towards the moving jaw
    q_open = bisect(lambda q: gap(q) - FINGER_CLEARANCE - OPEN_CLEARANCE, -0.5, 1.5) + OPEN_MARGIN
    return {
        'height': h,
        'tip_height': tip,
        'grasp_offset': offset,
        'gripper_open_position': q_open,
        'gripper_release_position': min(q_open, contact + RELEASE_OPENING),
        'contact_position': contact,
        'gripper_close_position': max(JAW_LOWER, contact - SQUEEZE),
    }


def write_objects_yaml(path: Path, grasps: dict, hover_tip_z: float, board_top: float,
                       grip: Gripper) -> None:
    # measured values (scripts/calibrate_place_offsets.py) survive a regeneration
    measured = {}
    if path.is_file():
        old = yaml.safe_load(path.read_text(encoding='utf-8')) or {}
        measured = {k: v['place_offset'] for k, v in (old.get('objects') or {}).items()
                    if v and 'place_offset' in v}
    lines = [
        '# Pick-and-place parameters per object type (= piece type in chess_board.action).',
        '# Generated by lara5_moveit/scripts/compute_piece_grasps.py from the Isaac pieces',
        '# (OpenChessSet, PhysX convex hulls) and the SO-101 collision geometry in the URDF.',
        '# Re-read on every move: with `colcon build --symlink-install` edits take effect without',
        '# a rebuild or restart.',
        '#',
        '# TCP = lara5_tcp, tip of the static finger (inner face). The SRDF {square}_hover poses',
        f'# put it straight above the square centre at z = {hover_tip_z:.3f} m (board top {board_top:.3f}).',
        '#',
        '# grasp_offset            m,   piece centre - TCP along the TCP x axis (static -> moving',
        '#                              finger). The TCP is shifted by -grasp_offset at the hover, so',
        '#                              the piece ends centred on the square when placed.',
        '# finger_clearance        m,   extra shift away from the piece while picking (no drag)',
        '# place_offset            m,   [x, y] piece centre in the TCP frame while carried, measured in',
        '#                              Isaac (articulation_orchestrator/scripts/calibrate_place_offsets.py);',
        '#                              without it the place uses [grasp_offset, 0]',
        '# place_press             m,   extra down at the place: a slightly tilted piece is set down',
        '# release_retreat         m,   static finger off the placed piece before going up',
        '# tip_height              m,   fingertip above the board at the grasp',
        '# lower_distance          m,   straight down from the hover (hover z - board top - tip_height)',
        '# higher                       the same at higher grips, up to one whose wrist clears a king',
        '#                              on a neighbouring square (the lowest clear level is used)',
        '# lift_distance           m,   straight up after the grasp (default: = lower_distance)',
        '# gripper_open_position   rad, lara5_gripper_finger_joint (limits -0.1745 .. 1.7453)',
        '# gripper_close_position  rad, ~0.3 past the predicted contact: the soft Isaac jaw squeezes',
        '# gripper_release_position rad, opening to let go of a placed piece',
        '',
        'defaults:',
        f'  finger_clearance: {FINGER_CLEARANCE}',
        '  place_press: 0.001',
        '  release_retreat: 0.002',
        '  # wrist above the fingers (URDF collision shapes, bounding boxes): TCP frame, z from',
        '  # the fingertip up; checked against neighbouring pieces to pick the grasp level',
        '  wrist:',
        *[f'    - {{z: [{lo[2]:.4f}, {hi[2]:.4f}], x: [{lo[0]:.4f}, {hi[0]:.4f}], '
          f'y: [{lo[1]:.4f}, {hi[1]:.4f}]}}' for lo, hi in grip.wrist],
        '',
        'objects:',
    ]
    def level(g: dict) -> str:
        return (f'tip_height: {g["tip_height"]:.4f}, grasp_offset: {g["grasp_offset"]:.4f}, '
                f'lower_distance: {hover_tip_z - board_top - g["tip_height"]:.4f}, '
                f'gripper_open_position: {g["gripper_open_position"]:.3f}, '
                f'gripper_close_position: {g["gripper_close_position"]:.3f}, '
                f'gripper_release_position: {g["gripper_release_position"]:.3f}')

    for kind, g in grasps.items():
        place = (f', place_offset: [{measured[kind][0]:.4f}, {measured[kind][1]:.4f}]'
                 if kind in measured else '')
        lines.append(f'  {kind}:   # h {g["height"] * 1000:.1f} mm, contact {g["contact_position"]:.3f}')
        lines.append(f'    {{{level(g)}{place}}}' if 'higher' not in g else
                     f'    {{{level(g)}{place},\n     higher: [')
        if 'higher' in g:
            lines += [f'       {{{level(h)}}},' for h in g['higher']]
            lines[-1] = lines[-1].rstrip(',') + ']}'

    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--hover-tip-z', type=float, default=HOVER_TIP_Z,
                    help='world z of lara5_tcp at the SRDF hover poses')
    ap.add_argument('--board-top', type=float, default=0.020, help='world z of the board top')
    ap.add_argument('--no-write', action='store_true', help='only print the table')
    args = ap.parse_args()

    grip = Gripper(URDF)
    print(f'static finger boxes (tcp frame): '
          f'{[(round(lo[2], 4), round(hi[2], 4), round(hi[0], 4)) for lo, hi in grip.fingers]}')
    print(f'wrist bottom z (tcp frame): {grip.wrist_bottom:.4f}')
    print(f'moving jaw inner x at the tip: q=0 {grip.jaw_inner_x(0.0, 0.002):.4f}, '
          f'q=0.25 {grip.jaw_inner_x(0.25, 0.002):.4f}')

    # TCP x axis in the world at the hover poses (all squares share the seed orientation)
    hover = yaml.safe_load(HOVER_YAML.read_text(encoding='utf-8'))
    x_axis = ArmModel(str(URDF)).fk(np.array(hover['hover']['e2']))[:3, 0]
    xdir = x_axis[:2] / np.linalg.norm(x_axis[:2])
    print(f'TCP x axis in the world (xy): {np.round(xdir, 3).tolist()}')

    hulls = {kind: isaac_piece_hulls(kind) for kind in TYPES}
    profiles = {kind: PieceProfile(h) for kind, h in hulls.items()}
    high_tip = max(p.height for p in profiles.values()) - (grip.wrist_bottom - TOP_CLEARANCE)

    def both_colours(kind: str, tip: float | None = None) -> dict:
        # white pieces stand at yaw 0, black at yaw pi: the axis is -xdir in a black piece
        white = solve(kind, profiles[kind], grip, xdir, tip)
        black = solve(kind, profiles[kind], grip, -xdir, tip)
        # max: close past the later contact, both colours get squeezed (knight: by colour)
        g = {k: max(white[k], black[k]) for k in white}
        g['offset_spread'] = abs(white['grasp_offset'] - black['grasp_offset'])
        return g

    grasps = {}
    for kind in TYPES:
        g = grasps[kind] = both_colours(kind)
        tips = np.arange(g['tip_height'] + LEVEL_STEP, high_tip, LEVEL_STEP).tolist()
        if g['tip_height'] < high_tip - 1e-4:
            g['higher'] = [both_colours(kind, t) for t in tips + [high_tip]]
        print(f'{kind:7s} h={g["height"] * 1000:5.1f}mm tip={g["tip_height"] * 1000:5.1f}mm '
              f'offset={g["grasp_offset"] * 1000:5.1f}mm open={g["gripper_open_position"]:.3f} '
              f'contact={g["contact_position"]:.3f} close={g["gripper_close_position"]:.3f} '
              f'white/black offset spread={g["offset_spread"] * 1000:.1f}mm'
              + (f'  | higher tips {[round(h["tip_height"] * 1000, 1) for h in g["higher"]]} mm'
                 if 'higher' in g else ''))
        if not args.no_write:
            pts = np.vstack(hulls[kind])
            # MoveIt mesh frame: chess_scene_collisions.piece_board_yaw() turns knights by
            # +pi/2 (white); Isaac puts the white knight at yaw 0 -> pre-rotate by -pi/2
            if kind == 'knight':
                pts = (rot_z(-math.pi / 2) @ pts.T).T
            pts = pts[ConvexHull(pts).vertices]
            write_stl(HULL_DIR / f'{kind}.stl', pts, ConvexHull(pts))
    if not args.no_write:
        write_objects_yaml(OBJECTS_YAML, grasps, args.hover_tip_z, args.board_top, grip)
        print('wrote', HULL_DIR, 'and', OBJECTS_YAML)


if __name__ == '__main__':
    main()
