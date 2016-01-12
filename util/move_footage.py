#!/usr/local/bin/python3
import sys
import datetime
import pysftp
import re
from path import path

SOURCE_DIR = '/home/weather/sec_video'
DEST_DIR = '/mnt/usbstorage/security'

today = datetime.date.today()

def now():
    return datetime.datetime.now()


print("{1} Moving footage not from {0}".format(today, now()))

# We search for file names with this pattern to identify files from today
today_str = "{0}{1:02d}{2:02d}".format(today.year, 
        today.month, today.day)

# Get the search pattern to identify the day to which a file belongs
# file names look like this "14-20150702090025.avi"
# Pattern looks for 4 digits of year, then two digits of month, then two of day
# pattern is anchored in file name with '-'
p = re.compile("-(\d\d\d\d)(\d\d)(\d\d)")

files_to_move = []
files_to_delete = []

src_dir = path(SOURCE_DIR)
for f in src_dir.files():
    if today_str in f.name or 'lastsnap' in f.name:
        print("{1} Not moving {0}".format(f.name, now()))
        continue
    files_to_move.append(f.name)
    files_to_delete.append(f)

with pysftp.Connection('192.168.0.224', username='nas', 
        password='vader370') as sftp:
    with pysftp.cd(SOURCE_DIR):
        for i in files_to_move:
            sftp.chdir(DEST_DIR)
            if not sftp.exists(i):
                print("{1} Moving {0}".format(i, now()))
                sftp.put(i, preserve_mtime=True)
            else:
                print("{1} Not moving {0} - already exists remotely".format(
                    i, now()))

for f in files_to_delete:
    print("{1} Removing {0}".format(f.name, now()))
    f.remove()
