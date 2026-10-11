// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from lara_interfaces:srv/GetTCPPose.idl
// generated code does not contain a copyright notice

#ifndef LARA_INTERFACES__SRV__DETAIL__GET_TCP_POSE__STRUCT_H_
#define LARA_INTERFACES__SRV__DETAIL__GET_TCP_POSE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/GetTCPPose in the package lara_interfaces.
typedef struct lara_interfaces__srv__GetTCPPose_Request
{
  uint8_t structure_needs_at_least_one_member;
} lara_interfaces__srv__GetTCPPose_Request;

// Struct for a sequence of lara_interfaces__srv__GetTCPPose_Request.
typedef struct lara_interfaces__srv__GetTCPPose_Request__Sequence
{
  lara_interfaces__srv__GetTCPPose_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} lara_interfaces__srv__GetTCPPose_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'pose'
#include "geometry_msgs/msg/detail/pose__struct.h"

/// Struct defined in srv/GetTCPPose in the package lara_interfaces.
typedef struct lara_interfaces__srv__GetTCPPose_Response
{
  geometry_msgs__msg__Pose pose;
} lara_interfaces__srv__GetTCPPose_Response;

// Struct for a sequence of lara_interfaces__srv__GetTCPPose_Response.
typedef struct lara_interfaces__srv__GetTCPPose_Response__Sequence
{
  lara_interfaces__srv__GetTCPPose_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} lara_interfaces__srv__GetTCPPose_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // LARA_INTERFACES__SRV__DETAIL__GET_TCP_POSE__STRUCT_H_
