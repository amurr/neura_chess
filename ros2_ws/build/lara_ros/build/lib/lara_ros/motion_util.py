"""Helpers for NeuraPy motion services."""

from __future__ import annotations

import math
import time
from typing import List, Optional

from lara_ros.neurapy.robot import Robot


def tcp_pose_close(
    tcp: List[float],
    target: List[float],
    pos_tol_m: float = 0.003,
    rot_tol_rad: float = 0.05,
) -> bool:
    for i in range(3):
        if abs(float(tcp[i]) - float(target[i])) > pos_tol_m:
            return False
    for i in range(3, 6):
        if abs(float(tcp[i]) - float(target[i])) > rot_tol_rad:
            return False
    return True


def offset_norm(offset: List[float]) -> float:
    return math.sqrt(sum(float(v) ** 2 for v in offset[:6]))


def wait_motion_with_timeout(
    robot: Robot,
    timeout_sec: float = 120.0,
    poll_sec: float = 0.05,
) -> None:
    """Poll wait_motion_finished; raise TimeoutError if motion never completes."""
    deadline = time.monotonic() + timeout_sec
    while time.monotonic() < deadline:
        try:
            robot.wait_motion_finished()
            return
        except Exception:
            time.sleep(poll_sec)
    raise TimeoutError(
        f"Motion did not finish within {timeout_sec:.0f}s "
        "(robot may already be at target, or wait_motion_finished is stuck)"
    )
