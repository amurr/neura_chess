"""Load pre-built convex-hull chess piece meshes for MoveIt collision."""

from __future__ import annotations

import struct
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from geometry_msgs.msg import Point
from shape_msgs.msg import Mesh, MeshTriangle

PIECE_MESH_TYPES = frozenset({'pawn', 'rook', 'knight', 'bishop', 'queen', 'king'})


@dataclass(frozen=True)
class PieceMeshInfo:
    piece_type: str
    mesh: Mesh
    height_m: float
    base_diameter_m: float


def _package_mesh_dir(subdir: str = 'collision_hulls') -> Path | None:
    try:
        from ament_index_python.packages import get_package_share_directory

        return Path(get_package_share_directory('xyz_motion')) / 'meshes' / 'chess_pieces' / subdir
    except Exception:
        return None


def _source_mesh_dir(subdir: str = 'collision_hulls') -> Path:
    installed = _package_mesh_dir(subdir)
    if installed is not None and installed.is_dir():
        return installed
    return Path(__file__).resolve().parent.parent / 'meshes' / 'chess_pieces' / subdir


def load_binary_stl(path: Path) -> tuple[list[tuple[float, float, float]], list[tuple[int, int, int]]]:
    data = path.read_bytes()
    tri_count = struct.unpack_from('<I', data, 80)[0]
    raw_verts: list[tuple[float, float, float]] = []
    offset = 84
    for _ in range(tri_count):
        offset += 12
        tri: list[int] = []
        for __ in range(3):
            x, y, z = struct.unpack_from('<fff', data, offset)
            raw_verts.append((x, y, z))
            tri.append(len(raw_verts) - 1)
            offset += 12
        offset += 2
    return raw_verts, [(tri[0], tri[1], tri[2])]


def stl_to_shape_mesh(path: Path) -> Mesh:
    vertices, triangles = load_binary_stl(path)
    mesh = Mesh()
    mesh.vertices = [Point(x=float(x), y=float(y), z=float(z)) for x, y, z in vertices]
    mesh.triangles = [
        MeshTriangle(vertex_indices=[int(a), int(b), int(c)]) for a, b, c in triangles
    ]
    return mesh


def _mesh_height(mesh: Mesh) -> float:
    if not mesh.vertices:
        return 0.0
    return max(float(v.z) for v in mesh.vertices)


def _mesh_base_diameter(mesh: Mesh) -> float:
    if not mesh.vertices:
        return 0.0
    xs = [float(v.x) for v in mesh.vertices]
    ys = [float(v.y) for v in mesh.vertices]
    return max(max(xs) - min(xs), max(ys) - min(ys))


class PieceMeshLibrary:
    """Cached convex-hull meshes keyed by piece type."""

    def __init__(self, mesh_dir: Path | None = None) -> None:
        self._mesh_dir = mesh_dir if mesh_dir is not None else _source_mesh_dir()

    @property
    def mesh_dir(self) -> Path:
        return self._mesh_dir

    def available(self) -> bool:
        return all((self._mesh_dir / f'{ptype}.stl').is_file() for ptype in PIECE_MESH_TYPES)

    @lru_cache(maxsize=len(PIECE_MESH_TYPES))
    def get(self, piece_type: str) -> PieceMeshInfo:
        ptype = piece_type.strip().lower()
        if ptype not in PIECE_MESH_TYPES:
            raise ValueError(f'unknown piece type {piece_type!r}')
        path = self._mesh_dir / f'{ptype}.stl'
        if not path.is_file():
            raise FileNotFoundError(f'collision hull missing: {path}')
        mesh = stl_to_shape_mesh(path)
        return PieceMeshInfo(
            piece_type=ptype,
            mesh=mesh,
            height_m=_mesh_height(mesh),
            base_diameter_m=_mesh_base_diameter(mesh),
        )

    def piece_height(self, piece_type: str) -> float:
        return self.get(piece_type).height_m

    def mesh_resource_uri(self, piece_type: str) -> str:
        ptype = piece_type.strip().lower()
        if ptype not in PIECE_MESH_TYPES:
            raise ValueError(f'unknown piece type {piece_type!r}')
        return f'package://xyz_motion/meshes/chess_pieces/collision_hulls/{ptype}.stl'


@lru_cache(maxsize=1)
def default_piece_mesh_library() -> PieceMeshLibrary:
    return PieceMeshLibrary()
