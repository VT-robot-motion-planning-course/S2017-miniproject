#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import tf
import math
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import PointCloud

# class Point:
# 	x = 0.0
# 	y = 0.0


# def onSegment(p,q,r):
# 	if(q.x <= math.max(p.x, r.x) and q.x >= math.min(p.x, r.x) and q.y <= math.max(p.y, r.y) and q.y >= math.min(p.y, r.y)):
# 		return True
# 	return False

# def orientation(p,q,r):
# 	val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
# 	if(val==0):
# 		return 0
# 	if(val>0):
# 		return 1
# 	return 2


# def doIntersect(p1,q1,p2,q2):
# 	o1=orientation(p1,q1,p2)
# 	o2=orientation(p1,q1,q2)
# 	o3=orientation(p2,q2,p1)
# 	o4=orientation(p2,q2,q1)
	
# 	if(o1 != o2 and o3 != o4):
# 		return True

# 	if (o1 == 0 and onSegment(p1, p2, q1)):
# 		return True

# 	if (o2 == 0 and onSegment(p1, q2, q1)):
# 		return True
# 	if (o3 == 0 and onSegment(p2, p1, q2)):
# 		return True
# 	if (o4 == 0 and onSegment(p2, q1, q2)):
# 		return True
# 	return False

def checkdir(goalX,goalY):
	msg= rospy.wait_for_message('/my_cloud', PointCloud)
	od= rospy.wait_for_message('/odom', Odometry)
	currX = int(round(od.pose.pose.position.x))
	currY = int(round(od.pose.pose.position.y))
	if(goalX-currX==1):
		xStep=float(currX)+0.1
		while(xStep<=goalX):
			for pt in msg.points:
				scan=np.array((pt.x,pt.y))
				rob=np.array((currX,currY))
				dist_from_rob=np.linalg.norm(rob-scan)
				step=np.array((xStep,currY))
				dist=np.linalg.norm(step-scan)
				if(dist<0.2 and dist_from_rob<1.5):
					return np.inf
			xStep+=0.1
	if(goalY-currY==1):
		yStep=float(currY)+0.1
		while(yStep<=goalY):
			for pt in msg.points:
				scan=np.array((pt.x,pt.y))
				rob=np.array((currX,currY))
				dist_from_rob=np.linalg.norm(rob-scan)
				step=np.array((currX,yStep))
				dist=np.linalg.norm(step-scan)
				if(dist<0.2 and dist_from_rob<1.5):
					return np.inf
			yStep+=0.1
	if(goalX-currX==-1):
		xStep=float(currX)-0.1
		while(xStep>=goalX):
			for pt in msg.points:
				scan=np.array((pt.x,pt.y))
				rob=np.array((currX,currY))
				dist_from_rob=np.linalg.norm(rob-scan)
				step=np.array((xStep,currY))
				dist=np.linalg.norm(step-scan)
				if(dist<0.2 and dist_from_rob<1.5):
					return np.inf
			xStep-=0.1
	if(goalY-currY==-1):
		yStep=float(currY)-0.1
		while(yStep>=goalY):
			for pt in msg.points:
				scan=np.array((pt.x,pt.y))
				rob=np.array((currX,currY))
				dist_from_rob=np.linalg.norm(rob-scan)
				step=np.array((currX,yStep))
				dist=np.linalg.norm(step-scan)
				if(dist<0.2 and dist_from_rob<1.5):
					return np.inf
			yStep-=0.1
	return 1
def getNodeNumber(currX,currY):
	node_number = 1
	node_number += currX*7
	node_number += currY
	return node_number

if __name__ == '__main__':
	rospy.init_node('dstar')
	print("initialized")
	rospy.set_param('/radius', '0.2')
	rad = rospy.get_param('/radius')
	while not rospy.is_shutdown():
		msg= rospy.wait_for_message('/odom', Odometry)
		currX = int(round(msg.pose.pose.position.x))
		currY = int(round(msg.pose.pose.position.y))

		ActX=msg.pose.pose.position.x
		ActY=msg.pose.pose.position.y

		node_position=np.array((currX,currY))
		rob_position=np.array((ActX,ActY))
		dist_from_node=np.linalg.norm(rob_position-node_position)
		if(dist_from_node<=rad):
			current_node_publisher = rospy.Publisher('/current_node', String)
			edge_cost_publisher = rospy.Publisher('/edge_costs', String)
			edge_costs=""
			#edge_costs+="\n"
			rospy.sleep(0.1)
			dir=0
			node_number=getNodeNumber(currX,currY)
			while(dir<4):
				ret=0
				if(dir==0 and currY<7):
					if(currY>=7):
						ret=0
					else:
						ret=checkdir(currX,currY+1)
						goalX=currX
						goalY=currY+1
				elif(dir==1 and currX<8):
					if(currX>=8):
						ret=0
					else:	
						ret=checkdir(currX+1,currY)
						goalX=currX+1
						goalY=currY
				elif(dir==2 and currY>0):
					if(currY<=0):
						ret = 0
					else:
						ret=checkdir(currX,currY-1)
						goalX=currX
						goalY=currY-1
				elif(dir==3 and currX>0):
					if(currX<=0):
						ret=0
					else:
						ret=checkdir(currX-1,currY)
						goalX=currX-1
						goalY=currY
				if(ret != 0):
					edge_costs+=str(getNodeNumber(currX,currY))
					edge_costs+="	"
					edge_costs+=str(getNodeNumber(goalX,goalY))
					edge_costs+="	"
					edge_costs+=str(ret)
					edge_costs+="\n"
				dir+=1
			rospy.sleep(1.0)
			current_node_publisher.publish(str(node_number))
			edge_cost_publisher.publish(edge_costs)
		else:
			print("robot too far from node")
			rospy.sleep(0.1)


	

