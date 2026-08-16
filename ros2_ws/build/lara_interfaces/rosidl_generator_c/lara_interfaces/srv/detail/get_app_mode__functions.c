// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from lara_interfaces:srv/GetAppMode.idl
// generated code does not contain a copyright notice
#include "lara_interfaces/srv/detail/get_app_mode__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

bool
lara_interfaces__srv__GetAppMode_Request__init(lara_interfaces__srv__GetAppMode_Request * msg)
{
  if (!msg) {
    return false;
  }
  // structure_needs_at_least_one_member
  return true;
}

void
lara_interfaces__srv__GetAppMode_Request__fini(lara_interfaces__srv__GetAppMode_Request * msg)
{
  if (!msg) {
    return;
  }
  // structure_needs_at_least_one_member
}

bool
lara_interfaces__srv__GetAppMode_Request__are_equal(const lara_interfaces__srv__GetAppMode_Request * lhs, const lara_interfaces__srv__GetAppMode_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // structure_needs_at_least_one_member
  if (lhs->structure_needs_at_least_one_member != rhs->structure_needs_at_least_one_member) {
    return false;
  }
  return true;
}

bool
lara_interfaces__srv__GetAppMode_Request__copy(
  const lara_interfaces__srv__GetAppMode_Request * input,
  lara_interfaces__srv__GetAppMode_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // structure_needs_at_least_one_member
  output->structure_needs_at_least_one_member = input->structure_needs_at_least_one_member;
  return true;
}

lara_interfaces__srv__GetAppMode_Request *
lara_interfaces__srv__GetAppMode_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  lara_interfaces__srv__GetAppMode_Request * msg = (lara_interfaces__srv__GetAppMode_Request *)allocator.allocate(sizeof(lara_interfaces__srv__GetAppMode_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(lara_interfaces__srv__GetAppMode_Request));
  bool success = lara_interfaces__srv__GetAppMode_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
lara_interfaces__srv__GetAppMode_Request__destroy(lara_interfaces__srv__GetAppMode_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    lara_interfaces__srv__GetAppMode_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
lara_interfaces__srv__GetAppMode_Request__Sequence__init(lara_interfaces__srv__GetAppMode_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  lara_interfaces__srv__GetAppMode_Request * data = NULL;

  if (size) {
    data = (lara_interfaces__srv__GetAppMode_Request *)allocator.zero_allocate(size, sizeof(lara_interfaces__srv__GetAppMode_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = lara_interfaces__srv__GetAppMode_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        lara_interfaces__srv__GetAppMode_Request__fini(&data[i - 1]);
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
lara_interfaces__srv__GetAppMode_Request__Sequence__fini(lara_interfaces__srv__GetAppMode_Request__Sequence * array)
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
      lara_interfaces__srv__GetAppMode_Request__fini(&array->data[i]);
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

lara_interfaces__srv__GetAppMode_Request__Sequence *
lara_interfaces__srv__GetAppMode_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  lara_interfaces__srv__GetAppMode_Request__Sequence * array = (lara_interfaces__srv__GetAppMode_Request__Sequence *)allocator.allocate(sizeof(lara_interfaces__srv__GetAppMode_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = lara_interfaces__srv__GetAppMode_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
lara_interfaces__srv__GetAppMode_Request__Sequence__destroy(lara_interfaces__srv__GetAppMode_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    lara_interfaces__srv__GetAppMode_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
lara_interfaces__srv__GetAppMode_Request__Sequence__are_equal(const lara_interfaces__srv__GetAppMode_Request__Sequence * lhs, const lara_interfaces__srv__GetAppMode_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!lara_interfaces__srv__GetAppMode_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
lara_interfaces__srv__GetAppMode_Request__Sequence__copy(
  const lara_interfaces__srv__GetAppMode_Request__Sequence * input,
  lara_interfaces__srv__GetAppMode_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(lara_interfaces__srv__GetAppMode_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    lara_interfaces__srv__GetAppMode_Request * data =
      (lara_interfaces__srv__GetAppMode_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!lara_interfaces__srv__GetAppMode_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          lara_interfaces__srv__GetAppMode_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!lara_interfaces__srv__GetAppMode_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `mode`
#include "rosidl_runtime_c/string_functions.h"

bool
lara_interfaces__srv__GetAppMode_Response__init(lara_interfaces__srv__GetAppMode_Response * msg)
{
  if (!msg) {
    return false;
  }
  // mode
  if (!rosidl_runtime_c__String__init(&msg->mode)) {
    lara_interfaces__srv__GetAppMode_Response__fini(msg);
    return false;
  }
  return true;
}

void
lara_interfaces__srv__GetAppMode_Response__fini(lara_interfaces__srv__GetAppMode_Response * msg)
{
  if (!msg) {
    return;
  }
  // mode
  rosidl_runtime_c__String__fini(&msg->mode);
}

bool
lara_interfaces__srv__GetAppMode_Response__are_equal(const lara_interfaces__srv__GetAppMode_Response * lhs, const lara_interfaces__srv__GetAppMode_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // mode
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->mode), &(rhs->mode)))
  {
    return false;
  }
  return true;
}

bool
lara_interfaces__srv__GetAppMode_Response__copy(
  const lara_interfaces__srv__GetAppMode_Response * input,
  lara_interfaces__srv__GetAppMode_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // mode
  if (!rosidl_runtime_c__String__copy(
      &(input->mode), &(output->mode)))
  {
    return false;
  }
  return true;
}

lara_interfaces__srv__GetAppMode_Response *
lara_interfaces__srv__GetAppMode_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  lara_interfaces__srv__GetAppMode_Response * msg = (lara_interfaces__srv__GetAppMode_Response *)allocator.allocate(sizeof(lara_interfaces__srv__GetAppMode_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(lara_interfaces__srv__GetAppMode_Response));
  bool success = lara_interfaces__srv__GetAppMode_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
lara_interfaces__srv__GetAppMode_Response__destroy(lara_interfaces__srv__GetAppMode_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    lara_interfaces__srv__GetAppMode_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
lara_interfaces__srv__GetAppMode_Response__Sequence__init(lara_interfaces__srv__GetAppMode_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  lara_interfaces__srv__GetAppMode_Response * data = NULL;

  if (size) {
    data = (lara_interfaces__srv__GetAppMode_Response *)allocator.zero_allocate(size, sizeof(lara_interfaces__srv__GetAppMode_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = lara_interfaces__srv__GetAppMode_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        lara_interfaces__srv__GetAppMode_Response__fini(&data[i - 1]);
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
lara_interfaces__srv__GetAppMode_Response__Sequence__fini(lara_interfaces__srv__GetAppMode_Response__Sequence * array)
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
      lara_interfaces__srv__GetAppMode_Response__fini(&array->data[i]);
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

lara_interfaces__srv__GetAppMode_Response__Sequence *
lara_interfaces__srv__GetAppMode_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  lara_interfaces__srv__GetAppMode_Response__Sequence * array = (lara_interfaces__srv__GetAppMode_Response__Sequence *)allocator.allocate(sizeof(lara_interfaces__srv__GetAppMode_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = lara_interfaces__srv__GetAppMode_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
lara_interfaces__srv__GetAppMode_Response__Sequence__destroy(lara_interfaces__srv__GetAppMode_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    lara_interfaces__srv__GetAppMode_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
lara_interfaces__srv__GetAppMode_Response__Sequence__are_equal(const lara_interfaces__srv__GetAppMode_Response__Sequence * lhs, const lara_interfaces__srv__GetAppMode_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!lara_interfaces__srv__GetAppMode_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
lara_interfaces__srv__GetAppMode_Response__Sequence__copy(
  const lara_interfaces__srv__GetAppMode_Response__Sequence * input,
  lara_interfaces__srv__GetAppMode_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(lara_interfaces__srv__GetAppMode_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    lara_interfaces__srv__GetAppMode_Response * data =
      (lara_interfaces__srv__GetAppMode_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!lara_interfaces__srv__GetAppMode_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          lara_interfaces__srv__GetAppMode_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!lara_interfaces__srv__GetAppMode_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
