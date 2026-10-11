from setuptools import find_packages, setup

package_name = 'articulation_orchestrator'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/assets', ['assets/objects_dictionary.yaml']),
    ],
    install_requires=['setuptools', 'PyYAML'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='root@todo.todo',
    description='TODO: Package description',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'articulation_orchestrator = articulation_orchestrator.articulation_orchestrator:main',
            'planning_scene_updater = articulation_orchestrator.planning_scene_updater:main',
            'chess_board_server = articulation_orchestrator.chess_board_server:main',
            'execution_logger = articulation_orchestrator.execution_logger:main',
        ],
    },
)
