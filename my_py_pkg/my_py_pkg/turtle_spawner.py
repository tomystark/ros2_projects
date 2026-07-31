#!/usr/bin/env python3
import math
import rclpy
import random
from rclpy.node import Node
from turtlesim_msgs.srv import Spawn
from turtlesim_msgs.srv import Kill
from functools import partial
from my_robot_interfaces.msg import AliveTurtles , Turtle
from my_robot_interfaces.srv import TigerSharkProtocol
 
 
class TurtleSpawnerNode(Node): 
    def __init__(self):
        super().__init__("turtle_spawner_node") 
        self.client_spawn_ = self.create_client(Spawn, "spawn")
        self.client_kill_ = self.create_client(Kill, "kill")
        self.alive_turtles_ = {}
        self.alive_turtles_publisher_ = self.create_publisher(AliveTurtles, "alive_turtles", 10)
        self.timer_ = self.create_timer(5, self.call_spawn)
        self.timer_publisher_ = self.create_timer(1.0, self.callback_alive_turtles_publisher)
        self.kill_turtle_service = self.create_service(TigerSharkProtocol, "kill_turtle", self.callback_kill_turtle)

    def call_spawn(self):
        while not self.client_spawn_.wait_for_service(1.0):
            self.get_logger().warn("Waiting for Turtle Spawn trigger...")
        request = Spawn.Request()
        request.x = random.uniform(1.0, 10.0)
        request.y = random.uniform(1.0, 10.0)
        request.theta = random.uniform(-math.pi, math.pi)
        future = self.client_spawn_.call_async(request)
        future.add_done_callback(partial(self.callback_spawn_turtle, request=request))

    def callback_spawn_turtle(self,future,request):
        try:
            response = future.result()
            if response.name != "":
                self.get_logger().info(f"Spawned {response.name} at {request.x}, {request.y}")
                # Store it in your dictionary!
                self.alive_turtles_[response.name] = [request.x, request.y]
        except Exception as e:
            self.get_logger().error(f"Service call failed: {e}")   
        
    def callback_alive_turtles_publisher(self):
        msg = AliveTurtles()
        for name, coords in self.alive_turtles_.items():
            t = Turtle()
            t.name = name
            t.x = coords[0]
            t.y = coords[1]
            msg.turtles.append(t)
        self.alive_turtles_publisher_.publish(msg)
    
    def callback_kill_turtle(self, request: TigerSharkProtocol.Request, response: TigerSharkProtocol.Response):
        target_name = request.target_turtle
        if target_name in self.alive_turtles_:
            # 1. Remove from your Spawner's internal memory
            del self.alive_turtles_[target_name]
            
            # 2. Tell the REAL turtlesim window to remove it
            kill_req = Kill.Request()
            kill_req.name = target_name
            self.client_kill_.call_async(kill_req)
            
            self.get_logger().info(f"TigerSharkProtocol: {target_name} has been caught!")
            response.success = True
        else:
            response.success = False
            
        return response

def main(args=None):
    rclpy.init(args=args)
    node = TurtleSpawnerNode() 
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()