#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};




// Corresponds to lara_interfaces__srv__GetTCPPose_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetTCPPose_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetTCPPose_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetTCPPose_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetTCPPose_Request {
  type RmwMsg = super::srv::rmw::GetTCPPose_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
    }
  }
}


// Corresponds to lara_interfaces__srv__GetTCPPose_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetTCPPose_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub pose: geometry_msgs::msg::Pose,

}



impl Default for GetTCPPose_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetTCPPose_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetTCPPose_Response {
  type RmwMsg = super::srv::rmw::GetTCPPose_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pose: geometry_msgs::msg::Pose::into_rmw_message(std::borrow::Cow::Owned(msg.pose)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pose: geometry_msgs::msg::Pose::into_rmw_message(std::borrow::Cow::Borrowed(&msg.pose)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      pose: geometry_msgs::msg::Pose::from_rmw_message(msg.pose),
    }
  }
}


// Corresponds to lara_interfaces__srv__MoveJoints_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveJoints_Request {
    /// if set, move to teach pendant point by name (e.g. "GP7")
    pub point_name: std::string::String,

    /// degrees, 6*k waypoints (ignored if point_name is set)
    pub target_joint: Vec<f64>,

    /// optional TCP [x,y,z,roll,pitch,yaw] m/rad — IK when target_joint empty
    pub target_pose: Vec<f64>,


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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveJoints_Request::default())
  }
}

impl rosidl_runtime_rs::Message for MoveJoints_Request {
  type RmwMsg = super::srv::rmw::MoveJoints_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        point_name: msg.point_name.as_str().into(),
        target_joint: msg.target_joint.as_slice().into(),
        target_pose: msg.target_pose.as_slice().into(),
        speed: msg.speed,
        acceleration: msg.acceleration,
        enable_safety: msg.enable_safety,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        point_name: msg.point_name.as_str().into(),
        target_joint: msg.target_joint.as_slice().into(),
        target_pose: msg.target_pose.as_slice().into(),
      speed: msg.speed,
      acceleration: msg.acceleration,
      enable_safety: msg.enable_safety,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      point_name: msg.point_name.to_string(),
      target_joint: msg.target_joint.into(),
      target_pose: msg.target_pose.into(),
      speed: msg.speed,
      acceleration: msg.acceleration,
      enable_safety: msg.enable_safety,
    }
  }
}


// Corresponds to lara_interfaces__srv__MoveJoints_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveJoints_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,

}



impl Default for MoveJoints_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveJoints_Response::default())
  }
}

impl rosidl_runtime_rs::Message for MoveJoints_Response {
  type RmwMsg = super::srv::rmw::MoveJoints_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        message: msg.message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        message: msg.message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      message: msg.message.to_string(),
    }
  }
}


// Corresponds to lara_interfaces__srv__MoveLinear_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveLinear_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub target_pose: Vec<f64>,

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
    pub offset_frame: std::string::String,

}



impl Default for MoveLinear_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveLinear_Request::default())
  }
}

impl rosidl_runtime_rs::Message for MoveLinear_Request {
  type RmwMsg = super::srv::rmw::MoveLinear_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        target_pose: msg.target_pose.as_slice().into(),
        speed: msg.speed,
        acceleration: msg.acceleration,
        enable_safety: msg.enable_safety,
        use_relative: msg.use_relative,
        offset_frame: msg.offset_frame.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        target_pose: msg.target_pose.as_slice().into(),
      speed: msg.speed,
      acceleration: msg.acceleration,
      enable_safety: msg.enable_safety,
      use_relative: msg.use_relative,
        offset_frame: msg.offset_frame.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      target_pose: msg.target_pose.into(),
      speed: msg.speed,
      acceleration: msg.acceleration,
      enable_safety: msg.enable_safety,
      use_relative: msg.use_relative,
      offset_frame: msg.offset_frame.to_string(),
    }
  }
}


// Corresponds to lara_interfaces__srv__MoveLinear_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveLinear_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,

}



impl Default for MoveLinear_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveLinear_Response::default())
  }
}

impl rosidl_runtime_rs::Message for MoveLinear_Response {
  type RmwMsg = super::srv::rmw::MoveLinear_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        message: msg.message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        message: msg.message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      message: msg.message.to_string(),
    }
  }
}


// Corresponds to lara_interfaces__srv__GetAppMode_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetAppMode_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetAppMode_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetAppMode_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetAppMode_Request {
  type RmwMsg = super::srv::rmw::GetAppMode_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
    }
  }
}


// Corresponds to lara_interfaces__srv__GetAppMode_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetAppMode_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub mode: std::string::String,

}



impl Default for GetAppMode_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetAppMode_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetAppMode_Response {
  type RmwMsg = super::srv::rmw::GetAppMode_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        mode: msg.mode.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        mode: msg.mode.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      mode: msg.mode.to_string(),
    }
  }
}


// Corresponds to lara_interfaces__srv__ComputeIK_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ComputeIK_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub target_pose: geometry_msgs::msg::Pose,


    // This member is not documented.
    #[allow(missing_docs)]
    pub seed_joint_positions: Vec<f64>,


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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ComputeIK_Request::default())
  }
}

impl rosidl_runtime_rs::Message for ComputeIK_Request {
  type RmwMsg = super::srv::rmw::ComputeIK_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        target_pose: geometry_msgs::msg::Pose::into_rmw_message(std::borrow::Cow::Owned(msg.target_pose)).into_owned(),
        seed_joint_positions: msg.seed_joint_positions.as_slice().into(),
        timeout_sec: msg.timeout_sec,
        position_tolerance: msg.position_tolerance,
        orientation_tolerance: msg.orientation_tolerance,
        enforce_joint_limits_mode: msg.enforce_joint_limits_mode,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        target_pose: geometry_msgs::msg::Pose::into_rmw_message(std::borrow::Cow::Borrowed(&msg.target_pose)).into_owned(),
        seed_joint_positions: msg.seed_joint_positions.as_slice().into(),
      timeout_sec: msg.timeout_sec,
      position_tolerance: msg.position_tolerance,
      orientation_tolerance: msg.orientation_tolerance,
      enforce_joint_limits_mode: msg.enforce_joint_limits_mode,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      target_pose: geometry_msgs::msg::Pose::from_rmw_message(msg.target_pose),
      seed_joint_positions: msg.seed_joint_positions.into(),
      timeout_sec: msg.timeout_sec,
      position_tolerance: msg.position_tolerance,
      orientation_tolerance: msg.orientation_tolerance,
      enforce_joint_limits_mode: msg.enforce_joint_limits_mode,
    }
  }
}


// Corresponds to lara_interfaces__srv__ComputeIK_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ComputeIK_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub joint_names: Vec<std::string::String>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub joint_positions: Vec<f64>,


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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ComputeIK_Response::default())
  }
}

impl rosidl_runtime_rs::Message for ComputeIK_Response {
  type RmwMsg = super::srv::rmw::ComputeIK_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        message: msg.message.as_str().into(),
        joint_names: msg.joint_names
          .into_iter()
          .map(|elem| elem.as_str().into())
          .collect(),
        joint_positions: msg.joint_positions.as_slice().into(),
        position_error: msg.position_error,
        orientation_error: msg.orientation_error,
        iterations: msg.iterations,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        message: msg.message.as_str().into(),
        joint_names: msg.joint_names
          .iter()
          .map(|elem| elem.as_str().into())
          .collect(),
        joint_positions: msg.joint_positions.as_slice().into(),
      position_error: msg.position_error,
      orientation_error: msg.orientation_error,
      iterations: msg.iterations,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      message: msg.message.to_string(),
      joint_names: msg.joint_names
          .into_iter()
          .map(|elem| elem.to_string())
          .collect(),
      joint_positions: msg.joint_positions.into(),
      position_error: msg.position_error,
      orientation_error: msg.orientation_error,
      iterations: msg.iterations,
    }
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


