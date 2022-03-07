# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 11:15:51 2022

@author: gegese
"""

from SISEval import SISEval
import datetime

timezone = "ETC/GMT-1"

# init Sensors
# sensor 1

sensor1 = SISEval.GenericSensor(timezone)

sensor2 = SISEval.GenericSensor(timezone)

resamp = 50000
thres_wave = 0.02
filter_frequ = 200
order = 5
meas_frequ = 1000
thres_ave = 0.1

measfilter = SISEval.MeasurementFilter(resamp, thres_wave,filter_frequ,order, meas_frequ,thres_ave)


# 1 Minute





while 1:
    data = sensor1.read()
    
    data2 = sensor2.read()
    print('data produced by sensor 1')
    print(data)
    print('data produced by sensor 2')
    print(data2)
    
    

