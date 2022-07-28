#! /usr/bin/env python

import rospy

from sensor_msgs.msg import LaserScan

def clbk_laser(msg):

    # cada region corresponde a 45 grados
    """
    regiones = {
        'derecha':  min(min(msg.ranges[270:314]),1),
        'derecha_adelante': min(min(msg.ranges[315:360]),1),
        'izquierda adelante':  min(min(msg.ranges[361:406]),1),
        'izquierda':   min(min(msg.ranges[407:452]),1),
    }
    """
    regiones = {
        #'R1': min(min(msg.ranges[0:59]),1),
        #'R2': min(min(msg.ranges[60:119]),1),
        #'R3': min(min(msg.ranges[120:179]),1),
        'derecha': min(min(msg.ranges[180:251]),1),
        'derecha_adelante': min(min(msg.ranges[252:323]),1),
        'frente': min(min(msg.ranges[324:395]),1),
        'izquierda_adelante': min(min(msg.ranges[396:467]),1),
        'izquierda': min(min(msg.ranges[468:540]),1),
        #'R9': min(min(msg.ranges[540:612]),1),
	#'R10': min(min(msg.ranges[540:599]),1),
	#'R11': min(min(msg.ranges[600:659]),1),
	#'R12': min(min(msg.ranges[660:719]),1),
 }
    
    rospy.loginfo(regiones)
def main():
    rospy.init_node('reading_laser')

    sub = rospy.Subscriber('/scan', LaserScan, clbk_laser)
    rospy.spin()

if __name__ == '__main__':
    main()

