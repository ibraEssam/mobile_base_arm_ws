cmake_minimum_required(VERSION 3.8)
project(platform_bt)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()


# find dependencies
find_package(ament_cmake REQUIRED)
find_package(behaviortree_ros2 REQUIRED)
find_package(moveit_ros_planning_interface REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)

include_directories(include)

add_executable(bt_executor src/bt_executor.cpp)
ament_target_dependencies(bt_executor
  behaviortree_ros2
)
install(TARGETS bt_executor
  DESTINATION lib/${PROJECT_NAME}
)

# add the command velocity publisher node
add_library(pub_cmd_vel SHARED src/pub_cmd_vel.cpp)
target_compile_definitions(pub_cmd_vel PRIVATE  BT_PLUGIN_EXPORT)
ament_target_dependencies(pub_cmd_vel
  behaviortree_ros2
  geometry_msgs
)
install(TARGETS
  pub_cmd_vel
  LIBRARY DESTINATION share/${PROJECT_NAME}/bt_plugins
  ARCHIVE DESTINATION share/${PROJECT_NAME}/bt_plugins
  RUNTIME DESTINATION share/${PROJECT_NAME}/bt_plugins
  )



install(DIRECTORY
    behavior_trees
    config
    launch
    DESTINATION share/${PROJECT_NAME}/
    )

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
