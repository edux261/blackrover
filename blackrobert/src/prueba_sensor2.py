#! /usr/bin/env python

import rospy

from sensor_msgs.msg import LaserScan

def clbk_laser(msg):

    # cada region corresponde a 45 grados
    regiones = {
        'derecha':  min(min(msg.ranges[270:314]),1),
        'derecha_adelante': min(min(msg.ranges[315:360]),1),
        'izquierda':  min(min(msg.ranges[45:89]),1),
        'izquierda_adelante':   min(min(msg.ranges[0:44]),1),
    }
    rospy.loginfo(regiones)
def main():
    rospy.init_node('reading_laser')

    sub = rospy.Subscriber('/scan', LaserScan, clbk_laser)
    rospy.spin()

if __name__ == '__main__':
    main()

