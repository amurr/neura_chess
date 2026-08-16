// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from lara_interfaces:srv/GetTCPPose.idl
// generated code does not contain a copyright notice

#ifndef LARA_INTERFACES__SRV__DETAIL__GET_TCP_POSE__TRAITS_HPP_
#define LARA_INTERFACES__SRV__DETAIL__GET_TCP_POSE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "lara_interfaces/srv/detail/get_tcp_pose__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace lara_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const GetTCPPose_Request & msg,
  std::ostream & out)
{
  (void)msg;
  out << "null";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const GetTCPPose_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  (void)msg;
  (void)indentation;
  out << "null\n";
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const GetTCPPose_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace lara_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use lara_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const lara_interfaces::srv::GetTCPPose_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  lara_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use lara_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const lara_interfaces::srv::GetTCPPose_Request & msg)
{
  return lara_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<lara_interfaces::srv::GetTCPPose_Request>()
{
  return "lara_interfaces::srv::GetTCPPose_Request";
}

template<>
inline const char * name<lara_interfaces::srv::GetTCPPose_Request>()
{
  return "lara_interfaces/srv/GetTCPPose_Request";
}

template<>
struct has_fixed_size<lara_interfaces::srv::GetTCPPose_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<lara_interfaces::srv::GetTCPPose_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<lara_interfaces::srv::GetTCPPose_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'pose'
#include "geometry_msgs/msg/detail/pose__traits.hpp"

namespace lara_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const GetTCPPose_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: pose
  {
    out << "pose: ";
    to_flow_style_yaml(msg.pose, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const GetTCPPose_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: pose
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "pose:\n";
    to_block_style_yaml(msg.pose, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const GetTCPPose_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace lara_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use lara_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const lara_interfaces::srv::GetTCPPose_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  lara_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use lara_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const lara_interfaces::srv::GetTCPPose_Response & msg)
{
  return lara_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<lara_interfaces::srv::GetTCPPose_Response>()
{
  return "lara_interfaces::srv::GetTCPPose_Response";
}

template<>
inline const char * name<lara_interfaces::srv::GetTCPPose_Response>()
{
  return "lara_interfaces/srv/GetTCPPose_Response";
}

template<>
struct has_fixed_size<lara_interfaces::srv::GetTCPPose_Response>
  : std::integral_constant<bool, has_fixed_size<geometry_msgs::msg::Pose>::value> {};

template<>
struct has_bounded_size<lara_interfaces::srv::GetTCPPose_Response>
  : std::integral_constant<bool, has_bounded_size<geometry_msgs::msg::Pose>::value> {};

template<>
struct is_message<lara_interfaces::srv::GetTCPPose_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<lara_interfaces::srv::GetTCPPose>()
{
  return "lara_interfaces::srv::GetTCPPose";
}

template<>
inline const char * name<lara_interfaces::srv::GetTCPPose>()
{
  return "lara_interfaces/srv/GetTCPPose";
}

template<>
struct has_fixed_size<lara_interfaces::srv::GetTCPPose>
  : std::integral_constant<
    bool,
    has_fixed_size<lara_interfaces::srv::GetTCPPose_Request>::value &&
    has_fixed_size<lara_interfaces::srv::GetTCPPose_Response>::value
  >
{
};

template<>
struct has_bounded_size<lara_interfaces::srv::GetTCPPose>
  : std::integral_constant<
    bool,
    has_bounded_size<lara_interfaces::srv::GetTCPPose_Request>::value &&
    has_bounded_size<lara_interfaces::srv::GetTCPPose_Response>::value
  >
{
};

template<>
struct is_service<lara_interfaces::srv::GetTCPPose>
  : std::true_type
{
};

template<>
struct is_service_request<lara_interfaces::srv::GetTCPPose_Request>
  : std::true_type
{
};

template<>
struct is_service_response<lara_interfaces::srv::GetTCPPose_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // LARA_INTERFACES__SRV__DETAIL__GET_TCP_POSE__TRAITS_HPP_
