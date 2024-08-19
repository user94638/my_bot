import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.substitutions import Command, LaunchConfiguration
from launch.actions import DeclareLaunchArgument

from launch_ros.actions import Node

def generate_launch_description():
    use_sim_time_launch_arg = DeclareLaunchArgument('use_sim_time', default_value='false')
    
    urdf_path = os.path.join(get_package_share_directory('my_bot'),'description','robot.urdf.xacro')
    robot_description_content = Command(['xacro ', urdf_path])
    
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description_content,
            'use_sim_time': LaunchConfiguration('use_sim_time')        
        }]
    )

    return LaunchDescription([
        use_sim_time_launch_arg,
        robot_state_publisher_node
    ])

