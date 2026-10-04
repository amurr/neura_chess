cmake_minimum_required(VERSION 3.8)
project(lara5_description)

find_package(ament_cmake REQUIRED)

install(DIRECTORY lara5 DESTINATION share/${PROJECT_NAME})

set(SO101_MESH_DIR "${CMAKE_CURRENT_SOURCE_DIR}/lara5/meshes/so101")
foreach(_m moving_jaw_so101_v1.stl wrist_roll_follower_so101_v1.stl)
  if(NOT EXISTS "${SO101_MESH_DIR}/${_m}")
    message(WARNING "Missing SO-101 mesh: ${SO101_MESH_DIR}/${_m}")
  endif()
endforeach()

ament_package()
