cmake_minimum_required(VERSION 3.8)
project(moveit_master)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_action REQUIRED)
find_package(moveit_ros_planning_interface REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)

# --- interfaces (msg + action) ---
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/MotionStep.msg"
  "action/ExecuteSequence.action"
  DEPENDENCIES geometry_msgs
)

# --- executable ---
add_executable(moveit_master src/moveit_master.cpp)
ament_target_dependencies(moveit_master
  rclcpp
  rclcpp_action
  moveit_ros_planning_interface
  geometry_msgs
)

# use the interfaces generated in this same package
rosidl_get_typesupport_target(cpp_typesupport_target ${PROJECT_NAME} "rosidl_typesupport_cpp")
target_link_libraries(moveit_master "${cpp_typesupport_target}")

install(TARGETS moveit_master DESTINATION lib/${PROJECT_NAME})

ament_export_dependencies(rosidl_default_runtime)
ament_package()