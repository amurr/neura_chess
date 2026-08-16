import math
from typing import List

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseStamped, WrenchStamped, Point, Quaternion
from std_msgs.msg import Float64

from lara_ros.neurapy.robot import Robot
from scipy.spatial.transform import Rotation as R


class LARAOdomPublisher(Node):
    def __init__(self):
        super().__init__('lara_odom_publisher')

        # params
        self.declare_parameter('publish_rate_hz', 1.0)
        self.declare_parameter('frame_id', 'base_link')
        self.declare_parameter('joint_names', ['joint_1','joint_2','joint_3','joint_4','joint_5','joint_6'])

        rate_hz = float(self.get_parameter('publish_rate_hz').value)
        self.frame_id = str(self.get_parameter('frame_id').value)
        self.joint_names: List[str] = list(self.get_parameter('joint_names').value)

        self._robot = None

        # publishers
        self.pub_joint = self.create_publisher(JointState, '/lara/joint_states', 10)
        self.pub_joint_deg = self.create_publisher(JointState, '/lara/joint_states_deg', 10)
        self.pub_pose  = self.create_publisher(PoseStamped, '/lara/tcp_pose', 10)
        self.pub_speed = self.create_publisher(Float64, '/lara/tcp_speed', 10)
        self.pub_wrench = self.create_publisher(WrenchStamped, '/lara/tcp_wrench', 10)

        # timer
        period = 1.0 / max(1e-3, rate_hz)
        self.timer = self.create_timer(period, self._tick)
        self.get_logger().info(f'Publishing at {rate_hz} Hz with frame {self.frame_id}')

        # simple throttle for logs so the console is readable
        self._log_every_n = max(1, int(5.0 / period))  # about 5 s
        self._tick_count = 0

    def _get_robot(self):
        if self._robot is None:
            self._robot = Robot()
        return self._robot

    def _tick(self):
        self._tick_count += 1
        now = self.get_clock().now().to_msg()

        # joint state
        try:
            pos = [float(x) for x in self._get_robot().get_current_joint_angles()]  # radians
            js = JointState()
            js.header.stamp = now
            js.name = self.joint_names
            js.position = pos

            vel = None
            trq = None
            try:
                vel = [float(x) for x in self._get_robot().get_current_joint_velocities()]  # rad s
                js.velocity = vel
            except Exception:
                pass
            try:
                trq = [float(x) for x in self._get_robot().get_current_joint_torques()]
                js.effort = trq
            except Exception:
                pass

            self.pub_joint.publish(js)

            # degrees topic
            js_deg = JointState()
            js_deg.header.stamp = now
            js_deg.name = self.joint_names
            pos_deg = [math.degrees(p) for p in pos]
            js_deg.position = pos_deg
            if vel is not None:
                vel_deg = [math.degrees(v) for v in vel]
                js_deg.velocity = vel_deg
            # optional keep effort as is since units are not angular
            if trq is not None:
                js_deg.effort = trq

            self.pub_joint_deg.publish(js_deg)

            if self._tick_count % self._log_every_n == 0:
                self.get_logger().info(f'joint_states pos={pos}'
                                       + (f' vel={vel}' if vel is not None else '')
                                       + (f' eff={trq}' if trq is not None else ''))
                self.get_logger().info(f'joint_states_deg pos={pos_deg}'
                                       + (f' vel={vel_deg}' if vel is not None else ''))
        except Exception as e:
            self.get_logger().warn(f'JointState read failed: {e}')

        # tcp pose
        try:
            pose_msg = PoseStamped()
            pose_msg.header.stamp = now
            pose_msg.header.frame_id = self.frame_id

            try:
                # preferred quaternion from sdk [X, Y, Z, w, x, y, z]
                pq = self._get_robot().get_tcp_pose_quaternion()
                x, y, z = float(pq[0]), float(pq[1]), float(pq[2])
                qw, qx, qy, qz = float(pq[3]), float(pq[4]), float(pq[5]), float(pq[6])
                pose_msg.pose.position = Point(x=x, y=y, z=z)
                pose_msg.pose.orientation = Quaternion(x=qx, y=qy, z=qz, w=qw)
                log_pose = f'pos=({x:.6f},{y:.6f},{z:.6f}) quat=({qx:.6f},{qy:.6f},{qz:.6f},{qw:.6f})'
            except Exception:
                # fallback sdk returns [x, y, z, roll, pitch, yaw] radians
                tcp = [float(v) for v in self._get_robot().get_tcp_pose()]
                x, y, z, roll, pitch, yaw = tcp
                r = R.from_euler('xyz', [roll, pitch, yaw])
                qx, qy, qz, qw = [float(q) for q in r.as_quat()]
                pose_msg.pose.position = Point(x=x, y=y, z=z)
                pose_msg.pose.orientation = Quaternion(x=qx, y=qy, z=qz, w=qw)
                log_pose = (f'raw_tcp={tcp} '
                            f'pos=({x:.6f},{y:.6f},{z:.6f}) '
                            f'quat=({qx:.6f},{qy:.6f},{qz:.6f},{qw:.6f})')

            self.pub_pose.publish(pose_msg)
            if self._tick_count % self._log_every_n == 0:
                self.get_logger().info(f'tcp_pose {log_pose}')
        except Exception as e:
            self.get_logger().warn(f'TCP pose read failed: {e}')

        # tcp speed
        try:
            sp = float(self._get_robot().get_tcp_speed())
            self.pub_speed.publish(Float64(data=sp))
            if self._tick_count % self._log_every_n == 0:
                self.get_logger().info(f'tcp_speed {sp:.6f}')
        except Exception:
            pass

        # tcp wrench
        try:
            wr = [float(v) for v in self._get_robot().get_tcp_wrench()]  # [Fx,Fy,Fz,Mx,My,Mz]
            w = WrenchStamped()
            w.header.stamp = now
            w.header.frame_id = self.frame_id
            w.wrench.force.x, w.wrench.force.y, w.wrench.force.z = wr[0], wr[1], wr[2]
            w.wrench.torque.x, w.wrench.torque.y, w.wrench.torque.z = wr[3], wr[4], wr[5]
            self.pub_wrench.publish(w)
            if self._tick_count % self._log_every_n == 0:
                self.get_logger().info(f'tcp_wrench F=({wr[0]:.3f},{wr[1]:.3f},{wr[2]:.3f}) '
                                       f'M=({wr[3]:.3f},{wr[4]:.3f},{wr[5]:.3f})')
        except Exception:
            pass


def main(args=None):
    rclpy.init(args=args)
    node = LARAOdomPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down on Ctrl C')
    finally:
        try:
            if node._robot is not None and hasattr(node._robot, 'close'):
                node._robot.close()
        except Exception:
            pass
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
