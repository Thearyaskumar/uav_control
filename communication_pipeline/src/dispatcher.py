#!/usr/bin/env python

from __future__ import division, print_function

import rospy
from geometry_msgs.msg import Twist
from mavros_msgs.msg import ExtendedState

_VELOCITY_COMMAND_LIMIT = 0.09

'''
A python script to practice communicating with PX4 over MAVROS
'''

class Dispatcher():
    ''' Subscribes to ROS messages
    '''
    def __init__(self):

        # subscription objects
        self.velocity_command_sub = rospy.Subscriber("/velocity_command", Twist, self.velocity_command_callback)
        self.extended_state_sub = rospy.Subscriber("/mavros/extended_state", ExtendedState, self.extended_state_callback)

        # publishing objects
        self.local_velocity_setpoint_pub = rospy.Publisher("mavros/setpoint_velocity/cmd_vel_unstamped", Twist, queue_size=1)

        # variable to track if the drone is landed or not
        self.landed = None

    def velocity_command_callback(self, msg):
        ''' Function to be run everytime a message is received on chatter topic
        '''

        vel_cmd_limited = Twist()

	if msg.linear.x > _VELOCITY_COMMAND_LIMIT:
		vel_cmd_limited.linear.x = _VELOCITY_COMMAND_LIMIT
	elif msg.linear.x < -_VELOCITY_COMMAND_LIMIT:
		vel_cmd_limited.linear.x = -_VELOCITY_COMMAND_LIMIT
	else:
		vel_cmd_limited.linear.x = msg.linear.x
	vel_cmd_limited.linear.y = 0
	vel_cmd_limited.linear.z = 0
        self.local_velocity_setpoint_pub.publish(vel_cmd_limited)


    def extended_state_callback(self, msg):
        if msg.landed_state == ExtendedState.LANDED_STATE_UNDEFINED:
            self.landed = None
        elif msg.landed_state == ExtendedState.LANDED_STATE_ON_GROUND:
            self.landed = True
        else:
            self.landed = False

if __name__ == '__main__':
    '''
    This is where the code starts running
    '''
    rospy.init_node('dispatcher')
    d_obj = Dispatcher()
    print("Dispatcher node running")
    rospy.spin()
