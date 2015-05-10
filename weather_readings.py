"""
    This file contains the main logic for setting up and gathering readings

"""

# Set up access to google spreadsheets
import g_spread
import time
import sensor
import power

# Interval in minutes between writes
INTERVAL = 10

ws = g_spread.Sheet()
sensors = sensor.Sensors()

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
    log_time = tnow + sleep_time
    print("tnow {0} sleep {1} log {2}".format(tnow, sleep_time, log_time))

    # Get INTERVAL readings of light, humid and temp, about 1 per minute
    for min in range(INTERVAL):
        #Get temp & humid
        (temp, humidity) = sensors.get_temp_humid()
        #Get light
        light = sensors.get_light()
        print("light {0}".format(light))

        avg_temp += temp
        avg_light += light
        avg_humid += humidity

        # sleep for the next reading, should be about 60 secs
        time.sleep(sleep_time)

    print("avg temp before {0}".format(avg_temp))
    avg_temp = avg_temp / INTERVAL
    print("avg temp after {0}".format(avg_temp))
    avg_light = avg_light / INTERVAL
    avg_humid = avg_humid / INTERVAL
    power_generated = power.get_power_generated(INTERVAL)

    print("avg temp \t avg light \t avg humid \t power")
    print("{0} \t {1} \t {2} \t {3}".format(avg_temp, avg_light, avg_humid, power_generated))




