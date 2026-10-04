# One step of a motion sequence executed by moveit_master.

uint8 ARM_POSE=0       # move arm EEF to `pose` (in the arm's pose reference frame, e.g. world)
uint8 ARM_NAMED=1      # move arm to SRDF named state `named_target` (e.g. "home")
uint8 GRIPPER_NAMED=2  # move gripper to SRDF named state `named_target` (e.g. "gripper_open")
uint8 WAIT=3           # pause for `duration` seconds

uint8 type
geometry_msgs/Pose pose
string named_target
float64 duration