"""
    This file contains the main logic for setting up and gathering readings

"""

# Set up access to google spreadsheets
import g_spread
import time
import sensor
import power
import sys
import signal

# Interval in minutes between writes, need the .0 for math but needs to be int
INTERVAL = 10.0

ws = g_spread.Sheet()
sensors = sensor.Sensors()

# Log if we get a signal
def signal_handler(signal, frame):
    print("Got signal <{0}>.".format(signal))
    sys.exit(0)
    return

signal.signal(15, signal_handler)

while True:

    '''
    We are going to take interval readings, one per min, from the light sensor
    and the temp / humid sensor. Then we are going to average them, get the 
    power from the solar monitor, and log the whole bunch. Some time 
    math at the beginning so that we keep more or less on the 10's
    '''
    tnow = time.time() # Get current time
    secs_in_interval = int(INTERVAL) * 60
    start_time = int(tnow / secs_in_interval) * secs_in_interval
    end_time = start_time + secs_in_interval
    sleep_time = int(end_time - tnow) / INTERVAL
    avg_temp = 0
    avg_humid = 0
    avg_light = 0

    # Get INTERVAL readings of light, humid and temp, about 1 per minute
    #print("secs in interval {0}".format(secs_in_interval))
    #print("now   {0}".format(tnow))
    #print("start {0}".format(start_time))
    #print("end   {0}".format(end_time))
    #print("sleep time in secs {0}".format(sleep_time))
    for min in range(int(INTERVAL)):
        #Get temp & humid
        try:
            #print("Getting temp / humid")
            (temp, humidity) = sensors.get_temp_humid()
        except Exception as e:
            print("Unexpected error getting temp/humid: \n{0}\n{1}\n{2}".format(
                    sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))

        #Get light
        try:
            #print("Getting light")
            light = sensors.get_light()
        except Exception as e:
            print("Unexpected error getting light: \n{0}".format(
                    sys.exc_info()[0]))

        avg_temp += temp
        avg_light += light
        avg_humid += humidity

        # sleep for the next reading, should be about 60 secs
        time.sleep(sleep_time)
        ###END FOR###

    avg_temp = avg_temp / INTERVAL
    avg_light = avg_light / INTERVAL
    avg_humid = avg_humid / INTERVAL
    try:
        #power_generated = "{:.3f}".format(power.get_power_generated(INTERVAL))
        power_generated = "{:.3f}".format(power.get_power_generated_t(
                start_time, end_time))
    except:
        print("Unexpected error getting power: \n{0}".format(
                sys.exc_info()[0]))

    #print("time \t avg temp \t avg light \t avg humid \t power")
    #print("{4} \t {0} \t {1} \t {2} \t {3}".format(avg_temp, avg_light, avg_humid, power_generated, end_time))

    ws.log_readings((end_time, time.ctime(end_time), avg_temp, 
            avg_light, avg_humid, power_generated))




