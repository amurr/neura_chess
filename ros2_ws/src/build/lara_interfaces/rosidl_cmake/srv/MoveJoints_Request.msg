# request
string point_name          # if set, move to teach pendant point by name (e.g. "GP7")
float64[] target_joint     # degrees, 6*k waypoints (ignored if point_name is set)
float64[] target_pose      # optional TCP [x,y,z,roll,pitch,yaw] m/rad — IK when target_joint empty
float64 speed
float64 acceleration
bool enable_safety
