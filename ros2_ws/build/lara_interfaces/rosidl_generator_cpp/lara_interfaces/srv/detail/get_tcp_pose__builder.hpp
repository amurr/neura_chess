// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from lara_interfaces:srv/GetTCPPose.idl
// generated code does not contain a copyright notice

#ifndef LARA_INTERFACES__SRV__DETAIL__GET_TCP_POSE__BUILDER_HPP_
#define LARA_INTERFACES__SRV__DETAIL__GET_TCP_POSE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "lara_interfaces/srv/detail/get_tcp_pose__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace lara_interfaces
{

namespace srv
{


}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::lara_interfaces::srv::GetTCPPose_Request>()
{
  return ::lara_interfaces::srv::GetTCPPose_Request(rosidl_runtime_cpp::MessageInitialization::ZERO);
}

}  // namespace lara_interfaces


namespace lara_interfaces
{

namespace srv
{

namespace builder
{

class Init_GetTCPPose_Response_pose
{
public:
  Init_GetTCPPose_Response_pose()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::lara_interfaces::srv::GetTCPPose_Response pose(::lara_interfaces::srv::GetTCPPose_Response::_pose_type arg)
  {
    msg_.pose = std::move(arg);
    return std::move(msg_);
  }

private:
  ::lara_interfaces::srv::GetTCPPose_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::lara_interfaces::srv::GetTCPPose_Response>()
{
  return lara_interfaces::srv::builder::Init_GetTCPPose_Response_pose();
}

}  // namespace lara_interfaces

#endif  // LARA_INTERFACES__SRV__DETAIL__GET_TCP_POSE__BUILDER_HPP_
