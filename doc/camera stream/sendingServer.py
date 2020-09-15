import cv2
import numpy as np
import socket
import sys
import pickle
import struct

HOST = ''
PORT = 8089

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST, PORT))
print('Socket bind complete')

s.listen(10)
print('Socket now listening')

connection, addr = s.accept()

cap=cv2.VideoCapture(0)

while True:
    if connection.recv(1024) == b'send':
        ret,frame=cap.read()
        # Serialize frame
        data = pickle.dumps(frame)

        # Send message length first
        message_size = struct.pack("L", len(data)) ### CHANGED

        # Then data
        connection.sendall(message_size + data)
