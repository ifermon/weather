#!/bin/bash

# Check to see if process exists
#go_pi=$(ps -ef | grep g[o])

# Put in a little delay before we start
date
echo "Starting up ... going to sleep for 30 seconds"
sleep 30

# Start the pi gpio deamon - should check to see if it's arleady running
date
echo "Launching pigpiod"
sudo pigpiod

# Launching motion
#date
echo "Launching motion"
sudo motion &
#sudo motion -n &

# Launching watchdog
#date
echo "Launching watchdog"
sudo watchdog -v

# Starting up weather if it's not a crontab reboot
if [ -f /home/weather/weather/cronboot ]; then
    echo "Not sending text, removing cronboot"
    rm /home/weather/weather/cronboot
else
    date
    echo "Sending text regarding reboot"
    wget --quiet --delete --no-check -t 1 "https://192.168.0.210:5000/send_message?msg=Starting weather" 
fi

# Start up readings
# Loop through in case we get an error
date
echo "Starting to get readings"
while :
do
    sudo python3 /home/weather/weather/weather_readings.py
    wget --quiet --delete --no-check -t 1 "https://192.168.0.210:5000/send_message?msg=Error in weather - restarting weather"
    date
    echo "Error in weather - restarting weather"
    sleep 5
done
