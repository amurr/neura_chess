// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from chess_interfaces:action/ChessBoard.idl
// generated code does not contain a copyright notice

#ifndef CHESS_INTERFACES__ACTION__DETAIL__CHESS_BOARD__STRUCT_HPP_
#define CHESS_INTERFACES__ACTION__DETAIL__CHESS_BOARD__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__chess_interfaces__action__ChessBoard_Goal __attribute__((deprecated))
#else
# define DEPRECATED__chess_interfaces__action__ChessBoard_Goal __declspec(deprecated)
#endif

namespace chess_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct ChessBoard_Goal_
{
  using Type = ChessBoard_Goal_<ContainerAllocator>;

  explicit ChessBoard_Goal_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->change_status = "";
      this->piece_type = "";
      this->to_pick = "";
      this->to_place = "";
      this->fen = "";
    }
  }

  explicit ChessBoard_Goal_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : change_status(_alloc),
    piece_type(_alloc),
    to_pick(_alloc),
    to_place(_alloc),
    fen(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->change_status = "";
      this->piece_type = "";
      this->to_pick = "";
      this->to_place = "";
      this->fen = "";
    }
  }

  // field types and members
  using _change_status_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _change_status_type change_status;
  using _piece_type_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _piece_type_type piece_type;
  using _to_pick_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _to_pick_type to_pick;
  using _to_place_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _to_place_type to_place;
  using _fen_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _fen_type fen;

  // setters for named parameter idiom
  Type & set__change_status(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->change_status = _arg;
    return *this;
  }
  Type & set__piece_type(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->piece_type = _arg;
    return *this;
  }
  Type & set__to_pick(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->to_pick = _arg;
    return *this;
  }
  Type & set__to_place(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->to_place = _arg;
    return *this;
  }
  Type & set__fen(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->fen = _arg;
    return *this;
  }

  // constant declarations
  static const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> ACTIVE;
  static const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> PASSIVE;

  // pointer types
  using RawPtr =
    chess_interfaces::action::ChessBoard_Goal_<ContainerAllocator> *;
  using ConstRawPtr =
    const chess_interfaces::action::ChessBoard_Goal_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<chess_interfaces::action::ChessBoard_Goal_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<chess_interfaces::action::ChessBoard_Goal_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      chess_interfaces::action::ChessBoard_Goal_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<chess_interfaces::action::ChessBoard_Goal_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      chess_interfaces::action::ChessBoard_Goal_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<chess_interfaces::action::ChessBoard_Goal_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<chess_interfaces::action::ChessBoard_Goal_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<chess_interfaces::action::ChessBoard_Goal_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__chess_interfaces__action__ChessBoard_Goal
    std::shared_ptr<chess_interfaces::action::ChessBoard_Goal_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__chess_interfaces__action__ChessBoard_Goal
    std::shared_ptr<chess_interfaces::action::ChessBoard_Goal_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ChessBoard_Goal_ & other) const
  {
    if (this->change_status != other.change_status) {
      return false;
    }
    if (this->piece_type != other.piece_type) {
      return false;
    }
    if (this->to_pick != other.to_pick) {
      return false;
    }
    if (this->to_place != other.to_place) {
      return false;
    }
    if (this->fen != other.fen) {
      return false;
    }
    return true;
  }
  bool operator!=(const ChessBoard_Goal_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ChessBoard_Goal_

// alias to use template instance with default allocator
using ChessBoard_Goal =
  chess_interfaces::action::ChessBoard_Goal_<std::allocator<void>>;

// constant definitions
template<typename ContainerAllocator>
const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>
ChessBoard_Goal_<ContainerAllocator>::ACTIVE = "active";
template<typename ContainerAllocator>
const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>
ChessBoard_Goal_<ContainerAllocator>::PASSIVE = "passive";

}  // namespace action

}  // namespace chess_interfaces


#ifndef _WIN32
# define DEPRECATED__chess_interfaces__action__ChessBoard_Result __attribute__((deprecated))
#else
# define DEPRECATED__chess_interfaces__action__ChessBoard_Result __declspec(deprecated)
#endif

namespace chess_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct ChessBoard_Result_
{
  using Type = ChessBoard_Result_<ContainerAllocator>;

  explicit ChessBoard_Result_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->message = "";
      this->fen = "";
    }
  }

  explicit ChessBoard_Result_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : message(_alloc),
    fen(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->message = "";
      this->fen = "";
    }
  }

  // field types and members
  using _success_type =
    bool;
  _success_type success;
  using _message_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _message_type message;
  using _fen_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _fen_type fen;

  // setters for named parameter idiom
  Type & set__success(
    const bool & _arg)
  {
    this->success = _arg;
    return *this;
  }
  Type & set__message(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->message = _arg;
    return *this;
  }
  Type & set__fen(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->fen = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    chess_interfaces::action::ChessBoard_Result_<ContainerAllocator> *;
  using ConstRawPtr =
    const chess_interfaces::action::ChessBoard_Result_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<chess_interfaces::action::ChessBoard_Result_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<chess_interfaces::action::ChessBoard_Result_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      chess_interfaces::action::ChessBoard_Result_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<chess_interfaces::action::ChessBoard_Result_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      chess_interfaces::action::ChessBoard_Result_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<chess_interfaces::action::ChessBoard_Result_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<chess_interfaces::action::ChessBoard_Result_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<chess_interfaces::action::ChessBoard_Result_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__chess_interfaces__action__ChessBoard_Result
    std::shared_ptr<chess_interfaces::action::ChessBoard_Result_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__chess_interfaces__action__ChessBoard_Result
    std::shared_ptr<chess_interfaces::action::ChessBoard_Result_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ChessBoard_Result_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    if (this->message != other.message) {
      return false;
    }
    if (this->fen != other.fen) {
      return false;
    }
    return true;
  }
  bool operator!=(const ChessBoard_Result_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ChessBoard_Result_

// alias to use template instance with default allocator
using ChessBoard_Result =
  chess_interfaces::action::ChessBoard_Result_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace chess_interfaces


#ifndef _WIN32
# define DEPRECATED__chess_interfaces__action__ChessBoard_Feedback __attribute__((deprecated))
#else
# define DEPRECATED__chess_interfaces__action__ChessBoard_Feedback __declspec(deprecated)
#endif

namespace chess_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct ChessBoard_Feedback_
{
  using Type = ChessBoard_Feedback_<ContainerAllocator>;

  explicit ChessBoard_Feedback_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->stage = "";
    }
  }

  explicit ChessBoard_Feedback_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : stage(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->stage = "";
    }
  }

  // field types and members
  using _stage_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _stage_type stage;

  // setters for named parameter idiom
  Type & set__stage(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->stage = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    chess_interfaces::action::ChessBoard_Feedback_<ContainerAllocator> *;
  using ConstRawPtr =
    const chess_interfaces::action::ChessBoard_Feedback_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<chess_interfaces::action::ChessBoard_Feedback_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<chess_interfaces::action::ChessBoard_Feedback_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      chess_interfaces::action::ChessBoard_Feedback_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<chess_interfaces::action::ChessBoard_Feedback_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      chess_interfaces::action::ChessBoard_Feedback_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<chess_interfaces::action::ChessBoard_Feedback_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<chess_interfaces::action::ChessBoard_Feedback_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<chess_interfaces::action::ChessBoard_Feedback_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__chess_interfaces__action__ChessBoard_Feedback
    std::shared_ptr<chess_interfaces::action::ChessBoard_Feedback_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__chess_interfaces__action__ChessBoard_Feedback
    std::shared_ptr<chess_interfaces::action::ChessBoard_Feedback_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ChessBoard_Feedback_ & other) const
  {
    if (this->stage != other.stage) {
      return false;
    }
    return true;
  }
  bool operator!=(const ChessBoard_Feedback_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ChessBoard_Feedback_

// alias to use template instance with default allocator
using ChessBoard_Feedback =
  chess_interfaces::action::ChessBoard_Feedback_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace chess_interfaces


// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__struct.hpp"
// Member 'goal'
#include "chess_interfaces/action/detail/chess_board__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__chess_interfaces__action__ChessBoard_SendGoal_Request __attribute__((deprecated))
#else
# define DEPRECATED__chess_interfaces__action__ChessBoard_SendGoal_Request __declspec(deprecated)
#endif

namespace chess_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct ChessBoard_SendGoal_Request_
{
  using Type = ChessBoard_SendGoal_Request_<ContainerAllocator>;

  explicit ChessBoard_SendGoal_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_init),
    goal(_init)
  {
    (void)_init;
  }

  explicit ChessBoard_SendGoal_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
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
    chess_interfaces::action::ChessBoard_Goal_<ContainerAllocator>;
  _goal_type goal;

  // setters for named parameter idiom
  Type & set__goal_id(
    const unique_identifier_msgs::msg::UUID_<ContainerAllocator> & _arg)
  {
    this->goal_id = _arg;
    return *this;
  }
  Type & set__goal(
    const chess_interfaces::action::ChessBoard_Goal_<ContainerAllocator> & _arg)
  {
    this->goal = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    chess_interfaces::action::ChessBoard_SendGoal_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const chess_interfaces::action::ChessBoard_SendGoal_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<chess_interfaces::action::ChessBoard_SendGoal_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<chess_interfaces::action::ChessBoard_SendGoal_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      chess_interfaces::action::ChessBoard_SendGoal_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<chess_interfaces::action::ChessBoard_SendGoal_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      chess_interfaces::action::ChessBoard_SendGoal_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<chess_interfaces::action::ChessBoard_SendGoal_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<chess_interfaces::action::ChessBoard_SendGoal_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<chess_interfaces::action::ChessBoard_SendGoal_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__chess_interfaces__action__ChessBoard_SendGoal_Request
    std::shared_ptr<chess_interfaces::action::ChessBoard_SendGoal_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__chess_interfaces__action__ChessBoard_SendGoal_Request
    std::shared_ptr<chess_interfaces::action::ChessBoard_SendGoal_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ChessBoard_SendGoal_Request_ & other) const
  {
    if (this->goal_id != other.goal_id) {
      return false;
    }
    if (this->goal != other.goal) {
      return false;
    }
    return true;
  }
  bool operator!=(const ChessBoard_SendGoal_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ChessBoard_SendGoal_Request_

// alias to use template instance with default allocator
using ChessBoard_SendGoal_Request =
  chess_interfaces::action::ChessBoard_SendGoal_Request_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace chess_interfaces


// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__chess_interfaces__action__ChessBoard_SendGoal_Response __attribute__((deprecated))
#else
# define DEPRECATED__chess_interfaces__action__ChessBoard_SendGoal_Response __declspec(deprecated)
#endif

namespace chess_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct ChessBoard_SendGoal_Response_
{
  using Type = ChessBoard_SendGoal_Response_<ContainerAllocator>;

  explicit ChessBoard_SendGoal_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : stamp(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->accepted = false;
    }
  }

  explicit ChessBoard_SendGoal_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
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
    chess_interfaces::action::ChessBoard_SendGoal_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const chess_interfaces::action::ChessBoard_SendGoal_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<chess_interfaces::action::ChessBoard_SendGoal_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<chess_interfaces::action::ChessBoard_SendGoal_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      chess_interfaces::action::ChessBoard_SendGoal_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<chess_interfaces::action::ChessBoard_SendGoal_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      chess_interfaces::action::ChessBoard_SendGoal_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<chess_interfaces::action::ChessBoard_SendGoal_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<chess_interfaces::action::ChessBoard_SendGoal_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<chess_interfaces::action::ChessBoard_SendGoal_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__chess_interfaces__action__ChessBoard_SendGoal_Response
    std::shared_ptr<chess_interfaces::action::ChessBoard_SendGoal_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__chess_interfaces__action__ChessBoard_SendGoal_Response
    std::shared_ptr<chess_interfaces::action::ChessBoard_SendGoal_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ChessBoard_SendGoal_Response_ & other) const
  {
    if (this->accepted != other.accepted) {
      return false;
    }
    if (this->stamp != other.stamp) {
      return false;
    }
    return true;
  }
  bool operator!=(const ChessBoard_SendGoal_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ChessBoard_SendGoal_Response_

// alias to use template instance with default allocator
using ChessBoard_SendGoal_Response =
  chess_interfaces::action::ChessBoard_SendGoal_Response_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace chess_interfaces

namespace chess_interfaces
{

namespace action
{

struct ChessBoard_SendGoal
{
  using Request = chess_interfaces::action::ChessBoard_SendGoal_Request;
  using Response = chess_interfaces::action::ChessBoard_SendGoal_Response;
};

}  // namespace action

}  // namespace chess_interfaces


// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__chess_interfaces__action__ChessBoard_GetResult_Request __attribute__((deprecated))
#else
# define DEPRECATED__chess_interfaces__action__ChessBoard_GetResult_Request __declspec(deprecated)
#endif

namespace chess_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct ChessBoard_GetResult_Request_
{
  using Type = ChessBoard_GetResult_Request_<ContainerAllocator>;

  explicit ChessBoard_GetResult_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_init)
  {
    (void)_init;
  }

  explicit ChessBoard_GetResult_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
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
    chess_interfaces::action::ChessBoard_GetResult_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const chess_interfaces::action::ChessBoard_GetResult_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<chess_interfaces::action::ChessBoard_GetResult_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<chess_interfaces::action::ChessBoard_GetResult_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      chess_interfaces::action::ChessBoard_GetResult_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<chess_interfaces::action::ChessBoard_GetResult_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      chess_interfaces::action::ChessBoard_GetResult_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<chess_interfaces::action::ChessBoard_GetResult_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<chess_interfaces::action::ChessBoard_GetResult_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<chess_interfaces::action::ChessBoard_GetResult_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__chess_interfaces__action__ChessBoard_GetResult_Request
    std::shared_ptr<chess_interfaces::action::ChessBoard_GetResult_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__chess_interfaces__action__ChessBoard_GetResult_Request
    std::shared_ptr<chess_interfaces::action::ChessBoard_GetResult_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ChessBoard_GetResult_Request_ & other) const
  {
    if (this->goal_id != other.goal_id) {
      return false;
    }
    return true;
  }
  bool operator!=(const ChessBoard_GetResult_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ChessBoard_GetResult_Request_

// alias to use template instance with default allocator
using ChessBoard_GetResult_Request =
  chess_interfaces::action::ChessBoard_GetResult_Request_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace chess_interfaces


// Include directives for member types
// Member 'result'
// already included above
// #include "chess_interfaces/action/detail/chess_board__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__chess_interfaces__action__ChessBoard_GetResult_Response __attribute__((deprecated))
#else
# define DEPRECATED__chess_interfaces__action__ChessBoard_GetResult_Response __declspec(deprecated)
#endif

namespace chess_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct ChessBoard_GetResult_Response_
{
  using Type = ChessBoard_GetResult_Response_<ContainerAllocator>;

  explicit ChessBoard_GetResult_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : result(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->status = 0;
    }
  }

  explicit ChessBoard_GetResult_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
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
    chess_interfaces::action::ChessBoard_Result_<ContainerAllocator>;
  _result_type result;

  // setters for named parameter idiom
  Type & set__status(
    const int8_t & _arg)
  {
    this->status = _arg;
    return *this;
  }
  Type & set__result(
    const chess_interfaces::action::ChessBoard_Result_<ContainerAllocator> & _arg)
  {
    this->result = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    chess_interfaces::action::ChessBoard_GetResult_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const chess_interfaces::action::ChessBoard_GetResult_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<chess_interfaces::action::ChessBoard_GetResult_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<chess_interfaces::action::ChessBoard_GetResult_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      chess_interfaces::action::ChessBoard_GetResult_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<chess_interfaces::action::ChessBoard_GetResult_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      chess_interfaces::action::ChessBoard_GetResult_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<chess_interfaces::action::ChessBoard_GetResult_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<chess_interfaces::action::ChessBoard_GetResult_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<chess_interfaces::action::ChessBoard_GetResult_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__chess_interfaces__action__ChessBoard_GetResult_Response
    std::shared_ptr<chess_interfaces::action::ChessBoard_GetResult_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__chess_interfaces__action__ChessBoard_GetResult_Response
    std::shared_ptr<chess_interfaces::action::ChessBoard_GetResult_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ChessBoard_GetResult_Response_ & other) const
  {
    if (this->status != other.status) {
      return false;
    }
    if (this->result != other.result) {
      return false;
    }
    return true;
  }
  bool operator!=(const ChessBoard_GetResult_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ChessBoard_GetResult_Response_

// alias to use template instance with default allocator
using ChessBoard_GetResult_Response =
  chess_interfaces::action::ChessBoard_GetResult_Response_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace chess_interfaces

namespace chess_interfaces
{

namespace action
{

struct ChessBoard_GetResult
{
  using Request = chess_interfaces::action::ChessBoard_GetResult_Request;
  using Response = chess_interfaces::action::ChessBoard_GetResult_Response;
};

}  // namespace action

}  // namespace chess_interfaces


// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.hpp"
// Member 'feedback'
// already included above
// #include "chess_interfaces/action/detail/chess_board__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__chess_interfaces__action__ChessBoard_FeedbackMessage __attribute__((deprecated))
#else
# define DEPRECATED__chess_interfaces__action__ChessBoard_FeedbackMessage __declspec(deprecated)
#endif

namespace chess_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct ChessBoard_FeedbackMessage_
{
  using Type = ChessBoard_FeedbackMessage_<ContainerAllocator>;

  explicit ChessBoard_FeedbackMessage_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_init),
    feedback(_init)
  {
    (void)_init;
  }

  explicit ChessBoard_FeedbackMessage_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
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
    chess_interfaces::action::ChessBoard_Feedback_<ContainerAllocator>;
  _feedback_type feedback;

  // setters for named parameter idiom
  Type & set__goal_id(
    const unique_identifier_msgs::msg::UUID_<ContainerAllocator> & _arg)
  {
    this->goal_id = _arg;
    return *this;
  }
  Type & set__feedback(
    const chess_interfaces::action::ChessBoard_Feedback_<ContainerAllocator> & _arg)
  {
    this->feedback = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    chess_interfaces::action::ChessBoard_FeedbackMessage_<ContainerAllocator> *;
  using ConstRawPtr =
    const chess_interfaces::action::ChessBoard_FeedbackMessage_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<chess_interfaces::action::ChessBoard_FeedbackMessage_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<chess_interfaces::action::ChessBoard_FeedbackMessage_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      chess_interfaces::action::ChessBoard_FeedbackMessage_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<chess_interfaces::action::ChessBoard_FeedbackMessage_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      chess_interfaces::action::ChessBoard_FeedbackMessage_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<chess_interfaces::action::ChessBoard_FeedbackMessage_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<chess_interfaces::action::ChessBoard_FeedbackMessage_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<chess_interfaces::action::ChessBoard_FeedbackMessage_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__chess_interfaces__action__ChessBoard_FeedbackMessage
    std::shared_ptr<chess_interfaces::action::ChessBoard_FeedbackMessage_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__chess_interfaces__action__ChessBoard_FeedbackMessage
    std::shared_ptr<chess_interfaces::action::ChessBoard_FeedbackMessage_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ChessBoard_FeedbackMessage_ & other) const
  {
    if (this->goal_id != other.goal_id) {
      return false;
    }
    if (this->feedback != other.feedback) {
      return false;
    }
    return true;
  }
  bool operator!=(const ChessBoard_FeedbackMessage_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ChessBoard_FeedbackMessage_

// alias to use template instance with default allocator
using ChessBoard_FeedbackMessage =
  chess_interfaces::action::ChessBoard_FeedbackMessage_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace chess_interfaces

#include "action_msgs/srv/cancel_goal.hpp"
#include "action_msgs/msg/goal_info.hpp"
#include "action_msgs/msg/goal_status_array.hpp"

namespace chess_interfaces
{

namespace action
{

struct ChessBoard
{
  /// The goal message defined in the action definition.
  using Goal = chess_interfaces::action::ChessBoard_Goal;
  /// The result message defined in the action definition.
  using Result = chess_interfaces::action::ChessBoard_Result;
  /// The feedback message defined in the action definition.
  using Feedback = chess_interfaces::action::ChessBoard_Feedback;

  struct Impl
  {
    /// The send_goal service using a wrapped version of the goal message as a request.
    using SendGoalService = chess_interfaces::action::ChessBoard_SendGoal;
    /// The get_result service using a wrapped version of the result message as a response.
    using GetResultService = chess_interfaces::action::ChessBoard_GetResult;
    /// The feedback message with generic fields which wraps the feedback message.
    using FeedbackMessage = chess_interfaces::action::ChessBoard_FeedbackMessage;

    /// The generic service to cancel a goal.
    using CancelGoalService = action_msgs::srv::CancelGoal;
    /// The generic message for the status of a goal.
    using GoalStatusMessage = action_msgs::msg::GoalStatusArray;
  };
};

typedef struct ChessBoard ChessBoard;

}  // namespace action

}  // namespace chess_interfaces

#endif  // CHESS_INTERFACES__ACTION__DETAIL__CHESS_BOARD__STRUCT_HPP_
