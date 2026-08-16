"""Integration-style tests for camera_xyz_to_joints node.

Runs the subscription callback end-to-end with faked TF + MoveIt IK.
"""

from __future__ import annotations

from dataclasses import dataclass

import pytest

rclpy = pytest.importorskip("rclpy")
from geometry_msgs.msg import PointStamped, TransformStamped
from moveit_msgs.msg import MoveItErrorCodes
from moveit_msgs.srv import GetPositionIK
from rclpy.time import Time
from sensor_msgs.msg import JointState

import xyz_motion.camera_xyz_to_joints as mod
from xyz_motion.camera_xyz_to_joints import CameraXyzToJointsNode


@dataclass
class _PubCapture:
    msgs: list

    def publish(self, msg):
        self.msgs.append(msg)


class _DoneFuture:
    def __init__(self, value):
        self._value = value

    def done(self) -> bool:
        return True

    def result(self):
        return self._value


class _FakeIkClient:
    def __init__(self, response: GetPositionIK.Response):
        self._resp = response

    def service_is_ready(self) -> bool:
        return True

    def call_async(self, _req):
        return _DoneFuture(self._resp)


class _FakeTfBuffer:
    def __init__(self, transform: TransformStamped):
        self.transform = transform
        self.calls = []

    def lookup_transform(self, target_frame, source_frame, time, timeout=None):
        self.calls.append((target_frame, source_frame, time, timeout))
        return self.transform


def _fake_do_transform_point(pt: PointStamped, tf: TransformStamped) -> PointStamped:
    out = PointStamped()
    out.header = pt.header
    out.point.x = pt.point.x + tf.transform.translation.x
    out.point.y = pt.point.y + tf.transform.translation.y
    out.point.z = pt.point.z + tf.transform.translation.z
    return out


def test_point_to_ik_solution_full_flow(monkeypatch):
    rclpy.init()
    try:
        node = CameraXyzToJointsNode()

        # Deterministic parameters for assertions.
        node._base_frame = "base_link"
        node._camera_frame = "camera_frame"
        node._assume_base = False
        node._z_offset = 0.1
        node._joint_names = ["j1", "j2"]

        # Capture published messages.
        target_pub = _PubCapture([])
        ik_pub = _PubCapture([])
        node._target_pose_pub = target_pub
        node._ik_solution_pub = ik_pub

        # Fake TF: translate by (1,2,3).
        tf = TransformStamped()
        tf.header.frame_id = "base_link"
        tf.child_frame_id = "camera_frame"
        tf.transform.translation.x = 1.0
        tf.transform.translation.y = 2.0
        tf.transform.translation.z = 3.0
        node._tf_buffer = _FakeTfBuffer(tf)

        monkeypatch.setattr(mod, "do_transform_point", _fake_do_transform_point)

        # Fake IK response.
        resp = GetPositionIK.Response()
        resp.error_code = MoveItErrorCodes()
        resp.error_code.val = MoveItErrorCodes.SUCCESS
        resp.solution.joint_state = JointState(name=["j1", "j2"], position=[0.5, -0.5])
        node._ik_client = _FakeIkClient(resp)

        # Send input point with a real timestamp.
        msg = PointStamped()
        msg.header.frame_id = "camera_frame"
        msg.header.stamp.sec = 10
        msg.header.stamp.nanosec = 20
        msg.point.x = 0.1
        msg.point.y = 0.2
        msg.point.z = 0.3

        node._on_object_xyz(msg)

        # TF was queried at the message time.
        assert len(node._tf_buffer.calls) == 1
        _, _, t, _ = node._tf_buffer.calls[0]
        assert isinstance(t, Time)
        assert t.nanoseconds == 10 * 1_000_000_000 + 20

        # Target pose published in base frame with z-offset applied after TF.
        assert len(target_pub.msgs) == 1
        target = target_pub.msgs[0]
        assert target.header.frame_id == "base_link"
        assert pytest.approx(target.pose.position.x) == 1.1
        assert pytest.approx(target.pose.position.y) == 2.2
        assert pytest.approx(target.pose.position.z) == 3.3 + 0.1

        # IK solution published.
        assert len(ik_pub.msgs) == 1
        out = ik_pub.msgs[0]
        assert out.name == ["j1", "j2"]
        assert out.position == [0.5, -0.5]
    finally:
        rclpy.shutdown()

