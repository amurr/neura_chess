cmake_minimum_required(VERSION 3.5)
project(lara_interfaces)

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(geometry_msgs REQUIRED)

# ensure the group is visible to rosidl checks
set(${PROJECT_NAME}_MEMBER_OF_GROUPS "rosidl_interface_packages")

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/XyzRpyGoal.msg"
  "srv/GetTCPPose.srv"
  "srv/MoveJoints.srv"
  "srv/MoveLinear.srv"
  "srv/GetAppMode.srv"
  "srv/ComputeIK.srv"
  DEPENDENCIES geometry_msgs
)

ament_export_dependencies(rosidl_default_runtime)
ament_package()
