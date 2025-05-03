from setuptools import find_packages, setup

package_name = 'my_camera_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],  # Add other runtime dependencies here if needed
    zip_safe=True,
    maintainer='ros2vm',
    maintainer_email='ros2vm@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    entry_points={
        'console_scripts': [
            "robot_camera_publisher = my_camera_pkg.robot_camera_publisher:main",
            "robot_camera_subscriber = my_camera_pkg.robot_camera_subscriber:main",
            "sample = my_camera_pkg.sample:main",
            "del = my_camera_pkg.del:main"
        ],
    },
)
