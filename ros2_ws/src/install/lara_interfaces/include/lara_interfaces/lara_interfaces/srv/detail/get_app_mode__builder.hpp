// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from lara_interfaces:srv/GetAppMode.idl
// generated code does not contain a copyright notice

#ifndef LARA_INTERFACES__SRV__DETAIL__GET_APP_MODE__BUILDER_HPP_
#define LARA_INTERFACES__SRV__DETAIL__GET_APP_MODE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "lara_interfaces/srv/detail/get_app_mode__struct.hpp"
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
auto build<::lara_interfaces::srv::GetAppMode_Request>()
{
  return ::lara_interfaces::srv::GetAppMode_Request(rosidl_runtime_cpp::MessageInitialization::ZERO);
}

}  // namespace lara_interfaces


namespace lara_interfaces
{

namespace srv
{

namespace builder
{

class Init_GetAppMode_Response_mode
{
public:
  Init_GetAppMode_Response_mode()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::lara_interfaces::srv::GetAppMode_Response mode(::lara_interfaces::srv::GetAppMode_Response::_mode_type arg)
  {
    msg_.mode = std::move(arg);
    return std::move(msg_);
  }

private:
  ::lara_interfaces::srv::GetAppMode_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::lara_interfaces::srv::GetAppMode_Response>()
{
  return lara_interfaces::srv::builder::Init_GetAppMode_Response_mode();
}

}  // namespace lara_interfaces

#endif  // LARA_INTERFACES__SRV__DETAIL__GET_APP_MODE__BUILDER_HPP_
