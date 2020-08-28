import pibot.motor.DRV8835_rpi
import socket
import ast

host = '127.0.0.1'
port = 50100

motorset = pibot.motor.DRV8835_rpi.DRV8835()

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(data)
                motorset.execute(ast.literal_eval(data.decode("utf-8")))
                conn.sendall(data)

