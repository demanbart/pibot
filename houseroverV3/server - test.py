import threading
import numpy as np
import socket
import sys
import pickle
import struct
import ast
import time
import cv2
import netifaces as ni

def sendPicture(host):
    print("start sending pictures")
    camera = cv2.VideoCapture(0)
    port = 50101
    print("opening picture connection")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        while True:
            s.listen()
            connection, address = s.accept()
            with connection:
                ret,frame=camera.read()
                data = pickle.dumps(frame)
                message_size = struct.pack("L", len(data))
                connection.sendall(message_size + data)

def handleCommand(host):
    port = 50102
    print("opening command connection")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        while True:
            s.listen()
            connection, address = s.accept()
            with connection:
                data = b''
                payloadSize = struct.calcsize("L")
                while len(data) < payloadSize:
                    data += connection.recv(1024)
                packedMsgSize = data[:payloadSize]
                data = data[payloadSize:]
                msgSize = struct.unpack("L", packedMsgSize)[0]
                while len(data) < msgSize:
                    data += connection.recv(1024)
                data = ast.literal_eval(data.decode("utf-8"))

                values = [
                        sorted([0, data[0], 80])[1],
                        sorted([0, data[1], 80])[1],
                        sorted([10, data[2], 170])[1],
                        sorted([10, data[3], 170])[1]
                    ]
                
                try:
                    print(values)    
                except Exception as e:
                    print(e)

host = 'localhost'
print("starting houserover server")
picturesender = threading.Thread(target=sendPicture, args=(host,), daemon = True)
picturesender.start()
commandhandler = threading.Thread(target=handleCommand, args=(host,), daemon = True)
commandhandler.start()
while True:
    time.sleep(5)

