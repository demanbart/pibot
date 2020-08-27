import pygame
import time
import sys
import pololu_drv8835_rpi

#controllers

class Controller:
    """this is the base class for controllers"""
    windowSize = (720,540)
    maxAxesLenght = 1000
    colorpallet = {
            "white": pygame.Color(255,255,255),
            "grey": pygame.Color(100,100,100),
            "red": pygame.Color(255,0,0)
        }
    
    def __init__(self):
        pass

    
    def __del__(self):
        if pygame.get_init():
            pygame.quit()

    def __str__(self):
        print(self.__dict__())

    def control(self):
        """should be a generator which return a dictionary containing all values to send to the robot"""
        pass

    def directionalGauge(self, direction):
        """ creates a directionindicator, needs tuple (x,y) as coördinates"""
        pygame.draw.circle(self.windowSurface,self.colorpallet["grey"] , (55, 55), 55)
        pygame.draw.circle(self.windowSurface, self.colorpallet["red"], (int(direction[0]/20)+55, int(-direction[1]/20)+55), 10)

    def drawController(self, directionalGauge = [0, 0]):
        if not pygame.get_init():
            pygame.init()
            pygame.display.set_mode(self.windowSize)
            self.windowSurface = pygame.display.get_surface()
        self.windowSurface.fill(self.colorpallet["white"])
        if(directionalGauge):
            self.directionalGauge(directionalGauge)
        pygame.display.update()
        
class FpsController(Controller):
    """this controller is using the keyboard and mouse fps style"""    
    def __init__(self):
        self.drawController()
        pygame.event.set_blocked(None)
        pygame.event.set_allowed([pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT])
        
    def control(self):
        while True:
            if pygame.event.peek():
                event = pygame.event.poll()
                if event.type == pygame.QUIT:
                        print("You quit")
                        pygame.quit()
                        sys.exit()
                if event.type in [2,3]:
                    pressedKeys = pygame.key.get_pressed()
                    pressed_keys = [i for i,v in enumerate(pressedKeys) if v==1 if i in [97, 100, 115, 119]]
                    if pressed_keys == [119]:
                        #forward
                        x, y = 0, self.maxAxesLenght
                    elif pressed_keys == [100,119]:
                        #forward right
                        x, y = self.maxAxesLenght, self.maxAxesLenght
                    elif pressed_keys == [100]:
                        #right
                        x, y = self.maxAxesLenght, 0
                    elif pressed_keys == [100, 115]:
                        #backward right
                        x, y = self.maxAxesLenght, -self.maxAxesLenght
                    elif pressed_keys == [115]:
                        #backward
                        x, y = 0, -self.maxAxesLenght
                    elif pressed_keys == [97, 115]:
                        #backward left
                        x, y = -self.maxAxesLenght, -self.maxAxesLenght
                    elif pressed_keys == [97]:
                        #left
                        x, y = -self.maxAxesLenght, 0
                    elif pressed_keys == [97, 119]:
                        #forward left
                        x, y = -self.maxAxesLenght, self.maxAxesLenght
                    else:
                        x, y = 0, 0
                        
                    self.drawController(directionalGauge = [x,y])

                    yield({"zdsq":{"x": x, "y": y}})

#command
class Command:
    driveVector = None
    
    def __init__(driveVector):
        self.driveVector = driveVector

    def __str__(self):
        print(self.__dict__())

#communication
class Communicator:
    name = "Communicator"

    def __str__(self):
        print(self.__dict__())
    
class TcpIpCommunicator(Communicator):
    host = None
    sendPort = None
    receivePort = None
    
    def __init__(self, host, port = 50100):
        self.host = host
        self.port = port
        
    def __str__():
        print(self.__dict__())
        
    def send(self, command):
        pass

    def receive(self):
        pass

class NRF24L01Communicator(Communicator):
    def send():
        pass

    def receive():
        pass

class MotorDriver:
    __driverName = ""
    __driverUrl = ""
    __driverBrand = ""
    __driverDescription = ""
    __commandStructure = ""
    
    def __str__():
        print(self.__dict__())

    def __validate_command_structure(self, command, commandstructure):
        return True

class DRV8835MotorDriver(MotorDriver):
    def __init__(self):
         self.__driverName = "DRV8835"
         self.__driverBrand = "Pololu"
         self.__driverDescription = "Dual motor driver kit for Raspberry Pi B+, DRV8835 dual H-bridge motor driver IC, Continuous output current per channel: 1.2A, PWM frequency: 250 kHz (maximum) ,The DRV8835 Dual Motor Driver Kit for Raspberry Pi B+ provides an easy and low-cost solution for driving a pair of small brushed DC motors with a Raspberry Pi Model B+. The expansion board features Texas Instruments' DRV8835 dual H-bridge motor driver IC."
         self.__driverUrl = "https://www.pololu.com/product/2753"
         self.__commandStructure = {"motor1": "int:0-248", "motor2": "int:0-248"}

         print(self.__dict__())
    
    def execute(command):
        #check if given command complies with the commandstructure before sending"
        if self.__validate_command_structure(command, self.__commandStructure):
            pololu_drv8835_rpi.motors.SetSpeeds(command["motor1"], command["motor2"])
         
