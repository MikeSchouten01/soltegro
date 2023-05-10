import serial

if __name__ == '__main__':
    test=serial.Serial("/dev/ttyAMA0",9600)
    # test.open()

    try:
        while True:
            line = test.readline()
            print(line)
    except KeyboardInterrupt:
        pass # do cleanup here