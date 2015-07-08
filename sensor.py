#!/usr/local/bin/python3
'''
    This files gets the readings from the light and temp / humid sensor
'''

import time
import pigpio
import logging
import smbus

_3W = (1<<9) # I have no idea what this is
_3WN = (15<<10) # I have no idea what this is

SPEED = 200000
BYTES = 130
INTERVAL = 60

# This is for the light sensor, it's address in the i2c bus
LIGHT_SENSOR_ADDR = 0x23


class Sensors(object):

    def __init__(self):
        # The light sensor is on i2c bus 1, address 23
        self.bus = smbus.SMBus(1)

        # Connect to local GPIO
        self.pi = pigpio.pi() 

        # Connect to temp / humid sensor
        self.am2302 = self.pi.spi_open(0, SPEED, _3W|_3WN)
        return


    '''
        I copied this, don't really understand it
    '''
    def get_bit(self, in_bit, in_byte, buf):
        global BYTES
        v = not (buf[in_byte] & (1<<(7-in_bit))) # Force logical result
        numbit = 1

        while in_byte < BYTES:
            in_bit += 1
            if in_bit > 7:
                in_bit = 0
                in_byte += 1
            nv = not (buf[in_byte] & (1<<(7-in_bit)))
            if nv == v:
                numbit += 1
            else:
                if not v: # Return high edge
                    return (numbit, in_bit, in_byte)
                else: # Skip low edge
                    v = nv
                    numbit = 1
        return (0, 0, 0)

    '''
        Temp and humidity come from the same sensor, so read them together
        I copied this stuff, don't understand much of it
    '''
    def get_temp_humid(self):
        # I don't understand this stuff, but it works
        (c, buf) = self.pi.spi_read(self.am2302, BYTES+1)
        numbit = 1
        in_bit = 0
        in_byte = 0
        (numbit, in_bit, in_byte) = self.get_bit(in_bit, in_byte, buf)
        logging.debug("numbit {0} in bit {1} in byte {2}".format(
                numbit, in_bit, in_byte))
        (numbit, in_bit, in_byte) = self.get_bit(in_bit, in_byte, buf)
        logging.debug("numbit {0} in bit {1} in byte {2}".format(
                numbit, in_bit, in_byte))
        bit = 0
        byte = 0
        val = [0]*5
        temp = 0
        humidity = 0
        while numbit:
            (numbit, in_bit, in_byte) = self.get_bit(in_bit, in_byte, buf)
            if numbit:
                if numbit > 9:
                    val[byte] |= (1<<(7-bit))
                bit += 1
                if bit > 7:
                    bit = 0
                    byte += 1
        checksum = 0
        for i in range(4):
            checksum += val[i]
        if val[4] == (checksum&255):
            humidity = ((val[0]*256) + val[1]) / 10.0

            sign = val[2] & 128
            val[2] &= 0x127
            temp = ((val[2]*256) + val[3]) / 10.0
            if sign:
                temp = -temp
            #convert to F
            temp = (temp * (9.0 / 5.0)) + 32.0
        logging.debug("In Sensor.py: temp {0} humid {1}".format(temp, humidity))
        return (temp, humidity)

    '''
        Get the light level
    '''
    def get_light(self):
        data = self.bus.read_i2c_block_data(LIGHT_SENSOR_ADDR, 0x11)
        light_level = int((data[1] + (256 * data[0])) / 1.2)
        return light_level



# Testing here
if __name__ == "__main__":
    
    s = Sensors()
    logging.basicConfig(format="%(asctime)s: %(message)s",
                level=logging.DEBUG)
    
    for i in range(10):
        logging.debug(s.get_light())
        logging.debug(s.get_temp_humid())
        time.sleep(60)
