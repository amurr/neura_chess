// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from lara_interfaces:msg/XyzRpyGoal.idl
// generated code does not contain a copyright notice

#ifndef LARA_INTERFACES__MSG__DETAIL__XYZ_RPY_GOAL__BUILDER_HPP_
#define LARA_INTERFACES__MSG__DETAIL__XYZ_RPY_GOAL__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "lara_interfaces/msg/detail/xyz_rpy_goal__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace lara_interfaces
{

namespace msg
{

namespace builder
{

class Init_XyzRpyGoal_use_orientation
{
public:
  explicit Init_XyzRpyGoal_use_orientation(::lara_interfaces::msg::XyzRpyGoal & msg)
  : msg_(msg)
  {}
  ::lara_interfaces::msg::XyzRpyGoal use_orientation(::lara_interfaces::msg::XyzRpyGoal::_use_orientation_type arg)
  {
    msg_.use_orientation = std::move(arg);
    return std::move(msg_);
  }

private:
  ::lara_interfaces::msg::XyzRpyGoal msg_;
};

class Init_XyzRpyGoal_yaw
{
public:
  explicit Init_XyzRpyGoal_yaw(::lara_interfaces::msg::XyzRpyGoal & msg)
  : msg_(msg)
  {}
  Init_XyzRpyGoal_use_orientation yaw(::lara_interfaces::msg::XyzRpyGoal::_yaw_type arg)
  {
    msg_.yaw = std::move(arg);
    return Init_XyzRpyGoal_use_orientation(msg_);
  }

private:
  ::lara_interfaces::msg::XyzRpyGoal msg_;
};

class Init_XyzRpyGoal_pitch
{
public:
  explicit Init_XyzRpyGoal_pitch(::lara_interfaces::msg::XyzRpyGoal & msg)
  : msg_(msg)
  {}
  Init_XyzRpyGoal_yaw pitch(::lara_interfaces::msg::XyzRpyGoal::_pitch_type arg)
  {
    msg_.pitch = std::move(arg);
    return Init_XyzRpyGoal_yaw(msg_);
  }

private:
  ::lara_interfaces::msg::XyzRpyGoal msg_;
};

class Init_XyzRpyGoal_roll
{
public:
  explicit Init_XyzRpyGoal_roll(::lara_interfaces::msg::XyzRpyGoal & msg)
  : msg_(msg)
  {}
  Init_XyzRpyGoal_pitch roll(::lara_interfaces::msg::XyzRpyGoal::_roll_type arg)
  {
    msg_.roll = std::move(arg);
    return Init_XyzRpyGoal_pitch(msg_);
  }

private:
  ::lara_interfaces::msg::XyzRpyGoal msg_;
};

class Init_XyzRpyGoal_z
{
public:
  explicit Init_XyzRpyGoal_z(::lara_interfaces::msg::XyzRpyGoal & msg)
  : msg_(msg)
  {}
  Init_XyzRpyGoal_roll z(::lara_interfaces::msg::XyzRpyGoal::_z_type arg)
  {
    msg_.z = std::move(arg);
    return Init_XyzRpyGoal_roll(msg_);
  }

private:
  ::lara_interfaces::msg::XyzRpyGoal msg_;
};

class Init_XyzRpyGoal_y
{
public:
  explicit Init_XyzRpyGoal_y(::lara_interfaces::msg::XyzRpyGoal & msg)
  : msg_(msg)
  {}
  Init_XyzRpyGoal_z y(::lara_interfaces::msg::XyzRpyGoal::_y_type arg)
  {
    msg_.y = std::move(arg);
    return Init_XyzRpyGoal_z(msg_);
  }

private:
  ::lara_interfaces::msg::XyzRpyGoal msg_;
};

class Init_XyzRpyGoal_x
{
public:
  Init_XyzRpyGoal_x()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_XyzRpyGoal_y x(::lara_interfaces::msg::XyzRpyGoal::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_XyzRpyGoal_y(msg_);
  }

private:
  ::lara_interfaces::msg::XyzRpyGoal msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::lara_interfaces::msg::XyzRpyGoal>()
{
  return lara_interfaces::msg::builder::Init_XyzRpyGoal_x();
}

}  // namespace lara_interfaces

#endif  // LARA_INTERFACES__MSG__DETAIL__XYZ_RPY_GOAL__BUILDER_HPP_
