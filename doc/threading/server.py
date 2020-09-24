import threading
import socket
import time

def sendPicture(host):
    port = 50101
    print("opening picture connection")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        while True:
            s.listen()
            connection, address = s.accept()
            with connection:
                connection.sendall(b'an image')

def handleCommand(host):
    port = 50102
    print("opening command connection")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        while True:
            s.listen()
            connection, address = s.accept()
            print("connected")
            with connection:
                data = connection.recv(1024)
                print("received command: ", repr(data))
    

host = 'localhost'
picturesender = threading.Thread(target=sendPicture, args=(host,), daemon = True)
picturesender.start()
commandhandler = threading.Thread(target=handleCommand, args=(host,), daemon = True)
commandhandler.start()
