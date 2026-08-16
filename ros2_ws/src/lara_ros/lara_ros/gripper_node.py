import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import socket

class GripperClient(Node):
    def __init__(self):
        super().__init__("gripper_client")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(("192.168.2.13", 5000))  # Robot IP
        self.sub = self.create_subscription(String, "command_gripper", self.cb, 10)

    def cb(self, msg):
        cmd = msg.data.strip().lower()
        self.get_logger().info(f"[CLIENT] sending '{cmd}'")
        self.sock.sendall(cmd.encode())

def main():
    rclpy.init()
    node = GripperClient()
    rclpy.spin(node)
    node.sock.close()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()