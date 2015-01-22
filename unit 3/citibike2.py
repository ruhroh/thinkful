import requests
import pandas as pd
import sqlite3 as lite
from pandas.io.json import json_normalize
import time
from dateutil.parser import parse 
import collections

i = 0
while i < 60:
	i = i+1
	time.sleep(60)
	r = requests.get('http://www.citibikenyc.com/stations/json')
	df = json_normalize(r.json()['stationBeanList'])
	con = lite.connect('citi_bike.db')
	# Here you connect to the database. The `connect()` method returns a connection object.
	cur = con.cursor()
	# From the connection, you get a cursor object. The cursor is what goes over the records that result from a query.

	#extract the column from the DataFrame and put them into a list
	station_ids = df['id'].tolist() 

	#add the '_' to the station name and also add the data type for SQLite
	station_ids = ['_' + str(x) + ' INT' for x in station_ids]

	#create the table
	#in this case, we're concatentating the string and joining all the station ids (now with '_' and 'INT' added)
	with con:
		try:
			cur.execute("CREATE TABLE available_bikes ( execution_time INT, " +  ", ".join(station_ids) + ");")
		except lite.OperationalError:
			pass

	#take the string and parse it into a Python datetime object
	exec_time = parse(r.json()['executionTime'])
	print exec_time

	with con:
	    cur.execute('INSERT INTO available_bikes (execution_time) VALUES (?)', (exec_time.strftime('%s'),))
	    id_bikes = collections.defaultdict(int) #defaultdict to store available bikes by station

	#loop through the stations in the station list
	for station in r.json()['stationBeanList']:
	    id_bikes[station['id']] = station['availableBikes']

	#iterate through the defaultdict to update the values in the database
	with con:
	    for k, v in id_bikes.iteritems():
	        cur.execute("UPDATE available_bikes SET _" + str(k) + " = " + str(v) + " WHERE execution_time = " + exec_time.strftime('%s') + ";")