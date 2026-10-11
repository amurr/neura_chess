Lara5 URDF (xacro chain)

  lara5.urdf.xacro
    includes lara5_macro.xacro (links, joints, gripper)
    adds world → lara5_root_link fixed joint

  lara5_macro.xacro
    includes:
      lara5_kinematic_parameters_nominal.xacro  DH / origins
      lara5_dynamic_parameters_nominal.xacro    masses / inertias
      lara5_limits.xacro                        joint limits
      so101_gripper.xacro                       jaw on link6

MoveIt does not load this folder directly. It loads
  lara5_moveit_config/config/lara5.urdf.xacro
which includes this package's lara5.urdf.xacro.

lara5.urdf is a flattened snapshot of the xacro (no ROS needed).
board_ik.py and the generate_*_goals.py scripts parse that file.

Regenerate the snapshot after xacro edits:

  xacro lara5.urdf.xacro > lara5.urdf
