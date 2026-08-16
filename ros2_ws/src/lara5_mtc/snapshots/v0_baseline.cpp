/*********************************************************************
 * Lara5 chess cylinder pick-and-place with MoveIt Task Constructor.
 *
 * MTC Pick/Place task for chess_scene cylinder collision objects (piece_<square>).
 * Gripper may touch board_sq_* collision boxes (needed for place IK); piece+gripper touch before pick.
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
#include <geometry_msgs/msg/twist_stamped.hpp>
#include <moveit/task_constructor/container.h>
#include <moveit/task_constructor/solvers.h>
#include <moveit/task_constructor/stages.h>
#include <moveit/task_constructor/stages/generate_grasp_pose.h>
#include <moveit/task_constructor/stages/generate_place_pose.h>
#include <moveit/task_constructor/stages/pick.h>
#include <moveit/task_constructor/stages/simple_grasp.h>
#include <moveit/task_constructor/task.h>
#include <moveit_msgs/msg/move_it_error_codes.hpp>
#include <rclcpp/rclcpp.hpp>
#include <tf2/LinearMath/Quaternion.h>
#include <tf2_eigen/tf2_eigen.hpp>
#include <tf2_geometry_msgs/tf2_geometry_msgs.hpp>

#include "lara5_mtc/chess_occupancy.hpp"

namespace mtc = moveit::task_constructor;

static const rclcpp::Logger LOGGER = rclcpp::get_logger("lara5_mtc_chess_cylinders_pick_place");

namespace
{

constexpr const char* kArmGroup = "arm";
constexpr const char* kGripperGroup = "gripper";
constexpr const char* kEefName = "lerobot_gripper";
constexpr const char* kEefLink = "lara5_gripper";
constexpr const char* kWorldFrame = "world";
constexpr const char* kHomePose = "stand";
constexpr const char* kGripperOpen = "open";
constexpr const char* kGripperClose = "close";

// Top-down tool orientation: tool Z toward world -Z (perpendicular to board).
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

geometry_msgs::msg::PoseStamped makeTopDownIkFrame(const double piece_height,
                                                   const std::string& piece_type,
                                                   const double grasp_clearance_m)
{
  // Match lara5_chess_mtc_pick_place.py — virtual grasp frame above cylinder top.
  const double z_offset = piece_type == "pawn" ? piece_height / 2.0 + grasp_clearance_m : 0.03;

  geometry_msgs::msg::PoseStamped ik_frame;
  ik_frame.header.frame_id = kEefLink;
  ik_frame.pose.orientation = eulerToQuaternion(kTopDownRoll, kTopDownPitch, kTopDownYaw);
  ik_frame.pose.position.z = z_offset;
  return ik_frame;
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
makeAllowGripperBoardCollisions(const moveit::core::RobotModelConstPtr& model)
{
  auto stage = std::make_unique<mtc::stages::ModifyPlanningScene>("allow gripper on board squares");
  const auto links = gripperCollisionLinks(model);
  for (const char file : { 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h' })
  {
    for (const char rank : { '1', '2', '3', '4', '5', '6', '7', '8' })
    {
      const std::string object_id = std::string("board_sq_") + file + rank;
      stage->allowCollisions(object_id, true);
      stage->allowCollisions(object_id, links, true);
    }
  }
  return stage;
}

std::unique_ptr<mtc::stages::ModifyPlanningScene>
makeAllowGripperAllPieceCollisions(const moveit::core::RobotModelConstPtr& model)
{
  auto stage = std::make_unique<mtc::stages::ModifyPlanningScene>("allow gripper on all pieces");
  const auto links = gripperCollisionLinks(model);
  for (const char file : { 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h' })
  {
    for (const char rank : { '1', '2', '3', '4', '5', '6', '7', '8' })
    {
      const std::string object_id = lara5_mtc::pieceObjectId(std::string(1, file) + rank);
      stage->allowCollisions(object_id, true);
      stage->allowCollisions(object_id, links, true);
    }
  }
  return stage;
}

std::unique_ptr<mtc::stages::ModifyPlanningScene>
makeAllowArmOtherPieceCollisions(const std::string& source_square,
                                 const moveit::core::RobotModelConstPtr& model)
{
  // Allow arm vs every piece on the board except the picked piece. Occupancy JSON may
  // only list move endpoints (e.g. e2_to_e4.json); chess_scene still has all 32 cylinders.
  auto stage = std::make_unique<mtc::stages::ModifyPlanningScene>("allow arm on other pieces");
  const auto arm_links = model->getJointModelGroup(kArmGroup)->getLinkModelNamesWithCollisionGeometry();
  const std::string source = source_square;
  for (const char file : { 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h' })
  {
    for (const char rank : { '1', '2', '3', '4', '5', '6', '7', '8' })
    {
      const std::string square = std::string(1, file) + rank;
      if (square == source)
      {
        continue;
      }
      stage->allowCollisions(lara5_mtc::pieceObjectId(square), arm_links, true);
    }
  }
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
  node->declare_parameter<std::string>("chess_seed_pose", "pre_pick");
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

  const std::string seed_pose = [&]() {
    if (const std::string env = envOrEmpty("CHESS_SEED_POSE"); !env.empty())
    {
      return env;
    }
    return node->get_parameter("chess_seed_pose").as_string();
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
                "pick_hover_z=%.3f  place_hover_z=%.3f  seed=%s",
                move.source.c_str(), move.target.c_str(), move.piece_type.c_str(), move.piece_diameter,
                move.piece_height, move.object_id.c_str(), pick_hover_z, place_hover_z, seed_pose.c_str());

    mtc::Task task;
    task.stages()->setName("lara5_mtc_chess_cylinders_pick_place");
    task.loadRobotModel(node);

    task.setProperty("group", kArmGroup);
    task.setProperty("eef", kEefName);
    task.setProperty("ik_frame", kEefLink);

    const auto joint_planner = std::make_shared<mtc::solvers::JointInterpolationPlanner>();
    auto pipeline_planner = std::make_shared<mtc::solvers::PipelinePlanner>(node, "ompl");

    auto cartesian_planner = std::make_shared<mtc::solvers::CartesianPath>();
    cartesian_planner->setMaxVelocityScalingFactor(1.0);
    cartesian_planner->setMaxAccelerationScalingFactor(1.0);
    cartesian_planner->setStepSize(0.01);

    const mtc::solvers::PlannerInterfacePtr arm_planner = pipeline_planner;
    const auto top_down_orientation = eulerToQuaternion(kTopDownRoll, kTopDownPitch, kTopDownYaw);

    const geometry_msgs::msg::PoseStamped top_down_ik_frame =
        makeTopDownIkFrame(move.piece_height, move.piece_type, grasp_clearance_m);

    // --- Current state ---
    {
      auto current = std::make_unique<mtc::stages::CurrentState>("current state");
      current->properties().set("timeout", planning_scene_timeout_s);
      task.add(std::move(current));
    }

    task.add(makeAllowGripperBoardCollisions(task.getRobotModel()));
    task.add(makeAllowGripperAllPieceCollisions(task.getRobotModel()));
    task.add(makeAllowArmOtherPieceCollisions(move.source, task.getRobotModel()));

    // --- Open gripper ---
    {
      auto stage = std::make_unique<mtc::stages::MoveTo>("open gripper", joint_planner);
      stage->setGroup(kGripperGroup);
      stage->setGoal(kGripperOpen);
      task.add(std::move(stage));
    }

    // --- Seed arm ---
    mtc::Stage* seed_stage = nullptr;
    {
      const std::string seed_stage_name = "seed " + seed_pose;
      auto stage = std::make_unique<mtc::stages::MoveTo>(seed_stage_name, joint_planner);
      stage->setGroup(kArmGroup);
      stage->setGoal(seed_pose);
      seed_stage = stage.get();
      task.add(std::move(stage));
    }

    // Allow gripper vs picked piece before connect (matches Python task order).
    task.add(makeAllowPieceCollisions("allow collision (gripper,piece)", move.object_id,
                                      task.getRobotModel()));

    // --- Connect to pick hover ---
    {
      mtc::stages::Connect::GroupPlannerVector planners = {
        { kArmGroup, arm_planner },
        { kGripperGroup, joint_planner },
      };
      auto connect = std::make_unique<mtc::stages::Connect>("connect to pick", planners);
      connect->setTimeout(10.0);
      connect->properties().configureInitFrom(mtc::Stage::PARENT);
      task.add(std::move(connect));
    }

    mtc::Stage* grasp_monitor = nullptr;
    {
      auto pick_pose = std::make_unique<mtc::stages::GenerateGraspPose>("generate pick pose");
      pick_pose->setMonitoredStage(seed_stage);
      pick_pose->setEndEffector(kEefName);
      pick_pose->setObject(move.object_id);
      pick_pose->setPreGraspPose(kGripperOpen);
      pick_pose->setGraspPose(kGripperClose);
      pick_pose->setRotationAxis(Eigen::Vector3d::UnitZ());
      pick_pose->setAngleDelta(move.piece_type == "pawn" ? 2.0 * M_PI : M_PI / 6.0);

      auto simple_grasp = std::make_unique<mtc::stages::SimpleGrasp>(std::move(pick_pose), "grasp");
      simple_grasp->setIKFrame(top_down_ik_frame);
      simple_grasp->setMaxIKSolutions(1);

      auto pick = std::make_unique<mtc::stages::Pick>(std::move(simple_grasp), "pick piece");
      pick->setEndEffector(kEefName);
      pick->properties().set("object", move.object_id);
      pick->properties().configureInitFrom(mtc::Stage::PARENT, { "group" });

      // Connect may end near the grasp pose; keep min small so Cartesian approach can finish.
      const double approach_min = move.piece_type == "pawn" ? 0.005 : 0.03;
      const double approach_max = move.piece_type == "pawn" ? 0.12 : approach_m;
      geometry_msgs::msg::TwistStamped approach;
      approach.header.frame_id = kWorldFrame;
      approach.twist.linear.z = -1.0;
      pick->setApproachMotion(approach, approach_min, approach_max);

      geometry_msgs::msg::TwistStamped lift;
      lift.header.frame_id = kWorldFrame;
      lift.twist.linear.z = 1.0;
      pick->setLiftMotion(lift, 0.02, std::max(lift_m, 0.12));

      grasp_monitor = pick.get();
      task.add(std::move(pick));
    }

    {
      mtc::stages::Connect::GroupPlannerVector planners = {
        { kArmGroup, arm_planner },
        { kGripperGroup, joint_planner },
      };
      auto connect = std::make_unique<mtc::stages::Connect>("connect to place", planners);
      connect->setTimeout(10.0);
      connect->properties().configureInitFrom(mtc::Stage::PARENT);
      task.add(std::move(connect));
    }

    {
      const double object_place_z = target_pose.z + move.piece_height / 2.0;
      const geometry_msgs::msg::PoseStamped object_place_pose =
          makeWorldPose(target_pose.x, target_pose.y, object_place_z, top_down_orientation);

      auto place_generator = std::make_unique<mtc::stages::GeneratePlacePose>("generate place pose");
      place_generator->setMonitoredStage(grasp_monitor);
      place_generator->setObject(move.object_id);
      place_generator->setPose(object_place_pose);
      // SimpleUnGrasp reads gripper goals from the generator (inverse of pick).
      place_generator->properties().set("pregrasp", kGripperClose);
      place_generator->properties().set("grasp", kGripperOpen);

      auto ungrasp = std::make_unique<mtc::stages::SimpleUnGrasp>(std::move(place_generator), "ungrasp");
      ungrasp->setIKFrame(top_down_ik_frame);
      auto place = std::make_unique<mtc::stages::Place>(std::move(ungrasp), "place piece");
      place->setEndEffector(kEefName);
      place->properties().set("object", move.object_id);
      place->properties().set("eef_frame", kEefLink);
      place->properties().configureInitFrom(mtc::Stage::PARENT, { "group" });

      geometry_msgs::msg::TwistStamped place_motion;
      place_motion.header.frame_id = kEefLink;
      place_motion.twist.linear.z = -1.0;
      place->setPlaceMotion(place_motion, place_descent_m * 0.8, place_descent_m);

      geometry_msgs::msg::TwistStamped retract_motion;
      retract_motion.header.frame_id = kWorldFrame;
      retract_motion.twist.linear.z = 1.0;
      place->setRetractMotion(retract_motion, 0.02, 0.05);
      task.add(std::move(place));
    }

    {
      auto stage = std::make_unique<mtc::stages::MoveTo>("move to stand", joint_planner);
      stage->properties().configureInitFrom(mtc::Stage::PARENT, { "group" });
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
      task.publishAllSolutions(false);

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
        RCLCPP_INFO(LOGGER, "Execution succeeded — watch motion in RViz");
      }
      else if (!auto_execute)
      {
        RCLCPP_INFO(LOGGER,
                    "auto_execute is false — re-run with auto_execute:=true to move the arm, "
                    "or use run_mtc_cpp_cylinder_test.sh for headless validation");
      }
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
