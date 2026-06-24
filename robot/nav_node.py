#!/usr/bin/env python
import rospy
import actionlib
import socket
import pickle
import tf
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

HOST = "192.168.43.159"
PORT = 2055


def patrol(waypoint_x, waypoint_y, delta):
    q = tf.transformations.quaternion_from_euler(0.0, 0.0, delta)

    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()

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

    client.send_goal(goal)


def goal():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))

    rospy.loginfo("Nav node listening on %s:%d", HOST, PORT)

    while not rospy.is_shutdown():
        data, addr = sock.recvfrom(1024)
        line = pickle.loads(data)
        if len(line) == 3:
            waypoint_x = float(line[0])
            waypoint_y = float(line[1])
            delta = float(line[2])
            rospy.loginfo("Goal received: x=%.2f  y=%.2f  yaw=%.2f", waypoint_x, waypoint_y, delta)
            patrol(waypoint_x, waypoint_y, delta)
        else:
            rospy.logwarn("Received incomplete UDP packet from master — ignoring.")


if __name__ == '__main__':
    rospy.init_node('shuttle_nav_node', anonymous=True)
    goal()
    rospy.spin()
