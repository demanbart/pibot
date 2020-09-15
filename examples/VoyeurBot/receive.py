import pibot.motor.DRV8835_rpi
import pibot.motor.microArduinoI2CServoController
import socket
import ast

host = '192.168.0.135'
port = 50101

motorset = pibot.motor.DRV8835_rpi.DRV8835()
cameramount = pibot.motor.microArduinoI2CServoController.CameraMount()

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                while True:
                    bytedata = conn.recv(1024)
                    if not bytedata:
                        break
                    else:
                        data = ast.literal_eval(bytedata.decode("utf-8"))
                        print(data)
                        if("motor" in data):
                            motorset.execute(data["motor"])
                        elif("mouse" in data):
                            cameramount.execute(data["mouse"])
except Exception as e:
    print(e)
finally:
    try:
        s.close()
    except Exception:
        pass
    
    


 #draw controller
        
