import requests
import datetime
import pandas as pd
import sqlite3 as lite

cities = {"ATX": '30.303936,-97.754355',
"LV": '36.229214,-115.26008',
"NYC": '40.663619,-73.938589'}
#api https://api.forecast.io/forecast/e0daf4356175c660310724403ce660ef/37.8267,-122.423
#/forecast/ APIKEY / LAT, LONG, TIME

end_date = datetime.datetime.now() # by setting this equal to a variable, we fix the calculation to the point when we started the scrip (rather than have things move aroudn while we're coding.)
api_key = "e0daf4356175c660310724403ce660ef/"
url = 'https://api.forecast.io/forecast/' + api_key
query_date = end_date - datetime.timedelta(days=30) 

con = lite.connect('weather.db')
	# Here you connect to the database. The `connect()` method returns a connection object.
cur = con.cursor()
	# From the connection, you get a cursor object. The cursor is what goes over the records that result from a query.

with con:
	try:
    		cur.execute('CREATE TABLE daily_temp (day_of_reading INT, LV REAL, ATX REAL, NYC REAL);') #use your own city names instead of city1...
	except lite.OperationalError:
		pass

with con:
    while query_date < end_date:
        cur.execute("INSERT INTO daily_temp(day_of_reading) VALUES (?)", (int(query_date.strftime('%s')),))
        query_date += datetime.timedelta(days=1)

for k,v in cities.iteritems():
    query_date = end_date - datetime.timedelta(days=30) #set value each time through the loop of cities
    while query_date < end_date:
        #query for the value
        r = requests.get(url + v + ',' +  query_date.strftime('%Y-%m-%dT12:00:00'))
        with con:
            #insert the temperature max to the database
            query = 'UPDATE daily_temp SET ' + k + ' = ' + str(r.json()['daily']['data'][0]['temperatureMax']) + ' WHERE day_of_reading = ' + query_date.strftime('%s')
            cur.execute(query)
            print(query)

        #increment query_date to the next day for next operation of loop
        query_date += datetime.timedelta(days=1) #increment query_date to the next day

con.close()