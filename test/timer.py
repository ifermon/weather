from threading import Timer
import time

def go_timer():
    print "Hello World!!"
    return

t = Timer(10.0, go_timer)
t.start()
print "Done"
