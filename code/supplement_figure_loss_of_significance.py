import os
import numpy as np
import pandas as pd
import matplotlib
import spearman_plotting_func as spearman_plotting
import setup_paths as paths
import matplotlib.pyplot as plt



matplotlib.rcParams.update({'font.size': 14})


filenames = ['eq_object_03s_bandpass_01_19_snr_20_blank_0_new_snr20',
             'eq_object_05s_bandpass_01_19_snr_20_blank_0_new_snr20',
             'eq_object_1s_bandpass_01_19_snr_20_blank_0_new_snr20',
             'eq_object_4s_bandpass_01_19_snr_20_blank_0_new_snr20']


min_dist = 0
max_dist = 200
n_stations = 1


tp_loss_significance = []
tc_loss_significance = []
pgd_loss_significance = []
iv2_loss_significance = []

n_stations_list = []
min_dist_list = []
max_dist_list = []

tp_n = []
tc_n = []
pgd_n = []
iv2_n = []

f = filenames[0]
df = pd.read_pickle(f'{paths.base_path}/paper_data/{f}')

# can run for multiple (minimum) n_stations and min_dist, but for now just look at all data
for n_stations in range(1, 7):
    for min_dist in range(0, 100, 10):
        for max_dist in range(0, 200, 10):
            if min_dist >= max_dist:
                continue
            print(f'n_stations: {n_stations}, min_dist: {min_dist}, max_dist: {max_dist}')

            # prepare data
            options = {'n': n_stations, 'min_dist': min_dist, 'max_dist': max_dist}
            x_tp, y_tp = spearman_plotting.calc_tp_mag_lim(df, 3., **options)
            x_pgd, y_pgd = spearman_plotting.calc_pgd_mag_lim(df, 3., **options)
            x_tc, y_tc = spearman_plotting.calc_tc_mag_lim(df, 3., **options)
            x_iv2, y_iv2 = spearman_plotting.calc_iv2_mag_lim(df, 3., **options)

            # predominant period
            # define empty lists to store the results
            gradt, intercept, gradt_std, intercept_std = [], [], [], []
            pearson = []
            spearman = []
            spearman_p = []
            n_l = []

            # loop over magnitudes and calculate statistical values for each. append to lists just defined.
            for mag_lim in spearman_plotting.magnitudes:
                x, y = spearman_plotting.calc_tp_mag_lim(df, mag_lim, **options)
                output = spearman_plotting.calc_opt(x, y,
                                                    gradt,
                                                    intercept,
                                                    gradt_std,
                                                    intercept_std,
                                                    pearson,
                                                    spearman,
                                                    spearman_p,
                                                    n_l)
                gradt, intercept, gradt_std, intercept_std, pearson, spearman, spearman_p, n = output
            tp_params = [gradt, gradt_std, np.array(pearson)**2, spearman, spearman_p, n, 'tp']

            # average period
            # define empty lists to store the results
            gradt, intercept, gradt_std, intercept_std = [], [], [], []
            pearson = []
            spearman = []
            spearman_p = []
            n_l = []
            # loop over magnitudes and calculate statistical values for each. append to lists just defined.
            for mag_lim in spearman_plotting.magnitudes:
                x, y = spearman_plotting.calc_tc_mag_lim(df, mag_lim, **options)
                output = spearman_plotting.calc_opt(x, y,
                                                    gradt,
                                                    intercept,
                                                    gradt_std,
                                                    intercept_std,
                                                    pearson,
                                                    spearman,
                                                    spearman_p,
                                                    n_l)
                gradt, intercept, gradt_std, intercept_std, pearson, spearman, spearman_p, n = output
            tc_params = [gradt, gradt_std, np.array(pearson)**2, spearman, spearman_p, n, 'tc']

            # peak ground displacement
            # define empty lists to store the results
            gradt, intercept, gradt_std, intercept_std = [], [], [], []
            pearson = []
            spearman = []
            spearman_p = []
            n_l = []

            # loop over magnitudes and calculate statistical values for each. append to lists just defined.
            for mag_lim in spearman_plotting.magnitudes:
                x, y = spearman_plotting.calc_pgd_mag_lim(df, mag_lim, **options)
                output = spearman_plotting.calc_opt(x, y,
                                                    gradt,
                                                    intercept,
                                                    gradt_std,
                                                    intercept_std,
                                                    pearson,
                                                    spearman,
                                                    spearman_p,
                                                    n_l)
                gradt, intercept, gradt_std, intercept_std, pearson, spearman, spearman_p, n = output
            pgd_params = [gradt, gradt_std, np.array(pearson)**2, spearman, spearman_p, n, 'pgd']

            # iv2
            # define empty lists to store the results
            gradt, intercept, gradt_std, intercept_std = [], [], [], []
            pearson = []
            spearman = []
            spearman_p = []
            n_l = []
            # loop over magnitudes and calculate statistical values for each. append to lists just defined.
            for mag_lim in spearman_plotting.magnitudes:
                x, y = spearman_plotting.calc_iv2_mag_lim(df, mag_lim, **options)
                output = spearman_plotting.calc_opt(x, y,
                                                    gradt,
                                                    intercept,
                                                    gradt_std,
                                                    intercept_std,
                                                    pearson,
                                                    spearman,
                                                    spearman_p,
                                                    n_l)
                gradt, intercept, gradt_std, intercept_std, pearson, spearman, spearman_p, n = output
            iv2_params = [gradt, gradt_std, np.array(pearson)**2, spearman, spearman_p, n, 'iv2']
            if len(np.where(np.array(tp_params[4])>0.05)[0]) > 0:
                tp_loss_significance.append(np.where(np.array(tp_params[4])>0.05)[0][0])
                tp_n.append(tp_params[5][np.where(np.array(tp_params[4])>0.05)[0][0]])
            else:
                tp_loss_significance.append(len(tp_params[4]))
                tp_n.append(tp_params[5][-1])
            if len(np.where(np.array(tc_params[4])>0.05)[0]) > 0:
                tc_loss_significance.append(np.where(np.array(tc_params[4])>0.05)[0][0])
                tc_n.append(tc_params[5][np.where(np.array(tc_params[4])>0.05)[0][0]])
            else:
                tc_loss_significance.append(len(tc_params[4]))
                tc_n.append(tc_params[5][-1])
            if len(np.where(np.array(pgd_params[4])>0.05)[0]) > 0:
                pgd_loss_significance.append(np.where(np.array(pgd_params[4])>0.05)[0][0])
                pgd_n.append(pgd_params[5][np.where(np.array(pgd_params[4])>0.05)[0][0]])
            else:
                pgd_loss_significance.append(len(pgd_params[4]))
                pgd_n.append(pgd_params[5][-1])
            if len(np.where(np.array(iv2_params[4])>0.05)[0]) > 0:
                iv2_loss_significance.append(np.where(np.array(iv2_params[4])>0.05)[0][0])
                iv2_n.append(iv2_params[5][np.where(np.array(iv2_params[4])>0.05)[0][0]])
            else:
                iv2_loss_significance.append(len(iv2_params[4]))
                iv2_n.append(iv2_params[5][-1])
            
            # tp_n.append(tp_params[5][np.where(np.array(tp_params[4])>0.05)[0][0]])
            # tc_n.append(tc_params[5][np.where(np.array(tc_params[4])>0.05)[0][0]])
            # pgd_n.append(pgd_params[5][np.where(np.array(pgd_params[4])>0.05)[0][0]])
            # iv2_n.append(iv2_params[5][np.where(np.array(iv2_params[4])>0.05)[0][0]])
            
            n_stations_list.append(n_stations)
            min_dist_list.append(min_dist)
            max_dist_list.append(max_dist)

# print(pgd_loss_significance)
# print(pgd_n)
# print(pgd_params[4])
# print(np.where(np.array(pgd_params[4])>0.05)[0][0])

# Write min_dist_list to file
with open(f'{f}_min_dist_list.txt', 'w') as file:
    for item in min_dist_list:
        file.write("%s\n" % item)

# Write max_dist_list to file
with open(f'{f}_max_dist_list.txt', 'w') as file:
    for item in max_dist_list:
        file.write("%s\n" % item)

# Write tp_loss_significance to file
with open(f'{f}_tp_loss_significance.txt', 'w') as file:
    for item in tp_loss_significance:
        file.write("%s\n" % item)

# Write tc_loss_significance to file
with open(f'{f}_tc_loss_significance.txt', 'w') as file:
    for item in tc_loss_significance:
        file.write("%s\n" % item)

# Write iv2_loss_significance to file
with open(f'{f}_iv2_loss_significance.txt', 'w') as file:
    for item in iv2_loss_significance:
        file.write("%s\n" % item)

# Write pgd_loss_significance to file
with open(f'{f}_pgd_loss_significance.txt', 'w') as file:
    for item in pgd_loss_significance:
        file.write("%s\n" % item)

# Write n_stations_list to file
with open(f'{f}_n_stations_list.txt', 'w') as file:
    for item in n_stations_list:
        file.write("%s\n" % item)

# Write tp_n to file
with open(f'{f}_tp_n.txt', 'w') as file:
    for item in tp_n:
        file.write("%s\n" % item)

# Write tc_n to file
with open(f'{f}_tc_n.txt', 'w') as file:
    for item in tc_n:
        file.write("%s\n" % item)

# Write iv2_n to file
with open(f'{f}_iv2_n.txt', 'w') as file:
    for item in iv2_n:
        file.write("%s\n" % item)	

# Write pgd_n to file	
with open(f'{f}_pgd_n.txt', 'w') as file:
    for item in pgd_n:
        file.write("%s\n" % item)	
