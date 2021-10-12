
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

iris_event_ids = [1403125,838326, 838398, 838446, 910375, 1121573, 1314687, 3287118, 1536066, 976427, 877061, 890803, 1016306, 1198237, 1116982, 1400015, 1575824, 1640816, 1634667, 1635243, 1654704, 1635699, 1695746]

my_picks_list = [['1992-06-28T11:57:34.130000Z', {'CI.PFO': 432.0}],
                 ['1994-01-17T12:30:55.390000Z', {'CI.PAS': 331.0, 'CI.SBC': 575.0}],
                 ['1995-09-20T23:27:36.270000Z', {'CI.GSC': 505.0}],
                 ['1996-11-27T20:17:24.110000Z', {'CI.GPO': 366.0}],
                 ['1997-03-18T15:24:47.720000Z', {'CI.GPO': 561.0, 'CI.GSC': 334.0}],
                 ['1997-04-26T10:37:30.670000Z',
                  {'CI.OSI': 300.0, 'CI.PAS': 377.0, 'CI.SBC': 515.0}],
                 ['1998-03-06T05:47:40.340000Z',
                  {'CI.OSI': 294.0, 'CI.PAS': 375.0, 'CI.SBC': 515.0}],
                 ['1998-03-07T00:36:46.840000Z',
                  {'CI.OSI': 299.0, 'CI.PAS': 375.0, 'CI.SBC': 514.0}],
                 ['1999-10-16T09:46:44.460000Z', {'CI.GSC': 552.0, 'CI.HEC': 1554.0}],
                 ['1999-10-16T09:59:35.210000Z',
                  {'CI.BKR': 2187.0, 'CI.DAN': 2425.0, 'CI.GSC': 485.0, 'CI.HEC': 1380.0}],
                 ['1999-10-16T10:20:52.660000Z',
                  {'AZ.BZN': 2810.0,
                   'AZ.FRD': 2758.0,
                   'AZ.PFO': 2468.0,
                   'AZ.SND': 2681.0,
                   'AZ.WMC': 2685.0,
                   'CI.BC3': 2710.0,
                   'CI.BKR': 2703.0,
                   'CI.DAN': 2324.0,
                   'II.PFO': 494.0}],
                 ['1999-10-16T11:26:05.380000Z',
                  {'CI.BKR': 1906.0, 'CI.DAN': 2221.0, 'CI.GSC': 427.0}],
                 ['1999-10-16T20:13:37.640000Z',
                  {'CI.BKR': 2133.0,
                   'CI.DAN': 2416.0,
                   'CI.DEV': 2531.0,
                   'CI.GSC': 484.0,
                   'CI.MGE': 2744.0}],
                 ['1999-10-16T22:53:41.270000Z',
                  {'CI.BKR': 2129.0,
                   'CI.DAN': 2504.0,
                   'CI.DEV': 2479.0,
                   'CI.GSC': 458.0,
                   'CI.MGE': 2681.0}],
                 ['1999-10-21T01:54:34.180000Z', {'CI.DAN': 426.0, 'CI.GSC': 410.0}],
                 ['1999-10-22T16:08:48.060000Z', {'CI.DAN': 536.0, 'CI.GSC': 413.0}],
                 ['2000-02-21T13:49:43.130000Z',
                  {'AZ.BZN': 2361.0,
                   'AZ.CRY': 2186.0,
                   'AZ.FRD': 2420.0,
                   'AZ.KNW': 2035.0,
                   'AZ.LVA2': 2654.0,
                   'AZ.PFO': 2439.0,
                   'AZ.RDM': 1991.0,
                   'AZ.SND': 2367.0,
                   'AZ.WMC': 2251.0,
                   'CI.CHF': 453.0,
                   'CI.DJJ': 550.0,
                   'CI.MWC': 450.0,
                   'CI.PAS': 470.0,
                   'CI.PLM': 476.0,
                   'CI.VCS': 501.0,
                   'II.PFO': 484.0}],
                 ['2000-06-26T15:43:07.550000Z', {'CI.DAN': 492.0, 'CI.GSC': 448.0}],
                 ['2000-09-16T13:24:41.330000Z',
                  {'CI.CHF': 376.0,
                   'CI.CIA': 410.0,
                   'CI.DJJ': 255.0,
                   'CI.LGU': 404.0,
                   'CI.MWC': 347.0,
                   'CI.OSI': 459.0,
                   'CI.PAS': 304.0,
                   'CI.TOV': 340.0,
                   'CI.VCS': 408.0}],
                 ['2001-01-14T02:26:14.060000Z',
                  {'CI.CHF': 320.0,
                   'CI.CIA': 520.0,
                   'CI.DJJ': 268.0,
                   'CI.LGU': 401.0,
                   'CI.OSI': 364.0,
                   'CI.PAS': 291.0,
                   'CI.SDD': 541.0,
                   'CI.TOV': 333.0,
                   'CI.VCS': 316.0}],
                 ['2001-01-14T02:26:14.060000Z',
                  {'CI.CHF': 318.0,
                   'CI.CIA': 516.0,
                   'CI.DJJ': 268.0,
                   'CI.LGU': 401.0,
                   'CI.OSI': 363.0,
                   'CI.PAS': 291.0,
                   'CI.SDD': 561.0,
                   'CI.TOV': 333.0,
                   'CI.VCS': 316.0}],
                 ['2001-02-13T03:04:35.400000Z',
                  {'AZ.CRY': 2387.0,
                   'AZ.KNW': 2128.0,
                   'AZ.PFO': 2443.0,
                   'AZ.RDM': 2442.0,
                   'AZ.SND': 2465.0,
                   'CI.CHF': 530.0,
                   'CI.MWC': 544.0,
                   'CI.PLM': 543.0,
                   'CI.SDD': 557.0,
                   'CI.VCS': 568.0,
                   'II.PFO': 485.0}],
                 ['2001-02-18T06:09:32.160000Z',
                  {'AZ.CRY': 1370.0,
                   'AZ.KNW': 1304.0,
                   'AZ.LVA2': 1772.0,
                   'AZ.MONP': 2548.0,
                   'AZ.PFO': 1575.0,
                   'AZ.RDM': 1313.0,
                   'AZ.SND': 1481.0,
                   'CI.JCS': 427.0,
                   'CI.PLM': 332.0,
                   'CI.SDD': 482.0,
                   'II.PFO': 314.0}],
                 ['2001-03-25T00:41:25.210000Z',
                  {'AZ.BZN': 2694.0,
                   'AZ.CRY': 2516.0,
                   'AZ.FRD': 2761.0,
                   'AZ.KNW': 2392.0,
                   'AZ.RDM': 2303.0,
                   'AZ.SND': 2708.0,
                   'AZ.WMC': 2597.0}],
                 ['2001-04-13T11:50:12.490000Z',
                  {'AZ.BZN': 2743.0,
                   'AZ.CRY': 2567.0,
                   'AZ.KNW': 2522.0,
                   'CI.CHF': 389.0,
                   'CI.CIA': 499.0,
                   'CI.DJJ': 438.0,
                   'CI.MWC': 366.0,
                   'CI.PAS': 368.0,
                   'CI.PLM': 512.0,
                   'CI.SDD': 326.0,
                   'CI.TOV': 548.0,
                   'CI.VCS': 451.0}],
                 ['2001-04-13T11:50:12.490000Z',
                  {'AZ.BZN': 2749.0,
                   'AZ.CRY': 2580.0,
                   'AZ.FRD': 2828.0,
                   'AZ.KNW': 2525.0,
                   'AZ.RDM': 2398.0,
                   'AZ.SND': 2809.0,
                   'AZ.WMC': 2650.0,
                   'CI.CHF': 387.0,
                   'CI.CIA': 499.0,
                   'CI.DJJ': 438.0,
                   'CI.MWC': 366.0,
                   'CI.PAS': 368.0,
                   'CI.PLM': 512.0,
                   'CI.SDD': 326.0,
                   'CI.TOV': 551.0,
                   'CI.VCS': 452.0}],
                 ['2001-05-17T22:56:45.850000Z',
                  {'CI.BAK': 565.0, 'CI.ISA': 343.0, 'CI.MPM': 394.0, 'CI.SLA': 430.0}],
                 ['2001-07-17T12:59:59.170000Z',
                  {'CI.ISA': 430.0, 'CI.MPM': 326.0, 'CI.SLA': 396.0, 'LB.DAC': 684.0}],
                 ['2001-07-17T12:07:26.100000Z',
                  {'CI.ISA': 427.0, 'CI.MPM': 320.0, 'CI.SLA': 388.0, 'LB.DAC': 665.0}],
                 ['2001-07-20T12:53:07.530000Z',
                  {'CI.ISA': 417.0, 'CI.MPM': 321.0, 'CI.SLA': 387.0, 'LB.DAC': 676.0}],
                 ['2001-09-17T01:14:49.010000Z',
                  {'AZ.CRY': 2704.0,
                   'AZ.KNW': 2655.0,
                   'AZ.RDM': 2501.0,
                   'AZ.WMC': 2806.0,
                   'CI.CHF': 364.0,
                   'CI.CIA': 469.0,
                   'CI.DJJ': 408.0,
                   'CI.MWC': 338.0,
                   'CI.PAS': 344.0,
                   'CI.PLM': 549.0,
                   'CI.TOV': 522.0,
                   'CI.VCS': 422.0}],
                 ['2001-10-28T16:27:45.550000Z',
                  {'CI.CHF': 370.0,
                   'CI.CIA': 404.0,
                   'CI.DJJ': 301.0,
                   'CI.DLA': 1500.0,
                   'CI.FMP': 1468.0,
                   'CI.LAF': 1349.0,
                   'CI.LCG': 1401.0,
                   'CI.LGB': 1414.0,
                   'CI.LGU': 442.0,
                   'CI.LTP': 1395.0,
                   'CI.MWC': 337.0,
                   'CI.OSI': 489.0,
                   'CI.PAS': 302.0,
                   'CI.RPV': 1188.0,
                   'CI.RUS': 1528.0,
                   'CI.SDD': 428.0,
                   'CI.SMS': 1459.0,
                   'CI.STS': 1454.0,
                   'CI.TOV': 387.0,
                   'CI.USC': 1108.0,
                   'CI.VCS': 414.0,
                   'CI.WTT': 1350.0}],
                 ['2001-10-28T16:29:54.520000Z',
                  {'CI.CHF': 377.0,
                   'CI.CIA': 406.0,
                   'CI.DJJ': 310.0,
                   'CI.DLA': 1549.0,
                   'CI.FMP': 1507.0,
                   'CI.LAF': 1392.0,
                   'CI.LCG': 1441.0,
                   'CI.LGB': 1466.0,
                   'CI.LGU': 1452.0,
                   'CI.LTP': 1444.0,
                   'CI.MWC': 342.0,
                   'CI.PAS': 303.0,
                   'CI.RPV': 1219.0,
                   'CI.RUS': 1579.0,
                   'CI.SDD': 619.0,
                   'CI.SMS': 1494.0,
                   'CI.STS': 1497.0,
                   'CI.USC': 1147.0,
                   'CI.VCS': 418.0,
                   'CI.WTT': 1397.0}],
                 ['2001-11-13T20:43:14.950000Z',
                    {'AZ.BZN': 2530.0,
                     'AZ.CRY': 2622.0,
                     'AZ.FRD': 2426.0,
                     'AZ.KNW': 2689.0,
                     'AZ.LVA2': 2340.0,
                     'AZ.MONP': 2385.0,
                     'AZ.PFO': 2266.0,
                     'AZ.SND': 2466.0,
                     'AZ.WMC': 2573.0,
                     'CI.GLA': 481.0,
                     'CI.JCS': 487.0,
                     'CI.PLM': 546.0,
                     'II.PFO': 453.0}]]
tp_estimates = []
count = 0
station_latitudes = []
station_longitudes = []
event_latitude = []
event_longitude = []
for i in event_ids:
    try: 
        event_id = i #9155518
        client = Client("SCEDC")
        cat = client.get_events(eventid=i, includearrivals=True)
    
        name = str(cat[0].origins[0].time)
        #name = name[0:13]+'/'+name[14:16]+'/'+name[17:]
        filename = difflib.get_close_matches(name, files)[0]
        data = obspy.read(rootpath+filename+"/mseed/*")
        time = data[0].stats.starttime + timedelta(minutes=5)
        print('details')
        available = []
        picks_available = []
        for m in range(0, len(cat[0].picks)):
            name = '.'.join([cat[0].picks[m].waveform_id.network_code, cat[0].picks[m].waveform_id.station_code])#,cat[0].picks[i].waveform_id.channel_code])
            available.append(name)
            picks_available.append(cat[0].picks[m].time)
            #picks_dict[name]=cat[0].picks[i].time
        #print(i, len(picks_available))
        
        #PUBLISHED PICKS
        data_names = []
        data_sample_rates = []
        for j in range(0, len(data)):
            name = '.'.join([data[j].stats.network, data[j].stats.station])#, data[j].stats.channel])
            data_names.append(name)
            data_sample_rates.append(data[j].stats.sampling_rate)
        print('datanames')
        a = np.intersect1d(available, data_names, return_indices=True)
        picks_dict = {}
        data_with_picks = obspy.Stream()
        picks = []
        for k in range(0, len(a[2])):
            data_with_picks.append(data[a[2][k]+2])
            picks_dict[available[a[1][k]]]=picks_available[a[1][k]]
            picks.append(picks_available[a[1][k]])
        print(len(picks))
        print(len(data_names))
        published = picks_dict.copy()
        print(picks_dict)
        for eq in my_picks_list:
            if eq[0]==name:
                my_picks_for_this_eq = i[1]
                for pick in my_picks_for_this_eq:
                    if pick not in picks:
                        index = data_names.index(pick)
                        sr = data_sample_rates[index]
                        picks_dict.append[pick]=data[0].stats.starttime+timedelta(my_picks_for_this_eq[pick]+290*sr)
                        picks.append(data[0].stats.starttime+timedelta(my_picks_for_this_eq[pick]+290*sr))
        #MY PICKS
        print(len(picks_dict), len(published))
        print(len(picks_available), len(data_with_picks))
        print('pick comparison')
        this_eq_station_latitudes = []
        this_eq_station_longitudes = []
        this_eq_event_latitude = cat[0].origins[0].latitude
        this_eq_event_longitude = cat[0].origins[0].longitude
        for tr in data_with_picks:
            inv=obspy.read_inventory(rootpath+filename+"/stations/"+str(tr.stats.network)+"."+str(tr.stats.station)+'.xml')
            nyquist = tr.stats.sampling_rate/2
            tr.remove_response(inventory=inv, water_level=60, pre_filt=[0.025,0.05, 0.8*nyquist, 0.9*nyquist])#, output="DISP", plot=True)
            #tr.remove_response(inventory=inv, pre_filt=None, output="DISP", water_level=60, plot=True)
            this_eq_station_latitudes.append(inv[0][0][0].latitude)
            this_eq_station_longitudes.append(inv[0][0][0].longitude)
            
        print('remove response')
        eq = earthquake('test', time, data_with_picks, picks)
        
        eq.calc_Tpmax()
        print('eq')
        tp_estimates.append([eq.time, eq._cached_params['tau_p_max'], np.average(eq._cached_params['tau_p_max'])])
        
        station_latitudes.append(this_eq_station_latitudes)
        station_longitudes.append(this_eq_station_longitudes)
        
        event_latitude.append(this_eq_event_latitude)
        event_longitude.append(this_eq_event_longitude)
        print('done')
    except:
        print(i, 'failed')
        tp_estimates.append([0,[0],0])
    count += 1
    print(count, len(station_latitudes), len(event_latitude), len(tp_estimates))
for i in iris_event_ids:
    try: 
        event_id = i #9155518
        client = Client("IRIS")
        cat = client.get_events(eventid=i, includearrivals=True)
    
        name = str(cat[0].origins[0].time)
        #name = name[0:13]+'/'+name[14:16]+'/'+name[17:]
        filename = difflib.get_close_matches(name, files)[0]
        data = obspy.read(rootpath+filename+"/mseed/*")
        time = data[0].stats.starttime + timedelta(minutes=5)
        print('details')
        available = []
        picks_available = []
        for m in range(0, len(cat[0].picks)):
            name = '.'.join([cat[0].picks[m].waveform_id.network_code, cat[0].picks[m].waveform_id.station_code])#,cat[0].picks[i].waveform_id.channel_code])
            available.append(name)
            picks_available.append(cat[0].picks[m].time)
            #picks_dict[name]=cat[0].picks[i].time
        #print(i, len(picks_available))
        
        #PUBLISHED PICKS
        data_names = []
        data_sample_rates = []
        for j in range(0, len(data)):
            name = '.'.join([data[j].stats.network, data[j].stats.station])#, data[j].stats.channel])
            data_names.append(name)
            data_sample_rates.append(data[j].stats.sampling_rate)
        print('datanames')
        a = np.intersect1d(available, data_names, return_indices=True)
        picks_dict = {}
        data_with_picks = obspy.Stream()
        picks = []
        for k in range(0, len(a[2])):
            data_with_picks.append(data[a[2][k]+2])
            picks_dict[available[a[1][k]]]=picks_available[a[1][k]]
            picks.append(picks_available[a[1][k]])
        '''print(len(picks))
        print(len(data_names))
        published = picks_dict.copy()
        print(picks_dict)
        for eq in my_picks_list:
            if eq[0]==name:
                my_picks_for_this_eq = i[1]
                for pick in my_picks_for_this_eq:
                    if pick not in picks:
                        index = data_names.index(pick)
                        sr = data_sample_rates[index]
                        picks_dict.append[pick]=data[0].stats.starttime+timedelta(my_picks_for_this_eq[pick]+290*sr)
                        picks.append(data[0].stats.starttime+timedelta(my_picks_for_this_eq[pick]+290*sr))
        #MY PICKS
        print(len(picks_dict), len(published))'''
        print(len(picks_available), len(data_with_picks))
        print('pick comparison')
        this_eq_station_latitudes = []
        this_eq_station_longitudes = []
        this_eq_event_latitude = cat[0].origins[0].latitude
        this_eq_event_longitude = cat[0].origins[0].longitude
        for tr in data_with_picks:
            inv=obspy.read_inventory(rootpath+filename+"/stations/"+str(tr.stats.network)+"."+str(tr.stats.station)+'.xml')
            nyquist = tr.stats.sampling_rate/2
            tr.remove_response(inventory=inv, water_level=60, pre_filt=[0.025,0.05, 0.8*nyquist, 0.9*nyquist])#, output="DISP", plot=True)
            #tr.remove_response(inventory=inv, pre_filt=None, output="DISP", water_level=60, plot=True)
            this_eq_station_latitudes.append(inv[0][0][0].latitude)
            this_eq_station_longitudes.append(inv[0][0][0].longitude)
            
        print('remove response')
        eq = earthquake('test', time, data_with_picks, picks)
        
        eq.calc_Tpmax()
        print('eq')
        tp_estimates.append([eq.time, eq._cached_params['tau_p_max'], np.average(eq._cached_params['tau_p_max'])])
        
        station_latitudes.append(this_eq_station_latitudes)
        station_longitudes.append(this_eq_station_longitudes)
        
        event_latitude.append(this_eq_event_latitude)
        event_longitude.append(this_eq_event_longitude)
        print('done')
    except:
        print(i, 'failed')
        tp_estimates.append([0,[0],0])
    count += 1
    print(count, len(station_latitudes), len(event_latitude), len(tp_estimates))
tp_olsen = [1.68, 1.44, 1.50, 0.95, 0.80, 0.63, 0.92, 0.69, 1.14, 1.16, 0.58, 0.74, 0.66, 0.50, 0.54, 0.75, 0.61, 0.63, 0.36, 0.70, 0.61, 0.33, 0.38, 0.63, 0.57, 1.12, 0.88, 0.61, 0.76, 0.41, 0.65, 0.41, 0.92, 0.50, 0.58, 0.62, 0.50, 0.43, 0.63, 0.35]

magnitudes = [7.3, 6.7, 5.8, 5.3, 5.3, 5.1, 5.2, 5.0, 7.1, 5.8, 4.8, 4.7, 4.6, 4.5, 5.1, 5.0, 4.3, 4.6, 3.2, 4.3, 3.5, 3.3, 3.4, 3.6, 4.1, 4.7, 4.8, 4.4, 4.2, 3.1, 4.0, 3.0, 4.1, 4.2, 3.6, 3.9, 3.5, 3.2, 4.4, 3.3]

tp_olsen_all = [1.68, 1.44, 1.50, 0.95, 0.80, 0.63, 0.92, 0.69, 1.14, 1.16, 0.58, 0.74, 0.66, 0.50, 0.54, 0.75, 0.61, 0.63, 0.36, 0.70, 0.61, 0.33, 0.38, 0.63, 0.57, 1.12, 0.88, 0.61, 0.76, 0.41, 0.65, 0.41, 0.92, 0.50, 0.58, 0.62, 0.50, 0.43, 0.63, 0.35]

magnitudes_all = [7.3, 6.7, 5.8, 5.3, 5.3, 5.1, 5.2, 5.0, 7.1, 5.8, 4.8, 4.7, 4.6, 4.5, 5.1, 5.0, 4.3, 4.6, 3.2, 4.3, 3.5, 3.3, 3.4, 3.6, 4.1, 4.7, 4.8, 4.4, 4.2, 3.1, 4.0, 3.0, 4.1, 4.2, 3.6, 3.9, 3.5, 3.2, 4.4, 3.3]

for i in range(0, len(tp_olsen)):
    good = []
    if tp_estimates[i][2] != 0:
        for est in tp_estimates[i][1]:
            if abs(est-tp_estimates[i][2])<= 1:
                plt.scatter(magnitudes[i], est, color='grey', marker='.', alpha = 0.7)
                good.append(est)
        plt.scatter(magnitudes[i], np.average(good), color='skyblue', alpha = 1)
        plt.scatter(magnitudes[i], tp_olsen[i], color = 'pink', alpha = 1)
        try:
            plt.scatter(magnitudes[i], min(tp_estimates[i][1]), color='black', marker='x', alpha = 0.5)
        except:
            False
plt.ylabel("predominant period")
plt.xlabel("Magnitude")

x = []; y = []; y_true = []
for i in range(0, len(tp_olsen)):
    good = []
    if tp_estimates[i][2] != 0:
        for est in tp_estimates[i][1]:
            if abs(est-tp_estimates[i][2])<= 2*np.std(tp_estimates[i][1]) and magnitudes[i]<5.7:
                plt.scatter(magnitudes[i], est, color='grey', marker='.', alpha = 0.7)
                good.append(est)
        if len(good)>0 and magnitudes[i]<5.7:
            plt.scatter(magnitudes[i], np.average(good), color='skyblue', alpha = 1)
            plt.scatter(magnitudes[i], tp_olsen[i], color = 'pink', alpha = 1)
            y.append(np.average(good))
            x.append(magnitudes[i])
            y_true.append(tp_olsen[i])
        try:
            plt.scatter(magnitudes[i], min(tp_estimates[i][1]), color='black', marker='x', alpha=0.5)
        except:
            False
m, b = np.polyfit(x, np.log(np.array(y)), 1)
x = np.array(x)
plt.plot(x, 10**(m*x + b), color='skyblue')
m_true, b_true = np.polyfit(x, np.log(np.array(y_true)), 1)
x = np.array(x)
plt.plot(x, 10**(m_true*x + b_true), color='pink')
plt.ylabel("predominant period")
plt.xlabel("Magnitude")
plt.plot(x, 10**(0.14*x-0.83))
plt.yscale('log')

station_latitudes
station_longitudes
event_latitude.append(cat[0].origins[0].latitude)
event_longitude.append(cat[0].origins[0].longitude)
        
for i in range(0, len(tp_olsen)):
    for j in range(0, len(tp_estimates[i][1])):
        try:
            distance = np.sqrt((event_latitude[i]-station_latitudes[i][j])**2+(event_longitude[i]-station_longitudes[i][j])**2)
            plt.scatter(distance, abs(tp_estimates[i][1][j]-tp_olsen[i]), color='grey', marker='.', alpha = 0.7)
            if tp_estimates[i][1][j]==min(tp_estimates[i][1]):
                plt.scatter(distance, abs(tp_estimates[i][1][j]-tp_olsen[i]), color='blue', marker='o')
        except:
            False

plot_no = 0
loc_no = 0
fig, axs = plt.subplots(5, 8)
for k in range(0, len(tp_olsen)):
    if tp_estimates[k][1]!=[0]:
        print(i, 'i=k')
        i=k
        use = []
        for j in range(0, len(tp_estimates[i][1])):
            print('plotno',plot_no)
            print(j,'j')
            if len(tp_estimates[i][1])>0:
                print('in if')
                distance = np.sqrt((event_latitude[loc_no]-station_latitudes[loc_no][j])**2+(event_longitude[loc_no]-station_longitudes[loc_no][j])**2)
                if distance <=1:
                    axs[int(np.floor(plot_no/8))][int(plot_no%8)].scatter(distance, tp_estimates[i][1][j]-tp_olsen[i], color='slategrey', marker='.', alpha = 0.9)
                    axs[int(np.floor(plot_no/8))][int(plot_no%8)].hlines(0, 0, 3, colors='pink', linestyles=':')
                    if tp_estimates[i][1][j]==min(tp_estimates[i][1]):
                        axs[int(np.floor(plot_no/8))][int(plot_no%8)].scatter(distance, tp_estimates[i][1][j]-tp_olsen[i], color='slategrey', marker='x')
                    use.append(tp_estimates[i][1][j])
        if len(tp_estimates[i][1])>0:
            axs[int(np.floor(plot_no/8))][int(plot_no%8)].hlines(np.average(use)-tp_olsen[i], 0, 2, color='skyblue', linestyles=':')
        plot_no += 1
        loc_no += 1
    else:
        plot_no += 1
plt.setp(axs, xlim=[0,1])
fig.add_subplot(111, frameon=False)
# hide tick and tick label of the big axis
plt.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)
plt.xlabel("distance (degrees)")
plt.ylabel("difference in tp")

plot_no = 0
loc_no = 0
fig, axs = plt.subplots(5, 8)
for k in range(0, len(tp_olsen)):
    if tp_estimates[k][1]!=[0]:
        print(i, 'i=k')
        i=k
        use = []
        for j in range(0, len(tp_estimates[i][1])):
            print('plotno',plot_no)
            print(j,'j')
            if len(tp_estimates[i][1])>0:
                print('in if')
                distance = np.sqrt((event_latitude[loc_no]-station_latitudes[loc_no][j])**2+(event_longitude[loc_no]-station_longitudes[loc_no][j])**2)
                if distance <= 1:
                    axs[int(np.floor(plot_no/8))][int(plot_no%8)].scatter(distance, tp_estimates[i][1][j], color='slategrey', marker='.', alpha = 0.9)
                    axs[int(np.floor(plot_no/8))][int(plot_no%8)].hlines(tp_olsen[i], 0, 3, colors='pink')
                    if tp_estimates[i][1][j]==min(tp_estimates[i][1]):
                        axs[int(np.floor(plot_no/8))][int(plot_no%8)].scatter(distance, tp_estimates[i][1][j], color='slategrey', marker='x')
                    use.append(tp_estimates[i][1][j])
        if len(tp_estimates[i][1])>0:
            axs[int(np.floor(plot_no/8))][int(plot_no%8)].hlines(np.average(use), 0, 2, color='skyblue')
        plot_no += 1
        loc_no += 1
    else:
        plot_no += 1
plt.setp(axs, xlim=[0,1.1])
fig.add_subplot(111, frameon=False)
# hide tick and tick label of the big axis
plt.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)
plt.xlabel("distance (degrees)")
plt.ylabel("tp")


    plt.scatter(magnitudes[i], tp_estimates[i][2], color='skyblue', alpha = 1)
    plt.scatter(magnitudes[i], tp_olsen[i], color = 'pink', alpha = 1)
    try:
        plt.scatter(magnitudes[i], min(tp_estimates[i][1]), color='black', marker='x', alpha = 0.5)
    except:
        False
plt.ylabel("predominant period")
plt.xlabel("Magnitude")

In [19]: for i in range(0,8):
    ...:     ax = plt.subplot(8,1, i+1)
    ...:     ax.plot(eq.data[i].data)
ax2=ax.twinx()
ax2.plot(data_with_picks[i].data)


fig, axs = plt.subplots(2,4)
for i in range(0, len(eq.data)):
    axs[int(np.floor(i/4))][i%4].plot(eq._cached_params["tau_p"][i], color='black')
    start = (eq.picks[i]-eq.data[i].stats.starttime)*eq.data[i].stats.sampling_rate
    end = start+eq.data[i].stats.sampling_rate*4
    axs[int(np.floor(i/4))][i%4].hlines([0.63], 0, 180000, color='slategrey')
    axs[int(np.floor(i/4))][i%4].vlines([start+0.05*eq.data[i].stats.sampling_rate, end+0.05*eq.data[i].stats.sampling_rate], 0, 10000, color='skyblue')
    axs[int(np.floor(i/4))][i%4].vlines([start], 0, 10000, color='steelblue', linestyle=':')
    axs[int(np.floor(i/4))][i%4].axis(xmin = start-100, xmax=end+500, ymin=0, ymax=10)
plt.suptitle('instrument response removed, start tpmax at pick+0.05s')
plt.show()
