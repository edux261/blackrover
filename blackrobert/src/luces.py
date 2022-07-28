#! /usr/bin/env python

import RPi.GPIO as GPIO
import time
## CONFIG BASICA ##
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
## LED
GPIO.setup(8, GPIO.OUT)

## BOTON
GPIO.setup(3, GPIO.IN,pull_up_down=GPIO.PUD_UP)

if __name__ == '__main__':
    while True:
        Boton1 = GPIO.input(3)
        GPIO.output(8, GPIO.HIGH)
        if Boton1 == False:
            GPIO.output(40, GPIO.LOW)

