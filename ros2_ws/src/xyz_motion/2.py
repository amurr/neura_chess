#!/usr/bin/env python3
"""Backward-compatible wrapper — prefer: ros2 run xyz_motion chess_move."""

from xyz_motion.chess_move_node import main

if __name__ == '__main__':
    main()
