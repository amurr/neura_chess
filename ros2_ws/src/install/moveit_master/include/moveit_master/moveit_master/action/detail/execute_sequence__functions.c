// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from moveit_master:action/ExecuteSequence.idl
// generated code does not contain a copyright notice
#include "moveit_master/action/detail/execute_sequence__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `steps`
#include "moveit_master/msg/detail/motion_step__functions.h"

bool
moveit_master__action__ExecuteSequence_Goal__init(moveit_master__action__ExecuteSequence_Goal * msg)
{
  if (!msg) {
    return false;
  }
  // steps
  if (!moveit_master__msg__MotionStep__Sequence__init(&msg->steps, 0)) {
    moveit_master__action__ExecuteSequence_Goal__fini(msg);
    return false;
  }
  // velocity_scaling
  return true;
}

void
moveit_master__action__ExecuteSequence_Goal__fini(moveit_master__action__ExecuteSequence_Goal * msg)
{
  if (!msg) {
    return;
  }
  // steps
  moveit_master__msg__MotionStep__Sequence__fini(&msg->steps);
  // velocity_scaling
}

bool
moveit_master__action__ExecuteSequence_Goal__are_equal(const moveit_master__action__ExecuteSequence_Goal * lhs, const moveit_master__action__ExecuteSequence_Goal * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // steps
  if (!moveit_master__msg__MotionStep__Sequence__are_equal(
      &(lhs->steps), &(rhs->steps)))
  {
    return false;
  }
  // velocity_scaling
  if (lhs->velocity_scaling != rhs->velocity_scaling) {
    return false;
  }
  return true;
}

bool
moveit_master__action__ExecuteSequence_Goal__copy(
  const moveit_master__action__ExecuteSequence_Goal * input,
  moveit_master__action__ExecuteSequence_Goal * output)
{
  if (!input || !output) {
    return false;
  }
  // steps
  if (!moveit_master__msg__MotionStep__Sequence__copy(
      &(input->steps), &(output->steps)))
  {
    return false;
  }
  // velocity_scaling
  output->velocity_scaling = input->velocity_scaling;
  return true;
}

moveit_master__action__ExecuteSequence_Goal *
moveit_master__action__ExecuteSequence_Goal__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  moveit_master__action__ExecuteSequence_Goal * msg = (moveit_master__action__ExecuteSequence_Goal *)allocator.allocate(sizeof(moveit_master__action__ExecuteSequence_Goal), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(moveit_master__action__ExecuteSequence_Goal));
  bool success = moveit_master__action__ExecuteSequence_Goal__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
moveit_master__action__ExecuteSequence_Goal__destroy(moveit_master__action__ExecuteSequence_Goal * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    moveit_master__action__ExecuteSequence_Goal__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
moveit_master__action__ExecuteSequence_Goal__Sequence__init(moveit_master__action__ExecuteSequence_Goal__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  moveit_master__action__ExecuteSequence_Goal * data = NULL;

  if (size) {
    data = (moveit_master__action__ExecuteSequence_Goal *)allocator.zero_allocate(size, sizeof(moveit_master__action__ExecuteSequence_Goal), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = moveit_master__action__ExecuteSequence_Goal__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        moveit_master__action__ExecuteSequence_Goal__fini(&data[i - 1]);
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
moveit_master__action__ExecuteSequence_Goal__Sequence__fini(moveit_master__action__ExecuteSequence_Goal__Sequence * array)
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
      moveit_master__action__ExecuteSequence_Goal__fini(&array->data[i]);
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

moveit_master__action__ExecuteSequence_Goal__Sequence *
moveit_master__action__ExecuteSequence_Goal__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  moveit_master__action__ExecuteSequence_Goal__Sequence * array = (moveit_master__action__ExecuteSequence_Goal__Sequence *)allocator.allocate(sizeof(moveit_master__action__ExecuteSequence_Goal__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = moveit_master__action__ExecuteSequence_Goal__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
moveit_master__action__ExecuteSequence_Goal__Sequence__destroy(moveit_master__action__ExecuteSequence_Goal__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    moveit_master__action__ExecuteSequence_Goal__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
moveit_master__action__ExecuteSequence_Goal__Sequence__are_equal(const moveit_master__action__ExecuteSequence_Goal__Sequence * lhs, const moveit_master__action__ExecuteSequence_Goal__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!moveit_master__action__ExecuteSequence_Goal__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
moveit_master__action__ExecuteSequence_Goal__Sequence__copy(
  const moveit_master__action__ExecuteSequence_Goal__Sequence * input,
  moveit_master__action__ExecuteSequence_Goal__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(moveit_master__action__ExecuteSequence_Goal);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    moveit_master__action__ExecuteSequence_Goal * data =
      (moveit_master__action__ExecuteSequence_Goal *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!moveit_master__action__ExecuteSequence_Goal__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          moveit_master__action__ExecuteSequence_Goal__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!moveit_master__action__ExecuteSequence_Goal__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `message`
#include "rosidl_runtime_c/string_functions.h"

bool
moveit_master__action__ExecuteSequence_Result__init(moveit_master__action__ExecuteSequence_Result * msg)
{
  if (!msg) {
    return false;
  }
  // success
  // failed_step
  // message
  if (!rosidl_runtime_c__String__init(&msg->message)) {
    moveit_master__action__ExecuteSequence_Result__fini(msg);
    return false;
  }
  return true;
}

void
moveit_master__action__ExecuteSequence_Result__fini(moveit_master__action__ExecuteSequence_Result * msg)
{
  if (!msg) {
    return;
  }
  // success
  // failed_step
  // message
  rosidl_runtime_c__String__fini(&msg->message);
}

bool
moveit_master__action__ExecuteSequence_Result__are_equal(const moveit_master__action__ExecuteSequence_Result * lhs, const moveit_master__action__ExecuteSequence_Result * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // success
  if (lhs->success != rhs->success) {
    return false;
  }
  // failed_step
  if (lhs->failed_step != rhs->failed_step) {
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
moveit_master__action__ExecuteSequence_Result__copy(
  const moveit_master__action__ExecuteSequence_Result * input,
  moveit_master__action__ExecuteSequence_Result * output)
{
  if (!input || !output) {
    return false;
  }
  // success
  output->success = input->success;
  // failed_step
  output->failed_step = input->failed_step;
  // message
  if (!rosidl_runtime_c__String__copy(
      &(input->message), &(output->message)))
  {
    return false;
  }
  return true;
}

moveit_master__action__ExecuteSequence_Result *
moveit_master__action__ExecuteSequence_Result__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  moveit_master__action__ExecuteSequence_Result * msg = (moveit_master__action__ExecuteSequence_Result *)allocator.allocate(sizeof(moveit_master__action__ExecuteSequence_Result), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(moveit_master__action__ExecuteSequence_Result));
  bool success = moveit_master__action__ExecuteSequence_Result__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
moveit_master__action__ExecuteSequence_Result__destroy(moveit_master__action__ExecuteSequence_Result * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    moveit_master__action__ExecuteSequence_Result__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
moveit_master__action__ExecuteSequence_Result__Sequence__init(moveit_master__action__ExecuteSequence_Result__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  moveit_master__action__ExecuteSequence_Result * data = NULL;

  if (size) {
    data = (moveit_master__action__ExecuteSequence_Result *)allocator.zero_allocate(size, sizeof(moveit_master__action__ExecuteSequence_Result), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = moveit_master__action__ExecuteSequence_Result__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        moveit_master__action__ExecuteSequence_Result__fini(&data[i - 1]);
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
moveit_master__action__ExecuteSequence_Result__Sequence__fini(moveit_master__action__ExecuteSequence_Result__Sequence * array)
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
      moveit_master__action__ExecuteSequence_Result__fini(&array->data[i]);
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

moveit_master__action__ExecuteSequence_Result__Sequence *
moveit_master__action__ExecuteSequence_Result__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  moveit_master__action__ExecuteSequence_Result__Sequence * array = (moveit_master__action__ExecuteSequence_Result__Sequence *)allocator.allocate(sizeof(moveit_master__action__ExecuteSequence_Result__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = moveit_master__action__ExecuteSequence_Result__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
moveit_master__action__ExecuteSequence_Result__Sequence__destroy(moveit_master__action__ExecuteSequence_Result__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    moveit_master__action__ExecuteSequence_Result__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
moveit_master__action__ExecuteSequence_Result__Sequence__are_equal(const moveit_master__action__ExecuteSequence_Result__Sequence * lhs, const moveit_master__action__ExecuteSequence_Result__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!moveit_master__action__ExecuteSequence_Result__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
moveit_master__action__ExecuteSequence_Result__Sequence__copy(
  const moveit_master__action__ExecuteSequence_Result__Sequence * input,
  moveit_master__action__ExecuteSequence_Result__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(moveit_master__action__ExecuteSequence_Result);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    moveit_master__action__ExecuteSequence_Result * data =
      (moveit_master__action__ExecuteSequence_Result *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!moveit_master__action__ExecuteSequence_Result__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          moveit_master__action__ExecuteSequence_Result__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!moveit_master__action__ExecuteSequence_Result__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


bool
moveit_master__action__ExecuteSequence_Feedback__init(moveit_master__action__ExecuteSequence_Feedback * msg)
{
  if (!msg) {
    return false;
  }
  // current_step
  return true;
}

void
moveit_master__action__ExecuteSequence_Feedback__fini(moveit_master__action__ExecuteSequence_Feedback * msg)
{
  if (!msg) {
    return;
  }
  // current_step
}

bool
moveit_master__action__ExecuteSequence_Feedback__are_equal(const moveit_master__action__ExecuteSequence_Feedback * lhs, const moveit_master__action__ExecuteSequence_Feedback * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // current_step
  if (lhs->current_step != rhs->current_step) {
    return false;
  }
  return true;
}

bool
moveit_master__action__ExecuteSequence_Feedback__copy(
  const moveit_master__action__ExecuteSequence_Feedback * input,
  moveit_master__action__ExecuteSequence_Feedback * output)
{
  if (!input || !output) {
    return false;
  }
  // current_step
  output->current_step = input->current_step;
  return true;
}

moveit_master__action__ExecuteSequence_Feedback *
moveit_master__action__ExecuteSequence_Feedback__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  moveit_master__action__ExecuteSequence_Feedback * msg = (moveit_master__action__ExecuteSequence_Feedback *)allocator.allocate(sizeof(moveit_master__action__ExecuteSequence_Feedback), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(moveit_master__action__ExecuteSequence_Feedback));
  bool success = moveit_master__action__ExecuteSequence_Feedback__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
moveit_master__action__ExecuteSequence_Feedback__destroy(moveit_master__action__ExecuteSequence_Feedback * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    moveit_master__action__ExecuteSequence_Feedback__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
moveit_master__action__ExecuteSequence_Feedback__Sequence__init(moveit_master__action__ExecuteSequence_Feedback__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  moveit_master__action__ExecuteSequence_Feedback * data = NULL;

  if (size) {
    data = (moveit_master__action__ExecuteSequence_Feedback *)allocator.zero_allocate(size, sizeof(moveit_master__action__ExecuteSequence_Feedback), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = moveit_master__action__ExecuteSequence_Feedback__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        moveit_master__action__ExecuteSequence_Feedback__fini(&data[i - 1]);
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
moveit_master__action__ExecuteSequence_Feedback__Sequence__fini(moveit_master__action__ExecuteSequence_Feedback__Sequence * array)
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
      moveit_master__action__ExecuteSequence_Feedback__fini(&array->data[i]);
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

moveit_master__action__ExecuteSequence_Feedback__Sequence *
moveit_master__action__ExecuteSequence_Feedback__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  moveit_master__action__ExecuteSequence_Feedback__Sequence * array = (moveit_master__action__ExecuteSequence_Feedback__Sequence *)allocator.allocate(sizeof(moveit_master__action__ExecuteSequence_Feedback__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = moveit_master__action__ExecuteSequence_Feedback__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
moveit_master__action__ExecuteSequence_Feedback__Sequence__destroy(moveit_master__action__ExecuteSequence_Feedback__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    moveit_master__action__ExecuteSequence_Feedback__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
moveit_master__action__ExecuteSequence_Feedback__Sequence__are_equal(const moveit_master__action__ExecuteSequence_Feedback__Sequence * lhs, const moveit_master__action__ExecuteSequence_Feedback__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!moveit_master__action__ExecuteSequence_Feedback__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
moveit_master__action__ExecuteSequence_Feedback__Sequence__copy(
  const moveit_master__action__ExecuteSequence_Feedback__Sequence * input,
  moveit_master__action__ExecuteSequence_Feedback__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(moveit_master__action__ExecuteSequence_Feedback);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    moveit_master__action__ExecuteSequence_Feedback * data =
      (moveit_master__action__ExecuteSequence_Feedback *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!moveit_master__action__ExecuteSequence_Feedback__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          moveit_master__action__ExecuteSequence_Feedback__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!moveit_master__action__ExecuteSequence_Feedback__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `goal_id`
#include "unique_identifier_msgs/msg/detail/uuid__functions.h"
// Member `goal`
// already included above
// #include "moveit_master/action/detail/execute_sequence__functions.h"

bool
moveit_master__action__ExecuteSequence_SendGoal_Request__init(moveit_master__action__ExecuteSequence_SendGoal_Request * msg)
{
  if (!msg) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__init(&msg->goal_id)) {
    moveit_master__action__ExecuteSequence_SendGoal_Request__fini(msg);
    return false;
  }
  // goal
  if (!moveit_master__action__ExecuteSequence_Goal__init(&msg->goal)) {
    moveit_master__action__ExecuteSequence_SendGoal_Request__fini(msg);
    return false;
  }
  return true;
}

void
moveit_master__action__ExecuteSequence_SendGoal_Request__fini(moveit_master__action__ExecuteSequence_SendGoal_Request * msg)
{
  if (!msg) {
    return;
  }
  // goal_id
  unique_identifier_msgs__msg__UUID__fini(&msg->goal_id);
  // goal
  moveit_master__action__ExecuteSequence_Goal__fini(&msg->goal);
}

bool
moveit_master__action__ExecuteSequence_SendGoal_Request__are_equal(const moveit_master__action__ExecuteSequence_SendGoal_Request * lhs, const moveit_master__action__ExecuteSequence_SendGoal_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__are_equal(
      &(lhs->goal_id), &(rhs->goal_id)))
  {
    return false;
  }
  // goal
  if (!moveit_master__action__ExecuteSequence_Goal__are_equal(
      &(lhs->goal), &(rhs->goal)))
  {
    return false;
  }
  return true;
}

bool
moveit_master__action__ExecuteSequence_SendGoal_Request__copy(
  const moveit_master__action__ExecuteSequence_SendGoal_Request * input,
  moveit_master__action__ExecuteSequence_SendGoal_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__copy(
      &(input->goal_id), &(output->goal_id)))
  {
    return false;
  }
  // goal
  if (!moveit_master__action__ExecuteSequence_Goal__copy(
      &(input->goal), &(output->goal)))
  {
    return false;
  }
  return true;
}

moveit_master__action__ExecuteSequence_SendGoal_Request *
moveit_master__action__ExecuteSequence_SendGoal_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  moveit_master__action__ExecuteSequence_SendGoal_Request * msg = (moveit_master__action__ExecuteSequence_SendGoal_Request *)allocator.allocate(sizeof(moveit_master__action__ExecuteSequence_SendGoal_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(moveit_master__action__ExecuteSequence_SendGoal_Request));
  bool success = moveit_master__action__ExecuteSequence_SendGoal_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
moveit_master__action__ExecuteSequence_SendGoal_Request__destroy(moveit_master__action__ExecuteSequence_SendGoal_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    moveit_master__action__ExecuteSequence_SendGoal_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
moveit_master__action__ExecuteSequence_SendGoal_Request__Sequence__init(moveit_master__action__ExecuteSequence_SendGoal_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  moveit_master__action__ExecuteSequence_SendGoal_Request * data = NULL;

  if (size) {
    data = (moveit_master__action__ExecuteSequence_SendGoal_Request *)allocator.zero_allocate(size, sizeof(moveit_master__action__ExecuteSequence_SendGoal_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = moveit_master__action__ExecuteSequence_SendGoal_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        moveit_master__action__ExecuteSequence_SendGoal_Request__fini(&data[i - 1]);
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
moveit_master__action__ExecuteSequence_SendGoal_Request__Sequence__fini(moveit_master__action__ExecuteSequence_SendGoal_Request__Sequence * array)
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
      moveit_master__action__ExecuteSequence_SendGoal_Request__fini(&array->data[i]);
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

moveit_master__action__ExecuteSequence_SendGoal_Request__Sequence *
moveit_master__action__ExecuteSequence_SendGoal_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  moveit_master__action__ExecuteSequence_SendGoal_Request__Sequence * array = (moveit_master__action__ExecuteSequence_SendGoal_Request__Sequence *)allocator.allocate(sizeof(moveit_master__action__ExecuteSequence_SendGoal_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = moveit_master__action__ExecuteSequence_SendGoal_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
moveit_master__action__ExecuteSequence_SendGoal_Request__Sequence__destroy(moveit_master__action__ExecuteSequence_SendGoal_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    moveit_master__action__ExecuteSequence_SendGoal_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
moveit_master__action__ExecuteSequence_SendGoal_Request__Sequence__are_equal(const moveit_master__action__ExecuteSequence_SendGoal_Request__Sequence * lhs, const moveit_master__action__ExecuteSequence_SendGoal_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!moveit_master__action__ExecuteSequence_SendGoal_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
moveit_master__action__ExecuteSequence_SendGoal_Request__Sequence__copy(
  const moveit_master__action__ExecuteSequence_SendGoal_Request__Sequence * input,
  moveit_master__action__ExecuteSequence_SendGoal_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(moveit_master__action__ExecuteSequence_SendGoal_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    moveit_master__action__ExecuteSequence_SendGoal_Request * data =
      (moveit_master__action__ExecuteSequence_SendGoal_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!moveit_master__action__ExecuteSequence_SendGoal_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          moveit_master__action__ExecuteSequence_SendGoal_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!moveit_master__action__ExecuteSequence_SendGoal_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `stamp`
#include "builtin_interfaces/msg/detail/time__functions.h"

bool
moveit_master__action__ExecuteSequence_SendGoal_Response__init(moveit_master__action__ExecuteSequence_SendGoal_Response * msg)
{
  if (!msg) {
    return false;
  }
  // accepted
  // stamp
  if (!builtin_interfaces__msg__Time__init(&msg->stamp)) {
    moveit_master__action__ExecuteSequence_SendGoal_Response__fini(msg);
    return false;
  }
  return true;
}

void
moveit_master__action__ExecuteSequence_SendGoal_Response__fini(moveit_master__action__ExecuteSequence_SendGoal_Response * msg)
{
  if (!msg) {
    return;
  }
  // accepted
  // stamp
  builtin_interfaces__msg__Time__fini(&msg->stamp);
}

bool
moveit_master__action__ExecuteSequence_SendGoal_Response__are_equal(const moveit_master__action__ExecuteSequence_SendGoal_Response * lhs, const moveit_master__action__ExecuteSequence_SendGoal_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // accepted
  if (lhs->accepted != rhs->accepted) {
    return false;
  }
  // stamp
  if (!builtin_interfaces__msg__Time__are_equal(
      &(lhs->stamp), &(rhs->stamp)))
  {
    return false;
  }
  return true;
}

bool
moveit_master__action__ExecuteSequence_SendGoal_Response__copy(
  const moveit_master__action__ExecuteSequence_SendGoal_Response * input,
  moveit_master__action__ExecuteSequence_SendGoal_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // accepted
  output->accepted = input->accepted;
  // stamp
  if (!builtin_interfaces__msg__Time__copy(
      &(input->stamp), &(output->stamp)))
  {
    return false;
  }
  return true;
}

moveit_master__action__ExecuteSequence_SendGoal_Response *
moveit_master__action__ExecuteSequence_SendGoal_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  moveit_master__action__ExecuteSequence_SendGoal_Response * msg = (moveit_master__action__ExecuteSequence_SendGoal_Response *)allocator.allocate(sizeof(moveit_master__action__ExecuteSequence_SendGoal_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(moveit_master__action__ExecuteSequence_SendGoal_Response));
  bool success = moveit_master__action__ExecuteSequence_SendGoal_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
moveit_master__action__ExecuteSequence_SendGoal_Response__destroy(moveit_master__action__ExecuteSequence_SendGoal_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    moveit_master__action__ExecuteSequence_SendGoal_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
moveit_master__action__ExecuteSequence_SendGoal_Response__Sequence__init(moveit_master__action__ExecuteSequence_SendGoal_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  moveit_master__action__ExecuteSequence_SendGoal_Response * data = NULL;

  if (size) {
    data = (moveit_master__action__ExecuteSequence_SendGoal_Response *)allocator.zero_allocate(size, sizeof(moveit_master__action__ExecuteSequence_SendGoal_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = moveit_master__action__ExecuteSequence_SendGoal_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        moveit_master__action__ExecuteSequence_SendGoal_Response__fini(&data[i - 1]);
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
moveit_master__action__ExecuteSequence_SendGoal_Response__Sequence__fini(moveit_master__action__ExecuteSequence_SendGoal_Response__Sequence * array)
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
      moveit_master__action__ExecuteSequence_SendGoal_Response__fini(&array->data[i]);
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

moveit_master__action__ExecuteSequence_SendGoal_Response__Sequence *
moveit_master__action__ExecuteSequence_SendGoal_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  moveit_master__action__ExecuteSequence_SendGoal_Response__Sequence * array = (moveit_master__action__ExecuteSequence_SendGoal_Response__Sequence *)allocator.allocate(sizeof(moveit_master__action__ExecuteSequence_SendGoal_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = moveit_master__action__ExecuteSequence_SendGoal_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
moveit_master__action__ExecuteSequence_SendGoal_Response__Sequence__destroy(moveit_master__action__ExecuteSequence_SendGoal_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    moveit_master__action__ExecuteSequence_SendGoal_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
moveit_master__action__ExecuteSequence_SendGoal_Response__Sequence__are_equal(const moveit_master__action__ExecuteSequence_SendGoal_Response__Sequence * lhs, const moveit_master__action__ExecuteSequence_SendGoal_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!moveit_master__action__ExecuteSequence_SendGoal_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
moveit_master__action__ExecuteSequence_SendGoal_Response__Sequence__copy(
  const moveit_master__action__ExecuteSequence_SendGoal_Response__Sequence * input,
  moveit_master__action__ExecuteSequence_SendGoal_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(moveit_master__action__ExecuteSequence_SendGoal_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    moveit_master__action__ExecuteSequence_SendGoal_Response * data =
      (moveit_master__action__ExecuteSequence_SendGoal_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!moveit_master__action__ExecuteSequence_SendGoal_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          moveit_master__action__ExecuteSequence_SendGoal_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!moveit_master__action__ExecuteSequence_SendGoal_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `goal_id`
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__functions.h"

bool
moveit_master__action__ExecuteSequence_GetResult_Request__init(moveit_master__action__ExecuteSequence_GetResult_Request * msg)
{
  if (!msg) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__init(&msg->goal_id)) {
    moveit_master__action__ExecuteSequence_GetResult_Request__fini(msg);
    return false;
  }
  return true;
}

void
moveit_master__action__ExecuteSequence_GetResult_Request__fini(moveit_master__action__ExecuteSequence_GetResult_Request * msg)
{
  if (!msg) {
    return;
  }
  // goal_id
  unique_identifier_msgs__msg__UUID__fini(&msg->goal_id);
}

bool
moveit_master__action__ExecuteSequence_GetResult_Request__are_equal(const moveit_master__action__ExecuteSequence_GetResult_Request * lhs, const moveit_master__action__ExecuteSequence_GetResult_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__are_equal(
      &(lhs->goal_id), &(rhs->goal_id)))
  {
    return false;
  }
  return true;
}

bool
moveit_master__action__ExecuteSequence_GetResult_Request__copy(
  const moveit_master__action__ExecuteSequence_GetResult_Request * input,
  moveit_master__action__ExecuteSequence_GetResult_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__copy(
      &(input->goal_id), &(output->goal_id)))
  {
    return false;
  }
  return true;
}

moveit_master__action__ExecuteSequence_GetResult_Request *
moveit_master__action__ExecuteSequence_GetResult_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  moveit_master__action__ExecuteSequence_GetResult_Request * msg = (moveit_master__action__ExecuteSequence_GetResult_Request *)allocator.allocate(sizeof(moveit_master__action__ExecuteSequence_GetResult_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(moveit_master__action__ExecuteSequence_GetResult_Request));
  bool success = moveit_master__action__ExecuteSequence_GetResult_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
moveit_master__action__ExecuteSequence_GetResult_Request__destroy(moveit_master__action__ExecuteSequence_GetResult_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    moveit_master__action__ExecuteSequence_GetResult_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
moveit_master__action__ExecuteSequence_GetResult_Request__Sequence__init(moveit_master__action__ExecuteSequence_GetResult_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  moveit_master__action__ExecuteSequence_GetResult_Request * data = NULL;

  if (size) {
    data = (moveit_master__action__ExecuteSequence_GetResult_Request *)allocator.zero_allocate(size, sizeof(moveit_master__action__ExecuteSequence_GetResult_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = moveit_master__action__ExecuteSequence_GetResult_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        moveit_master__action__ExecuteSequence_GetResult_Request__fini(&data[i - 1]);
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
moveit_master__action__ExecuteSequence_GetResult_Request__Sequence__fini(moveit_master__action__ExecuteSequence_GetResult_Request__Sequence * array)
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
      moveit_master__action__ExecuteSequence_GetResult_Request__fini(&array->data[i]);
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

moveit_master__action__ExecuteSequence_GetResult_Request__Sequence *
moveit_master__action__ExecuteSequence_GetResult_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  moveit_master__action__ExecuteSequence_GetResult_Request__Sequence * array = (moveit_master__action__ExecuteSequence_GetResult_Request__Sequence *)allocator.allocate(sizeof(moveit_master__action__ExecuteSequence_GetResult_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = moveit_master__action__ExecuteSequence_GetResult_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
moveit_master__action__ExecuteSequence_GetResult_Request__Sequence__destroy(moveit_master__action__ExecuteSequence_GetResult_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    moveit_master__action__ExecuteSequence_GetResult_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
moveit_master__action__ExecuteSequence_GetResult_Request__Sequence__are_equal(const moveit_master__action__ExecuteSequence_GetResult_Request__Sequence * lhs, const moveit_master__action__ExecuteSequence_GetResult_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!moveit_master__action__ExecuteSequence_GetResult_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
moveit_master__action__ExecuteSequence_GetResult_Request__Sequence__copy(
  const moveit_master__action__ExecuteSequence_GetResult_Request__Sequence * input,
  moveit_master__action__ExecuteSequence_GetResult_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(moveit_master__action__ExecuteSequence_GetResult_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    moveit_master__action__ExecuteSequence_GetResult_Request * data =
      (moveit_master__action__ExecuteSequence_GetResult_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!moveit_master__action__ExecuteSequence_GetResult_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          moveit_master__action__ExecuteSequence_GetResult_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!moveit_master__action__ExecuteSequence_GetResult_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `result`
// already included above
// #include "moveit_master/action/detail/execute_sequence__functions.h"

bool
moveit_master__action__ExecuteSequence_GetResult_Response__init(moveit_master__action__ExecuteSequence_GetResult_Response * msg)
{
  if (!msg) {
    return false;
  }
  // status
  // result
  if (!moveit_master__action__ExecuteSequence_Result__init(&msg->result)) {
    moveit_master__action__ExecuteSequence_GetResult_Response__fini(msg);
    return false;
  }
  return true;
}

void
moveit_master__action__ExecuteSequence_GetResult_Response__fini(moveit_master__action__ExecuteSequence_GetResult_Response * msg)
{
  if (!msg) {
    return;
  }
  // status
  // result
  moveit_master__action__ExecuteSequence_Result__fini(&msg->result);
}

bool
moveit_master__action__ExecuteSequence_GetResult_Response__are_equal(const moveit_master__action__ExecuteSequence_GetResult_Response * lhs, const moveit_master__action__ExecuteSequence_GetResult_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // status
  if (lhs->status != rhs->status) {
    return false;
  }
  // result
  if (!moveit_master__action__ExecuteSequence_Result__are_equal(
      &(lhs->result), &(rhs->result)))
  {
    return false;
  }
  return true;
}

bool
moveit_master__action__ExecuteSequence_GetResult_Response__copy(
  const moveit_master__action__ExecuteSequence_GetResult_Response * input,
  moveit_master__action__ExecuteSequence_GetResult_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // status
  output->status = input->status;
  // result
  if (!moveit_master__action__ExecuteSequence_Result__copy(
      &(input->result), &(output->result)))
  {
    return false;
  }
  return true;
}

moveit_master__action__ExecuteSequence_GetResult_Response *
moveit_master__action__ExecuteSequence_GetResult_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  moveit_master__action__ExecuteSequence_GetResult_Response * msg = (moveit_master__action__ExecuteSequence_GetResult_Response *)allocator.allocate(sizeof(moveit_master__action__ExecuteSequence_GetResult_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(moveit_master__action__ExecuteSequence_GetResult_Response));
  bool success = moveit_master__action__ExecuteSequence_GetResult_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
moveit_master__action__ExecuteSequence_GetResult_Response__destroy(moveit_master__action__ExecuteSequence_GetResult_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    moveit_master__action__ExecuteSequence_GetResult_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
moveit_master__action__ExecuteSequence_GetResult_Response__Sequence__init(moveit_master__action__ExecuteSequence_GetResult_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  moveit_master__action__ExecuteSequence_GetResult_Response * data = NULL;

  if (size) {
    data = (moveit_master__action__ExecuteSequence_GetResult_Response *)allocator.zero_allocate(size, sizeof(moveit_master__action__ExecuteSequence_GetResult_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = moveit_master__action__ExecuteSequence_GetResult_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        moveit_master__action__ExecuteSequence_GetResult_Response__fini(&data[i - 1]);
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
moveit_master__action__ExecuteSequence_GetResult_Response__Sequence__fini(moveit_master__action__ExecuteSequence_GetResult_Response__Sequence * array)
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
      moveit_master__action__ExecuteSequence_GetResult_Response__fini(&array->data[i]);
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

moveit_master__action__ExecuteSequence_GetResult_Response__Sequence *
moveit_master__action__ExecuteSequence_GetResult_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  moveit_master__action__ExecuteSequence_GetResult_Response__Sequence * array = (moveit_master__action__ExecuteSequence_GetResult_Response__Sequence *)allocator.allocate(sizeof(moveit_master__action__ExecuteSequence_GetResult_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = moveit_master__action__ExecuteSequence_GetResult_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
moveit_master__action__ExecuteSequence_GetResult_Response__Sequence__destroy(moveit_master__action__ExecuteSequence_GetResult_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    moveit_master__action__ExecuteSequence_GetResult_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
moveit_master__action__ExecuteSequence_GetResult_Response__Sequence__are_equal(const moveit_master__action__ExecuteSequence_GetResult_Response__Sequence * lhs, const moveit_master__action__ExecuteSequence_GetResult_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!moveit_master__action__ExecuteSequence_GetResult_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
moveit_master__action__ExecuteSequence_GetResult_Response__Sequence__copy(
  const moveit_master__action__ExecuteSequence_GetResult_Response__Sequence * input,
  moveit_master__action__ExecuteSequence_GetResult_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(moveit_master__action__ExecuteSequence_GetResult_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    moveit_master__action__ExecuteSequence_GetResult_Response * data =
      (moveit_master__action__ExecuteSequence_GetResult_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!moveit_master__action__ExecuteSequence_GetResult_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          moveit_master__action__ExecuteSequence_GetResult_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!moveit_master__action__ExecuteSequence_GetResult_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `goal_id`
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__functions.h"
// Member `feedback`
// already included above
// #include "moveit_master/action/detail/execute_sequence__functions.h"

bool
moveit_master__action__ExecuteSequence_FeedbackMessage__init(moveit_master__action__ExecuteSequence_FeedbackMessage * msg)
{
  if (!msg) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__init(&msg->goal_id)) {
    moveit_master__action__ExecuteSequence_FeedbackMessage__fini(msg);
    return false;
  }
  // feedback
  if (!moveit_master__action__ExecuteSequence_Feedback__init(&msg->feedback)) {
    moveit_master__action__ExecuteSequence_FeedbackMessage__fini(msg);
    return false;
  }
  return true;
}

void
moveit_master__action__ExecuteSequence_FeedbackMessage__fini(moveit_master__action__ExecuteSequence_FeedbackMessage * msg)
{
  if (!msg) {
    return;
  }
  // goal_id
  unique_identifier_msgs__msg__UUID__fini(&msg->goal_id);
  // feedback
  moveit_master__action__ExecuteSequence_Feedback__fini(&msg->feedback);
}

bool
moveit_master__action__ExecuteSequence_FeedbackMessage__are_equal(const moveit_master__action__ExecuteSequence_FeedbackMessage * lhs, const moveit_master__action__ExecuteSequence_FeedbackMessage * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__are_equal(
      &(lhs->goal_id), &(rhs->goal_id)))
  {
    return false;
  }
  // feedback
  if (!moveit_master__action__ExecuteSequence_Feedback__are_equal(
      &(lhs->feedback), &(rhs->feedback)))
  {
    return false;
  }
  return true;
}

bool
moveit_master__action__ExecuteSequence_FeedbackMessage__copy(
  const moveit_master__action__ExecuteSequence_FeedbackMessage * input,
  moveit_master__action__ExecuteSequence_FeedbackMessage * output)
{
  if (!input || !output) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__copy(
      &(input->goal_id), &(output->goal_id)))
  {
    return false;
  }
  // feedback
  if (!moveit_master__action__ExecuteSequence_Feedback__copy(
      &(input->feedback), &(output->feedback)))
  {
    return false;
  }
  return true;
}

moveit_master__action__ExecuteSequence_FeedbackMessage *
moveit_master__action__ExecuteSequence_FeedbackMessage__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  moveit_master__action__ExecuteSequence_FeedbackMessage * msg = (moveit_master__action__ExecuteSequence_FeedbackMessage *)allocator.allocate(sizeof(moveit_master__action__ExecuteSequence_FeedbackMessage), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(moveit_master__action__ExecuteSequence_FeedbackMessage));
  bool success = moveit_master__action__ExecuteSequence_FeedbackMessage__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
moveit_master__action__ExecuteSequence_FeedbackMessage__destroy(moveit_master__action__ExecuteSequence_FeedbackMessage * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    moveit_master__action__ExecuteSequence_FeedbackMessage__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
moveit_master__action__ExecuteSequence_FeedbackMessage__Sequence__init(moveit_master__action__ExecuteSequence_FeedbackMessage__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  moveit_master__action__ExecuteSequence_FeedbackMessage * data = NULL;

  if (size) {
    data = (moveit_master__action__ExecuteSequence_FeedbackMessage *)allocator.zero_allocate(size, sizeof(moveit_master__action__ExecuteSequence_FeedbackMessage), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = moveit_master__action__ExecuteSequence_FeedbackMessage__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        moveit_master__action__ExecuteSequence_FeedbackMessage__fini(&data[i - 1]);
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
moveit_master__action__ExecuteSequence_FeedbackMessage__Sequence__fini(moveit_master__action__ExecuteSequence_FeedbackMessage__Sequence * array)
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
      moveit_master__action__ExecuteSequence_FeedbackMessage__fini(&array->data[i]);
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

moveit_master__action__ExecuteSequence_FeedbackMessage__Sequence *
moveit_master__action__ExecuteSequence_FeedbackMessage__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  moveit_master__action__ExecuteSequence_FeedbackMessage__Sequence * array = (moveit_master__action__ExecuteSequence_FeedbackMessage__Sequence *)allocator.allocate(sizeof(moveit_master__action__ExecuteSequence_FeedbackMessage__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = moveit_master__action__ExecuteSequence_FeedbackMessage__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
moveit_master__action__ExecuteSequence_FeedbackMessage__Sequence__destroy(moveit_master__action__ExecuteSequence_FeedbackMessage__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    moveit_master__action__ExecuteSequence_FeedbackMessage__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
moveit_master__action__ExecuteSequence_FeedbackMessage__Sequence__are_equal(const moveit_master__action__ExecuteSequence_FeedbackMessage__Sequence * lhs, const moveit_master__action__ExecuteSequence_FeedbackMessage__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!moveit_master__action__ExecuteSequence_FeedbackMessage__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
moveit_master__action__ExecuteSequence_FeedbackMessage__Sequence__copy(
  const moveit_master__action__ExecuteSequence_FeedbackMessage__Sequence * input,
  moveit_master__action__ExecuteSequence_FeedbackMessage__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(moveit_master__action__ExecuteSequence_FeedbackMessage);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    moveit_master__action__ExecuteSequence_FeedbackMessage * data =
      (moveit_master__action__ExecuteSequence_FeedbackMessage *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!moveit_master__action__ExecuteSequence_FeedbackMessage__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          moveit_master__action__ExecuteSequence_FeedbackMessage__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!moveit_master__action__ExecuteSequence_FeedbackMessage__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
