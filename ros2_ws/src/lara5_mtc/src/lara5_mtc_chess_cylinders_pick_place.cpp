/*********************************************************************
 * Lara5 chess cylinder pick-and-place with MoveIt Task Constructor.
 *
 * TF-backed MTC chess pick-and-place: lookup grasp/<sq> frames, parametrized tree.
 *
 * Run:
 *   ros2 launch xyz_motion chess_scene.launch.py use_cylinder_collision:=true planning_scene_only:=true
 *   ros2 launch lara5_moveit_config mtc_demo_headless.launch.py
 *   ros2 launch lara5_mtc mtc_chess_cylinders_pick_place.launch.py keep_alive_s:=0
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
#include <tf2/exceptions.h>
#include <tf2/time.h>
#include <tf2_eigen/tf2_eigen.hpp>
#include <tf2_geometry_msgs/tf2_geometry_msgs.hpp>
#include <tf2_ros/buffer.h>
#include <tf2_ros/transform_listener.h>

#include "lara5_mtc/chess_occupancy.hpp"
#include "lara5_mtc/pick_place_task.hpp"

namespace mtc = moveit::task_constructor;

static const rclcpp::Logger LOGGER = rclcpp::get_logger("lara5_mtc_chess_cylinders_pick_place");

namespace
{

constexpr const char* kArmGroup = "arm";
constexpr const char* kGripperGroup = "gripper";
constexpr const char* kEefLink = "lara5_gripper";
constexpr const char* kWorldFrame = "world";

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

geometry_msgs::msg::PoseStamped lookupTfPose(tf2_ros::Buffer& buffer, const std::string& parent_frame,
                                             const std::string& child_frame, const double timeout_s)
{
  const auto tf = buffer.lookupTransform(parent_frame, child_frame, tf2::TimePointZero,
                                         tf2::durationFromSec(timeout_s));
  geometry_msgs::msg::PoseStamped pose;
  pose.header = tf.header;
  pose.header.frame_id = parent_frame;
  pose.pose.position.x = tf.transform.translation.x;
  pose.pose.position.y = tf.transform.translation.y;
  pose.pose.position.z = tf.transform.translation.z;
  pose.pose.orientation = tf.transform.rotation;
  return pose;
}

moveit::core::RobotState namedArmState(const moveit::core::RobotModelConstPtr& model, const std::string& named)
{
  moveit::core::RobotState state(model);
  state.setToDefaultValues();
  state.setToDefaultValues(model->getJointModelGroup(kArmGroup), named);
  state.update();
  return state;
}

bool solveIkForPose(const moveit::core::RobotModelConstPtr& model, moveit::core::RobotState& state,
                    const geometry_msgs::msg::Pose& pose, std::string* error = nullptr)
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
    if (const auto* container = dynamic_cast<const mtc::ContainerBase*>(solution.creator());
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

    const bool nested_container = dynamic_cast<const mtc::ContainerBase*>(solution.creator()) != nullptr;
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
  node->declare_parameter<std::string>("chess_grasp_frame_prefix", "grasp");
  node->declare_parameter<std::string>("chess_pick_frame", "");
  node->declare_parameter<std::string>("chess_place_frame", "");
  node->declare_parameter<std::string>("chess_world_frame", kWorldFrame);
  node->declare_parameter<double>("chess_tf_timeout_s", 10.0);
  node->declare_parameter<std::string>("chess_approach_frame", "world");
  node->declare_parameter<std::string>("chess_hover_mode", "cartesian");
  node->declare_parameter<double>("chess_square_size_m", 0.04);
  node->declare_parameter<double>("chess_grasp_clearance_m", 0.015);
  node->declare_parameter<double>("chess_approach_m", 0.08);
  node->declare_parameter<double>("chess_lift_m", 0.08);
  node->declare_parameter<double>("chess_place_descent_m", 0.04);
  node->declare_parameter<std::string>("chess_seed_pose", "pre_pick");
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
  (void)square_size_m;
  const double approach_m = node->get_parameter("chess_approach_m").as_double();
  const double lift_m = node->get_parameter("chess_lift_m").as_double();
  (void)node->get_parameter("chess_place_descent_m").as_double();
  (void)node->get_parameter("chess_grasp_clearance_m").as_double();
  const std::string grasp_prefix = node->get_parameter("chess_grasp_frame_prefix").as_string();
  const std::string world_frame = node->get_parameter("chess_world_frame").as_string();
  const double tf_timeout_s = node->get_parameter("chess_tf_timeout_s").as_double();
  const std::string approach_frame = node->get_parameter("chess_approach_frame").as_string();
  const std::string hover_mode = node->get_parameter("chess_hover_mode").as_string();
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

  tf2_ros::Buffer tf_buffer(node->get_clock());
  tf2_ros::TransformListener tf_listener(tf_buffer);

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
    const std::string pick_frame = [&]() {
      const std::string override_frame = node->get_parameter("chess_pick_frame").as_string();
      if (!override_frame.empty())
      {
        return override_frame;
      }
      return grasp_prefix + "/" + move.source;
    }();
    const std::string place_frame = [&]() {
      const std::string override_frame = node->get_parameter("chess_place_frame").as_string();
      if (!override_frame.empty())
      {
        return override_frame;
      }
      return grasp_prefix + "/" + move.target;
    }();

    RCLCPP_INFO(LOGGER,
                "Move %s -> %s  type=%s  object=%s  seed=%s  pick_tf=%s  place_tf=%s  "
                "hover_mode=%s  approach_frame=%s",
                move.source.c_str(), move.target.c_str(), move.piece_type.c_str(), move.object_id.c_str(),
                seed_pose.c_str(), pick_frame.c_str(), place_frame.c_str(), hover_mode.c_str(),
                approach_frame.c_str());

    if (!waitForPlanningSceneObject(node, move.object_id, planning_scene_timeout_s))
    {
      RCLCPP_ERROR(LOGGER,
                   "Object %s not in move_group planning scene — start chess_scene first: "
                   "ros2 launch xyz_motion chess_scene.launch.py "
                   "use_cylinder_collision:=true planning_scene_only:=true",
                   move.object_id.c_str());
      rclcpp::shutdown();
      spinner.join();
      return 1;
    }

    geometry_msgs::msg::PoseStamped pick_grasp;
    geometry_msgs::msg::PoseStamped place_grasp;
    try
    {
      pick_grasp = lookupTfPose(tf_buffer, world_frame, pick_frame, tf_timeout_s);
      place_grasp = lookupTfPose(tf_buffer, world_frame, place_frame, tf_timeout_s);
    }
    catch (const tf2::TransformException& e)
    {
      RCLCPP_ERROR(LOGGER,
                   "TF lookup failed for %s / %s in %s (timeout %.1fs): %s — start "
                   "ros2 launch xyz_motion grasp_tf.launch.py occupancy_file:=<same occupancy>",
                   pick_frame.c_str(), place_frame.c_str(), world_frame.c_str(), tf_timeout_s, e.what());
      rclcpp::shutdown();
      spinner.join();
      return 1;
    }

    RCLCPP_INFO(LOGGER,
                "TF pick %s xyz=(%.3f, %.3f, %.3f)  place %s xyz=(%.3f, %.3f, %.3f)",
                pick_frame.c_str(), pick_grasp.pose.position.x, pick_grasp.pose.position.y, pick_grasp.pose.position.z,
                place_frame.c_str(), place_grasp.pose.position.x, place_grasp.pose.position.y,
                place_grasp.pose.position.z);

    mtc::Task task;
    task.loadRobotModel(node);

    {
      auto pick_hover = lara5_mtc::hoverFromGrasp(pick_grasp, approach_m);
      moveit::core::RobotState ik_check = namedArmState(task.getRobotModel(), seed_pose);
      if (hover_mode == "cartesian")
      {
        pick_hover.pose.orientation = tf2::toMsg(ik_check.getGlobalLinkTransform(kEefLink)).orientation;
      }
      std::string ik_error;
      if (!solveIkForPose(task.getRobotModel(), ik_check, pick_hover.pose, &ik_error))
      {
        RCLCPP_ERROR(LOGGER, "pick hover pose unreachable from seed: %s", ik_error.c_str());
        rclcpp::shutdown();
        spinner.join();
        return 1;
      }
    }

    lara5_mtc::PickPlaceRequest req;
    req.object_id = move.object_id;
    req.source_square = move.source;
    req.target_square = move.target;
    req.seed_pose = seed_pose;
    req.pick_grasp = pick_grasp;
    req.place_grasp = place_grasp;
    req.approach_m = approach_m;
    req.lift_m = lift_m;
    req.planning_scene_timeout_s = planning_scene_timeout_s;
    req.approach_frame = approach_frame;
    req.hover_mode = hover_mode;
    lara5_mtc::populatePickPlaceTask(task, req, node);

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
