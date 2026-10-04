// mtc_pose_sequence.cpp
//
// MoveIt Task Constructor (MTC) demo:
//   1. Move EEF to the SRDF-named pose "mid_move"
//   2. Move EEF to the SRDF-named hover pose (`hover_pose`, default "a1_hover")
//   3. Open the gripper to `gripper_open_position` (default 0.25 rad)
//   4. Move EEF straight down (-Z) relative to that hover, by `lower_distance`
//   5. Close the gripper to `gripper_close_position`
//   6. Move EEF back up (+Z), by `lift_distance`
//
// All of these are ROS parameters, so no rebuild to change them. Distances in metres (default
// 0.05). hover_pose is an SRDF name ("e4_hover") or a square ("e4"). Jaw open defaults to
// 0.25 rad; jaw close defaults to the SRDF-named state "close":
//   ros2 launch lara5_mtc mtc_pose_sequence.launch.py hover_pose:=e4
//   ros2 launch lara5_mtc mtc_pose_sequence.launch.py lower_distance:=0.03
//   ros2 launch lara5_mtc mtc_pose_sequence.launch.py gripper_close_position:=0.2
//
// Structure follows the official MTC tutorial pattern:
// https://moveit.picknik.ai/main/doc/tutorials/task_constructor/tutorial_task_constructor.html

#include <algorithm>
#include <iomanip>
#include <map>
#include <sstream>
#include <string>

#include <rclcpp/rclcpp.hpp>
#include <moveit/robot_model/robot_model.h>
#include <moveit/task_constructor/task.h>
#include <moveit/task_constructor/stages/current_state.h>
#include <moveit/task_constructor/stages/move_to.h>
#include <moveit/task_constructor/stages/move_relative.h>
#include <moveit/task_constructor/solvers/pipeline_planner.h>
#include <moveit/task_constructor/solvers/cartesian_path.h>
#include <moveit/task_constructor/solvers/joint_interpolation.h>

namespace mtc = moveit::task_constructor;


static const std::string ARM_GROUP = "arm";
static const std::string GRIPPER_GROUP = "gripper";
static const std::string GRIPPER_JOINT = "lara5_gripper_finger_joint";
static const std::string CLOSE_STATE = "close";
static const std::string DEFAULT_HOVER_POSE = "a1_hover";
static constexpr double DEFAULT_Z_DISTANCE = 0.05;
static constexpr double DEFAULT_GRIPPER_OPEN = 0.25;

// "move down" + 0.03 -> "move down 3.0 cm", so the RViz task tree shows the real distance
static std::string zStageName(const std::string& verb, double meters)
{
  std::ostringstream name;
  name << verb << ' ' << std::fixed << std::setprecision(1) << meters * 100.0 << " cm";
  return name.str();
}

class PoseSequenceNode
{
public:
  PoseSequenceNode(const rclcpp::Node::SharedPtr& node) : node_(node)
  {
  }

  void doTask()
  {
    task_ = createTask();

    try
    {
      task_.init();
    }
    catch (mtc::InitStageException& e)
    {
      RCLCPP_ERROR_STREAM(node_->get_logger(), "Task init failed: " << e);
      return;
    }

    if (!task_.plan(5 /* max solutions */))
    {
      RCLCPP_ERROR(node_->get_logger(), "Task planning failed");
      return;
    }

    // Publish the solution so it shows up in the RViz MTC panel
    task_.introspection().publishSolution(*task_.solutions().front());

    auto result = task_.execute(*task_.solutions().front());
    if (result.val != moveit_msgs::msg::MoveItErrorCodes::SUCCESS)
    {
      RCLCPP_ERROR(node_->get_logger(), "Task execution failed");
    }
  }

private:
  mtc::Task createTask()
  {
    mtc::Task task;
    task.stages()->setName("pose_sequence_task");
    task.loadRobotModel(node_);

    task.setProperty("group", ARM_GROUP);

    // Planners
    auto sampling_planner = std::make_shared<mtc::solvers::PipelinePlanner>(node_);
    auto cartesian_planner = std::make_shared<mtc::solvers::CartesianPath>();
    cartesian_planner->setMaxVelocityScalingFactor(1.0);
    cartesian_planner->setMaxAccelerationScalingFactor(1.0);
    cartesian_planner->setStepSize(.01);

    // 0. Start from the robot's current state
    task.add(std::make_unique<mtc::stages::CurrentState>("current state"));

    // 1. Move EEF to SRDF-named pose "mid_move"
    {
      auto stage = std::make_unique<mtc::stages::MoveTo>("move to mid_move", sampling_planner);
      stage->setGroup(ARM_GROUP);
      stage->setGoal("mid_move");
      task.add(std::move(stage));
    }

    // 2. Move EEF to the chosen SRDF hover pose
    const std::string hover = hoverPoseName(task.getRobotModel());
    {
      auto stage = std::make_unique<mtc::stages::MoveTo>("move to " + hover, sampling_planner);
      stage->setGroup(ARM_GROUP);
      stage->setGoal(hover);
      task.add(std::move(stage));
    }

    // 3. Open the gripper at hover, before descending
    task.add(createGripperStage(task.getRobotModel(), "open", "gripper_open_position",
                                DEFAULT_GRIPPER_OPEN));

    // 4. Move EEF down along Z, relative to the current hover pose
    {
      const double distance = distanceParam("lower_distance");
      auto stage =
          std::make_unique<mtc::stages::MoveRelative>(zStageName("move down", distance), cartesian_planner);
      stage->setGroup(ARM_GROUP);

      geometry_msgs::msg::Vector3Stamped direction;
      direction.header.frame_id = "world";  // adjust to your planning/base frame if different
      direction.vector.z = -distance;
      stage->setDirection(direction);

      task.add(std::move(stage));
    }

    // 5. Close the gripper at the bottom of the descent
    task.add(createGripperStage(task.getRobotModel(), "close", "gripper_close_position"));

    // 6. Move EEF back up along Z, relative to the current hover pose
    {
      const double distance = distanceParam("lift_distance");
      auto stage =
          std::make_unique<mtc::stages::MoveRelative>(zStageName("move up", distance), cartesian_planner);
      stage->setGroup(ARM_GROUP);

      geometry_msgs::msg::Vector3Stamped direction;
      direction.header.frame_id = "world";  // adjust to your planning/base frame if different
      direction.vector.z = distance;
      stage->setDirection(direction);

      task.add(std::move(stage));
    }

    return task;
  }

  // SRDF group state for the hover, e.g. "e4_hover". "e4" is accepted and becomes "e4_hover".
  std::string hoverPoseName(const moveit::core::RobotModelConstPtr& model) const
  {
    std::string pose = DEFAULT_HOVER_POSE;
    node_->get_parameter("hover_pose", pose);
    if (pose.find("_hover") == std::string::npos)
      pose += "_hover";

    std::map<std::string, double> joints;
    if (!model->getJointModelGroup(ARM_GROUP)->getVariableDefaultPositions(pose, joints))
    {
      RCLCPP_WARN(node_->get_logger(), "hover_pose '%s' is not an SRDF arm state, using '%s'",
                  pose.c_str(), DEFAULT_HOVER_POSE.c_str());
      pose = DEFAULT_HOVER_POSE;
    }
    RCLCPP_INFO(node_->get_logger(), "hover_pose = %s", pose.c_str());
    return pose;
  }

  // Vertical travel in metres. Parameters come from the launch file; missing ones keep the
  // default, since get_parameter() only writes on a hit.
  double distanceParam(const std::string& name) const
  {
    double distance = DEFAULT_Z_DISTANCE;
    node_->get_parameter(name, distance);
    RCLCPP_INFO(node_->get_logger(), "%s = %.3f m", name.c_str(), distance);
    return distance;
  }

  // Move the gripper jaw to a joint angle in radians. `param_name` overrides `fallback`.
  // Joint interpolation is enough: one joint. Executed by gripper_controller (GripperCommand).
  std::unique_ptr<mtc::stages::MoveTo> createGripperStage(const moveit::core::RobotModelConstPtr& model,
                                                          const std::string& verb,
                                                          const std::string& param_name,
                                                          double fallback)
  {
    const double position = gripperJointPosition(model, param_name, fallback);

    std::ostringstream name;
    name << verb << " gripper to " << std::fixed << std::setprecision(3) << position << " rad";

    auto planner = std::make_shared<mtc::solvers::JointInterpolationPlanner>();
    auto stage = std::make_unique<mtc::stages::MoveTo>(name.str(), planner);
    stage->setGroup(GRIPPER_GROUP);
    stage->setGoal(std::map<std::string, double>{ { GRIPPER_JOINT, position } });
    return stage;
  }

  std::unique_ptr<mtc::stages::MoveTo> createGripperStage(const moveit::core::RobotModelConstPtr& model,
                                                          const std::string& verb,
                                                          const std::string& param_name)
  {
    std::map<std::string, double> srdf_close;
    model->getJointModelGroup(GRIPPER_GROUP)->getVariableDefaultPositions(CLOSE_STATE, srdf_close);
    return createGripperStage(model, verb, param_name, srdf_close.at(GRIPPER_JOINT));
  }

  double gripperJointPosition(const moveit::core::RobotModelConstPtr& model, const std::string& param_name,
                              double fallback) const
  {
    double position = fallback;
    node_->get_parameter(param_name, position);

    const auto& limits = model->getJointModel(GRIPPER_JOINT)->getVariableBounds(GRIPPER_JOINT);
    const double clamped = std::clamp(position, limits.min_position_, limits.max_position_);
    if (clamped != position)
      RCLCPP_WARN(node_->get_logger(), "%s %.3f rad outside [%.3f, %.3f], clamped", param_name.c_str(),
                  position, limits.min_position_, limits.max_position_);

    RCLCPP_INFO(node_->get_logger(), "%s = %.3f rad", param_name.c_str(), clamped);
    return clamped;
  }

  rclcpp::Node::SharedPtr node_;
  mtc::Task task_;
};

int main(int argc, char** argv)
{
  rclcpp::init(argc, argv);

  rclcpp::NodeOptions options;
  options.automatically_declare_parameters_from_overrides(true);
  auto node = rclcpp::Node::make_shared("mtc_pose_sequence_node", options);

  rclcpp::executors::MultiThreadedExecutor executor;
  executor.add_node(node);
  std::thread spin_thread([&executor]() { executor.spin(); });

  PoseSequenceNode task_node(node);
  task_node.doTask();

  // Task introspection (/description, /statistics, /solution) lives in this process, so
  // exiting here would drop the task from the RViz "Motion Planning Tasks" panel.
  RCLCPP_INFO(node->get_logger(), "Task done. Browse stages in RViz; Ctrl-C to exit.");
  spin_thread.join();
  rclcpp::shutdown();
  return 0;
}