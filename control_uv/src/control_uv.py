#! /usr/bin/env python
import rospy
from std_msgs.msg import String
import RPi.GPIO as GPIO
import time
#---------------------------------------------------------
GPIO.setmode(GPIO.BOARD)
pin = 8
GPIO.setup(pin, GPIO.OUT)
#---------------------------------------------------------

def main():
    rospy.Subscriber('/encendido', String, queue_size=10)
    rospy.init_node('luz_uv')
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        encendido = 1  #mensaje de otro nodo
        if encendido == 1:
            GPIO.output(pin, GPIO.HIGH)
        if encendido == 0:
            GPIO.output(pin, GPIO.LOW)
            
            

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        GPIO.cleanup()
        pass









