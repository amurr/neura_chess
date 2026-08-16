# Lara5 meshes

Arm visual STLs (`Link0_body.stl` … `Link6_body.stl`) and collision STLs live here and in `../collision/`. They are tracked in git via **Git LFS**.

SO-101 gripper STLs in `so101/` are not in git — `scripts/setup_lara5_assets.sh` downloads them.

One-time on a dev machine (if arm STLs are missing after clone):

```bash
NEURA_MESH_SRC=/path/to/neura_robot_description/lara5 bash scripts/seed_lara5_meshes.sh
git lfs install
git add src/lara5_description/lara5/meshes/*.stl src/lara5_description/lara5/collision/*.stl
git commit -m "Add Lara5 arm meshes"
git push
```

After clone on any machine: `git lfs pull`
