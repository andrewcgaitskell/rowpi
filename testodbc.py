import psycopg2

from sqlalchemy import create_engine

import pandas as pd

from pandas.io import sql

conn = psycopg2.connect('host=localhost user=andrew password=andrew dbname=test')

cur = conn.cursor()

cur.execute('select * from people')

results = cur.fetchall()

for result in results:
    print(result)

cur.close()
conn.close()    

####################### 

engine = create_engine('postgresql://andrew:andrew@localhost:5432/data')

sqlcmnd = 'SELECT stroketime, distance, spm, power, pace, calhr, calories, heartrate, status, rowingid FROM strokes.floats;'

df = pd.read_sql_query(sqlcmnd, engine)

print df
