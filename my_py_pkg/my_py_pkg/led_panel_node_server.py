#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_robot_interfaces.srv import SetLed
from my_robot_interfaces.msg import LedStatus 


class LedPanelNode(Node): # MODIFY NAME
    def __init__(self):
        super().__init__("led_panel_node") # MODIFY NAME
        self.get_logger().info("LED panel node has been started")
        self.declare_parameter("led_state", [0,0,0])
        self.led_ = self.get_parameter("led_state").value
        self.led_status_pub = self.create_publisher(LedStatus, "led_panel_state",10)
        self.timer_ = self.create_timer(1.0 , self.publish_panel_state)
        self.set_led_server_ = self.create_service(
            SetLed, "set_led", self.server_callback_set_led)
        
    def publish_panel_state(self):
        msg = LedStatus()
        msg.led_state[0] = self.led_[0]
        msg.led_state[1] = self.led_[1]
        msg.led_state[2] = self.led_[2]
        self.led_status_pub.publish(msg)

    def server_callback_set_led(self, request: SetLed.Request, response:SetLed.Response):
        # 1. Check if the LED index is valid
        if request.led_number < 0 or request.led_number >= len(self.led_states_):
            response.success = False
            self.get_logger().error(f"Invalid LED number: {request.led_number}")
            return response
        
        # 2. Check if the state is valid
        if request.state.upper() not in ["ON", "OFF"]:
            response.success = False
            return response
        # 3. Good ending
        if request.led_state.upper() == "ON":
            self.led_[request.led_number]= 1
            response.success = True
        elif request.led_state.upper()=="OFF":
            self.led_[request.led_number]= 0
            response.success = True
        else:
            response.success = False
        return response        
 
def main(args=None):
    rclpy.init(args=args)
    node = LedPanelNode() # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()