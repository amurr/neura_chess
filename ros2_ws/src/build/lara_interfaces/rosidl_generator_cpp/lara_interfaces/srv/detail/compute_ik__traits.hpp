// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from lara_interfaces:srv/ComputeIK.idl
// generated code does not contain a copyright notice

#ifndef LARA_INTERFACES__SRV__DETAIL__COMPUTE_IK__TRAITS_HPP_
#define LARA_INTERFACES__SRV__DETAIL__COMPUTE_IK__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "lara_interfaces/srv/detail/compute_ik__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'target_pose'
#include "geometry_msgs/msg/detail/pose__traits.hpp"

namespace lara_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const ComputeIK_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: target_pose
  {
    out << "target_pose: ";
    to_flow_style_yaml(msg.target_pose, out);
    out << ", ";
  }

  // member: seed_joint_positions
  {
    if (msg.seed_joint_positions.size() == 0) {
      out << "seed_joint_positions: []";
    } else {
      out << "seed_joint_positions: [";
      size_t pending_items = msg.seed_joint_positions.size();
      for (auto item : msg.seed_joint_positions) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: timeout_sec
  {
    out << "timeout_sec: ";
    rosidl_generator_traits::value_to_yaml(msg.timeout_sec, out);
    out << ", ";
  }

  // member: position_tolerance
  {
    out << "position_tolerance: ";
    rosidl_generator_traits::value_to_yaml(msg.position_tolerance, out);
    out << ", ";
  }

  // member: orientation_tolerance
  {
    out << "orientation_tolerance: ";
    rosidl_generator_traits::value_to_yaml(msg.orientation_tolerance, out);
    out << ", ";
  }

  // member: enforce_joint_limits_mode
  {
    out << "enforce_joint_limits_mode: ";
    rosidl_generator_traits::value_to_yaml(msg.enforce_joint_limits_mode, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ComputeIK_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: target_pose
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "target_pose:\n";
    to_block_style_yaml(msg.target_pose, out, indentation + 2);
  }

  // member: seed_joint_positions
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.seed_joint_positions.size() == 0) {
      out << "seed_joint_positions: []\n";
    } else {
      out << "seed_joint_positions:\n";
      for (auto item : msg.seed_joint_positions) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: timeout_sec
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "timeout_sec: ";
    rosidl_generator_traits::value_to_yaml(msg.timeout_sec, out);
    out << "\n";
  }

  // member: position_tolerance
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "position_tolerance: ";
    rosidl_generator_traits::value_to_yaml(msg.position_tolerance, out);
    out << "\n";
  }

  // member: orientation_tolerance
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "orientation_tolerance: ";
    rosidl_generator_traits::value_to_yaml(msg.orientation_tolerance, out);
    out << "\n";
  }

  // member: enforce_joint_limits_mode
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "enforce_joint_limits_mode: ";
    rosidl_generator_traits::value_to_yaml(msg.enforce_joint_limits_mode, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ComputeIK_Request & msg, bool use_flow_style = false)
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
  const lara_interfaces::srv::ComputeIK_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  lara_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use lara_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const lara_interfaces::srv::ComputeIK_Request & msg)
{
  return lara_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<lara_interfaces::srv::ComputeIK_Request>()
{
  return "lara_interfaces::srv::ComputeIK_Request";
}

template<>
inline const char * name<lara_interfaces::srv::ComputeIK_Request>()
{
  return "lara_interfaces/srv/ComputeIK_Request";
}

template<>
struct has_fixed_size<lara_interfaces::srv::ComputeIK_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<lara_interfaces::srv::ComputeIK_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<lara_interfaces::srv::ComputeIK_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace lara_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const ComputeIK_Response & msg,
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
    out << ", ";
  }

  // member: joint_names
  {
    if (msg.joint_names.size() == 0) {
      out << "joint_names: []";
    } else {
      out << "joint_names: [";
      size_t pending_items = msg.joint_names.size();
      for (auto item : msg.joint_names) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: joint_positions
  {
    if (msg.joint_positions.size() == 0) {
      out << "joint_positions: []";
    } else {
      out << "joint_positions: [";
      size_t pending_items = msg.joint_positions.size();
      for (auto item : msg.joint_positions) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: position_error
  {
    out << "position_error: ";
    rosidl_generator_traits::value_to_yaml(msg.position_error, out);
    out << ", ";
  }

  // member: orientation_error
  {
    out << "orientation_error: ";
    rosidl_generator_traits::value_to_yaml(msg.orientation_error, out);
    out << ", ";
  }

  // member: iterations
  {
    out << "iterations: ";
    rosidl_generator_traits::value_to_yaml(msg.iterations, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ComputeIK_Response & msg,
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

  // member: joint_names
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.joint_names.size() == 0) {
      out << "joint_names: []\n";
    } else {
      out << "joint_names:\n";
      for (auto item : msg.joint_names) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: joint_positions
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.joint_positions.size() == 0) {
      out << "joint_positions: []\n";
    } else {
      out << "joint_positions:\n";
      for (auto item : msg.joint_positions) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: position_error
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "position_error: ";
    rosidl_generator_traits::value_to_yaml(msg.position_error, out);
    out << "\n";
  }

  // member: orientation_error
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "orientation_error: ";
    rosidl_generator_traits::value_to_yaml(msg.orientation_error, out);
    out << "\n";
  }

  // member: iterations
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "iterations: ";
    rosidl_generator_traits::value_to_yaml(msg.iterations, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ComputeIK_Response & msg, bool use_flow_style = false)
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
  const lara_interfaces::srv::ComputeIK_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  lara_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use lara_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const lara_interfaces::srv::ComputeIK_Response & msg)
{
  return lara_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<lara_interfaces::srv::ComputeIK_Response>()
{
  return "lara_interfaces::srv::ComputeIK_Response";
}

template<>
inline const char * name<lara_interfaces::srv::ComputeIK_Response>()
{
  return "lara_interfaces/srv/ComputeIK_Response";
}

template<>
struct has_fixed_size<lara_interfaces::srv::ComputeIK_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<lara_interfaces::srv::ComputeIK_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<lara_interfaces::srv::ComputeIK_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<lara_interfaces::srv::ComputeIK>()
{
  return "lara_interfaces::srv::ComputeIK";
}

template<>
inline const char * name<lara_interfaces::srv::ComputeIK>()
{
  return "lara_interfaces/srv/ComputeIK";
}

template<>
struct has_fixed_size<lara_interfaces::srv::ComputeIK>
  : std::integral_constant<
    bool,
    has_fixed_size<lara_interfaces::srv::ComputeIK_Request>::value &&
    has_fixed_size<lara_interfaces::srv::ComputeIK_Response>::value
  >
{
};

template<>
struct has_bounded_size<lara_interfaces::srv::ComputeIK>
  : std::integral_constant<
    bool,
    has_bounded_size<lara_interfaces::srv::ComputeIK_Request>::value &&
    has_bounded_size<lara_interfaces::srv::ComputeIK_Response>::value
  >
{
};

template<>
struct is_service<lara_interfaces::srv::ComputeIK>
  : std::true_type
{
};

template<>
struct is_service_request<lara_interfaces::srv::ComputeIK_Request>
  : std::true_type
{
};

template<>
struct is_service_response<lara_interfaces::srv::ComputeIK_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // LARA_INTERFACES__SRV__DETAIL__COMPUTE_IK__TRAITS_HPP_
