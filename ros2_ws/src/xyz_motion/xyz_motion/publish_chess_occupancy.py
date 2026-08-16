#!/usr/bin/env python3
"""Publish a chess_occupancy JSON file to /chess_occupancy (one shot)."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from xyz_motion.chess_xyz import CHESS_OCCUPANCY_TOPIC


def _example_search_paths(name: str) -> list[Path]:
    """Installed share dir, then colcon source tree (for new files before rebuild)."""
    paths: list[Path] = []
    try:
        from ament_index_python.packages import get_package_share_directory

        share = Path(get_package_share_directory('xyz_motion'))
        paths.append(share / 'examples' / name)
    except Exception:
        pass

    ws = Path(os.environ.get('ROS2_WS', '/ros2_ws'))
    paths.append(ws / 'src' / 'xyz_motion' / 'config' / 'examples' / name)

    here = Path(__file__).resolve()
    for parent in here.parents:
        candidate = parent / 'config' / 'examples' / name
        if candidate.parent.is_dir():
            paths.append(candidate)
            break
    return paths


def _resolve_path(user_path: str) -> Path:
    path = Path(user_path)
    if path.is_file():
        return path

    name = path.name
    for candidate in _example_search_paths(name):
        if candidate.is_file():
            return candidate

    raise FileNotFoundError(
        f'occupancy file not found: {user_path!r} '
        f'(searched share/xyz_motion/examples and src/xyz_motion/config/examples)'
    )


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'file',
        nargs='?',
        default='full_board_after_d2d3.json',
        help='JSON path or filename under xyz_motion/config/examples/',
    )
    parser.add_argument('--topic', default=CHESS_OCCUPANCY_TOPIC)
    parser.add_argument('--count', type=int, default=1, help='publish count (default 1)')
    args = parser.parse_args(argv)

    path = _resolve_path(args.file)
    payload = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(payload, dict):
        raise SystemExit('JSON root must be an object')

    rclpy.init()
    node = Node('publish_chess_occupancy')
    pub = node.create_publisher(String, args.topic, 10)
    msg = String()
    msg.data = json.dumps(payload, separators=(',', ':'))

    import time

    deadline = time.monotonic() + 5.0
    while pub.get_subscription_count() == 0 and time.monotonic() < deadline:
        time.sleep(0.05)

    if pub.get_subscription_count() == 0:
        node.get_logger().error(
            'no subscriber on chess_occupancy — start chess_scene first, then retry'
        )
        node.destroy_node()
        rclpy.shutdown()
        raise SystemExit(1)

    for _ in range(max(1, args.count)):
        pub.publish(msg)
        time.sleep(0.1)

    squares = payload.get('squares')
    n = len(squares) if isinstance(squares, dict) else '?'
    node.get_logger().info(f'published {path.name} ({n} squares) -> {args.topic}')
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    try:
        main()
    except (FileNotFoundError, json.JSONDecodeError, SystemExit) as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)
