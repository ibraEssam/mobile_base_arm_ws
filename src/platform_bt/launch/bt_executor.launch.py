from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    # server parameters file
    bt_executor_params_file = DeclareLaunchArgument(
        "bt_executor_params_file",
        default_value=os.path.join(
            get_package_share_directory("platform_bt"),
            "config",
            "bt_executor_params.yaml",
        ),
        description="Path to the bt_executor parameters file",
    )

    bt_executor_node = Node(
        package="platform_bt",
        executable="bt_executor",
        output="screen",
        parameters=[
            LaunchConfiguration("bt_executor_params_file"),
        ],
    )

    return LaunchDescription([bt_executor_params_file, bt_executor_node])
