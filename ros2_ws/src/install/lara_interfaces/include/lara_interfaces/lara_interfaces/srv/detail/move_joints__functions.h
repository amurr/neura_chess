// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from lara_interfaces:srv/MoveJoints.idl
// generated code does not contain a copyright notice

#ifndef LARA_INTERFACES__SRV__DETAIL__MOVE_JOINTS__FUNCTIONS_H_
#define LARA_INTERFACES__SRV__DETAIL__MOVE_JOINTS__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "lara_interfaces/msg/rosidl_generator_c__visibility_control.h"

#include "lara_interfaces/srv/detail/move_joints__struct.h"

/// Initialize srv/MoveJoints message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * lara_interfaces__srv__MoveJoints_Request
 * )) before or use
 * lara_interfaces__srv__MoveJoints_Request__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_lara_interfaces
bool
lara_interfaces__srv__MoveJoints_Request__init(lara_interfaces__srv__MoveJoints_Request * msg);

/// Finalize srv/MoveJoints message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_lara_interfaces
void
lara_interfaces__srv__MoveJoints_Request__fini(lara_interfaces__srv__MoveJoints_Request * msg);

/// Create srv/MoveJoints message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * lara_interfaces__srv__MoveJoints_Request__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_lara_interfaces
lara_interfaces__srv__MoveJoints_Request *
lara_interfaces__srv__MoveJoints_Request__create();

/// Destroy srv/MoveJoints message.
/**
 * It calls
 * lara_interfaces__srv__MoveJoints_Request__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_lara_interfaces
void
lara_interfaces__srv__MoveJoints_Request__destroy(lara_interfaces__srv__MoveJoints_Request * msg);

/// Check for srv/MoveJoints message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_lara_interfaces
bool
lara_interfaces__srv__MoveJoints_Request__are_equal(const lara_interfaces__srv__MoveJoints_Request * lhs, const lara_interfaces__srv__MoveJoints_Request * rhs);

/// Copy a srv/MoveJoints message.
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
lara_interfaces__srv__MoveJoints_Request__copy(
  const lara_interfaces__srv__MoveJoints_Request * input,
  lara_interfaces__srv__MoveJoints_Request * output);

/// Initialize array of srv/MoveJoints messages.
/**
 * It allocates the memory for the number of elements and calls
 * lara_interfaces__srv__MoveJoints_Request__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_lara_interfaces
bool
lara_interfaces__srv__MoveJoints_Request__Sequence__init(lara_interfaces__srv__MoveJoints_Request__Sequence * array, size_t size);

/// Finalize array of srv/MoveJoints messages.
/**
 * It calls
 * lara_interfaces__srv__MoveJoints_Request__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_lara_interfaces
void
lara_interfaces__srv__MoveJoints_Request__Sequence__fini(lara_interfaces__srv__MoveJoints_Request__Sequence * array);

/// Create array of srv/MoveJoints messages.
/**
 * It allocates the memory for the array and calls
 * lara_interfaces__srv__MoveJoints_Request__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_lara_interfaces
lara_interfaces__srv__MoveJoints_Request__Sequence *
lara_interfaces__srv__MoveJoints_Request__Sequence__create(size_t size);

/// Destroy array of srv/MoveJoints messages.
/**
 * It calls
 * lara_interfaces__srv__MoveJoints_Request__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_lara_interfaces
void
lara_interfaces__srv__MoveJoints_Request__Sequence__destroy(lara_interfaces__srv__MoveJoints_Request__Sequence * array);

/// Check for srv/MoveJoints message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_lara_interfaces
bool
lara_interfaces__srv__MoveJoints_Request__Sequence__are_equal(const lara_interfaces__srv__MoveJoints_Request__Sequence * lhs, const lara_interfaces__srv__MoveJoints_Request__Sequence * rhs);

/// Copy an array of srv/MoveJoints messages.
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
lara_interfaces__srv__MoveJoints_Request__Sequence__copy(
  const lara_interfaces__srv__MoveJoints_Request__Sequence * input,
  lara_interfaces__srv__MoveJoints_Request__Sequence * output);

/// Initialize srv/MoveJoints message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * lara_interfaces__srv__MoveJoints_Response
 * )) before or use
 * lara_interfaces__srv__MoveJoints_Response__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_lara_interfaces
bool
lara_interfaces__srv__MoveJoints_Response__init(lara_interfaces__srv__MoveJoints_Response * msg);

/// Finalize srv/MoveJoints message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_lara_interfaces
void
lara_interfaces__srv__MoveJoints_Response__fini(lara_interfaces__srv__MoveJoints_Response * msg);

/// Create srv/MoveJoints message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * lara_interfaces__srv__MoveJoints_Response__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_lara_interfaces
lara_interfaces__srv__MoveJoints_Response *
lara_interfaces__srv__MoveJoints_Response__create();

/// Destroy srv/MoveJoints message.
/**
 * It calls
 * lara_interfaces__srv__MoveJoints_Response__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_lara_interfaces
void
lara_interfaces__srv__MoveJoints_Response__destroy(lara_interfaces__srv__MoveJoints_Response * msg);

/// Check for srv/MoveJoints message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_lara_interfaces
bool
lara_interfaces__srv__MoveJoints_Response__are_equal(const lara_interfaces__srv__MoveJoints_Response * lhs, const lara_interfaces__srv__MoveJoints_Response * rhs);

/// Copy a srv/MoveJoints message.
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
lara_interfaces__srv__MoveJoints_Response__copy(
  const lara_interfaces__srv__MoveJoints_Response * input,
  lara_interfaces__srv__MoveJoints_Response * output);

/// Initialize array of srv/MoveJoints messages.
/**
 * It allocates the memory for the number of elements and calls
 * lara_interfaces__srv__MoveJoints_Response__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_lara_interfaces
bool
lara_interfaces__srv__MoveJoints_Response__Sequence__init(lara_interfaces__srv__MoveJoints_Response__Sequence * array, size_t size);

/// Finalize array of srv/MoveJoints messages.
/**
 * It calls
 * lara_interfaces__srv__MoveJoints_Response__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_lara_interfaces
void
lara_interfaces__srv__MoveJoints_Response__Sequence__fini(lara_interfaces__srv__MoveJoints_Response__Sequence * array);

/// Create array of srv/MoveJoints messages.
/**
 * It allocates the memory for the array and calls
 * lara_interfaces__srv__MoveJoints_Response__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_lara_interfaces
lara_interfaces__srv__MoveJoints_Response__Sequence *
lara_interfaces__srv__MoveJoints_Response__Sequence__create(size_t size);

/// Destroy array of srv/MoveJoints messages.
/**
 * It calls
 * lara_interfaces__srv__MoveJoints_Response__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_lara_interfaces
void
lara_interfaces__srv__MoveJoints_Response__Sequence__destroy(lara_interfaces__srv__MoveJoints_Response__Sequence * array);

/// Check for srv/MoveJoints message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_lara_interfaces
bool
lara_interfaces__srv__MoveJoints_Response__Sequence__are_equal(const lara_interfaces__srv__MoveJoints_Response__Sequence * lhs, const lara_interfaces__srv__MoveJoints_Response__Sequence * rhs);

/// Copy an array of srv/MoveJoints messages.
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
lara_interfaces__srv__MoveJoints_Response__Sequence__copy(
  const lara_interfaces__srv__MoveJoints_Response__Sequence * input,
  lara_interfaces__srv__MoveJoints_Response__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // LARA_INTERFACES__SRV__DETAIL__MOVE_JOINTS__FUNCTIONS_H_
