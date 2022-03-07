# -*- coding: utf-8 -*-
"""
SIS Eval
"""

from SISEval import SISEval
import datetime
import numpy as np
import pytz
import os
import multiprocessing

# read measurement function to be executed in parallel
def read_measurement(timezone,acc_secs,sensor,start_time_frame,shared_dir):
    i = 0
    # track time cut off with t0 (beginning of the time stamp)
    # is equal to the starting time frame right after starting the script
    time_cut = start_time_frame
    # main loop
    while 1:
        # get current timestamp with reference to raspi timezone
        curr_timestamp = datetime.datetime.now()
        # get current global time
        tz_object = pytz.timezone(timezone)
        # localize timestamp
        curr_local = tz_object.localize(curr_timestamp)
        # current time in UNIX Epoch
        curr_time = curr_local.timestamp()
        
        # start writing if we reach the starting time frame
        # Boolean if we created file for this epoch
        file_created = False
        # check if the current unix epoch time is larger than the starting time
        # and below the starting time plus the accumulation period
        if curr_time >= time_cut and curr_time < (time_cut + acc_secs):
            # check if we already created the file for this epoch
            if not file_created:
                # create file name consitsing of sensor number and
                # Unix epoch time stamp
                outdir = shared_dir + '/Sensor%s_%s' % (sensor.sensorID, int(time_cut))
                # open file with mode append and create if it doesnt exist
                f = open(outdir,'a+')
                # return that we sucessfully created the file
                file_created = True
            # read measurement data from sensor
            data = sensor.read()
            # write measurement data to file
            f.write('%s %s\n' % (data[0],data[1]))
        # if this is not true we have to update some things
        # we cant use else due to initialization
        if curr_time >= (time_cut + acc_secs):
            # close the currently opened file 
            f.close()
            # reset file created boolean
            file_created = False
            # update starting timestep
            time_cut = time_cut + acc_secs
            # count up i
            i+= 1
            if i == 3:
               break
        
# Main function
def main():
    # define timezone of Raspberry
    timezone = "ETC/GMT-1"
    # accumulate seconds
    acc_secs = 60
    # init sensors
    sensors = [SISEval.GenericSensor(1,timezone),
               SISEval.GenericSensor(2,timezone)]
    # Generate start time
    curr_timestamp = datetime.datetime.now()
    # localize timestamp
    time_zone_object = pytz.timezone(timezone)
    # current local
    curr_local = time_zone_object.localize(curr_timestamp)
    # get start time
    start_time = curr_local.timestamp()
    # correct start time to timeframe
    start_time_frame = np.ceil(start_time / acc_secs) * acc_secs
    # shared folder
    shared_dir = os.path.dirname(os.path.realpath(SISEval.__file__)) + '/shared'
    
    # start processes for each sensor in parallel
    for i in range(0,len(sensors)):
        # start processes in parallel
        p = multiprocessing.Process(target = read_measurement, args=(timezone,
                                                                     acc_secs,
                                                                     sensors[i],
                                                                     start_time_frame,
                                                                     shared_dir))
        p.start()
    # join results, actually not needed since processes never finish regularely
    p.join()
    
# Run main routine
if __name__ ==  '__main__':
    main()    

