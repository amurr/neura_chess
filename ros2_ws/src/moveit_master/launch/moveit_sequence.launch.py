"""
it needs move_group node running with your config already loaded, exposing the action/services this interface talks to. That means launching your moveit_config's move_group.launch.py (which pulls in your robot_description, robot_description_semantic (SRDF), kinematics, joint limits, controllers, etc.) before or alongside this node.
"""