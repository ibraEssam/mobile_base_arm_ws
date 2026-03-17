#ifndef __BT_EXEC_SERVER_HPP__
#define __BT_EXEC_SERVER_HPP__

#include <behaviortree_cpp/xml_parsing.h>
#include <behaviortree_ros2/tree_execution_server.hpp>

class BtExecServer : public BT::TreeExecutionServer {
public:
  explicit BtExecServer(const rclcpp::NodeOptions &options)
      : BT::TreeExecutionServer(options) {}
  void onTreeCreated(BT::Tree &) {
    std::string xml_models = BT::writeTreeNodesModelXML(factory());
    RCLCPP_INFO(node()->get_logger(), "Behavior Tree XML models:\n%s",
                xml_models.c_str());
  }
};

#endif // __BT_EXEC_SERVER_HPP__