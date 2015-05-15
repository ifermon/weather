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

# Launching motion
date
echo "Launching motion"
sudo motion

# Starting up weather
date
echo "Sending text regarding reboot"
wget -q --no-check -t 1 "https://192.168.0.210:5000/send_message?msg=Starting weather" > /dev/null 

# Start up readings
date
echo "Starting to get readings"
sudo python3 /home/weather/weather/weather_readings.py
