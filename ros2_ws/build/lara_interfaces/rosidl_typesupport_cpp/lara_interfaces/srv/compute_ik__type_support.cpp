// generated from rosidl_typesupport_cpp/resource/idl__type_support.cpp.em
// with input from lara_interfaces:srv/ComputeIK.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "lara_interfaces/srv/detail/compute_ik__struct.hpp"
#include "rosidl_typesupport_cpp/identifier.hpp"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
#include "rosidl_typesupport_cpp/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace lara_interfaces
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _ComputeIK_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _ComputeIK_Request_type_support_ids_t;

static const _ComputeIK_Request_type_support_ids_t _ComputeIK_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _ComputeIK_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _ComputeIK_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _ComputeIK_Request_type_support_symbol_names_t _ComputeIK_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, lara_interfaces, srv, ComputeIK_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, lara_interfaces, srv, ComputeIK_Request)),
  }
};

typedef struct _ComputeIK_Request_type_support_data_t
{
  void * data[2];
} _ComputeIK_Request_type_support_data_t;

static _ComputeIK_Request_type_support_data_t _ComputeIK_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _ComputeIK_Request_message_typesupport_map = {
  2,
  "lara_interfaces",
  &_ComputeIK_Request_message_typesupport_ids.typesupport_identifier[0],
  &_ComputeIK_Request_message_typesupport_symbol_names.symbol_name[0],
  &_ComputeIK_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t ComputeIK_Request_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_ComputeIK_Request_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace lara_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<lara_interfaces::srv::ComputeIK_Request>()
{
  return &::lara_interfaces::srv::rosidl_typesupport_cpp::ComputeIK_Request_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, lara_interfaces, srv, ComputeIK_Request)() {
  return get_message_type_support_handle<lara_interfaces::srv::ComputeIK_Request>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "lara_interfaces/srv/detail/compute_ik__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace lara_interfaces
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _ComputeIK_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _ComputeIK_Response_type_support_ids_t;

static const _ComputeIK_Response_type_support_ids_t _ComputeIK_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _ComputeIK_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _ComputeIK_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _ComputeIK_Response_type_support_symbol_names_t _ComputeIK_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, lara_interfaces, srv, ComputeIK_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, lara_interfaces, srv, ComputeIK_Response)),
  }
};

typedef struct _ComputeIK_Response_type_support_data_t
{
  void * data[2];
} _ComputeIK_Response_type_support_data_t;

static _ComputeIK_Response_type_support_data_t _ComputeIK_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _ComputeIK_Response_message_typesupport_map = {
  2,
  "lara_interfaces",
  &_ComputeIK_Response_message_typesupport_ids.typesupport_identifier[0],
  &_ComputeIK_Response_message_typesupport_symbol_names.symbol_name[0],
  &_ComputeIK_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t ComputeIK_Response_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_ComputeIK_Response_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace lara_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<lara_interfaces::srv::ComputeIK_Response>()
{
  return &::lara_interfaces::srv::rosidl_typesupport_cpp::ComputeIK_Response_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, lara_interfaces, srv, ComputeIK_Response)() {
  return get_message_type_support_handle<lara_interfaces::srv::ComputeIK_Response>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "lara_interfaces/srv/detail/compute_ik__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
#include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/service_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace lara_interfaces
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _ComputeIK_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _ComputeIK_type_support_ids_t;

static const _ComputeIK_type_support_ids_t _ComputeIK_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _ComputeIK_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _ComputeIK_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _ComputeIK_type_support_symbol_names_t _ComputeIK_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, lara_interfaces, srv, ComputeIK)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, lara_interfaces, srv, ComputeIK)),
  }
};

typedef struct _ComputeIK_type_support_data_t
{
  void * data[2];
} _ComputeIK_type_support_data_t;

static _ComputeIK_type_support_data_t _ComputeIK_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _ComputeIK_service_typesupport_map = {
  2,
  "lara_interfaces",
  &_ComputeIK_service_typesupport_ids.typesupport_identifier[0],
  &_ComputeIK_service_typesupport_symbol_names.symbol_name[0],
  &_ComputeIK_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t ComputeIK_service_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_ComputeIK_service_typesupport_map),
  ::rosidl_typesupport_cpp::get_service_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace lara_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
get_service_type_support_handle<lara_interfaces::srv::ComputeIK>()
{
  return &::lara_interfaces::srv::rosidl_typesupport_cpp::ComputeIK_service_type_support_handle;
}

}  // namespace rosidl_typesupport_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_cpp, lara_interfaces, srv, ComputeIK)() {
  return ::rosidl_typesupport_cpp::get_service_type_support_handle<lara_interfaces::srv::ComputeIK>();
}

#ifdef __cplusplus
}
#endif
