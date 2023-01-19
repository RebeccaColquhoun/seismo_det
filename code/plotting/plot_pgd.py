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

magnitudes = np.arange(3,8, 0.1)
def sort_pgd_data(df, mag_lim = 0):
    list_pgd_all = list(df.pgd)
    list_mag_all = list(df.eq_mag)
    list_dist_Distance = list(df.pgd_distances)
    list_dist = []
    list_mag = []
    list_pgd = []
    eq = 0
    for m in range(0, len(list_mag_all)):
        if list_mag_all[m]>mag_lim:
            someTrue = len(list_pgd_all[m])
            for d in range(0, len(list_dist_Distance[m])):
                if list_pgd_all[m][d] != None:
                    list_mag.append(list_mag_all[m])
                    list_pgd.append(list_pgd_all[m][d])
                    list_dist.append(float(str(np.array(list_dist_Distance[m][d]))[:-3]))
                else:
                    someTrue -= 1
            if someTrue >0:
                eq += 1
    return list_mag, list_pgd, list_dist
        
def plot_pgd(title, mag_lim, corr_df):
    fig, axs = plt.subplots(1,1, figsize=(12.8,9.6))

    x = np.array(corr_df['mag'])-5
    y = corr_df['pgd']
    mask = ~np.isnan(x) & ~np.isnan(y)
    x_unique = np.arange(-2,3,0.1)
    #axs.scatter(x, y,  c = df['dist'], cmap = 'viridis')
    axs.scatter(x+np.random.uniform(-0.05, 0.05, len(x)), y, s = 10, c = '#003f5c', marker = 'x', alpha = 0.3)
    result = scipy.stats.linregress(x[mask],y[mask])
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

    #plt.scatter(x+np.random.uniform(-0.05, 0.05, len(x)),y, marker = 'x', color = 'k', s = 10, alpha = 0.5)
    axs.fill_between(x_unique, y_min_1sd, y_max_1sd, color = '#bc5090', alpha = 0.6, zorder = 100, label = '1sd')
    axs.fill_between(x_unique, y_min_2sd, y_max_2sd, color = '#ffa600', alpha = 0.6, zorder = 99, label = '2sd')

    axs.plot(x_unique, a*x_unique+b, color='#003f5c',zorder=102,label='{a:.2f}x+{b:.2f}\npearson r: {r:.4f}'.format(a=result.slope,b=result.intercept-5*result.slope,r=result.rvalue))
    plt.ylabel('log10(pgd)')
    plt.xlabel('magntitude')
    #plt.colorbar(label = 'distance') 
    axs.set_xticks([-2,-1,0,1,2,3], [3,4,5,6,7,8], zorder = 110)
    axs.legend()
    result_138 = result
    plt.ylim([-6.5,1])
    plt.savefig(f'/home/earthquakes1/homes/Rebecca/phd/seismo_det/figures/all_data/pgd/{title}/mag{mag_lim:.1f}_r138.pdf', format = 'pdf')
    plt.close()
    #081839

for f in filenames:
    if os.path.exists(f'/home/earthquakes1/homes/Rebecca/phd/seismo_det/figures/all_data/pgd/{f}') == False:
        os.makedirs(f'/home/earthquakes1/homes/Rebecca/phd/seismo_det/figures/all_data/pgd/{f}')
    for mag_lim in magnitudes:
        df = pd.read_pickle(f'/home/earthquakes1/homes/Rebecca/phd/data/results_database/{f}')
        list_mag, list_pgd, list_dist = sort_pgd_data(df, mag_lim)
        if len(list_mag)>1 and len(list_dist)>1 and len(list_pgd)>1:
            dist_corr_mult_alt = (np.array(list_dist)**1.38)*np.array(list_pgd)
            df3  = pd.DataFrame({'pgd':np.log10(dist_corr_mult_alt), 'mag':list_mag, 'dist':list_dist})
            plot_pgd(f, mag_lim, df3)
