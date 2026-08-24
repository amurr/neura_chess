"""Tests for Isaac JointState padding."""

from __future__ import annotations

import math

from builtin_interfaces.msg import Duration, Time
from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

from lara5_moveit.pad_joint_commands import pad_joint_state
from lara5_moveit.relay_isaac_joint_states import wall_stamp_joint_state
from lara5_moveit.sanitize_trajectory import sanitize_joint_trajectory


def test_pad_fills_empty_velocity_effort_with_nan() -> None:
    msg = JointState()
    msg.name = ['lara5_joint1', 'lara5_joint2']
    msg.position = [0.1, -0.2]
    out = pad_joint_state(msg)
    assert list(out.name) == msg.name
    assert list(out.position) == [0.1, -0.2]
    assert len(out.velocity) == 2
    assert len(out.effort) == 2
    assert all(math.isnan(v) for v in out.velocity)
    assert all(math.isnan(v) for v in out.effort)


def test_pad_keeps_matching_velocity() -> None:
    msg = JointState()
    msg.name = ['j']
    msg.position = [1.0]
    msg.velocity = [0.5]
    msg.effort = [0.0]
    out = pad_joint_state(msg)
    assert list(out.velocity) == [0.5]
    assert list(out.effort) == [0.0]


def test_wall_stamp_replaces_sim_time() -> None:
    msg = JointState()
    msg.header.stamp.sec = 51
    msg.name = ['lara5_joint1']
    msg.position = [0.1]
    stamp = Time(sec=1787585841, nanosec=0)
    out = wall_stamp_joint_state(msg, stamp)
    assert out.header.stamp.sec == 1787585841
    assert list(out.position) == [0.1]


def test_sanitize_makes_zero_times_strictly_increasing() -> None:
    traj = JointTrajectory()
    traj.joint_names = ['lara5_joint1']
    for _ in range(2):
        pt = JointTrajectoryPoint()
        pt.positions = [0.0]
        pt.time_from_start = Duration(sec=0, nanosec=0)
        traj.points.append(pt)
    out = sanitize_joint_trajectory(traj, min_dt_s=0.05)
    t0 = out.points[0].time_from_start.sec + out.points[0].time_from_start.nanosec * 1e-9
    t1 = out.points[1].time_from_start.sec + out.points[1].time_from_start.nanosec * 1e-9
    assert t1 > t0
