#!/usr/bin/env python3
import rclpy
import math
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim_msgs.msg import Pose
from my_robot_interfaces.msg import Turtle, AliveTurtles
from my_robot_interfaces.srv import TigerSharkProtocol 

class TurtleControllerNode(Node): # MODIFY NAME
    def __init__(self):
        super().__init__("turtle_controller_node") # MODIFY NAME
        self.subscriber_target_ = Turtle()
        self.subscriber_target_.name = "wololo"
        self.subscriber_target_.x = 1.0
        self.subscriber_target_.y = 1.0 #change, asumming, [name,x,y]
        self.turtles_ = AliveTurtles()
        self.subscriber_alive_turtles_ = self.create_subscription(AliveTurtles, "alive_turtles", self.callback_alive_turtles, 10)
        self.subscriber_turtle_ = self.create_subscription(Pose, "turtle1/pose", self.callback_pose, 10)
        self.publisher_turtle_ = self.create_publisher(Twist, "turtle1/cmd_vel", 10)
        self.timer_ = self.create_timer(0.5, self.publish_cmd_vel)
        self.current_position_= None
        self.client_kill_ = self.create_client(TigerSharkProtocol, "kill_turtle")


        self.get_logger().info("Turtle controller node has started.")

    def publish_cmd_vel(self): #Speed Commands Publisher
        if self.current_position_ is None:
            return
        self.subscriber_target_ = self.callback_target()
        linear_v, angular_v = self.control_action(self.subscriber_target_)
        msg = Twist()
        msg.linear.x = linear_v
        msg.linear.y = 0.0
        msg.linear.z = 0.0
        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z =  angular_v
        self.publisher_turtle_.publish(msg) 

    def callback_pose(self, msg:Pose): #Current Position Subscriber
        self.current_position_ = (msg.x,msg.y,msg.theta)
        self.get_logger().info("Current position updated!")
    
    def callback_turtle_distance(self, target): #Distance calculator
        turtle_distance = math.sqrt((self.current_position_[0] - target.x)**2 
                              + (self.current_position_[1] - target.y)**2)
        return turtle_distance
    
    def callback_angle_dif(self, target): #Angle calculator
        delta_x = target.x - self.current_position_[0]
        delta_y = target.y - self.current_position_[1]
        target_angle = math.atan2(delta_y, delta_x)
        angle_diff = target_angle - self.current_position_[2]
        return angle_diff
 
    def callback_target(self): #Closest turtle calculator
        closest_turtle_distance = 1000
        closest_turtle = self.subscriber_target_
        for turtle in self.turtles_.turtles:
            distance_to_turtle = self.callback_turtle_distance(turtle)
            if distance_to_turtle <= closest_turtle_distance:
                closest_turtle_distance = distance_to_turtle
                closest_turtle = turtle
        return closest_turtle
            
    def pid_controller(self, error):
        p_gain = 1
        i_gain = 0
        d_gain = 0
        u_t = p_gain*error
        return u_t


    def control_action(self, ref):
        angle_error = self.callback_angle_dif(ref)
        distance_error =  self.callback_turtle_distance(ref)
        # Normalize angle (Shortest turn)
        if angle_error > math.pi: angle_error -= 2*math.pi
        elif angle_error < -math.pi: angle_error += 2*math.pi

        # Blocking Logic: If angle error is significant, ONLY rotate
        if abs(angle_error) > 0.1:
            return 0.0, self.pid_controller(angle_error)
        # If aimed correctly, move forward (charge!)
        # We can also add a small deadzone so it stops at the target
        if distance_error > 0.1:
            return self.pid_controller(distance_error), 0.0
        if ref.name != "wololo": # Don't try to kill the ghost turtle
            self.call_kill_server(ref.name)
        return 0.0, 0.0 # Stop if reached  

    def callback_alive_turtles(self, msg):
        self.turtles_ = msg

    def call_kill_server(self, turtle_name):
        request = TigerSharkProtocol.Request()
        request.target_turtle = turtle_name
        self.client_kill_.call_async(request)
  

            




def main(args=None):
    rclpy.init(args=args)
    node = TurtleControllerNode() # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()