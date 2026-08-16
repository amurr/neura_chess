// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from lara_interfaces:msg/XyzRpyGoal.idl
// generated code does not contain a copyright notice

#ifndef LARA_INTERFACES__MSG__DETAIL__XYZ_RPY_GOAL__FUNCTIONS_H_
#define LARA_INTERFACES__MSG__DETAIL__XYZ_RPY_GOAL__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "lara_interfaces/msg/rosidl_generator_c__visibility_control.h"

#include "lara_interfaces/msg/detail/xyz_rpy_goal__struct.h"

/// Initialize msg/XyzRpyGoal message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * lara_interfaces__msg__XyzRpyGoal
 * )) before or use
 * lara_interfaces__msg__XyzRpyGoal__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_lara_interfaces
bool
lara_interfaces__msg__XyzRpyGoal__init(lara_interfaces__msg__XyzRpyGoal * msg);

/// Finalize msg/XyzRpyGoal message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_lara_interfaces
void
lara_interfaces__msg__XyzRpyGoal__fini(lara_interfaces__msg__XyzRpyGoal * msg);

/// Create msg/XyzRpyGoal message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * lara_interfaces__msg__XyzRpyGoal__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_lara_interfaces
lara_interfaces__msg__XyzRpyGoal *
lara_interfaces__msg__XyzRpyGoal__create();

/// Destroy msg/XyzRpyGoal message.
/**
 * It calls
 * lara_interfaces__msg__XyzRpyGoal__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_lara_interfaces
void
lara_interfaces__msg__XyzRpyGoal__destroy(lara_interfaces__msg__XyzRpyGoal * msg);

/// Check for msg/XyzRpyGoal message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_lara_interfaces
bool
lara_interfaces__msg__XyzRpyGoal__are_equal(const lara_interfaces__msg__XyzRpyGoal * lhs, const lara_interfaces__msg__XyzRpyGoal * rhs);

/// Copy a msg/XyzRpyGoal message.
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
ROSIDL_GENERATOR_C_PUBLIC_lara_interfaces
bool
lara_interfaces__msg__XyzRpyGoal__copy(
  const lara_interfaces__msg__XyzRpyGoal * input,
  lara_interfaces__msg__XyzRpyGoal * output);

/// Initialize array of msg/XyzRpyGoal messages.
/**
 * It allocates the memory for the number of elements and calls
 * lara_interfaces__msg__XyzRpyGoal__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_lara_interfaces
bool
lara_interfaces__msg__XyzRpyGoal__Sequence__init(lara_interfaces__msg__XyzRpyGoal__Sequence * array, size_t size);

/// Finalize array of msg/XyzRpyGoal messages.
/**
 * It calls
 * lara_interfaces__msg__XyzRpyGoal__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_lara_interfaces
void
lara_interfaces__msg__XyzRpyGoal__Sequence__fini(lara_interfaces__msg__XyzRpyGoal__Sequence * array);

/// Create array of msg/XyzRpyGoal messages.
/**
 * It allocates the memory for the array and calls
 * lara_interfaces__msg__XyzRpyGoal__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_lara_interfaces
lara_interfaces__msg__XyzRpyGoal__Sequence *
lara_interfaces__msg__XyzRpyGoal__Sequence__create(size_t size);

/// Destroy array of msg/XyzRpyGoal messages.
/**
 * It calls
 * lara_interfaces__msg__XyzRpyGoal__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_lara_interfaces
void
lara_interfaces__msg__XyzRpyGoal__Sequence__destroy(lara_interfaces__msg__XyzRpyGoal__Sequence * array);

/// Check for msg/XyzRpyGoal message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_lara_interfaces
bool
lara_interfaces__msg__XyzRpyGoal__Sequence__are_equal(const lara_interfaces__msg__XyzRpyGoal__Sequence * lhs, const lara_interfaces__msg__XyzRpyGoal__Sequence * rhs);

/// Copy an array of msg/XyzRpyGoal messages.
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
ROSIDL_GENERATOR_C_PUBLIC_lara_interfaces
bool
lara_interfaces__msg__XyzRpyGoal__Sequence__copy(
  const lara_interfaces__msg__XyzRpyGoal__Sequence * input,
  lara_interfaces__msg__XyzRpyGoal__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // LARA_INTERFACES__MSG__DETAIL__XYZ_RPY_GOAL__FUNCTIONS_H_
