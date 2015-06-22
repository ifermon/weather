#!/bin/bash

echo "Sleeping for 5 secs..."
date
sleep 5

echo "Bringing network down"
date
sudo ifconfig wlan0 down

echo "Sleeping for 5 secs"
date
sleep 5

echo "Bringing network back up"
date
sudo ifconfig wlan0 up
ret=$?

echo "Echo'ing with success"
exit $ret
