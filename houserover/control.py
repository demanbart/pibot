import pygame
import pickle
import socket
import time
import struct
import sys
import numpy as np

#the main code
guiWindowSize = (1280,720)
guiColorPallet = {
            "white": pygame.Color(255,255,255),
            "grey": pygame.Color(100,100,100),
            "red": pygame.Color(255,0,0),
            "tranparant": pygame.Color(240,240,240,100)
        }

host = '192.168.0.135'
port = 50101
cameraConnection = None
robotConnection = None

while True:
    command = None
    
    if not pygame.get_init():
        pygame.init()
        guiDisplay = pygame.display.set_mode(guiWindowSize)
        guiWindowSurface = pygame.display.get_surface()
        guiWindowSurface.fill(guiColorPallet["white"])
        x = np.arange(0, 1280)
        y = np.arange(0, 720)
        X, Y = np.meshgrid(x, y)
        Z = X + Y
        Z = 255*Z/Z.max()
        guiImageSurface = pygame.surfarray.make_surface(Z)
        
        pygame.event.set_blocked(None)
        pygame.event.set_allowed([pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT, pygame.MOUSEMOTION])

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
                right = 480
                left = 480
            elif pressed_keys == [100,119]:
                #forward right
                right = 240
                left = 480
            elif pressed_keys == [100]:
                #right
                right = -480
                left = 480
            elif pressed_keys == [100, 115]:
                #backward right
                right = -240
                left = -480
            elif pressed_keys == [115]:
                #backward
                right = -480
                left = -480
            elif pressed_keys == [97, 115]:
                #backward left
                right = -480
                left = -240
            elif pressed_keys == [97]:
                #left
                right = 480
                left = -480
            elif pressed_keys == [97, 119]:
                #forward left
                right = 480
                left = 240
            else:
                right = 0
                left = 0
            command = "{'direction':{'right':"+str(right)+", 'left':"+str(left)+"}}"

        elif event.type == pygame.MOUSEMOTION:
            mousepos = pygame.mouse.get_pos()
            x = int((mousepos[0]/guiWindowSize[0])*180)
            y = int((mousepos[1]/guiWindowSize[1])*180)
            command = {"camera":{"x": x, "y": y}}

    else:
        command = {}
            
    try:
        if not robotConnection:
            robotConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            robotConnection.settimeout(5)
            robotConnection.connect((host, port))
        try:
            print("send command: "+str(command))
            robotConnection.sendall(struct.pack("L",len(command))+bytearray(str(command),"utf-8"))

            #reveive camera image
            data = b''
            payload_size = struct.calcsize("L")
            print("receive camera ")
            # Retrieve message size
            while len(data) < payload_size:
                data += robotConnection.recv(4096)
            
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("L", packed_msg_size)[0] 

            # Retrieve all data based on message size
            while len(data) < msg_size:
                data += robotConnection.recv(4096)

            frame_data = data[:msg_size]
            data = data[msg_size:]

            # Extract frame
            frame = pickle.loads(frame_data)
            guiImageSurface = pygame.transform.rotate(pygame.surfarray.make_surface(frame),180)
        except socket.timeout:
            print("timed out waiting for image")
    except (ConnectionResetError, OSError, ConnectionAbortedError, ConnectionRefusedError):
        print("Connection was reset on robot side")
        robotConnection = None
            
    guiDisplay.blit(guiImageSurface,(0,0))
    pygame.mouse.set_cursor(*pygame.cursors.broken_x)
    pygame.display.update()

    
