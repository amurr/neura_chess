// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from moveit_master:msg/MotionStep.idl
// generated code does not contain a copyright notice

#ifndef MOVEIT_MASTER__MSG__DETAIL__MOTION_STEP__STRUCT_H_
#define MOVEIT_MASTER__MSG__DETAIL__MOTION_STEP__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Constant 'ARM_POSE'.
/**
  * move arm EEF to `pose` (in the arm's pose reference frame, e.g. world)
 */
enum
{
  moveit_master__msg__MotionStep__ARM_POSE = 0
};

/// Constant 'ARM_NAMED'.
/**
  * move arm to SRDF named state `named_target` (e.g. "home", "e2_hover")
 */
enum
{
  moveit_master__msg__MotionStep__ARM_NAMED = 1
};

/// Constant 'GRIPPER_NAMED'.
/**
  * move gripper to SRDF named state `named_target` (e.g. "open")
 */
enum
{
  moveit_master__msg__MotionStep__GRIPPER_NAMED = 2
};

/// Constant 'WAIT'.
/**
  * pause for `duration` seconds
 */
enum
{
  moveit_master__msg__MotionStep__WAIT = 3
};

/// Constant 'GRIPPER_JOINT'.
/**
  * move gripper joint to `joint_value` (rad)
 */
enum
{
  moveit_master__msg__MotionStep__GRIPPER_JOINT = 4
};

/// Constant 'ARM_CARTESIAN'.
/**
  * straight-line EEF move by `offset` (planning frame, m), e.g. z=-0.06 = straight down
 */
enum
{
  moveit_master__msg__MotionStep__ARM_CARTESIAN = 5
};

/// Constant 'ATTACH'.
/**
  * attach world object `object_id` to the EEF link; gripper links may touch it
 */
enum
{
  moveit_master__msg__MotionStep__ATTACH = 6
};

/// Constant 'DETACH'.
/**
  * detach `object_id`; it stays in the world where it was released
 */
enum
{
  moveit_master__msg__MotionStep__DETACH = 7
};

/// Constant 'ALLOW_COLLISION'.
/**
  * allow=true: `object_id` may touch gripper links + `touch_links`; false: undo
 */
enum
{
  moveit_master__msg__MotionStep__ALLOW_COLLISION = 8
};

// Include directives for member types
// Member 'pose'
#include "geometry_msgs/msg/detail/pose__struct.h"
// Member 'named_target'
// Member 'object_id'
// Member 'touch_links'
#include "rosidl_runtime_c/string.h"
// Member 'offset'
#include "geometry_msgs/msg/detail/vector3__struct.h"

/// Struct defined in msg/MotionStep in the package moveit_master.
/**
  * One step of a motion sequence executed by moveit_master.
 */
typedef struct moveit_master__msg__MotionStep
{
  uint8_t type;
  geometry_msgs__msg__Pose pose;
  rosidl_runtime_c__String named_target;
  double duration;
  double joint_value;
  geometry_msgs__msg__Vector3 offset;
  rosidl_runtime_c__String object_id;
  /// ALLOW_COLLISION: extra links / objects, e.g. the board square under the piece
  rosidl_runtime_c__String__Sequence touch_links;
  bool allow;
} moveit_master__msg__MotionStep;

// Struct for a sequence of moveit_master__msg__MotionStep.
typedef struct moveit_master__msg__MotionStep__Sequence
{
  moveit_master__msg__MotionStep * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} moveit_master__msg__MotionStep__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // MOVEIT_MASTER__MSG__DETAIL__MOTION_STEP__STRUCT_H_
