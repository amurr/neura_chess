import math
import time
from typing import List, Optional

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64
from lara_interfaces.srv import MoveJoints, GetAppMode


class LARADance(Node):
    def __init__(self):
        super().__init__('lara_dance')

        # --- params ---
        self.declare_parameter('service_name', 'move_joints')
        self.declare_parameter('app_mode_service', 'get_app_mode')    # <— service to query app mode
        self.declare_parameter('joint_states_topic', '/lara/joint_states_deg')  # degrees
        self.declare_parameter('frequency_hz', 0.5)          # semantic; timing via speed/acc
        self.declare_parameter('amplitude_deg', [15.0, 14.0, -22.0, 0.0, 22.0, -10.0])   # per-joint amplitudes (deg)
        self.declare_parameter('phase_deg', [45.0, 0.0, 45.0, 0.0, 90.0, 0.0])       # per-joint phase offsets (deg)

        # Defaults; we auto-scale speed/acc each send using effective frequency
        self.declare_parameter('speed', 20.0)
        self.declare_parameter('acceleration', 15.0)

        self.declare_parameter('enable_safety', True)
        self.declare_parameter('steps_per_cycle', 14)
        self.declare_parameter('ramp_time_sec', 1.0)
        self.declare_parameter('lock_base_on_first', True)
        self.declare_parameter('return_to_base_on_exit', True)
        # 'cycles' counts TRIOS (each trio = 3 cycles). 0 = endless.
        self.declare_parameter('cycles', 0)

        # autoscaling bounds
        self.declare_parameter('freq_min', 0.2)
        self.declare_parameter('freq_max', 3.0)
        self.declare_parameter('speed_min', 10.0)
        self.declare_parameter('speed_max', 100.0)
        self.declare_parameter('acc_min', 5.0)
        self.declare_parameter('acc_max', 150.0)

        # param values
        self.srv_name = str(self.get_parameter('service_name').value)
        self.mode_srv_name = str(self.get_parameter('app_mode_service').value)
        self.js_topic = str(self.get_parameter('joint_states_topic').value)
        self.freq_param = float(self.get_parameter('frequency_hz').value)  # keep param copy
        self.amp: List[float] = list(self.get_parameter('amplitude_deg').value)
        self.phase: List[float] = list(self.get_parameter('phase_deg').value)
        self.safe = bool(self.get_parameter('enable_safety').value)
        self.steps = int(self.get_parameter('steps_per_cycle').value)
        self.ramp_time = float(self.get_parameter('ramp_time_sec').value)
        self.lock_base_on_first = bool(self.get_parameter('lock_base_on_first').value)
        self.return_to_base = bool(self.get_parameter('return_to_base_on_exit').value)
        self.trios = int(self.get_parameter('cycles').value)

        self.freq_min = float(self.get_parameter('freq_min').value)
        self.freq_max = float(self.get_parameter('freq_max').value)
        self.speed_min = float(self.get_parameter('speed_min').value)
        self.speed_max = float(self.get_parameter('speed_max').value)
        self.acc_min = float(self.get_parameter('acc_min').value)
        self.acc_max = float(self.get_parameter('acc_max').value)

        if len(self.amp) != 6 or len(self.phase) != 6:
            raise ValueError('amplitude_deg and phase_deg must each contain 6 numbers')

        # --- dynamic inputs ---
        self.freq_override: Optional[float] = None  # from /lara/music_frequency_hz (beats/sec)

        # --- service clients ---
        self.cli = self.create_client(MoveJoints, self.srv_name)
        self.get_logger().info(f'Waiting for service {self.srv_name}')
        self.cli.wait_for_service()

        # App mode service client (non-blocking polling)
        self.mode_cli = self.create_client(GetAppMode, self.mode_srv_name)
        self._mode: Optional[str] = None
        self._mode_future = None
        self._mode_req_interval = 0.5   # seconds between requests
        self._mode_last_req = 0.0

        # --- subscriptions ---
        self.last_deg: Optional[List[float]] = None
        self.base_deg: Optional[List[float]] = None
        self._printed_wait = False
        self.create_subscription(JointState, self.js_topic, self._on_js_deg, 10)
        self.create_subscription(Float64, '/lara/music_frequency_hz', self._on_music_freq, 10)

        # --- timing / trio counting ---
        self._start_time = time.monotonic()
        self._trio_idx = 0
        self._finished = False
        self._busy = False
        self._next_wait_log = 0.0

        # periodic check to launch next trio
        self.timer = self.create_timer(0.1, self._tick)

        s, a = self._compute_speed_acc(self._effective_freq())
        self.get_logger().info(
            f'Dance ready | topic={self.js_topic} steps_per_cycle={self.steps} '
            f'freq_eff={self._effective_freq():.3f}Hz -> auto speed~{s:.1f} acc~{a:.1f} '
            f'ramp={self.ramp_time}s lock_base_on_first={self.lock_base_on_first} '
            f'trios={self.trios} (each trio=3 cycles). Will run only when app mode is "dance" (service: {self.mode_srv_name}).'
        )

    # --- helpers ---
    def _effective_freq(self) -> float:
        """Use topic override if available; else param."""
        return float(self.freq_override) if self.freq_override is not None else float(self.freq_param)

    @staticmethod
    def _clamp(x: float, lo: float, hi: float) -> float:
        return max(lo, min(hi, x))

    def _map(self, f: float, f_lo: float, f_hi: float, y_lo: float, y_hi: float) -> float:
        if f_hi <= f_lo:
            return y_lo
        t = (f - f_lo) / (f_hi - f_lo)
        t = self._clamp(t, 0.0, 1.0)
        return y_lo + t * (y_hi - y_lo)

    def _compute_speed_acc(self, freq_hz: float) -> (float, float):
        speed = self._map(freq_hz, self.freq_min, self.freq_max, self.speed_min, self.speed_max)
        acc = self._map(freq_hz, self.freq_min, self.freq_max, self.acc_min, self.acc_max)
        return (speed, acc)

    # --- app mode polling ---
    def _maybe_request_mode(self):
        now = time.monotonic()
        if self._mode_future is not None:
            return  # already pending
        if not self.mode_cli.wait_for_service(timeout_sec=0.0):
            # service not available; log sparsely
            if now >= self._next_wait_log:
                self.get_logger().debug(f'Waiting for mode service "{self.mode_srv_name}" …')
                self._next_wait_log = now + 5.0
            return
        if now - self._mode_last_req < self._mode_req_interval:
            return
        self._mode_last_req = now
        req = GetAppMode.Request()
        self._mode_future = self.mode_cli.call_async(req)

        def _done(fut):
            try:
                resp = fut.result()
                prev = self._mode
                self._mode = (resp.mode or '').lower().strip()
                if self._mode != prev:
                    self.get_logger().info(f'app mode -> "{self._mode}"')
                    if self._mode == 'dance':
                        # reset ramp when entering dance
                        self._start_time = time.monotonic()
            except Exception as e:
                self.get_logger().warn(f'mode query failed: {e}')
            finally:
                self._mode_future = None

        self._mode_future.add_done_callback(_done)

    # --- subscribers ---
    def _on_js_deg(self, msg: JointState):
        if len(msg.position) >= 6:
            self.last_deg = [float(p) for p in msg.position[:6]]
            if self.lock_base_on_first and self.base_deg is None:
                self.base_deg = list(self.last_deg)
                self.get_logger().info(f'Locked base to { [round(v,2) for v in self.base_deg] }')

    def _on_music_freq(self, msg: Float64):
        self.freq_override = float(msg.data)
        s, a = self._compute_speed_acc(self._effective_freq())
        #self.get_logger().info(f'freq override -> {self.freq_override:.3f} Hz | auto speed~{s:.1f} acc~{a:.1f}')

    # --- trajectory builders ---
    def _build_cycle_waypoints_deg(self, base: List[float], amp_scale: float) -> List[float]:
        """One full cycle, flattened (degrees). amp_scale in [0..1] for ramping."""
        traj_flat: List[float] = []
        phi = [math.radians(p) for p in self.phase]  # per-joint phase offsets
        for k in range(self.steps):
            theta = 2.0 * math.pi * (k / self.steps)  # 0..2π
            for i in range(6):
                delta = amp_scale * self.amp[i] * math.sin(theta + phi[i])
                traj_flat.append(base[i] + delta)
        return traj_flat

    def _build_trio_waypoints_deg(self, base: List[float], ramp: float) -> List[float]:
        """Three cycles back-to-back: ramped, then two full-amplitude cycles."""
        traj = []
        traj += self._build_cycle_waypoints_deg(base, amp_scale=ramp)
        traj += self._build_cycle_waypoints_deg(base, amp_scale=1.0)
        traj += self._build_cycle_waypoints_deg(base, amp_scale=1.0)
        return traj

    # --- main loop ---
    def _tick(self):
        if self._finished or self._busy:
            return

        # poll/refresh app mode via service
        self._maybe_request_mode()

        # Must be in dance mode to send
        if (self._mode or '') != 'dance':
            now = time.monotonic()
            if now >= self._next_wait_log:
                self.get_logger().debug('Waiting for app mode "dance"…')
                self._next_wait_log = now + 5.0
            return

        # Need at least one joint state
        if self.last_deg is None:
            if not self._printed_wait:
                self.get_logger().info(f'Waiting for {self.js_topic} …')
                self._printed_wait = True
            return

        # Determine base pose
        if not self.lock_base_on_first:
            self.base_deg = list(self.last_deg)
        if self.base_deg is None:
            self.base_deg = list(self.last_deg)

        # Ramp (soft start) for the first cycle in this trio
        ramp = min(1.0, (time.monotonic() - self._start_time) / max(1e-3, self.ramp_time))

        # Build three full cycles of waypoints (degrees), flattened
        traj_deg_flat = self._build_trio_waypoints_deg(self.base_deg, ramp)

        # Auto-scale speed/acc from *effective* frequency
        freq_eff = self._effective_freq()
        speed, acc = self._compute_speed_acc(freq_eff)

        # Send the trio in one request
        req = MoveJoints.Request()
        req.speed = speed
        req.acceleration = acc
        req.enable_safety = self.safe
        req.target_joint = traj_deg_flat

        self.get_logger().info(
            f'sending TRIO #{self._trio_idx+1} '
            f'(3 x {self.steps} waypoints; first={ [round(v,2) for v in traj_deg_flat[:6]] }) '
            f'freq_eff={freq_eff:.3f}Hz auto speed={speed:.1f} acc={acc:.1f}'
        )

        self._busy = True
        fut = self.cli.call_async(req)

        def _done_cb(f):
            try:
                resp = f.result()
                if not resp.success:
                    self.get_logger().error(f'move failed: {resp.message}')
                else:
                    self._trio_idx += 1
                    self.get_logger().info(f'TRIO {self._trio_idx} finished')
            except Exception as e:
                self.get_logger().error(f'move raised: {e}')
            finally:
                self._busy = False
                # If still in dance mode, reset ramp start for next trio’s fade-in
                if (self._mode or '') == 'dance':
                    self._start_time = time.monotonic()
                if self.trios > 0 and self._trio_idx >= self.trios:
                    self._finish()

        fut.add_done_callback(_done_cb)

    def _finish(self):
        if getattr(self, "_finished", False):
            return
        self._finished = True
        self.get_logger().info('Requested trios reached — stopping dance.')
        try:
            self.timer.cancel()
        except Exception:
            pass
        # Optionally return to base
        if self.return_to_base and self.base_deg is not None:
            req = MoveJoints.Request()
            ret_speed, ret_acc = self._compute_speed_acc(max(self.freq_min, 0.3))
            req.speed = ret_speed
            req.acceleration = ret_acc
            req.enable_safety = self.safe
            req.target_joint = list(self.base_deg)
            self.cli.call_async(req)
        self.destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = LARADance()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        rclpy.shutdown()


if __name__ == '__main__':
    main()
