"""
    This file contains the main logic for setting up and gathering readings

"""

# Set up access to google spreadsheets
import g_spread
import time
import sensor

# Interval in minutes between writes
INTERVAL = 10

ws = g_spread.Sheet()
ws.log_readings((123123,"Human time here", 12.3, 45.2, 69.0, 1234))
sensors = Sensors()

while True:

    '''
    We are going to take 10 readings, one per minute, from the light sensor
    and the temp / humid sensor. Then we are going to average them, get the 
    power from the solar monitor, and log the whole bunch. Some time 
    math at the beginning so that we keep more or less on the 10's
    '''
    tnow = time.time()
    secs_till_interval = (60.0 * INTERVAL) - (tnow % (60.0 * INTERVAL))
    sleep_time = secs_till_interval / INTERVAL
    avg_temp = 0
    avg_humid = 0
    avg_light = 0

    # Get INTERVAL readings of light, humid and temp, about 1 per minute
    for min in range(10):
        #Get temp & humid
        (temp, humidity) = sensors.get_temp_humid()
        #Get light
        light = sensors.get_light()

        avg_temp += temp
        avg_light += light
        avg_humid += humid

        # sleep for the next reading, should be about 60 secs
        time.sleep(sleep_time)

    avg_temp = avg_temp / INTERVAL
    avg_light = avg_light / INTERVAL
    avg_humid = avg_humid / INTERVAL




