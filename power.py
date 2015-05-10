'''
    This files pulls data from TED Pro
'''

'''
    IP is the IP of my TED Footprints server
    T: History Type (0=Second, 1=Minute, 2=Day, 3=Hour, 4=Month)
    D: Device Type. 0=MTU 1=Spyder
    M: The 1-based index of the MTU or Spyder being displayed.
    C: Count (optional): Number of records to return (starting with the most 
            recent)
    I: Index (optional): Number of records to offset (starting from the most 
            recent)
    S: start time (optional): Allows you to specify a date range of which to 
            return records. Time is specified in epoch time format.
    E: end time (optional): Allows you to specify a date range of which to 
            return records. Time is specified in epoch time format.
    T=2 seems to be minutes, but that's not what doc says
    M=2 is my solor MTU
'''
URI = 'http://192.168.0.207/history/export.xml?T=2&D=0&M=2'

import requests
import xml.etree.ElementTree as ET
import time


'''
    Takes a parameter of number of minutes, and gets the power generated
    over that time frame using the history api of the TEDPro
'''
def get_power_generated(minutes):

    # Ask for minute level history for the last x minutes
    # request takes an agruement in seconds since epoch and gives us
    # minute history after that value
    t = time.time()
    t = t - ((minutes + 1) * 60)# Add 
    r = requests.get("{0}&S={1}".format(URI,t))

    # Parse the returning xml
    # <MINUTE><TIME>seconds</TIME><POWER>power level</POWER></MINUTE>
    tree = ET.fromstring(r.text)

    # Now get the avg power produced each minute, figure the total power
    # prouduced over the period, and return the value
    avg_power = 0.0
    num_readings = 0
    for node in tree:
        for l in node:
            if l.tag == "POWER":
                avg_power += float(l.text)
                num_readings += 1
        
    '''
        Pulling the power rate generated every minute. It's in KWh. So get
        average kWh generated over minutes and multiply by 
        minutes / 60 should get you the power generated over that time period
    '''
    avg_power = avg_power / num_readings
    power_generated = avg_power * (num_readings / 60)
    print("avg power {0}".format(avg_power))
    print("power gen {0}".format(power_generated))
    return power_generated

