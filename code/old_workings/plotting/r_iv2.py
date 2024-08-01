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
              'eq_object_03s_bandpass_01_19_snr_20_blank_01_new',
             'eq_object_05s_bandpass_01_19_snr_20_blank_0_new',
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
              'eq_object_4s_bandpass_01_19_snr_20_blank_05_new']

magnitudes = np.arange(3,8, 0.1)
def sort_iv2_data(df, mag_lim = 0):
    list_iv2_all = list(df.iv2)
    list_mag_all = list(df.eq_mag)
    list_dist_Distance = list(df.iv2_distances)
    list_dist = []
    list_mag = []
    list_iv2 = []
    eq = 0
    for m in range(0, len(list_mag_all)):
        if list_mag_all[m]>mag_lim:
            someTrue = len(list_iv2_all[m])
            for d in range(0, len(list_dist_Distance[m])):
                if list_iv2_all[m][d] != None:
                    list_mag.append(list_mag_all[m])
                    list_iv2.append(list_iv2_all[m][d])
                    list_dist.append(float(str(np.array(list_dist_Distance[m][d]))[:-3]))
    return list_mag, list_iv2, list_dist
        
def plot_iv2(title, mag_lim, corr_df, corr_type = '2'):
    fig, axs = plt.subplots(1,1, figsize=(12.8,9.6))
    x = np.array(corr_df['mag'])-5
    y = corr_df['iv2']
    x_unique = np.arange(-2,3,0.1)
    mask = ~np.isnan(x) & ~np.isnan(y)
    #axs.scatter(x, y,  c = df['dist'], cmap = 'viridis')
    axs.scatter(x+np.random.uniform(-0.05, 0.05, len(x)), y, s = 10, c = '#003f5c', marker = 'x', alpha = 0.3)
    result = scipy.stats.linregress(x[mask],y[mask])
    return result.rvalue


for f in filenames:
    pearson_r_2 = []
    pearson_r_138 = []
    if os.path.exists(f'/home/earthquakes1/homes/Rebecca/phd/seismo_det/figures/all_data/iv2/{f}') == False:
        os.makedirs(f'/home/earthquakes1/homes/Rebecca/phd/seismo_det/figures/all_data/iv2/{f}')
    for mag_lim in magnitudes:
        df = pd.read_pickle(f'/home/earthquakes1/homes/Rebecca/phd/data/results_database/{f}')
        list_mag, list_iv2, list_dist = sort_iv2_data(df, mag_lim)
        dist_corr_mult = (np.array(list_dist)**2)*np.array(list_iv2)
        df2  = pd.DataFrame({'iv2':np.log10(dist_corr_mult), 'mag':list_mag, 'dist':list_dist})
        df2.drop(df2[df2.iv2 < -13].index, inplace=True)
        df2.drop(df2[df2.iv2 > 3].index, inplace=True)
        dist_corr_mult_alt = (np.array(list_dist)**1.38)*np.array(list_iv2)
        df138  = pd.DataFrame({'iv2':np.log10(dist_corr_mult_alt), 'mag':list_mag, 'dist':list_dist})
        df138.drop(df138[df138.iv2 < -13].index, inplace=True)
        df138.drop(df138[df138.iv2 > 3].index, inplace=True)
        if len(set(df2['mag'])) > 1:
            pearson_r_2.append(plot_iv2(f, mag_lim, df2, corr_type = '2'))
        else: 
            pearson_r_2.append(0)
        if len(set(df138['mag'])) > 1:
            pearson_r_138.append(plot_iv2(f, mag_lim, df138, corr_type = '138'))
        else:
            pearson_r_138.append(0)
