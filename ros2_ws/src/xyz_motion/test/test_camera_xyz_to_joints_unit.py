"""Unit tests for camera_xyz_to_joints helpers (minimal ROS usage)."""

from __future__ import annotations

import math

import pytest

rclpy = pytest.importorskip("rclpy")
from geometry_msgs.msg import PointStamped

from xyz_motion.camera_xyz_to_joints import CameraXyzToJointsNode, _rpy_to_quaternion


def test_rpy_to_quaternion_identity():
    qx, qy, qz, qw = _rpy_to_quaternion(0.0, 0.0, 0.0)
    assert qx == 0.0
    assert qy == 0.0
    assert qz == 0.0
    assert qw == 1.0


def test_rpy_to_quaternion_normalized():
    qx, qy, qz, qw = _rpy_to_quaternion(0.1, -0.3, 0.7)
    norm = math.sqrt(qx * qx + qy * qy + qz * qz + qw * qw)
    assert norm == pytest.approx(1.0, rel=1e-9, abs=1e-9)


def test_tf_lookup_time_prefers_header_stamp():
    from rclpy.time import Time

    msg = PointStamped()
    msg.header.stamp.sec = 123
    msg.header.stamp.nanosec = 456
    t = CameraXyzToJointsNode._tf_lookup_time_for_point(msg)
    assert isinstance(t, Time)
    assert t.nanoseconds == 123 * 1_000_000_000 + 456


def test_tf_lookup_time_falls_back_to_latest_on_zero_stamp():
    from rclpy.time import Time

    msg = PointStamped()
    msg.header.stamp.sec = 0
    msg.header.stamp.nanosec = 0
    t = CameraXyzToJointsNode._tf_lookup_time_for_point(msg)
    assert isinstance(t, Time)
    assert t.nanoseconds == 0


def test_seed_positions_prefers_last_ik_then_joint_state(monkeypatch):
    rclpy.init()
    try:
        node = CameraXyzToJointsNode()
        node._joint_names = ['j1', 'j2', 'j3']  # simplify
        node._use_last_seed = True
        node._last_ik_seed = [1.0, 2.0, 3.0]
        node._latest_joint_positions = [9.0, 9.0, 9.0]
        assert node._seed_positions() == [1.0, 2.0, 3.0]

        node._last_ik_seed = None
        assert node._seed_positions() == [9.0, 9.0, 9.0]

        node._latest_joint_positions = None
        assert node._seed_positions() == [0.0, 0.0, 0.0]
    finally:
        rclpy.shutdown()

