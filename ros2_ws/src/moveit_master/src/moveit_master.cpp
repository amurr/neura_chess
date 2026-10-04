// moveit_master: the ONLY node that commands the robot through MoveGroupInterface.
// It exposes one action, "moveit_master/execute_sequence", which runs a list of
// MotionSteps (arm pose / arm named state / gripper named state / wait) in order.
//
// The sequence and all its parameters come from articulation_orchestrator.py.

#include <atomic>
#include <chrono>
#include <memory>
#include <thread>

#include <rclcpp/rclcpp.hpp>
#include <rclcpp_action/rclcpp_action.hpp>
#include <moveit/move_group_interface/move_group_interface.hpp>

#include <articulation_interfaces/action/execute_sequence.hpp>
#include <articulation_interfaces/msg/motion_step.hpp>

using ExecuteSequence = articulation_interfaces::action::ExecuteSequence;
using MotionStep = articulation_interfaces::msg::MotionStep;
using GoalHandle = rclcpp_action::ServerGoalHandle<ExecuteSequence>;
using moveit::planning_interface::MoveGroupInterface;
using moveit::core::MoveItErrorCode;

class MoveItMaster
{
public:
  explicit MoveItMaster(const rclcpp::Node::SharedPtr & node)
  : node_(node), arm_(node, "arm"), gripper_(node, "gripper")
  {
    arm_.setPlanningTime(5.0);
    arm_.setNumPlanningAttempts(5);

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

  MoveItErrorCode runStep(const MotionStep & step)
  {
    switch (step.type) {
      case MotionStep::ARM_POSE:
        arm_.setPoseTarget(step.pose);
        return planAndExecute(arm_);
      case MotionStep::ARM_NAMED:
        arm_.setNamedTarget(step.named_target);
        return planAndExecute(arm_);
      case MotionStep::GRIPPER_NAMED:
        gripper_.setNamedTarget(step.named_target);
        return planAndExecute(gripper_);
      case MotionStep::WAIT:
        rclcpp::sleep_for(std::chrono::milliseconds(static_cast<int64_t>(step.duration * 1000)));
        return MoveItErrorCode::SUCCESS;
      default:
        return MoveItErrorCode::INVALID_MOTION_PLAN;
    }
  }

  void execute(std::shared_ptr<GoalHandle> gh)
  {
    const auto goal = gh->get_goal();
    auto result = std::make_shared<ExecuteSequence::Result>();
    auto feedback = std::make_shared<ExecuteSequence::Feedback>();

    const double vel = goal->velocity_scaling > 0.0 ? goal->velocity_scaling : 0.2;
    arm_.setMaxVelocityScalingFactor(vel);
    arm_.setMaxAccelerationScalingFactor(vel);

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
        result->message = moveit::core::errorCodeToString(ec);
        RCLCPP_ERROR(node_->get_logger(), "step %zu failed: %s", i, result->message.c_str());
        break;
      }
    }
    arm_.clearPoseTargets();

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
  rclcpp_action::Server<ExecuteSequence>::SharedPtr server_;
  std::atomic<bool> busy_{false};
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