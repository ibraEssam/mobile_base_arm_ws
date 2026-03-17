#ifndef __PLATOFRM_BT_PUB_CMD_VEL_HPP__
#define __PLATOFRM_BT_PUB_CMD_VEL_HPP__
#include "behaviortree_ros2/bt_topic_pub_node.hpp"
#include "geometry_msgs/msg/twist_stamped.hpp"

class PubCmdVel : public BT::RosTopicPubNode<geometry_msgs::msg::TwistStamped> {
public:
  explicit PubCmdVel(const std::string &name, const BT::NodeConfig &conf,
                     const BT::RosNodeParams &params)
      : BT::RosTopicPubNode<geometry_msgs::msg::TwistStamped>(name, conf,
                                                              params) {}

  static BT::PortsList providedPorts() {
    auto extra_ports =
        BT::PortsList{BT::InputPort<double>("linear_x", 0.0,
                                            "Linear velocity in x direction"),
                      BT::InputPort<double>("angular_z", 0.0,
                                            "Angular velocity around z axis")};
    return providedBasicPorts(extra_ports);
  }
  virtual bool setMessage(geometry_msgs::msg::TwistStamped &msg) override;
};

#endif