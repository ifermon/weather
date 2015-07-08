#!/bin/bash

# Check to see if process exists
#go_pi=$(ps -ef | grep g[o])

# Check to see if we stop , this is in case we just need to stop restarting
# You can just log in and touch stop, remove stop to keep going
date
if [ -f /home/weather/stop ]; then
    echo "Stopping go... file stop exists"
    exit 0
fi

# Put in a little delay before we start
date
echo "Starting up ... going to sleep for 30 seconds"
sleep 30

# Launching motion
#date
echo "Launching motion"
sudo motion &
#sudo motion -n &

# Start the pi gpio deamon
date
echo "Launching pigpiod"
sudo service pigpiod start

# Launching watchdog
date
echo "Launching watchdog"
sudo modprobe bcm2708_wdog
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
fail_count=0
while :
do
    sudo /home/weather/weather/weather_readings.py -d
    wget --quiet --delete --no-check -t 1 "https://192.168.0.210:5000/send_message?msg=Error in weather - restarting weather"
    date
    $((fail_count++))
    if [ ${fail_count} -eq 5 ]; then
        echo "Error in weather. Failed 5 times ... need to reboot"
        sudo reboot
    else
        echo "Error in weather. Restarting weather. fail_count = ${fail_count}"
        echo "Restart pigpiod"
        # We restart pigpiod because otherwise you leave open resources
        sudo service pigpiod restart
    fi
    sleep 5
done
