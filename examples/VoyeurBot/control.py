import pibot.control.fps as mycontroller
import pygame
import socket

controller = mycontroller.Fps()
HOST = '192.168.0.135'  # The server's hostname or IP address
PORT = 50101        # The port used by the server

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
        print(command)
        x = command["mouse"]["x"]*90+90
        y = command["mouse"]["y"]*90+90
        command = "{'mouse':["+str(int(x))+","+str(int(y))+"]}"
        print(command)
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.sendall(bytearray(command,"utf-8"))
        except ConnectionRefusedError:
            print("Could not reach robot")

    
