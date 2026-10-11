// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from moveit_master:msg/MotionStep.idl
// generated code does not contain a copyright notice

#ifndef MOVEIT_MASTER__MSG__DETAIL__MOTION_STEP__BUILDER_HPP_
#define MOVEIT_MASTER__MSG__DETAIL__MOTION_STEP__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "moveit_master/msg/detail/motion_step__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace moveit_master
{

namespace msg
{

namespace builder
{

class Init_MotionStep_allow
{
public:
  explicit Init_MotionStep_allow(::moveit_master::msg::MotionStep & msg)
  : msg_(msg)
  {}
  ::moveit_master::msg::MotionStep allow(::moveit_master::msg::MotionStep::_allow_type arg)
  {
    msg_.allow = std::move(arg);
    return std::move(msg_);
  }

private:
  ::moveit_master::msg::MotionStep msg_;
};

class Init_MotionStep_touch_links
{
public:
  explicit Init_MotionStep_touch_links(::moveit_master::msg::MotionStep & msg)
  : msg_(msg)
  {}
  Init_MotionStep_allow touch_links(::moveit_master::msg::MotionStep::_touch_links_type arg)
  {
    msg_.touch_links = std::move(arg);
    return Init_MotionStep_allow(msg_);
  }

private:
  ::moveit_master::msg::MotionStep msg_;
};

class Init_MotionStep_object_id
{
public:
  explicit Init_MotionStep_object_id(::moveit_master::msg::MotionStep & msg)
  : msg_(msg)
  {}
  Init_MotionStep_touch_links object_id(::moveit_master::msg::MotionStep::_object_id_type arg)
  {
    msg_.object_id = std::move(arg);
    return Init_MotionStep_touch_links(msg_);
  }

private:
  ::moveit_master::msg::MotionStep msg_;
};

class Init_MotionStep_offset
{
public:
  explicit Init_MotionStep_offset(::moveit_master::msg::MotionStep & msg)
  : msg_(msg)
  {}
  Init_MotionStep_object_id offset(::moveit_master::msg::MotionStep::_offset_type arg)
  {
    msg_.offset = std::move(arg);
    return Init_MotionStep_object_id(msg_);
  }

private:
  ::moveit_master::msg::MotionStep msg_;
};

class Init_MotionStep_joint_value
{
public:
  explicit Init_MotionStep_joint_value(::moveit_master::msg::MotionStep & msg)
  : msg_(msg)
  {}
  Init_MotionStep_offset joint_value(::moveit_master::msg::MotionStep::_joint_value_type arg)
  {
    msg_.joint_value = std::move(arg);
    return Init_MotionStep_offset(msg_);
  }

private:
  ::moveit_master::msg::MotionStep msg_;
};

class Init_MotionStep_duration
{
public:
  explicit Init_MotionStep_duration(::moveit_master::msg::MotionStep & msg)
  : msg_(msg)
  {}
  Init_MotionStep_joint_value duration(::moveit_master::msg::MotionStep::_duration_type arg)
  {
    msg_.duration = std::move(arg);
    return Init_MotionStep_joint_value(msg_);
  }

private:
  ::moveit_master::msg::MotionStep msg_;
};

class Init_MotionStep_named_target
{
public:
  explicit Init_MotionStep_named_target(::moveit_master::msg::MotionStep & msg)
  : msg_(msg)
  {}
  Init_MotionStep_duration named_target(::moveit_master::msg::MotionStep::_named_target_type arg)
  {
    msg_.named_target = std::move(arg);
    return Init_MotionStep_duration(msg_);
  }

private:
  ::moveit_master::msg::MotionStep msg_;
};

class Init_MotionStep_pose
{
public:
  explicit Init_MotionStep_pose(::moveit_master::msg::MotionStep & msg)
  : msg_(msg)
  {}
  Init_MotionStep_named_target pose(::moveit_master::msg::MotionStep::_pose_type arg)
  {
    msg_.pose = std::move(arg);
    return Init_MotionStep_named_target(msg_);
  }

private:
  ::moveit_master::msg::MotionStep msg_;
};

class Init_MotionStep_type
{
public:
  Init_MotionStep_type()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MotionStep_pose type(::moveit_master::msg::MotionStep::_type_type arg)
  {
    msg_.type = std::move(arg);
    return Init_MotionStep_pose(msg_);
  }

private:
  ::moveit_master::msg::MotionStep msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::moveit_master::msg::MotionStep>()
{
  return moveit_master::msg::builder::Init_MotionStep_type();
}

}  // namespace moveit_master

#endif  // MOVEIT_MASTER__MSG__DETAIL__MOTION_STEP__BUILDER_HPP_
