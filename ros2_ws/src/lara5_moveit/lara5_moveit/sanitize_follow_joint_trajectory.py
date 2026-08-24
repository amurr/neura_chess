"""Action relay: sanitize FollowJointTrajectory times, then forward to hardware.

MoveIt sends goals to follow_joint_trajectory_safe. This node fixes zero-dt
MTC points and forwards them to the JointTrajectoryController.
"""

from __future__ import annotations

import rclpy
from control_msgs.action import FollowJointTrajectory
from rclpy.action import ActionClient, ActionServer, CancelResponse, GoalResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.node import Node

from lara5_moveit.sanitize_trajectory import sanitize_joint_trajectory


class SanitizeFollowJointTrajectory(Node):
    """Accept MoveIt goals, fix times, forward to the hardware controller."""

    def __init__(self) -> None:
        super().__init__('sanitize_follow_joint_trajectory')
        inn = str(
            self.declare_parameter(
                'in_action', '/arm_controller/follow_joint_trajectory_safe'
            ).value
        )
        out = str(
            self.declare_parameter(
                'out_action', '/arm_controller/follow_joint_trajectory'
            ).value
        )
        cb = ReentrantCallbackGroup()
        self._client = ActionClient(self, FollowJointTrajectory, out, callback_group=cb)
        self._server = ActionServer(
            self,
            FollowJointTrajectory,
            inn,
            execute_callback=self._execute,
            goal_callback=self._on_goal,
            cancel_callback=self._on_cancel,
            callback_group=cb,
        )
        self.get_logger().info(f'sanitize {inn} → {out}')

    def _on_goal(self, _goal_request) -> GoalResponse:
        return GoalResponse.ACCEPT

    def _on_cancel(self, _cancel_request) -> CancelResponse:
        return CancelResponse.ACCEPT

    async def _execute(self, goal_handle):
        if not self._client.wait_for_server(timeout_sec=5.0):
            self.get_logger().error('hardware FollowJointTrajectory server missing')
            goal_handle.abort()
            return FollowJointTrajectory.Result()
        goal = FollowJointTrajectory.Goal()
        goal.trajectory = sanitize_joint_trajectory(goal_handle.request.trajectory)
        goal.path_tolerance = goal_handle.request.path_tolerance
        goal.goal_tolerance = goal_handle.request.goal_tolerance
        goal.goal_time_tolerance = goal_handle.request.goal_time_tolerance
        times = [
            float(p.time_from_start.sec) + float(p.time_from_start.nanosec) * 1e-9
            for p in goal.trajectory.points
        ]
        self.get_logger().info(
            f'sanitized {len(times)} pts t={times[:8]}{"..." if len(times) > 8 else ""}'
        )
        send = await self._client.send_goal_async(goal)
        if send is None or not send.accepted:
            self.get_logger().error('hardware rejected sanitized trajectory')
            goal_handle.abort()
            return FollowJointTrajectory.Result()
        result_wrap = await send.get_result_async()
        result = result_wrap.result
        if result.error_code == 0:
            goal_handle.succeed()
        else:
            self.get_logger().error(f'hardware error_code={result.error_code}')
            goal_handle.abort()
        return result


def main() -> None:
    """Spin the FollowJointTrajectory sanitizing relay."""
    rclpy.init()
    node = SanitizeFollowJointTrajectory()
    executor = rclpy.executors.MultiThreadedExecutor()
    executor.add_node(node)
    try:
        executor.spin()
    finally:
        executor.shutdown()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
