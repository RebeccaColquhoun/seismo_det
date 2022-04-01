'''
uses objects to calculate iv2 and then puts those into dataframe and list
'''
import os
# import pickle
import pandas as pd
import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt
import obspy
import earthquake
import util

iv2_2 = pd.DataFrame({'3.0': [[], [], [], [], [], [], [], []],
                      '3.1': [[], [], [], [], [], [], [], []],
                      '3.2': [[], [], [], [], [], [], [], []],
                      '3.3': [[], [], [], [], [], [], [], []],
                      '3.4': [[], [], [], [], [], [], [], []],
                      '3.5': [[], [], [], [], [], [], [], []],
                      '3.6': [[], [], [], [], [], [], [], []],
                      '3.7': [[], [], [], [], [], [], [], []],
                      '3.8': [[], [], [], [], [], [], [], []],
                      '3.9': [[], [], [], [], [], [], [], []],
                      '4.0': [[], [], [], [], [], [], [], []],
                      '4.1': [[], [], [], [], [], [], [], []],
                      '4.2': [[], [], [], [], [], [], [], []],
                      '4.3': [[], [], [], [], [], [], [], []],
                      '4.4': [[], [], [], [], [], [], [], []],
                      '4.5': [[], [], [], [], [], [], [], []],
                      '4.6': [[], [], [], [], [], [], [], []],
                      '4.7': [[], [], [], [], [], [], [], []],
                      '4.8': [[], [], [], [], [], [], [], []],
                      '4.9': [[], [], [], [], [], [], [], []],
                      '5.0': [[], [], [], [], [], [], [], []],
                      '5.1': [[], [], [], [], [], [], [], []],
                      '5.2': [[], [], [], [], [], [], [], []],
                      '5.3': [[], [], [], [], [], [], [], []],
                      '5.4': [[], [], [], [], [], [], [], []],
                      '5.5': [[], [], [], [], [], [], [], []],
                      '5.6': [[], [], [], [], [], [], [], []],
                      '5.7': [[], [], [], [], [], [], [], []],
                      '5.8': [[], [], [], [], [], [], [], []],
                      '5.9': [[], [], [], [], [], [], [], []],
                      '6.0': [[], [], [], [], [], [], [], []],
                      '6.1': [[], [], [], [], [], [], [], []],
                      '6.2': [[], [], [], [], [], [], [], []],
                      '6.3': [[], [], [], [], [], [], [], []],
                      '6.4': [[], [], [], [], [], [], [], []],
                      '6.5': [[], [], [], [], [], [], [], []],
                      '6.6': [[], [], [], [], [], [], [], []],
                      '6.7': [[], [], [], [], [], [], [], []],
                      '6.8': [[], [], [], [], [], [], [], []],
                      '6.9': [[], [], [], [], [], [], [], []],
                      '7.0': [[], [], [], [], [], [], [], []]})
list_mag_2 = []
list_dist_2 = []
list_iv2_2 = []
iv2_4 = pd.DataFrame({'3.0': [[], [], [], [], [], [], [], []],
                      '3.1': [[], [], [], [], [], [], [], []],
                      '3.2': [[], [], [], [], [], [], [], []],
                      '3.3': [[], [], [], [], [], [], [], []],
                      '3.4': [[], [], [], [], [], [], [], []],
                      '3.5': [[], [], [], [], [], [], [], []],
                      '3.6': [[], [], [], [], [], [], [], []],
                      '3.7': [[], [], [], [], [], [], [], []],
                      '3.8': [[], [], [], [], [], [], [], []],
                      '3.9': [[], [], [], [], [], [], [], []],
                      '4.0': [[], [], [], [], [], [], [], []],
                      '4.1': [[], [], [], [], [], [], [], []],
                      '4.2': [[], [], [], [], [], [], [], []],
                      '4.3': [[], [], [], [], [], [], [], []],
                      '4.4': [[], [], [], [], [], [], [], []],
                      '4.5': [[], [], [], [], [], [], [], []],
                      '4.6': [[], [], [], [], [], [], [], []],
                      '4.7': [[], [], [], [], [], [], [], []],
                      '4.8': [[], [], [], [], [], [], [], []],
                      '4.9': [[], [], [], [], [], [], [], []],
                      '5.0': [[], [], [], [], [], [], [], []],
                      '5.1': [[], [], [], [], [], [], [], []],
                      '5.2': [[], [], [], [], [], [], [], []],
                      '5.3': [[], [], [], [], [], [], [], []],
                      '5.4': [[], [], [], [], [], [], [], []],
                      '5.5': [[], [], [], [], [], [], [], []],
                      '5.6': [[], [], [], [], [], [], [], []],
                      '5.7': [[], [], [], [], [], [], [], []],
                      '5.8': [[], [], [], [], [], [], [], []],
                      '5.9': [[], [], [], [], [], [], [], []],
                      '6.0': [[], [], [], [], [], [], [], []],
                      '6.1': [[], [], [], [], [], [], [], []],
                      '6.2': [[], [], [], [], [], [], [], []],
                      '6.3': [[], [], [], [], [], [], [], []],
                      '6.4': [[], [], [], [], [], [], [], []],
                      '6.5': [[], [], [], [], [], [], [], []],
                      '6.6': [[], [], [], [], [], [], [], []],
                      '6.7': [[], [], [], [], [], [], [], []],
                      '6.8': [[], [], [], [], [], [], [], []],
                      '6.9': [[], [], [], [], [], [], [], []],
                      '7.0': [[], [], [], [], [], [], [], []]})
list_mag_4 = []
list_dist_4 = []
list_iv2_4 = []

ROOT = '/home/earthquakes1/homes/Rebecca/phd/data/2019_global_m3/'
eq_list = os.listdir(ROOT)
cat = obspy.read_events('/home/earthquakes1/homes/Rebecca/phd/data/2019_global_m3_catalog.xml')

eq_with_data = []
cat_with_data = obspy.Catalog()  # cat.copy()
# cat_with_data.clear()
for event in cat:  # check earthquakes have data AND PICKS
    eq_name = util.catEventToFileName(event)
    if (os.path.isdir(ROOT+eq_name) and
            os.path.isdir(ROOT+eq_name+'/station_xml_files') and
            os.path.exists(ROOT+eq_name+'/picks.pkl')):
        eq_with_data.append(eq_name)
        cat_with_data.extend([event])

print('make object')
for eq_no in range(0, 100):  # len(eq_with_data)):
    eq = earthquake.Earthquake(eq_with_data[eq_no], cat_with_data[eq_no])
    eq.eq_info()
    eq.calc_iv2(window_length=2)
    print(eq.calculated_params['iv2'])
    for num_iv2 in range(len(eq.calculated_params['iv2'])):
        distance = eq.calculated_params['iv2'][num_iv2][1]
        current = iv2_2[str(np.round(eq.event_stats['eq_mag'], 1))][int(distance//25)]
        current.append(eq.calculated_params['iv2'][num_iv2][0])
        iv2_2[str(np.round(eq.event_stats['eq_mag'], 1))][int(distance//25)] = current
        list_iv2_2.append(eq.calculated_params['iv2'][num_iv2][0])
        list_mag_2.append(eq.event_stats['eq_mag'])
        list_dist_2.append(distance)
    eq.calc_iv2(window_length=4)
    print(eq.calculated_params['iv2'])
    for num_iv2 in range(len(eq.calculated_params['iv2'])):
        distance = eq.calculated_params['iv2'][num_iv2][1]
        current = iv2_4[str(np.round(eq.event_stats['eq_mag'], 1))][int(distance//25)]
        current.append(eq.calculated_params['iv2'][num_iv2][0])
        iv2_4[str(np.round(eq.event_stats['eq_mag'], 1))][int(distance//25)] = current
        list_iv2_4.append(eq.calculated_params['iv2'][num_iv2][0])
        list_mag_4.append(eq.event_stats['eq_mag'])
        list_dist_4.append(distance)
    # with open(root+eq_with_data[eq_no]+'/eq_object', )
# =============================================================================
#     if eq_no % 100 == 0:
#         iv2_4.to_pickle(ROOT+'iv2_dataframe_bkg_window4.pkl')
#         with open(ROOT+'list_iv2_bkg_window4', "wb") as fp:
#             pickle.dump(list_iv2_4, fp)
#         with open(ROOT+'list_mag_bkg_window4', "wb") as fp:
#             pickle.dump(list_mag_4, fp)
#         with open(ROOT+'list_dist_bkg_window4', "wb") as fp:
#             pickle.dump(list_dist_4, fp)
#         iv2_2.to_pickle(ROOT+'iv2_dataframe_bkg_window2.pkl')
#         with open(ROOT+'list_iv2_bkg_window2', "wb") as fp:
#             pickle.dump(list_iv2_2, fp)
#         with open(ROOT+'list_mag_bkg_window2', "wb") as fp:
#             pickle.dump(list_mag_2, fp)
#         with open(ROOT+'list_dist_bkg_window2', "wb") as fp:
#             pickle.dump(list_dist_2, fp)
# =============================================================================
        # counts[str(eq.event_stats['eq_mag'])][int(distance//25)] =
        # counts[str(eq.event_stats['eq_mag'])][int(distance//25)] + 1

def obj(to_opt):
    '''optimisation function'''
    a_opt=to_opt[0]
    b_opt=to_opt[1]
    #importance = np.array(n)
    y_real= np.log10(dist_corr_mult)
    x_list = np.array(mag_plot)
    y_guess = (a_opt*x_list+b_opt)
    return sum(abs(y_guess-y_real))


dist_plot = []
iv2_plot = []
mag_plot = []
for i, iv2_entry in enumerate(list_iv2_4):
    if iv2_entry is not None and list_dist_4[i] is not None and list_mag_4[i] is not None:
        iv2_plot.append(iv2_entry)
        dist_plot.append(list_dist_4[i])
        mag_plot.append(list_mag_4[i])

dist_corr_mult = (np.array(dist_plot)**2)*np.array(iv2_plot)

iv2_in_mag_bins =  [[] for _ in range(int((max(list_mag_4)-min(list_mag_4))*10)+1)]
for i, mag in enumerate(mag_plot):  # in range(0, len(list_mag_4)):
    iv2_in_mag_bins[int((mag-min(list_mag_4))*10)].append(dist_corr_mult[i])

mag_bin_medians = []
for l in iv2_in_mag_bins:
    mag_bin_medians.append(np.median(l))

plt.figure(figsize=(12,9))
plt.scatter(mag_plot, np.log10(dist_corr_mult),  c = dist_plot, cmap = 'inferno', alpha = 1)
plt.ylabel('log10(iv2)')
plt.xlabel('magntitude')
plt.colorbar(label = 'distance')
initial_guess = (1.4,0)
res = optimize.minimize(obj, initial_guess, method = 'Nelder-mead')
x = np.arange(3, max(mag_plot), 0.1)
y = res.x[0] * x + res.x[1]
plt.plot(x,y, label = str(res.x[0]) + '*x+'+ str(res.x[1]))
#plt.vlines(res.x[0], 0 , 4, color='tab:blue', label = 'optimize.minimize all data, 1-norm')
plt.legend()
plt.title('log10(iv2) referenced to 1km by multiplying by distance^2')
plt.scatter(np.arange(min(mag_plot), max(mag_plot), 0.1), np.log10(mag_bin_medians), marker = 'x', color = 'silver')
