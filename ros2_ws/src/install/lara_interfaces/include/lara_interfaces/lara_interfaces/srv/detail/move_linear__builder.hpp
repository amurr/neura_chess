// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from lara_interfaces:srv/MoveLinear.idl
// generated code does not contain a copyright notice

#ifndef LARA_INTERFACES__SRV__DETAIL__MOVE_LINEAR__BUILDER_HPP_
#define LARA_INTERFACES__SRV__DETAIL__MOVE_LINEAR__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "lara_interfaces/srv/detail/move_linear__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace lara_interfaces
{

namespace srv
{

namespace builder
{

class Init_MoveLinear_Request_offset_frame
{
public:
  explicit Init_MoveLinear_Request_offset_frame(::lara_interfaces::srv::MoveLinear_Request & msg)
  : msg_(msg)
  {}
  ::lara_interfaces::srv::MoveLinear_Request offset_frame(::lara_interfaces::srv::MoveLinear_Request::_offset_frame_type arg)
  {
    msg_.offset_frame = std::move(arg);
    return std::move(msg_);
  }

private:
  ::lara_interfaces::srv::MoveLinear_Request msg_;
};

class Init_MoveLinear_Request_use_relative
{
public:
  explicit Init_MoveLinear_Request_use_relative(::lara_interfaces::srv::MoveLinear_Request & msg)
  : msg_(msg)
  {}
  Init_MoveLinear_Request_offset_frame use_relative(::lara_interfaces::srv::MoveLinear_Request::_use_relative_type arg)
  {
    msg_.use_relative = std::move(arg);
    return Init_MoveLinear_Request_offset_frame(msg_);
  }

private:
  ::lara_interfaces::srv::MoveLinear_Request msg_;
};

class Init_MoveLinear_Request_enable_safety
{
public:
  explicit Init_MoveLinear_Request_enable_safety(::lara_interfaces::srv::MoveLinear_Request & msg)
  : msg_(msg)
  {}
  Init_MoveLinear_Request_use_relative enable_safety(::lara_interfaces::srv::MoveLinear_Request::_enable_safety_type arg)
  {
    msg_.enable_safety = std::move(arg);
    return Init_MoveLinear_Request_use_relative(msg_);
  }

private:
  ::lara_interfaces::srv::MoveLinear_Request msg_;
};

class Init_MoveLinear_Request_acceleration
{
public:
  explicit Init_MoveLinear_Request_acceleration(::lara_interfaces::srv::MoveLinear_Request & msg)
  : msg_(msg)
  {}
  Init_MoveLinear_Request_enable_safety acceleration(::lara_interfaces::srv::MoveLinear_Request::_acceleration_type arg)
  {
    msg_.acceleration = std::move(arg);
    return Init_MoveLinear_Request_enable_safety(msg_);
  }

private:
  ::lara_interfaces::srv::MoveLinear_Request msg_;
};

class Init_MoveLinear_Request_speed
{
public:
  explicit Init_MoveLinear_Request_speed(::lara_interfaces::srv::MoveLinear_Request & msg)
  : msg_(msg)
  {}
  Init_MoveLinear_Request_acceleration speed(::lara_interfaces::srv::MoveLinear_Request::_speed_type arg)
  {
    msg_.speed = std::move(arg);
    return Init_MoveLinear_Request_acceleration(msg_);
  }

private:
  ::lara_interfaces::srv::MoveLinear_Request msg_;
};

class Init_MoveLinear_Request_target_pose
{
public:
  Init_MoveLinear_Request_target_pose()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MoveLinear_Request_speed target_pose(::lara_interfaces::srv::MoveLinear_Request::_target_pose_type arg)
  {
    msg_.target_pose = std::move(arg);
    return Init_MoveLinear_Request_speed(msg_);
  }

private:
  ::lara_interfaces::srv::MoveLinear_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::lara_interfaces::srv::MoveLinear_Request>()
{
  return lara_interfaces::srv::builder::Init_MoveLinear_Request_target_pose();
}

}  // namespace lara_interfaces


namespace lara_interfaces
{

namespace srv
{

namespace builder
{

class Init_MoveLinear_Response_message
{
public:
  explicit Init_MoveLinear_Response_message(::lara_interfaces::srv::MoveLinear_Response & msg)
  : msg_(msg)
  {}
  ::lara_interfaces::srv::MoveLinear_Response message(::lara_interfaces::srv::MoveLinear_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::lara_interfaces::srv::MoveLinear_Response msg_;
};

class Init_MoveLinear_Response_success
{
public:
  Init_MoveLinear_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MoveLinear_Response_message success(::lara_interfaces::srv::MoveLinear_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_MoveLinear_Response_message(msg_);
  }

private:
  ::lara_interfaces::srv::MoveLinear_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::lara_interfaces::srv::MoveLinear_Response>()
{
  return lara_interfaces::srv::builder::Init_MoveLinear_Response_success();
}

}  // namespace lara_interfaces

#endif  // LARA_INTERFACES__SRV__DETAIL__MOVE_LINEAR__BUILDER_HPP_
