from setuptools import setup

package_name = 'lara_ros'

setup(
    name=package_name,
    version='0.0.1',
    packages=['lara_ros', 'lara_ros.neurapy'],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/lara_ros']),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/bringup.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='andrew',
    maintainer_email='j.andregon15@gmail.com',
    description='Lara package',
    license='MIT',
    entry_points={
        'console_scripts': [
            'power = lara_ros.power:main',
            'tcp_service = lara_ros.tcp_service:main',
            'move_joint_service = lara_ros.move_joint_service:main',
            'move_linear_service = lara_ros.move_linear_service:main',
            'odom_publisher = lara_ros.odom_publisher:main',
            'command_node = lara_ros.command_node:main',
            'dance_node = lara_ros.dance_node:main',
            'music_node = lara_ros.music_node:main',
            'toast_node = lara_ros.toast_node:main',
            'gummy_bear_node = lara_ros.gummy_bear_node:main',
            'gripper_node = lara_ros.gripper_node:main'
        ],
    },
)
