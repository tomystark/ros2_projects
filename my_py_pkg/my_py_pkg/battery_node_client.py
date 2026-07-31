#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_robot_interfaces.srv import SetLed
from functools import partial 

class BatteryNode(Node): # MODIFY NAME
    def __init__(self):
        super().__init__("battery_node") # MODIFY NAME
        self.client_ =self.create_client(SetLed, "set_led")
        self.last_update_time_ = self.get_clock().now()
        self.battery_ = 1
        self.discharge_ = True
        self.timer_battery_cycle_ = self.create_timer(0.5 , self.callback_battery_life)
        self.get_logger().info("Battery node has been started")


    def callback_battery_life(self):
        current_time = self.get_clock().now()
        duration = (current_time - self.last_update_time_).nanoseconds/1e9
        if not self.discharge_:
            if duration >= 6.0: # Time to switch to charging
                self.battery_ = 1
                self.discharge_ = True
                self.last_update_time_ = current_time
                self.get_logger().info("Battery Full")
                self.call_set_led()
        else:
            if duration >= 4.0: # Time to switch to discharging
                self.battery_ = 0
                self.discharge_ = False
                self.last_update_time_ = current_time
                self.get_logger().info("Battery Low")
                self.call_set_led()
  

    def call_set_led(self):
        #Standby
        while not self.client_.wait_for_service(1.0):
            self.get_logger().warn("Waiting for Set led Server....")    
        
        # Engaged
        request = SetLed.Request()
        request.led_state  = "" #"ON - OFF"
        request.led_number = 0 # "Num between 1,3"

        if self.battery_ == 0:
            request.led_state  = "ON" #"ON - OFF"
            request.led_number = 0 # "Num between 1,3"
        else:
            request.led_state  = "OFF" #"ON - OFF"
            request.led_number = 0 # "Num between 1,3"
            

        future = self.client_.call_async(request)
        future.add_done_callback(partial(self.callback_call_set_led, request=request))

    def callback_call_set_led(self,future,request):
        response = future.result()
        self.get_logger().info("Set led"+str(response.success))    
 
 
def main(args=None):
    rclpy.init(args=args)
    node = BatteryNode() # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()