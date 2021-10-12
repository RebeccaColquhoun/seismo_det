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


root = '/home/earthquakes1/homes/Rebecca/phd/data/AK_data_eqtransformer/'

eq_list = os.listdir(root)

client = Client("IRIS")
cat = client.get_events(starttime=UTCDateTime("2019-06-26"), endtime=UTCDateTime("2020-06-26"), minlongitude=-179, maxlongitude=-145, minlatitude=42, maxlatitude=71, minmagnitude=5, includearrivals=True)

list_tpmax = []
list_tc= []
list_mags = []
eqs = {}
for eq_name in eq_list:
    
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
    eqs[obj_name].calc_Tc()
    list_tpmax.append(eqs[obj_name]._cached_params["tau_p_max"])
    list_tc.append(eqs[obj_name]._cached_params["tau_c"])
    list_mags.append(eqs[obj_name].event.magnitudes[0].mag)

from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
import numpy as np
#figure(figsize=(3, 5), dpi = 400)
c = 0
cs = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']    
fig, axs = plt.subplots(1,2)
for i  in range(0, len(list_mags)):  
    mean_tp = np.mean(list_tpmax[i]) 
    std_tp = np.std(list_tpmax[i]) 
    y_tp = [] 
    for j in list_tpmax[i]: 
        if j > mean_tp-std_tp and j < mean_tp + std_tp and j < 10: 
            y_tp.append(j) 
    x_tp = np.zeros(len(y_tp))  
    x_tp = x_tp + list_mags[i]  
    
    mean_tc = np.mean(list_tc[i]) 
    std_tc = np.std(list_tc[i]) 
    y_tc = [] 
    for k in list_tc[i]: 
        if k > mean_tc-std_tc and k < mean_tc + std_tc and k < 10: 
            y_tc.append(k) 
    x_tc = np.zeros(len(y_tc))  
    x_tc = x_tc + list_mags[i]  
    if len(x_tp)>0 or len(x_tc)>0:
        axs[0].scatter(x_tp, y_tp, s = 15, alpha = 0.4, c = cs[c], marker = '*') 
        axs[0].scatter(list_mags[i], np.mean(y_tp), s = 50, c = cs[c], marker = '^')
        axs[0].scatter(list_mags[i], np.median(y_tp), s = 50, c = cs[c], marker = 's')
        axs[1].scatter(x_tc, y_tc, s = 15, alpha = 0.4, c = cs[c], marker = '*') 
        axs[1].scatter(list_mags[i], np.median(y_tc), s = 50, c = cs[c], marker = 's')
        axs[1].scatter(list_mags[i], np.mean(y_tc), s = 50, c = cs[c], marker = '^')
        c += 1
    
axs[0].set_yscale('log')
axs[1].set_yscale('log')
axs[0].set_xlabel("magnitude") 
axs[1].set_xlabel("magnitude") 
axs[0].set_ylabel("tp_max") 
axs[1].set_ylabel("tc")
axs[0].set_title("tp_max") 
axs[1].set_title("tc") 
fig.suptitle("mean values = triangle, median = square")
    