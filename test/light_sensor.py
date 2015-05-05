import time
import smbus
import logging

_addr = 0x23

# Read the value of the light sensor
bus = smbus.SMBus(1)
logging.basicConfig(filename="level.out", format="%(message)s",
				level=logging.DEBUG)
while True:
	data = bus.read_i2c_block_data(_addr, 0x11)
	light_level = int((data[1] + (256 * data[0])) / 1.2)
	t = time.time()
	localtime = time.asctime( time.localtime(t))
	log_msg = "{2} | {1} | {0}".format(light_level, localtime, t)
	logging.debug(log_msg)
	time.sleep(60)


