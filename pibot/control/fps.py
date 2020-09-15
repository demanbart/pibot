import pibot.control.control
import pygame
import pickle
import socket
import struct
import cv2

class Fps(pibot.control.control.Controller):
    """this controller is using the keyboard and mouse fps style"""    
    def __init__(self, cameraServer=None, cameraPort=None):
        self.drawController()
        pygame.event.set_blocked(None)
        pygame.event.set_allowed([pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT, pygame.MOUSEMOTION])
        self.cameraServer = cameraServer
        self.cameraPort = cameraPort
        self.cameraConnection = None

    def openCameraConnection():
        if not self.cameraConnection:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print('Socket created')

            s.bind((HOST, PORT))
            print('Socket bind complete')
            s.listen(10)
            print('Socket now listening')
            
        
    def control(self):
        while True:
            if pygame.event.peek():
                event = pygame.event.poll()
                if event.type == pygame.QUIT:
                        print("You quit")
                        pygame.quit()
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
                        
                    self.drawController(directionalGauge = [x*50,y*50])

                    yield({"zdsq":{"x": x, "y": y}})

                elif event.type == pygame.MOUSEMOTION:
                    mousepos = pygame.mouse.get_pos()
                    x = (mousepos[0]-self.windowSize[0]/2)/(self.windowSize[0]/2)
                    y = -(mousepos[1]-self.windowSize[1]/2)/(self.windowSize[1]/2)
                    yield({"mouse":{"x": x, "y": y}})
            
	if(cameraServer):
            
		    
