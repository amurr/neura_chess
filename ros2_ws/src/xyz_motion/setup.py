import glob
import os

from setuptools import setup


def _example_data_files() -> list[str]:
    """Install only regular files (skip broken symlinks in build trees)."""
    paths: list[str] = []
    for path in glob.glob('config/examples/*'):
        if os.path.isfile(path):
            paths.append(path)
    return paths

package_name = 'xyz_motion'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob.glob('launch/*.launch.py')),
        ('share/' + package_name + '/config', glob.glob('config/*.yaml')),
        ('share/' + package_name + '/examples', _example_data_files()),
        (
            'share/' + package_name + '/meshes/chess_pieces/collision_hulls',
            glob.glob('meshes/chess_pieces/collision_hulls/*'),
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='andrew',
    maintainer_email='j.andregon15@gmail.com',
    description='Chess XYZ occupancy with fixed RPY for Lara TCP motion',
    license='MIT',
    entry_points={
        'console_scripts': [
            'chess_move = xyz_motion.chess_move_node:main',
            'chess_scene = xyz_motion.chess_scene_node:main',
            'publish_chess_occupancy = xyz_motion.publish_chess_occupancy:main',
            'publish_grasp_tf = xyz_motion.publish_grasp_tf:main',
            'mock_move_joints = xyz_motion.mock_move_joints:main',
            'ik_service = xyz_motion.ik_service:main',
            'camera_xyz_to_joints = xyz_motion.camera_xyz_to_joints:main',
            'gripper_joint_bridge = xyz_motion.gripper_joint_bridge:main',
        ],
    },
)
