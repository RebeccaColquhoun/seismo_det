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
    #fig, axs = plt.subplots(1,1, figsize=(12.8,9.6))

    x = np.array(corr_df['mag'])-5
    y = corr_df['pgd']
    mask = ~np.isnan(x) & ~np.isnan(y)
    x_unique = np.arange(-2,3,0.1)
    #axs.scatter(x, y,  c = df['dist'], cmap = 'viridis')
    #axs.scatter(x+np.random.uniform(-0.05, 0.05, len(x)), y, s = 10, c = '#003f5c', marker = 'x', alpha = 0.3)
    result = scipy.stats.linregress(x[mask],y[mask])
    return result.rvalue
    #081839

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
    #fig, axs = plt.subplots(1,1, figsize=(12.8,9.6))
    x = np.array(corr_df['mag'])-5
    y = corr_df['iv2']
    x_unique = np.arange(-2,3,0.1)
    mask = ~np.isnan(x) & ~np.isnan(y)
    #axs.scatter(x, y,  c = df['dist'], cmap = 'viridis')
    #axs.scatter(x+np.random.uniform(-0.05, 0.05, len(x)), y, s = 10, c = '#003f5c', marker = 'x', alpha = 0.3)
    result = scipy.stats.linregress(x[mask],y[mask])
    return result.rvalue


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
        #fig, axs = plt.subplots(1,1, figsize=(12.8,9.6))
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
                    #if len(x_tp)>0:
                        #if math.isnan(np.median(y_tp))==False:
                            #axs.scatter(list_mags[i]-5+np.random.uniform(-0.05, 0.05), np.median(y_tp), s = 10, c = '#003f5c', marker = 'x', zorder =110, alpha = 0.5)
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
            return result.rvalue
        else:
            return 0



df_results = pd.DataFrame(columns = [
'filename',
'pgd_r',
'pgd_n',
'tpmax_r',
'tpmax_n',
'iv2_r2_r',
'iv2_r2_n',
'iv2_r138_r',
'iv2_r138_n'])
for f in filenames:
    pearson_r_2_int = []
    pearson_r_138_int = []
    pearson_pgd_int = []
    tpmax_r_int = []
    pgd_n_int = []
    tp_max_n_int = []
    iv2_r2_n_int = []
    iv2_r138_n_int = []
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
            pearson_r_2_int.append(plot_iv2(f, mag_lim, df2, corr_type = '2'))
            iv2_r2_n_int.append(len(list_mag))
        else:
            iv2_r2_n_int.append(0)
            pearson_r_2_int.append(0)
        if len(set(df138['mag'])) > 1:
            iv2_r138_n_int.append(list_mag)
            pearson_r_138_int.append(plot_iv2(f, mag_lim, df138, corr_type = '138'))
        else:
            iv2_r138_n_int.append(0)
            pearson_r_138_int.append(0)
        list_mag, list_pgd, list_dist = sort_pgd_data(df, mag_lim)
        if len(list_mag)>1 and len(list_dist)>1 and len(list_pgd)>1:
            dist_corr_mult_alt = (np.array(list_dist)**1.38)*np.array(list_pgd)
            df3  = pd.DataFrame({'pgd':np.log10(dist_corr_mult_alt), 'mag':list_mag, 'dist':list_dist})
            pgd_n_int.append(len(list_mag))
            pearson_pgd_int.append(plot_pgd(f, mag_lim, df3))
        else:
            pgd_n_int.append(0)
            pearson_pgd_int.append(0)
        list_mags, list_tpmax = sort_tp_data(df, mag_lim)
        if len(set(list_mags)) > 1:
            tp_max_n_int.append(len(list_mags))
            tpmax_r_int.append(plot_tpmax(f, mag_lim, list_mags, list_tpmax))
        else:
            tp_max_n_int.append(0)
            tpmax_r_int.append(0)            
    df_results_2 = pd.DataFrame({'filename':[f],'pgd_r':[pearson_pgd_int],
        'pgd_n':[pgd_n_int],
        'tpmax_r':[tpmax_r_int],
        'tpmax_n':[tp_max_n_int],
        'iv2_r2_r':[pearson_r_2_int],
        'iv2_r2_n':[iv2_r2_n_int],
        'iv2_r138_r':[pearson_r_138_int],
        'iv2_r138_n':[iv2_r138_n_int]})
    df_results = pd.concat([df_results,df_results_2])
#df = df.reset_index()

plt.close('all')

colors = ['#7f58af', '#64c5eb', '#e84d8a', '#feb326']
colors_list = [colors[0], colors[0],colors[0], colors[1],colors[1],colors[1],colors[1], colors[2],colors[2],colors[2],colors[2],colors[2],colors[3],colors[3],colors[3],colors[3],colors[3]]
line_style = ['solid','dotted','dashed','solid','dotted','dashed','dashdot', 'solid', 'dotted', 'dashed', 'dashdot', (0, (5, 10)),'solid', 'dotted', 'dashed', 'dashdot', (0, (5, 10))]

for row in [0,3,7,12]:#range(0, len(df_results)):
    plt.plot(magnitudes, df_results.iloc[row]['iv2_r2_r'], label = df_results.iloc[row]['filename'], color = colors_list[row],linestyle = line_style[row])

plt.vlines([4,4.4,5],-1,1, color = ['k', 'k','k'])
plt.legend(fontsize=10)
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(18.5, 10.5)
plt.title('iv2 r^2')
plt.ylabel('pearson r')
plt.xlabel('magnitude')
plt.savefig('iv2_r2_r_different_mag.pdf')
plt.close('all')
for row in [0,3,7,12]:#range(0, len(df_results)):
    plt.plot(magnitudes, df_results.iloc[row]['pgd_r'], label = df_results.iloc[row]['filename'], color = colors_list[row],linestyle = line_style[row])

plt.vlines([4,4.4,5],-1,1, color = ['k', 'k','k'])
plt.legend(fontsize=10)
fig = matplotlib.pyplot.gcf()
plt.title('pgd')
plt.ylabel('pearson r')
plt.xlabel('magnitude')
fig.set_size_inches(18.5, 10.5)
plt.savefig('pgd_r_different_mag.pdf')
plt.close('all')


for row in range(0, len(df_results)):
    plt.plot(magnitudes, df_results.iloc[row]['tpmax_r'], label = df_results.iloc[row]['filename'], color = colors_list[row],linestyle = line_style[row])


plt.vlines([4,4.4,5],-1,1, color = ['k', 'k','k'])
plt.legend(fontsize=10)
fig = matplotlib.pyplot.gcf()
plt.ylabel('pearson r')
plt.xlabel('magnitude')
plt.title('tpmax')
fig.set_size_inches(18.5, 10.5)
plt.savefig('tpmax_r_different_mag.pdf')
plt.close('all')