#!/usr/bin/python
import os
from ftplib import FTP

local_path='./'
os.chdir(local_path)
ftp = FTP(host='nas', user='nas', passwd='vader370') 
ftp.cwd('/mnt/usbstorage/security')
f_list = ftp.nlst()
for f in f_list:
    if not f.endswith("py"):
        print("Not getting {0}".format(f))
        continue
    new_f_name = local_path + f
    if os.path.exists(new_f_name):
        continue
    print("Copying remote file <{0}> to local file <{1}>".format(f,
            new_f_name))
    ftp.retrbinary('RETR ' + f, open(new_f_name,'wb').write)
