// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from lara_interfaces:msg/XyzRpyGoal.idl
// generated code does not contain a copyright notice

#ifndef LARA_INTERFACES__MSG__DETAIL__XYZ_RPY_GOAL__STRUCT_H_
#define LARA_INTERFACES__MSG__DETAIL__XYZ_RPY_GOAL__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/XyzRpyGoal in the package lara_interfaces.
/**
  * TCP target (robot base frame, metres, radians).
 */
typedef struct lara_interfaces__msg__XyzRpyGoal
{
  double x;
  double y;
  double z;
  double roll;
  double pitch;
  double yaw;
  /// If false, executor uses view_rpy parameter instead of roll/pitch/yaw.
  bool use_orientation;
} lara_interfaces__msg__XyzRpyGoal;

// Struct for a sequence of lara_interfaces__msg__XyzRpyGoal.
typedef struct lara_interfaces__msg__XyzRpyGoal__Sequence
{
  lara_interfaces__msg__XyzRpyGoal * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} lara_interfaces__msg__XyzRpyGoal__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // LARA_INTERFACES__MSG__DETAIL__XYZ_RPY_GOAL__STRUCT_H_
