cmake_minimum_required(VERSION 3.8)
project(lara5_description)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

# URDF at package root (urdf/) OR under copied Neura tree (lara5/urdf/) — install what exists
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/urdf")
  install(DIRECTORY urdf DESTINATION share/${PROJECT_NAME})
endif()

if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/lara5")
  install(DIRECTORY lara5 DESTINATION share/${PROJECT_NAME})
endif()

# Warn at configure time if SO-101 gripper meshes are missing (run scripts/setup_so101_gripper.sh)
set(SO101_MESH_DIR "${CMAKE_CURRENT_SOURCE_DIR}/lara5/meshes/so101")
if(EXISTS "${SO101_MESH_DIR}")
  foreach(_m moving_jaw_so101_v1.stl wrist_roll_follower_so101_v1.stl)
    if(NOT EXISTS "${SO101_MESH_DIR}/${_m}")
      message(WARNING "Missing SO-101 mesh: ${SO101_MESH_DIR}/${_m} — run scripts/setup_so101_gripper.sh")
    endif()
  endforeach()
endif()

ament_package()
