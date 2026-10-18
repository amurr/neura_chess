from glob import glob

from setuptools import find_packages, setup

package_name = 'lara5_moveit'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (
            'share/' + package_name + '/config',
            [
                'config/board_hover_joints.yaml',
                'config/board_grasp_joints.yaml',
                'config/board_hover_joints_big.yaml',
                'config/board_grasp_joints_big.yaml',
                'chess_scene.yaml',
            ],
        ),
        (
            'share/' + package_name + '/meshes',
            ['meshes/chess_board.obj'],
        ),
        (
            'share/' + package_name + '/meshes/chess_pieces/collision_hulls',
            glob('meshes/chess_pieces/collision_hulls/*.stl'),
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='root@todo.todo',
    description='MoveIt helpers: chess scene collisions, board IK, moveit_master',
    license='TODO: License declaration',
    entry_points={
        'console_scripts': [
            'teach_board = lara5_moveit.teach_board:main',
            'moveit_master = lara5_moveit.moveit_master:main',
            'chess_scene_collisions = lara5_moveit.chess_scene_collisions:main',
            'chess_scene_big = lara5_moveit.chess_scene_big:main',
            'pad_joint_commands = lara5_moveit.pad_joint_commands:main',
            'isaac_state_velocity = lara5_moveit.isaac_state_velocity:main',
        ],
    },
)
