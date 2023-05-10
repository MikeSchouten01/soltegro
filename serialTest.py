import serial
import time
ser = serial.Serial()
ser.port = '/dev/ttyS0'
ser.baudrate = 9600
ser.timeout = 60  # 1 min
ser.open()

msg = 'test'
counter = 0
while True:
    x = ser.readline()
    print(type(x))
