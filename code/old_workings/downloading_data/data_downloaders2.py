#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 17:28:02 2021

@author: rebecca
"""

#https://docs.obspy.org/packages/autogen/obspy.clients.fdsn.mass_downloader.html#step-1-data-selection
import obspy
from obspy.clients.fdsn.mass_downloader import CircularDomain, Restrictions, MassDownloader
from obspy.clients.fdsn import Client
client = Client("SCEDC")
import numpy as np

# cal_event_catalog.clear()

#f = open('/home/earthquakes1/homes/Rebecca/phd/data/olsen_allen_2005/catalog_all.txt')
f = open('/Users/rebecca/Documents/PhD/Research/Frequency/Olsen and Allen/catalog_all.txt') 
lines = f.read().split("\n")
event_list = []
for a in lines:
    event_list.append(a.split(","))

cal_event_catalog = obspy.core.event.Catalog(None)

for i in event_list:
    lat = float(i[3])
    long = float(i[4])
    min_mag = float(i[6])-0.5
    t1 = UTCDateTime(i[2]) - timedelta(minutes=2)
    t2 = t1+timedelta(minutes=3)
    #if (lat > 30 and lat < 45) and (long > -120 and long < -110): #cal
    if (lat < 30 or lat > 45) or (long < -120 or long > -110): #not cal
        print('in if')
        print(i)
        try:    
            b = client.get_events(starttime=t1, endtime=t2, minmagnitude=min_mag, maxmagnitude=min_mag+1, latitude=lat, longitude=long, maxradius=1)
            print(b)
            cal_event_catalog.extend(b)
        except:
            print('failed')
            print(i)

print(str(cat[j].origins[0].time) +'    /    '+ str(cat[j].magnitudes[0].mag) +'    /    '+ str(cat[j].origins[0].latitude) +'    /    '+ str(cat[j].origins[0].longitude) +'    /    '+ str(cat[j].origins[0].depth)+'    /    '+str(cat[j].resource_id)[-7:])

cal_event_catalog = obspy.core.event.Catalog(None)
for i in event_ids:
    print(i)
    if len(str(i))>=7: 
        e = client.get_events(eventid = i, includearrivals=True)
        true_event_catalog.extend(e)

for i in e:# true_event_catalog:
    origin_time = i.origins[0].time

    # Circular domain around the epicenter. This will download all data between
    # 70 and 90 degrees distance from the epicenter. This module also offers
    # rectangular and global domains. More complex domains can be defined by
    # inheriting from the Domain class.
    domain = CircularDomain(latitude=i.origins[0].latitude, longitude=i.origins[0].longitude,
                            minradius=0, maxradius=1)

    restrictions = Restrictions(
        # Get data from 5 minutes before the event to half an hour after the
        # event. This defines the temporal bounds of the waveform data.
        starttime=origin_time - 5 * 60,
        endtime=origin_time + 1800,
        # You might not want to deal with gaps in the data. If this setting is
        # True, any trace with a gap/overlap will be discarded.
        reject_channels_with_gaps=True,
        # And you might only want waveforms that have data for at least 95 % of
        # the requested time span. Any trace that is shorter than 95 % of the
        # desired total duration will be discarded.
        minimum_length=0.95,
        # No two stations should be closer than 1 km to each other. This is
        # useful to for example filter out stations that are part of different
        # networks but at the same physical station. Settings this option to
        # zero or None will disable that filtering.
        minimum_interstation_distance_in_m=0, #10E3,
        # Only HH or BH channels. If a station has HH channels, those will be
        # downloaded, otherwise the BH. Nothing will be downloaded if it has
        # neither. You can add more/less patterns if you like.
        channel_priorities=["HH[ZNE]", "BH[ZNE]"],
        # Location codes are arbitrary and there is no rule as to which
        # location is best. Same logic as for the previous setting.
        location_priorities=["", "00", "10"])

    # No specified providers will result in all known ones being queried.
    mdl = MassDownloader()
    # The data will be downloaded to the ``./waveforms/`` and ``./stations/``
    # folders with automatically chosen file names.
    # mseed_storage_name = ("/home/earthquakes1/homes/Rebecca/phd/data/olsen_allen_2005_cal/mseed/{starttime}/{network}.{station}.{location}.{channel}.mseed")
    # mdl.download(domain, restrictions, mseed_storage="/home/earthquakes1/homes/Rebecca/phd/data/olsen_allen_2005_cal/"+str(origin_time)+"/mseed/",
                 # stationxml_storage="/home/earthquakes1/homes/Rebecca/phd/data/olsen_allen_2005_cal/"+str(origin_time)+"/stations/")
    '''mseed_storage_name = ("/home/earthquakes1/homes/Rebecca/phd/data/olsen_allen_2005_100_km/mseed/{starttime}/{network}.{station}.{location}.{channel}.mseed")
    mdl.download(domain, restrictions, mseed_storage="/home/earthquakes1/homes/Rebecca/phd/data/olsen_allen_2005_100_km/"+str(origin_time)+"/mseed/",
                 stationxml_storage="/home/earthquakes1/homes/Rebecca/phd/data/olsen_allen_2005_100_km/"+str(origin_time)+"/stations/")'''
    mseed_storage_name = ("/Users/rebecca/Documents/PhD/Research/Frequency/alaska_2020_100_km/mseed/{starttime}/{network}.{station}.{location}.{channel}.mseed")
    mdl.download(domain, restrictions, mseed_storage="/Users/rebecca/Documents/PhD/Research/Frequency/alaska_2020_100_km/"+str(origin_time)+"/mseed/",
                 stationxml_storage="/Users/rebecca/Documents/PhD/Research/Frequency/alaska_2020_100_km/"+str(origin_time)+"/stations/")


def make_obspyDMT_search(event_catalog):
    for i in event_catalog:
        lat1 = np.floor(i.origins[0].latitude)
        lat2 = np.floor(i.origins[0].latitude)+1
        long1 = np.floor(i.origins[0].longitude)
        long2 = np.floor(i.origins[0].longitude)+1
        event_rect = str(min(long1, long2))+"/"+str(max(long1, long2))+"/"+str(min(lat1, lat2))+"/"+str(max(lat1, lat2))
        min_mag = np.floor(i.magnitudes[0].mag)
        t = i.origins[0].time
        min_year = t.year
        min_month = t.month
        min_day = t.day
        min_date = str(min_year)+"-"+str(min_month)+"-"+str(min_day)
        t2 = t+timedelta(days=1)
        max_year = t2.year
        max_month = t2.month
        max_day = t2.day
        max_date = str(max_year)+"-"+str(max_month)+"-"+str(max_day)
        query = "obspyDMT --datapath olsen_allen_2005 --event_catalog IRIS --data_source IRIS --max_epi 1 --min_mag " + str(min_mag) + " --min_date " + min_date + " --max_date " + max_date + " --event_rect " + event_rect
        print(query)

def pick_japan_data():
    picks_dict = {}
    event_lat = 38.806
    event_long = 141.683
    #f = io.open("/Users/rebecca/Documents/PhD/Research/Frequency/japan_data/pick_info.txt", mode="r", encoding="utf-16")
    f = io.open("/Users/rebecca/Documents/PhD/Research/Frequency/Tokachi-Oki/picks.txt")
    lines = f.read().split("\n")
    for i in lines:
        entry = i
        picks_dict[entry[1:7]]=entry[19:27]
    #sac_data = obspy.read("/Users/rebecca/Documents/PhD/Research/Frequency/japan_data/*.SAC")
    sac_data = obspy.read("/Users/rebecca/Documents/PhD/Research/Frequency/Tokachi-Oki/*.SAC")
    picked_data = obspy.core.stream.Stream()
    nearby_data = obspy.core.stream.Stream()
    stations = []
    lat = []
    long = []
    for component in sac_data:
        try:
            sta = component.stats.station
            if len(sta)<6:
                sta = sta+' '*(6-len(sta))
            pick = picks_dict[sta]
            time_pick = UTCDateTime(str(component.stats.starttime.year)+str(component.stats.starttime.month)+str(component.stats.starttime.day)+pick[:-2]+'.'+pick[-2:])
            component.stats.t0 = time_pick
            picked_data.append(component)
            stations.append(component.stats.station)
            long.append(component.stats.sac['stlo'])
            lat.append(component.stats.sac['stla'])
            distance = math.sqrt((component.stats.sac['stlo']-event_long)**2+(component.stats.sac['stla']-event_lat)**2)
            if distance<1:
                nearby_data.append(component)
        except:
            print('failed')
            
    #for i in picked_data:
       # stations.append(i.stats.station)
       # long.append(i.stats.sac['stlo'])
       # lat.append(i.stats.sac['stla'])
    ax = plt.gca()
    circle1 = plt.Circle((141.683, 38.806), 1, color='r', alpha=0.3)
    ax.scatter(long, lat, marker='.')
    ax.scatter(event_long, event_lat, color='blue')
    ax.add_patch(circle1)
    plt.title("EVENT: 2003/05/26 18:24:33.47 38.806N/141.683E/70.7km")
    plt.show()
    
    data = nearby_data
    tau_p_list = []
    tp_max = []
    for i in range(0, len(data)):  # iterate through all traces
        if data[i].stats.channel == 'U':  # only use vertical components
            #print('in if')
            tr = data[i].copy()
            tr.filter('lowpass', freq=3)
            sampling_rate = tr.stats.sampling_rate
            #pick = picks[i]
            pick = 1340
            start_time = tr.stats.starttime
            tr.data[0:int((pick-start_time)*sampling_rate)] = 0
            if sampling_rate == 100:
                alpha = 0.99
            elif sampling_rate == 20:
                alpha = 0.95
            x = tr.data
            diff = (tr.differentiate()).data
            X = np.zeros(len(x))
            D = np.zeros(len(x))
            start = int((tr.stats.t0 - tr.stats.starttime)*sampling_rate)
            end = int(start + 4 * sampling_rate)
            for t in range(0, len(tr.data)):
                X[t] = alpha*X[t-1]+x[t]**2
                D[t] = alpha*D[t-1]+diff[t]**2
            tau_p = 2 * np.pi * np.sqrt(X/D)
            tau_p_list.append(tau_p[int(start):int(end)])
            #print(max(tau_p[int(start+0.2*sampling_rate):int(end)]))
            tp_max.append(max(tau_p[int(start+0.5*sampling_rate):int(end)]))


for i in tau_p_list:
    plt.plot(i)
    plt.axvspan(0, 5, alpha=0.5, color='red')
    plt.axvspan(0, 10, alpha=0.3, color='red')
    plt.axvspan(0, 20, alpha=0.2, color='red')
    plt.axvspan(0, 50, alpha=0.1, color='red') 




def acc_to_vel(a):
    q=0.998
    dt = 0.01
    v = np.zeros(len(a))
    for j in range(1, len(a)):
        v[j] = ((1+q)/2)*((a[j]+a[j-1])/2)*dt + q*v[j-1]
    return v


starttime = UTCDateTime("2019-06-26") 
endtime  = UTCDateTime("2020-06-26")
minlatitude = 71
maxlatitude = 42
minlongitude = 177.99
maxlongitude = -146.76
cat = client.get_events(starttime=starttime, endtime=endtime, minmagnitude=5, minlatitude = 71, maxlatitude = 42, minlongitude = 177.99, maxlongitude = -146.76)