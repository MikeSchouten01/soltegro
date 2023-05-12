# import socket programming library
import socket
import json
import serial
from _thread import *
import threading
from azure.iot.device import IoTHubDeviceClient
import datetime

connectionString = "HostName=aih-tba-tst.azure-devices.net;DeviceId=iot-toolkit-mschouten;SharedAccessKey=mPNXW6/7nxQzirTT3AWYuZuq8b5c8qQGwXBP2ADYlXY="

device_client = IoTHubDeviceClient.create_from_connection_string(
            connectionString
        )
device_client.connect()

print_lock = threading.Lock()

ser = serial.Serial()
ser.port = '/dev/ttyS0'
ser.baudrate = 9600
ser.timeout = 60  # 1 min
ser.open()

# thread function
def receiveData(c):
    try:
        data = c.recv(1024)
    except:
        print("error in c.recv()")
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

    Timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    TimeStampValue = datetime.datetime.now().replace(microsecond=0).isoformat()+"Z"
    TimeStampValue = TimeStampValue.replace(" ", "T")

    oneBitItems = jsonData["oneBitTags"].items()
    sixteenBitItems = jsonData["sixteenBitTags"].items()
    for oneBitItem in oneBitItems:
        message = {
                "Tag": oneBitItem[0],
                "Timestamp": Timestamp,
                "Value": {
                    "IntegerValue": None,
                    "DoubleValue": None,
                    "BoolValue": oneBitItem[1],
                    "StartOrEnd": None,
                    "BytesValue": None,
                    "Duration": None,
                    "StringValue": None,
                    "TimeStampValue": TimeStampValue,
                    "Type": 4
                }
        }
        for sixteenBitItem in sixteenBitItems:
            message = {
                "Tag": sixteenBitItem[0],
                "Timestamp": Timestamp,
                "Value": {
                    "IntegerValue": sixteenBitItem[1],
                    "DoubleValue": None,
                    "BoolValue": None,
                    "StartOrEnd": None,
                    "BytesValue": None,
                    "Duration": None,
                    "StringValue": None,
                    "TimeStampValue": TimeStampValue,
                    "Type": 2
            }
        }
    jsonString = json.dumps(message, indent=4, sort_keys=True)
    message = json.dumps(message, ensure_ascii=False).encode('utf8')
    print(jsonString)
    device_client.send_message(message)

def checkSerial():
    while True:
        if ser.in_waiting > 0:
            print('- ' * 20)
            print("Received from Serial: ")
            try:
                dataString = ser.readline().decode('utf-8')
            except:
                print("error in ser.readline().decode()")
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