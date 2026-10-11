// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from moveit_master:msg/MotionStep.idl
// generated code does not contain a copyright notice

#ifndef MOVEIT_MASTER__MSG__DETAIL__MOTION_STEP__TRAITS_HPP_
#define MOVEIT_MASTER__MSG__DETAIL__MOTION_STEP__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "moveit_master/msg/detail/motion_step__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'pose'
#include "geometry_msgs/msg/detail/pose__traits.hpp"
// Member 'offset'
#include "geometry_msgs/msg/detail/vector3__traits.hpp"

namespace moveit_master
{

namespace msg
{

inline void to_flow_style_yaml(
  const MotionStep & msg,
  std::ostream & out)
{
  out << "{";
  // member: type
  {
    out << "type: ";
    rosidl_generator_traits::value_to_yaml(msg.type, out);
    out << ", ";
  }

  // member: pose
  {
    out << "pose: ";
    to_flow_style_yaml(msg.pose, out);
    out << ", ";
  }

  // member: named_target
  {
    out << "named_target: ";
    rosidl_generator_traits::value_to_yaml(msg.named_target, out);
    out << ", ";
  }

  // member: duration
  {
    out << "duration: ";
    rosidl_generator_traits::value_to_yaml(msg.duration, out);
    out << ", ";
  }

  // member: joint_value
  {
    out << "joint_value: ";
    rosidl_generator_traits::value_to_yaml(msg.joint_value, out);
    out << ", ";
  }

  // member: offset
  {
    out << "offset: ";
    to_flow_style_yaml(msg.offset, out);
    out << ", ";
  }

  // member: object_id
  {
    out << "object_id: ";
    rosidl_generator_traits::value_to_yaml(msg.object_id, out);
    out << ", ";
  }

  // member: touch_links
  {
    if (msg.touch_links.size() == 0) {
      out << "touch_links: []";
    } else {
      out << "touch_links: [";
      size_t pending_items = msg.touch_links.size();
      for (auto item : msg.touch_links) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: allow
  {
    out << "allow: ";
    rosidl_generator_traits::value_to_yaml(msg.allow, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const MotionStep & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: type
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "type: ";
    rosidl_generator_traits::value_to_yaml(msg.type, out);
    out << "\n";
  }

  // member: pose
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "pose:\n";
    to_block_style_yaml(msg.pose, out, indentation + 2);
  }

  // member: named_target
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "named_target: ";
    rosidl_generator_traits::value_to_yaml(msg.named_target, out);
    out << "\n";
  }

  // member: duration
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "duration: ";
    rosidl_generator_traits::value_to_yaml(msg.duration, out);
    out << "\n";
  }

  // member: joint_value
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "joint_value: ";
    rosidl_generator_traits::value_to_yaml(msg.joint_value, out);
    out << "\n";
  }

  // member: offset
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "offset:\n";
    to_block_style_yaml(msg.offset, out, indentation + 2);
  }

  // member: object_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "object_id: ";
    rosidl_generator_traits::value_to_yaml(msg.object_id, out);
    out << "\n";
  }

  // member: touch_links
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.touch_links.size() == 0) {
      out << "touch_links: []\n";
    } else {
      out << "touch_links:\n";
      for (auto item : msg.touch_links) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: allow
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "allow: ";
    rosidl_generator_traits::value_to_yaml(msg.allow, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MotionStep & msg, bool use_flow_style = false)
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

}  // namespace moveit_master

namespace rosidl_generator_traits
{

[[deprecated("use moveit_master::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const moveit_master::msg::MotionStep & msg,
  std::ostream & out, size_t indentation = 0)
{
  moveit_master::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use moveit_master::msg::to_yaml() instead")]]
inline std::string to_yaml(const moveit_master::msg::MotionStep & msg)
{
  return moveit_master::msg::to_yaml(msg);
}

template<>
inline const char * data_type<moveit_master::msg::MotionStep>()
{
  return "moveit_master::msg::MotionStep";
}

template<>
inline const char * name<moveit_master::msg::MotionStep>()
{
  return "moveit_master/msg/MotionStep";
}

template<>
struct has_fixed_size<moveit_master::msg::MotionStep>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<moveit_master::msg::MotionStep>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<moveit_master::msg::MotionStep>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // MOVEIT_MASTER__MSG__DETAIL__MOTION_STEP__TRAITS_HPP_
