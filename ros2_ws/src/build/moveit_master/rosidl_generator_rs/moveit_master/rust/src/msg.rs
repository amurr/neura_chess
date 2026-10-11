#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to moveit_master__msg__MotionStep
/// One step of a motion sequence executed by moveit_master.

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MotionStep {

    // This member is not documented.
    #[allow(missing_docs)]
    pub type_: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub pose: geometry_msgs::msg::Pose,


    // This member is not documented.
    #[allow(missing_docs)]
    pub named_target: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub duration: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub joint_value: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub offset: geometry_msgs::msg::Vector3,


    // This member is not documented.
    #[allow(missing_docs)]
    pub object_id: std::string::String,

    /// ALLOW_COLLISION: extra links / objects, e.g. the board square under the piece
    pub touch_links: Vec<std::string::String>,


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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::MotionStep::default())
  }
}

impl rosidl_runtime_rs::Message for MotionStep {
  type RmwMsg = super::msg::rmw::MotionStep;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        type_: msg.type_,
        pose: geometry_msgs::msg::Pose::into_rmw_message(std::borrow::Cow::Owned(msg.pose)).into_owned(),
        named_target: msg.named_target.as_str().into(),
        duration: msg.duration,
        joint_value: msg.joint_value,
        offset: geometry_msgs::msg::Vector3::into_rmw_message(std::borrow::Cow::Owned(msg.offset)).into_owned(),
        object_id: msg.object_id.as_str().into(),
        touch_links: msg.touch_links
          .into_iter()
          .map(|elem| elem.as_str().into())
          .collect(),
        allow: msg.allow,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      type_: msg.type_,
        pose: geometry_msgs::msg::Pose::into_rmw_message(std::borrow::Cow::Borrowed(&msg.pose)).into_owned(),
        named_target: msg.named_target.as_str().into(),
      duration: msg.duration,
      joint_value: msg.joint_value,
        offset: geometry_msgs::msg::Vector3::into_rmw_message(std::borrow::Cow::Borrowed(&msg.offset)).into_owned(),
        object_id: msg.object_id.as_str().into(),
        touch_links: msg.touch_links
          .iter()
          .map(|elem| elem.as_str().into())
          .collect(),
      allow: msg.allow,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      type_: msg.type_,
      pose: geometry_msgs::msg::Pose::from_rmw_message(msg.pose),
      named_target: msg.named_target.to_string(),
      duration: msg.duration,
      joint_value: msg.joint_value,
      offset: geometry_msgs::msg::Vector3::from_rmw_message(msg.offset),
      object_id: msg.object_id.to_string(),
      touch_links: msg.touch_links
          .into_iter()
          .map(|elem| elem.to_string())
          .collect(),
      allow: msg.allow,
    }
  }
}


