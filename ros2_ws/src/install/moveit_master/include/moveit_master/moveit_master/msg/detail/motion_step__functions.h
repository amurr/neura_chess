// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from moveit_master:msg/MotionStep.idl
// generated code does not contain a copyright notice

#ifndef MOVEIT_MASTER__MSG__DETAIL__MOTION_STEP__FUNCTIONS_H_
#define MOVEIT_MASTER__MSG__DETAIL__MOTION_STEP__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "moveit_master/msg/rosidl_generator_c__visibility_control.h"

#include "moveit_master/msg/detail/motion_step__struct.h"

/// Initialize msg/MotionStep message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * moveit_master__msg__MotionStep
 * )) before or use
 * moveit_master__msg__MotionStep__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_moveit_master
bool
moveit_master__msg__MotionStep__init(moveit_master__msg__MotionStep * msg);

/// Finalize msg/MotionStep message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_moveit_master
void
moveit_master__msg__MotionStep__fini(moveit_master__msg__MotionStep * msg);

/// Create msg/MotionStep message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * moveit_master__msg__MotionStep__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_moveit_master
moveit_master__msg__MotionStep *
moveit_master__msg__MotionStep__create();

/// Destroy msg/MotionStep message.
/**
 * It calls
 * moveit_master__msg__MotionStep__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_moveit_master
void
moveit_master__msg__MotionStep__destroy(moveit_master__msg__MotionStep * msg);

/// Check for msg/MotionStep message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_moveit_master
bool
moveit_master__msg__MotionStep__are_equal(const moveit_master__msg__MotionStep * lhs, const moveit_master__msg__MotionStep * rhs);

/// Copy a msg/MotionStep message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_moveit_master
bool
moveit_master__msg__MotionStep__copy(
  const moveit_master__msg__MotionStep * input,
  moveit_master__msg__MotionStep * output);

/// Initialize array of msg/MotionStep messages.
/**
 * It allocates the memory for the number of elements and calls
 * moveit_master__msg__MotionStep__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_moveit_master
bool
moveit_master__msg__MotionStep__Sequence__init(moveit_master__msg__MotionStep__Sequence * array, size_t size);

/// Finalize array of msg/MotionStep messages.
/**
 * It calls
 * moveit_master__msg__MotionStep__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_moveit_master
void
moveit_master__msg__MotionStep__Sequence__fini(moveit_master__msg__MotionStep__Sequence * array);

/// Create array of msg/MotionStep messages.
/**
 * It allocates the memory for the array and calls
 * moveit_master__msg__MotionStep__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_moveit_master
moveit_master__msg__MotionStep__Sequence *
moveit_master__msg__MotionStep__Sequence__create(size_t size);

/// Destroy array of msg/MotionStep messages.
/**
 * It calls
 * moveit_master__msg__MotionStep__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_moveit_master
void
moveit_master__msg__MotionStep__Sequence__destroy(moveit_master__msg__MotionStep__Sequence * array);

/// Check for msg/MotionStep message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_moveit_master
bool
moveit_master__msg__MotionStep__Sequence__are_equal(const moveit_master__msg__MotionStep__Sequence * lhs, const moveit_master__msg__MotionStep__Sequence * rhs);

/// Copy an array of msg/MotionStep messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_moveit_master
bool
moveit_master__msg__MotionStep__Sequence__copy(
  const moveit_master__msg__MotionStep__Sequence * input,
  moveit_master__msg__MotionStep__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // MOVEIT_MASTER__MSG__DETAIL__MOTION_STEP__FUNCTIONS_H_
