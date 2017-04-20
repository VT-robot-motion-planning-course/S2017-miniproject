#include "ros/ros.h"
#include "geometry_msgs/Twist.h"
#include "sensor_msgs/Joy.h"
 
ros::Publisher pioneer_vel;
 
void joyCallback(const sensor_msgs::Joy::ConstPtr& joy)
{
	ROS_INFO("I heard: linear_:[%f]   angular_[%d]", joy->axes[1], joy->axes[0]);
  	geometry_msgs::Twist twist;
        twist.linear.x = joy->axes[1] > 0 ? (joy->axes[1] > 0.5 ? 1 : joy->axes[1]) : (joy->axes[1] < -0.5 ? -1 : joy->axes[1]) ;
        twist.linear.y = 0;
        twist.angular.z= joy->axes[0] > 0 ? (joy->axes[0] > 0.5 ? 1 : joy->axes[0]) : (joy->axes[0] < -0.5 ? -1 : joy->axes[0]);
        pioneer_vel.publish(twist);
}
 
int main(int argc, char **argv)
{
 
        // initialize ros
        ros::init(argc, argv, "Joystick_controller");
	ros::NodeHandle n;
 
        // create publisher
 
        ros::Publisher cmd_vel_topic = n.advertise<geometry_msgs::Twist>("/cmd_vel", 1000);
 
        pioneer_vel = cmd_vel_topic;
 
        ros::Subscriber joy_command = n.subscribe<sensor_msgs::Joy>("joy", 10, joyCallback);
 
        // our loop will publish at 10Hz
        ros::Rate loop_rate(5);
 
	ros::spin();
}
