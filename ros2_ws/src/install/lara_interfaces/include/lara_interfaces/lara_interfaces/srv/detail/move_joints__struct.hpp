// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from lara_interfaces:srv/MoveJoints.idl
// generated code does not contain a copyright notice

#ifndef LARA_INTERFACES__SRV__DETAIL__MOVE_JOINTS__STRUCT_HPP_
#define LARA_INTERFACES__SRV__DETAIL__MOVE_JOINTS__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__lara_interfaces__srv__MoveJoints_Request __attribute__((deprecated))
#else
# define DEPRECATED__lara_interfaces__srv__MoveJoints_Request __declspec(deprecated)
#endif

namespace lara_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct MoveJoints_Request_
{
  using Type = MoveJoints_Request_<ContainerAllocator>;

  explicit MoveJoints_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->point_name = "";
      this->speed = 0.0;
      this->acceleration = 0.0;
      this->enable_safety = false;
    }
  }

  explicit MoveJoints_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : point_name(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->point_name = "";
      this->speed = 0.0;
      this->acceleration = 0.0;
      this->enable_safety = false;
    }
  }

  // field types and members
  using _point_name_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _point_name_type point_name;
  using _target_joint_type =
    std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>>;
  _target_joint_type target_joint;
  using _target_pose_type =
    std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>>;
  _target_pose_type target_pose;
  using _speed_type =
    double;
  _speed_type speed;
  using _acceleration_type =
    double;
  _acceleration_type acceleration;
  using _enable_safety_type =
    bool;
  _enable_safety_type enable_safety;

  // setters for named parameter idiom
  Type & set__point_name(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->point_name = _arg;
    return *this;
  }
  Type & set__target_joint(
    const std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>> & _arg)
  {
    this->target_joint = _arg;
    return *this;
  }
  Type & set__target_pose(
    const std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>> & _arg)
  {
    this->target_pose = _arg;
    return *this;
  }
  Type & set__speed(
    const double & _arg)
  {
    this->speed = _arg;
    return *this;
  }
  Type & set__acceleration(
    const double & _arg)
  {
    this->acceleration = _arg;
    return *this;
  }
  Type & set__enable_safety(
    const bool & _arg)
  {
    this->enable_safety = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    lara_interfaces::srv::MoveJoints_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const lara_interfaces::srv::MoveJoints_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<lara_interfaces::srv::MoveJoints_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<lara_interfaces::srv::MoveJoints_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      lara_interfaces::srv::MoveJoints_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<lara_interfaces::srv::MoveJoints_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      lara_interfaces::srv::MoveJoints_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<lara_interfaces::srv::MoveJoints_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<lara_interfaces::srv::MoveJoints_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<lara_interfaces::srv::MoveJoints_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__lara_interfaces__srv__MoveJoints_Request
    std::shared_ptr<lara_interfaces::srv::MoveJoints_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__lara_interfaces__srv__MoveJoints_Request
    std::shared_ptr<lara_interfaces::srv::MoveJoints_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MoveJoints_Request_ & other) const
  {
    if (this->point_name != other.point_name) {
      return false;
    }
    if (this->target_joint != other.target_joint) {
      return false;
    }
    if (this->target_pose != other.target_pose) {
      return false;
    }
    if (this->speed != other.speed) {
      return false;
    }
    if (this->acceleration != other.acceleration) {
      return false;
    }
    if (this->enable_safety != other.enable_safety) {
      return false;
    }
    return true;
  }
  bool operator!=(const MoveJoints_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MoveJoints_Request_

// alias to use template instance with default allocator
using MoveJoints_Request =
  lara_interfaces::srv::MoveJoints_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace lara_interfaces


#ifndef _WIN32
# define DEPRECATED__lara_interfaces__srv__MoveJoints_Response __attribute__((deprecated))
#else
# define DEPRECATED__lara_interfaces__srv__MoveJoints_Response __declspec(deprecated)
#endif

namespace lara_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct MoveJoints_Response_
{
  using Type = MoveJoints_Response_<ContainerAllocator>;

  explicit MoveJoints_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->message = "";
    }
  }

  explicit MoveJoints_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : message(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->message = "";
    }
  }

  // field types and members
  using _success_type =
    bool;
  _success_type success;
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
  Type & set__message(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->message = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    lara_interfaces::srv::MoveJoints_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const lara_interfaces::srv::MoveJoints_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<lara_interfaces::srv::MoveJoints_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<lara_interfaces::srv::MoveJoints_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      lara_interfaces::srv::MoveJoints_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<lara_interfaces::srv::MoveJoints_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      lara_interfaces::srv::MoveJoints_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<lara_interfaces::srv::MoveJoints_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<lara_interfaces::srv::MoveJoints_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<lara_interfaces::srv::MoveJoints_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__lara_interfaces__srv__MoveJoints_Response
    std::shared_ptr<lara_interfaces::srv::MoveJoints_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__lara_interfaces__srv__MoveJoints_Response
    std::shared_ptr<lara_interfaces::srv::MoveJoints_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MoveJoints_Response_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    if (this->message != other.message) {
      return false;
    }
    return true;
  }
  bool operator!=(const MoveJoints_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MoveJoints_Response_

// alias to use template instance with default allocator
using MoveJoints_Response =
  lara_interfaces::srv::MoveJoints_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace lara_interfaces

namespace lara_interfaces
{

namespace srv
{

struct MoveJoints
{
  using Request = lara_interfaces::srv::MoveJoints_Request;
  using Response = lara_interfaces::srv::MoveJoints_Response;
};

}  // namespace srv

}  // namespace lara_interfaces

#endif  // LARA_INTERFACES__SRV__DETAIL__MOVE_JOINTS__STRUCT_HPP_
