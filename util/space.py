#!/usr/bin/python

from path import path
import time

'''
	Given a quote, delete all files older than 
'''

DAYS = 3
QUOTA = 5 #In gigabytes
removed = 0

d = path("/home/weather/video")

time_in_secs = time.time() - (DAYS * 24 * 60 * 60)

# Collect the list of files
file_list = []
for f in d.walk():
	if f.isfile():
		file_list.append((f.ctime, f))

# Now sort the list, newest first
file_list.sort(reverse = True, key = lambda tup: tup[0])

# Now iterate through the list, adding up size, until we reach out quota,
# then delete all files after that
cumulative_size = 0
for f in file_list:
	bsize = f[1].size
	cumulative_size += bsize / 1000000000.0
	if cumulative_size < QUOTA:
		print "Keeping {0}".format(f[1].name)
		continue
	print "Deleting {0}".format(f[1].name)
	f[1].remove

