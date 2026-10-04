#!/usr/bin/env python3
"""
this file fakes the controllers MoveIt expects, so Execute (and MTC task.execute())
works without ros2_control, Isaac Sim or hardware. It serves the two actions declared
in lara5_moveit_config/config/moveit_controllers.yaml and replays whatever trajectory
MoveIt sends by publishing /joint_states in real time.

Replaces joint_state_publisher_gui: both publish /joint_states, so run only one.

Started by rviz_moveit.launch.py (fake_controllers:=true), or:

    ros2 run lara5_moveit fake_controllers
"""

from __future__ import annotations

import threading
import time
from typing import Sequence

import rclpy
from builtin_interfaces.msg import Duration as DurationMsg
from control_msgs.action import FollowJointTrajectory, GripperCommand
from rclpy.action import ActionServer, CancelResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectoryPoint

ARM_JOINTS = [f'lara5_joint{i}' for i in range(1, 7)]
GRIPPER_JOINT = 'lara5_gripper_finger_joint'
GRIPPER_TRAVEL_TIME = 0.5


def _seconds(d: DurationMsg) -> float:
    return float(d.sec) + float(d.nanosec) * 1e-9


def _sample(points: Sequence[JointTrajectoryPoint], t: float) -> Sequence[float]:
    """Linearly interpolate joint positions at time t along the trajectory."""
    if t <= _seconds(points[0].time_from_start):
        return points[0].positions
    for prev, nxt in zip(points, points[1:]):
        t0, t1 = _seconds(prev.time_from_start), _seconds(nxt.time_from_start)
        if t <= t1:
            span = t1 - t0
            alpha = 1.0 if span <= 0.0 else (t - t0) / span
            return [p0 + alpha * (p1 - p0) for p0, p1 in zip(prev.positions, nxt.positions)]
    return points[-1].positions


class FakeControllers(Node):
    def __init__(self) -> None:
        super().__init__('fake_controllers')

        self.declare_parameter('arm_joints', ARM_JOINTS)
        self.declare_parameter('gripper_joint', GRIPPER_JOINT)
        self.declare_parameter('arm_action', '/arm_controller/follow_joint_trajectory_safe')
        self.declare_parameter('gripper_action', '/gripper_controller/gripper_cmd')
        self.declare_parameter('publish_rate', 50.0)

        arm_joints = list(self.get_parameter('arm_joints').value)
        gripper_joint = str(self.get_parameter('gripper_joint').value)
        self._rate = float(self.get_parameter('publish_rate').value)
        self._dt = 1.0 / self._rate

        self._lock = threading.Lock()
        self._positions = {name: 0.0 for name in [*arm_joints, gripper_joint]}

        group = ReentrantCallbackGroup()
        self._pub = self.create_publisher(JointState, 'joint_states', 10)
        self.create_timer(self._dt, self._publish_state, callback_group=group)

        arm_action = str(self.get_parameter('arm_action').value)
        gripper_action = str(self.get_parameter('gripper_action').value)
        ActionServer(
            self,
            FollowJointTrajectory,
            arm_action,
            execute_callback=self._follow_trajectory,
            cancel_callback=lambda _goal: CancelResponse.ACCEPT,
            callback_group=group,
        )
        ActionServer(
            self,
            GripperCommand,
            gripper_action,
            execute_callback=self._gripper_command,
            cancel_callback=lambda _goal: CancelResponse.ACCEPT,
            callback_group=group,
        )
        self.get_logger().info(
            f'fake controllers ready: {arm_action}, {gripper_action}; '
            f'publishing /joint_states at {self._rate:g} Hz'
        )

    def _publish_state(self) -> None:
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        with self._lock:
            msg.name = list(self._positions)
            msg.position = list(self._positions.values())
        self._pub.publish(msg)

    def _set(self, names: Sequence[str], positions: Sequence[float]) -> None:
        with self._lock:
            for name, position in zip(names, positions):
                if name in self._positions:
                    self._positions[name] = float(position)

    def _follow_trajectory(self, goal_handle):
        trajectory = goal_handle.request.trajectory
        points = trajectory.points
        result = FollowJointTrajectory.Result()

        if not points:
            goal_handle.succeed()
            result.error_code = FollowJointTrajectory.Result.SUCCESSFUL
            return result

        duration = _seconds(points[-1].time_from_start)
        self.get_logger().info(
            f'executing {len(points)} points over {duration:.2f} s '
            f'for [{", ".join(trajectory.joint_names)}]'
        )

        start = time.monotonic()
        while rclpy.ok():
            elapsed = time.monotonic() - start
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().warn('trajectory canceled')
                return result
            self._set(trajectory.joint_names, _sample(points, elapsed))
            if elapsed >= duration:
                break
            time.sleep(self._dt)

        self._set(trajectory.joint_names, points[-1].positions)
        goal_handle.succeed()
        result.error_code = FollowJointTrajectory.Result.SUCCESSFUL
        return result

    def _gripper_command(self, goal_handle):
        joint = str(self.get_parameter('gripper_joint').value)
        target = float(goal_handle.request.command.position)
        with self._lock:
            start_position = self._positions.get(joint, 0.0)

        start = time.monotonic()
        while rclpy.ok():
            alpha = min((time.monotonic() - start) / GRIPPER_TRAVEL_TIME, 1.0)
            self._set([joint], [start_position + alpha * (target - start_position)])
            if alpha >= 1.0:
                break
            time.sleep(self._dt)

        goal_handle.succeed()
        result = GripperCommand.Result()
        result.position = target
        result.reached_goal = True
        return result


def main(args=None) -> None:
    rclpy.init(args=args)
    node = FakeControllers()
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
