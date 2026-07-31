from ament_index_python.packages import get_package_share_path
from launch import LaunchDescription
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
import os

def generate_launch_description():
    ld = LaunchDescription()
    urdf_path = os.path.join(get_package_share_path("my_robot_description"),
                             "urdf","new_activity_robot.urdf.xacro")
    rviz_config_path = os.path.join(get_package_share_path("my_robot_description"),
                             "rviz","differential_traction_robot_config.rviz")
    robot_description = ParameterValue(Command(["xacro ", urdf_path]), value_type=str)

    #different node Node object than the one used in OOP
    robot_state_publisher_node = Node(
        package = "robot_state_publisher", 
        executable = "robot_state_publisher",
        parameters=[{"robot_description" : robot_description}]
    ) 
    joint_state_publisher_gui_node = Node(
        package = "joint_state_publisher_gui", 
        executable = "joint_state_publisher_gui"
    ) 
    rviz_node = Node(
        package = "rviz2", 
        executable = "rviz2",
    arguments=["-d",rviz_config_path]
    ) 

    ld.add_action(robot_state_publisher_node)
    ld.add_action(joint_state_publisher_gui_node)
    ld.add_action(rviz_node)
    
    return ld

#return LaunchDescription([
# robot_state_publisher_node,
# joint_state_publisher_gui_node,
# rviz_node
#])