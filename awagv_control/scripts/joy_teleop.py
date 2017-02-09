#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist

class Joy2Twist:
    def __init__(self):

        rospy.init_node('Joy2Twist', anonymous=False)
        rospy.on_shutdown(self.shutdown)
        self.sub = rospy.Subscriber('joy', Joy, self.joy_handler, queue_size=1)
        self.pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)

        rate = rospy.Rate(rospy.get_param('~rate', 20))

        self.joy = Joy()
        self.joy_flag = False
        svoff_flag = False
        svon_flag = False

        while not self.joy_flag:
            rate.sleep()

        while not rospy.is_shutdown():
            button_state=False
            vel = Twist()
            vel.linear.x = self.joy.axes[1] * (0.35 + 0.35 * self.joy.buttons[11])
            vel.angular.z = self.joy.axes[0] * (0.35 + 0.35 * self.joy.buttons[11])
#            vel.linear.x = self.joy.axes[1] * (0.35 * self.joy.buttons[12])
#            vel.angular.z = self.joy.axes[0] * (0.35 * self.joy.buttons[12])

            self.pub.publish(vel)
            button_state=True

            rate.sleep()

    def joy_handler(self, joy_msg):
        self.joy = joy_msg
        self.joy_flag = True

    def shutdown(self):
        pass

if __name__ == '__main__':
    try:
        manager = Joy2Twist()
    except rospy.ROSInterruptException:
            pass
