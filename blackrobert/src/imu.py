
import time
import board
import adafruit_bno055


i2c = board.I2C()
sensor = adafruit_bno055.BNO055_I2C(i2c)

last_val = 0xFFFF

# no debemos indicar pines de entrada, ya que las librerias los detectan por si solos


def temperature():
    global last_val  
    result = sensor.temperature
    if abs(result - last_val) == 128:
        result = sensor.temperature
        if abs(result - last_val) == 128:
            return 0b00111111 & result
    last_val = result
    return result


while True:

    print("Accelerometro (m/s^2): {}".format(sensor.acceleration))
    print("Magnetometro (microteslas): {}".format(sensor.magnetic))
    print("Gyroscopio (rad/sec): {}".format(sensor.gyro))
    print("Euler angle: {}".format(sensor.euler))
    print("Quaternion: {}".format(sensor.quaternion))
    print("Aceleracion lineal (m/s^2): {}".format(sensor.linear_acceleration))
    print("Gravedad (m/s^2): {}".format(sensor.gravity))
    print()

    time.sleep(1)
