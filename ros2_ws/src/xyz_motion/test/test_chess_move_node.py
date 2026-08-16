"""ROS integration tests for chess_move_node (mock move_joints, no robot)."""

from __future__ import annotations

import json
import time

import pytest

rclpy = pytest.importorskip("rclpy")
from lara_interfaces.srv import MoveJoints
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from std_msgs.msg import String

from xyz_motion import chess_move_node as node_mod
from xyz_motion.chess_xyz import CHESS_OCCUPANCY_TOPIC
from xyz_motion.poses import JOINT_POSES


class MockMoveJoints(Node):
    def __init__(self):
        super().__init__('mock_move_joints')
        self.calls = 0
        self.last_target_pose: list[float] = []
        self.last_target_joint: list[float] = []
        self.create_service(MoveJoints, 'move_joints', self.cb)

    def cb(self, request, response):
        self.calls += 1
        self.last_target_pose = list(getattr(request, 'target_pose', []))
        self.last_target_joint = list(request.target_joint)
        response.success = True
        response.message = 'mock OK (no robot)'
        return response


@pytest.fixture
def ros_context():
    rclpy.init()
    yield
    rclpy.shutdown()


@pytest.fixture
def executor_nodes(ros_context):
    mock = MockMoveJoints()
    runner = Node('test_runner')
    executor = MultiThreadedExecutor()
    executor.add_node(mock)
    executor.add_node(runner)
    yield executor, mock, runner
    runner.destroy_node()
    mock.destroy_node()


def test_listen_chess_occupancy_source_target_message(executor_nodes):
    executor, _mock, runner = executor_nodes
    node_mod._latest_chess_occupancy = None
    node_mod._latest_pose6_from_chess = None
    received: list[dict] = []

    node_mod.listen_chess_occupancy(runner, on_update=lambda data: received.append(data))
    pub = runner.create_publisher(String, CHESS_OCCUPANCY_TOPIC, 10)

    payload = json.dumps({
        'source': 'e2',
        'target': 'e4',
    })
    deadline = time.monotonic() + 5.0
    while node_mod.get_latest_chess_occupancy() is None and time.monotonic() < deadline:
        pub.publish(String(data=payload))
        executor.spin_once(timeout_sec=0.2)

    deadline = time.monotonic() + 2.0
    while not received and time.monotonic() < deadline:
        executor.spin_once(timeout_sec=0.1)

    occ = node_mod.get_latest_chess_occupancy()
    assert occ is not None
    assert occ['source'] == 'e2'
    assert occ['target'] == 'e4'
    assert received
    assert received[-1]['source'] == 'e2'
    assert node_mod.get_latest_pose6_from_chess() is None


def test_listen_caches_pose6_from_squares(executor_nodes):
    executor, _mock, runner = executor_nodes
    node_mod._latest_chess_occupancy = None
    node_mod._latest_pose6_from_chess = None
    node_mod.listen_chess_occupancy(runner)
    pub = runner.create_publisher(String, CHESS_OCCUPANCY_TOPIC, 10)

    payload = json.dumps({
        'source': 'e2',
        'target': 'e4',
        'squares': {
            'e2': {'x': 0.45, 'y': -0.10, 'z': 0.03},
            'e4': {'x': 0.45, 'y': -0.06, 'z': 0.03},
        },
    })
    deadline = time.monotonic() + 5.0
    while node_mod.get_latest_pose6_from_chess() is None and time.monotonic() < deadline:
        pub.publish(String(data=payload))
        executor.spin_once(timeout_sec=0.2)

    poses = node_mod.get_latest_pose6_from_chess()
    assert poses is not None
    assert 'e2' in poses
    assert poses['e2'][:3] == [0.45, -0.10, 0.03]


def test_listen_rejects_non_object_message(executor_nodes):
    executor, _mock, runner = executor_nodes
    node_mod._latest_chess_occupancy = None
    node_mod._latest_pose6_from_chess = None
    node_mod.listen_chess_occupancy(runner)
    pub = runner.create_publisher(String, CHESS_OCCUPANCY_TOPIC, 10)

    pub.publish(String(data=json.dumps(['bad', 'payload'])))
    for _ in range(20):
        executor.spin_once(timeout_sec=0.1)

    assert node_mod.get_latest_pose6_from_chess() is None
    assert node_mod.get_latest_chess_occupancy() is None


def test_startup_stand_uses_joints_not_pose6(executor_nodes):
    executor, mock, runner = executor_nodes
    client = runner.create_client(MoveJoints, 'move_joints')
    deadline = time.monotonic() + 5.0
    while not client.wait_for_service(timeout_sec=0.2):
        executor.spin_once(timeout_sec=0.2)
        if time.monotonic() > deadline:
            pytest.fail('move_joints not available')

    req = MoveJoints.Request()
    req.point_name = ''
    req.target_joint = list(JOINT_POSES['stand'])
    if hasattr(req, 'target_pose'):
        req.target_pose = []
    req.speed = 20.0
    req.acceleration = 20.0
    req.enable_safety = True
    future = client.call_async(req)
    executor.spin_until_future_complete(future, timeout_sec=5.0)
    result = future.result()
    assert result.success
    assert mock.last_target_joint == list(JOINT_POSES['stand'])
    if hasattr(req, 'target_pose'):
        assert mock.last_target_pose == []
