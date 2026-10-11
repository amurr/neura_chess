// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from lara_interfaces:srv/GetAppMode.idl
// generated code does not contain a copyright notice

#ifndef LARA_INTERFACES__SRV__DETAIL__GET_APP_MODE__TRAITS_HPP_
#define LARA_INTERFACES__SRV__DETAIL__GET_APP_MODE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "lara_interfaces/srv/detail/get_app_mode__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace lara_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const GetAppMode_Request & msg,
  std::ostream & out)
{
  (void)msg;
  out << "null";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const GetAppMode_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  (void)msg;
  (void)indentation;
  out << "null\n";
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const GetAppMode_Request & msg, bool use_flow_style = false)
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
  const lara_interfaces::srv::GetAppMode_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  lara_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use lara_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const lara_interfaces::srv::GetAppMode_Request & msg)
{
  return lara_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<lara_interfaces::srv::GetAppMode_Request>()
{
  return "lara_interfaces::srv::GetAppMode_Request";
}

template<>
inline const char * name<lara_interfaces::srv::GetAppMode_Request>()
{
  return "lara_interfaces/srv/GetAppMode_Request";
}

template<>
struct has_fixed_size<lara_interfaces::srv::GetAppMode_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<lara_interfaces::srv::GetAppMode_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<lara_interfaces::srv::GetAppMode_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace lara_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const GetAppMode_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: mode
  {
    out << "mode: ";
    rosidl_generator_traits::value_to_yaml(msg.mode, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const GetAppMode_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: mode
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "mode: ";
    rosidl_generator_traits::value_to_yaml(msg.mode, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const GetAppMode_Response & msg, bool use_flow_style = false)
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
  const lara_interfaces::srv::GetAppMode_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  lara_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use lara_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const lara_interfaces::srv::GetAppMode_Response & msg)
{
  return lara_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<lara_interfaces::srv::GetAppMode_Response>()
{
  return "lara_interfaces::srv::GetAppMode_Response";
}

template<>
inline const char * name<lara_interfaces::srv::GetAppMode_Response>()
{
  return "lara_interfaces/srv/GetAppMode_Response";
}

template<>
struct has_fixed_size<lara_interfaces::srv::GetAppMode_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<lara_interfaces::srv::GetAppMode_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<lara_interfaces::srv::GetAppMode_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<lara_interfaces::srv::GetAppMode>()
{
  return "lara_interfaces::srv::GetAppMode";
}

template<>
inline const char * name<lara_interfaces::srv::GetAppMode>()
{
  return "lara_interfaces/srv/GetAppMode";
}

template<>
struct has_fixed_size<lara_interfaces::srv::GetAppMode>
  : std::integral_constant<
    bool,
    has_fixed_size<lara_interfaces::srv::GetAppMode_Request>::value &&
    has_fixed_size<lara_interfaces::srv::GetAppMode_Response>::value
  >
{
};

template<>
struct has_bounded_size<lara_interfaces::srv::GetAppMode>
  : std::integral_constant<
    bool,
    has_bounded_size<lara_interfaces::srv::GetAppMode_Request>::value &&
    has_bounded_size<lara_interfaces::srv::GetAppMode_Response>::value
  >
{
};

template<>
struct is_service<lara_interfaces::srv::GetAppMode>
  : std::true_type
{
};

template<>
struct is_service_request<lara_interfaces::srv::GetAppMode_Request>
  : std::true_type
{
};

template<>
struct is_service_response<lara_interfaces::srv::GetAppMode_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // LARA_INTERFACES__SRV__DETAIL__GET_APP_MODE__TRAITS_HPP_
