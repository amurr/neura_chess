import rclpy
from rclpy.node import Node
from lara_interfaces.srv import MoveLinear
from lara_ros.neurapy.robot import Robot
from lara_ros.motion_prep import ensure_robot_ready
from lara_ros.motion_util import offset_norm, tcp_pose_close


def _chunk6(seq):
    if len(seq) % 6 != 0:
        raise ValueError(f"target_pose length must be 6*k; got {len(seq)}")
    return [seq[i : i + 6] for i in range(0, len(seq), 6)]


class MoveLinearService(Node):
    def __init__(self):
        super().__init__("move_linear_service")
        self.srv = self.create_service(MoveLinear, "move_linear", self.cb)
        self._robot = None
        self.get_logger().info("move_linear service ready (robot connects on first call)")

    def _get_robot(self):
        if self._robot is None:
            self._robot = Robot()
        return self._robot

    def _run_absolute(self, robot, pose, speed, acc, enable_safety):
        tcp = [float(v) for v in robot.get_tcp_pose()]
        if tcp_pose_close(tcp, pose):
            self.get_logger().info("Skipping move_linear — already at target pose")
            return

        prop = {
            "target_pose": [pose],
            "speed": speed,
            "acceleration": acc,
            "enable_safety": enable_safety,
            "blending": False,
            "blocking": True,
        }
        robot.move_linear(**prop)

    def _run_relative(self, robot, offset, frame, speed, acc):
        if offset_norm(offset) < 1e-6:
            return
        prop = {
            "cartesian_offset": [float(v) for v in offset],
            "offset_frame": frame,
            "speed": speed,
            "acceleration": acc,
            "blocking": True,
        }
        robot.move_linear_relative(**prop)

    def cb(self, request, response):
        try:
            robot = self._get_robot()
            ensure_robot_ready(robot, self.get_logger())

            steps = _chunk6([float(v) for v in request.target_pose])
            if len(steps) < 1:
                raise ValueError("target_pose must contain at least one 6-value pose")

            speed = float(request.speed)
            acc = float(request.acceleration)
            enable_safety = bool(request.enable_safety)
            use_relative = bool(request.use_relative)
            frame = (request.offset_frame or "Base").strip() or "Base"
            if frame not in ("Base", "Tool"):
                raise ValueError(f'offset_frame must be "Base" or "Tool", got {frame!r}')

            mode = f"relative/{frame}" if use_relative else "absolute"
            self.get_logger().info(
                f"move_linear {len(steps)} step(s) mode={mode} speed={speed} m/s"
            )

            for step in steps:
                if use_relative:
                    self._run_relative(robot, step, frame, speed, acc)
                else:
                    self._run_absolute(robot, step, speed, acc, enable_safety)

            response.success = True
            response.message = "motion completed"
        except Exception as e:
            response.success = False
            response.message = str(e)
            self.get_logger().error(f"move_linear failed: {e}")
        return response


def main(args=None):
    rclpy.init(args=args)
    node = MoveLinearService()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        try:
            if node._robot is not None:
                node._robot.stop()
        except Exception:
            pass
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
