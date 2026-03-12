import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.substitutions import Command, FindExecutable
from launch_ros.actions import Node


def generate_launch_description():
    urdf_file = os.path.join(
        get_package_share_directory("my_robot_description"),
        "urdf",
        "platform.urdf.xacro",
    )
    controller_params_file = os.path.join(
        get_package_share_directory("my_robot_bringup"),
        "config",
        "platform_controllers.yaml",
    )

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[
            {
                "robot_description": Command(
                    [FindExecutable(name="xacro"), " ", urdf_file]
                )
            }
        ],
    )
    controller_manager_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[controller_params_file],
    )

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster"],
    )

    diff_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_drive_controller"],
    )

    forward_command_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["forward_command_controller"],
    )

    # Delay start of robot_controller after `joint_state_broadcaster`
    delay_robot_controller_spawner_after_joint_state_broadcaster_spawner = (
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=joint_state_broadcaster_spawner,
                on_exit=[diff_controller_spawner],
            )
        )
    )

    rviz_config_file = os.path.join(
        get_package_share_directory("my_robot_description"),
        "rviz",
        "robot_display.rviz",
    )
    rviz_node = Node(
        package="rviz2", executable="rviz2", arguments=["-d", rviz_config_file]
    )

    return LaunchDescription(
        [
            controller_manager_node,
            robot_state_publisher_node,
            joint_state_broadcaster_spawner,
            forward_command_controller_spawner,
            delay_robot_controller_spawner_after_joint_state_broadcaster_spawner,
            rviz_node,
        ]
    )
