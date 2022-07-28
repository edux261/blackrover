#! /usr/bin/env python 

import rospy
import RPi.GPIO as GPIO
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import time
from time import sleep
pub = None


# instrucciones de movimiento :
# doblar a la derecha = angular_z = -1
# doblar a la izquierda = angular_z = 1
# adelante = linear_x = 0.5
# atraz = linear_x = -0.5




GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO_TRIGGER = 4
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)

ECHOS = {"ECHO_LEFT": 17, "ECHO_MIDDLE": 27, "ECHO_RIGHT": 22}
for e in ECHOS:
  GPIO.setup(ECHOS[e], GPIO.IN)

def distance(e):
  new_reading = False
  counter = 0
  GPIO.output(GPIO_TRIGGER, True)
  time.sleep(0.00001)
  GPIO.output(GPIO_TRIGGER, False)

  while GPIO.input(e) == 0:
    pass
    counter += 1
    if counter == 5000:
      new_reading = True
      break
  start_time = time.time()

  if new_reading:
    return False

  while GPIO.input(e) == 1:
    pass
  end_time = time.time()

  time_elapsed = end_time - start_time
  dist = (time_elapsed * 34300) / 2
  return dist

def run_distance():
    sensors = []
    for e in ECHOS:
      dist = distance(ECHOS[e])
      sensors.append("{}: {}".format(e, dist))
      time.sleep(1)
    return sensors

# programa sensores infra-rojos-------------------------------


#GPIO.setmode(GPIO.BOARD) # Set GPIO by numbers 
GPIO.setup(ObstaclePin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
 
def loop():
    while True:
        if (0 == GPIO.input(ObstaclePin)):
        
            print ("14CORE | Obstacle Avoidance Sensor Test \n")
            print (" DETECTED: There is an obstacle ahead")
    
def destroy():
    GPIO.cleanup() # Release resource
 
 # ---------------------------------------------------- sensores infra-rojos

def movimientos():
    msg = Twist()
    linear_x = 0
    angular_z = 0
    descripcion_estado = ''
    utrasonido = run_distance()



    
    if (0 == GPIO.input(ObstaclePin)) :  # detecta con un sensor infra rojo
       descripcion_estado = 'detencion : infra rojo'
       linear_x = 0
       angular_z = 0


    elif () :
       descripcion_estado = 'detencion : sensores ultrasonicos'
       linear_x = 0
       angular_z = 0
    


    rospy.loginfo(descripcion_estado)
    msg.linear.x = linear_x
    msg.angular.z = angular_z
    pub.publish(msg)

    
        
def main():
    global pub
    rospy.init_node('reading_laser')
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    # sub = rospy.Subscriber('/scan', LaserScan, clbk_laser)
    movimientos()
    rospy.spin()

if __name__ == '__main__':
        
        try:
            main()
        except KeyboardInterrupt: # Control C is pressed, the child program destroy will be executed.
            destroy()
        
    
