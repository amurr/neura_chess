# generated from rosidl_cmake/cmake/rosidl_cmake_aggregate_target-extras.cmake.in

# Create a convenience aggregate target lara_interfaces::lara_interfaces
# that links all generated interface targets, so downstream packages can use
# a single modern CMake target name instead of ${lara_interfaces_TARGETS}.
if(lara_interfaces_TARGETS AND NOT TARGET lara_interfaces::lara_interfaces)
  add_library(lara_interfaces::lara_interfaces INTERFACE IMPORTED)
  set_target_properties(lara_interfaces::lara_interfaces PROPERTIES
    INTERFACE_LINK_LIBRARIES "${lara_interfaces_TARGETS}")
endif()
