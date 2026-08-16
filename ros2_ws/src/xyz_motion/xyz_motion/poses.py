"""Joint poses (degrees) and default TCP orientation for chess XYZ targets."""

# Fixed view orientation for all chess square targets (roll, pitch, yaw) in radians.
DEFAULT_VIEW_RPY = [3.14159, 0.0, 0.0]

# --- Camera / view workflow (two levels) ---
# image_1: joint pose for a wide shot of the *whole* board (move_joints + target_joint).
# image_2: not a fixed entry here — same view angle (DEFAULT_VIEW_RPY) but TCP XYZ over a
#   *board region* from the chess module (/chess_occupancy squares + "target") via IK.
#   Teach/refine region XYZ in chess JSON; optional per-region joint poses can be added later.

# RPY values for perpendicular End-Effector: 0,90,0
#
# COMPLETE PICK-AND-PLACE PLAN (CHESS PIECES)
# 1) Hand-eye + board calibration (offline/at startup):
#    - Estimate T_base_camera (camera frame in robot base frame).
#    - Detect board corners and compute T_camera_board.
#    - Compute T_base_board = T_base_camera * T_camera_board.
#    - Persist T_base_board and verify by projecting all 64 square centers.
#
# 2) Define board frame and square mapping:
#    - Board origin: center of a1.
#    - +X: a1->b1 (files), +Y: a1->a2 (ranks), +Z: board normal.
#    - For square (file, rank) in [0..7]:
#         p_board = [(file+0.5)*square_size, (rank+0.5)*square_size, z_board]
#    - Convert to base frame with T_base_board.
#
# 3) Observation pose strategy:
#    - image_1 is a fixed, full-board overview joint pose (wide FOV, stable detection).
#    - Move to image_1 before each move cycle to refresh board occupancy.
#    - Optional: region-level image_2 poses (same tool angle, local closer view) for refinement.
#
# 4) Piece target pose generation:
#    - From board state, select source and destination squares.
#    - Build source/destination piece transforms in base frame.
#    - Apply grasp tool offset T_piece_grasp to get end-effector target pose.
#    - Build waypoints: approach (safe Z), grasp (piece Z), lift, transfer, place, retreat.
#
# 5) IK and joint-space planning:
#    - Solve IK for every Cartesian waypoint using previous q as seed.
#    - Reject solutions violating joint limits/collision constraints.
#    - Keep branch continuity (avoid elbow/wrist flips) by minimizing ||q_k - q_{k-1}||.
#    - Time-parameterize with velocity/acceleration limits.
#
# 6) Closed-loop pick accuracy (recommended):
#    - After coarse approach, capture close image and re-estimate piece center.
#    - Apply small XY correction, then descend slowly to grasp.
#    - Confirm grasp (gripper width/current/force), then lift.
#
# 7) Execution sequence:
#    - stand -> image_1 -> source_approach -> source_grasp -> close -> source_lift
#      -> dest_approach -> dest_place -> open -> dest_retreat -> stand.
#
# 8) Robustness + recovery:
#    - If IK fails: retry with alternative seed/approach yaw/safe Z.
#    - If grasp fails: retreat, re-detect locally, retry limited times.
#    - If board drift detected: rerun board calibration and continue.

# Named joint poses in degrees [A1, A2, A3, A4, A5, A6] (teach pendant order).
#
# Calibration workflow for board squares:
# 1) Keep "image_1" and "stand" as shared global poses.
# 2) For each square (a1..h8), teach 3 poses:
#    - <square>_approach : safe Z above the piece/square
#    - <square>_pick     : grasp height (used at source)
#    - <square>_place    : place height (used at destination)
# 3) Replace all placeholder values with calibrated joint angles before hardware use.
UNSET_JOINTS = [999.0, 999.0, 999.0, 999.0, 999.0, 999.0]

JOINT_POSES = {
    # Full-board camera view (overview).
    "image_1": [100.0, 0.0, -90.0, 0.0, -90.0, -90.0],

    # Arm ready between moves (chess_move startup).
    "stand": [100.0, 0.0, 0.0, 0.0, -90.0, -90.0],
}

# Auto-create calibration entries for all 64 squares.
_FILES = "abcdefgh"
_RANKS = "12345678"
for _file in _FILES:
    for _rank in _RANKS:
        _sq = f"{_file}{_rank}"
        JOINT_POSES.setdefault(f"{_sq}_approach", list(UNSET_JOINTS))
        JOINT_POSES.setdefault(f"{_sq}_pick", list(UNSET_JOINTS))
        JOINT_POSES.setdefault(f"{_sq}_place", list(UNSET_JOINTS))

# Example calibrated overrides (replace with your taught values).
JOINT_POSES["e2_approach"] = [102.3, -8.5, -92.1, 1.2, -88.0, -90.4]
JOINT_POSES["e2_pick"] = [102.9, -11.2, -96.8, 1.1, -86.7, -90.1]
JOINT_POSES["e2_place"] = [102.8, -10.9, -96.5, 1.0, -86.8, -90.2]

JOINT_POSES["e4_approach"] = [108.4, -5.1, -90.2, 1.4, -88.6, -89.7]
JOINT_POSES["e4_pick"] = [108.9, -7.6, -94.7, 1.3, -87.1, -89.5]
JOINT_POSES["e4_place"] = [108.7, -7.3, -94.4, 1.3, -87.2, -89.6]

# Backward-compatible alias used by legacy scripts.
POSES = JOINT_POSES
