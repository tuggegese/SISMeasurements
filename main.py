# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 11:15:51 2022

@author: gegese
"""

from SISEval import SISEval

timezone = "ETC/GMT-1"

# init Sensors
# sensor 1

sensor1 = SISEval.GenericSensor(timezone)

sensor2 = SISEval.GenericSensor(timezone)


while 1:
    data = sensor1.read()
    
    data2 = sensor2.read()
    print('data produced by sensor 1')
    print(data)
    print('data produced by sensor 2')
    print(data2)
    
    

