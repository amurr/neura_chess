# request — Cartesian path
# target_pose: flat list 6*k of [x,y,z,roll,pitch,yaw] (metres, radians)
#   absolute mode: world poses in base frame
#   relative mode: offsets applied per step (see use_relative)
float64[] target_pose
float64 speed              # m/s
float64 acceleration       # m/s^2
bool enable_safety
bool use_relative          # if true, each 6-tuple is a cartesian_offset (move_linear_relative)
string offset_frame        # "Base" or "Tool" (only when use_relative is true)
