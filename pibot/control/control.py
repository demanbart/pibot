import pygame
import time
import sys

class Controller:
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
    
    def __init__(self):
        pass

    
    def __del__(self):
        if pygame.get_init():
            pygame.quit()
            sys.exit()

    def __str__(self):
        print(self.__dict__())

    def control(self):
        """should be a generator which return a dictionary containing all values to send to the robot"""
        pass

    def drawDirectionalGauge(self, direction):
        """ creates a directionindicator, needs tuple (x,y) as coördinates"""
        pass

    def drawCameraView(self):
	    pygame.draw.circle(self.windowSurface,self.colorpallet["tranparant"] , self.windowCenter, 110, 5)
	    pygame.draw.rect(self.windowSurface, self.colorpallet["tranparant"], [(0,int(self.windowSize[1]/2)-50),(self.windowSize[0],int(self.windowSize[1]/2)+50)], 5)

    def decorateMouse(self):
        pygame.mouse.set_cursor(*pygame.cursors.broken_x)

    def drawController(self, directionalGauge = [0, 0]):
        if not pygame.get_init():
            pygame.init()
            pygame.display.set_mode(self.windowSize)
            self.windowSurface = pygame.display.get_surface()
        self.windowSurface.fill(self.colorpallet["white"])
        if(directionalGauge):
            self.drawDirectionalGauge(directionalGauge)
        self.drawCameraView()
        self.decorateMouse()
        pygame.display.update()
