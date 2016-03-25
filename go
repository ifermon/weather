#!/bin/bash

# Check to see if process exists
#go_pi=$(ps -ef | grep g[o])

# IP address for garagePi (and port) for messages
garagePi="192.168.0.215:5000"

# Check to see if we stop , this is in case we just need to stop restarting
# You can just log in and touch stop, remove stop to keep going
if [ "$1" != "skipcheck" ]; then
    if [ -f /home/weather/stop ]; then
        echo "$(date): Stopping go... file stop exists"
        exit 0
    fi
fi

# Put in a little delay before we start
echo "$(date): Starting up ... going to sleep for 30 seconds"
sleep 30

# Launching motion, first update the video driver to help w exposure issue
sudo modprobe bcm2835-v4l2 max_video_width=2592 max_video_height=1944
echo "$(date): Launching motion"
sudo strace -ff -t -o /home/weather/weather/logs/motion_trace.log /home/weather/weather/motion -c /home/weather/weather/config/motion.conf &
#sudo motion -n &

# Start the pi gpio deamon
echo "$(date): Launching pigpiod"
sudo service pigpiod start

# Launching watchdog
echo "$(date): Launching watchdog"
sudo modprobe bcm2708_wdog
sudo watchdog -v

# Starting up weather if it's not a crontab reboot
if [ -f /home/weather/weather/cronboot ]; then
    echo "Not sending text, removing cronboot"
    rm /home/weather/weather/cronboot
else
    echo "$(date): Sending text regarding reboot"
    wget --quiet --delete --no-check -t 1 "https://${garagePi}/send_message?msg=Starting weatherPi" 
fi

# Start up readings
# Loop through in case we get an error
echo "$(date): Starting to get readings"
fail_count=0
while :
do

    sudo  /home/weather/weather/weather_readings.py -l
    if [ -f /home/weather/weather/cronboot ]; then
        echo "Not sending text because cronboot exists, in fail loop, not deleting cronboot"
    else
        msg="Error in weather app.\nFail count = ${fail_count}\nRestarting app at $(date)"
        wget --quiet --delete --no-check -t 1 "https://${garagePi}/send_message?msg=${msg}"
    fi
    ((fail_count++))
    if [ ${fail_count} -eq 5 ]; then
        echo "$(date): Error in weather. Failed 5 times ... rebooting weatherPi"
        sudo reboot
    else
        echo "$(date): Error in weather. Restarting weather. fail_count = ${fail_count}"
        echo "$(date): Restart pigpiod"
        # We restart pigpiod because otherwise you leave open resources
        sudo service pigpiod restart
    fi
    sleep 5
done
