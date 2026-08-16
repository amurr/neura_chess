// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from lara_interfaces:msg/XyzRpyGoal.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "lara_interfaces/msg/detail/xyz_rpy_goal__rosidl_typesupport_introspection_c.h"
#include "lara_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "lara_interfaces/msg/detail/xyz_rpy_goal__functions.h"
#include "lara_interfaces/msg/detail/xyz_rpy_goal__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void lara_interfaces__msg__XyzRpyGoal__rosidl_typesupport_introspection_c__XyzRpyGoal_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  lara_interfaces__msg__XyzRpyGoal__init(message_memory);
}

void lara_interfaces__msg__XyzRpyGoal__rosidl_typesupport_introspection_c__XyzRpyGoal_fini_function(void * message_memory)
{
  lara_interfaces__msg__XyzRpyGoal__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember lara_interfaces__msg__XyzRpyGoal__rosidl_typesupport_introspection_c__XyzRpyGoal_message_member_array[7] = {
  {
    "x",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(lara_interfaces__msg__XyzRpyGoal, x),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "y",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(lara_interfaces__msg__XyzRpyGoal, y),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "z",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(lara_interfaces__msg__XyzRpyGoal, z),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "roll",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(lara_interfaces__msg__XyzRpyGoal, roll),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "pitch",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(lara_interfaces__msg__XyzRpyGoal, pitch),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "yaw",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(lara_interfaces__msg__XyzRpyGoal, yaw),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "use_orientation",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(lara_interfaces__msg__XyzRpyGoal, use_orientation),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers lara_interfaces__msg__XyzRpyGoal__rosidl_typesupport_introspection_c__XyzRpyGoal_message_members = {
  "lara_interfaces__msg",  // message namespace
  "XyzRpyGoal",  // message name
  7,  // number of fields
  sizeof(lara_interfaces__msg__XyzRpyGoal),
  lara_interfaces__msg__XyzRpyGoal__rosidl_typesupport_introspection_c__XyzRpyGoal_message_member_array,  // message members
  lara_interfaces__msg__XyzRpyGoal__rosidl_typesupport_introspection_c__XyzRpyGoal_init_function,  // function to initialize message memory (memory has to be allocated)
  lara_interfaces__msg__XyzRpyGoal__rosidl_typesupport_introspection_c__XyzRpyGoal_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t lara_interfaces__msg__XyzRpyGoal__rosidl_typesupport_introspection_c__XyzRpyGoal_message_type_support_handle = {
  0,
  &lara_interfaces__msg__XyzRpyGoal__rosidl_typesupport_introspection_c__XyzRpyGoal_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_lara_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, lara_interfaces, msg, XyzRpyGoal)() {
  if (!lara_interfaces__msg__XyzRpyGoal__rosidl_typesupport_introspection_c__XyzRpyGoal_message_type_support_handle.typesupport_identifier) {
    lara_interfaces__msg__XyzRpyGoal__rosidl_typesupport_introspection_c__XyzRpyGoal_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &lara_interfaces__msg__XyzRpyGoal__rosidl_typesupport_introspection_c__XyzRpyGoal_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
