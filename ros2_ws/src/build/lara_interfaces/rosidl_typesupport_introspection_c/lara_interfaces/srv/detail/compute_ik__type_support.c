// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from lara_interfaces:srv/ComputeIK.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "lara_interfaces/srv/detail/compute_ik__rosidl_typesupport_introspection_c.h"
#include "lara_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "lara_interfaces/srv/detail/compute_ik__functions.h"
#include "lara_interfaces/srv/detail/compute_ik__struct.h"


// Include directives for member types
// Member `target_pose`
#include "geometry_msgs/msg/pose.h"
// Member `target_pose`
#include "geometry_msgs/msg/detail/pose__rosidl_typesupport_introspection_c.h"
// Member `seed_joint_positions`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void lara_interfaces__srv__ComputeIK_Request__rosidl_typesupport_introspection_c__ComputeIK_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  lara_interfaces__srv__ComputeIK_Request__init(message_memory);
}

void lara_interfaces__srv__ComputeIK_Request__rosidl_typesupport_introspection_c__ComputeIK_Request_fini_function(void * message_memory)
{
  lara_interfaces__srv__ComputeIK_Request__fini(message_memory);
}

size_t lara_interfaces__srv__ComputeIK_Request__rosidl_typesupport_introspection_c__size_function__ComputeIK_Request__seed_joint_positions(
  const void * untyped_member)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return member->size;
}

const void * lara_interfaces__srv__ComputeIK_Request__rosidl_typesupport_introspection_c__get_const_function__ComputeIK_Request__seed_joint_positions(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void * lara_interfaces__srv__ComputeIK_Request__rosidl_typesupport_introspection_c__get_function__ComputeIK_Request__seed_joint_positions(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void lara_interfaces__srv__ComputeIK_Request__rosidl_typesupport_introspection_c__fetch_function__ComputeIK_Request__seed_joint_positions(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    lara_interfaces__srv__ComputeIK_Request__rosidl_typesupport_introspection_c__get_const_function__ComputeIK_Request__seed_joint_positions(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void lara_interfaces__srv__ComputeIK_Request__rosidl_typesupport_introspection_c__assign_function__ComputeIK_Request__seed_joint_positions(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    lara_interfaces__srv__ComputeIK_Request__rosidl_typesupport_introspection_c__get_function__ComputeIK_Request__seed_joint_positions(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

bool lara_interfaces__srv__ComputeIK_Request__rosidl_typesupport_introspection_c__resize_function__ComputeIK_Request__seed_joint_positions(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  rosidl_runtime_c__double__Sequence__fini(member);
  return rosidl_runtime_c__double__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember lara_interfaces__srv__ComputeIK_Request__rosidl_typesupport_introspection_c__ComputeIK_Request_message_member_array[6] = {
  {
    "target_pose",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(lara_interfaces__srv__ComputeIK_Request, target_pose),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "seed_joint_positions",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(lara_interfaces__srv__ComputeIK_Request, seed_joint_positions),  // bytes offset in struct
    NULL,  // default value
    lara_interfaces__srv__ComputeIK_Request__rosidl_typesupport_introspection_c__size_function__ComputeIK_Request__seed_joint_positions,  // size() function pointer
    lara_interfaces__srv__ComputeIK_Request__rosidl_typesupport_introspection_c__get_const_function__ComputeIK_Request__seed_joint_positions,  // get_const(index) function pointer
    lara_interfaces__srv__ComputeIK_Request__rosidl_typesupport_introspection_c__get_function__ComputeIK_Request__seed_joint_positions,  // get(index) function pointer
    lara_interfaces__srv__ComputeIK_Request__rosidl_typesupport_introspection_c__fetch_function__ComputeIK_Request__seed_joint_positions,  // fetch(index, &value) function pointer
    lara_interfaces__srv__ComputeIK_Request__rosidl_typesupport_introspection_c__assign_function__ComputeIK_Request__seed_joint_positions,  // assign(index, value) function pointer
    lara_interfaces__srv__ComputeIK_Request__rosidl_typesupport_introspection_c__resize_function__ComputeIK_Request__seed_joint_positions  // resize(index) function pointer
  },
  {
    "timeout_sec",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(lara_interfaces__srv__ComputeIK_Request, timeout_sec),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "position_tolerance",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(lara_interfaces__srv__ComputeIK_Request, position_tolerance),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "orientation_tolerance",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(lara_interfaces__srv__ComputeIK_Request, orientation_tolerance),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "enforce_joint_limits_mode",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(lara_interfaces__srv__ComputeIK_Request, enforce_joint_limits_mode),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers lara_interfaces__srv__ComputeIK_Request__rosidl_typesupport_introspection_c__ComputeIK_Request_message_members = {
  "lara_interfaces__srv",  // message namespace
  "ComputeIK_Request",  // message name
  6,  // number of fields
  sizeof(lara_interfaces__srv__ComputeIK_Request),
  lara_interfaces__srv__ComputeIK_Request__rosidl_typesupport_introspection_c__ComputeIK_Request_message_member_array,  // message members
  lara_interfaces__srv__ComputeIK_Request__rosidl_typesupport_introspection_c__ComputeIK_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  lara_interfaces__srv__ComputeIK_Request__rosidl_typesupport_introspection_c__ComputeIK_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t lara_interfaces__srv__ComputeIK_Request__rosidl_typesupport_introspection_c__ComputeIK_Request_message_type_support_handle = {
  0,
  &lara_interfaces__srv__ComputeIK_Request__rosidl_typesupport_introspection_c__ComputeIK_Request_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_lara_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, lara_interfaces, srv, ComputeIK_Request)() {
  lara_interfaces__srv__ComputeIK_Request__rosidl_typesupport_introspection_c__ComputeIK_Request_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, Pose)();
  if (!lara_interfaces__srv__ComputeIK_Request__rosidl_typesupport_introspection_c__ComputeIK_Request_message_type_support_handle.typesupport_identifier) {
    lara_interfaces__srv__ComputeIK_Request__rosidl_typesupport_introspection_c__ComputeIK_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &lara_interfaces__srv__ComputeIK_Request__rosidl_typesupport_introspection_c__ComputeIK_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "lara_interfaces/srv/detail/compute_ik__rosidl_typesupport_introspection_c.h"
// already included above
// #include "lara_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "lara_interfaces/srv/detail/compute_ik__functions.h"
// already included above
// #include "lara_interfaces/srv/detail/compute_ik__struct.h"


// Include directives for member types
// Member `message`
// Member `joint_names`
#include "rosidl_runtime_c/string_functions.h"
// Member `joint_positions`
// already included above
// #include "rosidl_runtime_c/primitives_sequence_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void lara_interfaces__srv__ComputeIK_Response__rosidl_typesupport_introspection_c__ComputeIK_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  lara_interfaces__srv__ComputeIK_Response__init(message_memory);
}

void lara_interfaces__srv__ComputeIK_Response__rosidl_typesupport_introspection_c__ComputeIK_Response_fini_function(void * message_memory)
{
  lara_interfaces__srv__ComputeIK_Response__fini(message_memory);
}

size_t lara_interfaces__srv__ComputeIK_Response__rosidl_typesupport_introspection_c__size_function__ComputeIK_Response__joint_names(
  const void * untyped_member)
{
  const rosidl_runtime_c__String__Sequence * member =
    (const rosidl_runtime_c__String__Sequence *)(untyped_member);
  return member->size;
}

const void * lara_interfaces__srv__ComputeIK_Response__rosidl_typesupport_introspection_c__get_const_function__ComputeIK_Response__joint_names(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__String__Sequence * member =
    (const rosidl_runtime_c__String__Sequence *)(untyped_member);
  return &member->data[index];
}

void * lara_interfaces__srv__ComputeIK_Response__rosidl_typesupport_introspection_c__get_function__ComputeIK_Response__joint_names(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__String__Sequence * member =
    (rosidl_runtime_c__String__Sequence *)(untyped_member);
  return &member->data[index];
}

void lara_interfaces__srv__ComputeIK_Response__rosidl_typesupport_introspection_c__fetch_function__ComputeIK_Response__joint_names(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const rosidl_runtime_c__String * item =
    ((const rosidl_runtime_c__String *)
    lara_interfaces__srv__ComputeIK_Response__rosidl_typesupport_introspection_c__get_const_function__ComputeIK_Response__joint_names(untyped_member, index));
  rosidl_runtime_c__String * value =
    (rosidl_runtime_c__String *)(untyped_value);
  *value = *item;
}

void lara_interfaces__srv__ComputeIK_Response__rosidl_typesupport_introspection_c__assign_function__ComputeIK_Response__joint_names(
  void * untyped_member, size_t index, const void * untyped_value)
{
  rosidl_runtime_c__String * item =
    ((rosidl_runtime_c__String *)
    lara_interfaces__srv__ComputeIK_Response__rosidl_typesupport_introspection_c__get_function__ComputeIK_Response__joint_names(untyped_member, index));
  const rosidl_runtime_c__String * value =
    (const rosidl_runtime_c__String *)(untyped_value);
  *item = *value;
}

bool lara_interfaces__srv__ComputeIK_Response__rosidl_typesupport_introspection_c__resize_function__ComputeIK_Response__joint_names(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__String__Sequence * member =
    (rosidl_runtime_c__String__Sequence *)(untyped_member);
  rosidl_runtime_c__String__Sequence__fini(member);
  return rosidl_runtime_c__String__Sequence__init(member, size);
}

size_t lara_interfaces__srv__ComputeIK_Response__rosidl_typesupport_introspection_c__size_function__ComputeIK_Response__joint_positions(
  const void * untyped_member)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return member->size;
}

const void * lara_interfaces__srv__ComputeIK_Response__rosidl_typesupport_introspection_c__get_const_function__ComputeIK_Response__joint_positions(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void * lara_interfaces__srv__ComputeIK_Response__rosidl_typesupport_introspection_c__get_function__ComputeIK_Response__joint_positions(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void lara_interfaces__srv__ComputeIK_Response__rosidl_typesupport_introspection_c__fetch_function__ComputeIK_Response__joint_positions(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    lara_interfaces__srv__ComputeIK_Response__rosidl_typesupport_introspection_c__get_const_function__ComputeIK_Response__joint_positions(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void lara_interfaces__srv__ComputeIK_Response__rosidl_typesupport_introspection_c__assign_function__ComputeIK_Response__joint_positions(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    lara_interfaces__srv__ComputeIK_Response__rosidl_typesupport_introspection_c__get_function__ComputeIK_Response__joint_positions(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

bool lara_interfaces__srv__ComputeIK_Response__rosidl_typesupport_introspection_c__resize_function__ComputeIK_Response__joint_positions(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  rosidl_runtime_c__double__Sequence__fini(member);
  return rosidl_runtime_c__double__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember lara_interfaces__srv__ComputeIK_Response__rosidl_typesupport_introspection_c__ComputeIK_Response_message_member_array[7] = {
  {
    "success",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(lara_interfaces__srv__ComputeIK_Response, success),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "message",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(lara_interfaces__srv__ComputeIK_Response, message),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "joint_names",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(lara_interfaces__srv__ComputeIK_Response, joint_names),  // bytes offset in struct
    NULL,  // default value
    lara_interfaces__srv__ComputeIK_Response__rosidl_typesupport_introspection_c__size_function__ComputeIK_Response__joint_names,  // size() function pointer
    lara_interfaces__srv__ComputeIK_Response__rosidl_typesupport_introspection_c__get_const_function__ComputeIK_Response__joint_names,  // get_const(index) function pointer
    lara_interfaces__srv__ComputeIK_Response__rosidl_typesupport_introspection_c__get_function__ComputeIK_Response__joint_names,  // get(index) function pointer
    lara_interfaces__srv__ComputeIK_Response__rosidl_typesupport_introspection_c__fetch_function__ComputeIK_Response__joint_names,  // fetch(index, &value) function pointer
    lara_interfaces__srv__ComputeIK_Response__rosidl_typesupport_introspection_c__assign_function__ComputeIK_Response__joint_names,  // assign(index, value) function pointer
    lara_interfaces__srv__ComputeIK_Response__rosidl_typesupport_introspection_c__resize_function__ComputeIK_Response__joint_names  // resize(index) function pointer
  },
  {
    "joint_positions",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(lara_interfaces__srv__ComputeIK_Response, joint_positions),  // bytes offset in struct
    NULL,  // default value
    lara_interfaces__srv__ComputeIK_Response__rosidl_typesupport_introspection_c__size_function__ComputeIK_Response__joint_positions,  // size() function pointer
    lara_interfaces__srv__ComputeIK_Response__rosidl_typesupport_introspection_c__get_const_function__ComputeIK_Response__joint_positions,  // get_const(index) function pointer
    lara_interfaces__srv__ComputeIK_Response__rosidl_typesupport_introspection_c__get_function__ComputeIK_Response__joint_positions,  // get(index) function pointer
    lara_interfaces__srv__ComputeIK_Response__rosidl_typesupport_introspection_c__fetch_function__ComputeIK_Response__joint_positions,  // fetch(index, &value) function pointer
    lara_interfaces__srv__ComputeIK_Response__rosidl_typesupport_introspection_c__assign_function__ComputeIK_Response__joint_positions,  // assign(index, value) function pointer
    lara_interfaces__srv__ComputeIK_Response__rosidl_typesupport_introspection_c__resize_function__ComputeIK_Response__joint_positions  // resize(index) function pointer
  },
  {
    "position_error",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(lara_interfaces__srv__ComputeIK_Response, position_error),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "orientation_error",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(lara_interfaces__srv__ComputeIK_Response, orientation_error),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "iterations",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(lara_interfaces__srv__ComputeIK_Response, iterations),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers lara_interfaces__srv__ComputeIK_Response__rosidl_typesupport_introspection_c__ComputeIK_Response_message_members = {
  "lara_interfaces__srv",  // message namespace
  "ComputeIK_Response",  // message name
  7,  // number of fields
  sizeof(lara_interfaces__srv__ComputeIK_Response),
  lara_interfaces__srv__ComputeIK_Response__rosidl_typesupport_introspection_c__ComputeIK_Response_message_member_array,  // message members
  lara_interfaces__srv__ComputeIK_Response__rosidl_typesupport_introspection_c__ComputeIK_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  lara_interfaces__srv__ComputeIK_Response__rosidl_typesupport_introspection_c__ComputeIK_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t lara_interfaces__srv__ComputeIK_Response__rosidl_typesupport_introspection_c__ComputeIK_Response_message_type_support_handle = {
  0,
  &lara_interfaces__srv__ComputeIK_Response__rosidl_typesupport_introspection_c__ComputeIK_Response_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_lara_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, lara_interfaces, srv, ComputeIK_Response)() {
  if (!lara_interfaces__srv__ComputeIK_Response__rosidl_typesupport_introspection_c__ComputeIK_Response_message_type_support_handle.typesupport_identifier) {
    lara_interfaces__srv__ComputeIK_Response__rosidl_typesupport_introspection_c__ComputeIK_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &lara_interfaces__srv__ComputeIK_Response__rosidl_typesupport_introspection_c__ComputeIK_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "lara_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "lara_interfaces/srv/detail/compute_ik__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers lara_interfaces__srv__detail__compute_ik__rosidl_typesupport_introspection_c__ComputeIK_service_members = {
  "lara_interfaces__srv",  // service namespace
  "ComputeIK",  // service name
  // these two fields are initialized below on the first access
  NULL,  // request message
  // lara_interfaces__srv__detail__compute_ik__rosidl_typesupport_introspection_c__ComputeIK_Request_message_type_support_handle,
  NULL  // response message
  // lara_interfaces__srv__detail__compute_ik__rosidl_typesupport_introspection_c__ComputeIK_Response_message_type_support_handle
};

static rosidl_service_type_support_t lara_interfaces__srv__detail__compute_ik__rosidl_typesupport_introspection_c__ComputeIK_service_type_support_handle = {
  0,
  &lara_interfaces__srv__detail__compute_ik__rosidl_typesupport_introspection_c__ComputeIK_service_members,
  get_service_typesupport_handle_function,
};

// Forward declaration of request/response type support functions
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, lara_interfaces, srv, ComputeIK_Request)();

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, lara_interfaces, srv, ComputeIK_Response)();

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_lara_interfaces
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, lara_interfaces, srv, ComputeIK)() {
  if (!lara_interfaces__srv__detail__compute_ik__rosidl_typesupport_introspection_c__ComputeIK_service_type_support_handle.typesupport_identifier) {
    lara_interfaces__srv__detail__compute_ik__rosidl_typesupport_introspection_c__ComputeIK_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)lara_interfaces__srv__detail__compute_ik__rosidl_typesupport_introspection_c__ComputeIK_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, lara_interfaces, srv, ComputeIK_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, lara_interfaces, srv, ComputeIK_Response)()->data;
  }

  return &lara_interfaces__srv__detail__compute_ik__rosidl_typesupport_introspection_c__ComputeIK_service_type_support_handle;
}
