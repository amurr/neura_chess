#!/usr/bin/env python3
"""Simple Lara5 MTC demo: joint-space move with gripper open/close."""

import os
import time

from moveit.task_constructor import core, stages

import rclcpp

rclcpp.init()
node = rclcpp.Node('lara5_mtc_simple')

arm = 'arm'
gripper = 'gripper'
jointspace = core.JointInterpolationPlanner()


def move_gripper(name, goal):
    stage = stages.MoveTo(name, jointspace)
    stage.group = gripper
    stage.setGoal(goal)
    return stage


task = core.Task()
task.name = 'simple_move'
task.loadRobotModel(node)

task.add(stages.CurrentState('current state'))
task.add(move_gripper('open gripper', 'open'))

move = stages.MoveTo('moveTo mid_move', jointspace)
move.group = arm
move.setGoal('mid_move')
task.add(move)

task.add(move_gripper('close gripper', 'close'))
task.add(move_gripper('open gripper', 'open'))

move = stages.MoveTo('moveTo stand', jointspace)
move.group = arm
move.setGoal('stand')
task.add(move)

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
