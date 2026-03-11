from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_demo_launch
from launch_ros.actions import Node

def generate_launch_description():
    moveit_config = MoveItConfigsBuilder("my_platform", package_name="platform_movit_config").to_moveit_configs()
    diff_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=["diff_drive_controller"],
    )
    moveit_launch = generate_demo_launch(moveit_config)
    moveit_launch.add_action(diff_controller_spawner)
    return moveit_launch
