#!/usr/bin/env python
#Copyright (c) 2011, Sam Gambrell
#Licensed under the Simplified BSD License.

#This is an example file to show how to make use of pyrow
#Have the rowing machine on and plugged into the computer before starting the program
#The program will record Time, Distance, SPM, Pace, and Force Data for each
#stroke and save it to 'workout.csv'

#NOTE: This code has not been thoroughly tested and may not function as advertised.
#Please report and findings to the author so that they may be addressed in a stable release.

import pyrow
import time

import psycopg2

conn = psycopg2.connect('host=localhost user=andrew password=andrew dbname=data')
cur = conn.cursor()

query = """
    insert into strokes.floats values %s
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


if __name__ == '__main__':

    #Connecting to erg
    ergs = list(pyrow.find())
    if len(ergs) == 0:
        exit("No ergs found.")

    erg = pyrow.pyrow(ergs[0])
    print "Connected to erg."

    #Open and prepare file
    write_file = open('workout.csv', 'w')
    #write_file.write('Time, Distance, SPM, Pace, Force Plot\n')
    #write_file.write('Time, Distance, SPM, Pace\n')
    write_file.write('time,distance,spm,power,pace,calhr,calories,heartrate,status\n')
    
    #Loop until workout has begun
    workout = erg.get_workout()
    print "Waiting for workout to start ..."
    while workout['state'] == 0:
        time.sleep(1)
        workout = erg.get_workout()
    print "Workout has begun"

    #Loop until workout ends
    while workout['state'] == 1:

        forceplot = erg.get_force_plot()
        #Loop while waiting for drive
        while forceplot['strokestate'] != 2 and workout['state'] == 1:
            #ToDo: sleep?
            #forceplot = erg.get_force_plot()
            workout = erg.get_workout()

        #Record force data during the drive
        force = forceplot['forceplot'] #start of pull (when strokestate first changed to 2)
        monitor = erg.get_monitor() #get monitor data for start of stroke
        #Loop during drive
        #while forceplot['strokestate'] == 2:
            #ToDo: sleep?
            #forceplot = erg.get_force_plot()
            #force.extend(forceplot['forceplot'])

        #forceplot = erg.get_force_plot()
        #force.extend(forceplot['forceplot'])

        #Write data to write_file
        
        time_str = str(monitor['time'])
        distance_str = str(monitor['distance'])
        spm_str = str(monitor['spm'])
        power_str = str(monitor['power'])
        pace_str = str(monitor['pace'])
        calhr_str = str(monitor['calhr'])
        calories_str = str(monitor['calories'])
        heartrate_str = str(monitor['heartrate'])
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
	
	workouttuple_float = (time_float,distance_float,spm_float,power_float,pace_float,calhr_float,calories_float,heartrate_float,status_float)
	
	
        #forceplot_str = str(monitor['forceplot'])
        #strokestate_str = str(monitor['strokerate'])
        
        # write data into database
        
        #sqlcmnd = "INSERT INTO strokes.raw('
	    #sqlcmnd = sqlcmnd + 'time,distance, spm, power, pace, calhr, calories, heartrate, status)'
	    #sqlcmnd = sqlcmnd + VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        
        
        
        #Write data to write_file
        
        workouttuple = (time_str,distance_str,spm_str,power_str,pace_str,calhr_str,calories_str,heartrate_str,status_str)
        workoutdata = ','.join(workouttuple)
        
        cur.execute(query, (workouttuple_float,))
        conn.commit()
        
        write_file.write(workoutdata+'\n') 
        
        #workoutdata = str(monitor['time']) + "," + str(monitor['distance']) + "," + \
        #    str(monitor['spm']) + "," + str(monitor['pace']) + ","

        #forcedata = ",".join([str(f) for f in force])
        #write_file.write(workoutdata + forcedata + '\n')
        #write_file.write(workoutdata + '\n')
        
        #Get workout conditions
        workout = erg.get_workout()

    write_file.close()
    
    cur.close()
    conn.close()
    
    print "Workout has ended"
