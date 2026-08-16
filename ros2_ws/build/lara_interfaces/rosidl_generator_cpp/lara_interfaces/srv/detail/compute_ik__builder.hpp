// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from lara_interfaces:srv/ComputeIK.idl
// generated code does not contain a copyright notice

#ifndef LARA_INTERFACES__SRV__DETAIL__COMPUTE_IK__BUILDER_HPP_
#define LARA_INTERFACES__SRV__DETAIL__COMPUTE_IK__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "lara_interfaces/srv/detail/compute_ik__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace lara_interfaces
{

namespace srv
{

namespace builder
{

class Init_ComputeIK_Request_enforce_joint_limits_mode
{
public:
  explicit Init_ComputeIK_Request_enforce_joint_limits_mode(::lara_interfaces::srv::ComputeIK_Request & msg)
  : msg_(msg)
  {}
  ::lara_interfaces::srv::ComputeIK_Request enforce_joint_limits_mode(::lara_interfaces::srv::ComputeIK_Request::_enforce_joint_limits_mode_type arg)
  {
    msg_.enforce_joint_limits_mode = std::move(arg);
    return std::move(msg_);
  }

private:
  ::lara_interfaces::srv::ComputeIK_Request msg_;
};

class Init_ComputeIK_Request_orientation_tolerance
{
public:
  explicit Init_ComputeIK_Request_orientation_tolerance(::lara_interfaces::srv::ComputeIK_Request & msg)
  : msg_(msg)
  {}
  Init_ComputeIK_Request_enforce_joint_limits_mode orientation_tolerance(::lara_interfaces::srv::ComputeIK_Request::_orientation_tolerance_type arg)
  {
    msg_.orientation_tolerance = std::move(arg);
    return Init_ComputeIK_Request_enforce_joint_limits_mode(msg_);
  }

private:
  ::lara_interfaces::srv::ComputeIK_Request msg_;
};

class Init_ComputeIK_Request_position_tolerance
{
public:
  explicit Init_ComputeIK_Request_position_tolerance(::lara_interfaces::srv::ComputeIK_Request & msg)
  : msg_(msg)
  {}
  Init_ComputeIK_Request_orientation_tolerance position_tolerance(::lara_interfaces::srv::ComputeIK_Request::_position_tolerance_type arg)
  {
    msg_.position_tolerance = std::move(arg);
    return Init_ComputeIK_Request_orientation_tolerance(msg_);
  }

private:
  ::lara_interfaces::srv::ComputeIK_Request msg_;
};

class Init_ComputeIK_Request_timeout_sec
{
public:
  explicit Init_ComputeIK_Request_timeout_sec(::lara_interfaces::srv::ComputeIK_Request & msg)
  : msg_(msg)
  {}
  Init_ComputeIK_Request_position_tolerance timeout_sec(::lara_interfaces::srv::ComputeIK_Request::_timeout_sec_type arg)
  {
    msg_.timeout_sec = std::move(arg);
    return Init_ComputeIK_Request_position_tolerance(msg_);
  }

private:
  ::lara_interfaces::srv::ComputeIK_Request msg_;
};

class Init_ComputeIK_Request_seed_joint_positions
{
public:
  explicit Init_ComputeIK_Request_seed_joint_positions(::lara_interfaces::srv::ComputeIK_Request & msg)
  : msg_(msg)
  {}
  Init_ComputeIK_Request_timeout_sec seed_joint_positions(::lara_interfaces::srv::ComputeIK_Request::_seed_joint_positions_type arg)
  {
    msg_.seed_joint_positions = std::move(arg);
    return Init_ComputeIK_Request_timeout_sec(msg_);
  }

private:
  ::lara_interfaces::srv::ComputeIK_Request msg_;
};

class Init_ComputeIK_Request_target_pose
{
public:
  Init_ComputeIK_Request_target_pose()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ComputeIK_Request_seed_joint_positions target_pose(::lara_interfaces::srv::ComputeIK_Request::_target_pose_type arg)
  {
    msg_.target_pose = std::move(arg);
    return Init_ComputeIK_Request_seed_joint_positions(msg_);
  }

private:
  ::lara_interfaces::srv::ComputeIK_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::lara_interfaces::srv::ComputeIK_Request>()
{
  return lara_interfaces::srv::builder::Init_ComputeIK_Request_target_pose();
}

}  // namespace lara_interfaces


namespace lara_interfaces
{

namespace srv
{

namespace builder
{

class Init_ComputeIK_Response_iterations
{
public:
  explicit Init_ComputeIK_Response_iterations(::lara_interfaces::srv::ComputeIK_Response & msg)
  : msg_(msg)
  {}
  ::lara_interfaces::srv::ComputeIK_Response iterations(::lara_interfaces::srv::ComputeIK_Response::_iterations_type arg)
  {
    msg_.iterations = std::move(arg);
    return std::move(msg_);
  }

private:
  ::lara_interfaces::srv::ComputeIK_Response msg_;
};

class Init_ComputeIK_Response_orientation_error
{
public:
  explicit Init_ComputeIK_Response_orientation_error(::lara_interfaces::srv::ComputeIK_Response & msg)
  : msg_(msg)
  {}
  Init_ComputeIK_Response_iterations orientation_error(::lara_interfaces::srv::ComputeIK_Response::_orientation_error_type arg)
  {
    msg_.orientation_error = std::move(arg);
    return Init_ComputeIK_Response_iterations(msg_);
  }

private:
  ::lara_interfaces::srv::ComputeIK_Response msg_;
};

class Init_ComputeIK_Response_position_error
{
public:
  explicit Init_ComputeIK_Response_position_error(::lara_interfaces::srv::ComputeIK_Response & msg)
  : msg_(msg)
  {}
  Init_ComputeIK_Response_orientation_error position_error(::lara_interfaces::srv::ComputeIK_Response::_position_error_type arg)
  {
    msg_.position_error = std::move(arg);
    return Init_ComputeIK_Response_orientation_error(msg_);
  }

private:
  ::lara_interfaces::srv::ComputeIK_Response msg_;
};

class Init_ComputeIK_Response_joint_positions
{
public:
  explicit Init_ComputeIK_Response_joint_positions(::lara_interfaces::srv::ComputeIK_Response & msg)
  : msg_(msg)
  {}
  Init_ComputeIK_Response_position_error joint_positions(::lara_interfaces::srv::ComputeIK_Response::_joint_positions_type arg)
  {
    msg_.joint_positions = std::move(arg);
    return Init_ComputeIK_Response_position_error(msg_);
  }

private:
  ::lara_interfaces::srv::ComputeIK_Response msg_;
};

class Init_ComputeIK_Response_joint_names
{
public:
  explicit Init_ComputeIK_Response_joint_names(::lara_interfaces::srv::ComputeIK_Response & msg)
  : msg_(msg)
  {}
  Init_ComputeIK_Response_joint_positions joint_names(::lara_interfaces::srv::ComputeIK_Response::_joint_names_type arg)
  {
    msg_.joint_names = std::move(arg);
    return Init_ComputeIK_Response_joint_positions(msg_);
  }

private:
  ::lara_interfaces::srv::ComputeIK_Response msg_;
};

class Init_ComputeIK_Response_message
{
public:
  explicit Init_ComputeIK_Response_message(::lara_interfaces::srv::ComputeIK_Response & msg)
  : msg_(msg)
  {}
  Init_ComputeIK_Response_joint_names message(::lara_interfaces::srv::ComputeIK_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return Init_ComputeIK_Response_joint_names(msg_);
  }

private:
  ::lara_interfaces::srv::ComputeIK_Response msg_;
};

class Init_ComputeIK_Response_success
{
public:
  Init_ComputeIK_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ComputeIK_Response_message success(::lara_interfaces::srv::ComputeIK_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_ComputeIK_Response_message(msg_);
  }

private:
  ::lara_interfaces::srv::ComputeIK_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::lara_interfaces::srv::ComputeIK_Response>()
{
  return lara_interfaces::srv::builder::Init_ComputeIK_Response_success();
}

}  // namespace lara_interfaces

#endif  // LARA_INTERFACES__SRV__DETAIL__COMPUTE_IK__BUILDER_HPP_
