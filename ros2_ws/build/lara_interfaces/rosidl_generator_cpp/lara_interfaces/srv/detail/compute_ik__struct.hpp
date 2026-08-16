// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from lara_interfaces:srv/ComputeIK.idl
// generated code does not contain a copyright notice

#ifndef LARA_INTERFACES__SRV__DETAIL__COMPUTE_IK__STRUCT_HPP_
#define LARA_INTERFACES__SRV__DETAIL__COMPUTE_IK__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'target_pose'
#include "geometry_msgs/msg/detail/pose__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__lara_interfaces__srv__ComputeIK_Request __attribute__((deprecated))
#else
# define DEPRECATED__lara_interfaces__srv__ComputeIK_Request __declspec(deprecated)
#endif

namespace lara_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct ComputeIK_Request_
{
  using Type = ComputeIK_Request_<ContainerAllocator>;

  explicit ComputeIK_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : target_pose(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->timeout_sec = 0.0;
      this->position_tolerance = 0.0;
      this->orientation_tolerance = 0.0;
      this->enforce_joint_limits_mode = 0;
    }
  }

  explicit ComputeIK_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : target_pose(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->timeout_sec = 0.0;
      this->position_tolerance = 0.0;
      this->orientation_tolerance = 0.0;
      this->enforce_joint_limits_mode = 0;
    }
  }

  // field types and members
  using _target_pose_type =
    geometry_msgs::msg::Pose_<ContainerAllocator>;
  _target_pose_type target_pose;
  using _seed_joint_positions_type =
    std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>>;
  _seed_joint_positions_type seed_joint_positions;
  using _timeout_sec_type =
    double;
  _timeout_sec_type timeout_sec;
  using _position_tolerance_type =
    double;
  _position_tolerance_type position_tolerance;
  using _orientation_tolerance_type =
    double;
  _orientation_tolerance_type orientation_tolerance;
  using _enforce_joint_limits_mode_type =
    int8_t;
  _enforce_joint_limits_mode_type enforce_joint_limits_mode;

  // setters for named parameter idiom
  Type & set__target_pose(
    const geometry_msgs::msg::Pose_<ContainerAllocator> & _arg)
  {
    this->target_pose = _arg;
    return *this;
  }
  Type & set__seed_joint_positions(
    const std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>> & _arg)
  {
    this->seed_joint_positions = _arg;
    return *this;
  }
  Type & set__timeout_sec(
    const double & _arg)
  {
    this->timeout_sec = _arg;
    return *this;
  }
  Type & set__position_tolerance(
    const double & _arg)
  {
    this->position_tolerance = _arg;
    return *this;
  }
  Type & set__orientation_tolerance(
    const double & _arg)
  {
    this->orientation_tolerance = _arg;
    return *this;
  }
  Type & set__enforce_joint_limits_mode(
    const int8_t & _arg)
  {
    this->enforce_joint_limits_mode = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    lara_interfaces::srv::ComputeIK_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const lara_interfaces::srv::ComputeIK_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<lara_interfaces::srv::ComputeIK_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<lara_interfaces::srv::ComputeIK_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      lara_interfaces::srv::ComputeIK_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<lara_interfaces::srv::ComputeIK_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      lara_interfaces::srv::ComputeIK_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<lara_interfaces::srv::ComputeIK_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<lara_interfaces::srv::ComputeIK_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<lara_interfaces::srv::ComputeIK_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__lara_interfaces__srv__ComputeIK_Request
    std::shared_ptr<lara_interfaces::srv::ComputeIK_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__lara_interfaces__srv__ComputeIK_Request
    std::shared_ptr<lara_interfaces::srv::ComputeIK_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ComputeIK_Request_ & other) const
  {
    if (this->target_pose != other.target_pose) {
      return false;
    }
    if (this->seed_joint_positions != other.seed_joint_positions) {
      return false;
    }
    if (this->timeout_sec != other.timeout_sec) {
      return false;
    }
    if (this->position_tolerance != other.position_tolerance) {
      return false;
    }
    if (this->orientation_tolerance != other.orientation_tolerance) {
      return false;
    }
    if (this->enforce_joint_limits_mode != other.enforce_joint_limits_mode) {
      return false;
    }
    return true;
  }
  bool operator!=(const ComputeIK_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ComputeIK_Request_

// alias to use template instance with default allocator
using ComputeIK_Request =
  lara_interfaces::srv::ComputeIK_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace lara_interfaces


#ifndef _WIN32
# define DEPRECATED__lara_interfaces__srv__ComputeIK_Response __attribute__((deprecated))
#else
# define DEPRECATED__lara_interfaces__srv__ComputeIK_Response __declspec(deprecated)
#endif

namespace lara_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct ComputeIK_Response_
{
  using Type = ComputeIK_Response_<ContainerAllocator>;

  explicit ComputeIK_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->message = "";
      this->position_error = 0.0;
      this->orientation_error = 0.0;
      this->iterations = 0l;
    }
  }

  explicit ComputeIK_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : message(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->message = "";
      this->position_error = 0.0;
      this->orientation_error = 0.0;
      this->iterations = 0l;
    }
  }

  // field types and members
  using _success_type =
    bool;
  _success_type success;
  using _message_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _message_type message;
  using _joint_names_type =
    std::vector<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>>;
  _joint_names_type joint_names;
  using _joint_positions_type =
    std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>>;
  _joint_positions_type joint_positions;
  using _position_error_type =
    double;
  _position_error_type position_error;
  using _orientation_error_type =
    double;
  _orientation_error_type orientation_error;
  using _iterations_type =
    int32_t;
  _iterations_type iterations;

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
  Type & set__joint_names(
    const std::vector<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>> & _arg)
  {
    this->joint_names = _arg;
    return *this;
  }
  Type & set__joint_positions(
    const std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>> & _arg)
  {
    this->joint_positions = _arg;
    return *this;
  }
  Type & set__position_error(
    const double & _arg)
  {
    this->position_error = _arg;
    return *this;
  }
  Type & set__orientation_error(
    const double & _arg)
  {
    this->orientation_error = _arg;
    return *this;
  }
  Type & set__iterations(
    const int32_t & _arg)
  {
    this->iterations = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    lara_interfaces::srv::ComputeIK_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const lara_interfaces::srv::ComputeIK_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<lara_interfaces::srv::ComputeIK_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<lara_interfaces::srv::ComputeIK_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      lara_interfaces::srv::ComputeIK_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<lara_interfaces::srv::ComputeIK_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      lara_interfaces::srv::ComputeIK_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<lara_interfaces::srv::ComputeIK_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<lara_interfaces::srv::ComputeIK_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<lara_interfaces::srv::ComputeIK_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__lara_interfaces__srv__ComputeIK_Response
    std::shared_ptr<lara_interfaces::srv::ComputeIK_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__lara_interfaces__srv__ComputeIK_Response
    std::shared_ptr<lara_interfaces::srv::ComputeIK_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ComputeIK_Response_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    if (this->message != other.message) {
      return false;
    }
    if (this->joint_names != other.joint_names) {
      return false;
    }
    if (this->joint_positions != other.joint_positions) {
      return false;
    }
    if (this->position_error != other.position_error) {
      return false;
    }
    if (this->orientation_error != other.orientation_error) {
      return false;
    }
    if (this->iterations != other.iterations) {
      return false;
    }
    return true;
  }
  bool operator!=(const ComputeIK_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ComputeIK_Response_

// alias to use template instance with default allocator
using ComputeIK_Response =
  lara_interfaces::srv::ComputeIK_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace lara_interfaces

namespace lara_interfaces
{

namespace srv
{

struct ComputeIK
{
  using Request = lara_interfaces::srv::ComputeIK_Request;
  using Response = lara_interfaces::srv::ComputeIK_Response;
};

}  // namespace srv

}  // namespace lara_interfaces

#endif  // LARA_INTERFACES__SRV__DETAIL__COMPUTE_IK__STRUCT_HPP_
