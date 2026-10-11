// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from lara_interfaces:srv/GetAppMode.idl
// generated code does not contain a copyright notice

#ifndef LARA_INTERFACES__SRV__DETAIL__GET_APP_MODE__STRUCT_HPP_
#define LARA_INTERFACES__SRV__DETAIL__GET_APP_MODE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__lara_interfaces__srv__GetAppMode_Request __attribute__((deprecated))
#else
# define DEPRECATED__lara_interfaces__srv__GetAppMode_Request __declspec(deprecated)
#endif

namespace lara_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct GetAppMode_Request_
{
  using Type = GetAppMode_Request_<ContainerAllocator>;

  explicit GetAppMode_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->structure_needs_at_least_one_member = 0;
    }
  }

  explicit GetAppMode_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->structure_needs_at_least_one_member = 0;
    }
  }

  // field types and members
  using _structure_needs_at_least_one_member_type =
    uint8_t;
  _structure_needs_at_least_one_member_type structure_needs_at_least_one_member;


  // constant declarations

  // pointer types
  using RawPtr =
    lara_interfaces::srv::GetAppMode_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const lara_interfaces::srv::GetAppMode_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<lara_interfaces::srv::GetAppMode_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<lara_interfaces::srv::GetAppMode_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      lara_interfaces::srv::GetAppMode_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<lara_interfaces::srv::GetAppMode_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      lara_interfaces::srv::GetAppMode_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<lara_interfaces::srv::GetAppMode_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<lara_interfaces::srv::GetAppMode_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<lara_interfaces::srv::GetAppMode_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__lara_interfaces__srv__GetAppMode_Request
    std::shared_ptr<lara_interfaces::srv::GetAppMode_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__lara_interfaces__srv__GetAppMode_Request
    std::shared_ptr<lara_interfaces::srv::GetAppMode_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GetAppMode_Request_ & other) const
  {
    if (this->structure_needs_at_least_one_member != other.structure_needs_at_least_one_member) {
      return false;
    }
    return true;
  }
  bool operator!=(const GetAppMode_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GetAppMode_Request_

// alias to use template instance with default allocator
using GetAppMode_Request =
  lara_interfaces::srv::GetAppMode_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace lara_interfaces


#ifndef _WIN32
# define DEPRECATED__lara_interfaces__srv__GetAppMode_Response __attribute__((deprecated))
#else
# define DEPRECATED__lara_interfaces__srv__GetAppMode_Response __declspec(deprecated)
#endif

namespace lara_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct GetAppMode_Response_
{
  using Type = GetAppMode_Response_<ContainerAllocator>;

  explicit GetAppMode_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->mode = "";
    }
  }

  explicit GetAppMode_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : mode(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->mode = "";
    }
  }

  // field types and members
  using _mode_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _mode_type mode;

  // setters for named parameter idiom
  Type & set__mode(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->mode = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    lara_interfaces::srv::GetAppMode_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const lara_interfaces::srv::GetAppMode_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<lara_interfaces::srv::GetAppMode_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<lara_interfaces::srv::GetAppMode_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      lara_interfaces::srv::GetAppMode_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<lara_interfaces::srv::GetAppMode_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      lara_interfaces::srv::GetAppMode_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<lara_interfaces::srv::GetAppMode_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<lara_interfaces::srv::GetAppMode_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<lara_interfaces::srv::GetAppMode_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__lara_interfaces__srv__GetAppMode_Response
    std::shared_ptr<lara_interfaces::srv::GetAppMode_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__lara_interfaces__srv__GetAppMode_Response
    std::shared_ptr<lara_interfaces::srv::GetAppMode_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GetAppMode_Response_ & other) const
  {
    if (this->mode != other.mode) {
      return false;
    }
    return true;
  }
  bool operator!=(const GetAppMode_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GetAppMode_Response_

// alias to use template instance with default allocator
using GetAppMode_Response =
  lara_interfaces::srv::GetAppMode_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace lara_interfaces

namespace lara_interfaces
{

namespace srv
{

struct GetAppMode
{
  using Request = lara_interfaces::srv::GetAppMode_Request;
  using Response = lara_interfaces::srv::GetAppMode_Response;
};

}  // namespace srv

}  // namespace lara_interfaces

#endif  // LARA_INTERFACES__SRV__DETAIL__GET_APP_MODE__STRUCT_HPP_
