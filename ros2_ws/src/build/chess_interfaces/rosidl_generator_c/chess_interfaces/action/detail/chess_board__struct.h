// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from chess_interfaces:action/ChessBoard.idl
// generated code does not contain a copyright notice

#ifndef CHESS_INTERFACES__ACTION__DETAIL__CHESS_BOARD__STRUCT_H_
#define CHESS_INTERFACES__ACTION__DETAIL__CHESS_BOARD__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Constant 'ACTIVE'.
/**
  * change_status values
  * the move already happened on the real board -> only update the PlanningScene
 */
static const char * const chess_interfaces__action__ChessBoard_Goal__ACTIVE = "active";

/// Constant 'PASSIVE'.
/**
  * the robot must execute the move -> pick and place with MoveItMaster
 */
static const char * const chess_interfaces__action__ChessBoard_Goal__PASSIVE = "passive";

// Include directives for member types
// Member 'change_status'
// Member 'piece_type'
// Member 'to_pick'
// Member 'to_place'
// Member 'fen'
#include "rosidl_runtime_c/string.h"

/// Struct defined in action/ChessBoard in the package chess_interfaces.
typedef struct chess_interfaces__action__ChessBoard_Goal
{
  /// Goal
  /// ACTIVE / PASSIVE
  rosidl_runtime_c__String change_status;
  /// pawn / rook / knight / bishop / queen / king (the piece on to_pick)
  rosidl_runtime_c__String piece_type;
  /// square, e.g. "e2"
  rosidl_runtime_c__String to_pick;
  /// square, e.g. "e4"
  rosidl_runtime_c__String to_place;
  /// board AFTER the move (FEN, piece-placement field is enough).
  /// Optional, but required for castling, en passant and promotion;
  /// an ACTIVE goal with only `fen` re-syncs the whole board.
  rosidl_runtime_c__String fen;
} chess_interfaces__action__ChessBoard_Goal;

// Struct for a sequence of chess_interfaces__action__ChessBoard_Goal.
typedef struct chess_interfaces__action__ChessBoard_Goal__Sequence
{
  chess_interfaces__action__ChessBoard_Goal * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} chess_interfaces__action__ChessBoard_Goal__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'message'
// Member 'fen'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in action/ChessBoard in the package chess_interfaces.
typedef struct chess_interfaces__action__ChessBoard_Result
{
  bool success;
  rosidl_runtime_c__String message;
  /// board as the server (and the PlanningScene) now holds it
  rosidl_runtime_c__String fen;
} chess_interfaces__action__ChessBoard_Result;

// Struct for a sequence of chess_interfaces__action__ChessBoard_Result.
typedef struct chess_interfaces__action__ChessBoard_Result__Sequence
{
  chess_interfaces__action__ChessBoard_Result * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} chess_interfaces__action__ChessBoard_Result__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'stage'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in action/ChessBoard in the package chess_interfaces.
typedef struct chess_interfaces__action__ChessBoard_Feedback
{
  /// e.g. "capture d5 -> discard", "move e2 -> e4", "planning scene sync"
  rosidl_runtime_c__String stage;
} chess_interfaces__action__ChessBoard_Feedback;

// Struct for a sequence of chess_interfaces__action__ChessBoard_Feedback.
typedef struct chess_interfaces__action__ChessBoard_Feedback__Sequence
{
  chess_interfaces__action__ChessBoard_Feedback * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} chess_interfaces__action__ChessBoard_Feedback__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'goal'
#include "chess_interfaces/action/detail/chess_board__struct.h"

/// Struct defined in action/ChessBoard in the package chess_interfaces.
typedef struct chess_interfaces__action__ChessBoard_SendGoal_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
  chess_interfaces__action__ChessBoard_Goal goal;
} chess_interfaces__action__ChessBoard_SendGoal_Request;

// Struct for a sequence of chess_interfaces__action__ChessBoard_SendGoal_Request.
typedef struct chess_interfaces__action__ChessBoard_SendGoal_Request__Sequence
{
  chess_interfaces__action__ChessBoard_SendGoal_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} chess_interfaces__action__ChessBoard_SendGoal_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in action/ChessBoard in the package chess_interfaces.
typedef struct chess_interfaces__action__ChessBoard_SendGoal_Response
{
  bool accepted;
  builtin_interfaces__msg__Time stamp;
} chess_interfaces__action__ChessBoard_SendGoal_Response;

// Struct for a sequence of chess_interfaces__action__ChessBoard_SendGoal_Response.
typedef struct chess_interfaces__action__ChessBoard_SendGoal_Response__Sequence
{
  chess_interfaces__action__ChessBoard_SendGoal_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} chess_interfaces__action__ChessBoard_SendGoal_Response__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"

/// Struct defined in action/ChessBoard in the package chess_interfaces.
typedef struct chess_interfaces__action__ChessBoard_GetResult_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
} chess_interfaces__action__ChessBoard_GetResult_Request;

// Struct for a sequence of chess_interfaces__action__ChessBoard_GetResult_Request.
typedef struct chess_interfaces__action__ChessBoard_GetResult_Request__Sequence
{
  chess_interfaces__action__ChessBoard_GetResult_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} chess_interfaces__action__ChessBoard_GetResult_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'result'
// already included above
// #include "chess_interfaces/action/detail/chess_board__struct.h"

/// Struct defined in action/ChessBoard in the package chess_interfaces.
typedef struct chess_interfaces__action__ChessBoard_GetResult_Response
{
  int8_t status;
  chess_interfaces__action__ChessBoard_Result result;
} chess_interfaces__action__ChessBoard_GetResult_Response;

// Struct for a sequence of chess_interfaces__action__ChessBoard_GetResult_Response.
typedef struct chess_interfaces__action__ChessBoard_GetResult_Response__Sequence
{
  chess_interfaces__action__ChessBoard_GetResult_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} chess_interfaces__action__ChessBoard_GetResult_Response__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'feedback'
// already included above
// #include "chess_interfaces/action/detail/chess_board__struct.h"

/// Struct defined in action/ChessBoard in the package chess_interfaces.
typedef struct chess_interfaces__action__ChessBoard_FeedbackMessage
{
  unique_identifier_msgs__msg__UUID goal_id;
  chess_interfaces__action__ChessBoard_Feedback feedback;
} chess_interfaces__action__ChessBoard_FeedbackMessage;

// Struct for a sequence of chess_interfaces__action__ChessBoard_FeedbackMessage.
typedef struct chess_interfaces__action__ChessBoard_FeedbackMessage__Sequence
{
  chess_interfaces__action__ChessBoard_FeedbackMessage * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} chess_interfaces__action__ChessBoard_FeedbackMessage__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // CHESS_INTERFACES__ACTION__DETAIL__CHESS_BOARD__STRUCT_H_
