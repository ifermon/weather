#!/bin/bash

# Check to see if process exists
#go_pi=$(ps -ef | grep g[o])

# Put in a little delay before we start
date
echo "Going to sleep for 10 seconds"
sleep 10

# Start the pi gpio deamon - should check to see if it's arleady running
date
echo "Launching pigpiod"
sudo pigpiod

# Start up readings
date
echo "Starting to get readings"
sudo python3 /home/weather/weather/weather_readings.py
