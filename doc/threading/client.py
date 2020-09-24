import threading
import socket

def getPicture(host):
    try:
        port = 50101
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                data = s.recv(1024)
                print(repr(data))
    except ConnectionRefusedError as e:
        print("Could not get picture: " + str(e))

def controller(host):
    try:
        port = 50102
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                s.sendall(b'this is a command')
    except ConnectionRefusedError as e:
        print("Could not send command: " + str(e))
        
host = 'localhost'
picturegetter = threading.Thread(target=getPicture, args=(host,), daemon = True)
picturegetter.start()
controller = threading.Thread(target=controller, args=(host,), daemon = True)
controller.start()
