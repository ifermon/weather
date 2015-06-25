#!/usr/local/bin/python3

import os
import sys
import time
import signal


def sig_handler(signal, frame):
    print("Got signal <{0}> and frame <{1}>.".format(signal, frame))
    sys.exit(0)
    return

for s in (2, 15):
    print("Setting signal {0}".format(s))
    signal.signal(s, sig_handler)
print("Send me a signal <{0}>".format(os.getpid()))
time.sleep(5000)


