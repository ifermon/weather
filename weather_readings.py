#!/usr/bin/python3
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
import getopt
import logging
import MySQLdb as db

# Interval in minutes between writes, need the .0 for math but needs to be int
INTERVAL = 10.0

# Usage message
USAGE="weather_readings.py [-l]"

# Log if we get a signal
def signal_handler(signal, frame):
    print("Got signal <{0}>.".format(signal))
    sys.exit(0)
    return

signal.signal(15, signal_handler)

# Process command line arguments
try:
    opts, args = getopt.getopt(sys.argv[1:], "ld")
except getopt.GetoptError:
    print(USAGE)
    sys.exit(2)

for opt, args in opts:
    if opt == '-l':
        logging.basicConfig(format="%(asctime)s: %(message)s",
                level=logging.INFO)
    elif opt == '-d':
        logging.basicConfig(format="%(asctime)s: %(message)s",
                level=logging.DEBUG)


logging.info("Starting weather_readings.py")

# Set up access to spreadsheet and temp sensor
ws = g_spread.Sheet()
logging.debug("Setup access to google spreadsheet")
sensors = sensor.Sensors()
logging.debug("Setup access to temp/humid and light sensors")

# Set up connection to database
conn = None
cursor = None
for msql_try_cnt in range(0,3):
    try:
        conn = db.connect(
                host="localhost",
                user="weather_program",
                db='weather')
        cursor = conn.cursor()
    except:
        if msql_try_cnt == 2:
            logging.error("Three consecutive msql connection failures. Exit")
            sys.exit(1)
        else:
            logging.error("Mysql connection failed, sleep for 30 seconds and retry")
            time.sleep(30)

while True:

    '''
    We are going to take interval readings, one per min, from the light sensor
    and the temp / humid sensor. Then we are going to average them, get the 
    power from the solar monitor, and log the whole bunch. Some time 
    math at the beginning so that we keep more or less on the 10's
    '''
    tnow = time.time() # Get current time
    secs_in_interval = int(INTERVAL * 60)
    # Round up to the next 10 minutes
    start_time = int(tnow / INTERVAL) * INTERVAL 
    end_time = start_time + secs_in_interval
    sleep_time = int((end_time - tnow) / INTERVAL)
    logging.debug("start {0} end {1} sleep {2}".format(time.ctime(start_time),
        time.ctime(end_time), sleep_time))
    avg_temp = 0
    avg_humid = 0
    avg_light = 0

    for min in range(int(INTERVAL)):
        #Get temp & humid
        try:
            logging.debug("Getting temp / humid")
            (temp, humidity) = sensors.get_temp_humid()
        except Exception as e:
            logging.error("Unexpected error getting temp/humid: \n{0}\n{1}\n{2}".format(
                    sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))

        #Get light
        try:
            logging.debug("Getting light")
            light = sensors.get_light()
        except Exception as e:
            print("Unexpected error getting light: \n{0}".format(
                    sys.exc_info()[0]))

        logging.debug("temp {0} light {1} humid {2}".format(temp, 
            light, humidity))

        # Log to database
        stmt = """INSERT INTO 
                    minute_data (humidity, light_level, temperature)
                VALUES
                    ({}, {}, {})""".format(humidity, light, temp)
        cursor.execute(stmt)
        conn.commit()

        avg_temp += temp
        avg_light += light
        avg_humid += humidity
        logging.debug("avg temp {0} avg light {1} avg humid {2}".format(
            avg_temp, avg_light, avg_humid))

        # sleep for the next reading, should be about 60 secs
        time.sleep(sleep_time)
        ###END FOR###

    avg_temp = avg_temp / INTERVAL
    avg_light = avg_light / INTERVAL
    avg_humid = avg_humid / INTERVAL
    power_generated = "0"
    try:
        power_generated = "{:.3f}".format(power.get_power_generated_t(
                start_time, end_time))
    except:
        logging.error("Unexpected error getting power: \n{0}".format(
                sys.exc_info()[0]))

    logging.debug("time \t avg temp \t avg light \t avg humid \t power")
    logging.debug("{4} \t {0} \t {1} \t {2} \t {3}".format(avg_temp, 
        avg_light, avg_humid, power_generated, end_time))

    # Log to database
    stmt = """INSERT INTO 
                ten_minute_data (
                    avg_temperature, avg_humidity, avg_light_level,
                    power, start_time_epoch, end_time_epoch)
            VALUES
                ({:.2f}, {:.2f}, {:.2f}, {}, {}, {})""".format(
                        avg_temp, avg_humid, avg_light, power_generated,
                        end_time, start_time)
    logging.debug("Stmt: {}".format(stmt))
    cursor.execute(stmt)
    conn.commit()

    ws.log_readings((end_time, time.ctime(end_time), avg_temp, 
            avg_light, avg_humid, power_generated))




