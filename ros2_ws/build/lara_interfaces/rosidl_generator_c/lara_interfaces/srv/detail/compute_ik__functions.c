// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from lara_interfaces:srv/ComputeIK.idl
// generated code does not contain a copyright notice
#include "lara_interfaces/srv/detail/compute_ik__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

// Include directives for member types
// Member `target_pose`
#include "geometry_msgs/msg/detail/pose__functions.h"
// Member `seed_joint_positions`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

bool
lara_interfaces__srv__ComputeIK_Request__init(lara_interfaces__srv__ComputeIK_Request * msg)
{
  if (!msg) {
    return false;
  }
  // target_pose
  if (!geometry_msgs__msg__Pose__init(&msg->target_pose)) {
    lara_interfaces__srv__ComputeIK_Request__fini(msg);
    return false;
  }
  // seed_joint_positions
  if (!rosidl_runtime_c__double__Sequence__init(&msg->seed_joint_positions, 0)) {
    lara_interfaces__srv__ComputeIK_Request__fini(msg);
    return false;
  }
  // timeout_sec
  // position_tolerance
  // orientation_tolerance
  // enforce_joint_limits_mode
  return true;
}

void
lara_interfaces__srv__ComputeIK_Request__fini(lara_interfaces__srv__ComputeIK_Request * msg)
{
  if (!msg) {
    return;
  }
  // target_pose
  geometry_msgs__msg__Pose__fini(&msg->target_pose);
  // seed_joint_positions
  rosidl_runtime_c__double__Sequence__fini(&msg->seed_joint_positions);
  // timeout_sec
  // position_tolerance
  // orientation_tolerance
  // enforce_joint_limits_mode
}

bool
lara_interfaces__srv__ComputeIK_Request__are_equal(const lara_interfaces__srv__ComputeIK_Request * lhs, const lara_interfaces__srv__ComputeIK_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // target_pose
  if (!geometry_msgs__msg__Pose__are_equal(
      &(lhs->target_pose), &(rhs->target_pose)))
  {
    return false;
  }
  // seed_joint_positions
  if (!rosidl_runtime_c__double__Sequence__are_equal(
      &(lhs->seed_joint_positions), &(rhs->seed_joint_positions)))
  {
    return false;
  }
  // timeout_sec
  if (lhs->timeout_sec != rhs->timeout_sec) {
    return false;
  }
  // position_tolerance
  if (lhs->position_tolerance != rhs->position_tolerance) {
    return false;
  }
  // orientation_tolerance
  if (lhs->orientation_tolerance != rhs->orientation_tolerance) {
    return false;
  }
  // enforce_joint_limits_mode
  if (lhs->enforce_joint_limits_mode != rhs->enforce_joint_limits_mode) {
    return false;
  }
  return true;
}

bool
lara_interfaces__srv__ComputeIK_Request__copy(
  const lara_interfaces__srv__ComputeIK_Request * input,
  lara_interfaces__srv__ComputeIK_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // target_pose
  if (!geometry_msgs__msg__Pose__copy(
      &(input->target_pose), &(output->target_pose)))
  {
    return false;
  }
  // seed_joint_positions
  if (!rosidl_runtime_c__double__Sequence__copy(
      &(input->seed_joint_positions), &(output->seed_joint_positions)))
  {
    return false;
  }
  // timeout_sec
  output->timeout_sec = input->timeout_sec;
  // position_tolerance
  output->position_tolerance = input->position_tolerance;
  // orientation_tolerance
  output->orientation_tolerance = input->orientation_tolerance;
  // enforce_joint_limits_mode
  output->enforce_joint_limits_mode = input->enforce_joint_limits_mode;
  return true;
}

lara_interfaces__srv__ComputeIK_Request *
lara_interfaces__srv__ComputeIK_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  lara_interfaces__srv__ComputeIK_Request * msg = (lara_interfaces__srv__ComputeIK_Request *)allocator.allocate(sizeof(lara_interfaces__srv__ComputeIK_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(lara_interfaces__srv__ComputeIK_Request));
  bool success = lara_interfaces__srv__ComputeIK_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
lara_interfaces__srv__ComputeIK_Request__destroy(lara_interfaces__srv__ComputeIK_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    lara_interfaces__srv__ComputeIK_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
lara_interfaces__srv__ComputeIK_Request__Sequence__init(lara_interfaces__srv__ComputeIK_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  lara_interfaces__srv__ComputeIK_Request * data = NULL;

  if (size) {
    data = (lara_interfaces__srv__ComputeIK_Request *)allocator.zero_allocate(size, sizeof(lara_interfaces__srv__ComputeIK_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = lara_interfaces__srv__ComputeIK_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        lara_interfaces__srv__ComputeIK_Request__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
lara_interfaces__srv__ComputeIK_Request__Sequence__fini(lara_interfaces__srv__ComputeIK_Request__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      lara_interfaces__srv__ComputeIK_Request__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

lara_interfaces__srv__ComputeIK_Request__Sequence *
lara_interfaces__srv__ComputeIK_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  lara_interfaces__srv__ComputeIK_Request__Sequence * array = (lara_interfaces__srv__ComputeIK_Request__Sequence *)allocator.allocate(sizeof(lara_interfaces__srv__ComputeIK_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = lara_interfaces__srv__ComputeIK_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
lara_interfaces__srv__ComputeIK_Request__Sequence__destroy(lara_interfaces__srv__ComputeIK_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    lara_interfaces__srv__ComputeIK_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
lara_interfaces__srv__ComputeIK_Request__Sequence__are_equal(const lara_interfaces__srv__ComputeIK_Request__Sequence * lhs, const lara_interfaces__srv__ComputeIK_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!lara_interfaces__srv__ComputeIK_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
lara_interfaces__srv__ComputeIK_Request__Sequence__copy(
  const lara_interfaces__srv__ComputeIK_Request__Sequence * input,
  lara_interfaces__srv__ComputeIK_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(lara_interfaces__srv__ComputeIK_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    lara_interfaces__srv__ComputeIK_Request * data =
      (lara_interfaces__srv__ComputeIK_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!lara_interfaces__srv__ComputeIK_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          lara_interfaces__srv__ComputeIK_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!lara_interfaces__srv__ComputeIK_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `message`
// Member `joint_names`
#include "rosidl_runtime_c/string_functions.h"
// Member `joint_positions`
// already included above
// #include "rosidl_runtime_c/primitives_sequence_functions.h"

bool
lara_interfaces__srv__ComputeIK_Response__init(lara_interfaces__srv__ComputeIK_Response * msg)
{
  if (!msg) {
    return false;
  }
  // success
  // message
  if (!rosidl_runtime_c__String__init(&msg->message)) {
    lara_interfaces__srv__ComputeIK_Response__fini(msg);
    return false;
  }
  // joint_names
  if (!rosidl_runtime_c__String__Sequence__init(&msg->joint_names, 0)) {
    lara_interfaces__srv__ComputeIK_Response__fini(msg);
    return false;
  }
  // joint_positions
  if (!rosidl_runtime_c__double__Sequence__init(&msg->joint_positions, 0)) {
    lara_interfaces__srv__ComputeIK_Response__fini(msg);
    return false;
  }
  // position_error
  // orientation_error
  // iterations
  return true;
}

void
lara_interfaces__srv__ComputeIK_Response__fini(lara_interfaces__srv__ComputeIK_Response * msg)
{
  if (!msg) {
    return;
  }
  // success
  // message
  rosidl_runtime_c__String__fini(&msg->message);
  // joint_names
  rosidl_runtime_c__String__Sequence__fini(&msg->joint_names);
  // joint_positions
  rosidl_runtime_c__double__Sequence__fini(&msg->joint_positions);
  // position_error
  // orientation_error
  // iterations
}

bool
lara_interfaces__srv__ComputeIK_Response__are_equal(const lara_interfaces__srv__ComputeIK_Response * lhs, const lara_interfaces__srv__ComputeIK_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // success
  if (lhs->success != rhs->success) {
    return false;
  }
  // message
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->message), &(rhs->message)))
  {
    return false;
  }
  // joint_names
  if (!rosidl_runtime_c__String__Sequence__are_equal(
      &(lhs->joint_names), &(rhs->joint_names)))
  {
    return false;
  }
  // joint_positions
  if (!rosidl_runtime_c__double__Sequence__are_equal(
      &(lhs->joint_positions), &(rhs->joint_positions)))
  {
    return false;
  }
  // position_error
  if (lhs->position_error != rhs->position_error) {
    return false;
  }
  // orientation_error
  if (lhs->orientation_error != rhs->orientation_error) {
    return false;
  }
  // iterations
  if (lhs->iterations != rhs->iterations) {
    return false;
  }
  return true;
}

bool
lara_interfaces__srv__ComputeIK_Response__copy(
  const lara_interfaces__srv__ComputeIK_Response * input,
  lara_interfaces__srv__ComputeIK_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // success
  output->success = input->success;
  // message
  if (!rosidl_runtime_c__String__copy(
      &(input->message), &(output->message)))
  {
    return false;
  }
  // joint_names
  if (!rosidl_runtime_c__String__Sequence__copy(
      &(input->joint_names), &(output->joint_names)))
  {
    return false;
  }
  // joint_positions
  if (!rosidl_runtime_c__double__Sequence__copy(
      &(input->joint_positions), &(output->joint_positions)))
  {
    return false;
  }
  // position_error
  output->position_error = input->position_error;
  // orientation_error
  output->orientation_error = input->orientation_error;
  // iterations
  output->iterations = input->iterations;
  return true;
}

lara_interfaces__srv__ComputeIK_Response *
lara_interfaces__srv__ComputeIK_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  lara_interfaces__srv__ComputeIK_Response * msg = (lara_interfaces__srv__ComputeIK_Response *)allocator.allocate(sizeof(lara_interfaces__srv__ComputeIK_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(lara_interfaces__srv__ComputeIK_Response));
  bool success = lara_interfaces__srv__ComputeIK_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
lara_interfaces__srv__ComputeIK_Response__destroy(lara_interfaces__srv__ComputeIK_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    lara_interfaces__srv__ComputeIK_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
lara_interfaces__srv__ComputeIK_Response__Sequence__init(lara_interfaces__srv__ComputeIK_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  lara_interfaces__srv__ComputeIK_Response * data = NULL;

  if (size) {
    data = (lara_interfaces__srv__ComputeIK_Response *)allocator.zero_allocate(size, sizeof(lara_interfaces__srv__ComputeIK_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = lara_interfaces__srv__ComputeIK_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        lara_interfaces__srv__ComputeIK_Response__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
lara_interfaces__srv__ComputeIK_Response__Sequence__fini(lara_interfaces__srv__ComputeIK_Response__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      lara_interfaces__srv__ComputeIK_Response__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

lara_interfaces__srv__ComputeIK_Response__Sequence *
lara_interfaces__srv__ComputeIK_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  lara_interfaces__srv__ComputeIK_Response__Sequence * array = (lara_interfaces__srv__ComputeIK_Response__Sequence *)allocator.allocate(sizeof(lara_interfaces__srv__ComputeIK_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = lara_interfaces__srv__ComputeIK_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
lara_interfaces__srv__ComputeIK_Response__Sequence__destroy(lara_interfaces__srv__ComputeIK_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    lara_interfaces__srv__ComputeIK_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
lara_interfaces__srv__ComputeIK_Response__Sequence__are_equal(const lara_interfaces__srv__ComputeIK_Response__Sequence * lhs, const lara_interfaces__srv__ComputeIK_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!lara_interfaces__srv__ComputeIK_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
lara_interfaces__srv__ComputeIK_Response__Sequence__copy(
  const lara_interfaces__srv__ComputeIK_Response__Sequence * input,
  lara_interfaces__srv__ComputeIK_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(lara_interfaces__srv__ComputeIK_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    lara_interfaces__srv__ComputeIK_Response * data =
      (lara_interfaces__srv__ComputeIK_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!lara_interfaces__srv__ComputeIK_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          lara_interfaces__srv__ComputeIK_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!lara_interfaces__srv__ComputeIK_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
