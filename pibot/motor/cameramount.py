import smbus2 as smbus

class CameraMount:
  def __init__():
    axes = 2
    DEVICE_BUS = 1
    DEVICE_ADDR = 0x04
    bus = smbus.SMBus(DEVICE_BUS)

  def execute(command):
    #this is how to send the position to the arduino, see /doc/cameramount for arduinocode
    try: 
      bus.write_block_data(DEVICE_ADDR, 0, [command["horizontal"], command["vertical"]])    
    except Exception as e:
      print(e)
