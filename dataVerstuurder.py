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
def threaded(c):
    
 
        # data received from client
    data = c.recv(1024)
    if not data:
        print('Bye')
        # lock released on exit
        print_lock.release()
        return
    my_json = data.decode('utf8')
    printJson(my_json)
    print_lock.release()
    # connection closed
    c.close()
 
def printJson(input):
    print('- ' * 20)
    data = json.loads(input)
    s = json.dumps(data, indent=4, sort_keys=True)
    print(s)

def Main():
    host = ""
 
    # reserve a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)
 
    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")
 
    # a forever loop until client wants to exit
    while True:
        if ser.in_waiting > 0:
            print("test")
            x = ser.readline().decode('utf-8')
            printJson(x)
        # establish connection with client
        # c, addr = s.accept()
 
        # # lock acquired by client
        # print_lock.acquire() 
        # # Start a new thread and return its identifier
        # start_new_thread(threaded, (c,))
    s.close()
 
 
if __name__ == '__main__':
    Main()