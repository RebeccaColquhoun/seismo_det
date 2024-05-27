import numpy as np
import os
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats

import matplotlib
matplotlib.rcParams.update({'font.size': 14})

from spearman_plotting_func import *

data_path = '/Users/rebecca/Documents/PhD/Research/Frequency/data/results_database_hypo'
save_path = '/Users/rebecca/Documents/PhD/Research/Frequency/seismo_det/figures/overlaps/hypocentral'

def test_overlap_subplots(params):
    print('testing overlap')
    param_names = ['tp', 'tc', 'iv2', 'pgd']
    colors = {'tp': '#7f58af', 'tc': '#e84d8a', 'iv2': '#64c5eb', 'pgd': '#7fb646'}
    colors_darker = {'tp': '#251A32', 'tc': '#5c2037', 'iv2': '#2b5160', 'pgd': '#39511f'}
    fig, axs = plt.subplots(2, 2, figsize = (12, 9))
    marker = ''
    always_significant = ''
    for i, p in enumerate(params):
        param_name = param_names[i]
        print(param_name)
        param_color = colors[param_name]
        flip_color = colors_darker[param_name]

        row, col = i%2, i//2

        res = [idx for idx, val in enumerate(p[4]) if val > 0.05]
        if len(res) > 0:
            flip = res[0]
        else:
            flip = -1
            always_significant += f'{param_name} '


        if p[0][flip] >= p[0][0]-p[1][0] and p[0][flip] <= p[0][0]+ p[1][0]:
            print('overlap at 1 s.d.')
            print(f'{p[0][flip]} in range [{p[0][0]-p[1][0]}, {p[0][0]+p[1][0]}]')
            marker = marker + '1_'
        else:
            marker = marker + '0_'
        if p[0][flip] >= p[0][0]-2*p[1][0] and p[0][flip] <= p[0][0]+2*p[1][0]:
            print('overlap at 2 s.d.')
            print(f'{p[0][flip]} in range [{p[0][0]-2*p[1][0]}, {p[0][0]+2*p[1][0]}]')
            marker = marker + '1_'
        else:
            marker = marker + '0_'
        if p[0][flip] <= p[0][0]-2*p[1][0] or p[0][flip] >= p[0][0]+2*p[1][0]:
            print('no overlap at 2 s.d')
            print(f'{p[0][flip]} NOT in range [{p[0][0]-2*p[1][0]}, {p[0][0]+2*p[1][0]}]')

        mu = p[0][0]
        sigma = p[1][0]
        x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
        pdf = stats.norm.pdf(x, mu, sigma)
        axs[row][col].plot(x, pdf, label = 'with all data', color = param_color)
        axs[row][col].fill_between(x, pdf, color = param_color, alpha = 0.5)
        axs[row][col].vlines(p[0][0], 0, max(pdf), color = param_color, linestyle = '-')

        difference_array = np.absolute(x-(p[0][0]-p[1][0]))
        index = difference_array.argmin()
        axs[row][col].vlines(p[0][0]-p[1][0], 0, pdf[index], color = param_color, linestyle = '--')
        axs[row][col].vlines(p[0][0]+p[1][0], 0, pdf[100-index], color = param_color, linestyle = '--')

        difference_array = np.absolute(x-(p[0][0]-2*p[1][0]))
        index = difference_array.argmin()
        axs[row][col].vlines(p[0][0]-2*p[1][0], 0, pdf[index], color = param_color, linestyle = ':')
        axs[row][col].vlines(p[0][0]+2*p[1][0], 0, pdf[100-index], color = param_color, linestyle = ':')

        mu = p[0][flip]
        sigma = p[1][flip]
        x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
        pdf = stats.norm.pdf(x, mu, sigma)
        axs[row][col].plot(x, pdf, label = 'at loss of significance', color = flip_color)
        axs[row][col].fill_between(x, pdf, color = flip_color, alpha = 0.5)
        axs[row][col].vlines(p[0][flip], 0, max(pdf), color = flip_color, linestyle = '-')

        difference_array = np.absolute(x-(p[0][flip]-p[1][flip]))
        index = difference_array.argmin()
        axs[row][col].vlines(p[0][flip]-p[1][flip], 0, pdf[index], color = flip_color, linestyle = '--')
        axs[row][col].vlines(p[0][flip]+p[1][flip], 0, pdf[100-index], color = flip_color, linestyle = '--')

        difference_array = np.absolute(x-(p[0][flip]-2*p[1][flip]))
        index = difference_array.argmin()
        axs[row][col].vlines(p[0][flip]-2*p[1][flip], 0, pdf[index], color = flip_color, linestyle = ':')
        axs[row][col].vlines(p[0][flip]+2*p[1][flip], 0, pdf[100-index], color = flip_color, linestyle = ':')
        axs[row][col].set_xlabel(f'{param_name}')#, 1/2 s.d. {marker}, \n flip = {p[0][flip]:.4f}, \n 1 s.d. = [{p[0][0]-1*p[1][0]:.4f}, {p[0][0]+1*p[1][0]:.4f}], \n 2 s.d. = [{p[0][0]-2*p[1][0]:.4f}, {p[0][0]+2*p[1][0]:.4f}]')
        axs[row][col].legend()

    if always_significant == '':
        fig.suptitle('overlap: ' + marker[:-1])
        fig.tight_layout()
        fig.savefig(f'{save_path}/{f}_nstations_{n_stations}_mindist_{min_dist}_overlap_{marker[:-1]}.png')

    else:
        fig.suptitle('overlap: ' + marker[:-1] + f' always significant: {always_significant}')
        fig.tight_layout()
        fig.savefig(f'{save_path}/{f}_nstations_{n_stations}_mindist_{min_dist}_overlap_{marker[:-1]}_always_significant_{always_significant}.png')

filenames = os.listdir('{data_path}/')
# ['eq_object_03s_bandpass_01_19_snr_20_blank_0_new_snr20',
#              'eq_object_05s_bandpass_01_19_snr_20_blank_0_new_snr20',
#              'eq_object_1s_bandpass_01_19_snr_20_blank_0_new_snr20',
#              'eq_object_4s_bandpass_01_19_snr_20_blank_0_new_snr20']

max_dist = 200
for f in filenames:
    print(f)
    df = pd.read_pickle(f'{data_path}/{f}')
    # print(df.head(10))
    for n_stations in range(0,7):
        for min_dist in range(0, 100, 10):
            options = {'n': n_stations, 'min_dist': min_dist, 'max_dist': max_dist}
            print(f'n_stations: {n_stations}, min_dist: {min_dist}, max_dist: {max_dist}')
            gradt, intercept, gradt_std, intercept_std = [],[],[],[]
            pearson = []
            spearman = []
            spearman_p = []
            n_l = []

            for mag_lim in magnitudes:
                x, y = calc_tp_mag_lim(df, mag_lim,**options)
                gradt, intercept, gradt_std, intercept_std, pearson, spearman, spearman_p, n = calc_opt(x,y, gradt, intercept, gradt_std, intercept_std, pearson, spearman, spearman_p, n_l)
            tp_params = [gradt, gradt_std, np.array(pearson)**2, spearman, spearman_p, n, 'tp']
            if len(spearman)>0:
                print('tp', spearman[0])

            gradt, intercept, gradt_std, intercept_std = [],[],[],[]
            pearson = []
            spearman = []
            spearman_p = []
            n_l = []

            for mag_lim in magnitudes:
                x, y = calc_pgd_mag_lim(df, mag_lim,**options)
                gradt, intercept, gradt_std, intercept_std, pearson, spearman, spearman_p, n = calc_opt(x,y, gradt, intercept, gradt_std, intercept_std, pearson, spearman, spearman_p, n_l)
            pgd_params = [gradt, gradt_std, np.array(pearson)**2, spearman, spearman_p, n,  'pgd']
            if len(spearman)>0:
                print('pgd', spearman[0])

            gradt, intercept, gradt_std, intercept_std = [],[],[],[]
            pearson = []
            spearman = []
            spearman_p = []
            n_l = []

            for mag_lim in magnitudes:
                x, y = calc_tc_mag_lim(df, mag_lim,**options)
                gradt, intercept, gradt_std, intercept_std, pearson, spearman, spearman_p, n = calc_opt(x,y, gradt, intercept, gradt_std, intercept_std, pearson, spearman, spearman_p, n_l)
            tc_params = [gradt, gradt_std, np.array(pearson)**2, spearman, spearman_p, n, 'tc']
            if len(spearman)>0:
                print('tc', spearman[0])

            gradt, intercept, gradt_std, intercept_std = [],[],[],[]
            pearson = []
            spearman = []
            spearman_p = []
            n_l = []

            for mag_lim in magnitudes:
                x, y = calc_iv2_mag_lim(df, mag_lim,**options)
                gradt, intercept, gradt_std, intercept_std, pearson, spearman, spearman_p, n = calc_opt(x,y, gradt, intercept, gradt_std, intercept_std, pearson, spearman, spearman_p, n_l)

            iv2_params = [gradt, gradt_std, np.array(pearson)**2, spearman, spearman_p, n,'iv2']
            if len(spearman)>0:
                print('iv2', spearman[0])

            test_overlap_subplots([tp_params, tc_params, iv2_params, pgd_params])
