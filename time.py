import time


t = time.time()
t = int(t)
mod = t % 600
st = mod / 10
mins = mod / 60
rnd_mins1 = round(mod / 60.0,1)
rnd_mins0 = round(mod / 60.0,0)
print "time in secs {0}".format(t)
print "secs to nearest 10 min mark {0}".format(mod)
print "secs between readings (10 readings) {0}".format(st)
print "minutes until next 10 min mark {0}".format(mins)
print "rounded mins until next 10 min mark {0}".format(rnd_mins1)
print "rounded mins until next 10 min mark {0}".format(rnd_mins0)
