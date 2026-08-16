// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from lara_interfaces:srv/ComputeIK.idl
// generated code does not contain a copyright notice

#ifndef LARA_INTERFACES__SRV__DETAIL__COMPUTE_IK__STRUCT_H_
#define LARA_INTERFACES__SRV__DETAIL__COMPUTE_IK__STRUCT_H_

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
#include "geometry_msgs/msg/detail/pose__struct.h"
// Member 'seed_joint_positions'
#include "rosidl_runtime_c/primitives_sequence.h"

/// Struct defined in srv/ComputeIK in the package lara_interfaces.
typedef struct lara_interfaces__srv__ComputeIK_Request
{
  geometry_msgs__msg__Pose target_pose;
  rosidl_runtime_c__double__Sequence seed_joint_positions;
  double timeout_sec;
  double position_tolerance;
  double orientation_tolerance;
  int8_t enforce_joint_limits_mode;
} lara_interfaces__srv__ComputeIK_Request;

// Struct for a sequence of lara_interfaces__srv__ComputeIK_Request.
typedef struct lara_interfaces__srv__ComputeIK_Request__Sequence
{
  lara_interfaces__srv__ComputeIK_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} lara_interfaces__srv__ComputeIK_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'message'
// Member 'joint_names'
#include "rosidl_runtime_c/string.h"
// Member 'joint_positions'
// already included above
// #include "rosidl_runtime_c/primitives_sequence.h"

/// Struct defined in srv/ComputeIK in the package lara_interfaces.
typedef struct lara_interfaces__srv__ComputeIK_Response
{
  bool success;
  rosidl_runtime_c__String message;
  rosidl_runtime_c__String__Sequence joint_names;
  rosidl_runtime_c__double__Sequence joint_positions;
  double position_error;
  double orientation_error;
  int32_t iterations;
} lara_interfaces__srv__ComputeIK_Response;

// Struct for a sequence of lara_interfaces__srv__ComputeIK_Response.
typedef struct lara_interfaces__srv__ComputeIK_Response__Sequence
{
  lara_interfaces__srv__ComputeIK_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} lara_interfaces__srv__ComputeIK_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // LARA_INTERFACES__SRV__DETAIL__COMPUTE_IK__STRUCT_H_
