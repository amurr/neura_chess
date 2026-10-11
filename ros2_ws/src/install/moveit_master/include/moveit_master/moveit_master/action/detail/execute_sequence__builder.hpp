// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from moveit_master:action/ExecuteSequence.idl
// generated code does not contain a copyright notice

#ifndef MOVEIT_MASTER__ACTION__DETAIL__EXECUTE_SEQUENCE__BUILDER_HPP_
#define MOVEIT_MASTER__ACTION__DETAIL__EXECUTE_SEQUENCE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "moveit_master/action/detail/execute_sequence__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace moveit_master
{

namespace action
{

namespace builder
{

class Init_ExecuteSequence_Goal_velocity_scaling
{
public:
  explicit Init_ExecuteSequence_Goal_velocity_scaling(::moveit_master::action::ExecuteSequence_Goal & msg)
  : msg_(msg)
  {}
  ::moveit_master::action::ExecuteSequence_Goal velocity_scaling(::moveit_master::action::ExecuteSequence_Goal::_velocity_scaling_type arg)
  {
    msg_.velocity_scaling = std::move(arg);
    return std::move(msg_);
  }

private:
  ::moveit_master::action::ExecuteSequence_Goal msg_;
};

class Init_ExecuteSequence_Goal_steps
{
public:
  Init_ExecuteSequence_Goal_steps()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ExecuteSequence_Goal_velocity_scaling steps(::moveit_master::action::ExecuteSequence_Goal::_steps_type arg)
  {
    msg_.steps = std::move(arg);
    return Init_ExecuteSequence_Goal_velocity_scaling(msg_);
  }

private:
  ::moveit_master::action::ExecuteSequence_Goal msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::moveit_master::action::ExecuteSequence_Goal>()
{
  return moveit_master::action::builder::Init_ExecuteSequence_Goal_steps();
}

}  // namespace moveit_master


namespace moveit_master
{

namespace action
{

namespace builder
{

class Init_ExecuteSequence_Result_message
{
public:
  explicit Init_ExecuteSequence_Result_message(::moveit_master::action::ExecuteSequence_Result & msg)
  : msg_(msg)
  {}
  ::moveit_master::action::ExecuteSequence_Result message(::moveit_master::action::ExecuteSequence_Result::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::moveit_master::action::ExecuteSequence_Result msg_;
};

class Init_ExecuteSequence_Result_failed_step
{
public:
  explicit Init_ExecuteSequence_Result_failed_step(::moveit_master::action::ExecuteSequence_Result & msg)
  : msg_(msg)
  {}
  Init_ExecuteSequence_Result_message failed_step(::moveit_master::action::ExecuteSequence_Result::_failed_step_type arg)
  {
    msg_.failed_step = std::move(arg);
    return Init_ExecuteSequence_Result_message(msg_);
  }

private:
  ::moveit_master::action::ExecuteSequence_Result msg_;
};

class Init_ExecuteSequence_Result_success
{
public:
  Init_ExecuteSequence_Result_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ExecuteSequence_Result_failed_step success(::moveit_master::action::ExecuteSequence_Result::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_ExecuteSequence_Result_failed_step(msg_);
  }

private:
  ::moveit_master::action::ExecuteSequence_Result msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::moveit_master::action::ExecuteSequence_Result>()
{
  return moveit_master::action::builder::Init_ExecuteSequence_Result_success();
}

}  // namespace moveit_master


namespace moveit_master
{

namespace action
{

namespace builder
{

class Init_ExecuteSequence_Feedback_current_step
{
public:
  Init_ExecuteSequence_Feedback_current_step()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::moveit_master::action::ExecuteSequence_Feedback current_step(::moveit_master::action::ExecuteSequence_Feedback::_current_step_type arg)
  {
    msg_.current_step = std::move(arg);
    return std::move(msg_);
  }

private:
  ::moveit_master::action::ExecuteSequence_Feedback msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::moveit_master::action::ExecuteSequence_Feedback>()
{
  return moveit_master::action::builder::Init_ExecuteSequence_Feedback_current_step();
}

}  // namespace moveit_master


namespace moveit_master
{

namespace action
{

namespace builder
{

class Init_ExecuteSequence_SendGoal_Request_goal
{
public:
  explicit Init_ExecuteSequence_SendGoal_Request_goal(::moveit_master::action::ExecuteSequence_SendGoal_Request & msg)
  : msg_(msg)
  {}
  ::moveit_master::action::ExecuteSequence_SendGoal_Request goal(::moveit_master::action::ExecuteSequence_SendGoal_Request::_goal_type arg)
  {
    msg_.goal = std::move(arg);
    return std::move(msg_);
  }

private:
  ::moveit_master::action::ExecuteSequence_SendGoal_Request msg_;
};

class Init_ExecuteSequence_SendGoal_Request_goal_id
{
public:
  Init_ExecuteSequence_SendGoal_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ExecuteSequence_SendGoal_Request_goal goal_id(::moveit_master::action::ExecuteSequence_SendGoal_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_ExecuteSequence_SendGoal_Request_goal(msg_);
  }

private:
  ::moveit_master::action::ExecuteSequence_SendGoal_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::moveit_master::action::ExecuteSequence_SendGoal_Request>()
{
  return moveit_master::action::builder::Init_ExecuteSequence_SendGoal_Request_goal_id();
}

}  // namespace moveit_master


namespace moveit_master
{

namespace action
{

namespace builder
{

class Init_ExecuteSequence_SendGoal_Response_stamp
{
public:
  explicit Init_ExecuteSequence_SendGoal_Response_stamp(::moveit_master::action::ExecuteSequence_SendGoal_Response & msg)
  : msg_(msg)
  {}
  ::moveit_master::action::ExecuteSequence_SendGoal_Response stamp(::moveit_master::action::ExecuteSequence_SendGoal_Response::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::moveit_master::action::ExecuteSequence_SendGoal_Response msg_;
};

class Init_ExecuteSequence_SendGoal_Response_accepted
{
public:
  Init_ExecuteSequence_SendGoal_Response_accepted()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ExecuteSequence_SendGoal_Response_stamp accepted(::moveit_master::action::ExecuteSequence_SendGoal_Response::_accepted_type arg)
  {
    msg_.accepted = std::move(arg);
    return Init_ExecuteSequence_SendGoal_Response_stamp(msg_);
  }

private:
  ::moveit_master::action::ExecuteSequence_SendGoal_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::moveit_master::action::ExecuteSequence_SendGoal_Response>()
{
  return moveit_master::action::builder::Init_ExecuteSequence_SendGoal_Response_accepted();
}

}  // namespace moveit_master


namespace moveit_master
{

namespace action
{

namespace builder
{

class Init_ExecuteSequence_GetResult_Request_goal_id
{
public:
  Init_ExecuteSequence_GetResult_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::moveit_master::action::ExecuteSequence_GetResult_Request goal_id(::moveit_master::action::ExecuteSequence_GetResult_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::moveit_master::action::ExecuteSequence_GetResult_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::moveit_master::action::ExecuteSequence_GetResult_Request>()
{
  return moveit_master::action::builder::Init_ExecuteSequence_GetResult_Request_goal_id();
}

}  // namespace moveit_master


namespace moveit_master
{

namespace action
{

namespace builder
{

class Init_ExecuteSequence_GetResult_Response_result
{
public:
  explicit Init_ExecuteSequence_GetResult_Response_result(::moveit_master::action::ExecuteSequence_GetResult_Response & msg)
  : msg_(msg)
  {}
  ::moveit_master::action::ExecuteSequence_GetResult_Response result(::moveit_master::action::ExecuteSequence_GetResult_Response::_result_type arg)
  {
    msg_.result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::moveit_master::action::ExecuteSequence_GetResult_Response msg_;
};

class Init_ExecuteSequence_GetResult_Response_status
{
public:
  Init_ExecuteSequence_GetResult_Response_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ExecuteSequence_GetResult_Response_result status(::moveit_master::action::ExecuteSequence_GetResult_Response::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_ExecuteSequence_GetResult_Response_result(msg_);
  }

private:
  ::moveit_master::action::ExecuteSequence_GetResult_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::moveit_master::action::ExecuteSequence_GetResult_Response>()
{
  return moveit_master::action::builder::Init_ExecuteSequence_GetResult_Response_status();
}

}  // namespace moveit_master


namespace moveit_master
{

namespace action
{

namespace builder
{

class Init_ExecuteSequence_FeedbackMessage_feedback
{
public:
  explicit Init_ExecuteSequence_FeedbackMessage_feedback(::moveit_master::action::ExecuteSequence_FeedbackMessage & msg)
  : msg_(msg)
  {}
  ::moveit_master::action::ExecuteSequence_FeedbackMessage feedback(::moveit_master::action::ExecuteSequence_FeedbackMessage::_feedback_type arg)
  {
    msg_.feedback = std::move(arg);
    return std::move(msg_);
  }

private:
  ::moveit_master::action::ExecuteSequence_FeedbackMessage msg_;
};

class Init_ExecuteSequence_FeedbackMessage_goal_id
{
public:
  Init_ExecuteSequence_FeedbackMessage_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ExecuteSequence_FeedbackMessage_feedback goal_id(::moveit_master::action::ExecuteSequence_FeedbackMessage::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_ExecuteSequence_FeedbackMessage_feedback(msg_);
  }

private:
  ::moveit_master::action::ExecuteSequence_FeedbackMessage msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::moveit_master::action::ExecuteSequence_FeedbackMessage>()
{
  return moveit_master::action::builder::Init_ExecuteSequence_FeedbackMessage_goal_id();
}

}  // namespace moveit_master

#endif  // MOVEIT_MASTER__ACTION__DETAIL__EXECUTE_SEQUENCE__BUILDER_HPP_
