#!/usr/bin/python

import sys
import shelve
import os.path
import time
from contextlib import closing

'''
    This file is designed to be invoked from command line or shell. It has two modes: 
    add_event tag_name
    event_count tag_name time_period (optional) time_period_type (optional)
    keeps track of events (tags), with times and can return the number of events occuring in the last xxx minutes
'''

EVENT_FILE_NAME = "event_times"

def add_event(tag_name):
    # Open event file with this tag name, it will create one if none exists
    with closing(shelve.open(EVENT_FILE_NAME, writeback=True)) as event_times:
        if not event_times.has_key(tag_name):
            event_times[tag_name] = []
        event_times[tag_name].append(time.time())
    return

def event_count(tag_name, minutes):
    seconds = int(minutes) * 60
    ret_value = 0
    with closing(shelve.open(EVENT_FILE_NAME)) as event_times:
        if event_times.has_key(tag_name):
            event_list = event_times[tag_name]
            event_list.sort()
            now = time.time()
            ts = now - seconds
            events_after_ts = 0
            for t in event_list:
                if t > ts:
                    events_after_ts += 1
                else:
                    break
            ret_value = events_after_ts
    return ret_value

def list_event_times(tag_name):
    with closing(shelve.open(EVENT_FILE_NAME)) as event_times:
        ret_code = ""
        for t in event_times[tag_name]:
            ret_code = "{}\t{}\n".format(ret_code, t)
        return ret_code


if len(sys.argv) < 2:
    print("No commands found")
    sys.exit(0)

if sys.argv[1] == "add_event":
    add_event(sys.argv[2])
    sys.exit(0)
elif sys.argv[1] == "event_count":
    print(event_count(sys.argv[2], sys.argv[3]))
    sys.exit(0)
elif sys.argv[1] == "list_event_times":
    print(list_event_times(sys.argv[2]))
    sys.exit(0)
else:
    print("No valid commands found")
    sys.exit(0)
