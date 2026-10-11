// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from lara_interfaces:srv/MoveJoints.idl
// generated code does not contain a copyright notice

#ifndef LARA_INTERFACES__SRV__DETAIL__MOVE_JOINTS__TRAITS_HPP_
#define LARA_INTERFACES__SRV__DETAIL__MOVE_JOINTS__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "lara_interfaces/srv/detail/move_joints__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace lara_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const MoveJoints_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: point_name
  {
    out << "point_name: ";
    rosidl_generator_traits::value_to_yaml(msg.point_name, out);
    out << ", ";
  }

  // member: target_joint
  {
    if (msg.target_joint.size() == 0) {
      out << "target_joint: []";
    } else {
      out << "target_joint: [";
      size_t pending_items = msg.target_joint.size();
      for (auto item : msg.target_joint) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: target_pose
  {
    if (msg.target_pose.size() == 0) {
      out << "target_pose: []";
    } else {
      out << "target_pose: [";
      size_t pending_items = msg.target_pose.size();
      for (auto item : msg.target_pose) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: speed
  {
    out << "speed: ";
    rosidl_generator_traits::value_to_yaml(msg.speed, out);
    out << ", ";
  }

  // member: acceleration
  {
    out << "acceleration: ";
    rosidl_generator_traits::value_to_yaml(msg.acceleration, out);
    out << ", ";
  }

  // member: enable_safety
  {
    out << "enable_safety: ";
    rosidl_generator_traits::value_to_yaml(msg.enable_safety, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const MoveJoints_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: point_name
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "point_name: ";
    rosidl_generator_traits::value_to_yaml(msg.point_name, out);
    out << "\n";
  }

  // member: target_joint
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.target_joint.size() == 0) {
      out << "target_joint: []\n";
    } else {
      out << "target_joint:\n";
      for (auto item : msg.target_joint) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: target_pose
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.target_pose.size() == 0) {
      out << "target_pose: []\n";
    } else {
      out << "target_pose:\n";
      for (auto item : msg.target_pose) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: speed
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "speed: ";
    rosidl_generator_traits::value_to_yaml(msg.speed, out);
    out << "\n";
  }

  // member: acceleration
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "acceleration: ";
    rosidl_generator_traits::value_to_yaml(msg.acceleration, out);
    out << "\n";
  }

  // member: enable_safety
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "enable_safety: ";
    rosidl_generator_traits::value_to_yaml(msg.enable_safety, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MoveJoints_Request & msg, bool use_flow_style = false)
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
  const lara_interfaces::srv::MoveJoints_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  lara_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use lara_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const lara_interfaces::srv::MoveJoints_Request & msg)
{
  return lara_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<lara_interfaces::srv::MoveJoints_Request>()
{
  return "lara_interfaces::srv::MoveJoints_Request";
}

template<>
inline const char * name<lara_interfaces::srv::MoveJoints_Request>()
{
  return "lara_interfaces/srv/MoveJoints_Request";
}

template<>
struct has_fixed_size<lara_interfaces::srv::MoveJoints_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<lara_interfaces::srv::MoveJoints_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<lara_interfaces::srv::MoveJoints_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace lara_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const MoveJoints_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << ", ";
  }

  // member: message
  {
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const MoveJoints_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: success
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << "\n";
  }

  // member: message
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MoveJoints_Response & msg, bool use_flow_style = false)
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
  const lara_interfaces::srv::MoveJoints_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  lara_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use lara_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const lara_interfaces::srv::MoveJoints_Response & msg)
{
  return lara_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<lara_interfaces::srv::MoveJoints_Response>()
{
  return "lara_interfaces::srv::MoveJoints_Response";
}

template<>
inline const char * name<lara_interfaces::srv::MoveJoints_Response>()
{
  return "lara_interfaces/srv/MoveJoints_Response";
}

template<>
struct has_fixed_size<lara_interfaces::srv::MoveJoints_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<lara_interfaces::srv::MoveJoints_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<lara_interfaces::srv::MoveJoints_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<lara_interfaces::srv::MoveJoints>()
{
  return "lara_interfaces::srv::MoveJoints";
}

template<>
inline const char * name<lara_interfaces::srv::MoveJoints>()
{
  return "lara_interfaces/srv/MoveJoints";
}

template<>
struct has_fixed_size<lara_interfaces::srv::MoveJoints>
  : std::integral_constant<
    bool,
    has_fixed_size<lara_interfaces::srv::MoveJoints_Request>::value &&
    has_fixed_size<lara_interfaces::srv::MoveJoints_Response>::value
  >
{
};

template<>
struct has_bounded_size<lara_interfaces::srv::MoveJoints>
  : std::integral_constant<
    bool,
    has_bounded_size<lara_interfaces::srv::MoveJoints_Request>::value &&
    has_bounded_size<lara_interfaces::srv::MoveJoints_Response>::value
  >
{
};

template<>
struct is_service<lara_interfaces::srv::MoveJoints>
  : std::true_type
{
};

template<>
struct is_service_request<lara_interfaces::srv::MoveJoints_Request>
  : std::true_type
{
};

template<>
struct is_service_response<lara_interfaces::srv::MoveJoints_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // LARA_INTERFACES__SRV__DETAIL__MOVE_JOINTS__TRAITS_HPP_
