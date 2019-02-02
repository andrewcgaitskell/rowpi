import pyrow
import time

import psycopg2
import datetime

from sqlalchemy import create_engine

import pandas as pd

from pandas.io import sql

##### hr stuff ####

import struct
import bluepy.btle as btle
import sys
from time import sleep

import atexit


heartrate_uuid = btle.UUID(0x2a37)

# Address of BLE device to connect to.
BLE_ADDRESS = "00:22:D0:2A:7F:99" # changed this to my own
# BLE heart rate service - 180d
BLE_SERVICE_UUID ="0000180d-0000-1000-8000-00805f9b34fb"
# Heart rate measurement that notifies - 2a37
BLE_CHARACTERISTIC_UUID= "00002a37-0000-1000-8000-00805f9b34fb";


#####


engine = create_engine('postgresql://pi:pi@localhost:5432/rowingdata')
sqlcmnd_data = 'SELECT stroketime, distance, spm, power, pace, calhr, calories, heartrate, status, rowingid'
sqlcmnd_data = sqlcmnd_data + ' FROM data.strokes;'

conn = psycopg2.connect('host=localhost user=pi password=raspberry dbname=rowingdata')
cur = conn.cursor()

query = """
    insert into data.strokes values %s
    returning *
"""

forceplotquery = """
    insert into data.forceplot(rowid,force,id,strokeid) values %s
    returning *
    """

#my_tuple = (2, 'b')

#cursor.execute(query, (my_tuple,)) # Notice the comma after my_tuple
#rs = cursor.fetchall()
#conn.commit()
#for row in rs:
#    print row

#cur = conn.cursor()

#cur.execute('select * from people')

############################
## https://github.com/danielfppps/hbpimon/blob/master/hb.py


class heartMonitor:
    def __init__(self, mac):
        try:
            self.p = btle.Peripheral(mac)
            self.p.setDelegate(heartDelegate())
        except Exception as e:
            print str(e)
            self.p = 0
            print "Not connected"

    def startMonitor(self):
        try:
            self.p.writeCharacteristic(0x12, struct.pack('<bb', 0x01, 0x00), False)
            self.p.writeCharacteristic(0x11, '\x04', False)
        except:
            e = sys.exc_info()[0]
            print("HeartMonitor Error: %s" % e)
            try:
                self.p.disconnect()
            except:
                return 0

    def getHeartbeat(self):
        try:
            self.p.waitForNotifications(1.0)
            return self.p.delegate.getlastbeat()
        except:
            return 0

    def stopMonitor(self):
        self.p.writeCharacteristic(0x11, '\x00', False)


class heartDelegate(btle.DefaultDelegate):
    message = 0

    def __init__(self):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        if(data[0] == '\x14'):
            self.message = "Connection Lost"
        if(data[0] == '\x16'):
            self.message = str(struct.unpack("B", data[1])[0])
        if(data[0] == '\x06'):
            self.message = "Booting"

    def getlastbeat(self):
        return self.message

##hrm = heartMonitor(BLE_ADDRESS)
##hrm.startMonitor()

######################################

def ConnectToErg():
    #Connecting to erg
    ergs = list(pyrow.find())
    if len(ergs) == 0:
        exit("No ergs found.")

    erg = pyrow.pyrow(ergs[0])
    print "Connected to erg."
    return erg
  
def Workout(erg_in, hrm_in):
    try:
        #Loop until workout has begun
        workout = erg_in.get_workout()
        print "Waiting for workout to start ..."
        while workout['state'] == 0:
            time.sleep(1)
            workout = erg_in.get_workout()
        print "Workout has begun"
        rowingid = datetime.datetime.utcnow().isoformat()

        stroke_counter = 0

        #Loop until workout ends
        while workout['state'] == 1:

            forceplot = erg_in.get_force_plot()
            #Loop while waiting for drive
            while forceplot['strokestate'] != 2 and workout['state'] == 1:
                #ToDo: sleep?
                forceplot = erg_in.get_force_plot()
                workout = erg_in.get_workout()

            #Record force data during the drive
            force = forceplot['forceplot'] #start of pull (when strokestate first changed to 2)
            monitor = erg_in.get_monitor() #get monitor data for start of stroke
            #Loop during drive
            while forceplot['strokestate'] == 2:
                #ToDo: sleep?
                forceplot = erg_in.get_force_plot()
                force.extend(forceplot['forceplot'])
            #Write data to write_file

            try:
                read = hrm_in.getHeartbeat()
                hb = int(read)
            except Exception as e:
                hb = 0

            time_str = str(monitor['time'])
            distance_str = str(monitor['distance'])
            spm_str = str(monitor['spm'])
            power_str = str(monitor['power'])
            pace_str = str(monitor['pace'])
            calhr_str = str(monitor['calhr'])
            calories_str = str(monitor['calories'])
            ##heartrate_str = str(monitor['heartrate'])
            heartrate_str = str(hb)
            status_str = str(monitor['status'])

            time_float = float(time_str)
            distance_float = float(distance_str)
            spm_float = float(spm_str)
            power_float = float(power_str)
            pace_float = float(pace_str)
            calhr_float = float(calhr_str)
            calories_float = float(calories_str)
            heartrate_float = float(heartrate_str)
            status_float = float(status_str)

            workouttuple_float = (time_float,distance_float,spm_float,power_float,pace_float,calhr_float,calories_float,heartrate_float,status_float,rowingid)

            forcedata = ";".join([str(f) for f in force])   

            print(force)

            i = 0

            for f in force:
                i=i+1
                forcetuple = (rowingid,f,i,stroke_counter)
                cur.execute(forceplotquery, (forcetuple,))

            conn.commit()   


            workouttuple = (time_str,distance_str,spm_str,power_str,pace_str,calhr_str,calories_str,heartrate_str,status_str,rowingid)

            workoutdata = ','.join(workouttuple)

            cur.execute(query, (workouttuple,))
            conn.commit()



            #Get workout conditions
            workout = erg_in.get_workout()
            stroke_counter = stroke_counter + 1
            print stroke_counter

            #df = pd.read_sql_query(sqlcmnd_data, engine)


        print "Workout has ended"

        Workout(erg_in,hrm_in)
        
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
   
    erg_out = ConnectToErg()
    hrm = heartMonitor(BLE_ADDRESS)
    hrm.startMonitor()
    Workout(erg_out,hrm)




