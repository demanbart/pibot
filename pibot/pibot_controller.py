import pygame
import time

class PiBotController:
    """this is the base class for controllers"""
    controllerState = None
    previousControllerState = None
    vectors = dict()
    maxAxesLenght = 10000
    
    def __init__(self):
        pass

    def __set_controls(self):
        pass

    def read(self):
        pass
    
    def get_current_controller_state(self):
        self.previousControllerState = self.controllerState
        self.controllerState = self.read()
        print("hello")
        return self.controllerState
    
class fps(PiBotController):
    """this controller is using the keyboard and mouse fps style"""
    def __init__(self):
        pygame.init()
        width = 720
        height = 540
        windowSurface = pygame.display.set_mode((width, height), 0, 32)
        pygame.event.set_blocked(None)
        pygame.event.set_allowed([pygame.KEYDOWN, pygame.KEYUP])
        self.vectors=[{"x":0,"y":0}]
        directionIndex = 0

    def __del__(self):
        pygame.quit()

    def control(self):
        while True:
            if pygame.event.peek():
                event = pygame.event.poll()
                if event.type in [2,3]:
                    pressed_keys = [i for i,v in enumerate(pygame.key.get_pressed()) if v and i in [119,100,115,97]].sort()
                    print(pressed_keys)
                    
                    if pressed_keys == [119]:
                        #forward
                        x, y = 0, maxAxesLenght
                    elif pressed_keys == [100,119]:
                        #forward right
                        x, y = maxAxesLenght, maxAxesLenght
                    elif pressed_keys == [100]:
                        #right
                        x, y = maxAxesLenght, 0
                    elif pressed_keys == [100, 115]:
                        #backward right
                        x, y = 0, -maxAxesLenght
                    elif pressed_keys == [115]:
                        #backward
                        x, y = -maxAxesLenght, 0
                    elif pressed_keys == [97, 115]:
                        #backward left
                        x, y = -maxAxesLenght, maxAxesLenght
                    elif pressed_keys == [97]:
                        #left
                        x, y = 0, maxAxesLenght
                    elif pressed_keys == [97]:
                        #forward left
                        x, y = 0, maxAxesLenght
                    else:
                        x, y = 0, 0
                                                
#controller to receive signals
controller = fps()
controller.control()
#to the motor
    
