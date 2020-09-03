import smbus2 as smbus

class CameraMount:
  def __init__(self):
    self.DEVICE_BUS = 1
    self.DEVICE_ADDR = 0x04
    self.bus = smbus.SMBus(self.DEVICE_BUS)

  def execute(self, command):
    #this is how to send the position to the arduino, see /doc/cameramount for arduinocode
    values = [i for k, i in command.items()]
    try:
      self.bus.write_block_data(self.DEVICE_ADDR, 0, values)    
    except Exception as e:
      print(e)
