import pysftp
import datetime
import sys
from path import path

SOURCE_DIR = '/home/weather/sec_video'
DEST_DIR = '/mnt/usbstorage/security'

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)

print("Moving footage from {0}".format(yesterday))

y_str = "{0}{1:02d}{2:02d}".format(yesterday.year, 
        yesterday.month, yesterday.day)

files_to_move = []
files_to_delete = []

src_dir = path(SOURCE_DIR)
for f in src_dir.files():
    if not y_str in f.name:
        print("Not moving {0}".format(f.name))
        continue
    files_to_move.append(f.name)
    files_to_delete.append(f)

with pysftp.Connection('192.168.0.224', username='nas', 
        password='vader370') as sftp:
    with pysftp.cd(SOURCE_DIR):
        sftp.chdir(DEST_DIR)
        for i in files_to_move:
            if not sftp.exists(i):
                print("Moving {0}".format(i))
                sftp.put(i, preserve_mtime=True)
            else:
                print("Not moving {0} - already exists remotely".format(i))

for f in files_to_delete:
    print("Removing {0}".format(f.name))
    f.remove()
