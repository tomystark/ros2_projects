#!/usr/bin/env python3
import rclpy
import time
import threading
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse, CancelResponse 
from rclpy.action.server import ServerGoalHandle
from my_robot_interfaces.action import MoveRobot
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup

 
class MoveRobotServerNode(Node): 
    def __init__(self):
        super().__init__("move_robot_server")
        self.goal_handle_: ServerGoalHandle = None
        self.goal_lock_ = threading.Lock()
        #self.goal_queue_= []
        self.robot_position_ = 50
        self.move_robot_server_ =  ActionServer(
            self,
            MoveRobot,
            "move_robot",
            goal_callback=self.goal_callback,
            #handle_accepted_callback=self.handle_accepted_callback,
            cancel_callback=self.cancel_callback,
            execute_callback=self.execute_callback,
            callback_group=ReentrantCallbackGroup())
        self.get_logger().info("Action has been started")
        self.get_logger().info("Robot position: " + str(self.robot_position_))
        
    def goal_callback(self, goal_request: MoveRobot.Goal):
        self.get_logger().info("Received a goal")
        #Policy: refuse new goal if currect goal is still active
        #if self.goal_handle_ is not None and self.goal_handle_.is_active:
        #    self.get_logger().info("A goal is already active, rejecting new goal")
        #    return GoalResponse.REJECT

        #Validate the goal request upper lower limit
        if goal_request.position not in range (0, 100) or goal_request.velocity <= 0 :
            self.get_logger().info("Rejecting the goal")
            return GoalResponse.REJECT
        
        #Policy: preempt existing goal when recieving new goal
        with self.goal_lock_:
            if self.goal_handle_ is not None and self.goal_handle_.is_active:
                self.get_logger().info("Abort current goal")
                self.goal_handle_.abort()

        self.get_logger().info("Accepting the goal")
        return GoalResponse.ACCEPT

    #def handle_accepted_callback(self, goal_handle:ServerGoalHandle):
        #with self.goal_lock_:
            #if self.goal_handle_ is not None:
                #self.goal_queue_.append(goal_handle)
            #else:
                #goal_handle.execute()

    def cancel_callback(self,goal_handle:ServerGoalHandle):
        self.get_logger().info("Received a cancel request")
        return CancelResponse.ACCEPT #or reject

    def execute_callback(self, goal_handle: ServerGoalHandle):
        with self.goal_lock_:
            self.goal_handle_ = goal_handle 

        #get request from goal
        goal_position = goal_handle.request.position
        velocity = goal_handle.request.velocity

        result = MoveRobot.Result()
        feedback = MoveRobot.Feedback() 

        self.get_logger().info("Execute goal")
        #Execute the action
        while rclpy.ok():
            if not goal_handle.is_active:
                result.position = self.robot_position_
                result.message = "Preempted by another goal"
                return result

            if goal_handle.is_cancel_requested:
                result.position = self.robot_position_
                if goal_position == self.robot_position_:
                    result.message = "Success after canceled call"
                    goal_handle.succeed()
                else:
                    result.message = "Canceled"
                    goal_handle.canceled()
                return result

            diff = goal_position - self.robot_position_
            if diff == 0:
                result.position = self.robot_position_
                result.message = "Success"
                goal_handle.succeed()
                return result
            elif diff > 0:
                if diff >= velocity:
                    self.robot_position_ += velocity
                else:
                    self.robot_position_ += diff    

            else:
                if abs(diff) >= velocity:
                    self.robot_position_ -= velocity
                else:
                    self.robot_position_ -= abs(diff)

            self.get_logger().info("Robot position: " + str(self.robot_position_))
            feedback.current_position = self.robot_position_
            goal_handle.publish_feedback(feedback)

            time.sleep(1.0)

        #Once done, set goal final state
        goal_handle.succeed()

        #Send result
        result = MoveRobot.Result.position()
        self.process_next_goal_in_queue()
        return result
    
    #def process_next_goal_in_queue(self):
        #with self.goal_lock_:
            #if len(self.goal_queue_) > 0:
                #self.goal_queue_.pop(0).execute()
            #else:
                #self.goal_handle_ = None
 
def main(args=None):
    rclpy.init(args=args)
    node = MoveRobotServerNode()
    rclpy.spin(node, MultiThreadedExecutor())
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()