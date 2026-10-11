// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from lara_interfaces:msg/XyzRpyGoal.idl
// generated code does not contain a copyright notice
#include "lara_interfaces/msg/detail/xyz_rpy_goal__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
lara_interfaces__msg__XyzRpyGoal__init(lara_interfaces__msg__XyzRpyGoal * msg)
{
  if (!msg) {
    return false;
  }
  // x
  // y
  // z
  // roll
  // pitch
  // yaw
  // use_orientation
  return true;
}

void
lara_interfaces__msg__XyzRpyGoal__fini(lara_interfaces__msg__XyzRpyGoal * msg)
{
  if (!msg) {
    return;
  }
  // x
  // y
  // z
  // roll
  // pitch
  // yaw
  // use_orientation
}

bool
lara_interfaces__msg__XyzRpyGoal__are_equal(const lara_interfaces__msg__XyzRpyGoal * lhs, const lara_interfaces__msg__XyzRpyGoal * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // x
  if (lhs->x != rhs->x) {
    return false;
  }
  // y
  if (lhs->y != rhs->y) {
    return false;
  }
  // z
  if (lhs->z != rhs->z) {
    return false;
  }
  // roll
  if (lhs->roll != rhs->roll) {
    return false;
  }
  // pitch
  if (lhs->pitch != rhs->pitch) {
    return false;
  }
  // yaw
  if (lhs->yaw != rhs->yaw) {
    return false;
  }
  // use_orientation
  if (lhs->use_orientation != rhs->use_orientation) {
    return false;
  }
  return true;
}

bool
lara_interfaces__msg__XyzRpyGoal__copy(
  const lara_interfaces__msg__XyzRpyGoal * input,
  lara_interfaces__msg__XyzRpyGoal * output)
{
  if (!input || !output) {
    return false;
  }
  // x
  output->x = input->x;
  // y
  output->y = input->y;
  // z
  output->z = input->z;
  // roll
  output->roll = input->roll;
  // pitch
  output->pitch = input->pitch;
  // yaw
  output->yaw = input->yaw;
  // use_orientation
  output->use_orientation = input->use_orientation;
  return true;
}

lara_interfaces__msg__XyzRpyGoal *
lara_interfaces__msg__XyzRpyGoal__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  lara_interfaces__msg__XyzRpyGoal * msg = (lara_interfaces__msg__XyzRpyGoal *)allocator.allocate(sizeof(lara_interfaces__msg__XyzRpyGoal), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(lara_interfaces__msg__XyzRpyGoal));
  bool success = lara_interfaces__msg__XyzRpyGoal__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
lara_interfaces__msg__XyzRpyGoal__destroy(lara_interfaces__msg__XyzRpyGoal * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    lara_interfaces__msg__XyzRpyGoal__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
lara_interfaces__msg__XyzRpyGoal__Sequence__init(lara_interfaces__msg__XyzRpyGoal__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  lara_interfaces__msg__XyzRpyGoal * data = NULL;

  if (size) {
    data = (lara_interfaces__msg__XyzRpyGoal *)allocator.zero_allocate(size, sizeof(lara_interfaces__msg__XyzRpyGoal), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = lara_interfaces__msg__XyzRpyGoal__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        lara_interfaces__msg__XyzRpyGoal__fini(&data[i - 1]);
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
lara_interfaces__msg__XyzRpyGoal__Sequence__fini(lara_interfaces__msg__XyzRpyGoal__Sequence * array)
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
      lara_interfaces__msg__XyzRpyGoal__fini(&array->data[i]);
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

lara_interfaces__msg__XyzRpyGoal__Sequence *
lara_interfaces__msg__XyzRpyGoal__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  lara_interfaces__msg__XyzRpyGoal__Sequence * array = (lara_interfaces__msg__XyzRpyGoal__Sequence *)allocator.allocate(sizeof(lara_interfaces__msg__XyzRpyGoal__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = lara_interfaces__msg__XyzRpyGoal__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
lara_interfaces__msg__XyzRpyGoal__Sequence__destroy(lara_interfaces__msg__XyzRpyGoal__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    lara_interfaces__msg__XyzRpyGoal__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
lara_interfaces__msg__XyzRpyGoal__Sequence__are_equal(const lara_interfaces__msg__XyzRpyGoal__Sequence * lhs, const lara_interfaces__msg__XyzRpyGoal__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!lara_interfaces__msg__XyzRpyGoal__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
lara_interfaces__msg__XyzRpyGoal__Sequence__copy(
  const lara_interfaces__msg__XyzRpyGoal__Sequence * input,
  lara_interfaces__msg__XyzRpyGoal__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(lara_interfaces__msg__XyzRpyGoal);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    lara_interfaces__msg__XyzRpyGoal * data =
      (lara_interfaces__msg__XyzRpyGoal *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!lara_interfaces__msg__XyzRpyGoal__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          lara_interfaces__msg__XyzRpyGoal__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!lara_interfaces__msg__XyzRpyGoal__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
