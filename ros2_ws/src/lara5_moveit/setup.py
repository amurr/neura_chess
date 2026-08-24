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
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='root@todo.todo',
    description='MoveIt chess pick using Isaac Sim piece poses',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'moveit_chess = lara5_moveit.moveit_chess:main',
            'pad_joint_commands = lara5_moveit.pad_joint_commands:main',
            'relay_isaac_joint_states = lara5_moveit.relay_isaac_joint_states:main',
            'activate_controllers = lara5_moveit.activate_controllers:main',
            'sanitize_follow_joint_trajectory = lara5_moveit.sanitize_follow_joint_trajectory:main',
        ],
    },
)
