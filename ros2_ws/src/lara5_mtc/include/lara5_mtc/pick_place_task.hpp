#pragma once

#include <string>

#include <geometry_msgs/msg/pose_stamped.hpp>
#include <moveit/task_constructor/task.h>
#include <rclcpp/rclcpp.hpp>

namespace lara5_mtc
{

struct PickPlaceRequest
{
  std::string object_id;
  std::string source_square;
  std::string target_square;
  std::string seed_pose{ "pre_pick" };
  std::string arm_group{ "arm" };
  std::string gripper_group{ "gripper" };
  std::string eef_link{ "lara5_gripper" };
  std::string world_frame{ "world" };
  std::string home_pose{ "stand" };
  std::string gripper_open{ "open" };
  std::string gripper_close{ "close" };
  geometry_msgs::msg::PoseStamped pick_grasp;
  geometry_msgs::msg::PoseStamped place_grasp;
  double approach_m{ 0.08 };
  double lift_m{ 0.08 };
  double planning_scene_timeout_s{ 30.0 };
  /// "eef" = MoveRelative along tool +Z (into the board). "world" = world ±Z.
  std::string approach_frame{ "eef" };
  /// "pose" = MoveTo TF hover pose (applies orientation). "cartesian" = XYZ delta from seed.
  std::string hover_mode{ "pose" };
};

geometry_msgs::msg::PoseStamped hoverFromGrasp(const geometry_msgs::msg::PoseStamped& grasp, double approach_m);

void populatePickPlaceTask(moveit::task_constructor::Task& task, const PickPlaceRequest& req,
                           const rclcpp::Node::SharedPtr& node);

}  // namespace lara5_mtc
