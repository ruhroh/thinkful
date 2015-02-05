import pandas as pd
import sqlite3 as lite
import collections

con = lite.connect('weather.db')
cur = con.cursor()

df = pd.read_sql_query("SELECT * FROM daily_temp ORDER BY day_of_reading", con, index_col='day_of_reading')

for col in df.columns:
	station_vals = df[col].tolist()
	station_id = col
	station_change = 0
	city = []
	for k,v in enumerate(station_vals):
		if k < len(station_vals) - 1:
			station_change = abs(station_vals[k] - station_vals[k+1])
		a = station_change
		city.append(a)
	print "For %s, the max change in temperature between any two continuous days is %s degrees C" % (station_id, max(city))

