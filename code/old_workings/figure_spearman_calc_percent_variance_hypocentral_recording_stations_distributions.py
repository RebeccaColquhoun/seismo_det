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
from scipy import stats
import matplotlib
from spearman_plotting_func import *


matplotlib.rcParams.update({'font.size': 14})

filenames = ['eq_object_03s_bandpass_01_19_snr_20_blank_0_new_snr20',
            'eq_object_05s_bandpass_01_19_snr_20_blank_0_new_snr20',
            'eq_object_1s_bandpass_01_19_snr_20_blank_0_new_snr20',
            'eq_object_4s_bandpass_01_19_snr_20_blank_0_new_snr20']
            # 'eq_object_03s_bandpass_01_19_snr_20_blank_0_new_snr5',
            #  'eq_object_03s_bandpass_01_19_snr_20_blank_005_new_snr5',
            #  'eq_object_03s_bandpass_01_19_snr_20_blank_01_new_snr5',
            #  'eq_object_05s_bandpass_01_19_snr_20_blank_0_new_snr5',
            #  'eq_object_05s_bandpass_01_19_snr_20_blank_005_new_snr5',
            #  'eq_object_05s_bandpass_01_19_snr_20_blank_01_new_snr5',
            #  'eq_object_05s_bandpass_01_19_snr_20_blank_025_new_snr5',
            #  'eq_object_1s_bandpass_01_19_snr_20_blank_0_new_snr5',
            #  'eq_object_1s_bandpass_01_19_snr_20_blank_005_new_snr5',
            #  'eq_object_1s_bandpass_01_19_snr_20_blank_01_new_snr5',
            #  'eq_object_1s_bandpass_01_19_snr_20_blank_025_new_snr5',
            #  'eq_object_1s_bandpass_01_19_snr_20_blank_05_new_snr5',
            #   'eq_object_4s_bandpass_01_19_snr_20_blank_0_new_snr5',
            #   'eq_object_4s_bandpass_01_19_snr_20_blank_005_new_snr5',
            #   'eq_object_4s_bandpass_01_19_snr_20_blank_01_new_snr5',
            #   'eq_object_4s_bandpass_01_19_snr_20_blank_025_new_snr5',gradt_spearman/
            #  'eq_object_05s_bandpass_01_19_snr_20_blank_0_new_snr20',
            #  'eq_object_05s_bandpass_01_19_snr_20_blank_005_new_snr20',
            #  'eq_object_05s_bandpass_01_19_snr_20_blank_01_new_snr20',
            #  'eq_object_05s_bandpass_01_19_snr_20_blank_025_new_snr20',
            #  'eq_object_1s_bandpass_01_19_snr_20_blank_0_new_snr20',
            #  'eq_object_1s_bandpass_01_19_snr_20_blank_005_new_snr20',
            #  'eq_object_1s_bandpass_01_19_snr_20_blank_01_new_snr20',
            #  'eq_object_1s_bandpass_01_19_snr_20_blank_025_new_snr20',
            #  'eq_object_1s_bandpass_01_19_snr_20_blank_05_new_snr20',
            #   'eq_object_4s_bandpass_01_19_snr_20_blank_0_new_snr20',
            #   'eq_object_4s_bandpass_01_19_snr_20_blank_005_new_snr20',
            #   'eq_object_4s_bandpass_01_19_snr_20_blank_01_new_snr20',
            #   'eq_object_4s_bandpass_01_19_snr_20_blank_025_new_snr20',
            #   'eq_object_4s_bandpass_01_19_snr_20_blank_05_new_snr20']



n_stations = 0
min_dist = 0
max_dist = 200

for f in filenames:
    print(f)
    df = pd.read_pickle(f'/home/earthquakes1/homes/Rebecca/phd/data/results_database_hypo/{f}')

    iv2_gradt = []
    iv2_gradt_std = []
    iv2_n = []
    tp_gradt = []
    tp_gradt_std = []
    tp_n = []
    pgd_gradt = []
    pgd_gradt_std = []
    pgd_n = []
    tc_gradt = []
    tc_gradt_std = []
    tc_n = []

    for n_stations in [1]:#range(0,7):
        for min_dist in [0]: #range(0, 100, 10):

            options = {'n': n_stations, 'min_dist': min_dist, 'max_dist': max_dist}
            x_tp, y_tp = calc_tp_mag_lim(df, 3.,**options)
            x_pgd, y_pgd = calc_pgd_mag_lim(df, 3.,**options)
            x_tc, y_tc = calc_tc_mag_lim(df, 3.,**options)
            x_iv2, y_iv2 = calc_iv2_mag_lim(df, 3.,**options)


            gradt, intercept, gradt_std, intercept_std = [],[],[],[]
            pearson = []
            spearman = []
            spearman_p = []
            n_l = []

            for mag_lim in magnitudes:
                x, y = calc_tp_mag_lim(df, mag_lim,**options)
                gradt, intercept, gradt_std, intercept_std, pearson, spearman, spearman_p, n = calc_opt(x,y, gradt, intercept, gradt_std, intercept_std, pearson, spearman, spearman_p, n_l)
            tp_params = [gradt, gradt_std, np.array(pearson)**2, spearman, spearman_p, n, 'tp']
            tp_gradt.append(gradt[0])
            tp_gradt_std.append(gradt_std[0])
            tp_n.append(n[0])


            gradt, intercept, gradt_std, intercept_std = [],[],[],[]
            pearson = []
            spearman = []
            spearman_p = []
            n_l = []

            for mag_lim in magnitudes:
                x, y = calc_pgd_mag_lim(df, mag_lim,**options)
                gradt, intercept, gradt_std, intercept_std, pearson, spearman, spearman_p, n = calc_opt(x,y, gradt, intercept, gradt_std, intercept_std, pearson, spearman, spearman_p, n_l)
            pgd_params = [gradt, gradt_std, np.array(pearson)**2, spearman, spearman_p, n,  'pgd']
            pgd_gradt.append(gradt[0])
            pgd_gradt_std.append(gradt_std[0])
            pgd_n.append(n[0])

            gradt, intercept, gradt_std, intercept_std = [],[],[],[]
            pearson = []
            spearman = []
            spearman_p = []
            n_l = []

            for mag_lim in magnitudes:
                x, y = calc_tc_mag_lim(df, mag_lim,**options)
                gradt, intercept, gradt_std, intercept_std, pearson, spearman, spearman_p, n = calc_opt(x,y, gradt, intercept, gradt_std, intercept_std, pearson, spearman, spearman_p, n_l)
            tc_params = [gradt, gradt_std, np.array(pearson)**2, spearman, spearman_p, n, 'tc']
            tc_gradt.append(gradt[0])
            tc_gradt_std.append(gradt_std[0])
            tc_n.append(n[0])

            gradt, intercept, gradt_std, intercept_std = [],[],[],[]
            pearson = []
            spearman = []
            spearman_p = []
            n_l = []

            for mag_lim in magnitudes:
                x, y = calc_iv2_mag_lim(df, mag_lim,**options)
                gradt, intercept, gradt_std, intercept_std, pearson, spearman, spearman_p, n = calc_opt(x,y, gradt, intercept, gradt_std, intercept_std, pearson, spearman, spearman_p, n_l)
            iv2_params = [gradt, gradt_std, np.array(pearson)**2, spearman, spearman_p, n,'iv2']
            iv2_gradt.append(gradt[0])
            iv2_gradt_std.append(gradt_std[0])
            iv2_n.append(n[0])

            plot_spearman_subplots_all_on_one_no_n_shaded_percent_var(f, tp_params, pgd_params, iv2_params, tc_params, log = False, save = True, **options)
