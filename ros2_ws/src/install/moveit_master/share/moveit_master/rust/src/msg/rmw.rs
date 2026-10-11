#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "moveit_master__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__moveit_master__msg__MotionStep() -> *const std::ffi::c_void;
}

#[link(name = "moveit_master__rosidl_generator_c")]
extern "C" {
    fn moveit_master__msg__MotionStep__init(msg: *mut MotionStep) -> bool;
    fn moveit_master__msg__MotionStep__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MotionStep>, size: usize) -> bool;
    fn moveit_master__msg__MotionStep__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MotionStep>);
    fn moveit_master__msg__MotionStep__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MotionStep>, out_seq: *mut rosidl_runtime_rs::Sequence<MotionStep>) -> bool;
}

// Corresponds to moveit_master__msg__MotionStep
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// One step of a motion sequence executed by moveit_master.

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MotionStep {

    // This member is not documented.
    #[allow(missing_docs)]
    pub type_: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub pose: geometry_msgs::msg::rmw::Pose,


    // This member is not documented.
    #[allow(missing_docs)]
    pub named_target: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub duration: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub joint_value: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub offset: geometry_msgs::msg::rmw::Vector3,


    // This member is not documented.
    #[allow(missing_docs)]
    pub object_id: rosidl_runtime_rs::String,

    /// ALLOW_COLLISION: extra links / objects, e.g. the board square under the piece
    pub touch_links: rosidl_runtime_rs::Sequence<rosidl_runtime_rs::String>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub allow: bool,

}

impl MotionStep {
    /// move arm EEF to `pose` (in the arm's pose reference frame, e.g. world)
    pub const ARM_POSE: u8 = 0;

    /// move arm to SRDF named state `named_target` (e.g. "home", "e2_hover")
    pub const ARM_NAMED: u8 = 1;

    /// move gripper to SRDF named state `named_target` (e.g. "open")
    pub const GRIPPER_NAMED: u8 = 2;

    /// pause for `duration` seconds
    pub const WAIT: u8 = 3;

    /// move gripper joint to `joint_value` (rad)
    pub const GRIPPER_JOINT: u8 = 4;

    /// straight-line EEF move by `offset` (planning frame, m), e.g. z=-0.06 = straight down
    pub const ARM_CARTESIAN: u8 = 5;

    /// attach world object `object_id` to the EEF link; gripper links may touch it
    pub const ATTACH: u8 = 6;

    /// detach `object_id`; it stays in the world where it was released
    pub const DETACH: u8 = 7;

    /// allow=true: `object_id` may touch gripper links + `touch_links`; false: undo
    pub const ALLOW_COLLISION: u8 = 8;

}


impl Default for MotionStep {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !moveit_master__msg__MotionStep__init(&mut msg as *mut _) {
        panic!("Call to moveit_master__msg__MotionStep__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MotionStep {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { moveit_master__msg__MotionStep__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { moveit_master__msg__MotionStep__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { moveit_master__msg__MotionStep__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MotionStep {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MotionStep where Self: Sized {
  const TYPE_NAME: &'static str = "moveit_master/msg/MotionStep";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__moveit_master__msg__MotionStep() }
  }
}


