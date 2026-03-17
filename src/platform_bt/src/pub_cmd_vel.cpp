#include "platform_bt/pub_cmd_vel.hpp"
#include "behaviortree_ros2/plugins.hpp"

bool PubCmdVel::setMessage(geometry_msgs::msg::TwistStamped &msg) {
  // Get current time for timestamp
  rclcpp::Time now = this->node_->now();
  msg.header.stamp = now;

  // Get linear_x and angular_z from input ports
  double linear_x;
  double angular_z;
  if (!getInput<double>("linear_x", linear_x)) {
    RCLCPP_ERROR(node_->get_logger(), "Failed to get input port: linear_x");
    return false;
  }
  if (!getInput<double>("angular_z", angular_z)) {
    RCLCPP_ERROR(node_->get_logger(), "Failed to get input port: angular_z");
    return false;
  }

  // Set the TwistStamped message fields
  msg.twist.linear.x = linear_x;
  msg.twist.linear.y = 0.0;
  msg.twist.linear.z = 0.0;
  msg.twist.angular.x = 0.0;
  msg.twist.angular.y = 0.0;
  msg.twist.angular.z = angular_z;

  return true;
}

// Plugin registration.
// The class SleepAction will self register with name  "SleepAction".
CreateRosNodePlugin(PubCmdVel, "PubCmdVel");