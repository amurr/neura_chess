#!/usr/bin/env python3
"""Download SO-101 gripper STL files into lara5/meshes/so101."""
from __future__ import annotations

import pathlib
import urllib.request

BASE = "https://raw.githubusercontent.com/TheRobotStudio/SO-ARM100/main/STL/SO101/Individual"
FILES = {
    "moving_jaw_so101_v1.stl": "Moving_Jaw_SO101.stl",
    "wrist_roll_follower_so101_v1.stl": "Wrist_Roll_Follower_SO101.stl",
}


def main() -> None:
    root = pathlib.Path(__file__).resolve().parents[1]
    out_dir = root / "lara5" / "meshes" / "so101"
    out_dir.mkdir(parents=True, exist_ok=True)
    for local, remote in FILES.items():
        dest = out_dir / local
        url = f"{BASE}/{remote}"
        print(f"Downloading {url} -> {dest}")
        urllib.request.urlretrieve(url, dest)
        print(f"  OK {dest.stat().st_size} bytes")
    print(f"Done. Meshes in {out_dir}")


if __name__ == "__main__":
    main()
