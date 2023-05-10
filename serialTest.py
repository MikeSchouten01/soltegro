import serial
import time
ser = serial.Serial()
ser.port = '/dev/ttyAMA0'
ser.baudrate = 9600
ser.timeout = 60  # 1 min
ser.open()

msg = ''
counter = 0
while True:
    ser.write("Test")
    x=ser.readline()
    print(x)
    time.sleep(1)
    counter += 1