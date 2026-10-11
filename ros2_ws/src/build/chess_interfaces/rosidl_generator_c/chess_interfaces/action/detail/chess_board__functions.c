// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from chess_interfaces:action/ChessBoard.idl
// generated code does not contain a copyright notice
#include "chess_interfaces/action/detail/chess_board__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `change_status`
// Member `piece_type`
// Member `to_pick`
// Member `to_place`
// Member `fen`
#include "rosidl_runtime_c/string_functions.h"

bool
chess_interfaces__action__ChessBoard_Goal__init(chess_interfaces__action__ChessBoard_Goal * msg)
{
  if (!msg) {
    return false;
  }
  // change_status
  if (!rosidl_runtime_c__String__init(&msg->change_status)) {
    chess_interfaces__action__ChessBoard_Goal__fini(msg);
    return false;
  }
  // piece_type
  if (!rosidl_runtime_c__String__init(&msg->piece_type)) {
    chess_interfaces__action__ChessBoard_Goal__fini(msg);
    return false;
  }
  // to_pick
  if (!rosidl_runtime_c__String__init(&msg->to_pick)) {
    chess_interfaces__action__ChessBoard_Goal__fini(msg);
    return false;
  }
  // to_place
  if (!rosidl_runtime_c__String__init(&msg->to_place)) {
    chess_interfaces__action__ChessBoard_Goal__fini(msg);
    return false;
  }
  // fen
  if (!rosidl_runtime_c__String__init(&msg->fen)) {
    chess_interfaces__action__ChessBoard_Goal__fini(msg);
    return false;
  }
  return true;
}

void
chess_interfaces__action__ChessBoard_Goal__fini(chess_interfaces__action__ChessBoard_Goal * msg)
{
  if (!msg) {
    return;
  }
  // change_status
  rosidl_runtime_c__String__fini(&msg->change_status);
  // piece_type
  rosidl_runtime_c__String__fini(&msg->piece_type);
  // to_pick
  rosidl_runtime_c__String__fini(&msg->to_pick);
  // to_place
  rosidl_runtime_c__String__fini(&msg->to_place);
  // fen
  rosidl_runtime_c__String__fini(&msg->fen);
}

bool
chess_interfaces__action__ChessBoard_Goal__are_equal(const chess_interfaces__action__ChessBoard_Goal * lhs, const chess_interfaces__action__ChessBoard_Goal * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // change_status
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->change_status), &(rhs->change_status)))
  {
    return false;
  }
  // piece_type
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->piece_type), &(rhs->piece_type)))
  {
    return false;
  }
  // to_pick
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->to_pick), &(rhs->to_pick)))
  {
    return false;
  }
  // to_place
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->to_place), &(rhs->to_place)))
  {
    return false;
  }
  // fen
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->fen), &(rhs->fen)))
  {
    return false;
  }
  return true;
}

bool
chess_interfaces__action__ChessBoard_Goal__copy(
  const chess_interfaces__action__ChessBoard_Goal * input,
  chess_interfaces__action__ChessBoard_Goal * output)
{
  if (!input || !output) {
    return false;
  }
  // change_status
  if (!rosidl_runtime_c__String__copy(
      &(input->change_status), &(output->change_status)))
  {
    return false;
  }
  // piece_type
  if (!rosidl_runtime_c__String__copy(
      &(input->piece_type), &(output->piece_type)))
  {
    return false;
  }
  // to_pick
  if (!rosidl_runtime_c__String__copy(
      &(input->to_pick), &(output->to_pick)))
  {
    return false;
  }
  // to_place
  if (!rosidl_runtime_c__String__copy(
      &(input->to_place), &(output->to_place)))
  {
    return false;
  }
  // fen
  if (!rosidl_runtime_c__String__copy(
      &(input->fen), &(output->fen)))
  {
    return false;
  }
  return true;
}

chess_interfaces__action__ChessBoard_Goal *
chess_interfaces__action__ChessBoard_Goal__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  chess_interfaces__action__ChessBoard_Goal * msg = (chess_interfaces__action__ChessBoard_Goal *)allocator.allocate(sizeof(chess_interfaces__action__ChessBoard_Goal), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(chess_interfaces__action__ChessBoard_Goal));
  bool success = chess_interfaces__action__ChessBoard_Goal__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
chess_interfaces__action__ChessBoard_Goal__destroy(chess_interfaces__action__ChessBoard_Goal * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    chess_interfaces__action__ChessBoard_Goal__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
chess_interfaces__action__ChessBoard_Goal__Sequence__init(chess_interfaces__action__ChessBoard_Goal__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  chess_interfaces__action__ChessBoard_Goal * data = NULL;

  if (size) {
    data = (chess_interfaces__action__ChessBoard_Goal *)allocator.zero_allocate(size, sizeof(chess_interfaces__action__ChessBoard_Goal), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = chess_interfaces__action__ChessBoard_Goal__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        chess_interfaces__action__ChessBoard_Goal__fini(&data[i - 1]);
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
chess_interfaces__action__ChessBoard_Goal__Sequence__fini(chess_interfaces__action__ChessBoard_Goal__Sequence * array)
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
      chess_interfaces__action__ChessBoard_Goal__fini(&array->data[i]);
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

chess_interfaces__action__ChessBoard_Goal__Sequence *
chess_interfaces__action__ChessBoard_Goal__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  chess_interfaces__action__ChessBoard_Goal__Sequence * array = (chess_interfaces__action__ChessBoard_Goal__Sequence *)allocator.allocate(sizeof(chess_interfaces__action__ChessBoard_Goal__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = chess_interfaces__action__ChessBoard_Goal__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
chess_interfaces__action__ChessBoard_Goal__Sequence__destroy(chess_interfaces__action__ChessBoard_Goal__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    chess_interfaces__action__ChessBoard_Goal__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
chess_interfaces__action__ChessBoard_Goal__Sequence__are_equal(const chess_interfaces__action__ChessBoard_Goal__Sequence * lhs, const chess_interfaces__action__ChessBoard_Goal__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!chess_interfaces__action__ChessBoard_Goal__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
chess_interfaces__action__ChessBoard_Goal__Sequence__copy(
  const chess_interfaces__action__ChessBoard_Goal__Sequence * input,
  chess_interfaces__action__ChessBoard_Goal__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(chess_interfaces__action__ChessBoard_Goal);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    chess_interfaces__action__ChessBoard_Goal * data =
      (chess_interfaces__action__ChessBoard_Goal *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!chess_interfaces__action__ChessBoard_Goal__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          chess_interfaces__action__ChessBoard_Goal__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!chess_interfaces__action__ChessBoard_Goal__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `message`
// Member `fen`
// already included above
// #include "rosidl_runtime_c/string_functions.h"

bool
chess_interfaces__action__ChessBoard_Result__init(chess_interfaces__action__ChessBoard_Result * msg)
{
  if (!msg) {
    return false;
  }
  // success
  // message
  if (!rosidl_runtime_c__String__init(&msg->message)) {
    chess_interfaces__action__ChessBoard_Result__fini(msg);
    return false;
  }
  // fen
  if (!rosidl_runtime_c__String__init(&msg->fen)) {
    chess_interfaces__action__ChessBoard_Result__fini(msg);
    return false;
  }
  return true;
}

void
chess_interfaces__action__ChessBoard_Result__fini(chess_interfaces__action__ChessBoard_Result * msg)
{
  if (!msg) {
    return;
  }
  // success
  // message
  rosidl_runtime_c__String__fini(&msg->message);
  // fen
  rosidl_runtime_c__String__fini(&msg->fen);
}

bool
chess_interfaces__action__ChessBoard_Result__are_equal(const chess_interfaces__action__ChessBoard_Result * lhs, const chess_interfaces__action__ChessBoard_Result * rhs)
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
  // fen
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->fen), &(rhs->fen)))
  {
    return false;
  }
  return true;
}

bool
chess_interfaces__action__ChessBoard_Result__copy(
  const chess_interfaces__action__ChessBoard_Result * input,
  chess_interfaces__action__ChessBoard_Result * output)
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
  // fen
  if (!rosidl_runtime_c__String__copy(
      &(input->fen), &(output->fen)))
  {
    return false;
  }
  return true;
}

chess_interfaces__action__ChessBoard_Result *
chess_interfaces__action__ChessBoard_Result__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  chess_interfaces__action__ChessBoard_Result * msg = (chess_interfaces__action__ChessBoard_Result *)allocator.allocate(sizeof(chess_interfaces__action__ChessBoard_Result), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(chess_interfaces__action__ChessBoard_Result));
  bool success = chess_interfaces__action__ChessBoard_Result__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
chess_interfaces__action__ChessBoard_Result__destroy(chess_interfaces__action__ChessBoard_Result * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    chess_interfaces__action__ChessBoard_Result__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
chess_interfaces__action__ChessBoard_Result__Sequence__init(chess_interfaces__action__ChessBoard_Result__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  chess_interfaces__action__ChessBoard_Result * data = NULL;

  if (size) {
    data = (chess_interfaces__action__ChessBoard_Result *)allocator.zero_allocate(size, sizeof(chess_interfaces__action__ChessBoard_Result), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = chess_interfaces__action__ChessBoard_Result__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        chess_interfaces__action__ChessBoard_Result__fini(&data[i - 1]);
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
chess_interfaces__action__ChessBoard_Result__Sequence__fini(chess_interfaces__action__ChessBoard_Result__Sequence * array)
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
      chess_interfaces__action__ChessBoard_Result__fini(&array->data[i]);
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

chess_interfaces__action__ChessBoard_Result__Sequence *
chess_interfaces__action__ChessBoard_Result__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  chess_interfaces__action__ChessBoard_Result__Sequence * array = (chess_interfaces__action__ChessBoard_Result__Sequence *)allocator.allocate(sizeof(chess_interfaces__action__ChessBoard_Result__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = chess_interfaces__action__ChessBoard_Result__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
chess_interfaces__action__ChessBoard_Result__Sequence__destroy(chess_interfaces__action__ChessBoard_Result__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    chess_interfaces__action__ChessBoard_Result__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
chess_interfaces__action__ChessBoard_Result__Sequence__are_equal(const chess_interfaces__action__ChessBoard_Result__Sequence * lhs, const chess_interfaces__action__ChessBoard_Result__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!chess_interfaces__action__ChessBoard_Result__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
chess_interfaces__action__ChessBoard_Result__Sequence__copy(
  const chess_interfaces__action__ChessBoard_Result__Sequence * input,
  chess_interfaces__action__ChessBoard_Result__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(chess_interfaces__action__ChessBoard_Result);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    chess_interfaces__action__ChessBoard_Result * data =
      (chess_interfaces__action__ChessBoard_Result *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!chess_interfaces__action__ChessBoard_Result__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          chess_interfaces__action__ChessBoard_Result__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!chess_interfaces__action__ChessBoard_Result__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `stage`
// already included above
// #include "rosidl_runtime_c/string_functions.h"

bool
chess_interfaces__action__ChessBoard_Feedback__init(chess_interfaces__action__ChessBoard_Feedback * msg)
{
  if (!msg) {
    return false;
  }
  // stage
  if (!rosidl_runtime_c__String__init(&msg->stage)) {
    chess_interfaces__action__ChessBoard_Feedback__fini(msg);
    return false;
  }
  return true;
}

void
chess_interfaces__action__ChessBoard_Feedback__fini(chess_interfaces__action__ChessBoard_Feedback * msg)
{
  if (!msg) {
    return;
  }
  // stage
  rosidl_runtime_c__String__fini(&msg->stage);
}

bool
chess_interfaces__action__ChessBoard_Feedback__are_equal(const chess_interfaces__action__ChessBoard_Feedback * lhs, const chess_interfaces__action__ChessBoard_Feedback * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // stage
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->stage), &(rhs->stage)))
  {
    return false;
  }
  return true;
}

bool
chess_interfaces__action__ChessBoard_Feedback__copy(
  const chess_interfaces__action__ChessBoard_Feedback * input,
  chess_interfaces__action__ChessBoard_Feedback * output)
{
  if (!input || !output) {
    return false;
  }
  // stage
  if (!rosidl_runtime_c__String__copy(
      &(input->stage), &(output->stage)))
  {
    return false;
  }
  return true;
}

chess_interfaces__action__ChessBoard_Feedback *
chess_interfaces__action__ChessBoard_Feedback__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  chess_interfaces__action__ChessBoard_Feedback * msg = (chess_interfaces__action__ChessBoard_Feedback *)allocator.allocate(sizeof(chess_interfaces__action__ChessBoard_Feedback), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(chess_interfaces__action__ChessBoard_Feedback));
  bool success = chess_interfaces__action__ChessBoard_Feedback__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
chess_interfaces__action__ChessBoard_Feedback__destroy(chess_interfaces__action__ChessBoard_Feedback * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    chess_interfaces__action__ChessBoard_Feedback__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
chess_interfaces__action__ChessBoard_Feedback__Sequence__init(chess_interfaces__action__ChessBoard_Feedback__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  chess_interfaces__action__ChessBoard_Feedback * data = NULL;

  if (size) {
    data = (chess_interfaces__action__ChessBoard_Feedback *)allocator.zero_allocate(size, sizeof(chess_interfaces__action__ChessBoard_Feedback), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = chess_interfaces__action__ChessBoard_Feedback__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        chess_interfaces__action__ChessBoard_Feedback__fini(&data[i - 1]);
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
chess_interfaces__action__ChessBoard_Feedback__Sequence__fini(chess_interfaces__action__ChessBoard_Feedback__Sequence * array)
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
      chess_interfaces__action__ChessBoard_Feedback__fini(&array->data[i]);
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

chess_interfaces__action__ChessBoard_Feedback__Sequence *
chess_interfaces__action__ChessBoard_Feedback__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  chess_interfaces__action__ChessBoard_Feedback__Sequence * array = (chess_interfaces__action__ChessBoard_Feedback__Sequence *)allocator.allocate(sizeof(chess_interfaces__action__ChessBoard_Feedback__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = chess_interfaces__action__ChessBoard_Feedback__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
chess_interfaces__action__ChessBoard_Feedback__Sequence__destroy(chess_interfaces__action__ChessBoard_Feedback__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    chess_interfaces__action__ChessBoard_Feedback__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
chess_interfaces__action__ChessBoard_Feedback__Sequence__are_equal(const chess_interfaces__action__ChessBoard_Feedback__Sequence * lhs, const chess_interfaces__action__ChessBoard_Feedback__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!chess_interfaces__action__ChessBoard_Feedback__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
chess_interfaces__action__ChessBoard_Feedback__Sequence__copy(
  const chess_interfaces__action__ChessBoard_Feedback__Sequence * input,
  chess_interfaces__action__ChessBoard_Feedback__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(chess_interfaces__action__ChessBoard_Feedback);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    chess_interfaces__action__ChessBoard_Feedback * data =
      (chess_interfaces__action__ChessBoard_Feedback *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!chess_interfaces__action__ChessBoard_Feedback__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          chess_interfaces__action__ChessBoard_Feedback__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!chess_interfaces__action__ChessBoard_Feedback__copy(
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
// #include "chess_interfaces/action/detail/chess_board__functions.h"

bool
chess_interfaces__action__ChessBoard_SendGoal_Request__init(chess_interfaces__action__ChessBoard_SendGoal_Request * msg)
{
  if (!msg) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__init(&msg->goal_id)) {
    chess_interfaces__action__ChessBoard_SendGoal_Request__fini(msg);
    return false;
  }
  // goal
  if (!chess_interfaces__action__ChessBoard_Goal__init(&msg->goal)) {
    chess_interfaces__action__ChessBoard_SendGoal_Request__fini(msg);
    return false;
  }
  return true;
}

void
chess_interfaces__action__ChessBoard_SendGoal_Request__fini(chess_interfaces__action__ChessBoard_SendGoal_Request * msg)
{
  if (!msg) {
    return;
  }
  // goal_id
  unique_identifier_msgs__msg__UUID__fini(&msg->goal_id);
  // goal
  chess_interfaces__action__ChessBoard_Goal__fini(&msg->goal);
}

bool
chess_interfaces__action__ChessBoard_SendGoal_Request__are_equal(const chess_interfaces__action__ChessBoard_SendGoal_Request * lhs, const chess_interfaces__action__ChessBoard_SendGoal_Request * rhs)
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
  if (!chess_interfaces__action__ChessBoard_Goal__are_equal(
      &(lhs->goal), &(rhs->goal)))
  {
    return false;
  }
  return true;
}

bool
chess_interfaces__action__ChessBoard_SendGoal_Request__copy(
  const chess_interfaces__action__ChessBoard_SendGoal_Request * input,
  chess_interfaces__action__ChessBoard_SendGoal_Request * output)
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
  if (!chess_interfaces__action__ChessBoard_Goal__copy(
      &(input->goal), &(output->goal)))
  {
    return false;
  }
  return true;
}

chess_interfaces__action__ChessBoard_SendGoal_Request *
chess_interfaces__action__ChessBoard_SendGoal_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  chess_interfaces__action__ChessBoard_SendGoal_Request * msg = (chess_interfaces__action__ChessBoard_SendGoal_Request *)allocator.allocate(sizeof(chess_interfaces__action__ChessBoard_SendGoal_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(chess_interfaces__action__ChessBoard_SendGoal_Request));
  bool success = chess_interfaces__action__ChessBoard_SendGoal_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
chess_interfaces__action__ChessBoard_SendGoal_Request__destroy(chess_interfaces__action__ChessBoard_SendGoal_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    chess_interfaces__action__ChessBoard_SendGoal_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
chess_interfaces__action__ChessBoard_SendGoal_Request__Sequence__init(chess_interfaces__action__ChessBoard_SendGoal_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  chess_interfaces__action__ChessBoard_SendGoal_Request * data = NULL;

  if (size) {
    data = (chess_interfaces__action__ChessBoard_SendGoal_Request *)allocator.zero_allocate(size, sizeof(chess_interfaces__action__ChessBoard_SendGoal_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = chess_interfaces__action__ChessBoard_SendGoal_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        chess_interfaces__action__ChessBoard_SendGoal_Request__fini(&data[i - 1]);
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
chess_interfaces__action__ChessBoard_SendGoal_Request__Sequence__fini(chess_interfaces__action__ChessBoard_SendGoal_Request__Sequence * array)
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
      chess_interfaces__action__ChessBoard_SendGoal_Request__fini(&array->data[i]);
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

chess_interfaces__action__ChessBoard_SendGoal_Request__Sequence *
chess_interfaces__action__ChessBoard_SendGoal_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  chess_interfaces__action__ChessBoard_SendGoal_Request__Sequence * array = (chess_interfaces__action__ChessBoard_SendGoal_Request__Sequence *)allocator.allocate(sizeof(chess_interfaces__action__ChessBoard_SendGoal_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = chess_interfaces__action__ChessBoard_SendGoal_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
chess_interfaces__action__ChessBoard_SendGoal_Request__Sequence__destroy(chess_interfaces__action__ChessBoard_SendGoal_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    chess_interfaces__action__ChessBoard_SendGoal_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
chess_interfaces__action__ChessBoard_SendGoal_Request__Sequence__are_equal(const chess_interfaces__action__ChessBoard_SendGoal_Request__Sequence * lhs, const chess_interfaces__action__ChessBoard_SendGoal_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!chess_interfaces__action__ChessBoard_SendGoal_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
chess_interfaces__action__ChessBoard_SendGoal_Request__Sequence__copy(
  const chess_interfaces__action__ChessBoard_SendGoal_Request__Sequence * input,
  chess_interfaces__action__ChessBoard_SendGoal_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(chess_interfaces__action__ChessBoard_SendGoal_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    chess_interfaces__action__ChessBoard_SendGoal_Request * data =
      (chess_interfaces__action__ChessBoard_SendGoal_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!chess_interfaces__action__ChessBoard_SendGoal_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          chess_interfaces__action__ChessBoard_SendGoal_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!chess_interfaces__action__ChessBoard_SendGoal_Request__copy(
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
chess_interfaces__action__ChessBoard_SendGoal_Response__init(chess_interfaces__action__ChessBoard_SendGoal_Response * msg)
{
  if (!msg) {
    return false;
  }
  // accepted
  // stamp
  if (!builtin_interfaces__msg__Time__init(&msg->stamp)) {
    chess_interfaces__action__ChessBoard_SendGoal_Response__fini(msg);
    return false;
  }
  return true;
}

void
chess_interfaces__action__ChessBoard_SendGoal_Response__fini(chess_interfaces__action__ChessBoard_SendGoal_Response * msg)
{
  if (!msg) {
    return;
  }
  // accepted
  // stamp
  builtin_interfaces__msg__Time__fini(&msg->stamp);
}

bool
chess_interfaces__action__ChessBoard_SendGoal_Response__are_equal(const chess_interfaces__action__ChessBoard_SendGoal_Response * lhs, const chess_interfaces__action__ChessBoard_SendGoal_Response * rhs)
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
chess_interfaces__action__ChessBoard_SendGoal_Response__copy(
  const chess_interfaces__action__ChessBoard_SendGoal_Response * input,
  chess_interfaces__action__ChessBoard_SendGoal_Response * output)
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

chess_interfaces__action__ChessBoard_SendGoal_Response *
chess_interfaces__action__ChessBoard_SendGoal_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  chess_interfaces__action__ChessBoard_SendGoal_Response * msg = (chess_interfaces__action__ChessBoard_SendGoal_Response *)allocator.allocate(sizeof(chess_interfaces__action__ChessBoard_SendGoal_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(chess_interfaces__action__ChessBoard_SendGoal_Response));
  bool success = chess_interfaces__action__ChessBoard_SendGoal_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
chess_interfaces__action__ChessBoard_SendGoal_Response__destroy(chess_interfaces__action__ChessBoard_SendGoal_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    chess_interfaces__action__ChessBoard_SendGoal_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
chess_interfaces__action__ChessBoard_SendGoal_Response__Sequence__init(chess_interfaces__action__ChessBoard_SendGoal_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  chess_interfaces__action__ChessBoard_SendGoal_Response * data = NULL;

  if (size) {
    data = (chess_interfaces__action__ChessBoard_SendGoal_Response *)allocator.zero_allocate(size, sizeof(chess_interfaces__action__ChessBoard_SendGoal_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = chess_interfaces__action__ChessBoard_SendGoal_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        chess_interfaces__action__ChessBoard_SendGoal_Response__fini(&data[i - 1]);
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
chess_interfaces__action__ChessBoard_SendGoal_Response__Sequence__fini(chess_interfaces__action__ChessBoard_SendGoal_Response__Sequence * array)
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
      chess_interfaces__action__ChessBoard_SendGoal_Response__fini(&array->data[i]);
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

chess_interfaces__action__ChessBoard_SendGoal_Response__Sequence *
chess_interfaces__action__ChessBoard_SendGoal_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  chess_interfaces__action__ChessBoard_SendGoal_Response__Sequence * array = (chess_interfaces__action__ChessBoard_SendGoal_Response__Sequence *)allocator.allocate(sizeof(chess_interfaces__action__ChessBoard_SendGoal_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = chess_interfaces__action__ChessBoard_SendGoal_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
chess_interfaces__action__ChessBoard_SendGoal_Response__Sequence__destroy(chess_interfaces__action__ChessBoard_SendGoal_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    chess_interfaces__action__ChessBoard_SendGoal_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
chess_interfaces__action__ChessBoard_SendGoal_Response__Sequence__are_equal(const chess_interfaces__action__ChessBoard_SendGoal_Response__Sequence * lhs, const chess_interfaces__action__ChessBoard_SendGoal_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!chess_interfaces__action__ChessBoard_SendGoal_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
chess_interfaces__action__ChessBoard_SendGoal_Response__Sequence__copy(
  const chess_interfaces__action__ChessBoard_SendGoal_Response__Sequence * input,
  chess_interfaces__action__ChessBoard_SendGoal_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(chess_interfaces__action__ChessBoard_SendGoal_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    chess_interfaces__action__ChessBoard_SendGoal_Response * data =
      (chess_interfaces__action__ChessBoard_SendGoal_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!chess_interfaces__action__ChessBoard_SendGoal_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          chess_interfaces__action__ChessBoard_SendGoal_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!chess_interfaces__action__ChessBoard_SendGoal_Response__copy(
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
chess_interfaces__action__ChessBoard_GetResult_Request__init(chess_interfaces__action__ChessBoard_GetResult_Request * msg)
{
  if (!msg) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__init(&msg->goal_id)) {
    chess_interfaces__action__ChessBoard_GetResult_Request__fini(msg);
    return false;
  }
  return true;
}

void
chess_interfaces__action__ChessBoard_GetResult_Request__fini(chess_interfaces__action__ChessBoard_GetResult_Request * msg)
{
  if (!msg) {
    return;
  }
  // goal_id
  unique_identifier_msgs__msg__UUID__fini(&msg->goal_id);
}

bool
chess_interfaces__action__ChessBoard_GetResult_Request__are_equal(const chess_interfaces__action__ChessBoard_GetResult_Request * lhs, const chess_interfaces__action__ChessBoard_GetResult_Request * rhs)
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
chess_interfaces__action__ChessBoard_GetResult_Request__copy(
  const chess_interfaces__action__ChessBoard_GetResult_Request * input,
  chess_interfaces__action__ChessBoard_GetResult_Request * output)
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

chess_interfaces__action__ChessBoard_GetResult_Request *
chess_interfaces__action__ChessBoard_GetResult_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  chess_interfaces__action__ChessBoard_GetResult_Request * msg = (chess_interfaces__action__ChessBoard_GetResult_Request *)allocator.allocate(sizeof(chess_interfaces__action__ChessBoard_GetResult_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(chess_interfaces__action__ChessBoard_GetResult_Request));
  bool success = chess_interfaces__action__ChessBoard_GetResult_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
chess_interfaces__action__ChessBoard_GetResult_Request__destroy(chess_interfaces__action__ChessBoard_GetResult_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    chess_interfaces__action__ChessBoard_GetResult_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
chess_interfaces__action__ChessBoard_GetResult_Request__Sequence__init(chess_interfaces__action__ChessBoard_GetResult_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  chess_interfaces__action__ChessBoard_GetResult_Request * data = NULL;

  if (size) {
    data = (chess_interfaces__action__ChessBoard_GetResult_Request *)allocator.zero_allocate(size, sizeof(chess_interfaces__action__ChessBoard_GetResult_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = chess_interfaces__action__ChessBoard_GetResult_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        chess_interfaces__action__ChessBoard_GetResult_Request__fini(&data[i - 1]);
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
chess_interfaces__action__ChessBoard_GetResult_Request__Sequence__fini(chess_interfaces__action__ChessBoard_GetResult_Request__Sequence * array)
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
      chess_interfaces__action__ChessBoard_GetResult_Request__fini(&array->data[i]);
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

chess_interfaces__action__ChessBoard_GetResult_Request__Sequence *
chess_interfaces__action__ChessBoard_GetResult_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  chess_interfaces__action__ChessBoard_GetResult_Request__Sequence * array = (chess_interfaces__action__ChessBoard_GetResult_Request__Sequence *)allocator.allocate(sizeof(chess_interfaces__action__ChessBoard_GetResult_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = chess_interfaces__action__ChessBoard_GetResult_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
chess_interfaces__action__ChessBoard_GetResult_Request__Sequence__destroy(chess_interfaces__action__ChessBoard_GetResult_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    chess_interfaces__action__ChessBoard_GetResult_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
chess_interfaces__action__ChessBoard_GetResult_Request__Sequence__are_equal(const chess_interfaces__action__ChessBoard_GetResult_Request__Sequence * lhs, const chess_interfaces__action__ChessBoard_GetResult_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!chess_interfaces__action__ChessBoard_GetResult_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
chess_interfaces__action__ChessBoard_GetResult_Request__Sequence__copy(
  const chess_interfaces__action__ChessBoard_GetResult_Request__Sequence * input,
  chess_interfaces__action__ChessBoard_GetResult_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(chess_interfaces__action__ChessBoard_GetResult_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    chess_interfaces__action__ChessBoard_GetResult_Request * data =
      (chess_interfaces__action__ChessBoard_GetResult_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!chess_interfaces__action__ChessBoard_GetResult_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          chess_interfaces__action__ChessBoard_GetResult_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!chess_interfaces__action__ChessBoard_GetResult_Request__copy(
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
// #include "chess_interfaces/action/detail/chess_board__functions.h"

bool
chess_interfaces__action__ChessBoard_GetResult_Response__init(chess_interfaces__action__ChessBoard_GetResult_Response * msg)
{
  if (!msg) {
    return false;
  }
  // status
  // result
  if (!chess_interfaces__action__ChessBoard_Result__init(&msg->result)) {
    chess_interfaces__action__ChessBoard_GetResult_Response__fini(msg);
    return false;
  }
  return true;
}

void
chess_interfaces__action__ChessBoard_GetResult_Response__fini(chess_interfaces__action__ChessBoard_GetResult_Response * msg)
{
  if (!msg) {
    return;
  }
  // status
  // result
  chess_interfaces__action__ChessBoard_Result__fini(&msg->result);
}

bool
chess_interfaces__action__ChessBoard_GetResult_Response__are_equal(const chess_interfaces__action__ChessBoard_GetResult_Response * lhs, const chess_interfaces__action__ChessBoard_GetResult_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // status
  if (lhs->status != rhs->status) {
    return false;
  }
  // result
  if (!chess_interfaces__action__ChessBoard_Result__are_equal(
      &(lhs->result), &(rhs->result)))
  {
    return false;
  }
  return true;
}

bool
chess_interfaces__action__ChessBoard_GetResult_Response__copy(
  const chess_interfaces__action__ChessBoard_GetResult_Response * input,
  chess_interfaces__action__ChessBoard_GetResult_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // status
  output->status = input->status;
  // result
  if (!chess_interfaces__action__ChessBoard_Result__copy(
      &(input->result), &(output->result)))
  {
    return false;
  }
  return true;
}

chess_interfaces__action__ChessBoard_GetResult_Response *
chess_interfaces__action__ChessBoard_GetResult_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  chess_interfaces__action__ChessBoard_GetResult_Response * msg = (chess_interfaces__action__ChessBoard_GetResult_Response *)allocator.allocate(sizeof(chess_interfaces__action__ChessBoard_GetResult_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(chess_interfaces__action__ChessBoard_GetResult_Response));
  bool success = chess_interfaces__action__ChessBoard_GetResult_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
chess_interfaces__action__ChessBoard_GetResult_Response__destroy(chess_interfaces__action__ChessBoard_GetResult_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    chess_interfaces__action__ChessBoard_GetResult_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
chess_interfaces__action__ChessBoard_GetResult_Response__Sequence__init(chess_interfaces__action__ChessBoard_GetResult_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  chess_interfaces__action__ChessBoard_GetResult_Response * data = NULL;

  if (size) {
    data = (chess_interfaces__action__ChessBoard_GetResult_Response *)allocator.zero_allocate(size, sizeof(chess_interfaces__action__ChessBoard_GetResult_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = chess_interfaces__action__ChessBoard_GetResult_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        chess_interfaces__action__ChessBoard_GetResult_Response__fini(&data[i - 1]);
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
chess_interfaces__action__ChessBoard_GetResult_Response__Sequence__fini(chess_interfaces__action__ChessBoard_GetResult_Response__Sequence * array)
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
      chess_interfaces__action__ChessBoard_GetResult_Response__fini(&array->data[i]);
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

chess_interfaces__action__ChessBoard_GetResult_Response__Sequence *
chess_interfaces__action__ChessBoard_GetResult_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  chess_interfaces__action__ChessBoard_GetResult_Response__Sequence * array = (chess_interfaces__action__ChessBoard_GetResult_Response__Sequence *)allocator.allocate(sizeof(chess_interfaces__action__ChessBoard_GetResult_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = chess_interfaces__action__ChessBoard_GetResult_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
chess_interfaces__action__ChessBoard_GetResult_Response__Sequence__destroy(chess_interfaces__action__ChessBoard_GetResult_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    chess_interfaces__action__ChessBoard_GetResult_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
chess_interfaces__action__ChessBoard_GetResult_Response__Sequence__are_equal(const chess_interfaces__action__ChessBoard_GetResult_Response__Sequence * lhs, const chess_interfaces__action__ChessBoard_GetResult_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!chess_interfaces__action__ChessBoard_GetResult_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
chess_interfaces__action__ChessBoard_GetResult_Response__Sequence__copy(
  const chess_interfaces__action__ChessBoard_GetResult_Response__Sequence * input,
  chess_interfaces__action__ChessBoard_GetResult_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(chess_interfaces__action__ChessBoard_GetResult_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    chess_interfaces__action__ChessBoard_GetResult_Response * data =
      (chess_interfaces__action__ChessBoard_GetResult_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!chess_interfaces__action__ChessBoard_GetResult_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          chess_interfaces__action__ChessBoard_GetResult_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!chess_interfaces__action__ChessBoard_GetResult_Response__copy(
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
// #include "chess_interfaces/action/detail/chess_board__functions.h"

bool
chess_interfaces__action__ChessBoard_FeedbackMessage__init(chess_interfaces__action__ChessBoard_FeedbackMessage * msg)
{
  if (!msg) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__init(&msg->goal_id)) {
    chess_interfaces__action__ChessBoard_FeedbackMessage__fini(msg);
    return false;
  }
  // feedback
  if (!chess_interfaces__action__ChessBoard_Feedback__init(&msg->feedback)) {
    chess_interfaces__action__ChessBoard_FeedbackMessage__fini(msg);
    return false;
  }
  return true;
}

void
chess_interfaces__action__ChessBoard_FeedbackMessage__fini(chess_interfaces__action__ChessBoard_FeedbackMessage * msg)
{
  if (!msg) {
    return;
  }
  // goal_id
  unique_identifier_msgs__msg__UUID__fini(&msg->goal_id);
  // feedback
  chess_interfaces__action__ChessBoard_Feedback__fini(&msg->feedback);
}

bool
chess_interfaces__action__ChessBoard_FeedbackMessage__are_equal(const chess_interfaces__action__ChessBoard_FeedbackMessage * lhs, const chess_interfaces__action__ChessBoard_FeedbackMessage * rhs)
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
  if (!chess_interfaces__action__ChessBoard_Feedback__are_equal(
      &(lhs->feedback), &(rhs->feedback)))
  {
    return false;
  }
  return true;
}

bool
chess_interfaces__action__ChessBoard_FeedbackMessage__copy(
  const chess_interfaces__action__ChessBoard_FeedbackMessage * input,
  chess_interfaces__action__ChessBoard_FeedbackMessage * output)
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
  if (!chess_interfaces__action__ChessBoard_Feedback__copy(
      &(input->feedback), &(output->feedback)))
  {
    return false;
  }
  return true;
}

chess_interfaces__action__ChessBoard_FeedbackMessage *
chess_interfaces__action__ChessBoard_FeedbackMessage__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  chess_interfaces__action__ChessBoard_FeedbackMessage * msg = (chess_interfaces__action__ChessBoard_FeedbackMessage *)allocator.allocate(sizeof(chess_interfaces__action__ChessBoard_FeedbackMessage), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(chess_interfaces__action__ChessBoard_FeedbackMessage));
  bool success = chess_interfaces__action__ChessBoard_FeedbackMessage__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
chess_interfaces__action__ChessBoard_FeedbackMessage__destroy(chess_interfaces__action__ChessBoard_FeedbackMessage * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    chess_interfaces__action__ChessBoard_FeedbackMessage__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
chess_interfaces__action__ChessBoard_FeedbackMessage__Sequence__init(chess_interfaces__action__ChessBoard_FeedbackMessage__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  chess_interfaces__action__ChessBoard_FeedbackMessage * data = NULL;

  if (size) {
    data = (chess_interfaces__action__ChessBoard_FeedbackMessage *)allocator.zero_allocate(size, sizeof(chess_interfaces__action__ChessBoard_FeedbackMessage), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = chess_interfaces__action__ChessBoard_FeedbackMessage__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        chess_interfaces__action__ChessBoard_FeedbackMessage__fini(&data[i - 1]);
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
chess_interfaces__action__ChessBoard_FeedbackMessage__Sequence__fini(chess_interfaces__action__ChessBoard_FeedbackMessage__Sequence * array)
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
      chess_interfaces__action__ChessBoard_FeedbackMessage__fini(&array->data[i]);
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

chess_interfaces__action__ChessBoard_FeedbackMessage__Sequence *
chess_interfaces__action__ChessBoard_FeedbackMessage__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  chess_interfaces__action__ChessBoard_FeedbackMessage__Sequence * array = (chess_interfaces__action__ChessBoard_FeedbackMessage__Sequence *)allocator.allocate(sizeof(chess_interfaces__action__ChessBoard_FeedbackMessage__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = chess_interfaces__action__ChessBoard_FeedbackMessage__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
chess_interfaces__action__ChessBoard_FeedbackMessage__Sequence__destroy(chess_interfaces__action__ChessBoard_FeedbackMessage__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    chess_interfaces__action__ChessBoard_FeedbackMessage__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
chess_interfaces__action__ChessBoard_FeedbackMessage__Sequence__are_equal(const chess_interfaces__action__ChessBoard_FeedbackMessage__Sequence * lhs, const chess_interfaces__action__ChessBoard_FeedbackMessage__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!chess_interfaces__action__ChessBoard_FeedbackMessage__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
chess_interfaces__action__ChessBoard_FeedbackMessage__Sequence__copy(
  const chess_interfaces__action__ChessBoard_FeedbackMessage__Sequence * input,
  chess_interfaces__action__ChessBoard_FeedbackMessage__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(chess_interfaces__action__ChessBoard_FeedbackMessage);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    chess_interfaces__action__ChessBoard_FeedbackMessage * data =
      (chess_interfaces__action__ChessBoard_FeedbackMessage *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!chess_interfaces__action__ChessBoard_FeedbackMessage__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          chess_interfaces__action__ChessBoard_FeedbackMessage__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!chess_interfaces__action__ChessBoard_FeedbackMessage__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
