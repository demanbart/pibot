import threading
import numpy as np
import socket
import sys
import pickle
import struct
import ast
import smbus2 as smbus
import picamera
import time
import nifaces as ni

def sendPicture(host):
    print("start sending pictures")
    camera = picamera.PiCamera()
    camera.framerate = 40
    camera.resolution = (240,352)
    camera.rotation = 180
    camera.start_preview()
    camera.vflip = True
    camera.hflip = False
    time.sleep(2)
    port = 50101
    print("opening picture connection")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        while True:
            try:
                s.listen()
                connection, address = s.accept()
                with connection:
                    output = np.empty((352, 240, 3), dtype=np.uint8)
                    camera.capture(output, use_video_port=True, format='rgb')
                    data = pickle.dumps(output)
                    message_size = struct.pack("L", len(data))
                    connection.sendall(message_size + data)
            except ConnectionResetError as e:
                print("connection reset by client")
            finally:
                if connection:
                    connection.close()

def handleCommand(host):
    port = 50102
    arduinoDeviceBus = 1
    arduinoDeviceAddr = 0x04
    arduinoBus = smbus.SMBus(arduinoDeviceBus)
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
                    arduinoBus.write_block_data(arduinoDeviceAddr, 0, values)    
                except Exception as e:
                    print(e)

host = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
print("starting houserover server")
picturesender = threading.Thread(target=sendPicture, args=(host,), daemon = True)
picturesender.start()
commandhandler = threading.Thread(target=handleCommand, args=(host,), daemon = True)
commandhandler.start()
while True:
    time.sleep(5)

