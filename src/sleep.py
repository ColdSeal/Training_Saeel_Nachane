#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import sys

class TurtleBot:
    def __init__(self):
        # Creates a node with name 'turtlebot_controller' and make sure it is a
        # unique node (using anonymous=True).
        rospy.init_node('my_initials', anonymous=True)
        # Publisher which will publish to the topic '/turtle1/cmd_vel'.
        self.velocity_publisher = rospy.Publisher('/turtle1/cmd_vel',Twist, queue_size=7)

        # A subscriber to the topic '/turtle1/pose'. self.update_pose is called
        # when a message of type Pose is received.
        self.pose_subscriber = rospy.Subscriber('/turtle1/pose',Pose, self.update_pose)

        self.pose = Pose()
        self.rate = rospy.Rate(7)
        self.num_goals = 0

    def update_pose(self, data):
        """Callback function which is called when a new message of type Pose is
        received by the subscriber."""
        self.pose = data

    def update_goal_pose(self):

        goal = [Pose(), Pose(), Pose(), Pose(), Pose(), Pose()]
        goal[0].x = 5.544445
        goal[0].y = 5.544445
        goal[1].x = 4.544445
        goal[1].y = 5.544445
        goal[2].x = 4.544445
        goal[2].y = 4.544445
        goal[3].x = 5.544445
        goal[3].y = 4.544445
        goal[4].x = 5.544445
        goal[4].y = 3.544445
        goal[5].x = 4.544445
        goal[5].y = 3.544445

        self.goal_pose = goal[self.num_goals]

    def checkpoint(self):
        if(abs(self.goal_pose.x - self.pose.x)<= 0.01 and abs(self.goal_pose.y - self.pose.y)<= 0.01):
            self.num_goals = self.num_goals + 1
            return True 
        else :
            return False 

    def find_vel(self):
        vel_msg = Twist()
        x, y, x0, y0 = self.pose.x, self.pose.y, self.goal_pose.x, self.goal_pose.y

        if(x0-x>0.01 and y0-y<=0.01):
            vel_msg.linear.x = -1
            vel_msg.linear.y = 0
        elif(abs(x0-x)<=0.01 and y0-y>0.01):
            vel_msg.linear.x = 0
            vel_msg.linear.y = -1
        elif(x0-x>0.01 and abs(y0-y)<=0.01):
            vel_msg.linear.x = 1
            vel_msg.linear.y = 0
        elif(x0-x<=0.01 and y-y0>0.01):
            vel_msg.linear.x = 0
            vel_msg.linear.y = -1
        elif(abs(x0-x)>0.01 and y-y0<=0.01):
            vel_msg.linear.x = -1
            vel_msg.linear.y = 0
        
            return vel_msg

    def move(self):
        vel_msg = Twist()
        vel_msg.linear.x = -1
        vel_msg.linear.y = 0
        self.update_goal_pose()
        while not rospy.is_shutdown():
            self.velocity_publisher.publish(vel_msg)
            self.rate.sleep()
            if (self.checkpoint()): 
                if(self.num_goals==6):
                    vel_msg.linear.x = 0
                    vel_msg.linear.y = 0
                    self.velocity_publisher.publish(vel_msg)
                    return
                self.update_goal_pose()	
                vel_msg = self.find_vel()		


if __name__ == '__main__':
	try:
		x = TurtleBot()
		x.move()
	except rospy.ROSInterruptException:
		pass
        