// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from lara_interfaces:srv/MoveLinear.idl
// generated code does not contain a copyright notice

#ifndef LARA_INTERFACES__SRV__DETAIL__MOVE_LINEAR__STRUCT_H_
#define LARA_INTERFACES__SRV__DETAIL__MOVE_LINEAR__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'target_pose'
#include "rosidl_runtime_c/primitives_sequence.h"
// Member 'offset_frame'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/MoveLinear in the package lara_interfaces.
typedef struct lara_interfaces__srv__MoveLinear_Request
{
  rosidl_runtime_c__double__Sequence target_pose;
  /// m/s
  double speed;
  /// m/s^2
  double acceleration;
  bool enable_safety;
  /// if true, each 6-tuple is a cartesian_offset (move_linear_relative)
  bool use_relative;
  /// "Base" or "Tool" (only when use_relative is true)
  rosidl_runtime_c__String offset_frame;
} lara_interfaces__srv__MoveLinear_Request;

// Struct for a sequence of lara_interfaces__srv__MoveLinear_Request.
typedef struct lara_interfaces__srv__MoveLinear_Request__Sequence
{
  lara_interfaces__srv__MoveLinear_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} lara_interfaces__srv__MoveLinear_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'message'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in srv/MoveLinear in the package lara_interfaces.
typedef struct lara_interfaces__srv__MoveLinear_Response
{
  bool success;
  rosidl_runtime_c__String message;
} lara_interfaces__srv__MoveLinear_Response;

// Struct for a sequence of lara_interfaces__srv__MoveLinear_Response.
typedef struct lara_interfaces__srv__MoveLinear_Response__Sequence
{
  lara_interfaces__srv__MoveLinear_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} lara_interfaces__srv__MoveLinear_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // LARA_INTERFACES__SRV__DETAIL__MOVE_LINEAR__STRUCT_H_
