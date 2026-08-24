"""Sanitize JointTrajectory times so ros2_control will accept MTC cartesian stages.

JointTrajectoryController rejects goals whose points are not strictly increasing
in time_from_start. MTC Connect/Cartesian stages often emit two points both at t=0.
"""

from __future__ import annotations

from typing import Sequence

from builtin_interfaces.msg import Duration
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

MIN_DT_S = 0.05


def _stamp_s(duration: Duration) -> float:
    return float(duration.sec) + float(duration.nanosec) * 1e-9


def _duration(seconds: float) -> Duration:
    if seconds < 0.0:
        seconds = 0.0
    sec = int(seconds)
    nanosec = int(round((seconds - sec) * 1e9))
    if nanosec >= 1_000_000_000:
        sec += 1
        nanosec -= 1_000_000_000
    return Duration(sec=sec, nanosec=nanosec)


def sanitize_joint_trajectory(
    traj: JointTrajectory, *, min_dt_s: float = MIN_DT_S
) -> JointTrajectory:
    """Return a copy whose point times are strictly increasing."""
    out = JointTrajectory()
    out.header = traj.header
    out.joint_names = list(traj.joint_names)
    prev = -min_dt_s
    for src in traj.points:
        dst = JointTrajectoryPoint()
        dst.positions = list(src.positions)
        dst.velocities = list(src.velocities)
        dst.accelerations = list(src.accelerations)
        dst.effort = list(src.effort)
        t = _stamp_s(src.time_from_start)
        if t <= prev:
            t = prev + min_dt_s
        dst.time_from_start = _duration(t)
        out.points.append(dst)
        prev = t
    return out


def points_strictly_increasing(points: Sequence[JointTrajectoryPoint]) -> bool:
    """True when successive time_from_start values increase."""
    prev = -1.0
    for point in points:
        t = _stamp_s(point.time_from_start)
        if t <= prev:
            return False
        prev = t
    return True
