#!/usr/bin/env python3
import collections
import numpy as np
import pyaudio
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64

class TempoNode(Node):
    def __init__(self):
        super().__init__('music_tempo_node')

        # --------- Config (tune here) ---------
        self.WINDOW_SEC = 6.0          # rolling analysis window
        self.MIN_BPM = 60.0
        self.MAX_BPM = 180.0
        self.SMOOTH_ALPHA = 0.8        # EMA smoothing for BPM output
        self.ANALYZE_EVERY_SEC = 0.2   # recompute tempo every X seconds

        # STFT / envelope params
        self.FRAME_SIZE = 2048         # analysis FFT size
        self.HOP_SIZE = 1024           # hop between frames (overlap=50%)
        self.BAND_LOW_HZ = 40.0        # ignore DC/very-low
        self.BAND_HIGH_HZ = 5000.0     # ignore very high
        self.ENVELOPE_SMOOTH = 0.3     # EMA smoothing for flux envelope (0..1)

        # --------- Audio setup ---------
        self.CHANNELS = 1
        self.FORMAT = pyaudio.paInt16

        self.p = pyaudio.PyAudio()

        # Choose input device (prefer Logitech/C920 if present)
        device_index = None
        for i in range(self.p.get_device_count()):
            info = self.p.get_device_info_by_index(i)
            name = info.get("name", "")
            if "C920" in name or "Logitech" in name:
                device_index = i
                self.get_logger().info(f"Using mic: [{i}] {name}")
                break
        if device_index is None:
            device_index = self.p.get_default_input_device_info()['index']
            self.get_logger().warn("Using default input device")

        self.RATE = int(self.p.get_device_info_by_index(device_index)["defaultSampleRate"])
        self.get_logger().info(f"Sample rate: {self.RATE} Hz")

        # Stream chunk = hop size for steady envelope rate; use a small internal buffer
        self.CHUNK = self.HOP_SIZE

        self.stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK,
            input_device_index=device_index,
        )

        # --------- Buffers ---------
        self.frame_buf = np.zeros(self.FRAME_SIZE, dtype=np.float32)
        self.frame_fill = 0
        self.hann = np.hanning(self.FRAME_SIZE).astype(np.float32)

        # Envelope (spectral flux) & timestamps
        self.env = collections.deque()   # onset envelope samples
        self.ts  = collections.deque()   # seconds timeline at envelope rate
        self.elapsed_sec = 0.0

        # State for spectral flux
        self.prev_mag = None
        self.env_ema = 0.0

        # Smoothed BPM
        self.bpm_smooth = None

        # Publishers
        self.pub_bps = self.create_publisher(Float64, '/lara/music_frequency_hz', 10)  # beats/sec
        self.pub_bpm = self.create_publisher(Float64, '/lara/music_bpm', 10)

        # Timers
        # Read audio at chunk cadence
        self.timer_audio = self.create_timer(self.CHUNK / self.RATE, self._read_chunk)
        # Analyze periodically
        self.timer_analyze = self.create_timer(self.ANALYZE_EVERY_SEC, self._analyze)

        self.get_logger().info("Tempo node running (spectral-flux + autocorr, 60–180 BPM)")

    # --------- Audio ingest -> STFT frames -> spectral flux envelope ---------
    def _read_chunk(self):
        try:
            raw = self.stream.read(self.CHUNK, exception_on_overflow=False)
            x = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0

            # Append to frame buffer
            need = self.FRAME_SIZE - self.frame_fill
            take = min(need, len(x))
            self.frame_buf[self.frame_fill:self.frame_fill+take] = x[:take]
            self.frame_fill += take

            # When a full frame is ready, process it, then roll by HOP_SIZE
            if self.frame_fill == self.FRAME_SIZE:
                frame = (self.frame_buf * self.hann)

                # FFT magnitude
                mag = np.abs(np.fft.rfft(frame))
                freqs = np.fft.rfftfreq(self.FRAME_SIZE, 1.0/self.RATE)

                # Band-limit
                band = (freqs >= self.BAND_LOW_HZ) & (freqs <= self.BAND_HIGH_HZ)
                mag = mag[band]

                # Spectral flux (rectified positive differences)
                if self.prev_mag is None:
                    flux = 0.0
                else:
                    diff = mag - self.prev_mag
                    flux = float(np.sum(np.maximum(diff, 0.0)))
                self.prev_mag = mag

                # Envelope smoothing (EMA) to reduce jitter
                self.env_ema = self.ENVELOPE_SMOOTH * self.env_ema + (1.0 - self.ENVELOPE_SMOOTH) * flux
                env_val = self.env_ema

                # Append envelope sample
                self.elapsed_sec += self.HOP_SIZE / self.RATE
                self.env.append(env_val)
                self.ts.append(self.elapsed_sec)

                # Keep only WINDOW_SEC seconds
                while self.ts and (self.elapsed_sec - self.ts[0] > self.WINDOW_SEC):
                    self.ts.popleft()
                    self.env.popleft()

                # Roll buffer by hop
                # Move last (FRAME_SIZE - HOP_SIZE) samples to start; fill tail with new zeros
                remain = self.FRAME_SIZE - self.HOP_SIZE
                self.frame_buf[:remain] = self.frame_buf[self.HOP_SIZE:]
                self.frame_fill = remain
        except Exception as e:
            self.get_logger().error(f"Audio read error: {e}")

    # --------- Tempo estimation (autocorr of onset envelope) ---------
    def _analyze(self):
        if len(self.env) < 8:
            return

        env = np.array(self.env, dtype=np.float32)

        # Normalize & lightly detrend
        env = env - np.median(env)
        std = env.std()
        if std > 1e-6:
            env = env / std

        # Half-wave rectify (keep onsets positive)
        env = np.maximum(env, 0.0)

        # Autocorrelation (positive lags only)
        ac = np.correlate(env, env, mode='full')
        ac = ac[len(ac)//2:]

        # Envelope sample rate (samples per second)
        if self.ts[-1] == self.ts[0]:
            return
        env_fs = len(env) / (self.ts[-1] - self.ts[0])

        # Convert BPM range to lag range (in envelope samples)
        min_period = 60.0 / self.MAX_BPM
        max_period = 60.0 / self.MIN_BPM
        min_lag = max(1, int(np.floor(min_period * env_fs)))
        max_lag = min(len(ac)-1, int(np.ceil(max_period * env_fs)))
        if max_lag <= min_lag + 1:
            return

        # Peak search in ROI (ignore the zero-lag)
        roi = ac[min_lag:max_lag+1]
        if roi.size < 3:
            return
        # optional small smoothing over ROI to reduce spurious spikes
        if roi.size >= 5:
            ker = np.array([1,2,3,2,1], dtype=np.float32)
            ker = ker / ker.sum()
            roi = np.convolve(roi, ker, mode='same')

        peak_lag = int(np.argmax(roi)) + min_lag

        # Convert lag -> BPM
        period_sec = peak_lag / env_fs
        bpm_primary = 60.0 / max(1e-6, period_sec)

        # Half/double-tempo disambiguation:
        # check energy at harmonics (0.5x, 1x, 2x) and pick the most plausible
        def autocorr_at_bpm(bpm):
            lag = int(round((60.0/bpm) * env_fs))
            if 0 <= lag < len(ac):
                return ac[lag]
            return -np.inf

        c1 = autocorr_at_bpm(bpm_primary)
        c2 = autocorr_at_bpm(bpm_primary * 2.0)
        c0 = autocorr_at_bpm(bpm_primary * 0.5)

        bpm_cands = []
        if self.MIN_BPM <= bpm_primary <= self.MAX_BPM:
            bpm_cands.append((c1, bpm_primary))
        if self.MIN_BPM <= bpm_primary*2.0 <= self.MAX_BPM:
            bpm_cands.append((c2, bpm_primary*2.0))
        if self.MIN_BPM <= bpm_primary*0.5 <= self.MAX_BPM:
            bpm_cands.append((c0, bpm_primary*0.5))

        if not bpm_cands:
            return
        bpm_est = max(bpm_cands, key=lambda t: t[0])[1]

        # Smooth BPM output
        if self.bpm_smooth is None:
            self.bpm_smooth = bpm_est
        else:
            a = self.SMOOTH_ALPHA
            self.bpm_smooth = a * self.bpm_smooth + (1 - a) * bpm_est

        bps = self.bpm_smooth / 60.0

        # Publish
        self.pub_bpm.publish(Float64(data=float(self.bpm_smooth)))
        self.pub_bps.publish(Float64(data=float(bps)))

        #self.get_logger().info(
        #    f"BPM ~ {self.bpm_smooth:6.1f} | BPS ~ {bps:4.2f} "
        #    f"(env_fs≈{env_fs:.1f} Hz, lag={peak_lag})"
        #)

    # --------- Cleanup ---------
    def destroy(self):
        try:
            self.stream.stop_stream(); self.stream.close()
        except Exception:
            pass
        try:
            self.p.terminate()
        except Exception:
            pass
        super().destroy_node()

def main():
    rclpy.init()
    node = TempoNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
