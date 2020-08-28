import pibot.control.fps as mycontroller
import pygame

controller = mycontroller.Fps()

for command in controller.control():
    print(command)
    #zdsq to drive motor 1 and motor 2
    x = command["zdsq"]["x"]
    y = command["zdsq"]["y"]
    
    if x > 0:
        m1 = y
        m2 = int((y - abs(x))*480/1000)
    else:
        m2 = y
        m1 = int((y - abs(x))*480/1000)
        
   # motorset.execute({"motor1": m1, "motor2": m2})

    
