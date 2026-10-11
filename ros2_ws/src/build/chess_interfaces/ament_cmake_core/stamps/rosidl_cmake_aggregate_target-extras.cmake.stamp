# generated from rosidl_cmake/cmake/rosidl_cmake_aggregate_target-extras.cmake.in

# Create a convenience aggregate target chess_interfaces::chess_interfaces
# that links all generated interface targets, so downstream packages can use
# a single modern CMake target name instead of ${chess_interfaces_TARGETS}.
if(chess_interfaces_TARGETS AND NOT TARGET chess_interfaces::chess_interfaces)
  add_library(chess_interfaces::chess_interfaces INTERFACE IMPORTED)
  set_target_properties(chess_interfaces::chess_interfaces PROPERTIES
    INTERFACE_LINK_LIBRARIES "${chess_interfaces_TARGETS}")
endif()
