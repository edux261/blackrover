#! /usr/bin/env python

# import ros stuff

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf import transformations

import math

pub_ = None
regiones_ = {
    'derecha': 0,
    'derecha_adelante': 0,
    'izquierda_adelante': 0,
    'izquierda': 0,
}

estado_ = 0

tipos_estado_ = {
    0: 'encontrar la pared',
    1: 'doblar a la izquierda',
    2: 'seguir la pared',
}

def clbk_laser(msg):
    global regiones_
    regiones_ = {
        'derecha':  min(min(msg.ranges[270:314]),1),
        'derecha_adelante': min(min(msg.ranges[315:360]),1),
        'izquierda':  min(min(msg.ranges[45:89]),1),
        'izquierda_adelante':   min(min(msg.ranges[0:44]),1),
    }
    
    acciones()


def cambiar_estado(estado):
    global estado_, tipos_estado_
    if estado is not estado_:
        print 'Wall follower - [%s] - %s' % (estado, tipos_estado_[estado])
        estado_ = estado


def acciones():
    global regiones_
    regiones = regiones_
    msg = Twist()
    linear_x = 0
    angular_z = 0

    descripcion_estado = ''

    d = 0.6 # distancia maxima a un objeto

    if regiones['derecha_adelante'] > d and regiones['izquierda_adelante'] > d and regiones['derecha'] > d and regiones['izquierda'] > d:
        descripcion_estado = 'case 1 - nada'
        cambiar_estado(0)
    elif regiones['derecha_adelante'] < d and regiones['izquierda_adelante'] < d and regiones['derecha'] > d and regiones['izquierda'] > d:
        descripcion_estado = 'case 2 - frente'
        cambiar_estado(1)
    elif regiones['derecha_adelante'] < d and regiones['izquierda_adelante'] > d and regiones['derecha'] > d and regiones['izquierda'] > d:
        descripcion_estado = 'case 3 - frente derecha'
        cambiar_estado(2)
    elif regiones['derecha_adelante'] > d and regiones['izquierda_adelante'] < d and regiones['derecha'] > d and regiones['izquierda'] > d:
        descripcion_estado = 'case 4 - frente izquierda'
        cambiar_estado(0)
    elif regiones['derecha_adelante'] < d and regiones['izquierda_adelante'] > d and regiones['derecha'] < d and regiones['izquierda'] > d:
        descripcion_estado= 'case 5 - frente y derecha'
        cambiar_estado(1)
    elif regiones['derecha_adelante'] > d and regiones['izquierda_adelante'] < d and regiones['derecha'] > d and regiones['izquierda'] < d:
        descripcion_estado = 'case 6 - frente e izquierda'
        cambiar_estado(1)
    elif regiones['derecha_adelante'] < d and regiones['izquierda_adelante'] < d and regiones['derecha'] < d and regiones['izquierda'] < d:
        descripcion_estado = 'case 7 - todos lados'
        cambiar_estado(1)
    elif regiones['derecha_adelante'] > d and regiones['izquierda_adelante'] > d and regiones['derecha'] < d and regiones['izquierda'] < d:
        descripcion_estado = 'case 8 - izquierda y derecha'
        cambiar_estado(0)
    else:
        descripcion_estado = 'caso desconocido'
        #rospy.loginfo(regiones)
    
    rospy.loginfo(descripcion_estado)



def encontrar_pared():
    msg = Twist()
    msg.linear.x = 0.0
    msg.angular.z = 0.0
    return msg

def doblar_izquierda():
    msg = Twist()
    msg.angular.z = 0.0
    return msg

def seguir_pared():
    global regions_

    msg = Twist()
    msg.linear.x = 0.0
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
        else:
            rospy.logerr('Estado desconocido!')

        pub_.publish(msg)

        rate.sleep()

if __name__ == '__main__':
    main()
