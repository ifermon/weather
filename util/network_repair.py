#!/usr/local/bin/python3

import time
import shelve
import subprocess
import sys

LOG_FILE="/home/weather/weather/logs/net_repair.log"
SHELF="/home/weather/weather/util/failure_log.shelf"
FAIL_COUNT="fail_count"
LAST_UPDATE="last_update_timestamp"

def log(msg):
    print("{0} {1}".format(time.asctime(), msg))
    return

def cycle_network():
    log("Sleeping for 5 seconds before bringing network down")
    time.sleep(5)
    ret_code = 0
    ret_code = subprocess.call(['ifconfig', 'wlan0', 'down'])
    log("wlan0 down ret_code {0}, sleeping for 5 secs".format(ret_code))
    time.sleep(5)
    ret_code = subprocess.call(['ifconfig', 'wlan0', 'up'])
    log("wlan0 up ret_code {0}, sleeping for 5 secs".format(ret_code))
    return int(ret_code)


s = shelve.open(SHELF, writeback=True)

# Check to see if we have failed before, this should only happen the very first
# time this runs or if we clear away the file
if FAIL_COUNT not in s:
    s[FAIL_COUNT] = 0
    s[LAST_UPDATE] = time.time()

# Get arguments passed to us by watchdog, the first argument is the error code
log("Called with these arguments {0}".format(str(sys.argv)))
s_str = ""
for k, v in s.items():
    s_str+="[{0}:{1}] ".format(k, v)
log("Stored values {0}".format(str(s_str)))
err_code = int(sys.argv[1])

# Check to see how long since last failure in seconds
network_uptime = time.time() - s[LAST_UPDATE]

# If network as been up for more than 15 minutes then reset counter
# 60 seconds * 15 minutes = 900 seconds
if network_uptime > 900:
    s[FAIL_COUNT] = 0
    s[LAST_UPDATE] = time.time()

# Check to see if we have failed more than 5 times, if so return 
# error code that was passed to us
if s[FAIL_COUNT] > 5:
    log("{0} failures, return error code".format(s[FAIL_COUNT]))
    s.close()
    sys.exit(err_code)

# All the checks are done, now recycle network, increment counter and update
# timestamp for last updated
if cycle_network() != 0:
    log("Unsuccessful restarting network, return error code.")
    s.close()
    sys.exit(err_code)

s[FAIL_COUNT]+=1
s[LAST_UPDATE] = time.time()
s.close()
sys.exit(0)
