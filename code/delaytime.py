import os
import scipy
import numpy as np
import matplotlib.pyplot as plt
import obspy
import pickle
from obspy import UTCDateTime

root = '/home/earthquakes1/homes/Rebecca/phd/data/AK_data_eqtransformer/'
eq_list = os.listdir(root)
eq_name = eq_list[0]
data = obspy.read(root+eq_name+'/data/*/*')
with open(root+eq_name+'/picks.pkl', 'rb') as f:
    picks = pickle.load(f)
n_records = 0

# sensor_types = self.data_stats['sensor_types'] for automated OOP
for i in range(0, len(data)):  # iterate through all traces
    if data[i].stats.channel[2] == 'Z' and data[i].stats.station in picks.keys():  # only use vertical components at stations with a pick
        tr = data[i].copy()
        pick = picks[tr.stats.station]
        pick_samples = int(round((UTCDateTime(picks[tr.stats.station]) - tr.stats.starttime)*tr.stats.sampling_rate, 0))
        '''if sensor_types[i][0] == 'a':
            tr.filter('highpass', freq=0.1, corners=3)  # 0.078)#i_freq)
            tr = tr.integrate()
            displ = tr.integrate()
        elif sensor_types[i][0] == 'v':'''
        tr.filter('bandpass', freqmin=0.1, freqmax = 3) 
        displ = tr.integrate()
        abs_displ = abs(displ.data) # find absolute of trace
        print(n_records)
        try:
            sum_abs_displ = sum_abs_displ + abs_displ[pick_samples-10000:pick_samples+10000]
        except:
            sum_abs_displ = abs_displ[pick_samples-10000:pick_samples+10000]
    '''peaks_x = scipy.signal.find_peaks(abs_displ)[0]
    peaks_y = []
    for peak in peaks_x:
        peaks_y.append(abs_displ[peak])'''
    n_records += 1
aad = sum_abs_displ/n_records


# now to find where departure delay exceeds DPD
# 'simple sequential computation ... comparing the amplitude at a sample
# with the one at the previous sample ...regardless of the magntiude of the decline'
# Noda and Ellsworth 2016
DPD_time = 0.05
DPD_samples = 2.5
delay_time = []
for point in range(1,len(aad)):
    if aad[point]<aad[point-1]:
        decline += 1
        if decline == np.ceil(DPD_samples)-1:
            delay_time.append(point)
    else:
        decline = 0
#T_dp = pick + delay_time
