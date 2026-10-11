// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from moveit_master:msg/MotionStep.idl
// generated code does not contain a copyright notice

#ifndef MOVEIT_MASTER__MSG__DETAIL__MOTION_STEP__STRUCT_HPP_
#define MOVEIT_MASTER__MSG__DETAIL__MOTION_STEP__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'pose'
#include "geometry_msgs/msg/detail/pose__struct.hpp"
// Member 'offset'
#include "geometry_msgs/msg/detail/vector3__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__moveit_master__msg__MotionStep __attribute__((deprecated))
#else
# define DEPRECATED__moveit_master__msg__MotionStep __declspec(deprecated)
#endif

namespace moveit_master
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct MotionStep_
{
  using Type = MotionStep_<ContainerAllocator>;

  explicit MotionStep_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : pose(_init),
    offset(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->type = 0;
      this->named_target = "";
      this->duration = 0.0;
      this->joint_value = 0.0;
      this->object_id = "";
      this->allow = false;
    }
  }

  explicit MotionStep_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : pose(_alloc, _init),
    named_target(_alloc),
    offset(_alloc, _init),
    object_id(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->type = 0;
      this->named_target = "";
      this->duration = 0.0;
      this->joint_value = 0.0;
      this->object_id = "";
      this->allow = false;
    }
  }

  // field types and members
  using _type_type =
    uint8_t;
  _type_type type;
  using _pose_type =
    geometry_msgs::msg::Pose_<ContainerAllocator>;
  _pose_type pose;
  using _named_target_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _named_target_type named_target;
  using _duration_type =
    double;
  _duration_type duration;
  using _joint_value_type =
    double;
  _joint_value_type joint_value;
  using _offset_type =
    geometry_msgs::msg::Vector3_<ContainerAllocator>;
  _offset_type offset;
  using _object_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _object_id_type object_id;
  using _touch_links_type =
    std::vector<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>>;
  _touch_links_type touch_links;
  using _allow_type =
    bool;
  _allow_type allow;

  // setters for named parameter idiom
  Type & set__type(
    const uint8_t & _arg)
  {
    this->type = _arg;
    return *this;
  }
  Type & set__pose(
    const geometry_msgs::msg::Pose_<ContainerAllocator> & _arg)
  {
    this->pose = _arg;
    return *this;
  }
  Type & set__named_target(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->named_target = _arg;
    return *this;
  }
  Type & set__duration(
    const double & _arg)
  {
    this->duration = _arg;
    return *this;
  }
  Type & set__joint_value(
    const double & _arg)
  {
    this->joint_value = _arg;
    return *this;
  }
  Type & set__offset(
    const geometry_msgs::msg::Vector3_<ContainerAllocator> & _arg)
  {
    this->offset = _arg;
    return *this;
  }
  Type & set__object_id(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->object_id = _arg;
    return *this;
  }
  Type & set__touch_links(
    const std::vector<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>> & _arg)
  {
    this->touch_links = _arg;
    return *this;
  }
  Type & set__allow(
    const bool & _arg)
  {
    this->allow = _arg;
    return *this;
  }

  // constant declarations
  static constexpr uint8_t ARM_POSE =
    0u;
  static constexpr uint8_t ARM_NAMED =
    1u;
  static constexpr uint8_t GRIPPER_NAMED =
    2u;
  static constexpr uint8_t WAIT =
    3u;
  static constexpr uint8_t GRIPPER_JOINT =
    4u;
  static constexpr uint8_t ARM_CARTESIAN =
    5u;
  static constexpr uint8_t ATTACH =
    6u;
  static constexpr uint8_t DETACH =
    7u;
  static constexpr uint8_t ALLOW_COLLISION =
    8u;

  // pointer types
  using RawPtr =
    moveit_master::msg::MotionStep_<ContainerAllocator> *;
  using ConstRawPtr =
    const moveit_master::msg::MotionStep_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<moveit_master::msg::MotionStep_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<moveit_master::msg::MotionStep_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      moveit_master::msg::MotionStep_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<moveit_master::msg::MotionStep_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      moveit_master::msg::MotionStep_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<moveit_master::msg::MotionStep_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<moveit_master::msg::MotionStep_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<moveit_master::msg::MotionStep_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__moveit_master__msg__MotionStep
    std::shared_ptr<moveit_master::msg::MotionStep_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__moveit_master__msg__MotionStep
    std::shared_ptr<moveit_master::msg::MotionStep_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MotionStep_ & other) const
  {
    if (this->type != other.type) {
      return false;
    }
    if (this->pose != other.pose) {
      return false;
    }
    if (this->named_target != other.named_target) {
      return false;
    }
    if (this->duration != other.duration) {
      return false;
    }
    if (this->joint_value != other.joint_value) {
      return false;
    }
    if (this->offset != other.offset) {
      return false;
    }
    if (this->object_id != other.object_id) {
      return false;
    }
    if (this->touch_links != other.touch_links) {
      return false;
    }
    if (this->allow != other.allow) {
      return false;
    }
    return true;
  }
  bool operator!=(const MotionStep_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MotionStep_

// alias to use template instance with default allocator
using MotionStep =
  moveit_master::msg::MotionStep_<std::allocator<void>>;

// constant definitions
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t MotionStep_<ContainerAllocator>::ARM_POSE;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t MotionStep_<ContainerAllocator>::ARM_NAMED;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t MotionStep_<ContainerAllocator>::GRIPPER_NAMED;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t MotionStep_<ContainerAllocator>::WAIT;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t MotionStep_<ContainerAllocator>::GRIPPER_JOINT;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t MotionStep_<ContainerAllocator>::ARM_CARTESIAN;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t MotionStep_<ContainerAllocator>::ATTACH;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t MotionStep_<ContainerAllocator>::DETACH;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t MotionStep_<ContainerAllocator>::ALLOW_COLLISION;
#endif  // __cplusplus < 201703L

}  // namespace msg

}  // namespace moveit_master

#endif  // MOVEIT_MASTER__MSG__DETAIL__MOTION_STEP__STRUCT_HPP_
