# -*- coding: utf-8 -*-
"""
    Python wrapper
"""

from ina219 import INA219
import pytz
import datetime
import random
import numpy as np
import time
import os

# Sensor class for realtime measurements
class Sensor:
    # init
    def __init__(self, sensorID,SHUNT_OHMS, MAX_EXPECTED_AMPS, address,SENSITIVITY,rptime):
        # sensor settings
        self.SHUNT_OHMS = SHUNT_OHMS
        self.MAX_EXPECTED_AMPS = MAX_EXPECTED_AMPS
        self.address = address
        self.SENSITIVITY = SENSITIVITY
        
        self.sensorID = sensorID
        
        # init sensor
        self.ina = INA219(self.SHUNT_OHMS,self.MAX_EXPECTED_AMPS,address = self.address)
        
        # configure sensor
        self.ina.configure(ina.RANGE_16V,ina.GAIN_AUTO,ina.ADC_12BIT)
        
        self.timezone = pytz.timezone("GMT-1")
    
    def read(self):
        # read current timestamp in time of sensor
        timestamp = datetime.datetime.now()
        # localize datetime object
        time_local = self.timezone.localize(timestamp)
        # convert to unix epoch timestamp
        time_unix = time_local.timestamp()
        
        # read acceleration value 
        sens_acc_y = (self.ina.current() - 12.0) / self.SENSITIVITY
        
        return time_unix,sens_acc_y
        

# Generates a random measurement signal defined by previously conducted measurements
# the readings are classified between -5 and -13, the weights are computed from the occurances
class GenericSensor:
    # init
    def __init__(self, sensorID,rptime):
        # init timezone
        self.timezone = pytz.timezone(rptime)
        
        self.sensorID = sensorID
        
        # sample list from previously conducted measurements
        self.sample_list = np.array([-5.5,-6.5,-7.5,-8.5,-9.5,-15.0,-11.5,-12.5])
        self.weights = np.array([0.2,0.2,23.31,71.27,4.42,0.2,0.2,0.2])   

    def read(self):
        # read current timestamp in time of sensor
        timestamp = datetime.datetime.now()
        # localize datetime object
        time_local = self.timezone.localize(timestamp)
        # convert to unix epoch timestamp
        time_unix = time_local.timestamp()
        
        # "read" value greate random signal
        # get random reading between previously defined classes
        reading = random.choices(self.sample_list, weights = self.weights, cum_weights = None,k=1)[0]
        # correct by random distance between classes
        reading = reading + random.uniform(-0.5, 0.5)
        
        # sleep for 1/10000 of a second
        time.sleep(0.0001)
        
        return time_unix, reading
    
class MeasurementFilter:
    # init
    def __init__(self, resamp, thres_wave, filter_frequ, order, meas_frequ, thres_ave):
        # Settings for resampling of measurement points
        # Resample timeseries in points/seconds
        self.resamp = resamp
        
        # Settings for wavelet transformation
        # threshold for wavelet filter
        self.thres_wave = thres_wave
        
        # Settings for Butterworth high pass filter
        self.filter_frequ = filter_frequ
        self.order = order
        self.meas_frequ = meas_frequ
        
        # Settings for accumulation
        self.thres_ave = thres_ave


