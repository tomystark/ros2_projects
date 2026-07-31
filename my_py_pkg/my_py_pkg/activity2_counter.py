#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64
 
 
class MyFirstCounter(Node): # MODIFY NAME
    def __init__(self):
        super().__init__("activity_counter") 
        self.last_number_ = 0
        self.counter = 0
        self.get_logger().info("Launching counter") #log/print para indicar lanzamiento del nodo
        self.publisher_ = self.create_publisher(Int64, "number_count", 10)
        self.subscriber_ = self.create_subscription(Int64, "number", self.callback_number, 10 )
        self.timer_ = self.create_timer(0.5, self.publish_news)

    def callback_number(self, msg:Int64): #SUBSCRIBER
        self.last_number_ = msg.data
        self.get_logger().info("Count"+str(self.counter)+"Value:"+str(msg.data))
        self.counter += 1

    def publish_news(self): #PUBLISHER
        msg = Int64()
        msg.data = self.last_number_
        self.publisher_.publish(msg)
 
def main(args=None):
    rclpy.init(args=args)
    node = MyFirstCounter() # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()