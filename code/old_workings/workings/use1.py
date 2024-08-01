#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  5 16:30:46 2021

@author: rebecca
"""
import numpy as np
from obspy.clients.fdsn.mass_downloader import CircularDomain, Restrictions, MassDownloader
from earthquake import earthquake
import matplotlib.pyplot as plt
from obspy.clients.fdsn import Client

st = obspy.read('/Users/rebecca/Documents/PhD/Research/Frequency/Olsen and Allen/data/2000-06-26T15:43:07.550000Z/mseed/*')
inv = obspy.read_inventory('/Users/rebecca/Documents/PhD/Research/Frequency/Olsen and Allen/data/2000-06-26T15:43:07.550000Zstations/CI.ISA.xml')

st2= st.copy()

rootpath = '/Users/rebecca/Documents/PhD/Research/Frequency/Olsen and Allen/data/'
event_file = '1992-06-28T11:57:34.130000Z'
data = obspy.read(rootpath+event_file+'/mseed/*')
for tr in data:
    inv=obspy.read_inventory(rootpath+event_file+'/stations/'+str(tr.stats.network)+"."+str(tr.stats.station)+'.xml')
    tr.remove_response(inventory=inv)
    data.plot()

event_id = 9155518
client = Client("SCEDC")
cat = client.get_events(eventid=9155518, includearrivals=True)


for i in range(0, len(cat[0].picks)):
    print(cat[0].picks[i].waveform_id.network_code, cat[0].picks[i].waveform_id.station_code)
    if cat[0].picks[0].waveform_id.network_code == "CI" and cat[0].picks[0].waveform_id.station_code=="ISA":
        print('pick')


eq = earthquake('test', st[0].stats.starttime, data)

eq.pgv
eq.calc_picks()
eq.calc_Tpmax()


data = eq.data
time = eq.time
picks = eq.picks
picks = [6740, 6740, 6740, 6520, 6520, 6520, 6880, 6880, 6880, 6240, 6240, 6240]
tau_p_list = []
for i in range(0, len(data)):  # iterate through all traces
    if data[i].stats.channel[2] == 'Z':  # only use vertical components
        tr = data[i]
        tr.filter('lowpass', freq=3)
        sampling_rate = tr.stats.sampling_rate
        if sampling_rate == 100:
            alpha = 0.99
        elif sampling_rate == 20:
            alpha = 0.95
        x = tr.data
        diff = (tr.differentiate()).data
        X = np.zeros(len(x))
        D = np.zeros(len(x))
        for t in range(0, len(tr.data)):
            X[t] = alpha*X[t-1]+x[t]**2
            D[t] = alpha*D[t-1]+diff[t]**2
        tau_p = 2 * np.pi * np.sqrt(X/D)
        tau_p_list.append(tau_p)
        start = picks[i]
        end = int(start + 4 * sampling_rate)
        print(max(tau_p[start:end]))






