import smbus2 as smbus
DEVICE_BUS = 1
DEVICE_ADDR = 0x04
bus = smbus.SMBus(DEVICE_BUS)
#this is how to send the position to 
bus.write_block_data(DEVICE_ADDR,0, [90,70])

