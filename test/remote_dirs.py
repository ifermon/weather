#!/usr/local/bin/python3
import os
import pysftp

local_path='/home/weather/'
os.chdir(local_path)
with pysftp.Connection('server', username='user',
                password='pwd') as sftp:
        f_list = sftp.listdir()
        for f in f_list:
            if not f.endswith("mp3"):
                continue
            ctr = 1
            new_f_name = f
            while os.path.exists(new_f_name):
                new_f_name = "{0}-{1}".format(ctr,f)
                ctr+=1
            print("Moving remote file <{0}> to local file <{1}>".format(f, 
                    new_f_name))
            sftp.get(f, localpath=local_path+new_f_name)


