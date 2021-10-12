#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 23 09:48:53 2021

@author: rebecca
"""

from earthquake import earthquake
import os
import obspy
import pickle
from obspy import UTCDateTime
from obspy.clients.fdsn import Client
import datetime
from datetime import timedelta

def filenameToDate(filename):
    year = int(filename[0:4])
    month = int(filename[4:6])
    day = int(filename[6:8])
    hour = int(filename[9:11])
    minute = int(filename[11:13])
    second = int(filename[13:15])
    date = datetime.datetime(year, month, day, hour, minute, second)
    return date


root = '/home/earthquakes1/homes/Rebecca/phd/data/2019_global_m5/'

eq_list = os.listdir(root)

client = Client("IRIS")
cat = client.get_events(starttime=UTCDateTime("2019-01-01"), endtime=UTCDateTime("2020-01-01"), minmagnitude=5, includearrivals=True)

list_tpmax = []
list_mags = []
eqs = {}
for eq_name in eq_list[0:10]:
    
    d = filenameToDate(eq_name)
    
    filter_start = str(UTCDateTime(d-timedelta(seconds=1)))
    filter_stop = str(UTCDateTime(d+timedelta(seconds=1)))
    
    event = cat.filter('time > ' + filter_start, 'time < ' + filter_stop)
    print(event)
    data = obspy.read(root+eq_name+'/data/*/*')
    with open(root+eq_name+'/picks.pkl', 'rb') as f:
        picks = pickle.load(f)
    obj_name = eq_name[0:-2]
    eqs[obj_name] = earthquake(eq_name, event, data, picks, sensor_types = [])
    eqs[obj_name].calc_Tpmax()
    list_tpmax.append(eqs[obj_name]._cached_params["tau_p_max"])
    list_mags.append(eqs[obj_name].event.magnitudes[0].mag)

from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
figure(figsize=(3, 5), dpi = 400)

for i  in range(0, len(list_mags)):  
    mean = np.mean(list_tpmax[i]) 
    std = np.std(list_tpmax[i]) 
    y = [] 
    for j in list_tpmax[i]: 
        if j > mean-std and j < mean + std and j < 10: 
            y.append(j) 
    x = np.zeros(len(y))  
    x = x + list_mags[i]  
    plt.scatter(x, y, s = 15, alpha = 0.4, c = 'orange', marker = '*') 
    plt.scatter(list_mags[i], np.mean(y), s = 50, c = 'orange', marker = '^')
plt.yscale('log')
    
    