#!/usr/bin/env python3
"""Cartesian MTC demo for Lara5 — small tool-frame moves after a known seed pose."""

from math import pi
import os
import time

from geometry_msgs.msg import Twist, TwistStamped, Vector3, Vector3Stamped
from moveit.task_constructor import core, stages
from std_msgs.msg import Header

import rclcpp

rclcpp.init()
node = rclcpp.Node('lara5_mtc_cartesian')

group = 'arm'
gripper = 'gripper'
eef_frame = 'lara5_gripper'
home_pose = 'stand'

cartesian = core.CartesianPath()
jointspace = core.JointInterpolationPlanner()


def move_gripper(name, goal):
    stage = stages.MoveTo(name, jointspace)
    stage.group = gripper
    stage.setGoal(goal)
    return stage


task = core.Task()
task.name = 'cartesian'
task.loadRobotModel(node)

task.add(stages.CurrentState('current state'))
task.add(move_gripper('open gripper', 'open'))

# Seed a collision-free configuration before Cartesian moves.
move = stages.MoveTo('moveTo mid_move', jointspace)
move.group = group
move.setGoal('mid_move')
task.add(move)

# Tool-frame moves (much more reliable than large world-frame steps for Lara5).
header = Header(frame_id=eef_frame)

move = stages.MoveRelative('z +5cm', cartesian)
move.group = group
move.setDirection(Vector3Stamped(header=header, vector=Vector3(x=0.0, y=0.0, z=0.05)))
task.add(move)

move = stages.MoveRelative('y -3cm', cartesian)
move.group = group
move.setDirection(Vector3Stamped(header=header, vector=Vector3(x=0.0, y=-0.03, z=0.0)))
task.add(move)

move = stages.MoveRelative('rz +15 deg', cartesian)
move.group = group
move.setDirection(
    TwistStamped(header=header, twist=Twist(angular=Vector3(x=0.0, y=0.0, z=pi / 12.0)))
)
task.add(move)

task.add(move_gripper('close gripper', 'close'))

move = stages.MoveTo(f'moveTo {home_pose}', jointspace)
move.group = group
move.setGoal(home_pose)
task.add(move)

task.add(move_gripper('open gripper', 'open'))

if task.plan():
    task.publish(task.solutions[0])
    print('Planning succeeded', flush=True)
    if os.environ.get('AUTO_EXECUTE', '').strip().lower() in ('1', 'true', 'yes'):
        result = task.execute(task.solutions[0])
        print(
            'Execution succeeded' if result.val == 1 else f'Execution failed ({result.val})',
            flush=True,
        )
else:
    print('Planning failed — check terminal for failing stage', flush=True)
time.sleep(100)
