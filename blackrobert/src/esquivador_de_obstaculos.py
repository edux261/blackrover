#!/usr/bin/env python 

import rospy

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
pub = None


# instrucciones de movimiento :
# doblar a la derecha = angular_z = -1
# doblar a la izquierda = angular_z = 1
# adelante = linear_x = 0.5
# atraz = linear_x = -0.5

'''def clbk_laser(msg):
    
    # 720 / 5 = 144
    regiones = {
        'R1': min(min(msg.ranges[0:44]),1),
        'R2': min(min(msg.ranges[45:89]),1),
        'R3': min(min(msg.ranges[90:134]),1),
      #  'R4': min(min(msg.ranges[135:179]),1),
      #  'R5': min(min(msg.ranges[180:224]),1),
        'R6': min(min(msg.ranges[225:269]),1),
        'R7': min(min(msg.ranges[270:314]),1),
        'R8': min(min(msg.ranges[315:360]),1),
    }
    rospy.loginfo(regiones)
    movimientos(regiones)



def movimientos(regiones):
    msg = Twist()
    linear_x = 0
    angular_z = 0
    descripcion_estado = ''

    # pared a la derecha
    if (regiones['R1'] >= 0.5)  and (regiones['R2'] >= 0.5) and (regiones['R3'] >= 0.5)  and (regiones['R6'] < 0.5) and (regiones['R7'] < 0.5) and (regiones['R8'] > 0.4) :
       descripcion_estado = 'caso 1 - pared a la derecha'
       linear_x = 0.5
       angular_z = 0

    # pared adelante y a la izquierda   
    # pared adelante y a la izquierda   
    elif (regiones['R1'] <= 1)  and (regiones['R2'] > 0.5) and (regiones['R3'] > 0.5)  and (regiones['R6'] <= 0.55) and (regiones['R7'] <= 0.55) and (regiones['R8'] <=0.7 ) :
       descripcion_estado = 'caso 2 - pared a la derecha y adelante'
       linear_x = 0
       angular_z = 1.0
    


    rospy.loginfo(descripcion_estado)
    msg.linear.x = linear_x
    msg.angular.z = angular_z
    pub.publish(msg)

    
        
def main():
    global pub
    rospy.init_node('reading_laser')
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    sub = rospy.Subscriber('/scan', LaserScan, clbk_laser)
    rospy.spin()

if __name__ == '__main__':
    main()
'''


















def clbk_laser(msg):
    regions = {
        'right':  min(min(msg.ranges[0:143]), 10),
        'fright': min(min(msg.ranges[144:287]), 10),
        'front':  min(min(msg.ranges[288:431]), 10),
        'fleft':  min(min(msg.ranges[432:575]), 10),
        'left':   min(min(msg.ranges[576:713]), 10),
    }

    take_action(regions)


def take_action(regions):
    msg = Twist()
    linear_x = 0
    angular_z = 0

    state_description = ''

    if regions['front'] > 1 and regions['fleft'] > 1 and regions['fright'] > 1:
        state_description = 'case 1 - nothing'
        linear_x = 0.6
        angular_z = 0
    elif regions['front'] < 1 and regions['fleft'] > 1 and regions['fright'] > 1:
        state_description = 'case 2 - front'
        linear_x = 0
        angular_z = -0.3
    elif regions['front'] > 1 and regions['fleft'] > 1 and regions['fright'] < 1:
        state_description = 'case 3 - fright'
        linear_x = 0
        angular_z = -0.3
    elif regions['front'] > 1 and regions['fleft'] < 1 and regions['fright'] > 1:
        state_description = 'case 4 - fleft'
        linear_x = 0
        angular_z = 0.3
    elif regions['front'] < 1 and regions['fleft'] > 1 and regions['fright'] < 1:
        state_description = 'case 5 - front and fright'
        linear_x = 0
        angular_z = -0.3
    elif regions['front'] < 1 and regions['fleft'] < 1 and regions['fright'] > 1:
        state_description = 'case 6 - front and fleft'
        linear_x = 0
        angular_z = 0.3
    elif regions['front'] < 1 and regions['fleft'] < 1 and regions['fright'] < 1:
        state_description = 'case 7 - front and fleft and fright'
        linear_x = 0
        angular_z = -0.3
    elif regions['front'] > 1 and regions['fleft'] < 1 and regions['fright'] < 1:
        state_description = 'case 8 - fleft and fright'
        linear_x = 0
        angular_z = -0.3
    else:
        state_description = 'unknown case'
        rospy.loginfo(regions)

    rospy.loginfo(state_description)
    msg.linear.x = linear_x
    msg.angular.z = angular_z
    pub.publish(msg)


def main():
    global pub

    rospy.init_node('reading_laser')

    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

    sub = rospy.Subscriber('/scan', LaserScan, clbk_laser)

    rospy.spin()


if __name__ == '__main__':
    main()







