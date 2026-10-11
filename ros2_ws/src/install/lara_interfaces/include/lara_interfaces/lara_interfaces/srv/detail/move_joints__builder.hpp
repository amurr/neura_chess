// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from lara_interfaces:srv/MoveJoints.idl
// generated code does not contain a copyright notice

#ifndef LARA_INTERFACES__SRV__DETAIL__MOVE_JOINTS__BUILDER_HPP_
#define LARA_INTERFACES__SRV__DETAIL__MOVE_JOINTS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "lara_interfaces/srv/detail/move_joints__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace lara_interfaces
{

namespace srv
{

namespace builder
{

class Init_MoveJoints_Request_enable_safety
{
public:
  explicit Init_MoveJoints_Request_enable_safety(::lara_interfaces::srv::MoveJoints_Request & msg)
  : msg_(msg)
  {}
  ::lara_interfaces::srv::MoveJoints_Request enable_safety(::lara_interfaces::srv::MoveJoints_Request::_enable_safety_type arg)
  {
    msg_.enable_safety = std::move(arg);
    return std::move(msg_);
  }

private:
  ::lara_interfaces::srv::MoveJoints_Request msg_;
};

class Init_MoveJoints_Request_acceleration
{
public:
  explicit Init_MoveJoints_Request_acceleration(::lara_interfaces::srv::MoveJoints_Request & msg)
  : msg_(msg)
  {}
  Init_MoveJoints_Request_enable_safety acceleration(::lara_interfaces::srv::MoveJoints_Request::_acceleration_type arg)
  {
    msg_.acceleration = std::move(arg);
    return Init_MoveJoints_Request_enable_safety(msg_);
  }

private:
  ::lara_interfaces::srv::MoveJoints_Request msg_;
};

class Init_MoveJoints_Request_speed
{
public:
  explicit Init_MoveJoints_Request_speed(::lara_interfaces::srv::MoveJoints_Request & msg)
  : msg_(msg)
  {}
  Init_MoveJoints_Request_acceleration speed(::lara_interfaces::srv::MoveJoints_Request::_speed_type arg)
  {
    msg_.speed = std::move(arg);
    return Init_MoveJoints_Request_acceleration(msg_);
  }

private:
  ::lara_interfaces::srv::MoveJoints_Request msg_;
};

class Init_MoveJoints_Request_target_pose
{
public:
  explicit Init_MoveJoints_Request_target_pose(::lara_interfaces::srv::MoveJoints_Request & msg)
  : msg_(msg)
  {}
  Init_MoveJoints_Request_speed target_pose(::lara_interfaces::srv::MoveJoints_Request::_target_pose_type arg)
  {
    msg_.target_pose = std::move(arg);
    return Init_MoveJoints_Request_speed(msg_);
  }

private:
  ::lara_interfaces::srv::MoveJoints_Request msg_;
};

class Init_MoveJoints_Request_target_joint
{
public:
  explicit Init_MoveJoints_Request_target_joint(::lara_interfaces::srv::MoveJoints_Request & msg)
  : msg_(msg)
  {}
  Init_MoveJoints_Request_target_pose target_joint(::lara_interfaces::srv::MoveJoints_Request::_target_joint_type arg)
  {
    msg_.target_joint = std::move(arg);
    return Init_MoveJoints_Request_target_pose(msg_);
  }

private:
  ::lara_interfaces::srv::MoveJoints_Request msg_;
};

class Init_MoveJoints_Request_point_name
{
public:
  Init_MoveJoints_Request_point_name()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MoveJoints_Request_target_joint point_name(::lara_interfaces::srv::MoveJoints_Request::_point_name_type arg)
  {
    msg_.point_name = std::move(arg);
    return Init_MoveJoints_Request_target_joint(msg_);
  }

private:
  ::lara_interfaces::srv::MoveJoints_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::lara_interfaces::srv::MoveJoints_Request>()
{
  return lara_interfaces::srv::builder::Init_MoveJoints_Request_point_name();
}

}  // namespace lara_interfaces


namespace lara_interfaces
{

namespace srv
{

namespace builder
{

class Init_MoveJoints_Response_message
{
public:
  explicit Init_MoveJoints_Response_message(::lara_interfaces::srv::MoveJoints_Response & msg)
  : msg_(msg)
  {}
  ::lara_interfaces::srv::MoveJoints_Response message(::lara_interfaces::srv::MoveJoints_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::lara_interfaces::srv::MoveJoints_Response msg_;
};

class Init_MoveJoints_Response_success
{
public:
  Init_MoveJoints_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MoveJoints_Response_message success(::lara_interfaces::srv::MoveJoints_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_MoveJoints_Response_message(msg_);
  }

private:
  ::lara_interfaces::srv::MoveJoints_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::lara_interfaces::srv::MoveJoints_Response>()
{
  return lara_interfaces::srv::builder::Init_MoveJoints_Response_success();
}

}  // namespace lara_interfaces

#endif  // LARA_INTERFACES__SRV__DETAIL__MOVE_JOINTS__BUILDER_HPP_
