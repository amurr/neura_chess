// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from chess_interfaces:action/ChessBoard.idl
// generated code does not contain a copyright notice

#ifndef CHESS_INTERFACES__ACTION__DETAIL__CHESS_BOARD__TRAITS_HPP_
#define CHESS_INTERFACES__ACTION__DETAIL__CHESS_BOARD__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "chess_interfaces/action/detail/chess_board__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace chess_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const ChessBoard_Goal & msg,
  std::ostream & out)
{
  out << "{";
  // member: change_status
  {
    out << "change_status: ";
    rosidl_generator_traits::value_to_yaml(msg.change_status, out);
    out << ", ";
  }

  // member: piece_type
  {
    out << "piece_type: ";
    rosidl_generator_traits::value_to_yaml(msg.piece_type, out);
    out << ", ";
  }

  // member: to_pick
  {
    out << "to_pick: ";
    rosidl_generator_traits::value_to_yaml(msg.to_pick, out);
    out << ", ";
  }

  // member: to_place
  {
    out << "to_place: ";
    rosidl_generator_traits::value_to_yaml(msg.to_place, out);
    out << ", ";
  }

  // member: fen
  {
    out << "fen: ";
    rosidl_generator_traits::value_to_yaml(msg.fen, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ChessBoard_Goal & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: change_status
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "change_status: ";
    rosidl_generator_traits::value_to_yaml(msg.change_status, out);
    out << "\n";
  }

  // member: piece_type
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "piece_type: ";
    rosidl_generator_traits::value_to_yaml(msg.piece_type, out);
    out << "\n";
  }

  // member: to_pick
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "to_pick: ";
    rosidl_generator_traits::value_to_yaml(msg.to_pick, out);
    out << "\n";
  }

  // member: to_place
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "to_place: ";
    rosidl_generator_traits::value_to_yaml(msg.to_place, out);
    out << "\n";
  }

  // member: fen
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "fen: ";
    rosidl_generator_traits::value_to_yaml(msg.fen, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ChessBoard_Goal & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace chess_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use chess_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const chess_interfaces::action::ChessBoard_Goal & msg,
  std::ostream & out, size_t indentation = 0)
{
  chess_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use chess_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const chess_interfaces::action::ChessBoard_Goal & msg)
{
  return chess_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<chess_interfaces::action::ChessBoard_Goal>()
{
  return "chess_interfaces::action::ChessBoard_Goal";
}

template<>
inline const char * name<chess_interfaces::action::ChessBoard_Goal>()
{
  return "chess_interfaces/action/ChessBoard_Goal";
}

template<>
struct has_fixed_size<chess_interfaces::action::ChessBoard_Goal>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<chess_interfaces::action::ChessBoard_Goal>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<chess_interfaces::action::ChessBoard_Goal>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace chess_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const ChessBoard_Result & msg,
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

  // member: fen
  {
    out << "fen: ";
    rosidl_generator_traits::value_to_yaml(msg.fen, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ChessBoard_Result & msg,
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

  // member: fen
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "fen: ";
    rosidl_generator_traits::value_to_yaml(msg.fen, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ChessBoard_Result & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace chess_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use chess_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const chess_interfaces::action::ChessBoard_Result & msg,
  std::ostream & out, size_t indentation = 0)
{
  chess_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use chess_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const chess_interfaces::action::ChessBoard_Result & msg)
{
  return chess_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<chess_interfaces::action::ChessBoard_Result>()
{
  return "chess_interfaces::action::ChessBoard_Result";
}

template<>
inline const char * name<chess_interfaces::action::ChessBoard_Result>()
{
  return "chess_interfaces/action/ChessBoard_Result";
}

template<>
struct has_fixed_size<chess_interfaces::action::ChessBoard_Result>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<chess_interfaces::action::ChessBoard_Result>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<chess_interfaces::action::ChessBoard_Result>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace chess_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const ChessBoard_Feedback & msg,
  std::ostream & out)
{
  out << "{";
  // member: stage
  {
    out << "stage: ";
    rosidl_generator_traits::value_to_yaml(msg.stage, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ChessBoard_Feedback & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: stage
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "stage: ";
    rosidl_generator_traits::value_to_yaml(msg.stage, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ChessBoard_Feedback & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace chess_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use chess_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const chess_interfaces::action::ChessBoard_Feedback & msg,
  std::ostream & out, size_t indentation = 0)
{
  chess_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use chess_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const chess_interfaces::action::ChessBoard_Feedback & msg)
{
  return chess_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<chess_interfaces::action::ChessBoard_Feedback>()
{
  return "chess_interfaces::action::ChessBoard_Feedback";
}

template<>
inline const char * name<chess_interfaces::action::ChessBoard_Feedback>()
{
  return "chess_interfaces/action/ChessBoard_Feedback";
}

template<>
struct has_fixed_size<chess_interfaces::action::ChessBoard_Feedback>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<chess_interfaces::action::ChessBoard_Feedback>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<chess_interfaces::action::ChessBoard_Feedback>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__traits.hpp"
// Member 'goal'
#include "chess_interfaces/action/detail/chess_board__traits.hpp"

namespace chess_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const ChessBoard_SendGoal_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: goal_id
  {
    out << "goal_id: ";
    to_flow_style_yaml(msg.goal_id, out);
    out << ", ";
  }

  // member: goal
  {
    out << "goal: ";
    to_flow_style_yaml(msg.goal, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ChessBoard_SendGoal_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: goal_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal_id:\n";
    to_block_style_yaml(msg.goal_id, out, indentation + 2);
  }

  // member: goal
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal:\n";
    to_block_style_yaml(msg.goal, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ChessBoard_SendGoal_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace chess_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use chess_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const chess_interfaces::action::ChessBoard_SendGoal_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  chess_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use chess_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const chess_interfaces::action::ChessBoard_SendGoal_Request & msg)
{
  return chess_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<chess_interfaces::action::ChessBoard_SendGoal_Request>()
{
  return "chess_interfaces::action::ChessBoard_SendGoal_Request";
}

template<>
inline const char * name<chess_interfaces::action::ChessBoard_SendGoal_Request>()
{
  return "chess_interfaces/action/ChessBoard_SendGoal_Request";
}

template<>
struct has_fixed_size<chess_interfaces::action::ChessBoard_SendGoal_Request>
  : std::integral_constant<bool, has_fixed_size<chess_interfaces::action::ChessBoard_Goal>::value && has_fixed_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct has_bounded_size<chess_interfaces::action::ChessBoard_SendGoal_Request>
  : std::integral_constant<bool, has_bounded_size<chess_interfaces::action::ChessBoard_Goal>::value && has_bounded_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct is_message<chess_interfaces::action::ChessBoard_SendGoal_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__traits.hpp"

namespace chess_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const ChessBoard_SendGoal_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: accepted
  {
    out << "accepted: ";
    rosidl_generator_traits::value_to_yaml(msg.accepted, out);
    out << ", ";
  }

  // member: stamp
  {
    out << "stamp: ";
    to_flow_style_yaml(msg.stamp, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ChessBoard_SendGoal_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: accepted
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "accepted: ";
    rosidl_generator_traits::value_to_yaml(msg.accepted, out);
    out << "\n";
  }

  // member: stamp
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "stamp:\n";
    to_block_style_yaml(msg.stamp, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ChessBoard_SendGoal_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace chess_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use chess_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const chess_interfaces::action::ChessBoard_SendGoal_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  chess_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use chess_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const chess_interfaces::action::ChessBoard_SendGoal_Response & msg)
{
  return chess_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<chess_interfaces::action::ChessBoard_SendGoal_Response>()
{
  return "chess_interfaces::action::ChessBoard_SendGoal_Response";
}

template<>
inline const char * name<chess_interfaces::action::ChessBoard_SendGoal_Response>()
{
  return "chess_interfaces/action/ChessBoard_SendGoal_Response";
}

template<>
struct has_fixed_size<chess_interfaces::action::ChessBoard_SendGoal_Response>
  : std::integral_constant<bool, has_fixed_size<builtin_interfaces::msg::Time>::value> {};

template<>
struct has_bounded_size<chess_interfaces::action::ChessBoard_SendGoal_Response>
  : std::integral_constant<bool, has_bounded_size<builtin_interfaces::msg::Time>::value> {};

template<>
struct is_message<chess_interfaces::action::ChessBoard_SendGoal_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<chess_interfaces::action::ChessBoard_SendGoal>()
{
  return "chess_interfaces::action::ChessBoard_SendGoal";
}

template<>
inline const char * name<chess_interfaces::action::ChessBoard_SendGoal>()
{
  return "chess_interfaces/action/ChessBoard_SendGoal";
}

template<>
struct has_fixed_size<chess_interfaces::action::ChessBoard_SendGoal>
  : std::integral_constant<
    bool,
    has_fixed_size<chess_interfaces::action::ChessBoard_SendGoal_Request>::value &&
    has_fixed_size<chess_interfaces::action::ChessBoard_SendGoal_Response>::value
  >
{
};

template<>
struct has_bounded_size<chess_interfaces::action::ChessBoard_SendGoal>
  : std::integral_constant<
    bool,
    has_bounded_size<chess_interfaces::action::ChessBoard_SendGoal_Request>::value &&
    has_bounded_size<chess_interfaces::action::ChessBoard_SendGoal_Response>::value
  >
{
};

template<>
struct is_service<chess_interfaces::action::ChessBoard_SendGoal>
  : std::true_type
{
};

template<>
struct is_service_request<chess_interfaces::action::ChessBoard_SendGoal_Request>
  : std::true_type
{
};

template<>
struct is_service_response<chess_interfaces::action::ChessBoard_SendGoal_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__traits.hpp"

namespace chess_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const ChessBoard_GetResult_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: goal_id
  {
    out << "goal_id: ";
    to_flow_style_yaml(msg.goal_id, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ChessBoard_GetResult_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: goal_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal_id:\n";
    to_block_style_yaml(msg.goal_id, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ChessBoard_GetResult_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace chess_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use chess_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const chess_interfaces::action::ChessBoard_GetResult_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  chess_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use chess_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const chess_interfaces::action::ChessBoard_GetResult_Request & msg)
{
  return chess_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<chess_interfaces::action::ChessBoard_GetResult_Request>()
{
  return "chess_interfaces::action::ChessBoard_GetResult_Request";
}

template<>
inline const char * name<chess_interfaces::action::ChessBoard_GetResult_Request>()
{
  return "chess_interfaces/action/ChessBoard_GetResult_Request";
}

template<>
struct has_fixed_size<chess_interfaces::action::ChessBoard_GetResult_Request>
  : std::integral_constant<bool, has_fixed_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct has_bounded_size<chess_interfaces::action::ChessBoard_GetResult_Request>
  : std::integral_constant<bool, has_bounded_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct is_message<chess_interfaces::action::ChessBoard_GetResult_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'result'
// already included above
// #include "chess_interfaces/action/detail/chess_board__traits.hpp"

namespace chess_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const ChessBoard_GetResult_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: status
  {
    out << "status: ";
    rosidl_generator_traits::value_to_yaml(msg.status, out);
    out << ", ";
  }

  // member: result
  {
    out << "result: ";
    to_flow_style_yaml(msg.result, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ChessBoard_GetResult_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: status
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "status: ";
    rosidl_generator_traits::value_to_yaml(msg.status, out);
    out << "\n";
  }

  // member: result
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "result:\n";
    to_block_style_yaml(msg.result, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ChessBoard_GetResult_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace chess_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use chess_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const chess_interfaces::action::ChessBoard_GetResult_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  chess_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use chess_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const chess_interfaces::action::ChessBoard_GetResult_Response & msg)
{
  return chess_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<chess_interfaces::action::ChessBoard_GetResult_Response>()
{
  return "chess_interfaces::action::ChessBoard_GetResult_Response";
}

template<>
inline const char * name<chess_interfaces::action::ChessBoard_GetResult_Response>()
{
  return "chess_interfaces/action/ChessBoard_GetResult_Response";
}

template<>
struct has_fixed_size<chess_interfaces::action::ChessBoard_GetResult_Response>
  : std::integral_constant<bool, has_fixed_size<chess_interfaces::action::ChessBoard_Result>::value> {};

template<>
struct has_bounded_size<chess_interfaces::action::ChessBoard_GetResult_Response>
  : std::integral_constant<bool, has_bounded_size<chess_interfaces::action::ChessBoard_Result>::value> {};

template<>
struct is_message<chess_interfaces::action::ChessBoard_GetResult_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<chess_interfaces::action::ChessBoard_GetResult>()
{
  return "chess_interfaces::action::ChessBoard_GetResult";
}

template<>
inline const char * name<chess_interfaces::action::ChessBoard_GetResult>()
{
  return "chess_interfaces/action/ChessBoard_GetResult";
}

template<>
struct has_fixed_size<chess_interfaces::action::ChessBoard_GetResult>
  : std::integral_constant<
    bool,
    has_fixed_size<chess_interfaces::action::ChessBoard_GetResult_Request>::value &&
    has_fixed_size<chess_interfaces::action::ChessBoard_GetResult_Response>::value
  >
{
};

template<>
struct has_bounded_size<chess_interfaces::action::ChessBoard_GetResult>
  : std::integral_constant<
    bool,
    has_bounded_size<chess_interfaces::action::ChessBoard_GetResult_Request>::value &&
    has_bounded_size<chess_interfaces::action::ChessBoard_GetResult_Response>::value
  >
{
};

template<>
struct is_service<chess_interfaces::action::ChessBoard_GetResult>
  : std::true_type
{
};

template<>
struct is_service_request<chess_interfaces::action::ChessBoard_GetResult_Request>
  : std::true_type
{
};

template<>
struct is_service_response<chess_interfaces::action::ChessBoard_GetResult_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__traits.hpp"
// Member 'feedback'
// already included above
// #include "chess_interfaces/action/detail/chess_board__traits.hpp"

namespace chess_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const ChessBoard_FeedbackMessage & msg,
  std::ostream & out)
{
  out << "{";
  // member: goal_id
  {
    out << "goal_id: ";
    to_flow_style_yaml(msg.goal_id, out);
    out << ", ";
  }

  // member: feedback
  {
    out << "feedback: ";
    to_flow_style_yaml(msg.feedback, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ChessBoard_FeedbackMessage & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: goal_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal_id:\n";
    to_block_style_yaml(msg.goal_id, out, indentation + 2);
  }

  // member: feedback
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "feedback:\n";
    to_block_style_yaml(msg.feedback, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ChessBoard_FeedbackMessage & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace chess_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use chess_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const chess_interfaces::action::ChessBoard_FeedbackMessage & msg,
  std::ostream & out, size_t indentation = 0)
{
  chess_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use chess_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const chess_interfaces::action::ChessBoard_FeedbackMessage & msg)
{
  return chess_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<chess_interfaces::action::ChessBoard_FeedbackMessage>()
{
  return "chess_interfaces::action::ChessBoard_FeedbackMessage";
}

template<>
inline const char * name<chess_interfaces::action::ChessBoard_FeedbackMessage>()
{
  return "chess_interfaces/action/ChessBoard_FeedbackMessage";
}

template<>
struct has_fixed_size<chess_interfaces::action::ChessBoard_FeedbackMessage>
  : std::integral_constant<bool, has_fixed_size<chess_interfaces::action::ChessBoard_Feedback>::value && has_fixed_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct has_bounded_size<chess_interfaces::action::ChessBoard_FeedbackMessage>
  : std::integral_constant<bool, has_bounded_size<chess_interfaces::action::ChessBoard_Feedback>::value && has_bounded_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct is_message<chess_interfaces::action::ChessBoard_FeedbackMessage>
  : std::true_type {};

}  // namespace rosidl_generator_traits


namespace rosidl_generator_traits
{

template<>
struct is_action<chess_interfaces::action::ChessBoard>
  : std::true_type
{
};

template<>
struct is_action_goal<chess_interfaces::action::ChessBoard_Goal>
  : std::true_type
{
};

template<>
struct is_action_result<chess_interfaces::action::ChessBoard_Result>
  : std::true_type
{
};

template<>
struct is_action_feedback<chess_interfaces::action::ChessBoard_Feedback>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits


#endif  // CHESS_INTERFACES__ACTION__DETAIL__CHESS_BOARD__TRAITS_HPP_
