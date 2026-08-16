import rclpy
from rclpy.node import Node
from lara_interfaces.srv import GetTCPPose
from geometry_msgs.msg import Pose, Point, Quaternion
from lara_ros.neurapy.robot import Robot
from scipy.spatial.transform import Rotation as R

class TCPService(Node):
    def __init__(self):
        super().__init__('tcp_service')
        self.srv = self.create_service(GetTCPPose, 'get_tcp_pose', self.get_pose_callback)
        self.robot = Robot()
        self.robot.init_program()

    def get_pose_callback(self, request, response):
        tcp = self.robot.get_tcp_pose()
        self.get_logger().info(f"TCP raw: {tcp}")

        x, y, z, roll, pitch, yaw = tcp
        pos = Point(x=x, y=y, z=z)

        r = R.from_euler('xyz', [roll, pitch, yaw])
        qx, qy, qz, qw = r.as_quat()

        # force cast to plain float
        qx, qy, qz, qw = float(qx), float(qy), float(qz), float(qw)

        # debug log helps confirm
        self.get_logger().info(f"Quaternion: {qx}, {qy}, {qz}, {qw}")

        quat = Quaternion(x=qx, y=qy, z=qz, w=qw)
        pose = Pose(position=pos, orientation=quat)
        response.pose = pose
        return response


def main(args=None):
    rclpy.init(args=args)
    node = TCPService()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
