#! /usr/bin/env python

# import ros stuff

import time as time
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf import transformations

import math

pub_ = None
regiones_ = {
    'derecha': 0,
    'f_derecha': 0,
    'frente': 0,
    'f_izquierda': 0,
    'izquierda': 0,
}

estado_ = 0

tipos_estado_ = {
    0: 'encontrar_pared',
    1: 'doblar_izquierda',
    2: 'seguir_pared',
    3: 'doblar_derecha',
}

def clbk_laser(msg):
    global regiones_
    regiones_ = {
            #'R1': min(min(msg.ranges[0:59]),1),
            #'R2': min(min(msg.ranges[60:119]),1),
            #'R3': min(min(msg.ranges[120:179]),1),
            'derecha': min(min(msg.ranges[180:251]),1),
            'f_derecha': min(min(msg.ranges[252:323]),1),
            'frente': min(min(msg.ranges[324:395]),1),
            'f_izquierda': min(min(msg.ranges[396:467]),1),
            'izquierda': min(min(msg.ranges[468:540]),1),
            #'R9': min(min(msg.ranges[540:612]),1),
            #'R10': min(min(msg.ranges[540:599]),1),
            #'R11': min(min(msg.ranges[600:659]),1),
            #'R12': min(min(msg.ranges[660:719]),1),
    }
    
    acciones()


def cambiar_estado(estado):
    global estado_, tipos_estado_
    if estado is not estado_:
        print ('Seguidor de pared - [%s] - %s' % (estado, tipos_estado_[estado]))
        estado_ = estado


def acciones():
    global regiones_
    regiones = regiones_
    msg = Twist()
    linear_x = 0
    angular_z = 0
    
    descripcion_estado = ''
    
    d = 0.6
    
    if regiones['frente'] > d and regiones['f_izquierda'] > d and regiones['f_derecha'] > (d) and regiones['derecha'] > d:
        descripcion_estado = 'case 1 - nada'
        cambiar_estado(0)
    elif regiones['frente'] < d and regiones['f_izquierda'] > d and regiones['f_derecha'] > d:
        descripcion_estado = 'case 2 - frente'
        cambiar_estado(1)
    elif regiones['frente'] > d and regiones['f_izquierda'] > d and regiones['f_derecha'] < d:
        descripcion_estado = 'case 3 - frente derecha'
        cambiar_estado(2)
    elif regiones['frente'] > d and regiones['f_izquierda'] < d and regiones['f_derecha'] > d:
        descripcion_estado = 'case 4 - frente izquierda'
        cambiar_estado(0)
    elif regiones['frente'] < d and regiones['f_izquierda'] > d and regiones['f_derecha'] < d:
        descripcion_estado = 'case 5 - frente y frente derecha'
        cambiar_estado(1)
    elif regiones['frente'] < d and regiones['f_izquierda'] < d and regiones['f_derecha'] > d:
        descripcion_estado = 'case 6 - frente y frente izquierda'
        cambiar_estado(1)
    elif regiones['frente'] < d and regiones['f_izquierda'] < d and regiones['f_derecha'] < d:
        descripcion_estado = 'case 7 - frente , frente izquierda y frente derecha'
        cambiar_estado(1)
    elif regiones['frente'] > d and regiones['f_izquierda'] < d and regiones['f_derecha'] < d:
        descripcion_estado = 'case 8 - frente izquierda y frente derecha'
        cambiar_estado(0)
    else:
        descripcion_estado = 'caso desconocido'
        rospy.loginfo(descripcion_estado)



def encontrar_pared():
    msg = Twist()
    seguir_pared()
    time.sleep(1.2)
    msg.linear.x = 0
    msg.angular.z = -0.2
    return msg

def doblar_izquierda():
    msg = Twist()
    msg.angular.z = 0.2
    return msg

def doblar_derecha():
    msg = Twist()
    msg.linear.x = 0.2
    msg.angular.z = -0.2
    return msg

def seguir_pared():
    global regiones_

    msg = Twist()
    msg.linear.x = 0.2
    return msg


def main():
    global pub_

    rospy.init_node('leyendo_laser')

    pub_ = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

    sub = rospy.Subscriber('/scan', LaserScan, clbk_laser)

    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        msg = Twist()
        if estado_ == 0:
            msg = encontrar_pared()
        elif estado_ == 1:
            msg = doblar_izquierda()
        elif estado_ == 2:
            msg = seguir_pared()
            pass
        elif estado_ == 3:
            msg = doblar_derecha()
            pass
        else:
            rospy.logerr('Estado desconocido!')

        pub_.publish(msg)

        rate.sleep()

if __name__ == '__main__':
    main()
