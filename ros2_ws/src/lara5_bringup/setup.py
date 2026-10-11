from glob import glob

from setuptools import find_packages, setup

package_name = 'lara5_bringup'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
        ('share/' + package_name + '/config', glob('config/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Artem',
    maintainer_email='mursalovartem@gmail.com',
    description='Staged bringup for Lara5: description, ros2_control, MoveIt, RViz, chess application nodes.',
    license='BSD',
)
