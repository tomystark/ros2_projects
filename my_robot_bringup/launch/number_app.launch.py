from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    #different node object
    number_publisher = Node(
        package = "my_py_pkg", 
        executable = "activity2_publisher",
        name = "my_number_publisher",
        remappings = [("/number","my_number")]
    ) 

    number_counter = Node(
        package = "my_cpp_pkg",
        executable = "number_counter",
        name = "my_number_counter",
        remappings=[("/number","/my_number")]
    )

    ld.add_action(number_publisher)
    ld.add_action(number_counter)

    return ld