# coding=utf-8
# originally from http://stackoverflow.com/questions/5061446/api-with-past-weather
import urllib2
import numpy as np
from matplotlib.dates import datestr2num
import re
from functional import compose
from datetime import datetime

def br_strip(str):
    return re.sub(r'<.*$', '', str)

def NA2NaN(str):
    if str=='N/A':
        return np.NaN
    else:
        return float(str)

class ReversedRange(Exception):
    def __init__(self):
        super(ReversedRange, self).__init__("End of range is smaller than beginning")

"""Gets daily temperatures from Weather Underground"""

class Weather():
    """For now, only has columns which make sense as numbers"""
    date = None # UTC Time
    T = None # Temp [°F]
    Dp = None # Dewpoint [°F]
    RH = None # 0-100
    P = None # in Hg at sea level?
    Vis = None # Visibility (Miles?)
# needs Calm parser    MPH_avg = None # Wind Speed
# needs - parser    MPH_gust = None # Wind Gust Speed
    Wind_Angle = None # Degrees
    Rain = None # Inches

def day_weather(airport, date, opener=None):
    url = get_url(airport, date.year, date.month, date.day)

    if opener==None:
        opener = urllib2.build_opener()

    f = opener.open(url)

    print(date.strftime("parsing %Y-%m-%d")
    return np.loadtxt(f,
                      skiprows=2,
                      delimiter=',',
                      usecols=[1,2,3,4,5,9,12,13],
                      unpack=True,
                      converters = {13: compose(datestr2num,br_strip),
                                     3: NA2NaN,
                                     9: NA2NaN}
                      )

def interval_weather(airport, start, stop):
    """return a Weather object with all data from start to stop"""
    if stop < start:
        raise ReversedRange
    opener = urllib2.build_opener()
    day = datetime(1970,1,2) - datetime(1970,1,1)
    d = start
    ws = []
    while d<stop:
        ws.append(day_weather(airport, d, opener))
        d += day
    
    ret = Weather()
    ret.T, ret.Dp, ret.RH, ret.P, ret.Vis, ret.Rain, ret.Wind_Angle, ret.date = np.hstack(ws)
    return ret
    
def get_url(airport, year, month, day):
    return 'http://www.wunderground.com/history/airport/{}/{:02d}/{:02d}/{:02d}/DailyHistory.html?req_city=NA&req_state=NA&req_statename=NA&format=1'.format(airport, year, month, day)
