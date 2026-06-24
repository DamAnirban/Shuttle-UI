#!/usr/bin/env python
import rospy
import actionlib
import socket
import pickle
import time
import tf
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Vector3
from math import sqrt,atan2,cos,sin,pi

count_flag = 0           # Sets the current count of goal
target = 4               # Number of goals


msg = ''' USER INTERFACE
----------------------------------
			   8 : move to nxt goal
			   5 : stop
			   2 : skip next goal
		   	   0 : retry goal
'''

def patrol(waypoint_x ,waypoint_y, delta):
	       
	#convert ypr to quarternion
	q = tf.transformations.quaternion_from_euler(0.0, 0.0, delta)

	# Get an action client
	client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
	client.wait_for_server()

	# Define the goal
	goal = MoveBaseGoal()
	goal.target_pose.header.frame_id = 'map'
	goal.target_pose.header.stamp = rospy.Time.now()
	goal.target_pose.pose.position.x = waypoint_x
	goal.target_pose.pose.position.y = waypoint_y
	goal.target_pose.pose.position.z = 0.0
	goal.target_pose.pose.orientation.x = q[0]
	goal.target_pose.pose.orientation.y = q[1]
	goal.target_pose.pose.orientation.z = q[2]
	goal.target_pose.pose.orientation.w = q[3]
	
	# Send the goal
	client.send_goal(goal)
	#client.wait_for_result()

def goal():
	
	host="192.168.43.159"
	port=2055
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind((host,port))
	
	global target, count_flag
	rate = rospy.Rate(10.0)

	while not rospy.is_shutdown():
		data,addr = sock.recvfrom(1024)
		line = pickle.loads(data)
		if len(line) == 3: 
			waypoint_x = float(line[0])
            waypoint_y = float(line[1])
	        delta = float(line[2])
			patrol (waypoint_x ,waypoint_y, delta)

		else:
            rospy.loginfo("received incomplete UDP packet from master")
	    continue


if __name__ == '__main__':
	print(msg)    
	rospy.init_node('goal_sequence', anonymous=True)
	goal()
	rospy.spin()


































