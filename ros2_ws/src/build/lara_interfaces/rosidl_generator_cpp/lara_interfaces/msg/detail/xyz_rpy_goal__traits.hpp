// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from lara_interfaces:msg/XyzRpyGoal.idl
// generated code does not contain a copyright notice

#ifndef LARA_INTERFACES__MSG__DETAIL__XYZ_RPY_GOAL__TRAITS_HPP_
#define LARA_INTERFACES__MSG__DETAIL__XYZ_RPY_GOAL__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "lara_interfaces/msg/detail/xyz_rpy_goal__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace lara_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const XyzRpyGoal & msg,
  std::ostream & out)
{
  out << "{";
  // member: x
  {
    out << "x: ";
    rosidl_generator_traits::value_to_yaml(msg.x, out);
    out << ", ";
  }

  // member: y
  {
    out << "y: ";
    rosidl_generator_traits::value_to_yaml(msg.y, out);
    out << ", ";
  }

  // member: z
  {
    out << "z: ";
    rosidl_generator_traits::value_to_yaml(msg.z, out);
    out << ", ";
  }

  // member: roll
  {
    out << "roll: ";
    rosidl_generator_traits::value_to_yaml(msg.roll, out);
    out << ", ";
  }

  // member: pitch
  {
    out << "pitch: ";
    rosidl_generator_traits::value_to_yaml(msg.pitch, out);
    out << ", ";
  }

  // member: yaw
  {
    out << "yaw: ";
    rosidl_generator_traits::value_to_yaml(msg.yaw, out);
    out << ", ";
  }

  // member: use_orientation
  {
    out << "use_orientation: ";
    rosidl_generator_traits::value_to_yaml(msg.use_orientation, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const XyzRpyGoal & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: x
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "x: ";
    rosidl_generator_traits::value_to_yaml(msg.x, out);
    out << "\n";
  }

  // member: y
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "y: ";
    rosidl_generator_traits::value_to_yaml(msg.y, out);
    out << "\n";
  }

  // member: z
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "z: ";
    rosidl_generator_traits::value_to_yaml(msg.z, out);
    out << "\n";
  }

  // member: roll
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "roll: ";
    rosidl_generator_traits::value_to_yaml(msg.roll, out);
    out << "\n";
  }

  // member: pitch
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "pitch: ";
    rosidl_generator_traits::value_to_yaml(msg.pitch, out);
    out << "\n";
  }

  // member: yaw
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "yaw: ";
    rosidl_generator_traits::value_to_yaml(msg.yaw, out);
    out << "\n";
  }

  // member: use_orientation
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "use_orientation: ";
    rosidl_generator_traits::value_to_yaml(msg.use_orientation, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const XyzRpyGoal & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace lara_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use lara_interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const lara_interfaces::msg::XyzRpyGoal & msg,
  std::ostream & out, size_t indentation = 0)
{
  lara_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use lara_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const lara_interfaces::msg::XyzRpyGoal & msg)
{
  return lara_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<lara_interfaces::msg::XyzRpyGoal>()
{
  return "lara_interfaces::msg::XyzRpyGoal";
}

template<>
inline const char * name<lara_interfaces::msg::XyzRpyGoal>()
{
  return "lara_interfaces/msg/XyzRpyGoal";
}

template<>
struct has_fixed_size<lara_interfaces::msg::XyzRpyGoal>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<lara_interfaces::msg::XyzRpyGoal>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<lara_interfaces::msg::XyzRpyGoal>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // LARA_INTERFACES__MSG__DETAIL__XYZ_RPY_GOAL__TRAITS_HPP_
