#!/usr/bin/python3
import sys
import datetime
import time
import pysftp
import re
import const # gpg fname.gpg to decrypt
from path import path

SOURCE_DIR = '/home/weather/sec_video'
DEST_DIR = '/media/usb/security'

today = datetime.date.today()

def now():
    return time.asctime()


print("{1} Moving footage not from {0}".format(today, now()))

# We search for file names with this pattern to identify files from today
today_str = "{0}{1:02d}{2:02d}".format(today.year, 
        today.month, today.day)

# Get the search pattern to identify the day to which a file belongs
# file names look like this "14-20150702090025.avi"
# Pattern looks for 4 digits of year, then two digits of month, then two of day
# pattern is anchored in file name with '-'
p = re.compile("-(\d\d\d\d)(\d\d)(\d\d)")

files_to_move = {}
#files_to_move = []
#files_to_delete = []

src_dir = path(SOURCE_DIR)
for f in src_dir.files():
    if today_str in f.name or 'lastsnap' in f.name:
        print("{} | Not moving {}".format(now(), f.name))
        continue
    #files_to_move.append(f.name)
    files_to_move[f.name] = f
    print("{} | Adding {} to list".format(now(), f.name))
    #files_to_delete.append(f)

with pysftp.Connection(const.NAS_IP, username=const.NAS_USER, 
        password=const.NAS_PWD) as sftp:
    print("Connected")
    with pysftp.cd(SOURCE_DIR):
        print("Changed directory")
        for i in files_to_move.keys():
            sftp.chdir(DEST_DIR)
            if not sftp.exists(i):
                print("{1} Moving {0}".format(i, now()))
                try:
                    sftp.put(i, preserve_mtime=True)
                except FileNotFoundError:
                    pass

            else:
                print("{1} Not moving {0} - already exists remotely".format(
                    i, now()))
            print("{1} Removing {0}".format(i, now()))
            try:
                files_to_move[i].remove()
            except FileNotFoundError:
                print("Error removing {}".format(i))
                pass

#for f in files_to_delete:
    #print("{1} Removing {0}".format(f.name, now()))
    #f.remove()
