cmake_minimum_required(VERSION 3.20)
project(my_cpp_pkg)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(example_interfaces REQUIRED)
find_package(my_robot_interfaces REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

add_executable(cpp_node src/my_first_node.cpp)
target_link_libraries(cpp_node rclcpp::rclcpp)

add_executable(robot_news_station src/robot_news_station.cpp)
target_link_libraries(robot_news_station rclcpp::rclcpp example_interfaces::example_interfaces)

add_executable(smartphone src/smartphone.cpp)
target_link_libraries(smartphone rclcpp::rclcpp example_interfaces::example_interfaces)

add_executable(add_two_ints_server src/add_two_ints_server.cpp)
target_link_libraries(add_two_ints_server rclcpp::rclcpp example_interfaces::example_interfaces)

add_executable(add_two_ints_client_no_oop src/add_two_ints_client_no_oop.cpp)
target_link_libraries(add_two_ints_client_no_oop rclcpp::rclcpp example_interfaces::example_interfaces)

add_executable(add_two_ints_client src/add_two_ints_client.cpp)
target_link_libraries(add_two_ints_client rclcpp::rclcpp example_interfaces::example_interfaces)

add_executable(number_counter src/number_counter.cpp)
target_link_libraries(number_counter rclcpp::rclcpp example_interfaces::example_interfaces)

add_executable(number_publisher src/number_publisher.cpp)
target_link_libraries(number_publisher rclcpp::rclcpp example_interfaces::example_interfaces)

add_executable(hw_status_publisher src/hardware_status_publisher.cpp)
target_link_libraries(hw_status_publisher rclcpp::rclcpp my_robot_interfaces::my_robot_interfaces)


install(TARGETS
    cpp_node
    robot_news_station
    smartphone
    add_two_ints_server
    add_two_ints_client_no_oop
    add_two_ints_client
    number_counter
    number_publisher       
    hw_status_publisher 
    DESTINATION lib/${PROJECT_NAME}
)

ament_package()
