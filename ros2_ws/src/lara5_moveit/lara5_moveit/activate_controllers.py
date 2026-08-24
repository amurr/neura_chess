"""Load, configure, and activate Lara5 ros2_control controllers.

Launch spawners often race the controller_manager and exit before arm_controller
exists, so MoveIt aborts on the first gripper/arm action. This node retries
until the named controllers are active, then exits.
"""

from __future__ import annotations

import sys
import time

import rclpy
from controller_manager_msgs.srv import (
    ConfigureController,
    ListControllers,
    LoadController,
    SwitchController,
)
from rclpy.node import Node

DEFAULT_CONTROLLERS = (
    'joint_state_broadcaster',
    'arm_controller',
    'gripper_controller',
)


class ActivateControllers(Node):
    """Retry load/configure/activate until every requested controller is active."""

    def __init__(self) -> None:
        super().__init__('activate_controllers')
        names = self.declare_parameter('controllers', list(DEFAULT_CONTROLLERS)).value
        self._timeout_s = float(self.declare_parameter('timeout_s', 60.0).value)
        self._manager = str(
            self.declare_parameter('controller_manager', '/controller_manager').value
        )
        self._names = [str(n) for n in names]
        self._list = self.create_client(ListControllers, f'{self._manager}/list_controllers')
        self._load = self.create_client(LoadController, f'{self._manager}/load_controller')
        self._configure = self.create_client(
            ConfigureController, f'{self._manager}/configure_controller'
        )
        self._switch = self.create_client(SwitchController, f'{self._manager}/switch_controller')

    def _call(self, client, request, timeout_s: float = 8.0):
        if not client.wait_for_service(timeout_sec=timeout_s):
            return None
        future = client.call_async(request)
        rclpy.spin_until_future_complete(self, future, timeout_sec=timeout_s)
        return future.result()

    def _states(self) -> dict[str, str]:
        result = self._call(self._list, ListControllers.Request())
        if result is None:
            return {}
        return {c.name: c.state for c in result.controller}

    def run(self) -> int:
        """Retry until every controller is active or timeout_s elapses."""
        deadline = time.monotonic() + self._timeout_s
        while time.monotonic() < deadline:
            states = self._states()
            missing = [name for name in self._names if states.get(name) != 'active']
            if not missing:
                self.get_logger().info(f'active: {self._names}')
                return 0
            for name in missing:
                state = states.get(name)
                if state is None:
                    req = LoadController.Request()
                    req.name = name
                    result = self._call(self._load, req)
                    self.get_logger().info(f'load {name}: {getattr(result, "ok", result)}')
                    states = self._states()
                    state = states.get(name)
                if state == 'unconfigured':
                    req = ConfigureController.Request()
                    req.name = name
                    result = self._call(self._configure, req)
                    self.get_logger().info(
                        f'configure {name}: {getattr(result, "ok", result)}'
                    )
            inactive = [
                name for name in self._names if self._states().get(name) != 'active'
            ]
            if inactive:
                req = SwitchController.Request()
                req.activate_controllers = inactive
                req.deactivate_controllers = []
                req.strictness = SwitchController.Request.BEST_EFFORT
                req.activate_asap = True
                result = self._call(self._switch, req)
                self.get_logger().info(
                    f'activate {inactive}: {getattr(result, "ok", result)}'
                )
            time.sleep(1.0)
        self.get_logger().error(f'timeout; last states={self._states()}')
        return 1


def main() -> int:
    """Activate arm, gripper, and joint_state_broadcaster, then exit."""
    rclpy.init()
    node = ActivateControllers()
    try:
        return node.run()
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    sys.exit(main())
