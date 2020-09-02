import pibot.motor.DRV8835_rpi
import socket
import ast

host = '192.168.0.135'
port = 50101

motorset = pibot.motor.DRV8835_rpi.DRV8835()
cameramount = pibot.motor.cameramount.CameraMount()

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    else:
                        print(data)
                        motorset.execute(ast.literal_eval(data.decode("utf-8")))
                        cameramount.execute(ast.literal_eval(data.decode("utf-8")))
except Exception as e:
    print(e)
finally:
    try:
        s.close()
    except Exception:
        pass
    
    


