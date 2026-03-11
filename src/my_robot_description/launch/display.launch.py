from launch_ros.actions import Node
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch.actions import DeclareLaunchArgument

def generate_launch_description():
    # choose from one of the available URDF/Xacro files in src/my_robot_description/urdf
    robot_variant_arg = DeclareLaunchArgument(
        'robot_variant',
        default_value='platform',
        choices=['arm_with_gripper', 'platform'],
        description='Select URDF/xacro file to use for the robot. Options: "arm_with_gripper" or "platform". Default is "platform".'
    )

    urdf_file_name = LaunchConfiguration('robot_variant')
    urdf_file = PathJoinSubstitution([
        get_package_share_directory('my_robot_description'),
        'urdf',
        [urdf_file_name,
        ".urdf.xacro"]
    ])

    # Process the chosen xacro file to generate the final URDF
    urdf_content = Command(['xacro ', urdf_file])

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': urdf_content}]
    )

    joint_state_publisher_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        output='screen'
    )

    rviz_config_file = get_package_share_directory('my_robot_description') + '/rviz/robot_display.rviz'
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_file]
    )

    return LaunchDescription([
        robot_variant_arg,
        robot_state_publisher_node,
        joint_state_publisher_node,
        rviz_node
    ])