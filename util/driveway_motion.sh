#!/bin/bash -v

# Sends a text message when something is moving in the driveway

LOGFILE="/home/weather/weather/logs/driveway_motion.log"
LOGERR="/home/weather/weather/logs/driveway_motion_err.log"

exec >> ${LOGFILE}
exec 2>> ${LOGERR}

date # For the log file

sudo -u weather wget --quiet --delete --no-check -t 1 "https://192.168.0.40:5000/send_message?msg=Driveway motion click to view: http://ifermon.ddns. net:9000/"
