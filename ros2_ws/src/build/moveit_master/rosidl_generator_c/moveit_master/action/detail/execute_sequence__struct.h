// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from moveit_master:action/ExecuteSequence.idl
// generated code does not contain a copyright notice

#ifndef MOVEIT_MASTER__ACTION__DETAIL__EXECUTE_SEQUENCE__STRUCT_H_
#define MOVEIT_MASTER__ACTION__DETAIL__EXECUTE_SEQUENCE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'steps'
#include "moveit_master/msg/detail/motion_step__struct.h"

/// Struct defined in action/ExecuteSequence in the package moveit_master.
typedef struct moveit_master__action__ExecuteSequence_Goal
{
  moveit_master__msg__MotionStep__Sequence steps;
  /// 0 = default (0.2)
  double velocity_scaling;
} moveit_master__action__ExecuteSequence_Goal;

// Struct for a sequence of moveit_master__action__ExecuteSequence_Goal.
typedef struct moveit_master__action__ExecuteSequence_Goal__Sequence
{
  moveit_master__action__ExecuteSequence_Goal * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} moveit_master__action__ExecuteSequence_Goal__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'message'
#include "rosidl_runtime_c/string.h"

/// Struct defined in action/ExecuteSequence in the package moveit_master.
typedef struct moveit_master__action__ExecuteSequence_Result
{
  bool success;
  /// index of the failing step (valid only if success == false)
  uint32_t failed_step;
  rosidl_runtime_c__String message;
} moveit_master__action__ExecuteSequence_Result;

// Struct for a sequence of moveit_master__action__ExecuteSequence_Result.
typedef struct moveit_master__action__ExecuteSequence_Result__Sequence
{
  moveit_master__action__ExecuteSequence_Result * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} moveit_master__action__ExecuteSequence_Result__Sequence;


// Constants defined in the message

/// Struct defined in action/ExecuteSequence in the package moveit_master.
typedef struct moveit_master__action__ExecuteSequence_Feedback
{
  uint32_t current_step;
} moveit_master__action__ExecuteSequence_Feedback;

// Struct for a sequence of moveit_master__action__ExecuteSequence_Feedback.
typedef struct moveit_master__action__ExecuteSequence_Feedback__Sequence
{
  moveit_master__action__ExecuteSequence_Feedback * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} moveit_master__action__ExecuteSequence_Feedback__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'goal'
#include "moveit_master/action/detail/execute_sequence__struct.h"

/// Struct defined in action/ExecuteSequence in the package moveit_master.
typedef struct moveit_master__action__ExecuteSequence_SendGoal_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
  moveit_master__action__ExecuteSequence_Goal goal;
} moveit_master__action__ExecuteSequence_SendGoal_Request;

// Struct for a sequence of moveit_master__action__ExecuteSequence_SendGoal_Request.
typedef struct moveit_master__action__ExecuteSequence_SendGoal_Request__Sequence
{
  moveit_master__action__ExecuteSequence_SendGoal_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} moveit_master__action__ExecuteSequence_SendGoal_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in action/ExecuteSequence in the package moveit_master.
typedef struct moveit_master__action__ExecuteSequence_SendGoal_Response
{
  bool accepted;
  builtin_interfaces__msg__Time stamp;
} moveit_master__action__ExecuteSequence_SendGoal_Response;

// Struct for a sequence of moveit_master__action__ExecuteSequence_SendGoal_Response.
typedef struct moveit_master__action__ExecuteSequence_SendGoal_Response__Sequence
{
  moveit_master__action__ExecuteSequence_SendGoal_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} moveit_master__action__ExecuteSequence_SendGoal_Response__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"

/// Struct defined in action/ExecuteSequence in the package moveit_master.
typedef struct moveit_master__action__ExecuteSequence_GetResult_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
} moveit_master__action__ExecuteSequence_GetResult_Request;

// Struct for a sequence of moveit_master__action__ExecuteSequence_GetResult_Request.
typedef struct moveit_master__action__ExecuteSequence_GetResult_Request__Sequence
{
  moveit_master__action__ExecuteSequence_GetResult_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} moveit_master__action__ExecuteSequence_GetResult_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'result'
// already included above
// #include "moveit_master/action/detail/execute_sequence__struct.h"

/// Struct defined in action/ExecuteSequence in the package moveit_master.
typedef struct moveit_master__action__ExecuteSequence_GetResult_Response
{
  int8_t status;
  moveit_master__action__ExecuteSequence_Result result;
} moveit_master__action__ExecuteSequence_GetResult_Response;

// Struct for a sequence of moveit_master__action__ExecuteSequence_GetResult_Response.
typedef struct moveit_master__action__ExecuteSequence_GetResult_Response__Sequence
{
  moveit_master__action__ExecuteSequence_GetResult_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} moveit_master__action__ExecuteSequence_GetResult_Response__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'feedback'
// already included above
// #include "moveit_master/action/detail/execute_sequence__struct.h"

/// Struct defined in action/ExecuteSequence in the package moveit_master.
typedef struct moveit_master__action__ExecuteSequence_FeedbackMessage
{
  unique_identifier_msgs__msg__UUID goal_id;
  moveit_master__action__ExecuteSequence_Feedback feedback;
} moveit_master__action__ExecuteSequence_FeedbackMessage;

// Struct for a sequence of moveit_master__action__ExecuteSequence_FeedbackMessage.
typedef struct moveit_master__action__ExecuteSequence_FeedbackMessage__Sequence
{
  moveit_master__action__ExecuteSequence_FeedbackMessage * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} moveit_master__action__ExecuteSequence_FeedbackMessage__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // MOVEIT_MASTER__ACTION__DETAIL__EXECUTE_SEQUENCE__STRUCT_H_
