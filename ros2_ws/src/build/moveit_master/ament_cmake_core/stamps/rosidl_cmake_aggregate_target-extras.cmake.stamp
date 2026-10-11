# generated from rosidl_cmake/cmake/rosidl_cmake_aggregate_target-extras.cmake.in

# Create a convenience aggregate target moveit_master::moveit_master
# that links all generated interface targets, so downstream packages can use
# a single modern CMake target name instead of ${moveit_master_TARGETS}.
if(moveit_master_TARGETS AND NOT TARGET moveit_master::moveit_master)
  add_library(moveit_master::moveit_master INTERFACE IMPORTED)
  set_target_properties(moveit_master::moveit_master PROPERTIES
    INTERFACE_LINK_LIBRARIES "${moveit_master_TARGETS}")
endif()
