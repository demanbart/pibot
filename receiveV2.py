import numpy as np
import socket
import sys
import pickle
import struct
import ast
import smbus2 as smbus
import picamera
import time

host = '192.168.0.135'
port = 50101

values = [0,0,0,0]

arduinoDeviceBus = 1
arduinoDeviceAddr = 0x04
arduinoBus = smbus.SMBus(self.DEVICE_BUS)

camera = picamera.PiCamera()
camera.resolution = (320, 240)
camera.framerate = 24
time.sleep(2)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST, PORT))
print('Socket bind complete')

s.listen(10)
print('Socket now listening')

connection = None

cap=cv2.VideoCapture(0)

while True:
    try:
        if not connection:
            connection, addr = s.accept()
            
        #receive command
        data = b''
        payload_size = struct.calcsize("L")
        print("receive command")
        # Retrieve message size
        while len(data) < payload_size:
            data += connection.recv(4096)
        
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("L", packed_msg_size)[0]

        # Retrieve all data based on message size
        while len(data) < msg_size:
            data += connection.recv(4096)

        frame_data = data[:msg_size]
        data = data[msg_size:]
        print(data)

        data = ast.literal_eval(bytedata.decode("utf-8"))
        print(data)
        if("motor" in data):
            values[0] = data["motor"]["right"]
            values[1] = data["motor"]["left"]
        elif("camera" in data):
            values[0] = data["camera"]["x"]
            values[1] = data["camera"]["y"]
        #this is how to send the position to the arduino, see /doc/cameramount for arduinocode
        print(values)
        try:
          self.bus.write_block_data(self.DEVICE_ADDR, 0, values)    
        except Exception as e:
          print(e)

        
        print("send image")
        #send frame
        output = np.empty((240, 320, 3), dtype=np.uint8)
        camera.capture(output, 'rgb')
        # Serialize frame
        data = pickle.dumps(output)

        # Send message length first
        message_size = struct.pack("L", len(data))

        # Then data
        connection.sendall(message_size + data)
    except ConnectionResetError:
        print("connection reset by host")
        connection = None
