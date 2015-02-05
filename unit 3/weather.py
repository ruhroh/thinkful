import requests
import datetime
import pandas as pd

cities = {"Austin": '30.303936,-97.754355',
"Las Vegas": '36.229214,-115.26008',
"New York": '40.663619,-73.938589'}
#api https://api.forecast.io/forecast/e0daf4356175c660310724403ce660ef/37.8267,-122.423
#/forecast/ APIKEY / LAT, LONG, TIME
url = "https://api.forecast.io/forecast/e0daf4356175c660310724403ce660ef/" 
urlList = []
time = datetime.datetime.now()
ftime = time.strftime('%Y-%m-%dT%H:%M:%S')

for k, v in cities.iteritems():
	urlList.append(url + v + "," + ftime)

results=[]
for url in urlList:
	r = requests.get(url)
	r2 = r.json()
	results.append(r2)

print(urlList)