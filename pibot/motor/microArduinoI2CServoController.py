import smbus2 as smbus

class CameraMount:
  def __init__(self):
    MAXVALUE = 180
    MINVALUE = 0
    DEVICE_BUS = 1
    DEVICE_ADDR = 0x04
    bus = smbus.SMBus(DEVICE_BUS)

  def execute(self, command):
    #this is how to send the position to the arduino, see /doc/cameramount for arduinocode
    try:
      values = [max([self.MINVALUE, min([i,self.MAXVALUE])]) for k, i in command.items()]
      bus.write_block_data(DEVICE_ADDR, 0, values)    
    except Exception as e:
      print(e)
