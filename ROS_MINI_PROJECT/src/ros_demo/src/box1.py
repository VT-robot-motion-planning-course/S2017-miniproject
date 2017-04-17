#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import tf
import math
import numpy as np
from std_msgs.msg import String
from std_msgs.msg import Int32




def callback(goalX,goalY):
	kP = 0.25
	tolerence = 0.1
	print(goalX)
	print(goalY)
	p = rospy.Publisher('/box1/cmd_vel', Twist)
	while(True):
		msg= rospy.wait_for_message('/box1/odom', Odometry)
		(roll, pitch, yaw) = tf.transformations.euler_from_quaternion([msg.pose.pose.orientation.x, msg.pose.pose.orientation.y, msg.pose.pose.orientation.z, msg.pose.pose.orientation.w])
		currX = msg.pose.pose.position.x
		currY = msg.pose.pose.position.y
		print "============CURRENT POSITION==========="
		print(currX)
		print(currY)
		twist=Twist()
		heading  = math.atan2((goalY - currY),(goalX - currX))
		#### modification ####
		#error = kP * (heading - yaw)
		error = heading - yaw
		error = ((error + np.pi)%(2.0*np.pi)) - np.pi
		error = kP * error
		######################
		errDist = math.sqrt((goalX - currX)*(goalX - currX)+(goalY - currY)*(goalY - currY))
		print "=============="
		print error
		print "=============="
		
		print "                "
		print "=============="
		print errDist
		print "=============="
		if errDist < tolerence:
			print "GOAL REACHED"
			twist.angular.z = 0
			twist.linear.x = 0
			p.publish(twist)
			return	
		twist.angular.z = error
		twist.linear.x = 0.1
		p.publish(twist)
		rospy.loginfo("Moving")
		rospy.sleep(0.1)

if __name__ == '__main__':
	rospy.init_node('move_box1')
	print("initialized")
	p = rospy.Publisher("/box1/cmd_vel", Twist)
	rospy.sleep(2.0)
	twist = Twist()
	twist.angular.z=0.18
	p.publish(twist)
	rospy.sleep(5)
	twist.angular.z=0
	p.publish(twist)
	rospy.sleep(1.0)
	while not rospy.is_shutdown():
		callback(5,2)
		rospy.sleep(1.0)
		twist.angular.z=0.4
		p.publish(twist)
		rospy.sleep(5)
		twist.angular.z=0
		p.publish(twist)
		rospy.sleep(1.0)
		callback(5,-4)
		rospy.sleep(1.0)
		twist.angular.z=0.4
		p.publish(twist)
		rospy.sleep(5)