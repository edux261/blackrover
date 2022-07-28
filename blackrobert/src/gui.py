#interfaz grafica para los programas y luces 
from Tkinter import *
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(8,GPIO.OUT)
GPIO.output(8,GPIO.HIGH)

global estado_boton
estado_boton = False
def switch():
	global estado_boton
	if estado_boton == False:
		ventana.config(bg="green")
		estado_boton = True
		GPIO.output(8,GPIO.LOW)
	else:
		ventana.config(bg="red")
		estado_boton = False
		GPIO.output(8,GPIO.HIGH)

def programas():
	os.system("roscore")


ventana = Tk()

ventana.geometry("400x300")
ventana.title("Control de BlackRover")
ventana.config(bg="red")
botonLuces = Button(ventana, text="luces",command=switch)
botonLuces.place(x=200,y=200)



ventana.mainloop()
