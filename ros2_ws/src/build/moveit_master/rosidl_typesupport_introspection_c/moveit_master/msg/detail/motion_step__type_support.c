// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from moveit_master:msg/MotionStep.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "moveit_master/msg/detail/motion_step__rosidl_typesupport_introspection_c.h"
#include "moveit_master/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "moveit_master/msg/detail/motion_step__functions.h"
#include "moveit_master/msg/detail/motion_step__struct.h"


// Include directives for member types
// Member `pose`
#include "geometry_msgs/msg/pose.h"
// Member `pose`
#include "geometry_msgs/msg/detail/pose__rosidl_typesupport_introspection_c.h"
// Member `named_target`
// Member `object_id`
// Member `touch_links`
#include "rosidl_runtime_c/string_functions.h"
// Member `offset`
#include "geometry_msgs/msg/vector3.h"
// Member `offset`
#include "geometry_msgs/msg/detail/vector3__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void moveit_master__msg__MotionStep__rosidl_typesupport_introspection_c__MotionStep_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  moveit_master__msg__MotionStep__init(message_memory);
}

void moveit_master__msg__MotionStep__rosidl_typesupport_introspection_c__MotionStep_fini_function(void * message_memory)
{
  moveit_master__msg__MotionStep__fini(message_memory);
}

size_t moveit_master__msg__MotionStep__rosidl_typesupport_introspection_c__size_function__MotionStep__touch_links(
  const void * untyped_member)
{
  const rosidl_runtime_c__String__Sequence * member =
    (const rosidl_runtime_c__String__Sequence *)(untyped_member);
  return member->size;
}

const void * moveit_master__msg__MotionStep__rosidl_typesupport_introspection_c__get_const_function__MotionStep__touch_links(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__String__Sequence * member =
    (const rosidl_runtime_c__String__Sequence *)(untyped_member);
  return &member->data[index];
}

void * moveit_master__msg__MotionStep__rosidl_typesupport_introspection_c__get_function__MotionStep__touch_links(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__String__Sequence * member =
    (rosidl_runtime_c__String__Sequence *)(untyped_member);
  return &member->data[index];
}

void moveit_master__msg__MotionStep__rosidl_typesupport_introspection_c__fetch_function__MotionStep__touch_links(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const rosidl_runtime_c__String * item =
    ((const rosidl_runtime_c__String *)
    moveit_master__msg__MotionStep__rosidl_typesupport_introspection_c__get_const_function__MotionStep__touch_links(untyped_member, index));
  rosidl_runtime_c__String * value =
    (rosidl_runtime_c__String *)(untyped_value);
  *value = *item;
}

void moveit_master__msg__MotionStep__rosidl_typesupport_introspection_c__assign_function__MotionStep__touch_links(
  void * untyped_member, size_t index, const void * untyped_value)
{
  rosidl_runtime_c__String * item =
    ((rosidl_runtime_c__String *)
    moveit_master__msg__MotionStep__rosidl_typesupport_introspection_c__get_function__MotionStep__touch_links(untyped_member, index));
  const rosidl_runtime_c__String * value =
    (const rosidl_runtime_c__String *)(untyped_value);
  *item = *value;
}

bool moveit_master__msg__MotionStep__rosidl_typesupport_introspection_c__resize_function__MotionStep__touch_links(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__String__Sequence * member =
    (rosidl_runtime_c__String__Sequence *)(untyped_member);
  rosidl_runtime_c__String__Sequence__fini(member);
  return rosidl_runtime_c__String__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember moveit_master__msg__MotionStep__rosidl_typesupport_introspection_c__MotionStep_message_member_array[9] = {
  {
    "type",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(moveit_master__msg__MotionStep, type),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "pose",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(moveit_master__msg__MotionStep, pose),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "named_target",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(moveit_master__msg__MotionStep, named_target),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "duration",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(moveit_master__msg__MotionStep, duration),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "joint_value",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(moveit_master__msg__MotionStep, joint_value),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "offset",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(moveit_master__msg__MotionStep, offset),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "object_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(moveit_master__msg__MotionStep, object_id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "touch_links",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(moveit_master__msg__MotionStep, touch_links),  // bytes offset in struct
    NULL,  // default value
    moveit_master__msg__MotionStep__rosidl_typesupport_introspection_c__size_function__MotionStep__touch_links,  // size() function pointer
    moveit_master__msg__MotionStep__rosidl_typesupport_introspection_c__get_const_function__MotionStep__touch_links,  // get_const(index) function pointer
    moveit_master__msg__MotionStep__rosidl_typesupport_introspection_c__get_function__MotionStep__touch_links,  // get(index) function pointer
    moveit_master__msg__MotionStep__rosidl_typesupport_introspection_c__fetch_function__MotionStep__touch_links,  // fetch(index, &value) function pointer
    moveit_master__msg__MotionStep__rosidl_typesupport_introspection_c__assign_function__MotionStep__touch_links,  // assign(index, value) function pointer
    moveit_master__msg__MotionStep__rosidl_typesupport_introspection_c__resize_function__MotionStep__touch_links  // resize(index) function pointer
  },
  {
    "allow",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(moveit_master__msg__MotionStep, allow),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers moveit_master__msg__MotionStep__rosidl_typesupport_introspection_c__MotionStep_message_members = {
  "moveit_master__msg",  // message namespace
  "MotionStep",  // message name
  9,  // number of fields
  sizeof(moveit_master__msg__MotionStep),
  moveit_master__msg__MotionStep__rosidl_typesupport_introspection_c__MotionStep_message_member_array,  // message members
  moveit_master__msg__MotionStep__rosidl_typesupport_introspection_c__MotionStep_init_function,  // function to initialize message memory (memory has to be allocated)
  moveit_master__msg__MotionStep__rosidl_typesupport_introspection_c__MotionStep_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t moveit_master__msg__MotionStep__rosidl_typesupport_introspection_c__MotionStep_message_type_support_handle = {
  0,
  &moveit_master__msg__MotionStep__rosidl_typesupport_introspection_c__MotionStep_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_moveit_master
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, moveit_master, msg, MotionStep)() {
  moveit_master__msg__MotionStep__rosidl_typesupport_introspection_c__MotionStep_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, Pose)();
  moveit_master__msg__MotionStep__rosidl_typesupport_introspection_c__MotionStep_message_member_array[5].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, Vector3)();
  if (!moveit_master__msg__MotionStep__rosidl_typesupport_introspection_c__MotionStep_message_type_support_handle.typesupport_identifier) {
    moveit_master__msg__MotionStep__rosidl_typesupport_introspection_c__MotionStep_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &moveit_master__msg__MotionStep__rosidl_typesupport_introspection_c__MotionStep_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
