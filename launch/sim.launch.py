import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import AppendEnvironmentVariable
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node

def generate_launch_description():
    pkg_path = os.path.join(get_package_share_directory('my_bot'))
    world_path = os.path.join(pkg_path, 'worlds', 'new_track.world')

    set_env_vars_resources = AppendEnvironmentVariable(
        'GZ_SIM_RESOURCE_PATH',
        os.path.join(pkg_path, 'models'))

    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(pkg_path,'launch','rsp.launch.py')]),
        launch_arguments={'use_sim_time': 'true'}.items()
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')]),
        launch_arguments={'gz_args': world_path}.items()
    )
 
    spawn_entity = Node(
        package='ros_gz_sim', 
        executable='create',
        arguments=['-name', 'my_bot', '-topic', 'robot_description', '-z', '0.1'],
        output='screen'
    )

    return LaunchDescription([
        set_env_vars_resources,
        rsp,
        gazebo,
        spawn_entity,
    ])