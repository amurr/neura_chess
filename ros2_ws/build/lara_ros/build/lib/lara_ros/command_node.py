# src/lara_ros/lara_ros/command_node.py
import sys
import threading
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from lara_ros.neurapy.robot import Robot
from lara_interfaces.srv import GetAppMode, MoveJoints   # <-- add MoveJoints
from rcl_interfaces.msg import Log

try:
    from prompt_toolkit import PromptSession
except Exception:
    PromptSession = None

HELP = """Commands:
  init
  stop
  pause
  resume
  mode <manual|auto>      # robot control mode (internal)
  dance                   # set application mode to "dance"
  chill                   # set application mode to "chill"
  toast                   # set application mode to "toast"
  getmode                 # print current application mode
  home                    # move to predefined home position
  gummy_bear              # pick gummy bear package from predefined position and hand it
  help
  exit
  packing                 # move into packing position
Type here or publish to /lara_cmd as std_msgs/msg/String
"""

class CommandNode(Node):
    def __init__(self):
        super().__init__('lara_command')

        # Relay only gummy_bear logs into this terminal:
        #self.create_subscription(Log, '/rosout', self._rosout_cb, 50)

        self.subscription = self.create_subscription(String, 'lara_cmd', self.cmd_cb, 10)

        self.r = Robot()
        self.robot_mode = 'manual'
        self.app_mode = 'chill'

        self.mode_srv = self.create_service(GetAppMode, 'get_app_mode', self._get_app_mode_cb)

        # create client for MoveJoints
        self.move_cli = self.create_client(MoveJoints, '/move_joints')
        while not self.move_cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn('Waiting for /move_joints service...')

        self._lock = threading.Lock()
        self.session = PromptSession("> ") if PromptSession else None

        self.get_logger().info('Command node ready')
        self.get_logger().info(HELP)
        self._start_input_thread()

    def _rosout_cb(self, msg: Log):
        # logger name equals Node name by default; you used 'gummy_bear'
        if msg.name == 'gummy_bear':
            # echo gummy logs into this terminal
            self.get_logger().info(f'[gummy_bear] {msg.msg}')

    def _get_app_mode_cb(self, request, response):
        response.mode = self.app_mode
        return response

    def _start_input_thread(self):
        t = threading.Thread(target=self._input_loop, daemon=True)
        t.start()

    def _input_loop(self):
        if self.session:
            while rclpy.ok():
                try:
                    line = self.session.prompt("> ")
                except (EOFError, KeyboardInterrupt):
                    self.get_logger().info('Shutting down on input close')
                    rclpy.shutdown()
                    break
                cmd = line.strip()
                if cmd:
                    self._execute(cmd)
        else:
            for line in sys.stdin:
                cmd = line.strip()
                if cmd:
                    self._execute(cmd)
            self.get_logger().info('Shutting down on input close')
            rclpy.shutdown()

    def cmd_cb(self, msg: String):
        self._execute(msg.data.strip())

    def _execute(self, cmd: str):
        with self._lock:
            try:
                if not cmd:
                    return
                self.get_logger().info(f'cmd: {cmd}')
                parts = cmd.split()
                c = parts[0].lower()

                if c == 'help':
                    self.get_logger().info('\n' + HELP)
                    return

                if c == 'init':
                    self.r.init_program()
                    self.get_logger().info('Program initialized')
                    return

                if c == 'stop':
                    self.r.stop()
                    self.get_logger().warn('Stopped. Run init before next motion')
                    return

                if c == 'pause':
                    self.r.pause()
                    self.get_logger().info('Paused')
                    return

                if c == 'resume':
                    self.r.unpause()
                    self.get_logger().info('Resumed')
                    return

                if c == 'mode' and len(parts) == 2:
                    m = parts[1].lower()
                    if m in ('manual', 'auto'):
                        self.robot_mode = m
                        self.get_logger().info(f'Robot mode set to {self.robot_mode}')
                    else:
                        self.get_logger().warn('Mode must be manual or auto')
                    return

                if c == 'dance':
                    self.app_mode = 'dance'
                    self.get_logger().info('Application mode set to "dance"')
                    return

                if c == 'chill':
                    self.app_mode = 'chill'
                    self.get_logger().info('Application mode set to "chill"')
                    return

                if c == 'toast':
                    self.app_mode = 'toast'
                    self.get_logger().info('Application mode set to "toast"')
                    return
                
                if c == 'gummy_bear':
                    self.app_mode = 'gummy_bear'
                    self.get_logger().info('Application mode set to "gummy_bear"')
                    return

                if c == 'getmode':
                    self.get_logger().info(f'Current application mode: {self.app_mode}')
                    return

                if c == 'home':
                    req = MoveJoints.Request()
                    req.speed = 100.0
                    req.acceleration = 50.0
                    req.enable_safety = True
                    req.target_joint = [90.0, 0.0, -120.0, 0.0, 30.0, -20.0]
                    future = self.move_cli.call_async(req)

                    def _done_cb(f):
                        try:
                            res = f.result()
                            self.get_logger().info(f'Moved to home: success={res.success}')
                        except Exception as e:
                            self.get_logger().error(f'Home command failed: {e}')

                    future.add_done_callback(_done_cb)
                    return

                if c == 'packing':
                    req = MoveJoints.Request()
                    req.speed = 100.0
                    req.acceleration = 50.0
                    req.enable_safety = True
                    req.target_joint = [100.0, 0.0, -140.0, 0.0, 30.0, -10.0]
                    future = self.move_cli.call_async(req)

                    def _done_cb(f):
                        try:
                            res = f.result()
                            self.get_logger().info(f'Moved to home: success={res.success}')
                        except Exception as e:
                            self.get_logger().error(f'Home command failed: {e}')

                    future.add_done_callback(_done_cb)
                    return

                if c in ('exit', 'quit', 'shutdown'):
                    self.get_logger().info('Shutting down on user request')
                    rclpy.shutdown()
                    return

                self.get_logger().warn('Unknown command. Type help')

            except Exception as e:
                self.get_logger().error(f'Command failed: {e}')

def main():
    rclpy.init()
    node = CommandNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
