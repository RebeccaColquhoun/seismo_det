import numpy as np
# import os
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats

from spearman_plotting_func import magnitudes
from spearman_plotting_func import calc_tp_mag_lim, calc_pgd_mag_lim, calc_tc_mag_lim, calc_iv2_mag_lim, calc_opt

import matplotlib
matplotlib.rcParams.update({'font.size': 14})


hypo = True
laptop = False

if hypo and not laptop:
    data_path = '/home/earthquakes1/homes/Rebecca/phd/data/results_database_hypo'
    save_path = '/home/earthquakes1/homes/Rebecca/phd/seismo_det/figures/gradt_hist_subplots/hypocentral'
elif not hypo and not laptop:
    data_path = '/home/earthquakes1/homes/Rebecca/phd/data/results_database'
    save_path = '/home/earthquakes1/homes/Rebecca/phd/seismo_det/figures/gradt_hist_subplots/epicentral'
elif hypo and laptop:
    data_path = '/Users/rebecca/Documents/PhD/Research/Frequency/data/results_database_hypo'
    save_path = '/Users/rebecca/Documents/PhD/Research/Frequency/seismo_det/figures/overlaps/scaled/hypocentral'
elif not hypo and laptop:
    data_path = '/Users/rebecca/Documents/PhD/Research/Frequency/data/results_database'
    save_path = '/Users/rebecca/Documents/PhD/Research/Frequency/seismo_det/figures/overlaps/scaled/epicentral'

durations = pd.DataFrame([[4.0, 4.45, 5.05, 6.25],
                          [4.6, 5.05, 5.65, 6.85],
                          [4.95, 5.4, 6.0, 7.2],
                          [6.0, 6.45, 7.05, 7.95]],
                         ['03s', '05s', '1s', '4s'],
                         ['one', 'two', 'three', 'ten'])

tp_df = pd.DataFrame(index=['03s_gradt', '03s_std',
                            '05s_gradt', '05s_std',
                            '1s_gradt', '1s_std',
                            '4s_gradt', '4s_std'],
                     columns=['one', 'two', 'three', 'ten'])

tc_df = pd.DataFrame(index=['03s_gradt', '03s_std',
                            '05s_gradt', '05s_std',
                            '1s_gradt', '1s_std',
                            '4s_gradt', '4s_std'],
                     columns=['one', 'two', 'three', 'ten'])

pgd_df = pd.DataFrame(index=['03s_gradt', '03s_std',
                             '05s_gradt', '05s_std',
                             '1s_gradt', '1s_std',
                             '4s_gradt', '4s_std'],
                      columns=['one', 'two', 'three', 'ten'])

iv2_df = pd.DataFrame(index=['03s_gradt', '03s_std',
                             '05s_gradt', '05s_std',
                             '1s_gradt', '1s_std',
                             '4s_gradt', '4s_std'],
                      columns=['one', 'two', 'three', 'ten'])


def gradt_hist_subplots(params, scale_size='one'):

    param_names = ['tp', 'tc', 'iv2', 'pgd']
    # colors = {'tp': '#7f58af', 'tc': '#e84d8a', 'iv2': '#64c5eb', 'pgd': '#7fb646'}
    # colors_darker = {'tp': '#4f407a', 'tc': '#5c2037', 'iv2': '#2b5160', 'pgd': '#39511f'}
    colors = {'tp': {'03s': '#4f407a', '05s': '#7f58af', '1s': '#d2c2ff', '4s': '#e9e0ff'},
              'tc': {'03s': '#a23679', '05s': '#e84d8a', '1s': '#ffaadf', '4s': '#ffd4ef'},
              'iv2': {'03s': '#0f5571', '05s': '#1788b5', '1s': '#66c5eb', '4s': '#b6f4ff'},
              'pgd': {'03s': '#4e6e2b', '05s': '#679339', '1s': '#7fb646', '4s': '#a7cd7e'}}

    fig, axs = plt.subplots(2, 2, figsize=(12, 9))
    marker = ''

    for i, p in enumerate(params):
        param_name = param_names[i]
        print(param_name)


        c = colors[param_name]

        row, col = i % 2, i // 2
        for time in ['03s', '05s', '1s', '4s']:
            mu = p.loc[f'{time}_gradt'][scale_size]
            sigma = p.loc[f'{time}_std'][scale_size]

            x = np.linspace(mu - 3 * sigma, mu + 3 * sigma, 100)
            pdf = stats.norm.pdf(x, mu, sigma)
            axs[row][col].plot(x, pdf, label=time, color=c[time])
            axs[row][col].fill_between(x, pdf, color=c[time], alpha=0.5)
            axs[row][col].vlines(mu, 0, max(pdf), color=c[time], linestyle='-')

            difference_array = np.absolute(x - (mu - sigma))
            index = difference_array.argmin()
            axs[row][col].vlines(mu - sigma, 0, pdf[index], color=c[time], linestyle='--')
            axs[row][col].vlines(mu + sigma, 0, pdf[100 - index], color=c[time], linestyle='--')

            difference_array = np.absolute(x - (mu - 2 * sigma))
            index = difference_array.argmin()
            axs[row][col].vlines(mu - 2 * sigma, 0, pdf[index], color=c[time], linestyle=':')
            axs[row][col].vlines(mu + 2 * sigma, 0, pdf[100 - index], color=c[time], linestyle=':')

        axs[row][col].legend()

    fig.suptitle(f'Distribution of gradients for different time windows \n min mag corresponding to {scale_size} x earthquake')
    fig.tight_layout()
    fig.savefig(f'{save_path}/scale_{scale_size}.png')


def fill_out_df(df_param, params, f, scale_size='one'):
    time = f[10:].split('_')[0]

    flip_mag = durations.loc[time][scale_size]
    idx = int((flip_mag - 3) * 10)

    idx = min(idx, len(params[0]) - 1)

    gradt = time + '_gradt'
    std = time + '_std'
    df_param.loc[gradt][scale_size] = params[0][idx]
    df_param.loc[std][scale_size] = params[1][idx]
    return df_param


# filenames = os.listdir(f'{data_path}/')
filenames = ['eq_object_03s_bandpass_01_19_snr_20_blank_0_new_snr20',
             'eq_object_05s_bandpass_01_19_snr_20_blank_0_new_snr20',
             'eq_object_1s_bandpass_01_19_snr_20_blank_0_new_snr20',
             'eq_object_4s_bandpass_01_19_snr_20_blank_0_new_snr20']

max_dist = 200
for f in filenames:
    print(f)
    df = pd.read_pickle(f'{data_path}/{f}')
    # print(df.head(10))
    for n_stations in [1]:  # range(0, 7):
        for min_dist in [0]:  # range(0, 100, 10):
            options = {'n': n_stations, 'min_dist': min_dist, 'max_dist': max_dist}
            print(f'n_stations: {n_stations}, min_dist: {min_dist}, max_dist: {max_dist}')
            gradt, intercept, gradt_std, intercept_std = [], [], [], []
            pearson = []
            spearman = []
            spearman_p = []
            n_l = []

            for mag_lim in magnitudes:
                x, y = calc_tp_mag_lim(df, mag_lim, **options)
                gradt, intercept, gradt_std, intercept_std, pearson, spearman, spearman_p, n = calc_opt(x, y,
                                                                                                        gradt,
                                                                                                        intercept,
                                                                                                        gradt_std,
                                                                                                        intercept_std,
                                                                                                        pearson,
                                                                                                        spearman,
                                                                                                        spearman_p,
                                                                                                        n_l)
            tp_params = [gradt, gradt_std, np.array(pearson)**2, spearman, spearman_p, n, 'tp']
            if len(spearman) > 0:
                print('tp', spearman[0])

            gradt, intercept, gradt_std, intercept_std = [], [], [], []
            pearson = []
            spearman = []
            spearman_p = []
            n_l = []

            for mag_lim in magnitudes:
                x, y = calc_pgd_mag_lim(df, mag_lim, **options)
                gradt, intercept, gradt_std, intercept_std, pearson, spearman, spearman_p, n = calc_opt(x, y,
                                                                                                        gradt,
                                                                                                        intercept,
                                                                                                        gradt_std,
                                                                                                        intercept_std,
                                                                                                        pearson,
                                                                                                        spearman,
                                                                                                        spearman_p,
                                                                                                        n_l)
            pgd_params = [gradt, gradt_std, np.array(pearson)**2, spearman, spearman_p, n, 'pgd']
            if len(spearman) > 0:
                print('pgd', spearman[0])

            gradt, intercept, gradt_std, intercept_std = [], [], [], []
            pearson = []
            spearman = []
            spearman_p = []
            n_l = []

            for mag_lim in magnitudes:
                x, y = calc_tc_mag_lim(df, mag_lim, **options)
                gradt, intercept, gradt_std, intercept_std, pearson, spearman, spearman_p, n = calc_opt(x, y,
                                                                                                        gradt,
                                                                                                        intercept,
                                                                                                        gradt_std,
                                                                                                        intercept_std,
                                                                                                        pearson,
                                                                                                        spearman,
                                                                                                        spearman_p,
                                                                                                        n_l)
            tc_params = [gradt, gradt_std, np.array(pearson)**2, spearman, spearman_p, n, 'tc']
            if len(spearman) > 0:
                print('tc', spearman[0])

            gradt, intercept, gradt_std, intercept_std = [], [], [], []
            pearson = []
            spearman = []
            spearman_p = []
            n_l = []

            for mag_lim in magnitudes:
                x, y = calc_iv2_mag_lim(df, mag_lim, **options)
                gradt, intercept, gradt_std, intercept_std, pearson, spearman, spearman_p, n = calc_opt(x, y,
                                                                                                        gradt,
                                                                                                        intercept,
                                                                                                        gradt_std,
                                                                                                        intercept_std,
                                                                                                        pearson,
                                                                                                        spearman,
                                                                                                        spearman_p,
                                                                                                        n_l)

            iv2_params = [gradt, gradt_std, np.array(pearson)**2, spearman, spearman_p, n, 'iv2']
            if len(spearman) > 0:
                print('iv2', spearman[0])

            for scale in ['one', 'two', 'three', 'ten']:
                tp_df = fill_out_df(tp_df, tp_params, f, scale_size=scale)
                tc_df = fill_out_df(tc_df, tc_params, f, scale_size=scale)
                iv2_df = fill_out_df(iv2_df, iv2_params, f, scale_size=scale)
                pgd_df = fill_out_df(pgd_df, pgd_params, f, scale_size=scale)
                # fill_out_df([tp_params, tc_params, iv2_params, pgd_params])
print(tp_df)
print(tc_df)
print(iv2_df)
print(pgd_df)

for scale_size in ['one', 'two', 'three', 'ten']:
    gradt_hist_subplots([tp_df, tc_df, iv2_df, pgd_df], scale_size=scale_size)
