from setuptools import find_packages
from setuptools import setup

setup(
    name='moveit_master',
    version='0.1.0',
    packages=find_packages(
        include=('moveit_master', 'moveit_master.*')),
)
