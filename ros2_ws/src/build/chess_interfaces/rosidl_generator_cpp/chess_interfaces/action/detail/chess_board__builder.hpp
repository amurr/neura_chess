// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from chess_interfaces:action/ChessBoard.idl
// generated code does not contain a copyright notice

#ifndef CHESS_INTERFACES__ACTION__DETAIL__CHESS_BOARD__BUILDER_HPP_
#define CHESS_INTERFACES__ACTION__DETAIL__CHESS_BOARD__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "chess_interfaces/action/detail/chess_board__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace chess_interfaces
{

namespace action
{

namespace builder
{

class Init_ChessBoard_Goal_fen
{
public:
  explicit Init_ChessBoard_Goal_fen(::chess_interfaces::action::ChessBoard_Goal & msg)
  : msg_(msg)
  {}
  ::chess_interfaces::action::ChessBoard_Goal fen(::chess_interfaces::action::ChessBoard_Goal::_fen_type arg)
  {
    msg_.fen = std::move(arg);
    return std::move(msg_);
  }

private:
  ::chess_interfaces::action::ChessBoard_Goal msg_;
};

class Init_ChessBoard_Goal_to_place
{
public:
  explicit Init_ChessBoard_Goal_to_place(::chess_interfaces::action::ChessBoard_Goal & msg)
  : msg_(msg)
  {}
  Init_ChessBoard_Goal_fen to_place(::chess_interfaces::action::ChessBoard_Goal::_to_place_type arg)
  {
    msg_.to_place = std::move(arg);
    return Init_ChessBoard_Goal_fen(msg_);
  }

private:
  ::chess_interfaces::action::ChessBoard_Goal msg_;
};

class Init_ChessBoard_Goal_to_pick
{
public:
  explicit Init_ChessBoard_Goal_to_pick(::chess_interfaces::action::ChessBoard_Goal & msg)
  : msg_(msg)
  {}
  Init_ChessBoard_Goal_to_place to_pick(::chess_interfaces::action::ChessBoard_Goal::_to_pick_type arg)
  {
    msg_.to_pick = std::move(arg);
    return Init_ChessBoard_Goal_to_place(msg_);
  }

private:
  ::chess_interfaces::action::ChessBoard_Goal msg_;
};

class Init_ChessBoard_Goal_piece_type
{
public:
  explicit Init_ChessBoard_Goal_piece_type(::chess_interfaces::action::ChessBoard_Goal & msg)
  : msg_(msg)
  {}
  Init_ChessBoard_Goal_to_pick piece_type(::chess_interfaces::action::ChessBoard_Goal::_piece_type_type arg)
  {
    msg_.piece_type = std::move(arg);
    return Init_ChessBoard_Goal_to_pick(msg_);
  }

private:
  ::chess_interfaces::action::ChessBoard_Goal msg_;
};

class Init_ChessBoard_Goal_change_status
{
public:
  Init_ChessBoard_Goal_change_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ChessBoard_Goal_piece_type change_status(::chess_interfaces::action::ChessBoard_Goal::_change_status_type arg)
  {
    msg_.change_status = std::move(arg);
    return Init_ChessBoard_Goal_piece_type(msg_);
  }

private:
  ::chess_interfaces::action::ChessBoard_Goal msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::chess_interfaces::action::ChessBoard_Goal>()
{
  return chess_interfaces::action::builder::Init_ChessBoard_Goal_change_status();
}

}  // namespace chess_interfaces


namespace chess_interfaces
{

namespace action
{

namespace builder
{

class Init_ChessBoard_Result_fen
{
public:
  explicit Init_ChessBoard_Result_fen(::chess_interfaces::action::ChessBoard_Result & msg)
  : msg_(msg)
  {}
  ::chess_interfaces::action::ChessBoard_Result fen(::chess_interfaces::action::ChessBoard_Result::_fen_type arg)
  {
    msg_.fen = std::move(arg);
    return std::move(msg_);
  }

private:
  ::chess_interfaces::action::ChessBoard_Result msg_;
};

class Init_ChessBoard_Result_message
{
public:
  explicit Init_ChessBoard_Result_message(::chess_interfaces::action::ChessBoard_Result & msg)
  : msg_(msg)
  {}
  Init_ChessBoard_Result_fen message(::chess_interfaces::action::ChessBoard_Result::_message_type arg)
  {
    msg_.message = std::move(arg);
    return Init_ChessBoard_Result_fen(msg_);
  }

private:
  ::chess_interfaces::action::ChessBoard_Result msg_;
};

class Init_ChessBoard_Result_success
{
public:
  Init_ChessBoard_Result_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ChessBoard_Result_message success(::chess_interfaces::action::ChessBoard_Result::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_ChessBoard_Result_message(msg_);
  }

private:
  ::chess_interfaces::action::ChessBoard_Result msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::chess_interfaces::action::ChessBoard_Result>()
{
  return chess_interfaces::action::builder::Init_ChessBoard_Result_success();
}

}  // namespace chess_interfaces


namespace chess_interfaces
{

namespace action
{

namespace builder
{

class Init_ChessBoard_Feedback_stage
{
public:
  Init_ChessBoard_Feedback_stage()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::chess_interfaces::action::ChessBoard_Feedback stage(::chess_interfaces::action::ChessBoard_Feedback::_stage_type arg)
  {
    msg_.stage = std::move(arg);
    return std::move(msg_);
  }

private:
  ::chess_interfaces::action::ChessBoard_Feedback msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::chess_interfaces::action::ChessBoard_Feedback>()
{
  return chess_interfaces::action::builder::Init_ChessBoard_Feedback_stage();
}

}  // namespace chess_interfaces


namespace chess_interfaces
{

namespace action
{

namespace builder
{

class Init_ChessBoard_SendGoal_Request_goal
{
public:
  explicit Init_ChessBoard_SendGoal_Request_goal(::chess_interfaces::action::ChessBoard_SendGoal_Request & msg)
  : msg_(msg)
  {}
  ::chess_interfaces::action::ChessBoard_SendGoal_Request goal(::chess_interfaces::action::ChessBoard_SendGoal_Request::_goal_type arg)
  {
    msg_.goal = std::move(arg);
    return std::move(msg_);
  }

private:
  ::chess_interfaces::action::ChessBoard_SendGoal_Request msg_;
};

class Init_ChessBoard_SendGoal_Request_goal_id
{
public:
  Init_ChessBoard_SendGoal_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ChessBoard_SendGoal_Request_goal goal_id(::chess_interfaces::action::ChessBoard_SendGoal_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_ChessBoard_SendGoal_Request_goal(msg_);
  }

private:
  ::chess_interfaces::action::ChessBoard_SendGoal_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::chess_interfaces::action::ChessBoard_SendGoal_Request>()
{
  return chess_interfaces::action::builder::Init_ChessBoard_SendGoal_Request_goal_id();
}

}  // namespace chess_interfaces


namespace chess_interfaces
{

namespace action
{

namespace builder
{

class Init_ChessBoard_SendGoal_Response_stamp
{
public:
  explicit Init_ChessBoard_SendGoal_Response_stamp(::chess_interfaces::action::ChessBoard_SendGoal_Response & msg)
  : msg_(msg)
  {}
  ::chess_interfaces::action::ChessBoard_SendGoal_Response stamp(::chess_interfaces::action::ChessBoard_SendGoal_Response::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::chess_interfaces::action::ChessBoard_SendGoal_Response msg_;
};

class Init_ChessBoard_SendGoal_Response_accepted
{
public:
  Init_ChessBoard_SendGoal_Response_accepted()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ChessBoard_SendGoal_Response_stamp accepted(::chess_interfaces::action::ChessBoard_SendGoal_Response::_accepted_type arg)
  {
    msg_.accepted = std::move(arg);
    return Init_ChessBoard_SendGoal_Response_stamp(msg_);
  }

private:
  ::chess_interfaces::action::ChessBoard_SendGoal_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::chess_interfaces::action::ChessBoard_SendGoal_Response>()
{
  return chess_interfaces::action::builder::Init_ChessBoard_SendGoal_Response_accepted();
}

}  // namespace chess_interfaces


namespace chess_interfaces
{

namespace action
{

namespace builder
{

class Init_ChessBoard_GetResult_Request_goal_id
{
public:
  Init_ChessBoard_GetResult_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::chess_interfaces::action::ChessBoard_GetResult_Request goal_id(::chess_interfaces::action::ChessBoard_GetResult_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::chess_interfaces::action::ChessBoard_GetResult_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::chess_interfaces::action::ChessBoard_GetResult_Request>()
{
  return chess_interfaces::action::builder::Init_ChessBoard_GetResult_Request_goal_id();
}

}  // namespace chess_interfaces


namespace chess_interfaces
{

namespace action
{

namespace builder
{

class Init_ChessBoard_GetResult_Response_result
{
public:
  explicit Init_ChessBoard_GetResult_Response_result(::chess_interfaces::action::ChessBoard_GetResult_Response & msg)
  : msg_(msg)
  {}
  ::chess_interfaces::action::ChessBoard_GetResult_Response result(::chess_interfaces::action::ChessBoard_GetResult_Response::_result_type arg)
  {
    msg_.result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::chess_interfaces::action::ChessBoard_GetResult_Response msg_;
};

class Init_ChessBoard_GetResult_Response_status
{
public:
  Init_ChessBoard_GetResult_Response_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ChessBoard_GetResult_Response_result status(::chess_interfaces::action::ChessBoard_GetResult_Response::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_ChessBoard_GetResult_Response_result(msg_);
  }

private:
  ::chess_interfaces::action::ChessBoard_GetResult_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::chess_interfaces::action::ChessBoard_GetResult_Response>()
{
  return chess_interfaces::action::builder::Init_ChessBoard_GetResult_Response_status();
}

}  // namespace chess_interfaces


namespace chess_interfaces
{

namespace action
{

namespace builder
{

class Init_ChessBoard_FeedbackMessage_feedback
{
public:
  explicit Init_ChessBoard_FeedbackMessage_feedback(::chess_interfaces::action::ChessBoard_FeedbackMessage & msg)
  : msg_(msg)
  {}
  ::chess_interfaces::action::ChessBoard_FeedbackMessage feedback(::chess_interfaces::action::ChessBoard_FeedbackMessage::_feedback_type arg)
  {
    msg_.feedback = std::move(arg);
    return std::move(msg_);
  }

private:
  ::chess_interfaces::action::ChessBoard_FeedbackMessage msg_;
};

class Init_ChessBoard_FeedbackMessage_goal_id
{
public:
  Init_ChessBoard_FeedbackMessage_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ChessBoard_FeedbackMessage_feedback goal_id(::chess_interfaces::action::ChessBoard_FeedbackMessage::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_ChessBoard_FeedbackMessage_feedback(msg_);
  }

private:
  ::chess_interfaces::action::ChessBoard_FeedbackMessage msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::chess_interfaces::action::ChessBoard_FeedbackMessage>()
{
  return chess_interfaces::action::builder::Init_ChessBoard_FeedbackMessage_goal_id();
}

}  // namespace chess_interfaces

#endif  // CHESS_INTERFACES__ACTION__DETAIL__CHESS_BOARD__BUILDER_HPP_
