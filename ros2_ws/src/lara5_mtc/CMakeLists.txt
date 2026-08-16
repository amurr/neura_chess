cmake_minimum_required(VERSION 3.22)
project(lara5_mtc)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(ament_cmake REQUIRED)
find_package(ament_index_cpp REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(moveit_common REQUIRED)
moveit_package()
find_package(moveit_core REQUIRED)
find_package(moveit_msgs REQUIRED)
find_package(moveit_task_constructor_core REQUIRED)
find_package(nlohmann_json REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_eigen REQUIRED)
find_package(tf2_geometry_msgs REQUIRED)
find_package(tf2_ros REQUIRED)

add_library(${PROJECT_NAME}_chess_occupancy SHARED
  src/chess_occupancy.cpp
)
target_include_directories(${PROJECT_NAME}_chess_occupancy
  PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
)
target_link_libraries(${PROJECT_NAME}_chess_occupancy
  PUBLIC
    nlohmann_json::nlohmann_json
    ament_index_cpp::ament_index_cpp
)

add_library(${PROJECT_NAME}_pick_place SHARED
  src/pick_place_task.cpp
)
target_include_directories(${PROJECT_NAME}_pick_place
  PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
)
target_link_libraries(${PROJECT_NAME}_pick_place
  PUBLIC
    ${PROJECT_NAME}_chess_occupancy
    ${moveit_task_constructor_core_TARGETS}
    ${moveit_core_TARGETS}
    rclcpp::rclcpp
    tf2_eigen::tf2_eigen
    tf2_geometry_msgs::tf2_geometry_msgs
)

add_executable(lara5_mtc_chess_cylinders_pick_place
  src/lara5_mtc_chess_cylinders_pick_place.cpp
)
target_include_directories(lara5_mtc_chess_cylinders_pick_place
  PRIVATE include
)
target_link_libraries(lara5_mtc_chess_cylinders_pick_place
  ${PROJECT_NAME}_chess_occupancy
  ${PROJECT_NAME}_pick_place
  ${moveit_task_constructor_core_TARGETS}
  rclcpp::rclcpp
  tf2_eigen::tf2_eigen
  tf2_geometry_msgs::tf2_geometry_msgs
)
ament_target_dependencies(lara5_mtc_chess_cylinders_pick_place moveit_msgs moveit_core tf2_ros tf2)

install(TARGETS
  ${PROJECT_NAME}_chess_occupancy
  ${PROJECT_NAME}_pick_place
  lara5_mtc_chess_cylinders_pick_place
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY include/
  DESTINATION include
)

install(DIRECTORY launch config arm_styles
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
