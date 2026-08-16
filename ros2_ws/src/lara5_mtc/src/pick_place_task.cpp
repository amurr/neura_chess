#include "lara5_mtc/pick_place_task.hpp"

#include <cmath>
#include <memory>
#include <stdexcept>
#include <vector>

#include <Eigen/Geometry>
#include <geometry_msgs/msg/vector3_stamped.hpp>
#include <moveit/robot_model/robot_model.h>
#include <moveit/robot_state/robot_state.h>
#include <moveit/task_constructor/solvers.h>
#include <moveit/task_constructor/stages.h>
#include <moveit/task_constructor/stages/move_relative.h>
#include <tf2_eigen/tf2_eigen.hpp>
#include <tf2_geometry_msgs/tf2_geometry_msgs.hpp>

#include "lara5_mtc/chess_occupancy.hpp"

namespace mtc = moveit::task_constructor;

namespace lara5_mtc
{
namespace
{

geometry_msgs::msg::PoseStamped makeIkFrame(const std::string& eef_link)
{
  geometry_msgs::msg::PoseStamped ik_frame;
  ik_frame.header.frame_id = eef_link;
  ik_frame.pose.orientation.w = 1.0;
  return ik_frame;
}

std::vector<std::string> gripperCollisionLinks(const moveit::core::RobotModelConstPtr& model,
                                               const std::string& gripper_group)
{
  return model->getJointModelGroup(gripper_group)->getLinkModelNamesWithCollisionGeometry();
}

moveit::core::RobotState namedArmState(const moveit::core::RobotModelConstPtr& model,
                                       const std::string& arm_group, const std::string& named)
{
  moveit::core::RobotState state(model);
  state.setToDefaultValues();
  state.setToDefaultValues(model->getJointModelGroup(arm_group), named);
  state.update();
  return state;
}

std::unique_ptr<mtc::stages::ModifyPlanningScene>
makeAllowPieceCollisions(const std::string& name, const std::string& object_id,
                         const moveit::core::RobotModelConstPtr& model, const std::string& gripper_group)
{
  auto stage = std::make_unique<mtc::stages::ModifyPlanningScene>(name);
  stage->allowCollisions(object_id, gripperCollisionLinks(model, gripper_group), true);
  return stage;
}

std::unique_ptr<mtc::stages::ModifyPlanningScene>
makeAllowGripperBoardCollisions(const moveit::core::RobotModelConstPtr& model, const std::string& gripper_group)
{
  auto stage = std::make_unique<mtc::stages::ModifyPlanningScene>("allow gripper on board squares");
  const auto links = gripperCollisionLinks(model, gripper_group);
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
makeAllowGripperAllPieceCollisions(const moveit::core::RobotModelConstPtr& model, const std::string& gripper_group)
{
  auto stage = std::make_unique<mtc::stages::ModifyPlanningScene>("allow gripper on all pieces");
  const auto links = gripperCollisionLinks(model, gripper_group);
  for (const char file : { 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h' })
  {
    for (const char rank : { '1', '2', '3', '4', '5', '6', '7', '8' })
    {
      const std::string object_id = pieceObjectId(std::string(1, file) + rank);
      stage->allowCollisions(object_id, true);
      stage->allowCollisions(object_id, links, true);
    }
  }
  return stage;
}

std::unique_ptr<mtc::stages::ModifyPlanningScene>
makeAllowReleaseCollisions(const std::string& object_id, const std::string& target_square,
                           const moveit::core::RobotModelConstPtr& model, const std::string& gripper_group)
{
  auto stage = std::make_unique<mtc::stages::ModifyPlanningScene>("allow release collisions");
  const std::string board_id = "board_sq_" + target_square;
  const auto gripper_links = gripperCollisionLinks(model, gripper_group);
  stage->allowCollisions(object_id, true);
  stage->allowCollisions(object_id, board_id, true);
  stage->allowCollisions(object_id, gripper_links, true);
  stage->allowCollisions(board_id, gripper_links, true);
  return stage;
}

std::unique_ptr<mtc::stages::ModifyPlanningScene>
makeAllowArmOtherPieceCollisions(const std::string& source_square, const moveit::core::RobotModelConstPtr& model,
                                 const std::string& arm_group)
{
  auto stage = std::make_unique<mtc::stages::ModifyPlanningScene>("allow arm on other pieces");
  const auto arm_links = model->getJointModelGroup(arm_group)->getLinkModelNamesWithCollisionGeometry();
  for (const char file : { 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h' })
  {
    for (const char rank : { '1', '2', '3', '4', '5', '6', '7', '8' })
    {
      const std::string square = std::string(1, file) + rank;
      if (square == source_square)
      {
        continue;
      }
      stage->allowCollisions(pieceObjectId(square), arm_links, true);
    }
  }
  return stage;
}

std::unique_ptr<mtc::stages::MoveRelative>
makeAxisMove(const std::string& name, const mtc::solvers::PlannerInterfacePtr& planner, const std::string& frame_id,
             const std::string& eef_link, const double dx, const double dy, const double dz,
             const mtc::PropagatingEitherWay::Direction propagation)
{
  const double dist = std::sqrt(dx * dx + dy * dy + dz * dz);
  if (dist < 1e-4)
  {
    return nullptr;
  }

  auto stage = std::make_unique<mtc::stages::MoveRelative>(name, planner);
  stage->properties().configureInitFrom(mtc::Stage::PARENT, { "group" });
  stage->setIKFrame(makeIkFrame(eef_link));
  stage->setMinMaxDistance(std::min(0.001, dist * 0.05), dist);

  geometry_msgs::msg::Vector3Stamped direction;
  direction.header.frame_id = frame_id;
  direction.vector.x = dx / dist;
  direction.vector.y = dy / dist;
  direction.vector.z = dz / dist;
  stage->setDirection(direction);
  stage->restrictDirection(propagation);
  return stage;
}

void addCartesianDelta(mtc::Task& task, const std::string& name, const mtc::solvers::PlannerInterfacePtr& planner,
                       const std::string& world_frame, const std::string& eef_link, const double dx, const double dy,
                       const double dz)
{
  if (auto stage = makeAxisMove(name, planner, world_frame, eef_link, dx, dy, dz, mtc::PropagatingEitherWay::FORWARD))
  {
    task.add(std::move(stage));
  }
}

void addMoveArmToPose(mtc::Task& task, const std::string& name, const mtc::solvers::PlannerInterfacePtr& planner,
                      const std::string& arm_group, const geometry_msgs::msg::PoseStamped& target)
{
  auto stage = std::make_unique<mtc::stages::MoveTo>(name, planner);
  stage->setGroup(arm_group);
  stage->setGoal(target);
  task.add(std::move(stage));
}

void addMoveArmToNamed(mtc::Task& task, const std::string& name, const mtc::solvers::PlannerInterfacePtr& planner,
                       const std::string& arm_group, const std::string& goal)
{
  auto stage = std::make_unique<mtc::stages::MoveTo>(name, planner);
  stage->setGroup(arm_group);
  stage->setGoal(goal);
  stage->restrictDirection(mtc::PropagatingEitherWay::FORWARD);
  task.add(std::move(stage));
}

void addApproachAlong(mtc::Task& task, const std::string& name, const mtc::solvers::PlannerInterfacePtr& planner,
                      const PickPlaceRequest& req, const double distance_m, const double eef_z_sign,
                      const double world_z_sign)
{
  std::unique_ptr<mtc::stages::MoveRelative> stage;
  if (req.approach_frame == "world")
  {
    stage = makeAxisMove(name, planner, req.world_frame, req.eef_link, 0.0, 0.0, world_z_sign * distance_m,
                         mtc::PropagatingEitherWay::FORWARD);
  }
  else
  {
    stage = makeAxisMove(name, planner, req.eef_link, req.eef_link, 0.0, 0.0, eef_z_sign * distance_m,
                         mtc::PropagatingEitherWay::FORWARD);
  }
  if (stage)
  {
    task.add(std::move(stage));
  }
}

}  // namespace

geometry_msgs::msg::PoseStamped hoverFromGrasp(const geometry_msgs::msg::PoseStamped& grasp, const double approach_m)
{
  Eigen::Isometry3d iso;
  tf2::fromMsg(grasp.pose, iso);
  iso.translation() -= approach_m * (iso.rotation() * Eigen::Vector3d::UnitZ());
  geometry_msgs::msg::PoseStamped hover = grasp;
  hover.pose = tf2::toMsg(iso);
  return hover;
}

void populatePickPlaceTask(mtc::Task& task, const PickPlaceRequest& req, const rclcpp::Node::SharedPtr& node)
{
  if (req.seed_pose.empty())
  {
    throw std::runtime_error("chess_seed_pose is required (e.g. pre_pick)");
  }

  task.stages()->setName("pick_" + req.object_id);
  task.setProperty("group", req.arm_group);
  task.setProperty("eef", req.eef_link);

  const auto joint_planner = std::make_shared<mtc::solvers::JointInterpolationPlanner>();
  auto pipeline_planner = std::make_shared<mtc::solvers::PipelinePlanner>(node, "ompl");
  auto cartesian_planner = std::make_shared<mtc::solvers::CartesianPath>();
  cartesian_planner->setMaxVelocityScalingFactor(1.0);
  cartesian_planner->setMaxAccelerationScalingFactor(1.0);
  cartesian_planner->setStepSize(0.005);
  cartesian_planner->setMinFraction(0.05);
  const mtc::solvers::PlannerInterfacePtr arm_planner = pipeline_planner;

  const geometry_msgs::msg::PoseStamped pick_hover = hoverFromGrasp(req.pick_grasp, req.approach_m);
  const geometry_msgs::msg::PoseStamped place_hover = hoverFromGrasp(req.place_grasp, req.approach_m);

  {
    auto current = std::make_unique<mtc::stages::CurrentState>("current state");
    current->properties().set("timeout", req.planning_scene_timeout_s);
    task.add(std::move(current));
  }

  {
    auto stage = std::make_unique<mtc::stages::MoveTo>("open gripper", joint_planner);
    stage->setGroup(req.gripper_group);
    stage->setGoal(req.gripper_open);
    task.add(std::move(stage));
  }

  {
    auto stage = std::make_unique<mtc::stages::MoveTo>("seed arm", joint_planner);
    stage->setGroup(req.arm_group);
    stage->setGoal(req.seed_pose);
    stage->restrictDirection(mtc::PropagatingEitherWay::FORWARD);
    task.add(std::move(stage));
  }

  const auto model = task.getRobotModel();
  task.add(makeAllowPieceCollisions("allow collision (gripper,piece)", req.object_id, model, req.gripper_group));
  task.add(makeAllowGripperBoardCollisions(model, req.gripper_group));
  task.add(makeAllowGripperAllPieceCollisions(model, req.gripper_group));
  task.add(makeAllowArmOtherPieceCollisions(req.source_square, model, req.arm_group));

  if (req.hover_mode == "cartesian")
  {
    const moveit::core::RobotState seed_state = namedArmState(model, req.arm_group, req.seed_pose);
    const auto& seed_tf = seed_state.getGlobalLinkTransform(req.eef_link);
    addCartesianDelta(task, "pick hover", cartesian_planner, req.world_frame, req.eef_link,
                      pick_hover.pose.position.x - seed_tf.translation().x(),
                      pick_hover.pose.position.y - seed_tf.translation().y(),
                      pick_hover.pose.position.z - seed_tf.translation().z());
  }
  else
  {
    addMoveArmToPose(task, "pick hover", arm_planner, req.arm_group, pick_hover);
  }

  addApproachAlong(task, "approach pick", cartesian_planner, req, req.approach_m, /*eef_z*/ 1.0, /*world_z*/ -1.0);

  {
    auto stage = std::make_unique<mtc::stages::MoveTo>("close gripper", joint_planner);
    stage->setGroup(req.gripper_group);
    stage->setGoal(req.gripper_close);
    task.add(std::move(stage));
  }
  {
    auto attach = std::make_unique<mtc::stages::ModifyPlanningScene>("attach piece");
    attach->attachObject(req.object_id, req.eef_link);
    task.add(std::move(attach));
  }
  addApproachAlong(task, "lift from pick", cartesian_planner, req, req.lift_m, /*eef_z*/ -1.0, /*world_z*/ 1.0);

  if (req.hover_mode == "cartesian")
  {
    addCartesianDelta(task, "place hover slide", cartesian_planner, req.world_frame, req.eef_link,
                      place_hover.pose.position.x - pick_hover.pose.position.x,
                      place_hover.pose.position.y - pick_hover.pose.position.y,
                      place_hover.pose.position.z - pick_hover.pose.position.z);
  }
  else
  {
    addMoveArmToPose(task, "place hover", arm_planner, req.arm_group, place_hover);
  }

  addApproachAlong(task, "descend place", cartesian_planner, req, req.approach_m, /*eef_z*/ 1.0, /*world_z*/ -1.0);
  task.add(makeAllowReleaseCollisions(req.object_id, req.target_square, model, req.gripper_group));
  {
    auto detach = std::make_unique<mtc::stages::ModifyPlanningScene>("detach piece");
    detach->detachObject(req.object_id, req.eef_link);
    task.add(std::move(detach));
  }
  addApproachAlong(task, "retreat after place", cartesian_planner, req, req.approach_m, /*eef_z*/ -1.0,
                   /*world_z*/ 1.0);
  {
    auto stage = std::make_unique<mtc::stages::MoveTo>("open gripper after place", joint_planner);
    stage->setGroup(req.gripper_group);
    stage->setGoal(req.gripper_open);
    task.add(std::move(stage));
  }

  addMoveArmToNamed(task, "move to stand", arm_planner, req.arm_group, req.home_pose);
}

}  // namespace lara5_mtc
