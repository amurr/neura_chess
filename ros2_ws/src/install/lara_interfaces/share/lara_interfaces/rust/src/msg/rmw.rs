#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "lara_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__lara_interfaces__msg__XyzRpyGoal() -> *const std::ffi::c_void;
}

#[link(name = "lara_interfaces__rosidl_generator_c")]
extern "C" {
    fn lara_interfaces__msg__XyzRpyGoal__init(msg: *mut XyzRpyGoal) -> bool;
    fn lara_interfaces__msg__XyzRpyGoal__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<XyzRpyGoal>, size: usize) -> bool;
    fn lara_interfaces__msg__XyzRpyGoal__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<XyzRpyGoal>);
    fn lara_interfaces__msg__XyzRpyGoal__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<XyzRpyGoal>, out_seq: *mut rosidl_runtime_rs::Sequence<XyzRpyGoal>) -> bool;
}

// Corresponds to lara_interfaces__msg__XyzRpyGoal
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// TCP target (robot base frame, metres, radians).

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct XyzRpyGoal {

    // This member is not documented.
    #[allow(missing_docs)]
    pub x: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub y: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub z: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub roll: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub pitch: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub yaw: f64,

    /// If false, executor uses view_rpy parameter instead of roll/pitch/yaw.
    pub use_orientation: bool,

}



impl Default for XyzRpyGoal {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !lara_interfaces__msg__XyzRpyGoal__init(&mut msg as *mut _) {
        panic!("Call to lara_interfaces__msg__XyzRpyGoal__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for XyzRpyGoal {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { lara_interfaces__msg__XyzRpyGoal__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { lara_interfaces__msg__XyzRpyGoal__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { lara_interfaces__msg__XyzRpyGoal__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for XyzRpyGoal {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for XyzRpyGoal where Self: Sized {
  const TYPE_NAME: &'static str = "lara_interfaces/msg/XyzRpyGoal";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__lara_interfaces__msg__XyzRpyGoal() }
  }
}


