import serial

ser = serial.Serial()
ser.port = '/dev/ttyAMA0'
ser.baudrate = 9600
ser.timeout = 60  # 1 min
ser.open()

msg = ''
while True:
    char = ser.read(1)  # 1 byte
    msg = msg+char.decode('utf-8')
    if char == b'\r':
        break