# coding=utf-8
# originally from http://stackoverflow.com/questions/5061446/api-with-past-weather
import urllib2
import numpy as np
from matplotlib.dates import datestr2num
import re
from functional import compose

def br_strip(str):
    return re.sub(r'<.*$', '', str)

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
# needs N/A parser    Rain = None # Inches

def day_weather(airport, date, opener=None):
    url = get_url(airport, date.year, date.month, date.day)

    if opener==None:
        opener = urllib2.build_opener()

    f = opener.open(url)

    return np.loadtxt(f,
                      skiprows=2,
                      delimiter=',',
                      usecols=[1,2,3,4,5,12,13],
                      unpack=True,
                      converters = {13: compose(datestr2num,br_strip)}
                      )
    
def get_url(airport, year, month, day):
    return 'http://www.wunderground.com/history/airport/{}/{:02d}/{:02d}/{:02d}/DailyHistory.html?req_city=NA&req_state=NA&req_statename=NA&format=1'.format(airport, year, month, day)
