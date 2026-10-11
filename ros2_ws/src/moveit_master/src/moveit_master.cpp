// moveit_master: the ONLY node that commands the robot through MoveGroupInterface.
// It exposes one action, "moveit_master/execute_sequence", which runs a list of
// MotionSteps in order: arm pose / arm named state / straight-line (cartesian) arm move /
// gripper named state / gripper joint value / wait / attach / detach / allow collision.
//
// The sequence and all its parameters come from articulation_orchestrator.py.
// If a sequence fails or is canceled, the PlanningScene changes it made (attached objects,
// allowed collisions) are rolled back, so the scene again matches what the orchestrator expects.

#include <atomic>
#include <chrono>
#include <map>
#include <memory>
#include <set>
#include <string>
#include <thread>
#include <vector>

#include <rclcpp/rclcpp.hpp>
#include <rclcpp_action/rclcpp_action.hpp>
#include <moveit/move_group_interface/move_group_interface.h>
#include <moveit/planning_scene_interface/planning_scene_interface.h>
#include <moveit/collision_detection/collision_matrix.h>
#include <moveit/robot_trajectory/robot_trajectory.h>
#include <moveit/trajectory_processing/time_optimal_trajectory_generation.h>
#include <moveit_msgs/srv/get_planning_scene.hpp>

#include <moveit_master/action/execute_sequence.hpp>
#include <moveit_master/msg/motion_step.hpp>

using ExecuteSequence = moveit_master::action::ExecuteSequence;
using MotionStep = moveit_master::msg::MotionStep;
using GoalHandle = rclcpp_action::ServerGoalHandle<ExecuteSequence>;
using GetPlanningScene = moveit_msgs::srv::GetPlanningScene;
using moveit::planning_interface::MoveGroupInterface;
using moveit::planning_interface::PlanningSceneInterface;
using moveit::core::MoveItErrorCode;

class MoveItMaster
{
public:
  explicit MoveItMaster(const rclcpp::Node::SharedPtr & node)
  : node_(node), arm_(node, "arm"), gripper_(node, "gripper")
  {
    arm_.setPlanningTime(5.0);
    arm_.setNumPlanningAttempts(5);

    // EEF link + every link below it: allowed to touch a grasped object
    eef_link_ = arm_.getEndEffectorLink();
    if (eef_link_.empty()) {
      eef_link_ = arm_.getLinkNames().back();
    }
    addLinksBelow(arm_.getRobotModel()->getLinkModel(eef_link_));
    RCLCPP_INFO(node_->get_logger(), "eef link '%s', %zu gripper links",
                eef_link_.c_str(), gripper_links_.size());

    scene_client_ = node_->create_client<GetPlanningScene>("/get_planning_scene");

    server_ = rclcpp_action::create_server<ExecuteSequence>(
      node_, "moveit_master/execute_sequence",
      // accept only one goal at a time
      [this](const rclcpp_action::GoalUUID &, std::shared_ptr<const ExecuteSequence::Goal>) {
        return busy_.exchange(true) ? rclcpp_action::GoalResponse::REJECT
                                    : rclcpp_action::GoalResponse::ACCEPT_AND_EXECUTE;
      },
      // cancel: stop the current motion; the step loop exits afterwards
      [this](std::shared_ptr<GoalHandle>) {
        arm_.stop();
        gripper_.stop();
        return rclcpp_action::CancelResponse::ACCEPT;
      },
      // run in a separate thread so the executor keeps spinning
      [this](std::shared_ptr<GoalHandle> gh) {
        std::thread([this, gh] { execute(gh); }).detach();
      });

    RCLCPP_INFO(node_->get_logger(), "moveit_master ready");
  }

private:
  void addLinksBelow(const moveit::core::LinkModel * link)
  {
    gripper_links_.push_back(link->getName());
    for (const auto * joint : link->getChildJointModels()) {
      addLinksBelow(joint->getChildLinkModel());
    }
  }

  // Plan + execute whatever target is currently set on `group`.
  MoveItErrorCode planAndExecute(MoveGroupInterface & group)
  {
    MoveGroupInterface::Plan plan;
    auto ec = group.plan(plan);
    if (ec == MoveItErrorCode::SUCCESS) {
      ec = group.execute(plan);
    }
    return ec;
  }

  // Straight-line EEF move by `offset` (planning frame), collision-checked.
  MoveItErrorCode moveCartesian(const geometry_msgs::msg::Vector3 & offset)
  {
    auto target = arm_.getCurrentPose(eef_link_).pose;
    target.position.x += offset.x;
    target.position.y += offset.y;
    target.position.z += offset.z;

    moveit_msgs::msg::RobotTrajectory traj;
    const double fraction = arm_.computeCartesianPath({target}, 0.005, 0.0, traj);
    if (fraction < 0.999) {
      RCLCPP_ERROR(node_->get_logger(), "cartesian path only %.0f%% feasible", fraction * 100.0);
      return MoveItErrorCode::PLANNING_FAILED;
    }
    // computeCartesianPath times the path at full speed -> re-time it with the sequence scaling
    robot_trajectory::RobotTrajectory rt(arm_.getRobotModel(), arm_.getName());
    rt.setRobotTrajectoryMsg(*arm_.getCurrentState(), traj);
    trajectory_processing::TimeOptimalTrajectoryGeneration totg;
    if (!totg.computeTimeStamps(rt, vel_, vel_)) {
      return MoveItErrorCode::INVALID_MOTION_PLAN;
    }
    rt.getRobotTrajectoryMsg(traj);
    return arm_.execute(traj);
  }

  // Attach a world object to the EEF link (attach=true) or put it back into the world.
  MoveItErrorCode attach(const std::string & id, bool attach)
  {
    moveit_msgs::msg::AttachedCollisionObject aco;
    aco.link_name = eef_link_;
    aco.object.id = id;
    aco.object.operation = attach ? moveit_msgs::msg::CollisionObject::ADD
                                  : moveit_msgs::msg::CollisionObject::REMOVE;
    if (attach) {
      aco.touch_links = gripper_links_;
    }
    if (!psi_.applyAttachedCollisionObject(aco)) {
      return MoveItErrorCode::INVALID_OBJECT_NAME;
    }
    if (attach) {
      attached_.insert(id);
    } else {
      attached_.erase(id);
    }
    return MoveItErrorCode::SUCCESS;
  }

  // Allow (or undo allowing) contacts between object `id` and gripper links + `names`.
  MoveItErrorCode allowCollision(const std::string & id, std::vector<std::string> names, bool allow)
  {
    names.insert(names.end(), gripper_links_.begin(), gripper_links_.end());

    if (!scene_client_->wait_for_service(std::chrono::seconds(2))) {
      return MoveItErrorCode::TIMED_OUT;
    }
    auto req = std::make_shared<GetPlanningScene::Request>();
    req->components.components = moveit_msgs::msg::PlanningSceneComponents::ALLOWED_COLLISION_MATRIX;
    auto future = scene_client_->async_send_request(req);
    if (future.wait_for(std::chrono::seconds(5)) != std::future_status::ready) {
      return MoveItErrorCode::TIMED_OUT;
    }

    // the ACM in a scene diff replaces the whole matrix -> modify the current one
    collision_detection::AllowedCollisionMatrix acm(future.get()->scene.allowed_collision_matrix);
    for (const auto & name : names) {
      if (allow) {
        acm.setEntry(id, name, true);
        allowed_[id].insert(name);
      } else {
        acm.removeEntry(id, name);
        allowed_[id].erase(name);
      }
    }
    if (allowed_[id].empty()) {
      allowed_.erase(id);
    }

    moveit_msgs::msg::PlanningScene diff;
    diff.is_diff = true;
    diff.robot_state.is_diff = true;
    acm.getMessage(diff.allowed_collision_matrix);
    return psi_.applyPlanningScene(diff) ? MoveItErrorCode::SUCCESS : MoveItErrorCode::FAILURE;
  }

  // Undo scene changes of a failed / canceled sequence.
  void rollbackScene()
  {
    for (const auto & id : std::set<std::string>(attached_)) {
      attach(id, false);
    }
    for (const auto & [id, names] : std::map<std::string, std::set<std::string>>(allowed_)) {
      allowCollision(id, {names.begin(), names.end()}, false);
    }
  }

  MoveItErrorCode runStep(const MotionStep & step)
  {
    switch (step.type) {
      case MotionStep::ARM_POSE:
        arm_.setPoseTarget(step.pose);
        return planAndExecute(arm_);
      case MotionStep::ARM_NAMED:
        if (!arm_.setNamedTarget(step.named_target)) {
          return MoveItErrorCode::INVALID_GOAL_CONSTRAINTS;
        }
        return planAndExecute(arm_);
      case MotionStep::ARM_CARTESIAN:
        return moveCartesian(step.offset);
      case MotionStep::GRIPPER_NAMED:
        if (!gripper_.setNamedTarget(step.named_target)) {
          return MoveItErrorCode::INVALID_GOAL_CONSTRAINTS;
        }
        return planAndExecute(gripper_);
      case MotionStep::GRIPPER_JOINT:
        if (!gripper_.setJointValueTarget(gripper_.getActiveJoints().front(), step.joint_value)) {
          return MoveItErrorCode::INVALID_GOAL_CONSTRAINTS;
        }
        return planAndExecute(gripper_);
      case MotionStep::WAIT:
        rclcpp::sleep_for(std::chrono::milliseconds(static_cast<int64_t>(step.duration * 1000)));
        return MoveItErrorCode::SUCCESS;
      case MotionStep::ATTACH:
        return attach(step.object_id, true);
      case MotionStep::DETACH:
        return attach(step.object_id, false);
      case MotionStep::ALLOW_COLLISION:
        return allowCollision(step.object_id, step.touch_links, step.allow);
      default:
        return MoveItErrorCode::INVALID_MOTION_PLAN;
    }
  }

  void execute(std::shared_ptr<GoalHandle> gh)
  {
    const auto goal = gh->get_goal();
    auto result = std::make_shared<ExecuteSequence::Result>();
    auto feedback = std::make_shared<ExecuteSequence::Feedback>();

    vel_ = goal->velocity_scaling > 0.0 ? goal->velocity_scaling : 0.2;
    arm_.setMaxVelocityScalingFactor(vel_);
    arm_.setMaxAccelerationScalingFactor(vel_);
    attached_.clear();
    allowed_.clear();

    result->success = true;
    for (size_t i = 0; i < goal->steps.size(); ++i) {
      if (gh->is_canceling()) {
        result->success = false;
        result->failed_step = i;
        result->message = "canceled";
        break;
      }
      feedback->current_step = i;
      gh->publish_feedback(feedback);

      const auto ec = runStep(goal->steps[i]);
      if (ec != MoveItErrorCode::SUCCESS) {
        result->success = false;
        result->failed_step = i;
        result->message = moveit::core::error_code_to_string(ec);
        RCLCPP_ERROR(node_->get_logger(), "step %zu failed: %s", i, result->message.c_str());
        break;
      }
    }
    arm_.clearPoseTargets();
    if (!result->success) {
      rollbackScene();
    }

    if (gh->is_canceling()) {
      gh->canceled(result);
    } else if (result->success) {
      result->message = "done";
      gh->succeed(result);
    } else {
      gh->abort(result);
    }
    busy_ = false;
  }

  rclcpp::Node::SharedPtr node_;
  MoveGroupInterface arm_;
  MoveGroupInterface gripper_;
  PlanningSceneInterface psi_;
  rclcpp::Client<GetPlanningScene>::SharedPtr scene_client_;
  rclcpp_action::Server<ExecuteSequence>::SharedPtr server_;
  std::atomic<bool> busy_{false};

  std::string eef_link_;
  std::vector<std::string> gripper_links_;
  double vel_{0.2};
  // scene changes made by the running sequence (rolled back if it fails)
  std::set<std::string> attached_;
  std::map<std::string, std::set<std::string>> allowed_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<rclcpp::Node>(
    "moveit_master",
    rclcpp::NodeOptions().automatically_declare_parameters_from_overrides(true));

  // MultiThreaded: MoveGroupInterface (joint states) and the action server must keep spinning
  rclcpp::executors::MultiThreadedExecutor executor;
  executor.add_node(node);
  std::thread spinner([&executor] { executor.spin(); });

  MoveItMaster master(node);

  spinner.join();
  rclcpp::shutdown();
  return 0;
}
