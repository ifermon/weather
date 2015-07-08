#!/usr/local/bin/python3
import sys
import datetime
import pysftp
from path import path

SOURCE_DIR = '/home/weather/sec_video'
DEST_DIR = '/mnt/usbstorage/security'

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)

def now():
    return datetime.datetime.now()


print("{1} Moving footage from {0}".format(yesterday, now()))

y_str = "{0}{1:02d}{2:02d}".format(yesterday.year, 
        yesterday.month, yesterday.day)

files_to_move = []
files_to_delete = []

src_dir = path(SOURCE_DIR)
for f in src_dir.files():
    if not y_str in f.name:
        print("{1} Not moving {0}".format(f.name, now()))
        continue
    files_to_move.append(f.name)
    files_to_delete.append(f)

with pysftp.Connection('192.168.0.224', username='nas', 
        password='vader370') as sftp:
    with pysftp.cd(SOURCE_DIR):
        sftp.chdir(DEST_DIR)
        for i in files_to_move:
            if not sftp.exists(i):
                print("{1} Moving {0}".format(i, now()))
                sftp.put(i, preserve_mtime=True)
            else:
                print("{1} Not moving {0} - already exists remotely".format(
                    i, now()))

for f in files_to_delete:
    print("{1} Removing {0}".format(f.name, now()))
    f.remove()
