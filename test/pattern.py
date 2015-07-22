#!/usr/local/bin/python3

# Test pattern matching

import re


test_str = '14-20150702090025.avi'


p = re.compile('-(\d\d\d\d)(\d\d)(\d\d)')

m = p.search(test_str)

print("Matches: {0}".format(m.group()))
print("Matches: {0}".format(m.group(1)))
print("Matches: {0}".format(m.group(2)))
print("Matches: {0}".format(m.group(3)))
