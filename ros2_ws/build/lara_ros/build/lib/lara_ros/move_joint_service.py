import math
import rclpy
from rclpy.node import Node
from lara_interfaces.srv import MoveJoints
from lara_ros.neurapy.robot import Robot
from lara_ros.motion_prep import ensure_robot_ready

def _chunk6(seq):
    if len(seq) % 6 != 0:
        raise ValueError(f"target_joint length must be 6*k; got {len(seq)}")
    return [seq[i:i+6] for i in range(0, len(seq), 6)]

class MoveJointService(Node):
    def __init__(self):
        super().__init__('move_joint_service')
        self.srv = self.create_service(MoveJoints, 'move_joints', self.cb)
        self._robot = None
        self.get_logger().info('move_joints service ready (robot connects on first call)')

    def _get_robot(self):
        if self._robot is None:
            self._robot = Robot()
        return self._robot

    def cb(self, request, response):
        try:
            robot = self._get_robot()
            ensure_robot_ready(robot, self.get_logger())

            prop = {
                "speed": float(request.speed),
                "acceleration": float(request.acceleration),
                "enable_safety": bool(request.enable_safety),
                "enable_blending": True,
                "blocking": True,
            }

            pname = (request.point_name or "").strip()
            if pname:
                prop["target_joint"] = pname
                self.get_logger().info(
                    f"MoveJoints -> teach point {pname!r} "
                    f"speed={prop['speed']} acc={prop['acceleration']}"
                )
            elif len(request.target_pose) == 6:
                pose6 = [float(v) for v in request.target_pose]
                ref = [float(v) for v in robot.get_current_joint_angles()]
                joints_rad = robot.compute_inverse_kinematics(
                    target_pose=pose6,
                    reference_joint=ref,
                    representation="rpy",
                )
                waypoints_rad = [[float(v) for v in joints_rad]]
                prop["target_joint"] = waypoints_rad
                prop["enable_blending"] = False
                self.get_logger().info(
                    f"MoveJoints IK pose6={[round(v, 4) for v in pose6]} "
                    f"joints(deg)={[[round(math.degrees(v), 3) for v in w] for w in waypoints_rad]} "
                    f"speed={prop['speed']} acc={prop['acceleration']}"
                )
            else:
                joints_deg_flat = [float(v) for v in request.target_joint]
                if len(joints_deg_flat) % 6 != 0:
                    raise ValueError(
                        f"target_joint length must be 6*k; got {len(joints_deg_flat)}. "
                        "Restart bringup after colcon build (kill old move_joint_service)."
                    )
                waypoints_deg = _chunk6(joints_deg_flat)
                waypoints_rad = [[math.radians(v) for v in w] for w in waypoints_deg]
                prop["target_joint"] = waypoints_rad
                # Blending merges waypoints into one path (looks like a single line).
                prop["enable_blending"] = len(waypoints_rad) > 1
                self.get_logger().info(
                    f"MoveJoints waypoints(deg)="
                    f"{[[round(v, 3) for v in w] for w in waypoints_deg]} "
                    f"blend={prop['enable_blending']} "
                    f"speed={prop['speed']} acc={prop['acceleration']}"
                )

            robot.move_joint(**prop)

            response.success = True
            response.message = "motion completed"
        except Exception as e:
            response.success = False
            response.message = str(e)
            self.get_logger().error(f"move_joints failed: {e}")
        return response

def main(args=None):
    rclpy.init(args=args)
    node = MoveJointService()
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

if __name__ == '__main__':
    main()
