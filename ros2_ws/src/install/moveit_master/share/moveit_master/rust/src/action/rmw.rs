
#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "moveit_master__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__moveit_master__action__ExecuteSequence_Goal() -> *const std::ffi::c_void;
}

#[link(name = "moveit_master__rosidl_generator_c")]
extern "C" {
    fn moveit_master__action__ExecuteSequence_Goal__init(msg: *mut ExecuteSequence_Goal) -> bool;
    fn moveit_master__action__ExecuteSequence_Goal__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ExecuteSequence_Goal>, size: usize) -> bool;
    fn moveit_master__action__ExecuteSequence_Goal__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ExecuteSequence_Goal>);
    fn moveit_master__action__ExecuteSequence_Goal__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ExecuteSequence_Goal>, out_seq: *mut rosidl_runtime_rs::Sequence<ExecuteSequence_Goal>) -> bool;
}

// Corresponds to moveit_master__action__ExecuteSequence_Goal
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecuteSequence_Goal {

    // This member is not documented.
    #[allow(missing_docs)]
    pub steps: rosidl_runtime_rs::Sequence<super::super::msg::rmw::MotionStep>,

    /// 0 = default (0.2)
    pub velocity_scaling: f64,

}



impl Default for ExecuteSequence_Goal {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !moveit_master__action__ExecuteSequence_Goal__init(&mut msg as *mut _) {
        panic!("Call to moveit_master__action__ExecuteSequence_Goal__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ExecuteSequence_Goal {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { moveit_master__action__ExecuteSequence_Goal__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { moveit_master__action__ExecuteSequence_Goal__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { moveit_master__action__ExecuteSequence_Goal__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ExecuteSequence_Goal {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ExecuteSequence_Goal where Self: Sized {
  const TYPE_NAME: &'static str = "moveit_master/action/ExecuteSequence_Goal";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__moveit_master__action__ExecuteSequence_Goal() }
  }
}


#[link(name = "moveit_master__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__moveit_master__action__ExecuteSequence_Result() -> *const std::ffi::c_void;
}

#[link(name = "moveit_master__rosidl_generator_c")]
extern "C" {
    fn moveit_master__action__ExecuteSequence_Result__init(msg: *mut ExecuteSequence_Result) -> bool;
    fn moveit_master__action__ExecuteSequence_Result__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ExecuteSequence_Result>, size: usize) -> bool;
    fn moveit_master__action__ExecuteSequence_Result__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ExecuteSequence_Result>);
    fn moveit_master__action__ExecuteSequence_Result__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ExecuteSequence_Result>, out_seq: *mut rosidl_runtime_rs::Sequence<ExecuteSequence_Result>) -> bool;
}

// Corresponds to moveit_master__action__ExecuteSequence_Result
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecuteSequence_Result {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

    /// index of the failing step (valid only if success == false)
    pub failed_step: u32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,

}



impl Default for ExecuteSequence_Result {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !moveit_master__action__ExecuteSequence_Result__init(&mut msg as *mut _) {
        panic!("Call to moveit_master__action__ExecuteSequence_Result__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ExecuteSequence_Result {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { moveit_master__action__ExecuteSequence_Result__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { moveit_master__action__ExecuteSequence_Result__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { moveit_master__action__ExecuteSequence_Result__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ExecuteSequence_Result {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ExecuteSequence_Result where Self: Sized {
  const TYPE_NAME: &'static str = "moveit_master/action/ExecuteSequence_Result";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__moveit_master__action__ExecuteSequence_Result() }
  }
}


#[link(name = "moveit_master__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__moveit_master__action__ExecuteSequence_Feedback() -> *const std::ffi::c_void;
}

#[link(name = "moveit_master__rosidl_generator_c")]
extern "C" {
    fn moveit_master__action__ExecuteSequence_Feedback__init(msg: *mut ExecuteSequence_Feedback) -> bool;
    fn moveit_master__action__ExecuteSequence_Feedback__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ExecuteSequence_Feedback>, size: usize) -> bool;
    fn moveit_master__action__ExecuteSequence_Feedback__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ExecuteSequence_Feedback>);
    fn moveit_master__action__ExecuteSequence_Feedback__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ExecuteSequence_Feedback>, out_seq: *mut rosidl_runtime_rs::Sequence<ExecuteSequence_Feedback>) -> bool;
}

// Corresponds to moveit_master__action__ExecuteSequence_Feedback
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecuteSequence_Feedback {

    // This member is not documented.
    #[allow(missing_docs)]
    pub current_step: u32,

}



impl Default for ExecuteSequence_Feedback {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !moveit_master__action__ExecuteSequence_Feedback__init(&mut msg as *mut _) {
        panic!("Call to moveit_master__action__ExecuteSequence_Feedback__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ExecuteSequence_Feedback {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { moveit_master__action__ExecuteSequence_Feedback__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { moveit_master__action__ExecuteSequence_Feedback__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { moveit_master__action__ExecuteSequence_Feedback__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ExecuteSequence_Feedback {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ExecuteSequence_Feedback where Self: Sized {
  const TYPE_NAME: &'static str = "moveit_master/action/ExecuteSequence_Feedback";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__moveit_master__action__ExecuteSequence_Feedback() }
  }
}


#[link(name = "moveit_master__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__moveit_master__action__ExecuteSequence_FeedbackMessage() -> *const std::ffi::c_void;
}

#[link(name = "moveit_master__rosidl_generator_c")]
extern "C" {
    fn moveit_master__action__ExecuteSequence_FeedbackMessage__init(msg: *mut ExecuteSequence_FeedbackMessage) -> bool;
    fn moveit_master__action__ExecuteSequence_FeedbackMessage__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ExecuteSequence_FeedbackMessage>, size: usize) -> bool;
    fn moveit_master__action__ExecuteSequence_FeedbackMessage__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ExecuteSequence_FeedbackMessage>);
    fn moveit_master__action__ExecuteSequence_FeedbackMessage__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ExecuteSequence_FeedbackMessage>, out_seq: *mut rosidl_runtime_rs::Sequence<ExecuteSequence_FeedbackMessage>) -> bool;
}

// Corresponds to moveit_master__action__ExecuteSequence_FeedbackMessage
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecuteSequence_FeedbackMessage {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub feedback: super::super::action::rmw::ExecuteSequence_Feedback,

}



impl Default for ExecuteSequence_FeedbackMessage {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !moveit_master__action__ExecuteSequence_FeedbackMessage__init(&mut msg as *mut _) {
        panic!("Call to moveit_master__action__ExecuteSequence_FeedbackMessage__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ExecuteSequence_FeedbackMessage {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { moveit_master__action__ExecuteSequence_FeedbackMessage__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { moveit_master__action__ExecuteSequence_FeedbackMessage__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { moveit_master__action__ExecuteSequence_FeedbackMessage__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ExecuteSequence_FeedbackMessage {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ExecuteSequence_FeedbackMessage where Self: Sized {
  const TYPE_NAME: &'static str = "moveit_master/action/ExecuteSequence_FeedbackMessage";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__moveit_master__action__ExecuteSequence_FeedbackMessage() }
  }
}




#[link(name = "moveit_master__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__moveit_master__action__ExecuteSequence_SendGoal_Request() -> *const std::ffi::c_void;
}

#[link(name = "moveit_master__rosidl_generator_c")]
extern "C" {
    fn moveit_master__action__ExecuteSequence_SendGoal_Request__init(msg: *mut ExecuteSequence_SendGoal_Request) -> bool;
    fn moveit_master__action__ExecuteSequence_SendGoal_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ExecuteSequence_SendGoal_Request>, size: usize) -> bool;
    fn moveit_master__action__ExecuteSequence_SendGoal_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ExecuteSequence_SendGoal_Request>);
    fn moveit_master__action__ExecuteSequence_SendGoal_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ExecuteSequence_SendGoal_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<ExecuteSequence_SendGoal_Request>) -> bool;
}

// Corresponds to moveit_master__action__ExecuteSequence_SendGoal_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecuteSequence_SendGoal_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub goal: super::super::action::rmw::ExecuteSequence_Goal,

}



impl Default for ExecuteSequence_SendGoal_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !moveit_master__action__ExecuteSequence_SendGoal_Request__init(&mut msg as *mut _) {
        panic!("Call to moveit_master__action__ExecuteSequence_SendGoal_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ExecuteSequence_SendGoal_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { moveit_master__action__ExecuteSequence_SendGoal_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { moveit_master__action__ExecuteSequence_SendGoal_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { moveit_master__action__ExecuteSequence_SendGoal_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ExecuteSequence_SendGoal_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ExecuteSequence_SendGoal_Request where Self: Sized {
  const TYPE_NAME: &'static str = "moveit_master/action/ExecuteSequence_SendGoal_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__moveit_master__action__ExecuteSequence_SendGoal_Request() }
  }
}


#[link(name = "moveit_master__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__moveit_master__action__ExecuteSequence_SendGoal_Response() -> *const std::ffi::c_void;
}

#[link(name = "moveit_master__rosidl_generator_c")]
extern "C" {
    fn moveit_master__action__ExecuteSequence_SendGoal_Response__init(msg: *mut ExecuteSequence_SendGoal_Response) -> bool;
    fn moveit_master__action__ExecuteSequence_SendGoal_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ExecuteSequence_SendGoal_Response>, size: usize) -> bool;
    fn moveit_master__action__ExecuteSequence_SendGoal_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ExecuteSequence_SendGoal_Response>);
    fn moveit_master__action__ExecuteSequence_SendGoal_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ExecuteSequence_SendGoal_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<ExecuteSequence_SendGoal_Response>) -> bool;
}

// Corresponds to moveit_master__action__ExecuteSequence_SendGoal_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecuteSequence_SendGoal_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub accepted: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::rmw::Time,

}



impl Default for ExecuteSequence_SendGoal_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !moveit_master__action__ExecuteSequence_SendGoal_Response__init(&mut msg as *mut _) {
        panic!("Call to moveit_master__action__ExecuteSequence_SendGoal_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ExecuteSequence_SendGoal_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { moveit_master__action__ExecuteSequence_SendGoal_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { moveit_master__action__ExecuteSequence_SendGoal_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { moveit_master__action__ExecuteSequence_SendGoal_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ExecuteSequence_SendGoal_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ExecuteSequence_SendGoal_Response where Self: Sized {
  const TYPE_NAME: &'static str = "moveit_master/action/ExecuteSequence_SendGoal_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__moveit_master__action__ExecuteSequence_SendGoal_Response() }
  }
}


#[link(name = "moveit_master__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__moveit_master__action__ExecuteSequence_GetResult_Request() -> *const std::ffi::c_void;
}

#[link(name = "moveit_master__rosidl_generator_c")]
extern "C" {
    fn moveit_master__action__ExecuteSequence_GetResult_Request__init(msg: *mut ExecuteSequence_GetResult_Request) -> bool;
    fn moveit_master__action__ExecuteSequence_GetResult_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ExecuteSequence_GetResult_Request>, size: usize) -> bool;
    fn moveit_master__action__ExecuteSequence_GetResult_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ExecuteSequence_GetResult_Request>);
    fn moveit_master__action__ExecuteSequence_GetResult_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ExecuteSequence_GetResult_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<ExecuteSequence_GetResult_Request>) -> bool;
}

// Corresponds to moveit_master__action__ExecuteSequence_GetResult_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecuteSequence_GetResult_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,

}



impl Default for ExecuteSequence_GetResult_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !moveit_master__action__ExecuteSequence_GetResult_Request__init(&mut msg as *mut _) {
        panic!("Call to moveit_master__action__ExecuteSequence_GetResult_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ExecuteSequence_GetResult_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { moveit_master__action__ExecuteSequence_GetResult_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { moveit_master__action__ExecuteSequence_GetResult_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { moveit_master__action__ExecuteSequence_GetResult_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ExecuteSequence_GetResult_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ExecuteSequence_GetResult_Request where Self: Sized {
  const TYPE_NAME: &'static str = "moveit_master/action/ExecuteSequence_GetResult_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__moveit_master__action__ExecuteSequence_GetResult_Request() }
  }
}


#[link(name = "moveit_master__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__moveit_master__action__ExecuteSequence_GetResult_Response() -> *const std::ffi::c_void;
}

#[link(name = "moveit_master__rosidl_generator_c")]
extern "C" {
    fn moveit_master__action__ExecuteSequence_GetResult_Response__init(msg: *mut ExecuteSequence_GetResult_Response) -> bool;
    fn moveit_master__action__ExecuteSequence_GetResult_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ExecuteSequence_GetResult_Response>, size: usize) -> bool;
    fn moveit_master__action__ExecuteSequence_GetResult_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ExecuteSequence_GetResult_Response>);
    fn moveit_master__action__ExecuteSequence_GetResult_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ExecuteSequence_GetResult_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<ExecuteSequence_GetResult_Response>) -> bool;
}

// Corresponds to moveit_master__action__ExecuteSequence_GetResult_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecuteSequence_GetResult_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub status: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub result: super::super::action::rmw::ExecuteSequence_Result,

}



impl Default for ExecuteSequence_GetResult_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !moveit_master__action__ExecuteSequence_GetResult_Response__init(&mut msg as *mut _) {
        panic!("Call to moveit_master__action__ExecuteSequence_GetResult_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ExecuteSequence_GetResult_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { moveit_master__action__ExecuteSequence_GetResult_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { moveit_master__action__ExecuteSequence_GetResult_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { moveit_master__action__ExecuteSequence_GetResult_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ExecuteSequence_GetResult_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ExecuteSequence_GetResult_Response where Self: Sized {
  const TYPE_NAME: &'static str = "moveit_master/action/ExecuteSequence_GetResult_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__moveit_master__action__ExecuteSequence_GetResult_Response() }
  }
}






#[link(name = "moveit_master__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__moveit_master__action__ExecuteSequence_SendGoal() -> *const std::ffi::c_void;
}

// Corresponds to moveit_master__action__ExecuteSequence_SendGoal
#[allow(missing_docs, non_camel_case_types)]
pub struct ExecuteSequence_SendGoal;

impl rosidl_runtime_rs::Service for ExecuteSequence_SendGoal {
    type Request = ExecuteSequence_SendGoal_Request;
    type Response = ExecuteSequence_SendGoal_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__moveit_master__action__ExecuteSequence_SendGoal() }
    }
}




#[link(name = "moveit_master__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__moveit_master__action__ExecuteSequence_GetResult() -> *const std::ffi::c_void;
}

// Corresponds to moveit_master__action__ExecuteSequence_GetResult
#[allow(missing_docs, non_camel_case_types)]
pub struct ExecuteSequence_GetResult;

impl rosidl_runtime_rs::Service for ExecuteSequence_GetResult {
    type Request = ExecuteSequence_GetResult_Request;
    type Response = ExecuteSequence_GetResult_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__moveit_master__action__ExecuteSequence_GetResult() }
    }
}


