#para montar el server
from http.server import BaseHTTPRequestHandler, HTTPServer
import random
#para controlar la consola
import os
import sys
import subprocess
#para controlar los pines de la RPI
import RPi.GPIO as GPIO
import time

#setea el pin del rele
GPIO.setmode(GPIO.BOARD)
pin = 8
GPIO.setup(pin, GPIO.OUT)

Request = None

class RequestHandler_httpd(BaseHTTPRequestHandler):
  def do_GET(self):
    global Request
    Request = self.requestline
    Request = Request[5 : int(len(Request)-9)]
    
    
#para comprobar conexion
    if Request == 'datos/0':#si es cero, refleja un "0" en la consola
      messagetosend = bytes('AKN0',"utf")
      self.send_response(200)
      self.send_header('Content-Type', 'text/plain')
      self.send_header('Content-Length', len(messagetosend))
      self.end_headers()
      self.wfile.write(messagetosend)
      print('cero') 
    if Request == 'datos/1':#si es "1" refleja un 1 en la consola
      messagetosend = bytes('AKN1',"utf")
      self.send_response(200)
      self.send_header('Content-Type', 'text/plain')
      self.send_header('Content-Length', len(messagetosend))
      self.end_headers()
      self.wfile.write(messagetosend)
      print('uno')
    if Request == 'datos/random':#envia un numero random a la consola y a la app. este numero debe ser el mismo en ambas cada vez
      messagetosend = bytes((str((random.randint(1, 100)))),"utf")
      self.send_response(200)
      self.send_header('Content-Type', 'text/plain')
      self.send_header('Content-Length', len(messagetosend))
      self.end_headers()
      self.wfile.write(messagetosend)
      print('dato enviado')
      
      
#parte para controlar el teleop
    if Request == 'teleop/iniciar':#activa el teleop, se envia al seleccionar ese modo en la pantalla principal
      messagetosend = bytes('AKN_INIT_TELEOP',"utf")
      self.send_response(200)
      self.send_header('Content-Type', 'text/plain')
      self.send_header('Content-Length', len(messagetosend))
      self.end_headers()
      self.wfile.write(messagetosend)
      print('iniciando teleop')
      print(subprocess.Popen("/home/pi/Desktop/teleop.sh", stdin=True))
    if Request == '3':#para avanzar
      messagetosend = bytes('AKN_MOV',"utf")
      self.send_response(200)
      self.send_header('Content-Type', 'text/plain')
      self.send_header('Content-Length', len(messagetosend))
      self.end_headers()
      self.wfile.write(messagetosend)
      print('avanzar')
      print(os.system("i"))
    if Request == '4':#para retroceder
      messagetosend = bytes('AKN_MOV',"utf")
      self.send_response(200)
      self.send_header('Content-Type', 'text/plain')
      self.send_header('Content-Length', len(messagetosend))
      self.end_headers()
      self.wfile.write(messagetosend)
      print('retroceder')
      #print(os.system("/home/pi/Desktop/teleop.sh"))
    if Request == '5':#para detenerse
      messagetosend = bytes('AKN_MOV',"utf")
      self.send_response(200)
      self.send_header('Content-Type', 'text/plain')
      self.send_header('Content-Length', len(messagetosend))
      self.end_headers()
      self.wfile.write(messagetosend)
      print('detener')
      print(os.system("k"))
    if Request == '6':#para girar a la derecha
      messagetosend = bytes('AKN_MOV',"utf")
      self.send_response(200)
      self.send_header('Content-Type', 'text/plain')
      self.send_header('Content-Length', len(messagetosend))
      self.end_headers()
      self.wfile.write(messagetosend)
      print('derecha')
      #print(os.system("/home/pi/Desktop/teleop.sh"))
    if Request == '7':#para girar a la izquierda
      messagetosend = bytes('AKN_MOV',"utf")
      self.send_response(200)
      self.send_header('Content-Type', 'text/plain')
      self.send_header('Content-Length', len(messagetosend))
      self.end_headers()
      self.wfile.write(messagetosend)
      print('izquierda')
      #print(os.system("/home/pi/Desktop/teleop.sh"))
      
      
#parte para controlar el seguidor de pared
    #activar el seguidor
    if Request == 'seguidor/iniciar':
      messagetosend = bytes('AKN_SGP',"utf")
      self.send_response(200)
      self.send_header('Content-Type', 'text/plain')
      self.send_header('Content-Length', len(messagetosend))
      self.end_headers()
      self.wfile.write(messagetosend)
      print('iniciar seguidor de pared')
      print(subprocess.Popen("/home/pi/Desktop/seguidor_pared.sh", stdin=True))
    #detener el seguidor
    if Request == 'seguidor/detener':
      messagetosend = bytes('AKN_SGP_STOP',"utf")
      self.send_response(200)
      self.send_header('Content-Type', 'text/plain')
      self.send_header('Content-Length', len(messagetosend))
      self.end_headers()
      self.wfile.write(messagetosend)
      print('deteniendo el modo de seguidor de pared')
      #print(os.system("^C"))
      
#parte para controlar la luz uv a traves del rele
    #encender la luz
    if Request == 'luz/on':
      messagetosend = bytes('AKN_MOV',"utf")
      self.send_response(200)
      self.send_header('Content-Type', 'text/plain')
      self.send_header('Content-Length', len(messagetosend))
      self.end_headers()
      self.wfile.write(messagetosend)
      print('cambiar_rele')
      GPIO.output(pin, GPIO.HIGH)
      print("rele encendido")
    #apagar la luz
    if Request == 'luz/off':
      messagetosend = bytes('AKN_MOV',"utf")
      self.send_response(200)
      self.send_header('Content-Type', 'text/plain')
      self.send_header('Content-Length', len(messagetosend))
      self.end_headers()
      self.wfile.write(messagetosend)
      print('cambiar_rele')
      GPIO.output(pin, GPIO.LOW)
      print("rele apagado")

    return


server_address_httpd = ('192.168.0.15',8080)
httpd = HTTPServer(server_address_httpd, RequestHandler_httpd)
print('iniciando server')
httpd.serve_forever()
