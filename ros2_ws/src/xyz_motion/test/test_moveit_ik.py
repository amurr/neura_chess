"""Unit tests for moveit_ik helpers (no MoveIt service)."""

from __future__ import annotations

import math

from xyz_motion.moveit_ik import (
    joint_positions_rad_to_deg,
    pose6_to_pose_stamped,
    pose6_with_z_offset,
    rpy_to_quaternion,
)


def test_rpy_to_quaternion_identity():
    qx, qy, qz, qw = rpy_to_quaternion(0.0, 0.0, 0.0)
    assert qw == 1.0
    assert qx == qy == qz == 0.0


def test_pose6_to_pose_stamped():
    msg = pose6_to_pose_stamped([0.1, 0.2, 0.3, 0.0, 0.0, 0.0], 'world')
    assert msg.header.frame_id == 'world'
    assert msg.pose.position.x == 0.1
    assert msg.pose.orientation.w == 1.0


def test_pose6_with_z_offset():
    out = pose6_with_z_offset([1.0, 2.0, 3.0, 0.0, 0.0, 0.0], 0.08)
    assert out[2] == 3.08


def test_joint_positions_rad_to_deg():
    out = joint_positions_rad_to_deg([0.0, math.pi / 2.0])
    assert out[0] == 0.0
    assert out[1] == 90.0
