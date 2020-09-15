import pygame
import pickle
import socket
import struct
import cv2
import time
import sys

class MyController:
    """this is the base class for controllers"""
    windowSize = (720,540)
    windowCenter = (int(windowSize[0]/2), int(windowSize[1]/2))
    maxAxesLenght = 1000
    colorpallet = {
            "white": pygame.Color(255,255,255),
            "grey": pygame.Color(100,100,100),
            "red": pygame.Color(255,0,0),
            "tranparant": pygame.Color(240,240,240,100)
        }
    cameraServer = None
    cameraPort = None
    cameraConnection = None

    """this controller is using the keyboard and mouse fps style"""    
    def __init__(self, cameraServer=None, cameraPort=None):
        self.cameraServer = 'localhost'
        self.cameraPort = cameraPort
        self.drawController()
        pygame.event.set_blocked(None)
        pygame.event.set_allowed([pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT, pygame.MOUSEMOTION])
        
    def __del__(self):
        if pygame.get_init():
            pygame.quit()
            sys.exit()
            
    def getCameraImage(self):
        data = b'' ### CHANGED
        payload_size = struct.calcsize("L") ### CHANGED
        # Retrieve message size
        while len(data) < payload_size:
            data += self.cameraConnection.recv(4096)
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("L", packed_msg_size)[0] ### CHANGE
        while len(data) < msg_size:
            data += self.cameraConnection.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
        return(frame)
    
    def drawController(self):
        if not pygame.get_init():
            pygame.init()
            pygame.display.set_mode(self.windowSize)
            self.windowSurface = pygame.display.get_surface()
        if not self.cameraConnection and self.cameraServer:
            print("connecting to camera")
            self.cameraConnection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.cameraConnection.connect((self.cameraServer, self.cameraPort))
        if self.cameraConnection:
            print(self.getCameraImage())
        else:
            print("no camera connected")
        self.windowSurface.fill(self.colorpallet["white"])
        pygame.mouse.set_cursor(*pygame.cursors.broken_x)
        pygame.display.update()

    def control(self):
        while True:
            if pygame.event.peek():
                event = pygame.event.poll()
                if event.type == pygame.QUIT:
                        print("You quit")
                        pygame.quit()
                        sys.exit()
                if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
                    pressedKeys = pygame.key.get_pressed()
                    pressed_keys = [i for i,v in enumerate(pressedKeys) if v==1 if i in [97, 100, 115, 119]]
                    if pressed_keys == [119]:
                        #forward
                        x, y = 0, 1
                    elif pressed_keys == [100,119]:
                        #forward right
                        x, y = 1, 1
                    elif pressed_keys == [100]:
                        #right
                        x, y = 1, 0
                    elif pressed_keys == [100, 115]:
                        #backward right
                        x, y = 1, -1
                    elif pressed_keys == [115]:
                        #backward
                        x, y = 0, -1
                    elif pressed_keys == [97, 115]:
                        #backward left
                        x, y = -1, -1
                    elif pressed_keys == [97]:
                        #left
                        x, y = -1, 0
                    elif pressed_keys == [97, 119]:
                        #forward left
                        x, y = -1, 1
                    else:
                        x, y = 0, 0
                        
                    command = {"zdsq":{"x": x, "y": y}}

                elif event.type == pygame.MOUSEMOTION:
                    mousepos = pygame.mouse.get_pos()
                    x = (mousepos[0]-self.windowSize[0]/2)/(self.windowSize[0]/2)
                    y = -(mousepos[1]-self.windowSize[1]/2)/(self.windowSize[1]/2)
                    command = {"mouse":{"x": x, "y": y}}

                self.drawController()
                yield(command)
            
HOST = 'localhost'  # The server's hostname or IP address
PORT = 50101        # The port used by the server
CAMERASTREAMPORT = 8089

controller = MyController(cameraPort=CAMERASTREAMPORT)

for command in controller.control():
    print(command)
    if "zdsq" in command:
        #zdsq to drive motor 1 and motor 2
        x = command["zdsq"]["x"]
        y = command["zdsq"]["y"]

        #straight
        if [x,y] == [0,1]:
            right = 480
            left = 480
        #back
        elif [x,y] == [0,-1]:
            right = -480
            left = -480
        #pivot right
        elif [x,y] == [1,0]:
            right = -480
            left = 480
        #pivot left
        elif [x,y] == [-1,0]:
            right = 480
            left = -480
        #turn right
        elif [x,y] == [1,1]:
            right = 240
            left = 480
    #turn left
        elif [x,y] == [-1,1]:
            right = 480
            left = 240
        #backward left
        elif [x,y] == [-1,-1]:
            right = -480
            left = -240
        #backward right
        elif [x,y] == [1,-1]:
            right = -240
            left = -480
        #stop
        else:
            right = 0
            left = 0

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                command = "{'motor':["+str(right)+", "+str(left)+"]}"
                s.sendall(bytearray(command,"utf-8"))      
        except ConnectionRefusedError:
            print("Could not reach robot")
    elif "mouse" in command:
        x = abs(180-command["mouse"]["x"]*90+90)
        y = abs(180-command["mouse"]["y"]*90+90)
        command = "{'mouse':["+str(int(x))+","+str(int(y))+"]}"
        print(command)
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.sendall(bytearray(command,"utf-8"))
        except ConnectionRefusedError:
            print("Could not reach robot")

    
