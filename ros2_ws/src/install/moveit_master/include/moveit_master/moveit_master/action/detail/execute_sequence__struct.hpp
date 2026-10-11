// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from moveit_master:action/ExecuteSequence.idl
// generated code does not contain a copyright notice

#ifndef MOVEIT_MASTER__ACTION__DETAIL__EXECUTE_SEQUENCE__STRUCT_HPP_
#define MOVEIT_MASTER__ACTION__DETAIL__EXECUTE_SEQUENCE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'steps'
#include "moveit_master/msg/detail/motion_step__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__moveit_master__action__ExecuteSequence_Goal __attribute__((deprecated))
#else
# define DEPRECATED__moveit_master__action__ExecuteSequence_Goal __declspec(deprecated)
#endif

namespace moveit_master
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct ExecuteSequence_Goal_
{
  using Type = ExecuteSequence_Goal_<ContainerAllocator>;

  explicit ExecuteSequence_Goal_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->velocity_scaling = 0.0;
    }
  }

  explicit ExecuteSequence_Goal_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->velocity_scaling = 0.0;
    }
  }

  // field types and members
  using _steps_type =
    std::vector<moveit_master::msg::MotionStep_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<moveit_master::msg::MotionStep_<ContainerAllocator>>>;
  _steps_type steps;
  using _velocity_scaling_type =
    double;
  _velocity_scaling_type velocity_scaling;

  // setters for named parameter idiom
  Type & set__steps(
    const std::vector<moveit_master::msg::MotionStep_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<moveit_master::msg::MotionStep_<ContainerAllocator>>> & _arg)
  {
    this->steps = _arg;
    return *this;
  }
  Type & set__velocity_scaling(
    const double & _arg)
  {
    this->velocity_scaling = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    moveit_master::action::ExecuteSequence_Goal_<ContainerAllocator> *;
  using ConstRawPtr =
    const moveit_master::action::ExecuteSequence_Goal_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<moveit_master::action::ExecuteSequence_Goal_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<moveit_master::action::ExecuteSequence_Goal_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      moveit_master::action::ExecuteSequence_Goal_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<moveit_master::action::ExecuteSequence_Goal_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      moveit_master::action::ExecuteSequence_Goal_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<moveit_master::action::ExecuteSequence_Goal_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<moveit_master::action::ExecuteSequence_Goal_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<moveit_master::action::ExecuteSequence_Goal_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__moveit_master__action__ExecuteSequence_Goal
    std::shared_ptr<moveit_master::action::ExecuteSequence_Goal_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__moveit_master__action__ExecuteSequence_Goal
    std::shared_ptr<moveit_master::action::ExecuteSequence_Goal_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ExecuteSequence_Goal_ & other) const
  {
    if (this->steps != other.steps) {
      return false;
    }
    if (this->velocity_scaling != other.velocity_scaling) {
      return false;
    }
    return true;
  }
  bool operator!=(const ExecuteSequence_Goal_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ExecuteSequence_Goal_

// alias to use template instance with default allocator
using ExecuteSequence_Goal =
  moveit_master::action::ExecuteSequence_Goal_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace moveit_master


#ifndef _WIN32
# define DEPRECATED__moveit_master__action__ExecuteSequence_Result __attribute__((deprecated))
#else
# define DEPRECATED__moveit_master__action__ExecuteSequence_Result __declspec(deprecated)
#endif

namespace moveit_master
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct ExecuteSequence_Result_
{
  using Type = ExecuteSequence_Result_<ContainerAllocator>;

  explicit ExecuteSequence_Result_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->failed_step = 0ul;
      this->message = "";
    }
  }

  explicit ExecuteSequence_Result_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : message(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->failed_step = 0ul;
      this->message = "";
    }
  }

  // field types and members
  using _success_type =
    bool;
  _success_type success;
  using _failed_step_type =
    uint32_t;
  _failed_step_type failed_step;
  using _message_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _message_type message;

  // setters for named parameter idiom
  Type & set__success(
    const bool & _arg)
  {
    this->success = _arg;
    return *this;
  }
  Type & set__failed_step(
    const uint32_t & _arg)
  {
    this->failed_step = _arg;
    return *this;
  }
  Type & set__message(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->message = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    moveit_master::action::ExecuteSequence_Result_<ContainerAllocator> *;
  using ConstRawPtr =
    const moveit_master::action::ExecuteSequence_Result_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<moveit_master::action::ExecuteSequence_Result_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<moveit_master::action::ExecuteSequence_Result_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      moveit_master::action::ExecuteSequence_Result_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<moveit_master::action::ExecuteSequence_Result_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      moveit_master::action::ExecuteSequence_Result_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<moveit_master::action::ExecuteSequence_Result_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<moveit_master::action::ExecuteSequence_Result_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<moveit_master::action::ExecuteSequence_Result_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__moveit_master__action__ExecuteSequence_Result
    std::shared_ptr<moveit_master::action::ExecuteSequence_Result_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__moveit_master__action__ExecuteSequence_Result
    std::shared_ptr<moveit_master::action::ExecuteSequence_Result_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ExecuteSequence_Result_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    if (this->failed_step != other.failed_step) {
      return false;
    }
    if (this->message != other.message) {
      return false;
    }
    return true;
  }
  bool operator!=(const ExecuteSequence_Result_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ExecuteSequence_Result_

// alias to use template instance with default allocator
using ExecuteSequence_Result =
  moveit_master::action::ExecuteSequence_Result_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace moveit_master


#ifndef _WIN32
# define DEPRECATED__moveit_master__action__ExecuteSequence_Feedback __attribute__((deprecated))
#else
# define DEPRECATED__moveit_master__action__ExecuteSequence_Feedback __declspec(deprecated)
#endif

namespace moveit_master
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct ExecuteSequence_Feedback_
{
  using Type = ExecuteSequence_Feedback_<ContainerAllocator>;

  explicit ExecuteSequence_Feedback_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->current_step = 0ul;
    }
  }

  explicit ExecuteSequence_Feedback_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->current_step = 0ul;
    }
  }

  // field types and members
  using _current_step_type =
    uint32_t;
  _current_step_type current_step;

  // setters for named parameter idiom
  Type & set__current_step(
    const uint32_t & _arg)
  {
    this->current_step = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    moveit_master::action::ExecuteSequence_Feedback_<ContainerAllocator> *;
  using ConstRawPtr =
    const moveit_master::action::ExecuteSequence_Feedback_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<moveit_master::action::ExecuteSequence_Feedback_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<moveit_master::action::ExecuteSequence_Feedback_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      moveit_master::action::ExecuteSequence_Feedback_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<moveit_master::action::ExecuteSequence_Feedback_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      moveit_master::action::ExecuteSequence_Feedback_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<moveit_master::action::ExecuteSequence_Feedback_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<moveit_master::action::ExecuteSequence_Feedback_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<moveit_master::action::ExecuteSequence_Feedback_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__moveit_master__action__ExecuteSequence_Feedback
    std::shared_ptr<moveit_master::action::ExecuteSequence_Feedback_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__moveit_master__action__ExecuteSequence_Feedback
    std::shared_ptr<moveit_master::action::ExecuteSequence_Feedback_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ExecuteSequence_Feedback_ & other) const
  {
    if (this->current_step != other.current_step) {
      return false;
    }
    return true;
  }
  bool operator!=(const ExecuteSequence_Feedback_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ExecuteSequence_Feedback_

// alias to use template instance with default allocator
using ExecuteSequence_Feedback =
  moveit_master::action::ExecuteSequence_Feedback_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace moveit_master


// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__struct.hpp"
// Member 'goal'
#include "moveit_master/action/detail/execute_sequence__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__moveit_master__action__ExecuteSequence_SendGoal_Request __attribute__((deprecated))
#else
# define DEPRECATED__moveit_master__action__ExecuteSequence_SendGoal_Request __declspec(deprecated)
#endif

namespace moveit_master
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct ExecuteSequence_SendGoal_Request_
{
  using Type = ExecuteSequence_SendGoal_Request_<ContainerAllocator>;

  explicit ExecuteSequence_SendGoal_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_init),
    goal(_init)
  {
    (void)_init;
  }

  explicit ExecuteSequence_SendGoal_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_alloc, _init),
    goal(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _goal_id_type =
    unique_identifier_msgs::msg::UUID_<ContainerAllocator>;
  _goal_id_type goal_id;
  using _goal_type =
    moveit_master::action::ExecuteSequence_Goal_<ContainerAllocator>;
  _goal_type goal;

  // setters for named parameter idiom
  Type & set__goal_id(
    const unique_identifier_msgs::msg::UUID_<ContainerAllocator> & _arg)
  {
    this->goal_id = _arg;
    return *this;
  }
  Type & set__goal(
    const moveit_master::action::ExecuteSequence_Goal_<ContainerAllocator> & _arg)
  {
    this->goal = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    moveit_master::action::ExecuteSequence_SendGoal_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const moveit_master::action::ExecuteSequence_SendGoal_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<moveit_master::action::ExecuteSequence_SendGoal_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<moveit_master::action::ExecuteSequence_SendGoal_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      moveit_master::action::ExecuteSequence_SendGoal_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<moveit_master::action::ExecuteSequence_SendGoal_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      moveit_master::action::ExecuteSequence_SendGoal_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<moveit_master::action::ExecuteSequence_SendGoal_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<moveit_master::action::ExecuteSequence_SendGoal_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<moveit_master::action::ExecuteSequence_SendGoal_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__moveit_master__action__ExecuteSequence_SendGoal_Request
    std::shared_ptr<moveit_master::action::ExecuteSequence_SendGoal_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__moveit_master__action__ExecuteSequence_SendGoal_Request
    std::shared_ptr<moveit_master::action::ExecuteSequence_SendGoal_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ExecuteSequence_SendGoal_Request_ & other) const
  {
    if (this->goal_id != other.goal_id) {
      return false;
    }
    if (this->goal != other.goal) {
      return false;
    }
    return true;
  }
  bool operator!=(const ExecuteSequence_SendGoal_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ExecuteSequence_SendGoal_Request_

// alias to use template instance with default allocator
using ExecuteSequence_SendGoal_Request =
  moveit_master::action::ExecuteSequence_SendGoal_Request_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace moveit_master


// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__moveit_master__action__ExecuteSequence_SendGoal_Response __attribute__((deprecated))
#else
# define DEPRECATED__moveit_master__action__ExecuteSequence_SendGoal_Response __declspec(deprecated)
#endif

namespace moveit_master
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct ExecuteSequence_SendGoal_Response_
{
  using Type = ExecuteSequence_SendGoal_Response_<ContainerAllocator>;

  explicit ExecuteSequence_SendGoal_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : stamp(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->accepted = false;
    }
  }

  explicit ExecuteSequence_SendGoal_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : stamp(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->accepted = false;
    }
  }

  // field types and members
  using _accepted_type =
    bool;
  _accepted_type accepted;
  using _stamp_type =
    builtin_interfaces::msg::Time_<ContainerAllocator>;
  _stamp_type stamp;

  // setters for named parameter idiom
  Type & set__accepted(
    const bool & _arg)
  {
    this->accepted = _arg;
    return *this;
  }
  Type & set__stamp(
    const builtin_interfaces::msg::Time_<ContainerAllocator> & _arg)
  {
    this->stamp = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    moveit_master::action::ExecuteSequence_SendGoal_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const moveit_master::action::ExecuteSequence_SendGoal_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<moveit_master::action::ExecuteSequence_SendGoal_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<moveit_master::action::ExecuteSequence_SendGoal_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      moveit_master::action::ExecuteSequence_SendGoal_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<moveit_master::action::ExecuteSequence_SendGoal_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      moveit_master::action::ExecuteSequence_SendGoal_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<moveit_master::action::ExecuteSequence_SendGoal_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<moveit_master::action::ExecuteSequence_SendGoal_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<moveit_master::action::ExecuteSequence_SendGoal_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__moveit_master__action__ExecuteSequence_SendGoal_Response
    std::shared_ptr<moveit_master::action::ExecuteSequence_SendGoal_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__moveit_master__action__ExecuteSequence_SendGoal_Response
    std::shared_ptr<moveit_master::action::ExecuteSequence_SendGoal_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ExecuteSequence_SendGoal_Response_ & other) const
  {
    if (this->accepted != other.accepted) {
      return false;
    }
    if (this->stamp != other.stamp) {
      return false;
    }
    return true;
  }
  bool operator!=(const ExecuteSequence_SendGoal_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ExecuteSequence_SendGoal_Response_

// alias to use template instance with default allocator
using ExecuteSequence_SendGoal_Response =
  moveit_master::action::ExecuteSequence_SendGoal_Response_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace moveit_master

namespace moveit_master
{

namespace action
{

struct ExecuteSequence_SendGoal
{
  using Request = moveit_master::action::ExecuteSequence_SendGoal_Request;
  using Response = moveit_master::action::ExecuteSequence_SendGoal_Response;
};

}  // namespace action

}  // namespace moveit_master


// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__moveit_master__action__ExecuteSequence_GetResult_Request __attribute__((deprecated))
#else
# define DEPRECATED__moveit_master__action__ExecuteSequence_GetResult_Request __declspec(deprecated)
#endif

namespace moveit_master
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct ExecuteSequence_GetResult_Request_
{
  using Type = ExecuteSequence_GetResult_Request_<ContainerAllocator>;

  explicit ExecuteSequence_GetResult_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_init)
  {
    (void)_init;
  }

  explicit ExecuteSequence_GetResult_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _goal_id_type =
    unique_identifier_msgs::msg::UUID_<ContainerAllocator>;
  _goal_id_type goal_id;

  // setters for named parameter idiom
  Type & set__goal_id(
    const unique_identifier_msgs::msg::UUID_<ContainerAllocator> & _arg)
  {
    this->goal_id = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    moveit_master::action::ExecuteSequence_GetResult_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const moveit_master::action::ExecuteSequence_GetResult_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<moveit_master::action::ExecuteSequence_GetResult_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<moveit_master::action::ExecuteSequence_GetResult_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      moveit_master::action::ExecuteSequence_GetResult_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<moveit_master::action::ExecuteSequence_GetResult_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      moveit_master::action::ExecuteSequence_GetResult_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<moveit_master::action::ExecuteSequence_GetResult_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<moveit_master::action::ExecuteSequence_GetResult_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<moveit_master::action::ExecuteSequence_GetResult_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__moveit_master__action__ExecuteSequence_GetResult_Request
    std::shared_ptr<moveit_master::action::ExecuteSequence_GetResult_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__moveit_master__action__ExecuteSequence_GetResult_Request
    std::shared_ptr<moveit_master::action::ExecuteSequence_GetResult_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ExecuteSequence_GetResult_Request_ & other) const
  {
    if (this->goal_id != other.goal_id) {
      return false;
    }
    return true;
  }
  bool operator!=(const ExecuteSequence_GetResult_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ExecuteSequence_GetResult_Request_

// alias to use template instance with default allocator
using ExecuteSequence_GetResult_Request =
  moveit_master::action::ExecuteSequence_GetResult_Request_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace moveit_master


// Include directives for member types
// Member 'result'
// already included above
// #include "moveit_master/action/detail/execute_sequence__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__moveit_master__action__ExecuteSequence_GetResult_Response __attribute__((deprecated))
#else
# define DEPRECATED__moveit_master__action__ExecuteSequence_GetResult_Response __declspec(deprecated)
#endif

namespace moveit_master
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct ExecuteSequence_GetResult_Response_
{
  using Type = ExecuteSequence_GetResult_Response_<ContainerAllocator>;

  explicit ExecuteSequence_GetResult_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : result(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->status = 0;
    }
  }

  explicit ExecuteSequence_GetResult_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : result(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->status = 0;
    }
  }

  // field types and members
  using _status_type =
    int8_t;
  _status_type status;
  using _result_type =
    moveit_master::action::ExecuteSequence_Result_<ContainerAllocator>;
  _result_type result;

  // setters for named parameter idiom
  Type & set__status(
    const int8_t & _arg)
  {
    this->status = _arg;
    return *this;
  }
  Type & set__result(
    const moveit_master::action::ExecuteSequence_Result_<ContainerAllocator> & _arg)
  {
    this->result = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    moveit_master::action::ExecuteSequence_GetResult_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const moveit_master::action::ExecuteSequence_GetResult_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<moveit_master::action::ExecuteSequence_GetResult_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<moveit_master::action::ExecuteSequence_GetResult_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      moveit_master::action::ExecuteSequence_GetResult_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<moveit_master::action::ExecuteSequence_GetResult_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      moveit_master::action::ExecuteSequence_GetResult_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<moveit_master::action::ExecuteSequence_GetResult_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<moveit_master::action::ExecuteSequence_GetResult_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<moveit_master::action::ExecuteSequence_GetResult_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__moveit_master__action__ExecuteSequence_GetResult_Response
    std::shared_ptr<moveit_master::action::ExecuteSequence_GetResult_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__moveit_master__action__ExecuteSequence_GetResult_Response
    std::shared_ptr<moveit_master::action::ExecuteSequence_GetResult_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ExecuteSequence_GetResult_Response_ & other) const
  {
    if (this->status != other.status) {
      return false;
    }
    if (this->result != other.result) {
      return false;
    }
    return true;
  }
  bool operator!=(const ExecuteSequence_GetResult_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ExecuteSequence_GetResult_Response_

// alias to use template instance with default allocator
using ExecuteSequence_GetResult_Response =
  moveit_master::action::ExecuteSequence_GetResult_Response_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace moveit_master

namespace moveit_master
{

namespace action
{

struct ExecuteSequence_GetResult
{
  using Request = moveit_master::action::ExecuteSequence_GetResult_Request;
  using Response = moveit_master::action::ExecuteSequence_GetResult_Response;
};

}  // namespace action

}  // namespace moveit_master


// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.hpp"
// Member 'feedback'
// already included above
// #include "moveit_master/action/detail/execute_sequence__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__moveit_master__action__ExecuteSequence_FeedbackMessage __attribute__((deprecated))
#else
# define DEPRECATED__moveit_master__action__ExecuteSequence_FeedbackMessage __declspec(deprecated)
#endif

namespace moveit_master
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct ExecuteSequence_FeedbackMessage_
{
  using Type = ExecuteSequence_FeedbackMessage_<ContainerAllocator>;

  explicit ExecuteSequence_FeedbackMessage_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_init),
    feedback(_init)
  {
    (void)_init;
  }

  explicit ExecuteSequence_FeedbackMessage_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_alloc, _init),
    feedback(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _goal_id_type =
    unique_identifier_msgs::msg::UUID_<ContainerAllocator>;
  _goal_id_type goal_id;
  using _feedback_type =
    moveit_master::action::ExecuteSequence_Feedback_<ContainerAllocator>;
  _feedback_type feedback;

  // setters for named parameter idiom
  Type & set__goal_id(
    const unique_identifier_msgs::msg::UUID_<ContainerAllocator> & _arg)
  {
    this->goal_id = _arg;
    return *this;
  }
  Type & set__feedback(
    const moveit_master::action::ExecuteSequence_Feedback_<ContainerAllocator> & _arg)
  {
    this->feedback = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    moveit_master::action::ExecuteSequence_FeedbackMessage_<ContainerAllocator> *;
  using ConstRawPtr =
    const moveit_master::action::ExecuteSequence_FeedbackMessage_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<moveit_master::action::ExecuteSequence_FeedbackMessage_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<moveit_master::action::ExecuteSequence_FeedbackMessage_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      moveit_master::action::ExecuteSequence_FeedbackMessage_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<moveit_master::action::ExecuteSequence_FeedbackMessage_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      moveit_master::action::ExecuteSequence_FeedbackMessage_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<moveit_master::action::ExecuteSequence_FeedbackMessage_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<moveit_master::action::ExecuteSequence_FeedbackMessage_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<moveit_master::action::ExecuteSequence_FeedbackMessage_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__moveit_master__action__ExecuteSequence_FeedbackMessage
    std::shared_ptr<moveit_master::action::ExecuteSequence_FeedbackMessage_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__moveit_master__action__ExecuteSequence_FeedbackMessage
    std::shared_ptr<moveit_master::action::ExecuteSequence_FeedbackMessage_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ExecuteSequence_FeedbackMessage_ & other) const
  {
    if (this->goal_id != other.goal_id) {
      return false;
    }
    if (this->feedback != other.feedback) {
      return false;
    }
    return true;
  }
  bool operator!=(const ExecuteSequence_FeedbackMessage_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ExecuteSequence_FeedbackMessage_

// alias to use template instance with default allocator
using ExecuteSequence_FeedbackMessage =
  moveit_master::action::ExecuteSequence_FeedbackMessage_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace moveit_master

#include "action_msgs/srv/cancel_goal.hpp"
#include "action_msgs/msg/goal_info.hpp"
#include "action_msgs/msg/goal_status_array.hpp"

namespace moveit_master
{

namespace action
{

struct ExecuteSequence
{
  /// The goal message defined in the action definition.
  using Goal = moveit_master::action::ExecuteSequence_Goal;
  /// The result message defined in the action definition.
  using Result = moveit_master::action::ExecuteSequence_Result;
  /// The feedback message defined in the action definition.
  using Feedback = moveit_master::action::ExecuteSequence_Feedback;

  struct Impl
  {
    /// The send_goal service using a wrapped version of the goal message as a request.
    using SendGoalService = moveit_master::action::ExecuteSequence_SendGoal;
    /// The get_result service using a wrapped version of the result message as a response.
    using GetResultService = moveit_master::action::ExecuteSequence_GetResult;
    /// The feedback message with generic fields which wraps the feedback message.
    using FeedbackMessage = moveit_master::action::ExecuteSequence_FeedbackMessage;

    /// The generic service to cancel a goal.
    using CancelGoalService = action_msgs::srv::CancelGoal;
    /// The generic message for the status of a goal.
    using GoalStatusMessage = action_msgs::msg::GoalStatusArray;
  };
};

typedef struct ExecuteSequence ExecuteSequence;

}  // namespace action

}  // namespace moveit_master

#endif  // MOVEIT_MASTER__ACTION__DETAIL__EXECUTE_SEQUENCE__STRUCT_HPP_
