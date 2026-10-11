#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



#[link(name = "lara_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__lara_interfaces__srv__GetTCPPose_Request() -> *const std::ffi::c_void;
}

#[link(name = "lara_interfaces__rosidl_generator_c")]
extern "C" {
    fn lara_interfaces__srv__GetTCPPose_Request__init(msg: *mut GetTCPPose_Request) -> bool;
    fn lara_interfaces__srv__GetTCPPose_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetTCPPose_Request>, size: usize) -> bool;
    fn lara_interfaces__srv__GetTCPPose_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetTCPPose_Request>);
    fn lara_interfaces__srv__GetTCPPose_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetTCPPose_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<GetTCPPose_Request>) -> bool;
}

// Corresponds to lara_interfaces__srv__GetTCPPose_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetTCPPose_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetTCPPose_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !lara_interfaces__srv__GetTCPPose_Request__init(&mut msg as *mut _) {
        panic!("Call to lara_interfaces__srv__GetTCPPose_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetTCPPose_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { lara_interfaces__srv__GetTCPPose_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { lara_interfaces__srv__GetTCPPose_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { lara_interfaces__srv__GetTCPPose_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetTCPPose_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetTCPPose_Request where Self: Sized {
  const TYPE_NAME: &'static str = "lara_interfaces/srv/GetTCPPose_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__lara_interfaces__srv__GetTCPPose_Request() }
  }
}


#[link(name = "lara_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__lara_interfaces__srv__GetTCPPose_Response() -> *const std::ffi::c_void;
}

#[link(name = "lara_interfaces__rosidl_generator_c")]
extern "C" {
    fn lara_interfaces__srv__GetTCPPose_Response__init(msg: *mut GetTCPPose_Response) -> bool;
    fn lara_interfaces__srv__GetTCPPose_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetTCPPose_Response>, size: usize) -> bool;
    fn lara_interfaces__srv__GetTCPPose_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetTCPPose_Response>);
    fn lara_interfaces__srv__GetTCPPose_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetTCPPose_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<GetTCPPose_Response>) -> bool;
}

// Corresponds to lara_interfaces__srv__GetTCPPose_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetTCPPose_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub pose: geometry_msgs::msg::rmw::Pose,

}



impl Default for GetTCPPose_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !lara_interfaces__srv__GetTCPPose_Response__init(&mut msg as *mut _) {
        panic!("Call to lara_interfaces__srv__GetTCPPose_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetTCPPose_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { lara_interfaces__srv__GetTCPPose_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { lara_interfaces__srv__GetTCPPose_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { lara_interfaces__srv__GetTCPPose_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetTCPPose_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetTCPPose_Response where Self: Sized {
  const TYPE_NAME: &'static str = "lara_interfaces/srv/GetTCPPose_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__lara_interfaces__srv__GetTCPPose_Response() }
  }
}


#[link(name = "lara_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__lara_interfaces__srv__MoveJoints_Request() -> *const std::ffi::c_void;
}

#[link(name = "lara_interfaces__rosidl_generator_c")]
extern "C" {
    fn lara_interfaces__srv__MoveJoints_Request__init(msg: *mut MoveJoints_Request) -> bool;
    fn lara_interfaces__srv__MoveJoints_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MoveJoints_Request>, size: usize) -> bool;
    fn lara_interfaces__srv__MoveJoints_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MoveJoints_Request>);
    fn lara_interfaces__srv__MoveJoints_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MoveJoints_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<MoveJoints_Request>) -> bool;
}

// Corresponds to lara_interfaces__srv__MoveJoints_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveJoints_Request {
    /// if set, move to teach pendant point by name (e.g. "GP7")
    pub point_name: rosidl_runtime_rs::String,

    /// degrees, 6*k waypoints (ignored if point_name is set)
    pub target_joint: rosidl_runtime_rs::Sequence<f64>,

    /// optional TCP [x,y,z,roll,pitch,yaw] m/rad — IK when target_joint empty
    pub target_pose: rosidl_runtime_rs::Sequence<f64>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub speed: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub acceleration: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub enable_safety: bool,

}



impl Default for MoveJoints_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !lara_interfaces__srv__MoveJoints_Request__init(&mut msg as *mut _) {
        panic!("Call to lara_interfaces__srv__MoveJoints_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MoveJoints_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { lara_interfaces__srv__MoveJoints_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { lara_interfaces__srv__MoveJoints_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { lara_interfaces__srv__MoveJoints_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MoveJoints_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MoveJoints_Request where Self: Sized {
  const TYPE_NAME: &'static str = "lara_interfaces/srv/MoveJoints_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__lara_interfaces__srv__MoveJoints_Request() }
  }
}


#[link(name = "lara_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__lara_interfaces__srv__MoveJoints_Response() -> *const std::ffi::c_void;
}

#[link(name = "lara_interfaces__rosidl_generator_c")]
extern "C" {
    fn lara_interfaces__srv__MoveJoints_Response__init(msg: *mut MoveJoints_Response) -> bool;
    fn lara_interfaces__srv__MoveJoints_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MoveJoints_Response>, size: usize) -> bool;
    fn lara_interfaces__srv__MoveJoints_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MoveJoints_Response>);
    fn lara_interfaces__srv__MoveJoints_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MoveJoints_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<MoveJoints_Response>) -> bool;
}

// Corresponds to lara_interfaces__srv__MoveJoints_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveJoints_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,

}



impl Default for MoveJoints_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !lara_interfaces__srv__MoveJoints_Response__init(&mut msg as *mut _) {
        panic!("Call to lara_interfaces__srv__MoveJoints_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MoveJoints_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { lara_interfaces__srv__MoveJoints_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { lara_interfaces__srv__MoveJoints_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { lara_interfaces__srv__MoveJoints_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MoveJoints_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MoveJoints_Response where Self: Sized {
  const TYPE_NAME: &'static str = "lara_interfaces/srv/MoveJoints_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__lara_interfaces__srv__MoveJoints_Response() }
  }
}


#[link(name = "lara_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__lara_interfaces__srv__MoveLinear_Request() -> *const std::ffi::c_void;
}

#[link(name = "lara_interfaces__rosidl_generator_c")]
extern "C" {
    fn lara_interfaces__srv__MoveLinear_Request__init(msg: *mut MoveLinear_Request) -> bool;
    fn lara_interfaces__srv__MoveLinear_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MoveLinear_Request>, size: usize) -> bool;
    fn lara_interfaces__srv__MoveLinear_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MoveLinear_Request>);
    fn lara_interfaces__srv__MoveLinear_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MoveLinear_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<MoveLinear_Request>) -> bool;
}

// Corresponds to lara_interfaces__srv__MoveLinear_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveLinear_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub target_pose: rosidl_runtime_rs::Sequence<f64>,

    /// m/s
    pub speed: f64,

    /// m/s^2
    pub acceleration: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub enable_safety: bool,

    /// if true, each 6-tuple is a cartesian_offset (move_linear_relative)
    pub use_relative: bool,

    /// "Base" or "Tool" (only when use_relative is true)
    pub offset_frame: rosidl_runtime_rs::String,

}



impl Default for MoveLinear_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !lara_interfaces__srv__MoveLinear_Request__init(&mut msg as *mut _) {
        panic!("Call to lara_interfaces__srv__MoveLinear_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MoveLinear_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { lara_interfaces__srv__MoveLinear_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { lara_interfaces__srv__MoveLinear_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { lara_interfaces__srv__MoveLinear_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MoveLinear_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MoveLinear_Request where Self: Sized {
  const TYPE_NAME: &'static str = "lara_interfaces/srv/MoveLinear_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__lara_interfaces__srv__MoveLinear_Request() }
  }
}


#[link(name = "lara_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__lara_interfaces__srv__MoveLinear_Response() -> *const std::ffi::c_void;
}

#[link(name = "lara_interfaces__rosidl_generator_c")]
extern "C" {
    fn lara_interfaces__srv__MoveLinear_Response__init(msg: *mut MoveLinear_Response) -> bool;
    fn lara_interfaces__srv__MoveLinear_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MoveLinear_Response>, size: usize) -> bool;
    fn lara_interfaces__srv__MoveLinear_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MoveLinear_Response>);
    fn lara_interfaces__srv__MoveLinear_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MoveLinear_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<MoveLinear_Response>) -> bool;
}

// Corresponds to lara_interfaces__srv__MoveLinear_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveLinear_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,

}



impl Default for MoveLinear_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !lara_interfaces__srv__MoveLinear_Response__init(&mut msg as *mut _) {
        panic!("Call to lara_interfaces__srv__MoveLinear_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MoveLinear_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { lara_interfaces__srv__MoveLinear_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { lara_interfaces__srv__MoveLinear_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { lara_interfaces__srv__MoveLinear_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MoveLinear_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MoveLinear_Response where Self: Sized {
  const TYPE_NAME: &'static str = "lara_interfaces/srv/MoveLinear_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__lara_interfaces__srv__MoveLinear_Response() }
  }
}


#[link(name = "lara_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__lara_interfaces__srv__GetAppMode_Request() -> *const std::ffi::c_void;
}

#[link(name = "lara_interfaces__rosidl_generator_c")]
extern "C" {
    fn lara_interfaces__srv__GetAppMode_Request__init(msg: *mut GetAppMode_Request) -> bool;
    fn lara_interfaces__srv__GetAppMode_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetAppMode_Request>, size: usize) -> bool;
    fn lara_interfaces__srv__GetAppMode_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetAppMode_Request>);
    fn lara_interfaces__srv__GetAppMode_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetAppMode_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<GetAppMode_Request>) -> bool;
}

// Corresponds to lara_interfaces__srv__GetAppMode_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetAppMode_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetAppMode_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !lara_interfaces__srv__GetAppMode_Request__init(&mut msg as *mut _) {
        panic!("Call to lara_interfaces__srv__GetAppMode_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetAppMode_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { lara_interfaces__srv__GetAppMode_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { lara_interfaces__srv__GetAppMode_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { lara_interfaces__srv__GetAppMode_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetAppMode_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetAppMode_Request where Self: Sized {
  const TYPE_NAME: &'static str = "lara_interfaces/srv/GetAppMode_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__lara_interfaces__srv__GetAppMode_Request() }
  }
}


#[link(name = "lara_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__lara_interfaces__srv__GetAppMode_Response() -> *const std::ffi::c_void;
}

#[link(name = "lara_interfaces__rosidl_generator_c")]
extern "C" {
    fn lara_interfaces__srv__GetAppMode_Response__init(msg: *mut GetAppMode_Response) -> bool;
    fn lara_interfaces__srv__GetAppMode_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetAppMode_Response>, size: usize) -> bool;
    fn lara_interfaces__srv__GetAppMode_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetAppMode_Response>);
    fn lara_interfaces__srv__GetAppMode_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetAppMode_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<GetAppMode_Response>) -> bool;
}

// Corresponds to lara_interfaces__srv__GetAppMode_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetAppMode_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub mode: rosidl_runtime_rs::String,

}



impl Default for GetAppMode_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !lara_interfaces__srv__GetAppMode_Response__init(&mut msg as *mut _) {
        panic!("Call to lara_interfaces__srv__GetAppMode_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetAppMode_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { lara_interfaces__srv__GetAppMode_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { lara_interfaces__srv__GetAppMode_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { lara_interfaces__srv__GetAppMode_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetAppMode_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetAppMode_Response where Self: Sized {
  const TYPE_NAME: &'static str = "lara_interfaces/srv/GetAppMode_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__lara_interfaces__srv__GetAppMode_Response() }
  }
}


#[link(name = "lara_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__lara_interfaces__srv__ComputeIK_Request() -> *const std::ffi::c_void;
}

#[link(name = "lara_interfaces__rosidl_generator_c")]
extern "C" {
    fn lara_interfaces__srv__ComputeIK_Request__init(msg: *mut ComputeIK_Request) -> bool;
    fn lara_interfaces__srv__ComputeIK_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ComputeIK_Request>, size: usize) -> bool;
    fn lara_interfaces__srv__ComputeIK_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ComputeIK_Request>);
    fn lara_interfaces__srv__ComputeIK_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ComputeIK_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<ComputeIK_Request>) -> bool;
}

// Corresponds to lara_interfaces__srv__ComputeIK_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ComputeIK_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub target_pose: geometry_msgs::msg::rmw::Pose,


    // This member is not documented.
    #[allow(missing_docs)]
    pub seed_joint_positions: rosidl_runtime_rs::Sequence<f64>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub timeout_sec: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub position_tolerance: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub orientation_tolerance: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub enforce_joint_limits_mode: i8,

}



impl Default for ComputeIK_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !lara_interfaces__srv__ComputeIK_Request__init(&mut msg as *mut _) {
        panic!("Call to lara_interfaces__srv__ComputeIK_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ComputeIK_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { lara_interfaces__srv__ComputeIK_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { lara_interfaces__srv__ComputeIK_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { lara_interfaces__srv__ComputeIK_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ComputeIK_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ComputeIK_Request where Self: Sized {
  const TYPE_NAME: &'static str = "lara_interfaces/srv/ComputeIK_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__lara_interfaces__srv__ComputeIK_Request() }
  }
}


#[link(name = "lara_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__lara_interfaces__srv__ComputeIK_Response() -> *const std::ffi::c_void;
}

#[link(name = "lara_interfaces__rosidl_generator_c")]
extern "C" {
    fn lara_interfaces__srv__ComputeIK_Response__init(msg: *mut ComputeIK_Response) -> bool;
    fn lara_interfaces__srv__ComputeIK_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ComputeIK_Response>, size: usize) -> bool;
    fn lara_interfaces__srv__ComputeIK_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ComputeIK_Response>);
    fn lara_interfaces__srv__ComputeIK_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ComputeIK_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<ComputeIK_Response>) -> bool;
}

// Corresponds to lara_interfaces__srv__ComputeIK_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ComputeIK_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub joint_names: rosidl_runtime_rs::Sequence<rosidl_runtime_rs::String>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub joint_positions: rosidl_runtime_rs::Sequence<f64>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub position_error: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub orientation_error: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub iterations: i32,

}



impl Default for ComputeIK_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !lara_interfaces__srv__ComputeIK_Response__init(&mut msg as *mut _) {
        panic!("Call to lara_interfaces__srv__ComputeIK_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ComputeIK_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { lara_interfaces__srv__ComputeIK_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { lara_interfaces__srv__ComputeIK_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { lara_interfaces__srv__ComputeIK_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ComputeIK_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ComputeIK_Response where Self: Sized {
  const TYPE_NAME: &'static str = "lara_interfaces/srv/ComputeIK_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__lara_interfaces__srv__ComputeIK_Response() }
  }
}






#[link(name = "lara_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__lara_interfaces__srv__GetTCPPose() -> *const std::ffi::c_void;
}

// Corresponds to lara_interfaces__srv__GetTCPPose
#[allow(missing_docs, non_camel_case_types)]
pub struct GetTCPPose;

impl rosidl_runtime_rs::Service for GetTCPPose {
    type Request = GetTCPPose_Request;
    type Response = GetTCPPose_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__lara_interfaces__srv__GetTCPPose() }
    }
}




#[link(name = "lara_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__lara_interfaces__srv__MoveJoints() -> *const std::ffi::c_void;
}

// Corresponds to lara_interfaces__srv__MoveJoints
#[allow(missing_docs, non_camel_case_types)]
pub struct MoveJoints;

impl rosidl_runtime_rs::Service for MoveJoints {
    type Request = MoveJoints_Request;
    type Response = MoveJoints_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__lara_interfaces__srv__MoveJoints() }
    }
}




#[link(name = "lara_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__lara_interfaces__srv__MoveLinear() -> *const std::ffi::c_void;
}

// Corresponds to lara_interfaces__srv__MoveLinear
#[allow(missing_docs, non_camel_case_types)]
pub struct MoveLinear;

impl rosidl_runtime_rs::Service for MoveLinear {
    type Request = MoveLinear_Request;
    type Response = MoveLinear_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__lara_interfaces__srv__MoveLinear() }
    }
}




#[link(name = "lara_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__lara_interfaces__srv__GetAppMode() -> *const std::ffi::c_void;
}

// Corresponds to lara_interfaces__srv__GetAppMode
#[allow(missing_docs, non_camel_case_types)]
pub struct GetAppMode;

impl rosidl_runtime_rs::Service for GetAppMode {
    type Request = GetAppMode_Request;
    type Response = GetAppMode_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__lara_interfaces__srv__GetAppMode() }
    }
}




#[link(name = "lara_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__lara_interfaces__srv__ComputeIK() -> *const std::ffi::c_void;
}

// Corresponds to lara_interfaces__srv__ComputeIK
#[allow(missing_docs, non_camel_case_types)]
pub struct ComputeIK;

impl rosidl_runtime_rs::Service for ComputeIK {
    type Request = ComputeIK_Request;
    type Response = ComputeIK_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__lara_interfaces__srv__ComputeIK() }
    }
}


