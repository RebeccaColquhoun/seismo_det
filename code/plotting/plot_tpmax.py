import os
import scipy
import numpy as np
import matplotlib.pyplot as plt
import obspy
import pickle
from obspy import UTCDateTime
from obspy.clients.fdsn import Client
import pandas as pd
import math

import matplotlib
matplotlib.rcParams.update({'font.size': 20})

filenames = ['eq_object_03s_bandpass_01_19_snr_20_blank_0_new',
              'eq_object_03s_bandpass_01_19_snr_20_blank_005_new',
              'eq_object_03s_bandpass_01_19_snr_20_blank_01_new']
'''filenames = ['eq_object_05s_bandpass_01_19_snr_20_blank_0_new',
             'eq_object_05s_bandpass_01_19_snr_20_blank_005_new', 
             'eq_object_05s_bandpass_01_19_snr_20_blank_01_new',
             'eq_object_05s_bandpass_01_19_snr_20_blank_025_new',
             'eq_object_1s_bandpass_01_19_snr_20_blank_0_new', 
             'eq_object_1s_bandpass_01_19_snr_20_blank_005_new',
             'eq_object_1s_bandpass_01_19_snr_20_blank_01_new',
             'eq_object_1s_bandpass_01_19_snr_20_blank_025_new',
             'eq_object_1s_bandpass_01_19_snr_20_blank_05_new',
              'eq_object_4s_bandpass_01_19_snr_20_blank_0_new',
              'eq_object_4s_bandpass_01_19_snr_20_blank_005_new',
              'eq_object_4s_bandpass_01_19_snr_20_blank_01_new',
              'eq_object_4s_bandpass_01_19_snr_20_blank_025_new',
              'eq_object_4s_bandpass_01_19_snr_20_blank_05_new']'''
filenames = ['eq_object_03s_bandpass_01_19_snr_20_blank_0_new',
            'eq_object_05s_bandpass_01_19_snr_20_blank_0_new',
            'eq_object_1s_bandpass_01_19_snr_20_blank_0_new',
            'eq_object_4s_bandpass_01_19_snr_20_blank_0_new']

magnitudes = np.arange(3,8, 0.1)
def sort_tp_data(df, mag_lim = 0):
    list_tp_all = list(df.tp_max)
    list_mag_all = list(df.eq_mag)
    list_mag = []
    list_tpmax = []
    count = 0
    for m in range(0, len(list_mag_all)):
        if list_mag_all[m] > mag_lim:
            list_mag.append(list_mag_all[m])
            list_tpmax.append([])
            for d in range(0, len(list_tp_all[m])):
                if list_tp_all[m][d] != None and list_tp_all[m][d]>0:
                    list_tpmax[count].append(list_tp_all[m][d])
            count += 1
    return list_mag, list_tpmax
        
def plot_tpmax(title, mag_lim, list_mags, list_tpmax):
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
        #for mag_lim in [3.]:#, 3.4, 4.0, 4.4]:#np.arange(3.0, 6.5, 0.1):
        y_aves_tp = []
        x_aves_tp = []
        for i  in range(0, len(list_mags)):
            if list_mags[i] > mag_lim and list_mags[i]<=max(list_mags):
                #if list_mags[i] >= 4 and list_mags[i]<=5:
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
                    if len(x_tp)>0:
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
            x_unique = np.arange(-2,3,0.1)
            df_tp = pd.DataFrame(columns = x_unique)

            result = scipy.stats.linregress(x,y)
            a = result.slope
            b = result.intercept
            std_a = result.stderr
            std_b = result.intercept_stderr

            y_1 = (a+std_a)*x_unique + (b+std_b)
            y_2 = (a+std_a)*x_unique + (b-std_b)
            y_3 = (a-std_a)*x_unique + (b+std_b)
            y_4 = (a-std_a)*x_unique + (b-std_b)


            y_min_1sd = np.minimum(np.minimum(y_1, y_2), np.minimum(y_3, y_4))
            y_max_1sd = np.maximum(np.maximum(y_1, y_2), np.maximum(y_3, y_4))

            y_1 = (a+2*std_a)*x_unique + (b+2*std_b)
            y_2 = (a+2*std_a)*x_unique + (b-2*std_b)
            y_3 = (a-2*std_a)*x_unique + (b+2*std_b)
            y_4 = (a-2*std_a)*x_unique + (b-2*std_b)

            y_min_2sd = np.minimum(np.minimum(y_1, y_2), np.minimum(y_3, y_4))
            y_max_2sd = np.maximum(np.maximum(y_1, y_2), np.maximum(y_3, y_4))        
            
            median, bin_edges, bin_number = scipy.stats.binned_statistic(x, y, statistic='median', bins=np.arange(-2,3,0.1), range=None)
            
            #plt.scatter(x+np.random.uniform(-0.05, 0.05, len(x)),y, marker = 'x', color = 'k', s = 10, alpha = 0.5)
            axs.fill_between(x_unique, y_min_1sd, y_max_1sd, color = '#bc5090', alpha = 0.6, zorder = 100, label = '1sd')
            axs.fill_between(x_unique, y_min_2sd, y_max_2sd, color = '#ffa600', alpha = 0.6, zorder = 99, label = '2sd')
            popt = np.polyfit(x, y, 1)
            axs.plot(x_unique, popt[0]*x_unique+popt[1], color='#003f5c',zorder=102,label='{a:.2f}x+{b:.2f}\npearson r: {r:.4f}'.format(a=result.slope,b=result.intercept-5*result.slope,r=result.rvalue))
            axs.set_ylabel('log10(tpmax)')
            axs.set_xlabel('magnitude')
            axs.scatter(bin_edges[:-1]+0.05, median, marker = 'o', color = 'orange', zorder = 1000)
            axs.set_xticks([-2,-1,0,1,2,3], [3,4,5,6,7,8], zorder = 110)
            axs.legend()
            #axs.set_ylim([-2,1])
            t = title.split('_')
            axs.set_title(f'Predominant period, window = {t[2]}, blanked time = {t[-2][0]}.{t[-2][1:]}s')
            #plt.show()
            plt.savefig(f'/home/earthquakes1/homes/Rebecca/phd/seismo_det/figures/all_data/tpmax/{title}_medians.pdf', format = 'pdf')
            plt.close()
            return result.rvalue


for f in filenames:
    if os.path.exists(f'/home/earthquakes1/homes/Rebecca/phd/seismo_det/figures/all_data/tpmax/{f}') == False:
        os.makedirs(f'/home/earthquakes1/homes/Rebecca/phd/seismo_det/figures/all_data/tpmax/{f}')
    if True: #for mag_lim in magnitudes:
        mag_lim = 3.
        df = pd.read_pickle(f'/home/earthquakes1/homes/Rebecca/phd/data/results_database/{f}')
        list_mags, list_tpmax = sort_tp_data(df, mag_lim)
        print(len(list_mags), len(list_tpmax))
        plot_tpmax(f, mag_lim, list_mags, list_tpmax)
