import serial

if __name__ == '__main__':
    ser = serial.Serial(port = "/dev/ttyS0",baudrate = 9600,parity = serial.PARITY_NONE,stopbits = serial.STOPBITS_ONE,bytesize = serial.EIGHTBITS,timeout = 1)  

    try:
        while True:
            line = ser.readline()
            print(line)
    except KeyboardInterrupt:
        pass # do cleanup here