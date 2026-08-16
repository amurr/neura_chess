/*********************************************************************
 * Lara5 chess cylinder pick-and-place with MoveIt Task Constructor.
 *
 * Flat MTC tree: seed → pick hover (world Δ) → approach → lift → slide to place.
 * Minimal collision allows (picked piece + source/target board squares).
 *
 * Run:
 *   ros2 launch xyz_motion chess_scene.launch.py use_cylinder_collision:=true
 *   ros2 launch lara5_moveit_config mtc_demo_headless.launch.py
 *   ros2 launch lara5_mtc mtc_chess_cylinders_pick_place.launch.py
 *********************************************************************/

#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdlib>
#include <filesystem>
#include <fstream>
#include <future>
#include <iomanip>
#include <memory>
#include <sstream>
#include <string>
#include <thread>
#include <vector>

#include <geometry_msgs/msg/pose_stamped.hpp>
#include <geometry_msgs/msg/vector3_stamped.hpp>
#include <moveit_msgs/msg/planning_scene_components.hpp>
#include <moveit_msgs/srv/get_planning_scene.hpp>
#include <moveit/task_constructor/container.h>
#include <moveit/task_constructor/solvers.h>
#include <moveit/task_constructor/stages.h>
#include <moveit/planning_scene/planning_scene.h>
#include <moveit/robot_state/robot_state.h>
#include <moveit/robot_trajectory/robot_trajectory.h>
#include <moveit/task_constructor/stages/move_relative.h>
#include <moveit/task_constructor/storage.h>
#include <moveit/task_constructor/task.h>
#include <moveit_msgs/msg/move_it_error_codes.hpp>
#include <nlohmann/json.hpp>
#include <rclcpp/rclcpp.hpp>
#include <tf2/LinearMath/Matrix3x3.h>
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
constexpr const char* kEefLink = "lara5_gripper";
constexpr const char* kWorldFrame = "world";
constexpr const char* kHomePose = "stand";
constexpr const char* kGripperOpen = "open";
constexpr const char* kGripperClose = "close";

// Default top-down RPY in world frame (EEF perpendicular to XY board, approach along world −Z).
// Override via chess_top_down_roll/pitch/yaw if the ghost arm still looks horizontal in RViz.
constexpr double kDefaultTopDownRoll = 0.0;
constexpr double kDefaultTopDownPitch = M_PI_2;
constexpr double kDefaultTopDownYaw = 0.0;

std::string envOrEmpty(const char* name)
{
  if (const char* value = std::getenv(name))
  {
    return std::string(value);
  }
  return {};
}

constexpr const char* kDefaultSuperbloomRepoMount =
    "/mnt/d/dev/superbloom/lara_superbloom-lucas-le_robot_gripper/lara_superbloom-lucas-le_robot_gripper";

std::string superbloomWorkspaceRoot()
{
  if (const std::string env = envOrEmpty("SUPERBLOOM_WS"); !env.empty())
  {
    return env;
  }
  if (const char* home = std::getenv("HOME"))
  {
    return std::string(home) + "/superbloom";
  }
  return std::filesystem::current_path().string();
}

std::string superbloomRepoRoot()
{
  if (const std::string env = envOrEmpty("SUPERBLOOM_REPO"); !env.empty())
  {
    return env;
  }
  const std::string mounted = std::string(kDefaultSuperbloomRepoMount);
  if (std::filesystem::is_directory(mounted + "/src/lara5_mtc"))
  {
    return mounted;
  }
  return superbloomWorkspaceRoot();
}

std::string defaultSolutionPreviewDir()
{
  return superbloomRepoRoot() + "/src/lara5_mtc/log";
}

std::string timestampForFilename()
{
  const auto now = std::chrono::system_clock::now();
  const std::time_t t = std::chrono::system_clock::to_time_t(now);
  std::tm tm_buf{};
  localtime_r(&t, &tm_buf);
  std::ostringstream oss;
  oss << std::put_time(&tm_buf, "%Y%m%d_%H%M%S");
  return oss.str();
}

std::string isoTimestamp()
{
  const auto now = std::chrono::system_clock::now();
  const std::time_t t = std::chrono::system_clock::to_time_t(now);
  std::tm tm_buf{};
  localtime_r(&t, &tm_buf);
  std::ostringstream oss;
  oss << std::put_time(&tm_buf, "%Y-%m-%dT%H:%M:%S");
  return oss.str();
}

struct SolutionPreviewPaths
{
  std::string archive_file;
  std::string latest_file;
};

SolutionPreviewPaths resolveSolutionPreviewPaths(const rclcpp::Node::SharedPtr& node,
                                                 const std::string& source_square,
                                                 const std::string& target_square)
{
  const std::string dir_param = node->get_parameter("solution_preview_dir").as_string();
  const std::string file_param = node->get_parameter("solution_preview_file").as_string();

  const std::string dir = [&]() {
    if (!dir_param.empty())
    {
      return dir_param;
    }
    if (!file_param.empty())
    {
      return std::filesystem::path(file_param).parent_path().string();
    }
    return defaultSolutionPreviewDir();
  }();

  std::filesystem::create_directories(dir);

  SolutionPreviewPaths paths;
  paths.latest_file = dir + "/solution_latest.json";
  if (file_param.empty())
  {
    paths.archive_file =
        dir + "/solution_" + source_square + "_to_" + target_square + '_' + timestampForFilename() + ".json";
  }
  else
  {
    paths.archive_file = file_param;
    const auto parent = std::filesystem::path(paths.archive_file).parent_path();
    if (!parent.empty())
    {
      std::filesystem::create_directories(parent);
    }
  }
  return paths;
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

geometry_msgs::msg::Quaternion orientationFromNamedState(const moveit::core::RobotModelConstPtr& model,
                                                           const std::string& named_state)
{
  moveit::core::RobotState state(model);
  state.setToDefaultValues();
  if (!named_state.empty())
  {
    state.setToDefaultValues(model->getJointModelGroup(kArmGroup), named_state);
  }
  return tf2::toMsg(state.getGlobalLinkTransform(kEefLink)).orientation;
}

geometry_msgs::msg::PoseStamped makeTopDownIkFrame()
{
  geometry_msgs::msg::PoseStamped ik_frame;
  ik_frame.header.frame_id = kEefLink;
  ik_frame.pose.orientation.w = 1.0;
  return ik_frame;
}

moveit::core::RobotState namedArmState(const moveit::core::RobotModelConstPtr& model, const std::string& named)
{
  moveit::core::RobotState state(model);
  state.setToDefaultValues();
  state.setToDefaultValues(model->getJointModelGroup(kArmGroup), named);
  state.update();
  return state;
}

bool solveIkForPose(const moveit::core::RobotModelConstPtr& model,
                    moveit::core::RobotState& state,
                    const geometry_msgs::msg::Pose& pose,
                    std::string* error = nullptr)
{
  const auto* jmg = model->getJointModelGroup(kArmGroup);
  if (!state.setFromIK(jmg, pose, kEefLink, 0.05))
  {
    if (error != nullptr)
    {
      *error = "setFromIK failed for " + std::string(kEefLink);
    }
    return false;
  }
  state.update();
  return true;
}

void addMoveArmToNamed(mtc::Task& task,
                       const std::string& name,
                       const mtc::solvers::PlannerInterfacePtr& planner,
                       const std::string& goal)
{
  auto stage = std::make_unique<mtc::stages::MoveTo>(name, planner);
  stage->setGroup(kArmGroup);
  stage->setGoal(goal);
  stage->restrictDirection(mtc::PropagatingEitherWay::FORWARD);
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

std::unique_ptr<mtc::stages::ModifyPlanningScene>
makeAllowArmOtherPieceCollisions(const std::string& source_square,
                                 const moveit::core::RobotModelConstPtr& model)
{
  auto stage = std::make_unique<mtc::stages::ModifyPlanningScene>("allow arm on other pieces");
  const auto arm_links = model->getJointModelGroup(kArmGroup)->getLinkModelNamesWithCollisionGeometry();
  for (const char file : { 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h' })
  {
    for (const char rank : { '1', '2', '3', '4', '5', '6', '7', '8' })
    {
      const std::string square = std::string(1, file) + rank;
      if (square == source_square)
      {
        continue;
      }
      stage->allowCollisions(lara5_mtc::pieceObjectId(square), arm_links, true);
    }
  }
  return stage;
}

std::unique_ptr<mtc::stages::MoveRelative>
makeWorldDeltaMove(const std::string& name,
                   const mtc::solvers::PlannerInterfacePtr& planner,
                   const double dx,
                   const double dy,
                   const double dz,
                   const mtc::PropagatingEitherWay::Direction propagation)
{
  const double dist = std::sqrt(dx * dx + dy * dy + dz * dz);
  if (dist < 1e-4)
  {
    return nullptr;
  }

  auto stage = std::make_unique<mtc::stages::MoveRelative>(name, planner);
  stage->properties().configureInitFrom(mtc::Stage::PARENT, { "group" });
  stage->setIKFrame(makeTopDownIkFrame());
  stage->setMinMaxDistance(std::min(0.001, dist * 0.05), dist);

  geometry_msgs::msg::Vector3Stamped direction;
  direction.header.frame_id = kWorldFrame;
  direction.vector.x = dx / dist;
  direction.vector.y = dy / dist;
  direction.vector.z = dz / dist;
  stage->setDirection(direction);
  stage->restrictDirection(propagation);
  return stage;
}

void addWorldDeltaMove(mtc::Task& task,
                       const std::string& name,
                       const mtc::solvers::PlannerInterfacePtr& planner,
                       const double dx,
                       const double dy,
                       const double dz,
                       const mtc::PropagatingEitherWay::Direction propagation)
{
  if (auto stage = makeWorldDeltaMove(name, planner, dx, dy, dz, propagation))
  {
    task.add(std::move(stage));
  }
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
  stage->setIKFrame(makeTopDownIkFrame());
  stage->setMinMaxDistance(std::min(0.001, distance_m * 0.05), distance_m);

  geometry_msgs::msg::Vector3Stamped direction;
  direction.header.frame_id = kWorldFrame;
  direction.vector.x = 0.0;
  direction.vector.y = 0.0;
  direction.vector.z = axis_sign;
  stage->setDirection(direction);
  stage->restrictDirection(propagation);
  return stage;
}

void addPickHoverTransit(mtc::Task& task,
                         const mtc::solvers::PlannerInterfacePtr& cartesian_planner,
                         const moveit::core::RobotModelConstPtr& model,
                         const std::string& seed_pose,
                         const geometry_msgs::msg::PoseStamped& pick_hover_pose)
{
  const moveit::core::RobotState seed_state = namedArmState(model, seed_pose);
  const auto& seed_tf = seed_state.getGlobalLinkTransform(kEefLink);
  const double seed_x = seed_tf.translation().x();
  const double seed_y = seed_tf.translation().y();
  const double seed_z = seed_tf.translation().z();

  const double dx = pick_hover_pose.pose.position.x - seed_x;
  const double dy = pick_hover_pose.pose.position.y - seed_y;
  const double dz = pick_hover_pose.pose.position.z - seed_z;

  // Single stage so RViz/MTC panel shows the hover end pose on one click (not only on a child).
  addWorldDeltaMove(task, "pick hover", cartesian_planner, dx, dy, dz, mtc::PropagatingEitherWay::FORWARD);
}

void addPlaceHoverTransit(mtc::Task& task,
                          const mtc::solvers::PlannerInterfacePtr& cartesian_planner,
                          const geometry_msgs::msg::PoseStamped& pick_hover_pose,
                          const geometry_msgs::msg::PoseStamped& place_hover_pose)
{
  addWorldDeltaMove(task, "place hover slide", cartesian_planner,
                    place_hover_pose.pose.position.x - pick_hover_pose.pose.position.x,
                    place_hover_pose.pose.position.y - pick_hover_pose.pose.position.y,
                    place_hover_pose.pose.position.z - pick_hover_pose.pose.position.z,
                    mtc::PropagatingEitherWay::FORWARD);
}

bool waitForPlanningSceneObject(const rclcpp::Node::SharedPtr& node,
                                const std::string& object_id,
                                const double timeout_s)
{
  using GetPlanningScene = moveit_msgs::srv::GetPlanningScene;
  auto client = node->create_client<GetPlanningScene>("/get_planning_scene");
  const rclcpp::Time deadline = node->now() + rclcpp::Duration::from_seconds(timeout_s);
  while (rclcpp::ok() && node->now() < deadline)
  {
    if (!client->wait_for_service(std::chrono::milliseconds(200)))
    {
      continue;
    }
    auto request = std::make_shared<GetPlanningScene::Request>();
    request->components.components = moveit_msgs::msg::PlanningSceneComponents::WORLD_OBJECT_GEOMETRY;
    auto future = client->async_send_request(request);
    if (future.wait_for(std::chrono::milliseconds(500)) != std::future_status::ready)
    {
      continue;
    }
    auto response = future.get();
    for (const auto& object : response->scene.world.collision_objects)
    {
      if (object.id == object_id)
      {
        return true;
      }
    }
    std::this_thread::sleep_for(std::chrono::milliseconds(500));
  }
  return false;
}

const moveit::core::RobotState& endRobotState(const mtc::SolutionBase& solution)
{
  if (const auto* sub = dynamic_cast<const mtc::SubTrajectory*>(&solution))
  {
    if (const auto& traj = sub->trajectory())
    {
      if (traj->getWayPointCount() > 0)
      {
        return traj->getLastWayPoint();
      }
    }
  }
  if (solution.end() != nullptr && solution.end()->scene() != nullptr)
  {
    return solution.end()->scene()->getCurrentState();
  }
  throw std::runtime_error("solution has no end robot state");
}

nlohmann::json jointGroupJson(const moveit::core::RobotState& state, const char* group_name,
                              const moveit::core::RobotModelConstPtr& model)
{
  nlohmann::json joints = nlohmann::json::object();
  const auto* jmg = model->getJointModelGroup(group_name);
  if (jmg == nullptr)
  {
    return joints;
  }
  for (const std::string& name : jmg->getVariableNames())
  {
    joints[name] = state.getVariablePosition(name);
  }
  return joints;
}

nlohmann::json eefPoseJson(const moveit::core::RobotState& state)
{
  const Eigen::Isometry3d& tf = state.getGlobalLinkTransform(kEefLink);
  const geometry_msgs::msg::Pose pose = tf2::toMsg(tf);
  tf2::Quaternion q(pose.orientation.x, pose.orientation.y, pose.orientation.z, pose.orientation.w);
  double roll = 0.0;
  double pitch = 0.0;
  double yaw = 0.0;
  tf2::Matrix3x3(q).getRPY(roll, pitch, yaw);
  return {
    { "frame", kWorldFrame },
    { "x", pose.position.x },
    { "y", pose.position.y },
    { "z", pose.position.z },
    { "roll_rad", roll },
    { "pitch_rad", pitch },
    { "yaw_rad", yaw },
  };
}

void collectSolutionPreview(const mtc::SolutionBase& solution,
                            const moveit::core::RobotModelConstPtr& model,
                            nlohmann::json& stages,
                            const int depth)
{
  if (const auto* wrapped = dynamic_cast<const mtc::WrappedSolution*>(&solution))
  {
    collectSolutionPreview(*wrapped->wrapped(), model, stages, depth);
    return;
  }

  if (const auto* seq = dynamic_cast<const mtc::SolutionSequence*>(&solution))
  {
    if (const auto* container = dynamic_cast<const mtc::Container*>(solution.creator());
        container != nullptr && !seq->solutions().empty())
    {
      nlohmann::json entry;
      entry["depth"] = depth;
      entry["name"] = container->name();
      entry["cost"] = solution.cost();
      entry["container"] = true;
      try
      {
        const moveit::core::RobotState& state = endRobotState(*seq->solutions().back());
        entry["arm_joints_rad"] = jointGroupJson(state, kArmGroup, model);
        entry["gripper_joints_rad"] = jointGroupJson(state, kGripperGroup, model);
        entry["eef"] = eefPoseJson(state);
        stages.push_back(entry);
      }
      catch (const std::exception& e)
      {
        entry["state_error"] = e.what();
        stages.push_back(entry);
      }
    }

    const bool nested_container = dynamic_cast<const mtc::Container*>(solution.creator()) != nullptr;
    for (const mtc::SolutionBase* sub : seq->solutions())
    {
      collectSolutionPreview(*sub, model, stages, nested_container ? depth + 1 : depth);
    }
    return;
  }

  const mtc::Stage* stage = solution.creator();
  nlohmann::json entry;
  entry["depth"] = depth;
  entry["name"] = stage != nullptr ? stage->name() : "unknown";
  entry["cost"] = solution.cost();

  if (solution.isFailure())
  {
    entry["failed"] = true;
    entry["comment"] = solution.comment();
    stages.push_back(entry);
    RCLCPP_WARN(LOGGER, "[preview %d] %s FAILED: %s", depth, entry["name"].get<std::string>().c_str(),
                solution.comment().c_str());
    return;
  }

  try
  {
    const moveit::core::RobotState& state = endRobotState(solution);
    entry["arm_joints_rad"] = jointGroupJson(state, kArmGroup, model);
    entry["gripper_joints_rad"] = jointGroupJson(state, kGripperGroup, model);
    entry["eef"] = eefPoseJson(state);

    if (const auto* sub = dynamic_cast<const mtc::SubTrajectory*>(&solution))
    {
      if (const auto& traj = sub->trajectory())
      {
        entry["waypoints"] = traj->getWayPointCount();
      }
    }

    stages.push_back(entry);

    const auto& eef = entry["eef"];
    RCLCPP_INFO(LOGGER,
                "[preview %d] %s  eef=(%.3f, %.3f, %.3f) rpy=(%.2f, %.2f, %.2f)  arm_j1=%.3f",
                depth, entry["name"].get<std::string>().c_str(), eef["x"].get<double>(), eef["y"].get<double>(),
                eef["z"].get<double>(), eef["roll_rad"].get<double>(), eef["pitch_rad"].get<double>(),
                eef["yaw_rad"].get<double>(), entry["arm_joints_rad"]["lara5_joint1"].get<double>());
  }
  catch (const std::exception& e)
  {
    entry["state_error"] = e.what();
    stages.push_back(entry);
    RCLCPP_WARN(LOGGER, "[preview %d] %s — no robot state: %s", depth, entry["name"].get<std::string>().c_str(),
                e.what());
  }
}

void dumpSolutionPreview(const mtc::SolutionBase& solution,
                         const moveit::core::RobotModelConstPtr& model,
                         const SolutionPreviewPaths& paths,
                         const std::string& source_square,
                         const std::string& target_square)
{
  nlohmann::json report;
  report["task"] = "lara5_mtc_chess_cylinders_pick_place";
  report["eef_link"] = kEefLink;
  report["move"] = { { "source", source_square }, { "target", target_square } };
  report["timestamp"] = isoTimestamp();
  report["workspace"] = superbloomRepoRoot();
  report["stages"] = nlohmann::json::array();
  collectSolutionPreview(solution, model, report["stages"], 0);

  const auto parent = std::filesystem::path(paths.archive_file).parent_path();
  if (!parent.empty())
  {
    std::filesystem::create_directories(parent);
  }

  std::ofstream out(paths.archive_file);
  if (!out)
  {
    RCLCPP_ERROR(LOGGER, "Could not write solution preview to %s", paths.archive_file.c_str());
    return;
  }
  out << report.dump(2) << '\n';
  out.close();

  std::error_code ec;
  std::filesystem::copy_file(paths.archive_file, paths.latest_file,
                               std::filesystem::copy_options::overwrite_existing, ec);
  if (ec)
  {
    RCLCPP_WARN(LOGGER, "Could not update %s: %s", paths.latest_file.c_str(), ec.message().c_str());
  }

  RCLCPP_INFO(LOGGER, "Solution preview (%zu stages) written to %s (latest: %s)", report["stages"].size(),
              paths.archive_file.c_str(), paths.latest_file.c_str());
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
  node->declare_parameter<std::string>("chess_seed_pose", "pre_pick");
  node->declare_parameter<double>("chess_top_down_roll", kDefaultTopDownRoll);
  node->declare_parameter<double>("chess_top_down_pitch", kDefaultTopDownPitch);
  node->declare_parameter<double>("chess_top_down_yaw", kDefaultTopDownYaw);
  node->declare_parameter<double>("planning_scene_timeout_s", 30.0);
  node->declare_parameter<bool>("auto_execute", false);
  // -1 = spin until Ctrl+C (RViz inspect/execute); 0 = exit immediately (CI); >0 = seconds
  node->declare_parameter<double>("keep_alive_s", -1.0);
  node->declare_parameter<bool>("dump_solution_preview", true);
  // Empty dir/file → <repo>/src/lara5_mtc/log/solution_<src>_to_<tgt>_<timestamp>.json + solution_latest.json
  node->declare_parameter<std::string>("solution_preview_dir", "");
  node->declare_parameter<std::string>("solution_preview_file", "");

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
  (void)node->get_parameter("chess_place_descent_m").as_double();  // legacy; hover uses approach_m
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
  const double keep_alive_s = [&]() {
    if (const std::string env = envOrEmpty("KEEP_ALIVE_S"); !env.empty())
    {
      return std::stod(env);
    }
    return node->get_parameter("keep_alive_s").as_double();
  }();
  const bool dump_solution_preview = node->get_parameter("dump_solution_preview").as_bool();
  const std::string seed_pose = [&]() {
    if (const std::string env = envOrEmpty("CHESS_SEED_POSE"); !env.empty())
    {
      return env;
    }
    return node->get_parameter("chess_seed_pose").as_string();
  }();
  const double top_down_roll = node->get_parameter("chess_top_down_roll").as_double();
  const double top_down_pitch = node->get_parameter("chess_top_down_pitch").as_double();
  const double top_down_yaw = node->get_parameter("chess_top_down_yaw").as_double();

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

    const double pick_grasp_z = source_pose.z + move.piece_height + grasp_clearance_m;
    const double pick_hover_z = pick_grasp_z + approach_m;
    const double place_grasp_z = target_pose.z + move.piece_height + grasp_clearance_m;
    const double place_hover_z = place_grasp_z + approach_m;

    RCLCPP_INFO(LOGGER,
                "Move %s -> %s  type=%s  cylinder(d=%.3f, h=%.3f)  object=%s  "
                "seed=%s  top_down_rpy=(%.2f, %.2f, %.2f)  "
                "pick_hover_z=%.3f  pick_grasp_z=%.3f  place_hover_z=%.3f  place_grasp_z=%.3f",
                move.source.c_str(), move.target.c_str(), move.piece_type.c_str(), move.piece_diameter,
                move.piece_height, move.object_id.c_str(), seed_pose.c_str(), top_down_roll, top_down_pitch,
                top_down_yaw, pick_hover_z, pick_grasp_z, place_hover_z, place_grasp_z);

    if (!waitForPlanningSceneObject(node, move.object_id, planning_scene_timeout_s))
    {
      RCLCPP_ERROR(LOGGER,
                   "Object %s not in move_group planning scene — start T2 first: "
                   "ros2 launch xyz_motion chess_scene.launch.py "
                   "use_cylinder_collision:=true planning_scene_only:=true",
                   move.object_id.c_str());
      rclcpp::shutdown();
      spinner.join();
      return 1;
    }

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
    cartesian_planner->setMinFraction(0.05);

    const mtc::solvers::PlannerInterfacePtr arm_planner = pipeline_planner;

    const std::string orientation_seed = seed_pose.empty() ? kHomePose : seed_pose;
    const bool use_explicit_rpy = top_down_roll != kDefaultTopDownRoll || top_down_pitch != kDefaultTopDownPitch ||
                                  top_down_yaw != kDefaultTopDownYaw;
    const auto grasp_orientation = use_explicit_rpy ?
                                       eulerToQuaternion(top_down_roll, top_down_pitch, top_down_yaw) :
                                       orientationFromNamedState(task.getRobotModel(), orientation_seed);

    const geometry_msgs::msg::PoseStamped pick_hover_pose =
        makeWorldPose(source_pose.x, source_pose.y, pick_hover_z, grasp_orientation);
    const geometry_msgs::msg::PoseStamped place_hover_pose =
        makeWorldPose(target_pose.x, target_pose.y, place_hover_z, grasp_orientation);

    RCLCPP_INFO(LOGGER,
                "EEF orientation: %s",
                use_explicit_rpy ? "explicit RPY params" : ("FK from seed '" + orientation_seed + "'").c_str());

    {
      moveit::core::RobotState ik_check = namedArmState(task.getRobotModel(), seed_pose);
      std::string ik_error;
      if (!solveIkForPose(task.getRobotModel(), ik_check, pick_hover_pose.pose, &ik_error))
      {
        RCLCPP_ERROR(LOGGER, "pick hover pose unreachable from seed: %s", ik_error.c_str());
        rclcpp::shutdown();
        spinner.join();
        return 1;
      }
    }

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

    // Joint-space seed over the board (orientation reference for hover IK goals).
    if (!seed_pose.empty())
    {
      auto stage = std::make_unique<mtc::stages::MoveTo>("seed arm", joint_planner);
      stage->setGroup(kArmGroup);
      stage->setGoal(seed_pose);
      stage->restrictDirection(mtc::PropagatingEitherWay::FORWARD);
      task.add(std::move(stage));
    }

    // Minimal collision allows (piece + all board squares / pieces for vertical approach).
    task.add(makeAllowPieceCollisions("allow collision (gripper,piece)", move.object_id,
                                      task.getRobotModel()));
    task.add(makeAllowGripperBoardCollisions(task.getRobotModel()));
    task.add(makeAllowGripperAllPieceCollisions(task.getRobotModel()));
    task.add(makeAllowArmOtherPieceCollisions(move.source, task.getRobotModel()));

    if (seed_pose.empty())
    {
      RCLCPP_ERROR(LOGGER, "chess_seed_pose is required (e.g. pre_pick)");
      rclcpp::shutdown();
      spinner.join();
      return 1;
    }

    // --- Pick: Cartesian hover (world −Z then XY at height) → vertical descend → lift ---
    addPickHoverTransit(task, cartesian_planner, task.getRobotModel(), seed_pose, pick_hover_pose);
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

    addPlaceHoverTransit(task, cartesian_planner, pick_hover_pose, place_hover_pose);

    // --- Place: vertical descend → release → retreat ---
    task.add(makeWorldZMove("descend place", cartesian_planner, approach_m, -1.0,
                            mtc::PropagatingEitherWay::FORWARD));
    task.add(makeAllowReleaseCollisions(move.object_id, move.target, task.getRobotModel()));
    {
      auto detach = std::make_unique<mtc::stages::ModifyPlanningScene>("detach piece");
      detach->detachObject(move.object_id, kEefLink);
      task.add(std::move(detach));
    }
    task.add(makeWorldZMove("retreat after place", cartesian_planner, approach_m, 1.0,
                            mtc::PropagatingEitherWay::FORWARD));
    {
      auto stage = std::make_unique<mtc::stages::MoveTo>("open gripper after place", joint_planner);
      stage->setGroup(kGripperGroup);
      stage->setGoal(kGripperOpen);
      task.add(std::move(stage));
    }

    addMoveArmToNamed(task, "move to stand", arm_planner, kHomePose);

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
        if (dump_solution_preview)
        {
          const auto preview_paths = resolveSolutionPreviewPaths(node, source_override, target_override);
          dumpSolutionPreview(*task.solutions().front(), task.getRobotModel(), preview_paths, source_override,
                              target_override);
        }
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
      else if (keep_alive_s < 0.0)
      {
        RCLCPP_INFO(LOGGER,
                    "Plan OK — in RViz: Motion Planning Tasks → expand root solution → "
                    "Execute (Ctrl+C here to exit)");
        while (rclcpp::ok())
        {
          std::this_thread::sleep_for(std::chrono::milliseconds(200));
        }
      }
      else if (keep_alive_s > 0.0)
      {
        RCLCPP_INFO(LOGGER, "Plan OK — node stays up %.0f s for RViz inspect/execute", keep_alive_s);
        std::this_thread::sleep_for(
            std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::duration<double>(keep_alive_s)));
      }
      else
      {
        RCLCPP_INFO(LOGGER, "Plan OK (keep_alive_s=0 — exiting)");
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
