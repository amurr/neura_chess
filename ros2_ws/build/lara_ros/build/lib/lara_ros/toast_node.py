import time
from typing import List, Optional

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from lara_interfaces.srv import MoveJoints, GetAppMode


class LARAToast(Node):
    def __init__(self):
        super().__init__('lara_toast')

        # --- parameters ---
        self.declare_parameter('service_name', 'move_joints')
        self.declare_parameter('app_mode_service', 'get_app_mode')
        self.declare_parameter('joint_states_topic', '/lara/joint_states_deg')

        # Motion settings
        self.declare_parameter('speed', 60.0)          # normal legs
        self.declare_parameter('acceleration', 30.0)
        self.declare_parameter('slow_speed', 5.0)     # P2 -> P3
        self.declare_parameter('slow_acceleration', 5.0)
        self.declare_parameter('return_speed', 60.0)   # P3 -> HOME
        self.declare_parameter('return_acceleration', 30.0)
        self.declare_parameter('enable_safety', True)
        self.declare_parameter('dwell_sec', 2.0)

        # Home pose
        self.declare_parameter('home_from_current', True)
        self.declare_parameter('home_deg', [0.0] * 6)

        # Trigger word
        self.declare_parameter('trigger_mode', 'toast')

        # --- hard-coded toast sequence points (degrees) ---
        self.p1 = [90.0, 0.0, -80.0, 0.0, -10.0, -20.0]
        self.p2 = [90.0, 15.0, -80.0, 0.0, -25.0, -20.0]
        self.p3 = [90.0, 10.0, -80.0, 0.0, -15.0, -20.0]

        # --- read params ---
        self.srv_name = str(self.get_parameter('service_name').value)
        self.mode_srv_name = str(self.get_parameter('app_mode_service').value)
        self.js_topic = str(self.get_parameter('joint_states_topic').value)

        self.speed = float(self.get_parameter('speed').value)
        self.acc = float(self.get_parameter('acceleration').value)
        self.slow_speed = float(self.get_parameter('slow_speed').value)
        self.slow_acc = float(self.get_parameter('slow_acceleration').value)
        self.ret_speed = float(self.get_parameter('return_speed').value)
        self.ret_acc = float(self.get_parameter('return_acceleration').value)
        self.safe = bool(self.get_parameter('enable_safety').value)
        self.dwell_sec = float(self.get_parameter('dwell_sec').value)

        self.home_from_current = bool(self.get_parameter('home_from_current').value)
        self.home_param = list(self.get_parameter('home_deg').value)
        self.trigger_mode = str(self.get_parameter('trigger_mode').value).lower()

        # --- service clients ---
        self.move_cli = self.create_client(MoveJoints, self.srv_name)
        self.get_logger().info(f'Waiting for service {self.srv_name}')
        self.move_cli.wait_for_service()

        self.mode_cli = self.create_client(GetAppMode, self.mode_srv_name)

        # --- joint state subscription (for capturing HOME if requested) ---
        self.last_deg: Optional[List[float]] = None
        self.create_subscription(JointState, self.js_topic, self._on_js_deg, 10)

        # --- state machine ---
        self._mode: Optional[str] = None
        self._mode_future = None
        self._last_mode_req = 0.0
        self._mode_req_period = 0.3

        self._armed = False
        self._running = False
        self._step = 0
        self._home: Optional[List[float]] = None
        self._dwell_timer = None

        self.timer = self.create_timer(0.05, self._tick)

        self.get_logger().info(
            f'Toast ready. Trigger mode="{self.trigger_mode}". '
            f'Using hard-coded points p1={self.p1}, p2={self.p2}, p3={self.p3}.'
        )

    def _on_js_deg(self, msg: JointState):
        if len(msg.position) >= 6:
            self.last_deg = [float(p) for p in msg.position[:6]]

    # ----- mode query -----
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

    # ----- move helpers -----
    def _send_move(self, joints_deg: List[float], speed: float, acc: float):
        req = MoveJoints.Request()
        req.speed = float(speed)
        req.acceleration = float(acc)
        req.enable_safety = self.safe
        req.target_joint = list(joints_deg)
        self.get_logger().info(
            f'MOVE step {self._step}: target={ [round(v,2) for v in joints_deg] } '
            f'speed={speed} acc={acc}'
        )
        fut = self.move_cli.call_async(req)

        def _done(f):
            try:
                resp = f.result()
                if not resp.success:
                    self.get_logger().error(f'move failed: {resp.message}')
                    self._running = False
                    self._armed = False
                    return
                if self._step == 2:
                    self.get_logger().info(f'Dwelling {self.dwell_sec:.1f}s at P3…')
                    self._dwell_timer = self.create_timer(self.dwell_sec, self._after_dwell_go_home)
                else:
                    self._step += 1
                    self._progress_sequence()
            except Exception as e:
                self.get_logger().error(f'move raised: {e}')
                self._running = False
                self._armed = False

        fut.add_done_callback(_done)

    def _after_dwell_go_home(self):
        try:
            if self._dwell_timer:
                self._dwell_timer.cancel()
        except Exception:
            pass
        self._dwell_timer = None
        self._step += 1
        self._progress_sequence()

    def _progress_sequence(self):
        if self._step == 0:
            self._send_move(self.p1, self.speed, self.acc)
        elif self._step == 1:
            self._send_move(self.p2, self.speed, self.acc)
        elif self._step == 2:
            self._send_move(self.p3, self.slow_speed, self.slow_acc)
        elif self._step == 3:
            home = self._home if self._home is not None else self.home_param
            self._send_move(home, self.ret_speed, self.ret_acc)
            self._step = 4
        else:
            self.get_logger().info('Toast sequence completed.')
            self._running = False
            self._armed = False

    def _tick(self):
        self._request_mode_if_needed()
        if self._armed and not self._running:
            if self.home_from_current:
                if self.last_deg is None:
                    return
                self._home = list(self.last_deg)
            else:
                self._home = list(self.home_param)
            self._running = True
            self._step = 0
            self.get_logger().info('Starting toast sequence')
            self._progress_sequence()


def main(args=None):
    rclpy.init(args=args)
    node = LARAToast()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
