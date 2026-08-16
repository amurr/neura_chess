// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from lara_interfaces:srv/MoveLinear.idl
// generated code does not contain a copyright notice
#include "lara_interfaces/srv/detail/move_linear__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

// Include directives for member types
// Member `target_pose`
#include "rosidl_runtime_c/primitives_sequence_functions.h"
// Member `offset_frame`
#include "rosidl_runtime_c/string_functions.h"

bool
lara_interfaces__srv__MoveLinear_Request__init(lara_interfaces__srv__MoveLinear_Request * msg)
{
  if (!msg) {
    return false;
  }
  // target_pose
  if (!rosidl_runtime_c__double__Sequence__init(&msg->target_pose, 0)) {
    lara_interfaces__srv__MoveLinear_Request__fini(msg);
    return false;
  }
  // speed
  // acceleration
  // enable_safety
  // use_relative
  // offset_frame
  if (!rosidl_runtime_c__String__init(&msg->offset_frame)) {
    lara_interfaces__srv__MoveLinear_Request__fini(msg);
    return false;
  }
  return true;
}

void
lara_interfaces__srv__MoveLinear_Request__fini(lara_interfaces__srv__MoveLinear_Request * msg)
{
  if (!msg) {
    return;
  }
  // target_pose
  rosidl_runtime_c__double__Sequence__fini(&msg->target_pose);
  // speed
  // acceleration
  // enable_safety
  // use_relative
  // offset_frame
  rosidl_runtime_c__String__fini(&msg->offset_frame);
}

bool
lara_interfaces__srv__MoveLinear_Request__are_equal(const lara_interfaces__srv__MoveLinear_Request * lhs, const lara_interfaces__srv__MoveLinear_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // target_pose
  if (!rosidl_runtime_c__double__Sequence__are_equal(
      &(lhs->target_pose), &(rhs->target_pose)))
  {
    return false;
  }
  // speed
  if (lhs->speed != rhs->speed) {
    return false;
  }
  // acceleration
  if (lhs->acceleration != rhs->acceleration) {
    return false;
  }
  // enable_safety
  if (lhs->enable_safety != rhs->enable_safety) {
    return false;
  }
  // use_relative
  if (lhs->use_relative != rhs->use_relative) {
    return false;
  }
  // offset_frame
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->offset_frame), &(rhs->offset_frame)))
  {
    return false;
  }
  return true;
}

bool
lara_interfaces__srv__MoveLinear_Request__copy(
  const lara_interfaces__srv__MoveLinear_Request * input,
  lara_interfaces__srv__MoveLinear_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // target_pose
  if (!rosidl_runtime_c__double__Sequence__copy(
      &(input->target_pose), &(output->target_pose)))
  {
    return false;
  }
  // speed
  output->speed = input->speed;
  // acceleration
  output->acceleration = input->acceleration;
  // enable_safety
  output->enable_safety = input->enable_safety;
  // use_relative
  output->use_relative = input->use_relative;
  // offset_frame
  if (!rosidl_runtime_c__String__copy(
      &(input->offset_frame), &(output->offset_frame)))
  {
    return false;
  }
  return true;
}

lara_interfaces__srv__MoveLinear_Request *
lara_interfaces__srv__MoveLinear_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  lara_interfaces__srv__MoveLinear_Request * msg = (lara_interfaces__srv__MoveLinear_Request *)allocator.allocate(sizeof(lara_interfaces__srv__MoveLinear_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(lara_interfaces__srv__MoveLinear_Request));
  bool success = lara_interfaces__srv__MoveLinear_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
lara_interfaces__srv__MoveLinear_Request__destroy(lara_interfaces__srv__MoveLinear_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    lara_interfaces__srv__MoveLinear_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
lara_interfaces__srv__MoveLinear_Request__Sequence__init(lara_interfaces__srv__MoveLinear_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  lara_interfaces__srv__MoveLinear_Request * data = NULL;

  if (size) {
    data = (lara_interfaces__srv__MoveLinear_Request *)allocator.zero_allocate(size, sizeof(lara_interfaces__srv__MoveLinear_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = lara_interfaces__srv__MoveLinear_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        lara_interfaces__srv__MoveLinear_Request__fini(&data[i - 1]);
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
lara_interfaces__srv__MoveLinear_Request__Sequence__fini(lara_interfaces__srv__MoveLinear_Request__Sequence * array)
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
      lara_interfaces__srv__MoveLinear_Request__fini(&array->data[i]);
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

lara_interfaces__srv__MoveLinear_Request__Sequence *
lara_interfaces__srv__MoveLinear_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  lara_interfaces__srv__MoveLinear_Request__Sequence * array = (lara_interfaces__srv__MoveLinear_Request__Sequence *)allocator.allocate(sizeof(lara_interfaces__srv__MoveLinear_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = lara_interfaces__srv__MoveLinear_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
lara_interfaces__srv__MoveLinear_Request__Sequence__destroy(lara_interfaces__srv__MoveLinear_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    lara_interfaces__srv__MoveLinear_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
lara_interfaces__srv__MoveLinear_Request__Sequence__are_equal(const lara_interfaces__srv__MoveLinear_Request__Sequence * lhs, const lara_interfaces__srv__MoveLinear_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!lara_interfaces__srv__MoveLinear_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
lara_interfaces__srv__MoveLinear_Request__Sequence__copy(
  const lara_interfaces__srv__MoveLinear_Request__Sequence * input,
  lara_interfaces__srv__MoveLinear_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(lara_interfaces__srv__MoveLinear_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    lara_interfaces__srv__MoveLinear_Request * data =
      (lara_interfaces__srv__MoveLinear_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!lara_interfaces__srv__MoveLinear_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          lara_interfaces__srv__MoveLinear_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!lara_interfaces__srv__MoveLinear_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `message`
// already included above
// #include "rosidl_runtime_c/string_functions.h"

bool
lara_interfaces__srv__MoveLinear_Response__init(lara_interfaces__srv__MoveLinear_Response * msg)
{
  if (!msg) {
    return false;
  }
  // success
  // message
  if (!rosidl_runtime_c__String__init(&msg->message)) {
    lara_interfaces__srv__MoveLinear_Response__fini(msg);
    return false;
  }
  return true;
}

void
lara_interfaces__srv__MoveLinear_Response__fini(lara_interfaces__srv__MoveLinear_Response * msg)
{
  if (!msg) {
    return;
  }
  // success
  // message
  rosidl_runtime_c__String__fini(&msg->message);
}

bool
lara_interfaces__srv__MoveLinear_Response__are_equal(const lara_interfaces__srv__MoveLinear_Response * lhs, const lara_interfaces__srv__MoveLinear_Response * rhs)
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
  return true;
}

bool
lara_interfaces__srv__MoveLinear_Response__copy(
  const lara_interfaces__srv__MoveLinear_Response * input,
  lara_interfaces__srv__MoveLinear_Response * output)
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
  return true;
}

lara_interfaces__srv__MoveLinear_Response *
lara_interfaces__srv__MoveLinear_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  lara_interfaces__srv__MoveLinear_Response * msg = (lara_interfaces__srv__MoveLinear_Response *)allocator.allocate(sizeof(lara_interfaces__srv__MoveLinear_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(lara_interfaces__srv__MoveLinear_Response));
  bool success = lara_interfaces__srv__MoveLinear_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
lara_interfaces__srv__MoveLinear_Response__destroy(lara_interfaces__srv__MoveLinear_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    lara_interfaces__srv__MoveLinear_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
lara_interfaces__srv__MoveLinear_Response__Sequence__init(lara_interfaces__srv__MoveLinear_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  lara_interfaces__srv__MoveLinear_Response * data = NULL;

  if (size) {
    data = (lara_interfaces__srv__MoveLinear_Response *)allocator.zero_allocate(size, sizeof(lara_interfaces__srv__MoveLinear_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = lara_interfaces__srv__MoveLinear_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        lara_interfaces__srv__MoveLinear_Response__fini(&data[i - 1]);
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
lara_interfaces__srv__MoveLinear_Response__Sequence__fini(lara_interfaces__srv__MoveLinear_Response__Sequence * array)
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
      lara_interfaces__srv__MoveLinear_Response__fini(&array->data[i]);
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

lara_interfaces__srv__MoveLinear_Response__Sequence *
lara_interfaces__srv__MoveLinear_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  lara_interfaces__srv__MoveLinear_Response__Sequence * array = (lara_interfaces__srv__MoveLinear_Response__Sequence *)allocator.allocate(sizeof(lara_interfaces__srv__MoveLinear_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = lara_interfaces__srv__MoveLinear_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
lara_interfaces__srv__MoveLinear_Response__Sequence__destroy(lara_interfaces__srv__MoveLinear_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    lara_interfaces__srv__MoveLinear_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
lara_interfaces__srv__MoveLinear_Response__Sequence__are_equal(const lara_interfaces__srv__MoveLinear_Response__Sequence * lhs, const lara_interfaces__srv__MoveLinear_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!lara_interfaces__srv__MoveLinear_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
lara_interfaces__srv__MoveLinear_Response__Sequence__copy(
  const lara_interfaces__srv__MoveLinear_Response__Sequence * input,
  lara_interfaces__srv__MoveLinear_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(lara_interfaces__srv__MoveLinear_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    lara_interfaces__srv__MoveLinear_Response * data =
      (lara_interfaces__srv__MoveLinear_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!lara_interfaces__srv__MoveLinear_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          lara_interfaces__srv__MoveLinear_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!lara_interfaces__srv__MoveLinear_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
