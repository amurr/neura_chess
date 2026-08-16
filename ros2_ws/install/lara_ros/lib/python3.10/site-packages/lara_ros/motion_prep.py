"""Shared robot prep before motion (power, mode, faults, init_program)."""

from __future__ import annotations

import logging
from typing import Any, Optional

from lara_ros.neurapy.robot import Robot


def _log(logger: Optional[Any], level: str, msg: str) -> None:
    if logger is None:
        return
    getattr(logger, level, logger.info)(msg)


def ensure_robot_ready(robot: Robot, logger: Optional[Any] = None) -> None:
    """
    Prepare robot for motion. Raises RuntimeError if not safe to move.

    Red end-effector LED usually means critical fault — clear on teach pendant first.
    """
    try:
        robot.power_on()
    except Exception as e:
        _log(logger, "debug", f"power_on: {e}")

    if not (
        robot.is_robot_in_automatic_mode()
        or robot.is_robot_in_semi_automatic_mode()
    ):
        _log(logger, "info", "Switching robot to Automatic mode")
        robot.switch_to_automatic_mode()

    diag = robot.get_diagnostics()
    if diag.get("critical"):
        issues = diag.get("issues", {})
        try:
            robot.reset_errors()
        except Exception:
            pass
        try:
            robot.reset_collision()
        except Exception:
            pass
        diag = robot.get_diagnostics()
        if diag.get("critical"):
            err_list = issues.get("other_errors") or issues
            raise RuntimeError(
                "Robot has a critical fault (red LED). "
                f"Diagnostics: {err_list}. "
                "On the teach pendant / web UI: acknowledge errors, Reset control, "
                "then run: python3 src/xyz_motion/prep_robot.py"
            )

    robot.init_program()
