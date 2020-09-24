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

values = [0,0,90,90]

arduinoDeviceBus = 1
arduinoDeviceAddr = 0x04
arduinoBus = smbus.SMBus(arduinoDeviceBus)

camera = picamera.PiCamera()
camera.framerate = 40
camera.resolution = (240,352)
camera.rotation = 180
camera.start_preview()
camera.vflip = True
camera.hflip = False
time.sleep(2)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

s.bind((host, port))
print('Socket bind complete')

s.listen(10)
print('Socket now listening')

connection = None
try:
    while True:
        try:
            if not connection:
                connection, addr = s.accept()
                
            #receive command
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
            print(data)
            if("direction" in data):
                values[0] = sorted([0, data["direction"]["right"], 70])[1]
                values[1] = sorted([0, data["direction"]["left"], 70])[1]
            elif("camera" in data):
                values[2] = min([175, data["camera"]["x"]])
                values[3] = min([175, data["camera"]["y"]])
            #this is how to send the position to the arduino, see /doc/cameramount for arduinocode
            print(values)
            try:
              arduinoBus.write_block_data(arduinoDeviceAddr, 0, values)    
            except Exception as e:
              print(e)

            
            print("send image")
            #send frame
            output = np.empty((352, 240, 3), dtype=np.uint8)
            camera.capture(output, use_video_port=True, format='rgb')
            # Serialize frame
            data = pickle.dumps(output)

            # Send message length firstz
            message_size = struct.pack("L", len(data))

            # Then data
            connection.sendall(message_size + data)
        except ConnectionResetError:
            print("connection reset by host")
            connection = None
except Exception as e:
    print(e)
finally:
    connection.close()
        






