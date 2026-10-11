
#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to chess_interfaces__action__ChessBoard_Goal

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ChessBoard_Goal {
    /// Goal
    /// ACTIVE / PASSIVE
    pub change_status: std::string::String,

    /// pawn / rook / knight / bishop / queen / king (the piece on to_pick)
    pub piece_type: std::string::String,

    /// square, e.g. "e2"
    pub to_pick: std::string::String,

    /// square, e.g. "e4"
    pub to_place: std::string::String,

    /// board AFTER the move (FEN, piece-placement field is enough).
    /// Optional, but required for castling, en passant and promotion;
    /// an ACTIVE goal with only `fen` re-syncs the whole board.
    pub fen: std::string::String,

}

impl ChessBoard_Goal {
    /// change_status values
    /// the move already happened on the real board -> only update the PlanningScene
    pub const ACTIVE: &'static str = "active";

    /// the robot must execute the move -> pick and place with MoveItMaster
    pub const PASSIVE: &'static str = "passive";

}


impl Default for ChessBoard_Goal {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::ChessBoard_Goal::default())
  }
}

impl rosidl_runtime_rs::Message for ChessBoard_Goal {
  type RmwMsg = super::action::rmw::ChessBoard_Goal;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        change_status: msg.change_status.as_str().into(),
        piece_type: msg.piece_type.as_str().into(),
        to_pick: msg.to_pick.as_str().into(),
        to_place: msg.to_place.as_str().into(),
        fen: msg.fen.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        change_status: msg.change_status.as_str().into(),
        piece_type: msg.piece_type.as_str().into(),
        to_pick: msg.to_pick.as_str().into(),
        to_place: msg.to_place.as_str().into(),
        fen: msg.fen.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      change_status: msg.change_status.to_string(),
      piece_type: msg.piece_type.to_string(),
      to_pick: msg.to_pick.to_string(),
      to_place: msg.to_place.to_string(),
      fen: msg.fen.to_string(),
    }
  }
}


// Corresponds to chess_interfaces__action__ChessBoard_Result

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ChessBoard_Result {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,

    /// board as the server (and the PlanningScene) now holds it
    pub fen: std::string::String,

}



impl Default for ChessBoard_Result {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::ChessBoard_Result::default())
  }
}

impl rosidl_runtime_rs::Message for ChessBoard_Result {
  type RmwMsg = super::action::rmw::ChessBoard_Result;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        message: msg.message.as_str().into(),
        fen: msg.fen.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        message: msg.message.as_str().into(),
        fen: msg.fen.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      message: msg.message.to_string(),
      fen: msg.fen.to_string(),
    }
  }
}


// Corresponds to chess_interfaces__action__ChessBoard_Feedback

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ChessBoard_Feedback {
    /// e.g. "capture d5 -> discard", "move e2 -> e4", "planning scene sync"
    pub stage: std::string::String,

}



impl Default for ChessBoard_Feedback {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::ChessBoard_Feedback::default())
  }
}

impl rosidl_runtime_rs::Message for ChessBoard_Feedback {
  type RmwMsg = super::action::rmw::ChessBoard_Feedback;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        stage: msg.stage.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        stage: msg.stage.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      stage: msg.stage.to_string(),
    }
  }
}


// Corresponds to chess_interfaces__action__ChessBoard_FeedbackMessage

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ChessBoard_FeedbackMessage {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub feedback: super::action::ChessBoard_Feedback,

}



impl Default for ChessBoard_FeedbackMessage {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::ChessBoard_FeedbackMessage::default())
  }
}

impl rosidl_runtime_rs::Message for ChessBoard_FeedbackMessage {
  type RmwMsg = super::action::rmw::ChessBoard_FeedbackMessage;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_id)).into_owned(),
        feedback: super::action::ChessBoard_Feedback::into_rmw_message(std::borrow::Cow::Owned(msg.feedback)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_id)).into_owned(),
        feedback: super::action::ChessBoard_Feedback::into_rmw_message(std::borrow::Cow::Borrowed(&msg.feedback)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      goal_id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_id),
      feedback: super::action::ChessBoard_Feedback::from_rmw_message(msg.feedback),
    }
  }
}






// Corresponds to chess_interfaces__action__ChessBoard_SendGoal_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ChessBoard_SendGoal_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub goal: super::action::ChessBoard_Goal,

}



impl Default for ChessBoard_SendGoal_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::ChessBoard_SendGoal_Request::default())
  }
}

impl rosidl_runtime_rs::Message for ChessBoard_SendGoal_Request {
  type RmwMsg = super::action::rmw::ChessBoard_SendGoal_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_id)).into_owned(),
        goal: super::action::ChessBoard_Goal::into_rmw_message(std::borrow::Cow::Owned(msg.goal)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_id)).into_owned(),
        goal: super::action::ChessBoard_Goal::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      goal_id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_id),
      goal: super::action::ChessBoard_Goal::from_rmw_message(msg.goal),
    }
  }
}


// Corresponds to chess_interfaces__action__ChessBoard_SendGoal_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ChessBoard_SendGoal_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub accepted: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::Time,

}



impl Default for ChessBoard_SendGoal_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::ChessBoard_SendGoal_Response::default())
  }
}

impl rosidl_runtime_rs::Message for ChessBoard_SendGoal_Response {
  type RmwMsg = super::action::rmw::ChessBoard_SendGoal_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        accepted: msg.accepted,
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.stamp)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      accepted: msg.accepted,
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.stamp)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      accepted: msg.accepted,
      stamp: builtin_interfaces::msg::Time::from_rmw_message(msg.stamp),
    }
  }
}


// Corresponds to chess_interfaces__action__ChessBoard_GetResult_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ChessBoard_GetResult_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::UUID,

}



impl Default for ChessBoard_GetResult_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::ChessBoard_GetResult_Request::default())
  }
}

impl rosidl_runtime_rs::Message for ChessBoard_GetResult_Request {
  type RmwMsg = super::action::rmw::ChessBoard_GetResult_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_id)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_id)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      goal_id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_id),
    }
  }
}


// Corresponds to chess_interfaces__action__ChessBoard_GetResult_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ChessBoard_GetResult_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub status: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub result: super::action::ChessBoard_Result,

}



impl Default for ChessBoard_GetResult_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::ChessBoard_GetResult_Response::default())
  }
}

impl rosidl_runtime_rs::Message for ChessBoard_GetResult_Response {
  type RmwMsg = super::action::rmw::ChessBoard_GetResult_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        status: msg.status,
        result: super::action::ChessBoard_Result::into_rmw_message(std::borrow::Cow::Owned(msg.result)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      status: msg.status,
        result: super::action::ChessBoard_Result::into_rmw_message(std::borrow::Cow::Borrowed(&msg.result)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      status: msg.status,
      result: super::action::ChessBoard_Result::from_rmw_message(msg.result),
    }
  }
}






#[link(name = "chess_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__chess_interfaces__action__ChessBoard_SendGoal() -> *const std::ffi::c_void;
}

// Corresponds to chess_interfaces__action__ChessBoard_SendGoal
#[allow(missing_docs, non_camel_case_types)]
pub struct ChessBoard_SendGoal;

impl rosidl_runtime_rs::Service for ChessBoard_SendGoal {
    type Request = ChessBoard_SendGoal_Request;
    type Response = ChessBoard_SendGoal_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__chess_interfaces__action__ChessBoard_SendGoal() }
    }
}




#[link(name = "chess_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__chess_interfaces__action__ChessBoard_GetResult() -> *const std::ffi::c_void;
}

// Corresponds to chess_interfaces__action__ChessBoard_GetResult
#[allow(missing_docs, non_camel_case_types)]
pub struct ChessBoard_GetResult;

impl rosidl_runtime_rs::Service for ChessBoard_GetResult {
    type Request = ChessBoard_GetResult_Request;
    type Response = ChessBoard_GetResult_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__chess_interfaces__action__ChessBoard_GetResult() }
    }
}






#[link(name = "chess_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_action_type_support_handle__chess_interfaces__action__ChessBoard() -> *const std::ffi::c_void;
}

// Corresponds to chess_interfaces__action__ChessBoard
#[allow(missing_docs, non_camel_case_types)]
pub struct ChessBoard;

impl rosidl_runtime_rs::Action for ChessBoard {
  // --- Associated types for client library users ---
  /// The goal message defined in the action definition.
  type Goal = ChessBoard_Goal;

  /// The result message defined in the action definition.
  type Result = ChessBoard_Result;

  /// The feedback message defined in the action definition.
  type Feedback = ChessBoard_Feedback;

  // --- Associated types for client library implementation ---
  /// The feedback message with generic fields which wraps the feedback message.
  type FeedbackMessage = super::action::ChessBoard_FeedbackMessage;

  /// The send_goal service using a wrapped version of the goal message as a request.
  type SendGoalService = super::action::ChessBoard_SendGoal;

  /// The generic service to cancel a goal.
  type CancelGoalService = action_msgs::srv::rmw::CancelGoal;

  /// The get_result service using a wrapped version of the result message as a response.
  type GetResultService = super::action::ChessBoard_GetResult;

  // --- Methods for client library implementation ---
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_action_type_support_handle__chess_interfaces__action__ChessBoard() }
  }

  fn create_goal_request(
    goal_id: &[u8; 16],
    goal: super::action::rmw::ChessBoard_Goal,
  ) -> super::action::rmw::ChessBoard_SendGoal_Request {
   super::action::rmw::ChessBoard_SendGoal_Request {
      goal_id: unique_identifier_msgs::msg::rmw::UUID { uuid: *goal_id },
      goal,
    }
  }

  fn split_goal_request(
    request: super::action::rmw::ChessBoard_SendGoal_Request,
  ) -> (
    [u8; 16],
   super::action::rmw::ChessBoard_Goal,
  ) {
    (request.goal_id.uuid, request.goal)
  }

  fn create_goal_response(
    accepted: bool,
    stamp: (i32, u32),
  ) -> super::action::rmw::ChessBoard_SendGoal_Response {
   super::action::rmw::ChessBoard_SendGoal_Response {
      accepted,
      stamp: builtin_interfaces::msg::rmw::Time {
        sec: stamp.0,
        nanosec: stamp.1,
      },
    }
  }

  fn get_goal_response_accepted(
    response: &super::action::rmw::ChessBoard_SendGoal_Response,
  ) -> bool {
    response.accepted
  }

  fn get_goal_response_stamp(
    response: &super::action::rmw::ChessBoard_SendGoal_Response,
  ) -> (i32, u32) {
    (response.stamp.sec, response.stamp.nanosec)
  }

  fn create_feedback_message(
    goal_id: &[u8; 16],
    feedback: super::action::rmw::ChessBoard_Feedback,
  ) -> super::action::rmw::ChessBoard_FeedbackMessage {
    let mut message = super::action::rmw::ChessBoard_FeedbackMessage::default();
    message.goal_id.uuid = *goal_id;
    message.feedback = feedback;
    message
  }

  fn split_feedback_message(
    feedback: super::action::rmw::ChessBoard_FeedbackMessage,
  ) -> (
    [u8; 16],
   super::action::rmw::ChessBoard_Feedback,
  ) {
    (feedback.goal_id.uuid, feedback.feedback)
  }

  fn create_result_request(
    goal_id: &[u8; 16],
  ) -> super::action::rmw::ChessBoard_GetResult_Request {
   super::action::rmw::ChessBoard_GetResult_Request {
      goal_id: unique_identifier_msgs::msg::rmw::UUID { uuid: *goal_id },
    }
  }

  fn get_result_request_uuid(
    request: &super::action::rmw::ChessBoard_GetResult_Request,
  ) -> &[u8; 16] {
    &request.goal_id.uuid
  }

  fn create_result_response(
    status: i8,
    result: super::action::rmw::ChessBoard_Result,
  ) -> super::action::rmw::ChessBoard_GetResult_Response {
   super::action::rmw::ChessBoard_GetResult_Response {
      status,
      result,
    }
  }

  fn split_result_response(
    response: super::action::rmw::ChessBoard_GetResult_Response
  ) -> (
    i8,
   super::action::rmw::ChessBoard_Result,
  ) {
    (response.status, response.result)
  }
}


