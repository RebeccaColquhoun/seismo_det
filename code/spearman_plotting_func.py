import scipy
import numpy as np
import matplotlib.pyplot as plt
import math
import figure_sizes
import matplotlib
matplotlib.rcParams.update({'font.size': 20})

magnitudes = np.arange(3, 7.1, 0.1)
colors = {'tp': '#7f58af', 'tc': '#e84d8a', 'iv2': '#64c5eb', 'pgd': '#7fb646'}
window_lengths = {'0.3': 4, '0.5': 4.4, '1': 5.02, '4': 6.22}
half_lengths = {'0.3': 4.6, '0.5': 5.04, '1': 5.65, '4': 6.85}
third_lengths = {'0.3': 4.95, '0.5': 5.4, '1': 6.0, '4': 7.2}
tenth_lengths = {'0.3': 6, '0.5': 6.45, '1': 7.05, '4': 7.95}


def sort_tp_data(df, mag_lim=0, n=0, min_dist=0, max_dist=1000):
    list_mag = []
    list_tpmax = []
    count = 0
    if type(mag_lim) in [int, float, np.float64]:
        min_mag_lim = mag_lim
        max_mag_lim = 10
    else:
        (min_mag_lim, max_mag_lim) = mag_lim
    for index, row in df.iterrows():
        if row.eq_mag > min_mag_lim and row.eq_mag < max_mag_lim and len(row.tp_max) >= n:
            list_mag.append(row.eq_mag)
            list_tpmax.append([])
            for d in range(0, len(row.tp_max)):
                if (row.tp_max[d] is not None
                        and row.tp_max[d] > 0
                        and row.distance_dict[row.tp_max_stations[d]] > min_dist
                        and row.distance_dict[row.tp_max_stations[d]] < max_dist):
                    list_tpmax[count].append(row.tp_max[d])
            count += 1
    return list_mag, list_tpmax


def sort_tc_data(df, mag_lim=0, n=0, min_dist=0, max_dist=1000):
    list_mag = []
    list_tc = []
    count = 0
    if type(mag_lim) in [int, float, np.float64]:
        min_mag_lim = mag_lim
        max_mag_lim = 10
    else:
        (min_mag_lim, max_mag_lim) = mag_lim
    for index, row in df.iterrows():
        if row.eq_mag > min_mag_lim and row.eq_mag < max_mag_lim and len(row.tc) >= n:
            list_mag.append(row.eq_mag)
            list_tc.append([])
            for d in range(0, len(row.tc)):
                if (row.tc[d] is not None
                        and row.tc[d] > 0
                        and row.distance_dict[row.tc_stations[d]] > min_dist
                        and row.distance_dict[row.tc_stations[d]] < max_dist):
                    list_tc[count].append(row.tc[d])
            count += 1
    return list_mag, list_tc


def sort_iv2_data(df, mag_lim=0, n=0, min_dist=0, max_dist=1000):
    list_iv2_all = list(df.iv2)
    list_mag_all = list(df.eq_mag)
    list_dist_Distance = list(df.iv2_distances)
    list_dist = []
    list_mag = []
    list_iv2 = []
    if type(mag_lim) in [int, float, np.float64]:
        min_mag_lim = mag_lim
        max_mag_lim = 10
    else:
        (min_mag_lim, max_mag_lim) = mag_lim
    for m in range(0, len(list_mag_all)):
        if list_mag_all[m] > min_mag_lim and list_mag_all[m] < max_mag_lim and len(list_iv2_all[m]) >= n:
            for d in range(0, len(list_dist_Distance[m])):
                if (list_iv2_all[m][d] is not None
                        and list_iv2_all[m][d] > 0
                        and list_dist_Distance[m][d] > min_dist
                        and list_dist_Distance[m][d] < max_dist):
                    list_mag.append(list_mag_all[m])
                    list_iv2.append(list_iv2_all[m][d])
                    list_dist.append(float(str(np.array(list_dist_Distance[m][d]))[:-3]))
    return list_mag, list_iv2, list_dist


def sort_pgd_data(df, mag_lim=0, n=0, min_dist=0, max_dist=1000):
    list_pgd_all = list(df.pgd)
    list_mag_all = list(df.eq_mag)
    list_dist_Distance = list(df.pgd_distances)
    list_dist = []
    list_mag = []
    list_pgd = []
    eq = 0
    if type(mag_lim) in [int, float, np.float64]:
        min_mag_lim = mag_lim
        max_mag_lim = 10
    else:
        (min_mag_lim, max_mag_lim) = mag_lim
    for m in range(0, len(list_mag_all)):
        if list_mag_all[m] > min_mag_lim and list_mag_all[m] < max_mag_lim and len(list_pgd_all[m]) >= n:
            someTrue = len(list_pgd_all[m])
            for d in range(0, len(list_dist_Distance[m])):
                if (list_pgd_all[m][d] is not None
                        and list_pgd_all[m][d] > 0
                        and list_dist_Distance[m][d] > min_dist
                        and list_dist_Distance[m][d] < max_dist):
                    list_mag.append(list_mag_all[m])
                    list_pgd.append(list_pgd_all[m][d])
                    list_dist.append(float(str(np.array(list_dist_Distance[m][d]))[:-3]))
                else:
                    someTrue -= 1
            if someTrue > 0:
                eq += 1
    return list_mag, list_pgd, list_dist


def calc_tp_mag_lim(df, mag_lim, n=0, min_dist=0, max_dist=1000):
    # print(mag_lim)
    list_mags, list_tpmax = sort_tp_data(df, mag_lim, n=n, min_dist=min_dist, max_dist=max_dist)
    y_aves_tp = []
    x_aves_tp = []
    i = 0
    for i in range(0, len(list_mags)):
        if len(list_tpmax[i]) >= 1:
            mean_tp = np.mean(list_tpmax[i])
            std_tp = np.std(list_tpmax[i])
            y_tp = []
            for j in list_tpmax[i]:
                if j > mean_tp - 2 * std_tp and j < mean_tp + 2 * std_tp:  # and j < 100:
                    y_tp.append(math.log(j, 10))
                elif len(list_tpmax[i]) == 1:
                    y_tp.append(math.log(j, 10))
            x_tp = np.zeros(len(y_tp))
            x_tp = x_tp + list_mags[i]
            if math.isnan(np.median(y_tp)) is False:
                y_aves_tp.append(np.median(y_tp))
                x_aves_tp.append(list_mags[i])
    return x_aves_tp, y_aves_tp


def calc_tc_mag_lim(df, mag_lim, n=0, min_dist=0, max_dist=1000):
    # print(mag_lim)
    list_mags, list_tc = sort_tc_data(df, mag_lim, n=n, min_dist=min_dist, max_dist=max_dist)
    y_aves_tc = []
    x_aves_tc = []
    i = 0
    for i in range(0, len(list_mags)):
        if len(list_tc[i]) >= 1:
            mean_tc = np.mean(list_tc[i])
            std_tc = np.std(list_tc[i])
            y_tc = []
            for j in list_tc[i]:
                if j > mean_tc - 2 * std_tc and j < mean_tc + 2 * std_tc:  # and j < 100:
                    y_tc.append(math.log(j, 10))
                elif len(list_tc[i]) == 1:
                    y_tc.append(math.log(j, 10))
            x_tc = np.zeros(len(y_tc))
            x_tc = x_tc + list_mags[i]
            if math.isnan(np.median(y_tc)) is False:
                y_aves_tc.append(np.median(y_tc))
                x_aves_tc.append(list_mags[i])
    return x_aves_tc, y_aves_tc


def calc_pgd_mag_lim(df, mag_lim, n=0, min_dist=0, max_dist=1000):
    list_mag, list_pgd, list_dist = sort_pgd_data(df, mag_lim, n=n, min_dist=min_dist, max_dist=max_dist)
    if len(list_mag) > 1 and len(list_dist) > 1 and len(list_pgd) > 1:
        dist_corr_mult_alt = (np.array(list_dist) ** 1.38) * np.array(list_pgd)
        y = np.log10(dist_corr_mult_alt)
        x = np.array(list_mag)
        mask = ~np.isnan(x) & ~np.isnan(y)
        return x[mask], y[mask]
    else:
        return [], []


def calc_iv2_mag_lim(df, mag_lim, r_corr='2', n=0, min_dist=0, max_dist=1000):
    list_mag, list_iv2, list_dist = sort_iv2_data(df, mag_lim, n=n, min_dist=min_dist, max_dist=max_dist)
    if len(list_mag) > 1 and len(list_dist) > 1 and len(list_iv2) > 1:
        r_corr = float(r_corr)
        dist_corr_mult = (np.array(list_dist) ** r_corr) * np.array(list_iv2)
        y = np.log10(dist_corr_mult)
        x = np.array(list_mag)
        mask = ~np.isnan(x) & ~np.isnan(y)
        return x[mask], y[mask]
    else:
        return [], []


def calc_opt(x, y, gradt, intercept, gradt_std, intercept_std, pearson, spearman, spearman_p, n_l):
    if len(y) > 0:
        x_use = np.array(x) - 5
        y_use = np.array(y)

        x = x_use
        y = y_use

        if len(set(x)) > 1:
            result = scipy.stats.linregress(x, y)
            a = result.slope
            gradt.append(a)
            b = result.intercept
            intercept.append(b)
            std_a = result.stderr
            gradt_std.append(std_a)
            std_b = result.intercept_stderr
            intercept_std.append(std_b)
            # plt.scatter(x,y)
            # x_plot = np.array([-2,3])
            # plt.plot(x_plot,a*x_plot+b)
            pearson.append(result.rvalue)
            spearman.append(scipy.stats.spearmanr(x, y)[0])
            spearman_p.append(scipy.stats.spearmanr(x, y)[1])
            n_l.append(len(x))
    return gradt, intercept, gradt_std, intercept_std, pearson, spearman, spearman_p, n_l


def name_to_time(f):
    split_underscore = f.split('_')
    time = split_underscore[2][:-1]
    if time == '1' or time == '4':
        return time
    else:
        time = time[0] + '.' + time[1]
        return time


def name_to_snr(f):
    split_underscore = f.split('_')
    snr = split_underscore[-1]
    if snr[0:3] == 'snr':
        return snr[3:]


def name_to_blank(f):
    split_underscore = f.split('_')
    blank = split_underscore[9]
    return blank


def plot_spearman_subplots(f, gradt, gradt_std, spearman, spearman_p,
                           var='tp', save=False, min_dist=0, max_dist=200, n=0):
    matplotlib.rcParams.update({'font.size': 20})
    time = name_to_time(f)
    snr = name_to_snr(f)
    fig, axs = plt.subplots(5, 1, figsize=figure_sizes.a4portrait, sharex=True)
    magn = magnitudes[0:len(spearman)]
    axs[0].plot(magn, gradt, color=colors[var])
    axs[0].set_ylabel('gradient')
    axs[1].plot(magn, gradt_std, color=colors[var])
    axs[1].set_ylabel('gradient std')
    axs[2].plot(magn, spearman, color=colors[var])
    axs[2].set_ylabel('spearman r')
    axs[3].plot(magn, spearman_p, color=colors[var])
    mask = np.array(spearman_p) > 0.05
    mag_mask = magn[mask]
    axs[3].plot(mag_mask, np.array(spearman_p)[mask], color=colors[var], linestyle='', marker='o')
    axs[3].set_ylabel('p-value of\n  spearman \n (H0=linearly \n uncorrelated)')
    axs[3].axhspan(0, 0.05, facecolor=colors[var], alpha=0.2)
    axs[4].plot(magn, np.array(n), color=colors[var])
    axs[4].set_ylabel('n')
    axs[0].set_title(f'log$_{10}$({var}) - {time} s window')
    axs[4].set_xlabel('max mag')
    axs[3].set_xlim([3, 7])
    axs[0].grid(True)
    axs[1].grid(True)
    axs[2].grid(True)
    axs[3].grid(True)
    axs[4].grid(True)
    if save is True:
        plt.savefig(f'''/home/earthquakes1/homes/Rebecca/phd/seismo_det/figures/gradt_spearman/
                    {var}_with_number_window_{time}_snr{snr}_n{n}_dist{min_dist}_{max_dist}.pdf''', dpi=400)
    plt.show()


def plot_spearman_subplots_all_on_one(f, tp_params, pgd_params, iv2_params, tc_params,
                                      save=False, min_dist=0, max_dist=200, n=0):
    params = [tp_params, pgd_params, iv2_params, tc_params]
    # [gradt, gradt_std, spearman, spearman_p, n, var]
    time = name_to_time(f)
    snr = name_to_snr(f)
    blank = name_to_blank(f)
    fig, axs = plt.subplots(5, 1, figsize=figure_sizes.a5landscape, sharex=True)
    axs[0].plot([], [], color='k', label='significant')
    axs[0].plot([], [], color='k', linestyle=':', label='insignificant')

    for p in params:
        magn = magnitudes[0:len(p[2])]
        res = [idx for idx, val in enumerate(p[3]) if val > 0.05]
        if len(res) > 0:
            flip = res[0]
            mag_mask = magn[(flip - 1):]
            mag_neg_mask = magn[:flip]
            for i in range(0, 5):
                axs[i].plot(mag_mask, np.array(p[i])[(flip - 1):], color=colors[p[5]], linestyle=':')
                axs[i].plot(mag_neg_mask, np.array(p[i])[:flip], color=colors[p[5]], label=p[-1])
        else:
            for i in range(0, 5):
                axs[i].plot(magn, p[i], color=colors[p[5]])

        axs[3].axhspan(0, 0.05, facecolor='grey', alpha=0.2)
    for ax in axs:
        ax.vlines(window_lengths[str(time)], 0, 1, transform=ax.get_xaxis_transform(), color='grey', linewidth=1.5)

    axs[0].set_ylabel('gradient')
    axs[1].set_ylabel('gradient std')
    axs[2].set_ylabel('spearman r')
    axs[3].set_ylabel('p-value of\n  spearman \n (H0=linearly \n uncorrelated)')
    axs[4].set_ylabel('n')
    axs[0].set_title(f'{time} s window')
    axs[4].set_xlabel('max mag')
    axs[3].set_xlim([3, 7])
    axs[0].grid(True)
    axs[1].grid(True)
    axs[2].grid(True)
    axs[3].grid(True)
    axs[4].grid(True)
    axs[0].autoscale(True, 'y')
    axs[1].autoscale(True, 'y')
    axs[2].autoscale(True, 'y')
    axs[3].autoscale(True, 'y')
    axs[4].autoscale(True, 'y')
    handles, labels = axs[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', ncol=len(labels))
    figure = plt.gcf()
    figure.set_size_inches(figure_sizes.a5landscape)
    if save is True:
        plt.savefig(f'''/home/earthquakes1/homes/Rebecca/phd/seismo_det/figures/gradt_spearman/
                    combined_with_number_window_{time}_snr{snr}_blank_{blank}_n{n}_dist{min_dist}_{max_dist}.pdf''',
                    dpi=400)
    plt.show()


def plot_spearman_subplots_all_on_one_no_n(f, tp_params, pgd_params, iv2_params, tc_params,
                                           save=False, min_dist=0, max_dist=200, n=0):
    params = [tp_params, pgd_params, iv2_params, tc_params]
    # [gradt, gradt_std, spearman, spearman_p, n, var]
    time = name_to_time(f)
    snr = name_to_snr(f)
    blank = name_to_blank(f)
    fig, axs = plt.subplots(4, 1, figsize=figure_sizes.a5landscape, sharex=True)
    axs[0].plot([], [], color='k', label='significant')
    axs[0].plot([], [], color='k', linestyle=':', label='insignificant')
    for p in params:
        magn = magnitudes[0:len(p[2])]
        res = [idx for idx, val in enumerate(p[3]) if val > 0.05]
        if len(res) > 0:
            flip = res[0]
            mag_mask = magn[(flip - 1):]
            mag_neg_mask = magn[:flip]
            for i in range(0, 4):
                axs[i].plot(mag_mask, np.array(p[i])[(flip - 1):], color=colors[p[5]], linestyle=':', linewidth=2)
                axs[i].plot(mag_neg_mask, np.array(p[i])[:flip], color=colors[p[5]], label=p[-1], linewidth=2)
        else:
            for i in range(0, 4):
                axs[i].plot(magn, p[i], color=colors[p[5]], linewidth=2)

        axs[3].axhspan(0, 0.05, facecolor='grey', alpha=0.2)
    for ax in axs:
        ax.vlines(window_lengths[str(time)], 0, 1, transform=ax.get_xaxis_transform(), color='grey', linewidth=1.5)

    axs[0].set_ylabel('gradient')
    axs[1].set_ylabel('gradient std')
    axs[2].set_ylabel('spearman r')
    axs[3].set_ylabel('p-value of\n  spearman \n (H0=linearly \n uncorrelated)')
    # axs[4].set_ylabel('n')
    axs[0].set_title(f'{time} s window')
    axs[3].set_xlabel('max mag')
    axs[3].set_xlim([3, 7])
    axs[0].grid(True)
    axs[1].grid(True)
    axs[2].grid(True)
    axs[3].grid(True)
    axs[0].autoscale(True, 'y')
    axs[1].autoscale(True, 'y')
    axs[2].autoscale(True, 'y')
    axs[3].autoscale(True, 'y')
    handles, labels = axs[0].get_legend_handles_labels()
    figure = plt.gcf()
    figure.set_size_inches(figure_sizes.a4portrait)
    fig.legend(handles, labels, loc='lower center', ncol=len(labels),
               bbox_to_anchor=(0.03, -0.03, 1, 1), bbox_transform=figure.transFigure)
    figure.tight_layout()
    if save is True:
        plt.savefig(f'''/home/earthquakes1/homes/Rebecca/phd/seismo_det/figures/gradt_spearman/
                    combined_no_number_window_{time}_snr{snr}_blank_{blank}_n{n}_dist{min_dist}_{max_dist}.pdf''',
                    dpi=400, bbox_inches='tight')
    plt.show()


def plot_spearman_subplots_all_on_one_no_n_shaded(f, tp_params, pgd_params, iv2_params, tc_params,
                                                  log=False, save=False, min_dist=0, max_dist=200, n=0):
    params = [tp_params, pgd_params, iv2_params, tc_params]
    #  [gradt, gradt_std, spearman, spearman_p, n, var]
    time = name_to_time(f)
    snr = name_to_snr(f)
    blank = name_to_blank(f)
    fig, axs = plt.subplots(3, 1, figsize=figure_sizes.a4square, sharex=True, height_ratios=[2, 1, 1])
    axs[0].plot([], [], color='k', label='significant')
    axs[0].plot([], [], color='k', linestyle=':', label='insignificant')
    # axs[0].fill_between([],[], [],color='k',alpha = 0.3, label = '1 s.d.')
    for p in params:
        magn = magnitudes[0:len(p[2])]
        res = [idx for idx, val in enumerate(p[3]) if val > 0.05]
        if len(res) > 0:
            flip = res[0]
            mag_mask = magn[(flip - 1):]
            mag_neg_mask = magn[:flip]
            for i in range(0, 4):
                if i == 0:
                    print('i=0')
                    axs[i].plot(mag_mask, np.array(p[i])[(flip - 1):], color=colors[p[5]], linestyle=':', linewidth=2)
                    axs[i].plot(mag_neg_mask, np.array(p[i])[:flip], color=colors[p[5]], label=p[-1], linewidth=2)
                elif i == 1:
                    print('i=1')
                    axs[0].fill_between(magn, np.array(p[1]) + np.array(p[0]), np.array(p[0]) - np.array(p[1]),
                                        color=colors[p[5]], alpha=0.3)
                    # axs[1].plot(mag_neg_mask,np.array(p[i])[:flip], color = colors[p[5]], label = p[-1], linewidth=2)
                else:
                    print('in else')
                    axs[i - 1].plot(mag_mask, np.array(p[i])[(flip - 1):],
                                    color=colors[p[5]], linestyle=':', linewidth=2)
                    axs[i - 1].plot(mag_neg_mask, np.array(p[i])[:flip], color=colors[p[5]], label=p[-1], linewidth=2)
        else:
            for i in [0, 2, 3]:
                if i == 0:
                    axs[i].plot(magn, p[i], color=colors[p[5]], linewidth=2)
                elif i == 1:
                    axs[0].fill_between(magn, np.array(p[1]) + np.array(p[0]), np.array(p[0]) - np.array(p[1]),
                                        color=colors[p[5]], alpha=0.3)
                    # axs[1].plot(mag_neg_mask,np.array(p[i])[:flip], color = colors[p[5]], label = p[-1], linewidth=2)
                else:
                    axs[i - 1].plot(magn, p[i], color=colors[p[5]], linewidth=2)

        axs[2].axhspan(0, 0.05, facecolor='grey', alpha=0.05)
    for ax in axs:
        ax.vlines(window_lengths[str(time)], 0, 1, transform=ax.get_xaxis_transform(), color='grey', linewidth=1.5)
        ax.tick_params(axis='both', which='major', labelsize=14)
        # ax.tick_params(axis='both', which='minor', labelsize=8)
    axs[0].set_ylabel('Gradient', fontsize=14)
    axs[1].set_ylabel('Spearman r', fontsize=14)
    axs[2].set_ylabel('p-value of\n  spearman r', fontsize=14)
    # axs[4].set_ylabel('n')
    axs[0].set_title(f'{time} s Window', fontsize=14)
    axs[2].set_xlabel('Min mag', fontsize=14)
    axs[2].set_xlim([3, 7])
    axs[0].grid(True)
    axs[1].grid(True)
    axs[2].grid(True)
    axs[0].autoscale(True, 'y')
    axs[1].autoscale(True, 'y')
    axs[2].autoscale(True, 'y')
    matplotlib.rcParams.update({'font.size': 14})
    import matplotlib.transforms as mtransforms
    trans = mtransforms.ScaledTranslation(-20 / 72, 7 / 72, fig.dpi_scale_trans)
    axs[0].text(0.0, 1.0, 'a)', transform=axs[0].transAxes + trans,
                fontsize='14', va='bottom')
    axs[1].text(0.0, 1.0, 'b)', transform=axs[1].transAxes + trans,
                fontsize='14', va='bottom')
    axs[2].text(0.0, 1.0, 'c)', transform=axs[2].transAxes + trans,
                fontsize='14', va='bottom')
    if log is True:
        axs[2].set_yscale('log')
    handles, labels = axs[0].get_legend_handles_labels()
    figure = plt.gcf()
    figure.set_size_inches(figure_sizes.a4square)
    fig.legend(handles, labels, loc='lower center', ncol=3,
               bbox_to_anchor=(0.03, -0.1, 1, 1), bbox_transform=figure.transFigure)
    figure.tight_layout()
    if save is True:
        if log is True:
            plt.savefig(f'''/home/earthquakes1/homes/Rebecca/phd/seismo_det/figures/gradt_spearman/
                        shaded_combined_no_number_window_{time}_blankwindow_{blank}_
                        snr{snr}_n{n}_dist{min_dist}_{max_dist}_log.pdf''',
                        dpi=400, bbox_inches='tight')
        else:
            plt.savefig(f'''/home/earthquakes1/homes/Rebecca/phd/seismo_det/figures/gradt_spearman/
                        shaded_combined_no_number_window_{time}_blankwindow_{blank}
                        _snr{snr}_n{n}_dist{min_dist}_{max_dist}.pdf''',
                        dpi=400, bbox_inches='tight')
    plt.show()


def plot_spearman_subplots_all_on_one_no_n_shaded_percent_var(f,
                                                              tp_params, pgd_params, iv2_params, tc_params,
                                                              log=False, save=False, g_r=False,
                                                              min_dist=0, max_dist=200,
                                                              n=0):
    params = [tp_params, pgd_params, iv2_params, tc_params]
    # [gradt, gradt_std, pearson, spearman, spearman_p, n, var]
    time = name_to_time(f)
    snr = name_to_snr(f)
    blank = name_to_blank(f)
    fig, axs = plt.subplots(4, 1, figsize=figure_sizes.a4square, sharex=True, height_ratios=[2, 1, 1, 1])
    axs[0].plot([], [], color='k', label='significant')
    axs[0].plot([], [], color='k', linestyle=':', label='insignificant')
    axs[0].plot([], [], color=colors['tp'], label=r'$\tau_{P}^{\max}$')
    axs[0].plot([], [], color=colors['tc'], label=r'$\tau_{C}$')
    axs[0].plot([], [], color=colors['iv2'], label='IV2')
    axs[0].plot([], [], color=colors['pgd'], label=r'$P_D$')
    # axs[0].fill_between([],[], [],color='k',alpha = 0.3, label = '1 s.d.')
    for p in params:
        magn = magnitudes[0:len(p[2])]
        res = [idx for idx, val in enumerate(p[4]) if val > 0.05]
        # print(p[0])
        # print(res)
        # print(magn)
        # print(p)
        if len(magn) == 0:
            for ax in axs:
                ax.plot([], [], color=colors[p[6]], linewidth=2, label=p[-1])
        elif res == []:
            print('in if, len(res)==0')
            for i in [0, 2, 3, 4]:
                if i == 0:
                    # print('else, i=0')
                    # print(p[i],p[5])
                    axs[i].plot(magn, np.array(p[i]), color=colors[p[6]], linewidth=2, label=p[-1])
                    ax2 = axs[i].twinx()
                elif i == 1:
                    # print('else, i=1')
                    axs[0].fill_between(magn, np.array(p[1]) + np.array(p[0]), np.array(p[0]) - np.array(p[1]),
                                        color=colors[p[6]], alpha=0.3)
                    # axs[1].plot(mag_neg_mask,np.array(p[i])[:flip], color = colors[p[5]], label = p[-1], linewidth=2)
                else:
                    # print('else, i=else')
                    axs[i - 1].plot(magn, np.array(p[i]), color=colors[p[5]], linewidth=2)
        elif res[0] == 0:
            print('in elif, res[0]==0')
            mag_mask = magn[0:]
            mag_neg_mask = magn[:0]
            for i in range(0, 5):
                if i == 0:
                    # print(' i=0')
                    # print(p[i],p[5])
                    axs[i].plot(magn, np.array(p[i]), color=colors[p[6]], linewidth=2, linestyle=':')
                elif i == 1:
                    # print(' i=1')
                    axs[0].fill_between(magn, np.array(p[1]) + np.array(p[0]), np.array(p[0]) - np.array(p[1]),
                                        color=colors[p[6]], alpha=0.3, linestyle=':')
                    # axs[1].plot(mag_neg_mask,np.array(p[i])[:flip], color = colors[p[5]], label = p[-1], linewidth=2)
                else:
                    # print('i=else')
                    axs[i - 1].plot(magn, np.array(p[i]), color=colors[p[6]], linewidth=2, linestyle=':')
        else:  # elif len(res) > 0:
            print('in else, len(res)>0')
            flip = res[0]
            if flip != 0:
                mag_mask = magn[(flip - 1):]
                mag_neg_mask = magn[:flip]
            for i in range(0, 5):
                if i == 0:
                    # print('i=0')
                    axs[i].plot(mag_mask, np.array(p[i])[(flip - 1):],
                                color=colors[p[6]], linestyle=':', linewidth=2)
                    axs[i].plot(mag_neg_mask, np.array(p[i])[:flip], color=colors[p[6]], linewidth=2)#, label=p[-1])
                elif i == 1:
                    # print('i=1')
                    axs[0].fill_between(magn, np.array(p[0]) + np.array(p[1]), np.array(p[0]) - np.array(p[1]),
                                        color=colors[p[6]], alpha=0.3)
                    axs[0].fill_between(magn, np.array(p[0]) + 2 * np.array(p[1]), np.array(p[0]) - 2 * np.array(p[1]),
                                        color=colors[p[6]], alpha=0.15)
                    # axs[1].plot(mag_neg_mask,np.array(p[i])[:flip], color = colors[p[5]], label = p[-1], linewidth=2)
                else:
                    # print('in else')
                    axs[i - 1].plot(mag_mask, np.array(p[i])[(flip - 1):],
                                    color=colors[p[6]], linestyle=':', linewidth=2)
                    axs[i - 1].plot(mag_neg_mask, np.array(p[i])[:flip],
                                    color=colors[p[6]], linewidth=2) #, label=p[-1]

        axs[3].axhspan(0, 0.05, facecolor='grey', alpha=0.05)
    for ax in axs:
        ax.vlines(window_lengths[str(time)], 0, 1, transform=ax.get_xaxis_transform(),
                  color='grey', linewidth=1.5)
        ax.vlines(third_lengths[str(time)], 0, 1, transform=ax.get_xaxis_transform(),
                  color='grey', linewidth=1.5, linestyle='-.')
        ax.vlines(half_lengths[str(time)], 0, 1, transform=ax.get_xaxis_transform(),
                  color='grey', linewidth=1.5, linestyle='dashed')
        ax.vlines(tenth_lengths[str(time)], 0, 1, transform=ax.get_xaxis_transform(),
                  color='grey', linewidth=1.5, linestyle='dotted')
        ax.tick_params(axis='both', which='major', labelsize=14)
        # ax.tick_params(axis='both', which='minor', labelsize=8)
    axs[0].set_ylabel('Gradient', fontsize=14)
    axs[1].set_ylabel('Variance \n explained', fontsize=14)
    axs[2].set_ylabel("Spearman's r", fontsize=14)
    axs[3].set_ylabel("p-value of\n  Spearman's r", fontsize=14)
    # axs[4].set_ylabel('n')
    # axs[0].set_title(f'{time} s Window, snr = {snr}, n >= {n}, distances = {min_dist}--{max_dist} km', fontsize=14)
    axs[3].set_xlabel('Minimum magnitude considered', fontsize=14)
    axs[3].set_xlim([3, 7])
    axs[0].grid(True)
    axs[1].grid(True)
    axs[2].grid(True)
    axs[3].grid(True)
    axs[0].autoscale(True, 'y')
    axs[1].autoscale(True, 'y')
    axs[2].autoscale(True, 'y')
    matplotlib.rcParams.update({'font.size': 14})
    import matplotlib.transforms as mtransforms
    trans = mtransforms.ScaledTranslation(-20 / 72, 7 / 72, fig.dpi_scale_trans)
    axs[0].text(0.0, 1.0, 'a)', transform=axs[0].transAxes + trans,
                fontsize='14', va='bottom')
    axs[1].text(0.0, 1.0, 'b)', transform=axs[1].transAxes + trans,
                fontsize='14', va='bottom')
    axs[2].text(0.0, 1.0, 'c)', transform=axs[2].transAxes + trans,
                fontsize='14', va='bottom')
    axs[3].text(0.0, 1.0, 'd)', transform=axs[3].transAxes + trans,
                fontsize='14', va='bottom')
    if log is True:
        axs[3].set_yscale('log')
    handles, labels = axs[0].get_legend_handles_labels()
    figure = plt.gcf()
    figure.set_size_inches(figure_sizes.a4square)
    fig.legend(handles, labels, loc='lower center', ncol=3,
               bbox_to_anchor=(0.03, -0.1, 1, 1), bbox_transform=figure.transFigure)
    figure.tight_layout()
    if save is True:
        if log is True:
            plt.savefig(f'/home/earthquakes1/homes/Rebecca/phd/seismo_det/figures/final/gradt_spearman/shaded_combined_no_number_window_{time}_blankwindow_{blank}_snr{snr}_n{n}_dist{min_dist}_{max_dist}_log_var_durations.pdf',
                        dpi=400, bbox_inches='tight')
        elif g_r is True:
            plt.savefig(f'/home/earthquakes1/homes/Rebecca/phd/seismo_det/figures/final/gradt_spearman/shaded_combined_no_number_window_{time}_blankwindow_{blank}_snr{snr}_n{n}_dist{min_dist}_{max_dist}_gr_var_durations.pdf',
                        dpi=400, bbox_inches='tight')
        else:
            plt.savefig(f'/home/earthquakes1/homes/Rebecca/phd/seismo_det/figures/final/gradt_spearman/shaded_combined_no_number_window_{time}_blankwindow_{blank}_snr{snr}_n{n}_dist{min_dist}_{max_dist}_var_durations.pdf''',
                        dpi=400, bbox_inches='tight')
    #plt.show()
