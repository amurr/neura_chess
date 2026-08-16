#!/usr/bin/env python3
import time
from typing import List, Optional

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import JointState
from lara_interfaces.srv import MoveJoints, GetAppMode


class LARA_Gummy_Bear(Node):
    def __init__(self):
        super().__init__('gummy_bear')

        # ---------- Params ----------
        self.declare_parameter('service_name', 'move_joints')          # relative: inherits namespace
        self.declare_parameter('app_mode_service', 'get_app_mode')
        self.declare_parameter('joint_states_topic', '/lara/joint_states_deg')

        self.declare_parameter('speed', 80.0)
        self.declare_parameter('acceleration', 40.0)
        self.declare_parameter('enable_safety', True)

        # Sequence poses (degrees) — adapt as needed
        self.declare_parameter('home_deg', [95.0, 0.0, -122.0, 0.0, -60.0, -20.0])   # 1
        self.declare_parameter('take_deg', [151.0, 10.0, -122.0, 0.0, -65.0, -50.0])   # 2
        self.declare_parameter('give_deg', [151.0, -7.0, -126.0, 0.0,  -55.0, -50.0])   # 3
        self.declare_parameter('give_2_deg', [151.0, 10.0, -122.0, 0.0,  -65.0, -50.0])   # 4
        self.declare_parameter('give_3_deg', [90.0, 0.0, -120.0, 0.0,  30.0, -20.0])   # 5
        self.declare_parameter('rest_deg', [95.0, 0.0, -122.0, 0.0, -60.0, -20.0])   # 6

        # Gripper behavior (strings published to /command_gripper)
        self.declare_parameter('after_take_gripper_cmd', 'close')  # open|close|none
        self.declare_parameter('after_give_gripper_cmd', 'open')   # open|close|none
        self.declare_parameter('gripper_pause_sec', 0.6)

        # Mode trigger
        self.declare_parameter('trigger_mode', 'gummy_bear')

        # ---------- Read params ----------
        self.srv_name = str(self.get_parameter('service_name').value)
        self.mode_srv_name = str(self.get_parameter('app_mode_service').value)
        self.js_topic = str(self.get_parameter('joint_states_topic').value)

        self.speed = float(self.get_parameter('speed').value)
        self.acc = float(self.get_parameter('acceleration').value)
        self.safe = bool(self.get_parameter('enable_safety').value)

        self.home = list(self.get_parameter('home_deg').value)
        self.take = list(self.get_parameter('take_deg').value)
        self.give = list(self.get_parameter('give_deg').value)
        self.give_2 = list(self.get_parameter('give_2_deg').value)
        self.give_3 = list(self.get_parameter('give_3_deg').value)
        self.rest = list(self.get_parameter('rest_deg').value)

        self.grip_after_take = str(self.get_parameter('after_take_gripper_cmd').value)
        self.grip_after_give = str(self.get_parameter('after_give_gripper_cmd').value)
        self.grip_pause = float(self.get_parameter('gripper_pause_sec').value)

        self.trigger_mode = str(self.get_parameter('trigger_mode').value).lower()

        # ---------- Interfaces ----------
        self.move_cli = self.create_client(MoveJoints, self.srv_name)
        self.get_logger().info(f'Waiting for service {self.srv_name} …')
        self.move_cli.wait_for_service()

        self.mode_cli = self.create_client(GetAppMode, self.mode_srv_name)

        self.grip_pub = self.create_publisher(String, 'command_gripper', 10)
        self.create_subscription(JointState, self.js_topic, self._on_js_deg, 10)

        # ---------- State machine ----------
        self.last_deg: Optional[List[float]] = None
        self._mode: Optional[str] = None
        self._mode_future = None
        self._last_mode_req = 0.0
        self._mode_req_period = 0.3

        self._armed = False
        self._running = False
        self._step = 0
        self._grip_timer = None

        self.timer = self.create_timer(0.05, self._tick)

        self.get_logger().info('GummyBear ready. Will start when app mode = "gummy_bear".')

    # --------- Callbacks / polling ----------
    def _on_js_deg(self, msg: JointState):
        if len(msg.position) >= 6:
            self.last_deg = [float(p) for p in msg.position[:6]]

    def _request_mode_if_needed(self):
        now = time.monotonic()
        if self._mode_future is not None:
            return
        if not self.mode_cli.wait_for_service(timeout_sec=0.0):
            return
        if now - self._last_mode_req < self._mode_req_period:
            return
        self._last_mode_req = now
        req = GetAppMode.Request()
        self._mode_future = self.mode_cli.call_async(req)

        def _done(fut):
            try:
                resp = fut.result()
                prev = self._mode
                self._mode = (resp.mode or '').strip().lower()
                if self._mode != prev:
                    self.get_logger().info(f'app mode -> "{self._mode}"')
                if prev != self.trigger_mode and self._mode == self.trigger_mode and not self._running:
                    self._armed = True
            except Exception as e:
                self.get_logger().warn(f'mode query failed: {e}')
            finally:
                self._mode_future = None

        self._mode_future.add_done_callback(_done)

    # --------- Primitives ----------
    def _send_move(self, joints_deg: List[float], speed: float, acc: float):
        req = MoveJoints.Request()
        req.speed = float(speed)
        req.acceleration = float(acc)
        req.enable_safety = self.safe
        req.target_joint = [float(x) for x in joints_deg]  # degrees
        self.get_logger().info(f'MOVE step {self._step}: { [round(v,1) for v in joints_deg] }')
        fut = self.move_cli.call_async(req)

        def _done(f):
            try:
                resp = f.result()
                if not resp.success:
                    self.get_logger().error(f'move failed: {resp.message}')
                    self._running = False
                    self._armed = False
                    return
                self._step += 1
                self._progress_sequence()
            except Exception as e:
                self.get_logger().error(f'move raised: {e}')
                self._running = False
                self._armed = False

        fut.add_done_callback(_done)

    def _grip_and_after(self, cmd: str, after_fn):
        """Publish gripper cmd, then continue after a short pause."""
        if cmd and cmd != 'none':
            self.get_logger().info(f'GRIPPER -> "{cmd}"')
            self.grip_pub.publish(String(data=cmd))
        # non-blocking wait
        def _after():
            try:
                if self._grip_timer:
                    self._grip_timer.cancel()
            except Exception:
                pass
            after_fn()
        self._grip_timer = self.create_timer(self.grip_pause, _after)

    def _grip_now(self, cmd: str):
        if cmd and cmd != 'none':
            self.get_logger().info(f'GRIPPER -> "{cmd}"')
            self.grip_pub.publish(String(data=cmd))

    def _pause_then(self, seconds, after_fn):
        self.get_logger().info(f'Waiting {seconds}s…')
        def _go():
            try: self._pause_timer.cancel()
            except Exception: pass
            after_fn()
        self._pause_timer = self.create_timer(seconds, _go)

    # --------- Sequence ----------
    def _progress_sequence(self):
        if self._step == 0:
            # HOME
            self._send_move(self.home, self.speed, self.acc)

        elif self._step == 1:
            # OPEN first (so it's open while descending), then go to TAKE
            self._grip_now('open')
            self._send_move(self.take, self.speed, self.acc)

        elif self._step == 2:
            # At TAKE: CLOSE, then continue (keeps closed until the end)
        
            # self._grip_and_after(self.grip_after_take,  # should be 'close'
            #                    after_fn=lambda: self._advance_after_grip())
            self._send_move(self.give, self.speed, self.acc)

        elif self._step == 3:
            # GIVE
            
            self._grip_and_after(self.grip_after_take,  # should be 'close'
                                after_fn=lambda: self._advance_after_grip())

        elif self._step == 4:
            # GIVE_2 
            self._send_move(self.give_2, self.speed, self.acc)

        elif self._step == 5:
            # GIVE_3 
            self._send_move(self.give_3, self.speed, self.acc)

        elif self._step == 6:
            # Release at the end
            self._pause_then(2.0, after_fn=lambda: self._grip_and_after(self.grip_after_give,  # should be 'open'
                                after_fn=lambda: self._advance_after_grip()))

        elif self._step == 7:
            # REST
            self._pause_then(2.0, after_fn=lambda: self._send_move(self.rest, self.speed, self.acc))

        else:
            self.get_logger().info('GummyBear sequence completed.')
            self._running = False
            self._armed = False

    def _advance_after_grip(self):
        self._step += 1
        self._progress_sequence()

    # --------- Main tick ----------
    def _tick(self):
        self._request_mode_if_needed()
        if self._armed and not self._running:
            self._running = True
            self._step = 0
            self.get_logger().info('Starting GummyBear sequence')
            self._progress_sequence()


def main(args=None):
    rclpy.init(args=args)
    node = LARA_Gummy_Bear()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()