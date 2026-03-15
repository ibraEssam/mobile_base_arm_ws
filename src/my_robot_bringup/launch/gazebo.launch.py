import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, FindExecutable
from launch_ros.actions import Node


def generate_launch_description():
    urdf_file = os.path.join(
        get_package_share_directory("my_robot_description"), "urdf", "platform.gazebo"
    )
    gz_bridge_config = os.path.join(
        get_package_share_directory("my_robot_bringup"), "config", "gazebo_bridge.yaml"
    )
    world_file = os.path.join(
        get_package_share_directory("my_robot_bringup"), "worlds", "warehouse.sdf"
    )

    # include gazebo launch file
    gz_launch_file = os.path.join(
        get_package_share_directory("ros_gz_sim"), "launch", "gz_sim.launch.py"
    )
    gz_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gz_launch_file),
        launch_arguments={"gz_args": f"{world_file} -r "}.items(),
    )

    # spawn robot in gazebo
    spawn_entity_node = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=[
            "-string",
            Command([FindExecutable(name="xacro"), " ", urdf_file]),
            "-model",
            "my_robot",
        ],
        output="screen",
    )

    # Bridge
    bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        name="bridge_ros_gz",
        parameters=[
            {
                "config_file": gz_bridge_config,
                "use_sim_time": True,
            }
        ],
        output="screen",
    )

    # robot state publisher
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[{"robot_description": Command(["xacro ", urdf_file])}],
    )

    # spawn controllers after the robot is spawned in gazebo
    spawn_controllers_launch_file = os.path.join(
        get_package_share_directory("platform_movit_config"),
        "launch",
        "spawn_controllers.launch.py",
    )
    spawn_controllers_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(spawn_controllers_launch_file)
    )
    diff_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_drive_controller"],
    )

    # move_group launch after controllers are spawned
    move_group_launch_file = os.path.join(
        get_package_share_directory("platform_movit_config"),
        "launch",
        "move_group.launch.py",
    )
    move_group_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(move_group_launch_file),
        launch_arguments={"use_rviz": "false"}.items(),
    )

    ## Rviz
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        arguments=[
            "-d",
            os.path.join(
                get_package_share_directory("my_robot_bringup"), "rviz", "gazebo.rviz"
            ),
        ],
    )

    return LaunchDescription(
        [
            gz_launch,
            spawn_entity_node,
            bridge,
            robot_state_publisher_node,
            spawn_controllers_launch,
            diff_controller_spawner,
            move_group_launch,
            rviz_node,
        ]
    )
