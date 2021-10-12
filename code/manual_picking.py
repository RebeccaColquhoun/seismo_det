import numpy as np
from earthquake import earthquake
import obspy
from obspy.clients.fdsn import Client
from datetime import timedelta
import matplotlib.pyplot as plt
import difflib
import os

#rootpath = '/Users/rebecca/Documents/PhD/Research/Frequency/Olsen and Allen/data3/'
#rootpath = '/home/earthquakes1/homes/Rebecca/phd/data/olsen_allen_2005_100_km/'
rootpath = '/Users/rebecca/Documents/PhD/Research/Frequency/olsen_allen_2005_100_km/'
#data = obspy.read("/Users/rebecca/Documents/PhD/Research/Frequency/Olsen and Allen/data2/2000-06-26T15:43:07.550000Z/mseed/*")
#time = data[0].stats.starttime + timedelta(minutes=5)
event_ids = [3031111, 3144585, 3231786, 7050470, 7062511, 9008753, 9044494, 9045109, 9108652, 3320848, 9108709, 9108775, 9109442, 9109636, 3321590, 9114812, 9140050, 9155518, 9163314, 9173365, 9628901, 9630113, 9639729, 9644101, 9653493, 9674213, 9674049, 10992159, 9703873, 9706897, 9716853, 9716861, 9722633, 9753485, 9753949, 9753489, 9755013, 12663484, 9775765, 9796589]
files =os.listdir(rootpath)

tp_estimates = []
count = 0
station_latitudes = []
station_longitudes = []
event_latitude = []
event_longitude = []
all_picks = []
for eq_number in range(23, len(event_ids)):
    failed = False
    try:
        print('in try')
        event_id = event_ids[eq_number] #9155518
        client = Client("SCEDC")
        cat = client.get_events(eventid=event_id, includearrivals=True)
        
        eq_name = str(cat[0].origins[0].time)
        #name = name[0:13]+'/'+name[14:16]+'/'+name[17:]
        filename = difflib.get_close_matches(eq_name, files)[0]
        data = obspy.read(rootpath+filename+"/mseed/*")
        time = data[0].stats.starttime + timedelta(minutes=5)
        print('details')


        #print(len(picks_available), len(data_with_picks))
        print('pick comparison')
        for tr in data:
            inv=obspy.read_inventory(rootpath+filename+"/stations/"+str(tr.stats.network)+"."+str(tr.stats.station)+'.xml')
            nyquist = tr.stats.sampling_rate/2
            tr.remove_response(inventory=inv, water_level=60, pre_filt=[0.025,0.05, 0.5*nyquist, 0.75*nyquist])#, output="DISP", plot=True)
    except:
        print('this eq doesnt quite work')
        failed = True
    if failed == False:
        eq_picks = {}
        i = 0
        while i < len(data):
            s_r = data[i].stats.sampling_rate
            if len(data)-i>=3 and ('.'.join([data[i].stats.network, data[i].stats.station]))==('.'.join([data[i+1].stats.network, data[i+1].stats.station])) and ('.'.join([data[i].stats.network, data[i].stats.station]))==('.'.join([data[i+2].stats.network, data[i+2].stats.station])): 
                print('in if')
                data[i:i+3].plot()
                fig, axs = plt.subplots(3,1, sharex=True)
                axs[0].plot(data[i].data[int(290*s_r):int(360*s_r)])
                axs[1].plot(data[i+1].data[int(290*s_r):int(360*s_r)])
                axs[2].plot(data[i+2].data[int(290*s_r):int(360*s_r)]) 
                skip = 3
            elif len(data)-i>=2 and ('.'.join([data[i].stats.network, data[i].stats.station]))==('.'.join([data[i+1].stats.network, data[i+1].stats.station])):
                print('in elif')
                data[i:i+2].plot()
                fig, axs = plt.subplots(2,1, sharex=True)
                axs[0].plot(data[i].data[int(290*s_r):int(360*s_r)])
                axs[1].plot(data[i+1].data[int(290*s_r):int(360*s_r)]) 
                skip = 2
            else: 
                print('in else')
                data[i].plot()
                fig, axs = plt.subplots(1,1, sharex=True)
                axs.plot(data[i].data[int(290*s_r):int(360*s_r)])
                skip = 1
            plt.show()
            pick_time = input()
            pick_time = float(pick_time)
            if pick_time > 0:
                eq_picks[str(data[i].stats.network)+"."+str(data[i].stats.station)] = pick_time
            i += skip
        all_picks.append([eq_name, eq_picks])
        

    print('yay 1 earthquake done, do you want to do another one? y/n')
    answer = input()
    if answer[0] == 'n':
        print('you got to earthquake number=' + str(eq_number))
        break