// NOLINT: This file starts with a BOM since it contain non-ASCII characters
// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from lara_interfaces:srv/MoveJoints.idl
// generated code does not contain a copyright notice

#ifndef LARA_INTERFACES__SRV__DETAIL__MOVE_JOINTS__STRUCT_H_
#define LARA_INTERFACES__SRV__DETAIL__MOVE_JOINTS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'point_name'
#include "rosidl_runtime_c/string.h"
// Member 'target_joint'
// Member 'target_pose'
#include "rosidl_runtime_c/primitives_sequence.h"

/// Struct defined in srv/MoveJoints in the package lara_interfaces.
typedef struct lara_interfaces__srv__MoveJoints_Request
{
  /// if set, move to teach pendant point by name (e.g. "GP7")
  rosidl_runtime_c__String point_name;
  /// degrees, 6*k waypoints (ignored if point_name is set)
  rosidl_runtime_c__double__Sequence target_joint;
  /// optional TCP [x,y,z,roll,pitch,yaw] m/rad — IK when target_joint empty
  rosidl_runtime_c__double__Sequence target_pose;
  double speed;
  double acceleration;
  bool enable_safety;
} lara_interfaces__srv__MoveJoints_Request;

// Struct for a sequence of lara_interfaces__srv__MoveJoints_Request.
typedef struct lara_interfaces__srv__MoveJoints_Request__Sequence
{
  lara_interfaces__srv__MoveJoints_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} lara_interfaces__srv__MoveJoints_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'message'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in srv/MoveJoints in the package lara_interfaces.
typedef struct lara_interfaces__srv__MoveJoints_Response
{
  bool success;
  rosidl_runtime_c__String message;
} lara_interfaces__srv__MoveJoints_Response;

// Struct for a sequence of lara_interfaces__srv__MoveJoints_Response.
typedef struct lara_interfaces__srv__MoveJoints_Response__Sequence
{
  lara_interfaces__srv__MoveJoints_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} lara_interfaces__srv__MoveJoints_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // LARA_INTERFACES__SRV__DETAIL__MOVE_JOINTS__STRUCT_H_
