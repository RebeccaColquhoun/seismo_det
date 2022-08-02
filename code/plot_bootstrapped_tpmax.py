#!/usr/bin/env python
# coding: utf-8

# ## Imports

# In[2]:


print('')


# In[1]:


import os
import math
import obspy
import pickle
import datetime
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.pyplot import figure
from scipy.optimize import curve_fit
from datetime import timedelta
from obspy import UTCDateTime
from obspy.clients.fdsn import Client

from earthquake import Earthquake
import util
import pandas as pd
from multiprocessing import Pool
import random


list_tpmax = []
list_mags = []
list_mag_types = []
list_eq = []
eqs = {}
count = 0

parameters = [[1,0.1,19,0,'eq_object_1s_bandpass_01_19_snr_20_blank_0'],
[1,0.1,19,0.05,'eq_object_1s_bandpass_01_19_snr_20_blank_005'],
[1,0.1,19,0.1,'eq_object_1s_bandpass_01_19_snr_20_blank_01'],
[1,0.1,19,0.25,'eq_object_1s_bandpass_01_19_snr_20_blank_025'],
[1,0.1,19,0.5,'eq_object_1s_bandpass_01_19_snr_20_blank_05'],
[4,0.1,19,0,'eq_object_4s_bandpass_01_19_snr_20_blank_0'],
[4,0.1,19,0.05,'eq_object_4s_bandpass_01_19_snr_20_blank_005'],
[4,0.1,19,0.1,'eq_object_4s_bandpass_01_19_snr_20_blank_01'],
[4,0.1,19,0.25,'eq_object_4s_bandpass_01_19_snr_20_blank_025'],
[4,0.1,19,0.5,'eq_object_4s_bandpass_01_19_snr_20_blank_05'],
[2,0.1,19,0.5,'eq_object_2s_bandpass_01_19_snr_20'],
[3,0.1,19,0.5,'eq_object_3s_bandpass_01_19_snr_20']]

def gen_bs_data(x,y):
    x_bs = []
    y_bs = []
    for _ in range(0, len(x)):
        n = random.randint(0, len(x)-1)
        x_bs.append(x[n])
        y_bs.append(y[n])
    return x_bs, y_bs

def plot_for_params(list_mags, list_tpmax, title):
    #get_ipython().run_line_magic('matplotlib', 'inline')
    params = []
    opacities = np.linspace(0.2,1,45)
    import matplotlib.pyplot as plt
    cs = ['midnightblue']
    #fig, axs = plt.subplots(1,1, figsize=(12.8,9.6))
    y_aves_tp = []
    x_aves_tp = []
    count = 1
    eq_count = 0
    medians = [[] for _ in range(0, 45)]
    medians_of_medians = [[] for _ in range(0, 45)]
    n = 0
    median_absolute_deviation = []
    sum_absolute_deviation = []
    all_abs_deviation = []
    for n in [1]:#range(1, 10):#number of stations eq at least measured at
        med_for_ad = []
        mag_for_ad = []
        fig, axs = plt.subplots(1,1, figsize=(12.8,9.6))
        for mag_lim in [3.4]:#, 3.4, 4.0, 4.4]:#np.arange(3.0, 6.5, 0.1):
            y_aves_tp = []
            x_aves_tp = []
            for i  in range(0, len(list_mags)):
                if list_mags[i] > mag_lim and list_mags[i]<=max(list_mags):
                    if len(list_tpmax[i])>=n:
                        mean_tp = np.mean(list_tpmax[i]) 
                        std_tp = np.std(list_tpmax[i]) 
                        y_tp = [] 
                        for j in list_tpmax[i]: 
                            if j > mean_tp-2*std_tp and j < mean_tp + 2*std_tp:# and j < 100: 
                                y_tp.append(math.log(j, 10))
                            elif len(list_tpmax[i])==1:
                                y_tp.append(math.log(j, 10))
                        x_tp = np.zeros(len(y_tp))  
                        x_tp = x_tp + list_mags[i]
                        c = 0
                        if len(x_tp)>0 and mag_lim == 3.4:
                            if math.isnan(np.median(y_tp))==False:
                                axs.scatter(list_mags[i]-5+np.random.uniform(-0.05, 0.05), np.median(y_tp), s = 10, c = '#003f5c', marker = 'x', zorder =110, alpha = 0.5)
                        if math.isnan(np.median(y_tp))==False:  
                            y_aves_tp.append(np.median(y_tp))
                            x_aves_tp.append(list_mags[i])
            if len(y_aves_tp)>0:
                x_use = np.array(x_aves_tp) - 5
                y_use = np.array(y_aves_tp)

                print(len(x_aves_tp), len(y_aves_tp))
                count += 1
        x = x_use
        y = y_use
        x_unique = np.arange(-1.6,2.1,0.1)
        df = pd.DataFrame(columns = x_unique)
        for runs in range(0,1000):
            x_bs, y_bs = gen_bs_data(x,y)
            popt = np.polyfit(x_bs, y_bs, 1)
            df2 = pd.DataFrame([popt[0]*x_unique+popt[1]],columns = x_unique)
            df = pd.concat([df,df2], ignore_index=True)
        ub_95, lb_95 = [], []
        ub_68, lb_68 = [], []
        
        for column in df.columns:
            sorted_array = np.array(df[column])
            sorted_array.sort()
            ub_95.append(sorted_array[975])
            lb_95.append(sorted_array[25])
            ub_68.append(sorted_array[840])
            lb_68.append(sorted_array[160])
            
        #plt.scatter(x+np.random.uniform(-0.05, 0.05, len(x)),y, marker = 'x', color = 'k', s = 10, alpha = 0.5)
        axs.fill_between(x_unique, lb_68, ub_68, color = '#bc5090', alpha = 0.6, zorder = 100, label = '1sd')
        axs.fill_between(x_unique, lb_95, ub_95, color = '#ffa600', alpha = 0.6, zorder = 99, label = '2sd')
        popt = np.polyfit(x, y, 1)
        axs.plot(x_unique, popt[0]*x_unique+popt[1], color='#003f5c',zorder=102,label='{a:.2f}x+{b:.2f}'.format(a=popt[0],b=popt[1]))
        axs.set_ylabel('log10(tpmax)')
        axs.set_xlabel('magnitude')   
        axs.set_xticks([-2,-1,0,1,2,3], [3,4,5,6,7,8], zorder = 110)
        axs.legend()
        #axs.set_ylim([-2,1])
        axs.set_title(title)
        plt.savefig('/home/earthquakes1/homes/Rebecca/phd/seismo_det/figures/tp_different_params/'+title+'_all_bootstrapped_1000', format = 'pdf')
        return np.array(x_aves_tp)-5, y_aves_tp




def load_and_plot(p):
    fn = p[-1]
    print(fn)
    list_tpmax = []
    list_mags = []
    list_mag_types = []
    folders = os.listdir('/home/earthquakes1/homes/Rebecca/phd/data/2018_2021_global_m5/')
    for eq_no in range(0, len(folders)):
        if os.path.exists('/home/earthquakes1/homes/Rebecca/phd/data/2018_2021_global_m5/'+folders[eq_no]+'/'+fn+'.pkl'):
            with open('/home/earthquakes1/homes/Rebecca/phd/data/2018_2021_global_m5/'+folders[eq_no]+'/'+fn+'.pkl', 'rb') as picklefile:
                eq = pickle.load(picklefile)
            list_tpmax.append(eq.calculated_params['tau_p_max'])
            list_mags.append(eq.event_stats['eq_mag'])
            list_mag_types.append(eq.event_stats['eq_mag_type'])
    folders = os.listdir('/home/earthquakes1/homes/Rebecca/phd/data/2019_global_m3/')
    for eq_no in range(0, len(folders)):
        if os.path.exists('/home/earthquakes1/homes/Rebecca/phd/data/2019_global_m3/'+folders[eq_no]+'/'+fn+'.pkl'):
            with open('/home/earthquakes1/homes/Rebecca/phd/data/2019_global_m3/'+folders[eq_no]+'/'+fn+'.pkl', 'rb') as picklefile:
                eq = pickle.load(picklefile)
            list_tpmax.append(eq.calculated_params['tau_p_max'])
            list_mags.append(eq.event_stats['eq_mag'])
            list_mag_types.append(eq.event_stats['eq_mag_type'])
            
    x, y = plot_for_params(list_mags, list_tpmax, p[-1])

    return x, y


with Pool(5) as pool:
    pool.map(load_and_plot, parameters)

