import time
import smbus

_addr = 0x23

# Read the value of the light sensor
bus = smbus.SMBus(1)
while True:
	data = bus.read_i2c_block_data(_addr, 0x11)
	light_level = int((data[1] + (256 * data[0])) / 1.2)
	print light_level
	time.sleep(3)


