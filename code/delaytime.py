import os
import scipy
import numpy as np
import matplotlib.pyplot as plt
import obspy
import pickle
from obspy import UTCDateTime
from obspy.clients.fdsn import Client
import util
import pandas as pd

root = '/home/earthquakes1/homes/Rebecca/phd/data/AK_data_eqtransformer/'
eq_list = os.listdir(root)

df = pd.DataFrame({'5.0':[np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000)],
                   '6.0':[np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000)],
                   '7.0':[np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000)]})
counts = pd.DataFrame({'5.0':[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       '6.0':[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       '7.0':[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]})

aad = pd.DataFrame({'5.0':[np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000)],
                   '6.0':[np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000)],
                   '7.0':[np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000), np.zeros(10000)]})

ad = pd.DataFrame({'5.0':[[], [], [], [], [], [], [], [], [], [], [], []],
                   '6.0':[[], [], [], [], [], [], [], [], [], [], [], []],
                   '7.0':[[], [], [], [], [], [], [], [], [], [], [], []]})

client = Client("IRIS")
cat = client.get_events(starttime=UTCDateTime("2019-06-26"), endtime=UTCDateTime("2020-06-26"), minlongitude=-179, maxlongitude=-145, minlatitude=42, maxlatitude=71, minmagnitude=5, includearrivals=True)
dists = []
for eq_name in eq_list:
    # find matching cat event:
    for event in cat:
        if eq_name == util.catEventToFileName(event):
            cat_entry = event
            break
    eq_lat= cat_entry.origins[0].latitude
    eq_long = cat_entry.origins[0].longitude
    eq_mag = cat_entry.magnitudes[0].mag

    data = obspy.read(root+eq_name+'/data/*/*')
    inv = obspy.read_inventory(root+eq_name+'/station_xml_files/*')

    with open(root+eq_name+'/picks.pkl', 'rb') as f:
        picks = pickle.load(f)
    n_records = 0
    sampling_rate = 50 # get this from tr.stats.sampling_rate
    # sensor_types = self.data_stats['sensor_types'] for automated OOP
    
    for i in range(0, len(data)):  # iterate through all traces
        if data[i].stats.channel[2] == 'Z' and data[i].stats.station in picks.keys():  # only use vertical components at stations with a pick
            tr = data[i].copy()
            tr.remove_response(inv)
            pick = picks[tr.stats.station]
            pick_samples = int(round((UTCDateTime(picks[tr.stats.station]) - tr.stats.starttime)*tr.stats.sampling_rate, 0))

            sta_lat = inv.select(network = tr.stats.network, station = tr.stats.station)[0][0].latitude
            sta_long = inv.select(network = tr.stats.network, station = tr.stats.station)[0][0].longitude

            distance = np.sqrt((eq_lat - sta_lat)**2 + (eq_long - sta_long)**2) * 110 # 2D for now...
            dists.append(distance)
            print(distance)
            tr.filter('bandpass', freqmin=0.1, freqmax = 3) 
            displ = tr.integrate()
            abs_displ = abs(displ.data) # find absolute of trace
            sum_abs_displ = df[str(np.floor(eq_mag))][int(distance//25)]
            sum_abs_displ =  sum_abs_displ + abs_displ[pick_samples:pick_samples+10000] # calculate aad for 10000 samples after p wave arrival
            df[str(np.floor(eq_mag))][int(distance//25)] = sum_abs_displ
            current = ad[str(np.floor(eq_mag))][int(distance//25)]
            current.append(abs_displ[pick_samples:pick_samples+10000])
            ad[str(np.floor(eq_mag))][int(distance//25)]= current
            counts[str(np.floor(eq_mag))][int(distance//25)] = counts[str(np.floor(eq_mag))][int(distance//25)]  + 1

            
        # n_records += 1

    '''aad = sum_abs_displ/n_records'''
fig, axs = plt.subplots(4, df.shape[1]-1)

row_count = 0
for row in range(4):
    col_count = 0
    for column in df.columns[:-1]:
        aad[column][row]=df[column][row]/counts[column][row]
        aad_bin = aad[column][row]
        # now to find where departure delay exceeds DPD
        # 'simple sequential computation ... comparing the amplitude at a sample
        # with the one at the previous sample ...regardless of the magntiude of the decline'
        # Noda and Ellsworth 2016
        DPD_time = 0.05
        DPD_samples = 2 # sampling rate is 50 Hz
        delay_time = []
        decline = 0 # count how many amplitudes have decreased in a row
        for point in range(1,len(aad)):
            if aad_bin[point]>aad_bin[point-1]:
                print('less than previous point')
                decline += 1
                if decline == np.ceil(DPD_samples)-1: #if surpassed the DPD
                    delay_time.append(point)
            else:
                decline = 0 #reset decline counter
        T_dp = np.array(delay_time)/sampling_rate # convert to seconds
        if len(T_dp)>0:
            for i in range(0, min(5, len(T_dp))): # vertical lines marking potential Tdp locations (first 5 after P wave pick)
                axs[row_count][col_count].vlines(T_dp[i], min(aad_bin), max(aad_bin))

        axs[row_count][col_count].plot(np.arange(0, 50, 0.02), aad[column][row][:2500], zorder = 50)
        for ind_ad in ad[column][row]:
            axs[row_count][col_count].plot(np.arange(0, 50, 0.02), ind_ad[:2500], color='lightgrey')
        axs[row_count][col_count].set_xscale('log')
        axs[row_count][col_count].set_yscale('log') # in log space
        col_count += 1
    row_count += 1


axs[0][0].set_title('M5-6')
axs[0][1].set_title('M6-7')
axs[0][0].set_ylabel('0-25 km')
axs[1][0].set_ylabel('25-50 km')
axs[2][0].set_ylabel('50-75 km')
axs[3][0].set_ylabel('75-100 km')
plt.ylabel('displacement')
plt.xlabel('time (s)')
plt.show()
        
'''
# now to find where departure delay exceeds DPD
# 'simple sequential computation ... comparing the amplitude at a sample
# with the one at the previous sample ...regardless of the magntiude of the decline'
# Noda and Ellsworth 2016
DPD_time = 0.05
DPD_samples = 2.5 # sampling rate is 50 Hz
delay_time = []
decline = 0 # count how many amplitudes have decreased in a row
for point in range(1,len(aad)):
    if aad[point]<aad[point-1]:
        decline += 1
        if decline == np.ceil(DPD_samples)-1: #if surpassed the DPD
            delay_time.append(point)
    else:
        decline = 0 #reset decline counter
T_dp = np.array(delay_time)/sampling_rate # convert to seconds

plt.plot(np.arange(0, 5, 0.02), aad[:250]) # plot aad against time for first 5 seconds
for i in range(0, 5): # vertical lines marking potential Tdp locations (first 5 after P wave pick)
    plt.vlines(T_dp[i], min(aad), max(aad))
plt.xscale('log'), plt.yscale('log') # in log space
plt.ylabel('displacement')
plt.xlabel('time (s)')
plt.show()

'''



'''if sensor_types[i][0] == 'a':
tr.filter('highpass', freq=0.1, corners=3)  # 0.078)#i_freq)
tr = tr.integrate()
displ = tr.integrate()
elif sensor_types[i][0] == 'v':'''


'''peaks_x = scipy.signal.find_peaks(abs_displ)[0]
peaks_y = []
for peak in peaks_x:
peaks_y.append(abs_displ[peak])'''
