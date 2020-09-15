import socket
import ast
import smbus2 as smbus

host = '192.168.0.135'
port = 50101

values = [0,0,0,0]

arduinoDeviceBus = 1
arduinoDeviceAddr = 0x04
arduinoBus = smbus.SMBus(self.DEVICE_BUS)
videoCapture = None

try:
    videoCapture = cv2.VideoCapture(0)
except Exception as e:
    print(e)

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
                            values[0] = data["motor"]["right"]
                            values[1] = data["motor"]["left"]
                        elif("camera" in data):
                            values[0] = data["camera"]["x"]
                            values[1] = data["camera"]["y"]
                        #this is how to send the position to the arduino, see /doc/cameramount for arduinocode
                        print(values)
                        try:
                          self.bus.write_block_data(self.DEVICE_ADDR, 0, values)    
                        except Exception as e:
                          print(e)

                        if videoCapture:
                            ret,frame=videoCapture.read()
                            # Serialize frame
                            data = pickle.dumps(frame)
                            # Send message length first
                            message_size = struct.pack("L", len(data))
                            # Then data
                            s.sendall(message_size + data)
                        else:
                            s.sendall(0)
                    
except ConnectionRefusedError:
    print("Could not connect to robot")
finally:
    s.close()

        
