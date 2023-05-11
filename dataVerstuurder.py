# import socket programming library
import socket
import json
import serial
from _thread import *
import threading
 
print_lock = threading.Lock()

ser = serial.Serial()
ser.port = '/dev/ttyS0'
ser.baudrate = 9600
ser.timeout = 60  # 1 min
ser.open()

# thread function
def receiveData(c):
    data = c.recv(1024)
    if not data:
        print('Bye')
        print_lock.release()
        return
    dataString = data.decode('utf8')
    print('- ' * 20)
    print("Received from TCP socket: ")
    printJson(dataString)
    print_lock.release()
    # connection closed
    c.close()
 
def printJson(input):
    
    jsonData = json.loads(input)
    jsonString = json.dumps(jsonData, indent=4, sort_keys=True)
    print(jsonString)

def checkSerial():
    while True:
        if ser.in_waiting > 0:
            print('- ' * 20)
            print("Received from Serial: ")
            dataString = ser.readline().decode('utf-8')
            printJson(dataString)

def Main():
    start_new_thread(checkSerial, ())
    host = ""
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)
    s.listen(5)
    print("socket is listening")

    while True:
        c, addr = s.accept()
        print_lock.acquire() 
        start_new_thread(receiveData, (c,))
 
if __name__ == '__main__':
    Main()