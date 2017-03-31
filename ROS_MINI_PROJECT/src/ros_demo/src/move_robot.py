#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import tf
import math
import numpy as np
from std_msgs.msg import String
from std_msgs.msg import Int32


def getXY(node_number):
	node_number-=1
	grid_size_x = rospy.get_param('/grid_size_x')
	grid_size_y = rospy.get_param('/grid_size_y')
	grid_step = rospy.get_param('/grid_step') 
	goalX=node_number/(grid_size_y*grid_step)
	goalY=node_number%(grid_size_y*grid_step)
	return goalX,goalY

def move(goalX,goalY):
	kP = 0.75
	tolerence = 0.1
	print(goalX)
	print(goalY)
	p = rospy.Publisher('/cmd_vel', Twist)
	while(True):
		msg= rospy.wait_for_message('/odom', Odometry)
		(roll, pitch, yaw) = tf.transformations.euler_from_quaternion([msg.pose.pose.orientation.x, msg.pose.pose.orientation.y, msg.pose.pose.orientation.z, msg.pose.pose.orientation.w])
		currX = msg.pose.pose.position.x
		currY = msg.pose.pose.position.y
		print "============CURRENT POSITION==========="
		print(currX)
		print(currY)
		twist=Twist()
		heading  = math.atan2((goalY - currY),(goalX - currX))
		error = kP * (heading - yaw)
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
	rospy.init_node('move_robot')
	print("initialized")
	while not rospy.is_shutdown():
		msg= rospy.wait_for_message('/goal', Int32)
		goalX,goalY=getXY(msg.data)
		move(goalX,goalY)
		rospy.sleep(1.0)



	

