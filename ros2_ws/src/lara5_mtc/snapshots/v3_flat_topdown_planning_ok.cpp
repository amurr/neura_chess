/*********************************************************************
 * Lara5 chess cylinder pick-and-place with MoveIt Task Constructor.
 *
 * Flat MTC tree: top-down hover poses + Cartesian approach/lift/descend.
 * Minimal collision allows (picked piece + source/target board squares).
 *
 * Run:
 *   ros2 launch xyz_motion chess_scene.launch.py use_cylinder_collision:=true
 *   ros2 launch lara5_moveit_config mtc_demo_headless.launch.py
 *   ros2 launch lara5_mtc mtc_chess_cylinders_pick_place.launch.py
 *********************************************************************/

#include <cmath>
#include <cstdlib>
#include <memory>
#include <sstream>
#include <string>
#include <thread>
#include <vector>

#include <geometry_msgs/msg/pose_stamped.hpp>
#include <geometry_msgs/msg/vector3_stamped.hpp>
#include <moveit/task_constructor/container.h>
#include <moveit/task_constructor/solvers.h>
#include <moveit/task_constructor/stages.h>
#include <moveit/task_constructor/stages/move_relative.h>
#include <moveit/task_constructor/task.h>
#include <moveit_msgs/msg/move_it_error_codes.hpp>
#include <rclcpp/rclcpp.hpp>
#include <tf2/LinearMath/Quaternion.h>
#include <tf2_geometry_msgs/tf2_geometry_msgs.hpp>

#include "lara5_mtc/chess_occupancy.hpp"

namespace mtc = moveit::task_constructor;

static const rclcpp::Logger LOGGER = rclcpp::get_logger("lara5_mtc_chess_cylinders_pick_place");

namespace
{

constexpr const char* kArmGroup = "arm";
constexpr const char* kGripperGroup = "gripper";
constexpr const char* kEefLink = "lara5_gripper";
constexpr const char* kWorldFrame = "world";
constexpr const char* kHomePose = "stand";
constexpr const char* kGripperOpen = "open";
constexpr const char* kGripperClose = "close";

// Top-down: EEF +Z toward world -Z (perpendicular to board). Tune if jaw axis differs.
constexpr double kTopDownRoll = 0.0;
constexpr double kTopDownPitch = M_PI_2;
constexpr double kTopDownYaw = 0.0;

std::string envOrEmpty(const char* name)
{
  if (const char* value = std::getenv(name))
  {
    return std::string(value);
  }
  return {};
}

geometry_msgs::msg::Quaternion eulerToQuaternion(const double roll, const double pitch, const double yaw)
{
  tf2::Quaternion q;
  q.setRPY(roll, pitch, yaw);
  return tf2::toMsg(q);
}

geometry_msgs::msg::PoseStamped makeWorldPose(const double x,
                                              const double y,
                                              const double z,
                                              const geometry_msgs::msg::Quaternion& orientation)
{
  geometry_msgs::msg::PoseStamped pose;
  pose.header.frame_id = kWorldFrame;
  pose.pose.position.x = x;
  pose.pose.position.y = y;
  pose.pose.position.z = z;
  pose.pose.orientation = orientation;
  return pose;
}

std::vector<std::string> gripperCollisionLinks(const moveit::core::RobotModelConstPtr& model)
{
  return model->getJointModelGroup(kGripperGroup)->getLinkModelNamesWithCollisionGeometry();
}

std::unique_ptr<mtc::stages::ModifyPlanningScene>
makeAllowPieceCollisions(const std::string& name,
                         const std::string& object_id,
                         const moveit::core::RobotModelConstPtr& model)
{
  auto stage = std::make_unique<mtc::stages::ModifyPlanningScene>(name);
  stage->allowCollisions(object_id, gripperCollisionLinks(model), true);
  return stage;
}

std::unique_ptr<mtc::stages::ModifyPlanningScene>
makeAllowGripperBoardSquare(const std::string& square,
                            const moveit::core::RobotModelConstPtr& model)
{
  auto stage = std::make_unique<mtc::stages::ModifyPlanningScene>("allow gripper on board_sq_" + square);
  const auto links = gripperCollisionLinks(model);
  const std::string object_id = "board_sq_" + square;
  stage->allowCollisions(object_id, true);
  stage->allowCollisions(object_id, links, true);
  return stage;
}

void addMoveArmToWorldPose(mtc::Task& task,
                           const std::string& name,
                           const mtc::solvers::PlannerInterfacePtr& planner,
                           const geometry_msgs::msg::PoseStamped& target)
{
  auto stage = std::make_unique<mtc::stages::MoveTo>(name, planner);
  stage->setGroup(kArmGroup);
  stage->setGoal(target);
  task.add(std::move(stage));
}

std::unique_ptr<mtc::stages::ModifyPlanningScene>
makeAllowReleaseCollisions(const std::string& object_id,
                           const std::string& target_square,
                           const moveit::core::RobotModelConstPtr& model)
{
  auto stage = std::make_unique<mtc::stages::ModifyPlanningScene>("allow release collisions");
  const std::string board_id = "board_sq_" + target_square;
  const auto gripper_links = gripperCollisionLinks(model);
  stage->allowCollisions(object_id, true);
  stage->allowCollisions(object_id, board_id, true);
  stage->allowCollisions(object_id, gripper_links, true);
  stage->allowCollisions(board_id, gripper_links, true);
  return stage;
}

std::unique_ptr<mtc::stages::MoveRelative>
makeWorldZMove(const std::string& name,
               const mtc::solvers::PlannerInterfacePtr& planner,
               const double distance_m,
               const double axis_sign,
               const mtc::PropagatingEitherWay::Direction propagation)
{
  auto stage = std::make_unique<mtc::stages::MoveRelative>(name, planner);
  stage->properties().configureInitFrom(mtc::Stage::PARENT, { "group" });
  stage->setIKFrame(kEefLink);
  stage->setMinMaxDistance(std::min(0.005, distance_m * 0.1), distance_m);

  geometry_msgs::msg::Vector3Stamped direction;
  direction.header.frame_id = kWorldFrame;
  direction.vector.z = axis_sign;
  stage->setDirection(direction);
  stage->restrictDirection(propagation);
  return stage;
}

}  // namespace

int main(int argc, char** argv)
{
  rclcpp::init(argc, argv);
  auto node = rclcpp::Node::make_shared("lara5_mtc_chess_cylinders_pick_place");
  std::thread spinner([node] { rclcpp::spin(node); });

  node->declare_parameter<std::string>("chess_source_square", "e2");
  node->declare_parameter<std::string>("chess_target_square", "e4");
  node->declare_parameter<std::string>("chess_occupancy_file", "");
  node->declare_parameter<double>("chess_square_size_m", 0.04);
  node->declare_parameter<double>("chess_grasp_clearance_m", 0.015);
  node->declare_parameter<double>("chess_approach_m", 0.08);
  node->declare_parameter<double>("chess_lift_m", 0.08);
  node->declare_parameter<double>("chess_place_descent_m", 0.04);
  node->declare_parameter<double>("planning_scene_timeout_s", 30.0);
  node->declare_parameter<bool>("auto_execute", false);

  const std::string occupancy_path = [&]() {
    if (const std::string env = envOrEmpty("CHESS_OCCUPANCY_FILE"); !env.empty())
    {
      return env;
    }
    if (node->has_parameter("chess_occupancy_file"))
    {
      const auto value = node->get_parameter("chess_occupancy_file").as_string();
      if (!value.empty())
      {
        return value;
      }
    }
    return lara5_mtc::defaultOccupancyPath();
  }();

  const std::string source_override = [&]() {
    if (const std::string env = envOrEmpty("CHESS_SOURCE"); !env.empty())
    {
      return env;
    }
    return node->get_parameter("chess_source_square").as_string();
  }();

  const std::string target_override = [&]() {
    if (const std::string env = envOrEmpty("CHESS_TARGET"); !env.empty())
    {
      return env;
    }
    return node->get_parameter("chess_target_square").as_string();
  }();

  const double square_size_m = node->get_parameter("chess_square_size_m").as_double();
  const double approach_m = node->get_parameter("chess_approach_m").as_double();
  const double lift_m = node->get_parameter("chess_lift_m").as_double();
  const double place_descent_m = node->get_parameter("chess_place_descent_m").as_double();
  const double grasp_clearance_m = [&]() {
    if (const std::string env = envOrEmpty("CHESS_GRASP_CLEARANCE_M"); !env.empty())
    {
      return std::stod(env);
    }
    return node->get_parameter("chess_grasp_clearance_m").as_double();
  }();
  const double planning_scene_timeout_s = node->get_parameter("planning_scene_timeout_s").as_double();
  const bool auto_execute = [&]() {
    if (const std::string env = envOrEmpty("AUTO_EXECUTE"); !env.empty())
    {
      return env == "1" || env == "true" || env == "yes";
    }
    return node->get_parameter("auto_execute").as_bool();
  }();

  nlohmann::json occupancy;
  try
  {
    occupancy = lara5_mtc::loadOccupancyFile(occupancy_path);
  }
  catch (const std::exception& e)
  {
    RCLCPP_ERROR(LOGGER, "Failed to load occupancy: %s", e.what());
    rclcpp::shutdown();
    spinner.join();
    return 1;
  }

  lara5_mtc::ChessMove move;
  try
  {
    move = lara5_mtc::resolveChessMove(occupancy, source_override, target_override);
    const auto source_pose = lara5_mtc::inferSquarePose(occupancy, move.source, move.source, square_size_m);
    const auto target_pose = lara5_mtc::inferSquarePose(occupancy, move.target, move.source, square_size_m);

    const double pick_hover_z = source_pose.z + move.piece_height + approach_m + grasp_clearance_m;
    const double place_hover_z = target_pose.z + move.piece_height + place_descent_m;

    RCLCPP_INFO(LOGGER,
                "Move %s -> %s  type=%s  cylinder(d=%.3f, h=%.3f)  object=%s  "
                "pick_hover_z=%.3f  place_hover_z=%.3f",
                move.source.c_str(), move.target.c_str(), move.piece_type.c_str(), move.piece_diameter,
                move.piece_height, move.object_id.c_str(), pick_hover_z, place_hover_z);

    mtc::Task task;
    task.stages()->setName("lara5_mtc_chess_cylinders_pick_place");
    task.loadRobotModel(node);

    task.setProperty("group", kArmGroup);
    task.setProperty("eef", kEefLink);

    const auto joint_planner = std::make_shared<mtc::solvers::JointInterpolationPlanner>();
    auto pipeline_planner = std::make_shared<mtc::solvers::PipelinePlanner>(node, "ompl");
    auto cartesian_planner = std::make_shared<mtc::solvers::CartesianPath>();
    cartesian_planner->setMaxVelocityScalingFactor(1.0);
    cartesian_planner->setMaxAccelerationScalingFactor(1.0);
    cartesian_planner->setStepSize(0.005);
    cartesian_planner->setMinFraction(0.35);

    const mtc::solvers::PlannerInterfacePtr arm_planner = pipeline_planner;
    const auto top_down_orientation = eulerToQuaternion(kTopDownRoll, kTopDownPitch, kTopDownYaw);

    const geometry_msgs::msg::PoseStamped pick_hover_pose =
        makeWorldPose(source_pose.x, source_pose.y, pick_hover_z, top_down_orientation);
    const geometry_msgs::msg::PoseStamped place_hover_pose =
        makeWorldPose(target_pose.x, target_pose.y, place_hover_z, top_down_orientation);

    // --- Current state ---
    {
      auto current = std::make_unique<mtc::stages::CurrentState>("current state");
      current->properties().set("timeout", planning_scene_timeout_s);
      task.add(std::move(current));
    }

    // --- Open gripper ---
    {
      auto stage = std::make_unique<mtc::stages::MoveTo>("open gripper", joint_planner);
      stage->setGroup(kGripperGroup);
      stage->setGoal(kGripperOpen);
      task.add(std::move(stage));
    }

    // Minimal collision allows (piece + source/target board squares only).
    task.add(makeAllowPieceCollisions("allow collision (gripper,piece)", move.object_id,
                                      task.getRobotModel()));
    task.add(makeAllowGripperBoardSquare(move.source, task.getRobotModel()));
    task.add(makeAllowGripperBoardSquare(move.target, task.getRobotModel()));

    // --- Pick: top-down hover → descend → grasp ---
    addMoveArmToWorldPose(task, "pick hover", arm_planner, pick_hover_pose);
    task.add(makeWorldZMove("approach pick", cartesian_planner, approach_m, -1.0,
                            mtc::PropagatingEitherWay::FORWARD));

    {
      auto stage = std::make_unique<mtc::stages::MoveTo>("close gripper", joint_planner);
      stage->setGroup(kGripperGroup);
      stage->setGoal(kGripperClose);
      task.add(std::move(stage));
    }

    {
      auto attach = std::make_unique<mtc::stages::ModifyPlanningScene>("attach piece");
      attach->attachObject(move.object_id, kEefLink);
      task.add(std::move(attach));
    }

    task.add(makeWorldZMove("lift from pick", cartesian_planner, lift_m, 1.0,
                            mtc::PropagatingEitherWay::FORWARD));

    // --- Place: top-down hover → descend → release ---
    addMoveArmToWorldPose(task, "place hover", arm_planner, place_hover_pose);
    task.add(makeWorldZMove("descend place", cartesian_planner, place_descent_m, -1.0,
                            mtc::PropagatingEitherWay::FORWARD));

    task.add(makeAllowReleaseCollisions(move.object_id, move.target, task.getRobotModel()));

    {
      auto detach = std::make_unique<mtc::stages::ModifyPlanningScene>("detach piece");
      detach->detachObject(move.object_id, kEefLink);
      task.add(std::move(detach));
    }

    task.add(makeWorldZMove("retreat after place", cartesian_planner, place_descent_m + 0.02, 1.0,
                            mtc::PropagatingEitherWay::FORWARD));

    {
      auto stage = std::make_unique<mtc::stages::MoveTo>("open gripper after place", joint_planner);
      stage->setGroup(kGripperGroup);
      stage->setGoal(kGripperOpen);
      task.add(std::move(stage));
    }

    {
      auto stage = std::make_unique<mtc::stages::MoveTo>("move to stand", joint_planner);
      stage->setGroup(kArmGroup);
      stage->setGoal(kHomePose);
      stage->restrictDirection(mtc::PropagatingEitherWay::FORWARD);
      task.add(std::move(stage));
    }

    try
    {
      task.init();
    }
    catch (const mtc::InitStageException& e)
    {
      RCLCPP_ERROR_STREAM(LOGGER, "Task initialization failed: " << e);
      rclcpp::shutdown();
      spinner.join();
      return 1;
    }

    if (task.plan(1))
    {
      RCLCPP_INFO(LOGGER, "Planning succeeded (%zu solution)", task.numSolutions());
      if (task.numSolutions() > 0)
      {
        task.introspection().publishSolution(*task.solutions().front());
      }

      if (auto_execute && task.numSolutions() > 0)
      {
        const auto result = task.execute(*task.solutions().front());
        if (result.val != moveit_msgs::msg::MoveItErrorCodes::SUCCESS)
        {
          RCLCPP_ERROR(LOGGER, "Execution failed (error code %d)", result.val);
          rclcpp::shutdown();
          spinner.join();
          return 1;
        }
        RCLCPP_INFO(LOGGER, "Execution succeeded");
      }
      else
      {
        RCLCPP_INFO(LOGGER, "Plan OK (auto_execute=false)");
      }
      rclcpp::shutdown();
    }
    else
    {
      RCLCPP_ERROR(LOGGER,
                   "Planning failed — ensure chess_scene (cylinders) is running and piece %s is in the scene",
                   move.object_id.c_str());
      std::ostringstream oss;
      task.explainFailure(oss);
      RCLCPP_ERROR_STREAM(LOGGER, oss.str());
      rclcpp::shutdown();
      spinner.join();
      return 1;
    }
  }
  catch (const std::exception& e)
  {
    RCLCPP_ERROR(LOGGER, "Error: %s", e.what());
    rclcpp::shutdown();
    spinner.join();
    return 1;
  }

  spinner.join();
  return 0;
}
