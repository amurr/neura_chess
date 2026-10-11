// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__rosidl_typesupport_fastrtps_cpp.hpp.em
// with input from moveit_master:msg/MotionStep.idl
// generated code does not contain a copyright notice

#ifndef MOVEIT_MASTER__MSG__DETAIL__MOTION_STEP__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
#define MOVEIT_MASTER__MSG__DETAIL__MOTION_STEP__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_

#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "moveit_master/msg/rosidl_typesupport_fastrtps_cpp__visibility_control.h"
#include "moveit_master/msg/detail/motion_step__struct.hpp"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

#include "fastcdr/Cdr.h"

namespace moveit_master
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_moveit_master
cdr_serialize(
  const moveit_master::msg::MotionStep & ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_moveit_master
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  moveit_master::msg::MotionStep & ros_message);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_moveit_master
get_serialized_size(
  const moveit_master::msg::MotionStep & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_moveit_master
max_serialized_size_MotionStep(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace moveit_master

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_moveit_master
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, moveit_master, msg, MotionStep)();

#ifdef __cplusplus
}
#endif

#endif  // MOVEIT_MASTER__MSG__DETAIL__MOTION_STEP__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
