# import socket programming library
import socket
import json
# import thread module
from _thread import *
import threading
 
print_lock = threading.Lock()
 
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
    print(my_json)
    print('- ' * 20)
    # Load the JSON to a Python list & dump it back out as formatted JSON
    data = json.loads(my_json)
    s = json.dumps(data, indent=4, sort_keys=True)
    print(s)
    print_lock.release()
    # connection closed
    c.close()
 
 
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
 
        # establish connection with client
        c, addr = s.accept()
 
        # lock acquired by client
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])
 
        # Start a new thread and return its identifier
        start_new_thread(threaded, (c,))
    s.close()
 
 
if __name__ == '__main__':
    Main()