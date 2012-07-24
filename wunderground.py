# originally from http://stackoverflow.com/questions/5061446/api-with-past-weather
import urllib2
import csv 
import datetime

"""Gets daily temperatures from Weather Underground"""

def get_temperature_data(airport, date):
    url = get_url(airport, date.year, date.month, date.day)
    proxy_handler = urllib2.ProxyHandler({'http': 'http://user:pass@proxy.domain.com:3128'})

    opener = urllib2.build_opener(proxy_handler)

    data = []

    f = opener.open(url)
    reader = csv.reader(f)
    for row in reader:
        if len(row) > 1:
            # print row[0], row[1]
            try:
                time = datetime.datetime.strptime(row[0],"%I:%M %p")
                dt = datetime.datetime.combine(date.date(), time.time()) 
                temp = float(row[1])
                # print dt, temp
                data.append({'time':dt, 'temperature':temp})
            except ValueError, e:
                # ignore parsing errors
                pass
            except Exception, e:
                print e
                raise

    return data

def get_url(airport, year, month, day):
    return 'http://www.wunderground.com/history/airport/{}/{:02d}/{:02d}/{:02d}/DailyHistory.html?req_city=NA&req_state=NA&req_statename=NA&format=1'.format(airport, year, month, day)
