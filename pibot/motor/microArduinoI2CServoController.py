import smbus2 as smbus

class CameraMount:
  def __init__(self):
    self.MAXVALUE = 180
    self.MINVALUE = 0
    self.DEVICE_BUS = 1
    self.DEVICE_ADDR = 0x04
    self.bus = smbus.SMBus(DEVICE_BUS)

  def execute(self, command):
    #this is how to send the position to the arduino, see /doc/cameramount for arduinocode
    try:
      values = [max([self.MINVALUE, min([i,self.MAXVALUE])]) for k, i in command.items()]
      bus.write_block_data(DEVICE_ADDR, 0, values)    
    except Exception as e:
      print(e)
