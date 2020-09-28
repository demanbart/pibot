import threading
import socket
import datetime
import queue
import os
import pygame
import struct
import sys
import pickle
import tkinter as tk
import cv2

def getPicture(host, frameQueue):
        port = 50101
        while True:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((host, port))
                    data = b''
                    payload_size = struct.calcsize("L")
                    while len(data) < payload_size:
                        data += s.recv(4096)
                    
                    packed_msg_size = data[:payload_size]
                    data = data[payload_size:]
                    msg_size = struct.unpack("L", packed_msg_size)[0] 
                    while len(data) < msg_size:
                        data += s.recv(4096)

                    frame_data = data[:msg_size]
                    data = data[msg_size:]
                    frame = pickle.loads(frame_data)
                    frameQueue.put(frame)
            except (ConnectionRefusedError, ConnectionResetError) as e:
                print("Could not get picture: " + str(e))

def controller(frameQueue, commandQueue):
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    pygame.event.set_blocked(None)
    pygame.event.set_allowed([pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT, pygame.MOUSEBUTTONUP])
    pygame.mouse.set_visible(True)
    display = pygame.display.set_mode((500,300))
    surface = pygame.display.get_surface()
    displayWidth = surface.get_width()
    displayHeight = surface.get_height()
    
    command = [0,0,90,90]
    frame = None
    previousCommand = [i for i in command]
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
                    right = 78
                    left = 80
                elif pressed_keys == [100,119]:
                    #forward right
                    right = 50
                    left = 80
                elif pressed_keys == [100]:
                    #right
                    right = -80
                    left = 80
                elif pressed_keys == [100, 115]:
                    #backward right
                    right = -50
                    left = -80
                elif pressed_keys == [115]:
                    #backward
                    right = -80
                    left = -80
                elif pressed_keys == [97, 115]:
                    #backward left
                    right = -80
                    left = -50
                elif pressed_keys == [97]:
                    #left
                    right = 80
                    left = -50
                elif pressed_keys == [97, 119]:
                    #forward left
                    right = 80
                    left = 50
                else:
                    right = 0
                    left = 0
                    
                command[0] = right
                command[1] = left

            elif event.type == pygame.MOUSEBUTTONUP:
                if surface.get_rect().collidepoint(pygame.mouse.get_pos()):
                    print(event)
                    if event.button == 1:
                        mousepos = pygame.mouse.get_pos()
                        x = int(abs(180-(mousepos[0]/displayWidth*180)))
                        y = int(mousepos[1]/displayHeight*180)
                        command[2] = x
                        command[3] = y
                    elif event.button == 3:
                        fileName = f"output/{str(datetime.datetime.now()).translate({ord(i): None for i in '-: .'})}.jpg"
                        print(fileName)
                        cv2.imwrite(fileName, frame)

            if (command[0:1] != previousCommand[0:1]
                or abs(command[2]-previousCommand[2]) > 2
                or abs(command[3]-previousCommand[3]) > 2):
                commandQueue.put(command)
                previousCommand = [i for i in command]

        if frameQueue.qsize() > 0:
            frame = frameQueue.get()
            image = pygame.surfarray.make_surface(frame)
            if image.get_width() != displayWidth:
                display = pygame.display.set_mode((image.get_width(), image.get_height()))
                displayWidth = surface.get_width()
                displayHeight = surface.get_height()
            display.blit(image,(0,0))
        pygame.display.update()

def sendCommand(host, commandQueue):
    port = 50102
    while True:
        if commandQueue.qsize() > 0:
            command = commandQueue.get()
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.connect((host, port))
                        s.sendall(struct.pack("L",len(command))+bytearray(str(command),"utf-8"))
            except (ConnectionRefusedError, ConnectionResetError) as e:
                print("Could not send command: " + str(e))

settings = tk.Tk()
tk.Label(settings, text="server name").grid(row=0)
tk.Label(settings, text="server IP").grid(row=1)

serverName = tk.Entry(settings)
serverIP = tk.Entry(settings)

serverName.grid(row=0, column=1)
serverIP.grid(row=1, column=1)

tk.Button(settings, text='Start', command=settings.quit).grid(row=3, 
                                                       column=1, 
                                                       sticky=tk.W, 
                                                       pady=4)

settings.mainloop()

frameQueue = queue.LifoQueue()
commandQueue = queue.LifoQueue()
lock = threading.Lock()
host = serverIP.get()
print(host)
picturegetter = threading.Thread(target=getPicture, args=(host,frameQueue,), daemon = True)
picturegetter.start()
controller = threading.Thread(target=controller, args=(frameQueue, commandQueue,), daemon = True)
controller.start()
commandSender = threading.Thread(target=sendCommand, args=(host, commandQueue,), daemon = True)
commandSender.start()

