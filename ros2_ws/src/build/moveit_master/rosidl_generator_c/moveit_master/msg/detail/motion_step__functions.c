// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from moveit_master:msg/MotionStep.idl
// generated code does not contain a copyright notice
#include "moveit_master/msg/detail/motion_step__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `pose`
#include "geometry_msgs/msg/detail/pose__functions.h"
// Member `named_target`
// Member `object_id`
// Member `touch_links`
#include "rosidl_runtime_c/string_functions.h"
// Member `offset`
#include "geometry_msgs/msg/detail/vector3__functions.h"

bool
moveit_master__msg__MotionStep__init(moveit_master__msg__MotionStep * msg)
{
  if (!msg) {
    return false;
  }
  // type
  // pose
  if (!geometry_msgs__msg__Pose__init(&msg->pose)) {
    moveit_master__msg__MotionStep__fini(msg);
    return false;
  }
  // named_target
  if (!rosidl_runtime_c__String__init(&msg->named_target)) {
    moveit_master__msg__MotionStep__fini(msg);
    return false;
  }
  // duration
  // joint_value
  // offset
  if (!geometry_msgs__msg__Vector3__init(&msg->offset)) {
    moveit_master__msg__MotionStep__fini(msg);
    return false;
  }
  // object_id
  if (!rosidl_runtime_c__String__init(&msg->object_id)) {
    moveit_master__msg__MotionStep__fini(msg);
    return false;
  }
  // touch_links
  if (!rosidl_runtime_c__String__Sequence__init(&msg->touch_links, 0)) {
    moveit_master__msg__MotionStep__fini(msg);
    return false;
  }
  // allow
  return true;
}

void
moveit_master__msg__MotionStep__fini(moveit_master__msg__MotionStep * msg)
{
  if (!msg) {
    return;
  }
  // type
  // pose
  geometry_msgs__msg__Pose__fini(&msg->pose);
  // named_target
  rosidl_runtime_c__String__fini(&msg->named_target);
  // duration
  // joint_value
  // offset
  geometry_msgs__msg__Vector3__fini(&msg->offset);
  // object_id
  rosidl_runtime_c__String__fini(&msg->object_id);
  // touch_links
  rosidl_runtime_c__String__Sequence__fini(&msg->touch_links);
  // allow
}

bool
moveit_master__msg__MotionStep__are_equal(const moveit_master__msg__MotionStep * lhs, const moveit_master__msg__MotionStep * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // type
  if (lhs->type != rhs->type) {
    return false;
  }
  // pose
  if (!geometry_msgs__msg__Pose__are_equal(
      &(lhs->pose), &(rhs->pose)))
  {
    return false;
  }
  // named_target
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->named_target), &(rhs->named_target)))
  {
    return false;
  }
  // duration
  if (lhs->duration != rhs->duration) {
    return false;
  }
  // joint_value
  if (lhs->joint_value != rhs->joint_value) {
    return false;
  }
  // offset
  if (!geometry_msgs__msg__Vector3__are_equal(
      &(lhs->offset), &(rhs->offset)))
  {
    return false;
  }
  // object_id
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->object_id), &(rhs->object_id)))
  {
    return false;
  }
  // touch_links
  if (!rosidl_runtime_c__String__Sequence__are_equal(
      &(lhs->touch_links), &(rhs->touch_links)))
  {
    return false;
  }
  // allow
  if (lhs->allow != rhs->allow) {
    return false;
  }
  return true;
}

bool
moveit_master__msg__MotionStep__copy(
  const moveit_master__msg__MotionStep * input,
  moveit_master__msg__MotionStep * output)
{
  if (!input || !output) {
    return false;
  }
  // type
  output->type = input->type;
  // pose
  if (!geometry_msgs__msg__Pose__copy(
      &(input->pose), &(output->pose)))
  {
    return false;
  }
  // named_target
  if (!rosidl_runtime_c__String__copy(
      &(input->named_target), &(output->named_target)))
  {
    return false;
  }
  // duration
  output->duration = input->duration;
  // joint_value
  output->joint_value = input->joint_value;
  // offset
  if (!geometry_msgs__msg__Vector3__copy(
      &(input->offset), &(output->offset)))
  {
    return false;
  }
  // object_id
  if (!rosidl_runtime_c__String__copy(
      &(input->object_id), &(output->object_id)))
  {
    return false;
  }
  // touch_links
  if (!rosidl_runtime_c__String__Sequence__copy(
      &(input->touch_links), &(output->touch_links)))
  {
    return false;
  }
  // allow
  output->allow = input->allow;
  return true;
}

moveit_master__msg__MotionStep *
moveit_master__msg__MotionStep__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  moveit_master__msg__MotionStep * msg = (moveit_master__msg__MotionStep *)allocator.allocate(sizeof(moveit_master__msg__MotionStep), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(moveit_master__msg__MotionStep));
  bool success = moveit_master__msg__MotionStep__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
moveit_master__msg__MotionStep__destroy(moveit_master__msg__MotionStep * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    moveit_master__msg__MotionStep__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
moveit_master__msg__MotionStep__Sequence__init(moveit_master__msg__MotionStep__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  moveit_master__msg__MotionStep * data = NULL;

  if (size) {
    data = (moveit_master__msg__MotionStep *)allocator.zero_allocate(size, sizeof(moveit_master__msg__MotionStep), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = moveit_master__msg__MotionStep__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        moveit_master__msg__MotionStep__fini(&data[i - 1]);
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
moveit_master__msg__MotionStep__Sequence__fini(moveit_master__msg__MotionStep__Sequence * array)
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
      moveit_master__msg__MotionStep__fini(&array->data[i]);
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

moveit_master__msg__MotionStep__Sequence *
moveit_master__msg__MotionStep__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  moveit_master__msg__MotionStep__Sequence * array = (moveit_master__msg__MotionStep__Sequence *)allocator.allocate(sizeof(moveit_master__msg__MotionStep__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = moveit_master__msg__MotionStep__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
moveit_master__msg__MotionStep__Sequence__destroy(moveit_master__msg__MotionStep__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    moveit_master__msg__MotionStep__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
moveit_master__msg__MotionStep__Sequence__are_equal(const moveit_master__msg__MotionStep__Sequence * lhs, const moveit_master__msg__MotionStep__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!moveit_master__msg__MotionStep__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
moveit_master__msg__MotionStep__Sequence__copy(
  const moveit_master__msg__MotionStep__Sequence * input,
  moveit_master__msg__MotionStep__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(moveit_master__msg__MotionStep);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    moveit_master__msg__MotionStep * data =
      (moveit_master__msg__MotionStep *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!moveit_master__msg__MotionStep__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          moveit_master__msg__MotionStep__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!moveit_master__msg__MotionStep__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
