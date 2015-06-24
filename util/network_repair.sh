#!/bin/bash

LOG_FILE=/home/weather/weather/logs/net_repair.log

REPAIR_COUNT=/home/weather/weather/util/net_rep_count

if [ ! -f ${REPAIR_COUNT} ]; then
    sudo echo "1" > ${REPAIR_COUNT}
fi

repair_count=$(cat ${REPAIR_COUNT})
if [ "${repair_count}" -gt "5" ]; then
    echo "$(date) Repair count too high, exit w/ failure" 
    rm ${REPAIR_COUNT}
    exit $1
else
    echo "$(date) Repair count okay (${repair_count})" 
    ((repair_count++))
    echo ${repair_count} > ${REPAIR_COUNT}
fi


exit 0

echo "$(date) In network_repair.sh, called with $1 and $2" 
echo "$(date) Sleeping for 5 secs..." 
sleep 5

echo "$(date) Bringing network down" 
sudo ifconfig wlan0 down

echo "$(date) Network down, sleeping for 5 secs" 
sleep 5

echo "$(date) Bringing network back up" 
sudo ifconfig wlan0 up
ret=$?

echo "$(date) Completed wlan0 up with code $ret" 
exit $ret
