#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from example_interfaces.msg import Int64
 
 
class MyFirstPublisher(Node): # MODIFY NAME
    def __init__(self):
        super().__init__("activity_publisher") 
        self.declare_parameter("number", 2)
        self.declare_parameter("timer_period", 0.5)
        self.robot_number_= self.get_parameter("number").value
        self.timer_period_ = self.get_parameter("timer_period").value
        self.add_post_set_parameters_callback(self.parameters_callback)

        self.publisher_ = self.create_publisher(Int64, "number", 10)
        self.timer_ = self.create_timer(self.timer_period_, self.publish_news)
        self.get_logger().info("Launching test publisher")

    def publish_news(self):
        msg = Int64()
        msg.data = self.robot_number_
        self.publisher_.publish(msg)

    def parameters_callback(self, params: list[Parameter]):
        for param in params:
            if param.name == "number":
                self.robot_number_ = param.value

def main(args=None):
    rclpy.init(args=args)
    node = MyFirstPublisher() # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()