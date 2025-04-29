import scipy
import numpy as np
import matplotlib.pyplot as plt
import math
import figure_sizes
import matplotlib
import setup_paths as paths

matplotlib.rcParams.update({'font.size': 12})


magnitudes = np.arange(3, 7.1, 0.1)
colors = {'tp': '#7f58af', 'tc': '#e84d8a', 'iv2': '#64c5eb', 'pgd': '#7fb646'}

window_lengths = {'0.3': 4, '0.5': 4.4, '1': 5.02, '4': 6.22}

labels = {'tp': r'$\tau_p^{\max}$, s',
          'tc': r'$\tau_c$, s',
          'pgd': r'$P_d$, m',
          'iv2': r'$IV2$, m$^2$s$^2$'}


def sort_tp_data_az(df, mag_lim=0, n=0, min_dist=0, max_dist=1000):
    list_mag = []
    list_tpmax = []
    list_n_stations = []
    list_azimuths = []
    list_distances = []
    list_ids = []
    count = 0
    # print(mag_lim, type(mag_lim))
    if type(mag_lim) in [int, float, np.float64]:
        min_mag_lim = mag_lim
        max_mag_lim = 10
    else:
        (min_mag_lim, max_mag_lim) = mag_lim
    for index, row in df.iterrows():
        if (row.eq_mag > min_mag_lim
                and row.eq_mag < max_mag_lim
                and len(row.tp_max) >= n):
            list_mag.append(row.eq_mag)
            list_tpmax.append([])
            list_n_stations.append([])
            list_azimuths.append([])
            list_distances.append([])
            list_ids.append([])
            for d in range(0, len(row.tp_max)):
                if (row.tp_max[d] is not None
                        and row.tp_max[d] > 0
                        and row.distance_dict[row.tp_max_stations[d]] > min_dist
                        and row.distance_dict[row.tp_max_stations[d]] < max_dist):
                    list_tpmax[count].append(row.tp_max[d])
                    list_n_stations[count].append(row.tp_max_stations[d])
                    list_azimuths[count].append(row.azimuth_dict[row.tp_max_stations[d]])
                    #if index < 10:
                    #print(count)
                    #print(row.azimuth_dict[row.tp_max_stations[d]])
                    #print(list_azimuths)
                    list_distances[count].append(row.distance_dict[row.tp_max_stations[d]])
                    list_ids[count].append(row.eq_id)

            count += 1
    return list_mag, list_tpmax, list_n_stations, list_azimuths, list_distances, list_ids



def sort_tc_data_az(df, mag_lim=0, n=0, min_dist=0, max_dist=1000):
    list_mag = []
    list_tc = []
    list_n_stations = []
    list_azimuths = []
    list_distances = []
    list_ids = []
    count = 0
    if type(mag_lim) in [int, float, np.float64]:
        min_mag_lim = mag_lim
        max_mag_lim = 10
    else:
        (min_mag_lim, max_mag_lim) = mag_lim
    for index, row in df.iterrows():
        if (row.eq_mag > min_mag_lim
                and row.eq_mag < max_mag_lim
                and len(row.tc) >= n):
            list_mag.append(row.eq_mag)
            list_tc.append([])
            list_n_stations.append([])
            list_azimuths.append([])
            list_distances.append([])
            list_ids.append([])
            for d in range(0, len(row.tc)):
                if (row.tc[d] is not None
                    and row.tc[d] > 0
                    and row.distance_dict[row.tc_stations[d]] > min_dist
                        and row.distance_dict[row.tc_stations[d]] < max_dist):
                    list_tc[count].append(row.tc[d])
                    list_n_stations[count].append(row.tc_stations[d])
                    list_azimuths[count].append(row.azimuth_dict[row.tc_stations[d]])
                    list_distances[count].append(row.distance_dict[row.tc_stations[d]])
                    list_ids[count].append(row.eq_id)
            count += 1
    return list_mag, list_tc, list_n_stations, list_azimuths, list_distances, list_ids


def sort_iv2_data_az(df, mag_lim=0, n=0, min_dist=0, max_dist=1000):
    list_mag = []
    list_iv2 = []
    list_n_stations = []
    list_azimuths = []
    list_distances = []
    list_ids = []
    count = 0
    if type(mag_lim) in [int, float, np.float64]:
        min_mag_lim = mag_lim
        max_mag_lim = 10
    else:
        (min_mag_lim, max_mag_lim) = mag_lim

    for index, row in df.iterrows():
        if (row.eq_mag > min_mag_lim
                and row.eq_mag < max_mag_lim
                and len(row.iv2) >= n):
            list_mag.append(row.eq_mag)
            list_iv2.append([])
            list_n_stations.append([])
            list_azimuths.append([])
            list_distances.append([])
            list_ids.append([])
            for d in range(0, len(row.iv2)):
                if (row.iv2[d] is not None
                        and row.iv2[d] > 0
                        and row.distance_dict[row.iv2_stations[d]] > min_dist
                        and row.distance_dict[row.iv2_stations[d]] < max_dist):
                    list_iv2[count].append(row.iv2[d])
                    list_n_stations[count].append(row.iv2_stations[d])
                    list_azimuths[count].append(row.azimuth_dict[row.iv2_stations[d]])
                    list_distances[count].append(row.distance_dict[row.iv2_stations[d]])
                    list_ids[count].append(row.eq_id)
            count += 1

    return list_mag, list_iv2, list_n_stations, list_azimuths, list_distances, list_ids


def sort_pgd_data(df, mag_lim=0, n=0, min_dist=0, max_dist=1000):
    list_mag = []
    list_pgd = []
    list_n_stations = []
    list_azimuths = []
    list_distances = []
    list_ids = []

    count = 0
    if type(mag_lim) in [int, float, np.float64]:
        min_mag_lim = mag_lim
        max_mag_lim = 10
    else:
        (min_mag_lim, max_mag_lim) = mag_lim
    for index, row in df.iterrows():
        if (row.eq_mag > min_mag_lim
                and row.eq_mag < max_mag_lim
                and len(row.pgd) >= n):
            list_mag.append(row.eq_mag)
            list_pgd.append([])
            list_n_stations.append([])
            list_azimuths.append([])
            list_distances.append([])
            list_ids.append([])
            for d in range(0, len(row.pgd)):
                if (row.pgd[d] is not None
                    and row.pgd[d] > 0
                    and row.distance_dict[row.pgd_stations[d]] > min_dist
                        and row.distance_dict[row.pgd_stations[d]] < max_dist):
                    list_pgd[count].append(row.pgd[d])
                    list_n_stations[count].append(row.tp_max_stations[d])
                    list_azimuths[count].append(row.azimuth_dict[row.tp_max_stations[d]])
                    list_distances[count].append(row.distance_dict[row.tp_max_stations[d]])
                    list_ids[count].append(row.eq_id)

            count += 1
    return list_mag, list_pgd, list_n_stations, list_azimuths, list_distances, list_ids


def calc_tp_mag_lim_az(df, mag_lim, n=0, min_dist=0, max_dist=1000):
    # print(mag_lim)
    list_mags, list_tpmax, list_n_stations, list_azimuths, list_distances, list_ids = sort_tp_data_az(
        df, mag_lim, n=n, min_dist=min_dist, max_dist=max_dist)
    y_aves_tp = []
    x_aves_tp = []
    n_stations_tp = []
    azimuths_tp = []
    distances_tp = []
    ids_tp = []
    x_tp_all = []
    y_tp_all = []
    i = 0
    for i in range(0, len(list_mags)):
        azimuths_tp.append([])
        distances_tp.append([])
        ids_tp.append([])
        if len(list_tpmax[i]) >= 1:
            mean_tp = np.mean(list_tpmax[i])
            std_tp = np.std(list_tpmax[i])
            y_tp = []
            for count, j in enumerate(list_tpmax[i]):
                if (j > mean_tp - 2 * std_tp
                        and j < mean_tp + 2 * std_tp):  # and j < 100:
                    y_tp.append(math.log(j, 10))
                    #print(list_azimuths[i])
                    azimuths_tp[i].append(list_azimuths[i][count])
                    distances_tp[i].append(list_distances[i][count])
                    # print(list_ids[count])
                    # print(ids_tp)
                    # print(i, count)
                    ids_tp[i].append(list_ids[i][count])
                elif len(list_tpmax[i]) == 1:
                    y_tp.append(math.log(j, 10))
                    azimuths_tp[i].append(list_azimuths[i][count])
                    distances_tp[i].append(list_distances[i][count])
                    # print(list_ids[count])
                    # print(ids_tp[i])
                    # print(i, count)
                    ids_tp[i].append(list_ids[i][count])
            x_tp = np.zeros(len(y_tp))
            x_tp = x_tp + list_mags[i]
            if math.isnan(np.median(y_tp)) is False:
                y_aves_tp.append(np.median(y_tp))
                x_aves_tp.append(list_mags[i])
                y_tp_all.append(y_tp)
                x_tp_all.append(x_tp)
                n_stations_tp.append(list_n_stations[i])
            else:
                azimuths_tp[i] = []
                distances_tp[i] = []
                ids_tp[i] = []

    return x_aves_tp, y_aves_tp, n_stations_tp, azimuths_tp, distances_tp, ids_tp, x_tp_all, y_tp_all



def calc_tc_mag_lim_az(df, mag_lim, n=0, min_dist=0, max_dist=1000):
	# print(mag_lim)
	list_mags, list_tc, list_n_stations, list_azimuths, list_distances, list_ids = sort_tc_data_az(
		df, mag_lim, n=n, min_dist=min_dist, max_dist=max_dist)
	y_aves_tc = []
	x_aves_tc = []
	n_stations_tc = []
	azimuths_tc = []
	distances_tc = []
	ids_tc = []
	x_tc_all = []
	y_tc_all = []
	i = 0
	for i in range(0, len(list_mags)):
		azimuths_tc.append([])
		distances_tc.append([])
		ids_tc.append([])
		if len(list_tc[i]) >= 1:
			mean_tc = np.mean(list_tc[i])
			std_tc = np.std(list_tc[i])
			y_tc = []
			for count, j in enumerate(list_tc[i]):
				if (j > mean_tc - 2 * std_tc
						and j < mean_tc + 2 * std_tc):  # and j < 100:
					y_tc.append(math.log(j, 10))
					#print(list_azimuths[i])
					azimuths_tc[i].append(list_azimuths[i][count])
					distances_tc[i].append(list_distances[i][count])
					# print(list_ids[count])
					# print(ids_tp)
					# print(i, count)
					ids_tc[i].append(list_ids[i][count])
				elif len(list_tc[i]) == 1:
					y_tc.append(math.log(j, 10))
					azimuths_tc[i].append(list_azimuths[i][count])
					distances_tc[i].append(list_distances[i][count])
					# print(list_ids[count])
					# print(ids_tp[i])
					# print(i, count)
					ids_tc[i].append(list_ids[i][count])
			x_tc = np.zeros(len(y_tc))
			x_tc = x_tc + list_mags[i]
			if math.isnan(np.median(y_tc)) is False:
				y_aves_tc.append(np.median(y_tc))
				x_aves_tc.append(list_mags[i])
				y_tc_all.append(y_tc)
				x_tc_all.append(x_tc)
				n_stations_tc.append(list_n_stations[i])
			else:
				azimuths_tc[i] = []
				distances_tc[i] = []
				ids_tc[i] = []

	return x_aves_tc, y_aves_tc, n_stations_tc, azimuths_tc, distances_tc, ids_tc, x_tc_all, y_tc_all



def calc_pgd_mag_lim_az(df, mag_lim, n=0, min_dist=0, max_dist=1000):
    list_mag, list_pgd, list_n_stations, list_azimuths, list_distances, list_ids = sort_pgd_data(
        df, mag_lim, n=n, min_dist=min_dist, max_dist=max_dist)
    pgd_corrected = []
    mags_with_data = []
    #print(list_mag[0:10])
    for i, pgd_for_event in enumerate(list_pgd):
        distances_event = list_distances[i]
        mag_event = list_mag[i]
        #print(mag_event)
        #print(pgd_for_event)
        dist_corr_mult_alt = (np.array(distances_event) ** 1.38) * np.array(pgd_for_event)
        y = np.log10(dist_corr_mult_alt)
        #print(y)
        x_pgd = np.zeros(len(y))
        x_pgd = x_pgd + mag_event
        mask = ~np.isnan(y)
        #print(mask)
        pgd_corrected.append(y[mask])
        mags_with_data.append(x_pgd)
    return mags_with_data, pgd_corrected, list_n_stations, list_azimuths, list_distances, list_ids, list_mag, list_pgd



def calc_iv2_mag_lim_az(df, mag_lim, r_corr='2', n=0, min_dist=0, max_dist=1000):
    list_mag, list_iv2, list_n_stations, list_azimuths, list_distances, list_ids = sort_iv2_data_az(
        df, mag_lim, n=n, min_dist=min_dist, max_dist=max_dist)
    iv2_corrected = []
    mags_with_data = []
    for i, iv2_for_event in enumerate(list_iv2):
        distances_event = list_distances[i]
        mag_event = list_mag[i]
        r_corr = float(r_corr)
        dist_corr_mult = (np.array(distances_event) ** r_corr) * np.array(iv2_for_event)
        y = np.log10(dist_corr_mult)
        x_iv2 = np.zeros(len(y))
        x_iv2 = x_iv2 + mag_event
        mask = ~np.isnan(y)
        iv2_corrected.append(y[mask])
        mags_with_data.append(x_iv2)
    return mags_with_data, iv2_corrected, list_n_stations, list_azimuths, list_distances, list_ids, list_mag, list_iv2



def calc_opt(x, y, gradt, intercept, gradt_std, intercept_std, pearson, spearman, spearman_p, n_l):
    if len(y) > 0:
        x_use = np.array(x) - 5
        y_use = np.array(y)

        x = x_use
        y = y_use
        # x_unique = np.arange(min(x_use), max(x_use), 0.1)

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
    split_at_underscore = f.split('_')
    time = split_at_underscore[2][:-1]
    if time == '1' or time == '4':
        return time
    else:
        time = time[0] + '.' + time[1]
        return time


def name_to_snr(f):
    split_at_underscore = f.split('_')
    snr = split_at_underscore[-1]
    if snr[0:3] == 'snr':
        return snr[3:]


def name_to_blank(f):
    split_at_underscore = f.split('_')
    blank = split_at_underscore[9]
    return blank


def calc_min_max(std_level, a, b, std_a, std_b, x_unique=np.arange(3, 8, 0.1)):
    """
    Calculate the minimum and maximum values of a set of linear functions.

    Given input of the line of best fit's gradient and intercept, and the standard deviations
    of them, this function calculates the minimum and maximum y values which could be expected
    values over a range of x values.

    Parameters:
    std_level (float): Scaling factor for standard deviations.
    a (float): the gradient of the best fit line.
    b (float): the y-intercept of the best fit line.
    std_a (float): Standard deviation of the gradient.
    std_b (float): Standard deviation of  the y-intercept.
    x_unique (numpy.ndarray, optional): Array of unique x values to evaluate the linear functions.
        Defaults to np.arange(3, 8, 0.1).

    Returns:
    two numpy arrays.
        - y_min (numpy.ndarray): Array of minimum y values for each x value.
        - y_max (numpy.ndarray): Array of maximum y values for each x value.

    """
    y_1 = (a + (std_a * std_level)) * x_unique + (b + (std_b * std_level))
    y_2 = (a + (std_a * std_level)) * x_unique + (b - (std_b * std_level))
    y_3 = (a - (std_a * std_level)) * x_unique + (b + (std_b * std_level))
    y_4 = (a - (std_a * std_level)) * x_unique + (b - (std_b * std_level))

    y_min = np.minimum(np.minimum(y_1, y_2), np.minimum(y_3, y_4))
    y_max = np.maximum(np.maximum(y_1, y_2), np.maximum(y_3, y_4))

    return y_min, y_max


def plot_data_subplots(x_list, y_list, types, f,
                       save=False, show=True, title=None, path=None, min_dist=0, max_dist=200, n=0):
    fig, axs = plt.subplots(
        2, 2, figsize=figure_sizes.a4landscape, sharex=True)
    time = name_to_time(f)
    snr = name_to_snr(f)
    blank = name_to_blank(f)
    for i in range(0, 4):
        col = i // 2
        row = i % 2
        axs[row][col].grid(True)
        axs[row][col].scatter(x_list[i] + np.random.uniform(-0.05, 0.05, len(x_list[i])), y_list[i],
                              marker='x', color=colors[types[i]], s=10, alpha=0.5, zorder=100, rasterized=True)
        axs[row][col].set_ylabel(labels[types[i]], fontsize=12, labelpad=0)
        axs[row][col].tick_params(axis='both', which='major', labelsize=12)
        axs[row][col].set_xticks([3, 4, 5, 6, 7, 8], [], zorder=110)

        ax2 = axs[row][col].twiny()

        new_tick_locations = 2 / 3 * (np.arange(14, 22, 1) - 9.1)

        def tick_function(X):
            V = 10 ** ((1.5 * X) + 9.1)
            V = np.log10(V)
            return [str(int(z)) for z in V]

        ax2.set_xlim(axs[row][col].get_xlim())
        ax2.set_xticks(new_tick_locations)
        if row == 0:
            ax2.set_xticklabels(tick_function(new_tick_locations), fontsize=12)
            ax2.set_xlabel(r'$\log_{10}(M_0)$', fontsize=12)
        if row == 1:
            axs[row][col].set_xlabel('Magnitude', fontsize=12)
            ax2.set_xticklabels([])
        median, bin_edges, bin_number = scipy.stats.binned_statistic(
            x_list[i], y_list[i], statistic='median', bins=np.arange(2.95, 8.05, 0.1), range=None)
        axs[row][col].scatter(bin_edges[:-1] + 0.05, median, marker='o',
                              facecolor='lightgrey', edgecolors=colors[types[i]], zorder=1000)
    import matplotlib.transforms as mtransforms
    trans = mtransforms.ScaledTranslation(-20 / 72, 7 / 72, fig.dpi_scale_trans)
    axs[0][0].text(0.0, 1.0, 'a)', transform=axs[0][0].transAxes + trans,
                   fontsize='12', va='bottom')
    axs[0][1].text(0.0, 1.0, 'b)', transform=axs[0][1].transAxes + trans,
                   fontsize='12', va='bottom')
    axs[1][0].text(0.0, 1.0, 'c)', transform=axs[1][0].transAxes + trans,
                   fontsize='12', va='bottom')
    axs[1][1].text(0.0, 1.0, 'd)', transform=axs[1][1].transAxes + trans,
                   fontsize='12', va='bottom')
    # y = ax.get_yticks()

    axs[0][0].set_yticks([-1, 0, 1, 2], [fr'$10^{{{-1}}}$', 1, 10, fr'$10^{{{2}}}$'])
    axs[0][0].set_ylim([-1, 2])

    axs[0][1].set_yticks([-1, 0, 1, 2], [fr'$10^{{{-1}}}$', 1, 10, fr'$10^{{{2}}}$'])
    axs[0][1].set_ylim([-1, 2])

    axs[1][0].set_yticks(axs[1][0].get_yticks(), [fr'$10^{{{int(flt)}}}$' for flt in axs[1][0].get_yticks()])
    axs[1][1].set_yticks(axs[1][1].get_yticks(), [fr'$10^{{{int(flt)}}}$' for flt in axs[1][1].get_yticks()])
    axs[0][1].set_xticks([3, 4, 5, 6, 7, 8], [3, 4, 5, 6, 7, 8], zorder=110)
    axs[1][1].set_xticks([3, 4, 5, 6, 7, 8], [3, 4, 5, 6, 7, 8], zorder=110)

    # if title is not None:
    #     fig.suptitle(f'''
    #                  {title} ---
    #                  {name_to_time(f)} s window,
    #                  snr = {snr}, n >= {n},
    #                  distances = {min_dist}--{max_dist} km''',
    #                  fontsize=14, horizontalalignment = 'center')
    # else:
    #     fig.suptitle(
    #         f'''
    #         {name_to_time(f)} s window,
    #         snr = {snr}, n >= {n},
    #         distances = {min_dist}--{max_dist} km''', fontsize=14, horizontalalignment = 'center')
    figure = plt.gcf()
    figure.set_size_inches(figure_sizes.a4landscape)
    figure.tight_layout()
    if save is True and path is None:
        plt.savefig(
            f'''{paths.figure_path}/no_lines_{time}_blankwindow_{blank}_snr{snr}_n{n}_dist{min_dist}_{max_dist}.pdf''')
        print('saved default')
    elif save is True and path is not None:
        plt.savefig(f'''{path}/no_lines_{time}_blankwindow_{blank}_snr{snr}_n{n}_dist{min_dist}_{max_dist}.pdf''')
        print('saved to path')
    if show is True:
        plt.show()
    return figure


def plot_data_subplots_grey(x_list, y_list, types, f,
                            min_dist=0, max_dist=200, n=0, save=False, show=True, path=None):
    fig, axs = plt.subplots(
        2, 2, figsize=figure_sizes.a4landscape, sharex=True)
    time = name_to_time(f)
    snr = name_to_snr(f)
    blank = name_to_blank(f)
    for i in range(0, 4):
        col = i // 2
        row = i % 2
        axs[row][col].grid(True)
        axs[row][col].scatter(x_list[i] + np.random.uniform(-0.05, 0.05, len(x_list[i])), y_list[i],
                              marker='x', color='lightgrey', s=10, alpha=0.5, zorder=100, rasterized=True)
        axs[row][col].set_ylabel(labels[types[i]], fontsize=12, labelpad=0)
        axs[row][col].tick_params(axis='both', which='major', labelsize=12)
        axs[row][col].set_xticks([3, 4, 5, 6, 7, 8], [], zorder=110)

        ax2 = axs[row][col].twiny()

        new_tick_locations = 2 / 3 * (np.arange(14, 22, 1) - 9.1)
        # print(new_tick_locations, len(new_tick_locations))

        def tick_function(X):
            V = 10 ** ((1.5 * X) + 9.1)
            V = np.log10(V)
            return [str(int(z)) for z in V]
        # print(tick_function(new_tick_locations), len(tick_function(new_tick_locations)))
        ax2.set_xlim(axs[row][col].get_xlim())
        ax2.set_xticks(new_tick_locations)
        if row == 0:
            ax2.set_xticklabels(tick_function(new_tick_locations), fontsize=12)
            ax2.set_xlabel(r'$\log_{10}(M_0)$', fontsize=12)
        if row == 1:
            axs[row][col].set_xlabel('Magnitude', fontsize=12)
            ax2.set_xticklabels([])

        median, bin_edges, bin_number = scipy.stats.binned_statistic(
            x_list[i], y_list[i], statistic='median', bins=np.arange(2.95, 8.05, 0.1), range=None)
        axs[row][col].scatter(bin_edges[:-1] + 0.05, median, marker='x',
                              facecolor=colors[types[i]], edgecolors=colors[types[i]], zorder=1000)
    import matplotlib.transforms as mtransforms
    trans = mtransforms.ScaledTranslation(-20 / 72, 7 / 72, fig.dpi_scale_trans)
    axs[0][0].text(0.0, 1.0, 'a)', transform=axs[0][0].transAxes + trans,
                   fontsize='12', va='bottom')
    axs[0][1].text(0.0, 1.0, 'b)', transform=axs[0][1].transAxes + trans,
                   fontsize='12', va='bottom')
    axs[1][0].text(0.0, 1.0, 'c)', transform=axs[1][0].transAxes + trans,
                   fontsize='12', va='bottom')
    axs[1][1].text(0.0, 1.0, 'd)', transform=axs[1][1].transAxes + trans,
                   fontsize='12', va='bottom')
    # y = ax.get_yticks()

    axs[0][0].set_yticks([-1, 0, 1, 2], [fr'$10^{{{-1}}}$', 1, 10, fr'$10^{{{2}}}$'])
    axs[0][0].set_ylim([-1, 2])

    axs[0][1].set_yticks([-1, 0, 1, 2], [fr'$10^{{{-1}}}$', 1, 10, fr'$10^{{{2}}}$'])
    axs[0][1].set_ylim([-1, 2])

    axs[1][0].set_yticks(axs[1][0].get_yticks(), [fr'$10^{{{int(flt)}}}$' for flt in axs[1][0].get_yticks()])
    axs[1][1].set_yticks(axs[1][1].get_yticks(), [fr'$10^{{{int(flt)}}}$' for flt in axs[1][1].get_yticks()])
    axs[0][1].set_xticks([3, 4, 5, 6, 7, 8], [3, 4, 5, 6, 7, 8], zorder=110)
    axs[1][1].set_xticks([3, 4, 5, 6, 7, 8], [3, 4, 5, 6, 7, 8], zorder=110)

    # fig.suptitle(
    #     f'''
    #     {name_to_time(f)} s window,
    #     snr = {snr}, n >= {n},
    #     distances = {min_dist}--{max_dist} km''',
    #     ha='center',
    #     fontsize=14)
    figure = plt.gcf()
    figure.set_size_inches(figure_sizes.a4landscape)
    figure.tight_layout()

    if save is True and path is None:
        plt.savefig(
            f'''{paths.figure_path}/no_lines_{time}_blankwindow_{blank}_snr{snr}_n{n}_dist{min_dist}_{max_dist}_grey.pdf''')
        print('saved default')
    elif save is True and path is not None:
        plt.savefig(f'''{path}/no_lines_{time}_blankwindow_{blank}_snr{snr}_n{n}_dist{min_dist}_{max_dist}_grey.pdf''')
        print('saved to path')
    if show is True:
        plt.show()
    return figure


def plot_data_subplots_line(x_list, y_list, types, f, tp_params, pgd_params, tc_params, iv2_params,
                            n=0, save=False, show=True, min_dist=0, max_dist=200, hyp=False, path=None):

    params = [tp_params, pgd_params, tc_params, iv2_params]
    time = name_to_time(f)
    snr = name_to_snr(f)
    blank = name_to_blank(f)
    # [gradt, gradt_std, intercept, intercept_std]
    x_unique = np.arange(3, 8, 0.1)
    fig, axs = plt.subplots(
        2, 2, figsize=figure_sizes.a4landscape, sharex=True)
    for i in range(0, 4):  # for each parameter
        col = i // 2
        row = i % 2
        axs[row][col].grid(True)
        axs[row][col].scatter(x_list[i] + np.random.uniform(-0.05, 0.05, len(x_list[i])),
                              y_list[i],
                              marker='x',
                              color=colors[types[i]],
                              s=10,
                              alpha=0.5,
                              zorder=80,
                              rasterized=True)
        axs[row][col].set_ylabel(labels[types[i]], fontsize=12, labelpad=-2)
        axs[row][col].tick_params(axis='both', which='major', labelsize=12)
        axs[row][col].set_xticks([3, 4, 5, 6, 7, 8], [], zorder=110)

        ax2 = axs[row][col].twiny()

        new_tick_locations = 2 / 3 * (np.arange(14, 22, 1) - 9.1)

        def tick_function(X):
            V = 10 ** ((1.5 * X) + 9.1)
            V = np.log10(V)
            return [str(int(z)) for z in V]

        ax2.set_xlim(axs[row][col].get_xlim())
        ax2.set_xticks(new_tick_locations)
        if row == 0:
            ax2.set_xticklabels(tick_function(new_tick_locations), fontsize=12)
            ax2.set_xlabel(r'$\log_{10}(M_0)$', fontsize=12)
        if row == 1:
            axs[row][col].set_xlabel('Magnitude', fontsize=12)
            ax2.set_xticklabels([])

        x_unique = np.arange(3, 8, 0.1)

        a = params[i][0][0]
        std_a = params[i][1][0]
        b = params[i][2][0]
        std_b = params[i][3][0]
        median, bin_edges, bin_number = scipy.stats.binned_statistic(
            x_list[i], y_list[i], statistic='median', bins=np.arange(2.95, 8.05, 0.1), range=None)
        axs[row][col].scatter(bin_edges[:-1] + 0.05, median, marker='o',
                              facecolor='lightgrey', edgecolors=colors[types[i]], zorder=90)
        y_min, y_max = calc_min_max(1, a, b, std_a, std_b, x_unique=x_unique)
        axs[row][col].fill_between(x_unique, y_min - 5 * a, y_max - 5 * a,
                                   color='#003f5c', alpha=0.2, zorder=100)  # , label = '1sd')
        y_min, y_max = calc_min_max(2, a, b, std_a, std_b, x_unique=x_unique)
        axs[row][col].fill_between(x_unique, y_min - 5 * a, y_max - 5 * a,
                                   color='#003f5c', alpha=0.1, zorder=99)  # , label = '2sd')
        if b - 5 * a >= 0:
            axs[row][col].plot(x_unique, a * x_unique + (b - (5 * a)), color='#003f5c',
                               zorder=102, label=f'M3+: {a:.2f}M+{(b - 5 * a):.2f}')
        else:
            axs[row][col].plot(x_unique, a * x_unique + (b - (5 * a)), color='#003f5c',
                               zorder=102, label=f'M3+: {a:.2f}M-{abs((b - 5 * a)):.2f}')

        x_unique = np.arange(window_lengths[time], 8, 0.1)
        print(i, len(params[i][0]), time, len(window_lengths), params[i], window_lengths[time])
        print(int((window_lengths[time] - 3) * 10))
        print(len(params[i][0]))
        if int((window_lengths[time] - 3) * 10) < len(params[i][0]):
            print('in if')
            a = params[i][0][int((window_lengths[time] - 3) * 10)]
            std_a = params[i][1][int((window_lengths[time] - 3) * 10)]
            b = params[i][2][int((window_lengths[time] - 3) * 10)]
            std_b = params[i][3][int((window_lengths[time] - 3) * 10)]
            y_min, y_max = calc_min_max(1, a, b, std_a, std_b, x_unique=x_unique)
            axs[row][col].fill_between(
                x_unique, y_min - 5 * a, y_max - 5 * a, color='#003f5c', alpha=0.2, zorder=100)
            y_min, y_max = calc_min_max(2, a, b, std_a, std_b, x_unique=x_unique)
            axs[row][col].fill_between(
                x_unique, y_min - 5 * a, y_max - 5 * a, color='#003f5c', alpha=0.1, zorder=99)
            if b - 5 * a >= 0:
                axs[row][col].plot(x_unique, a * x_unique + (b - (5 * a)), color='#003f5c', zorder=102,
                                   linestyle='--', label=f'M{window_lengths[time]}+ : {a:.2f}M+{(b-5*a):.2f}')
            else:
                axs[row][col].plot(x_unique, a * x_unique + (b - (5 * a)), color='#003f5c', zorder=102,
                                   linestyle='--', label=f'M{window_lengths[time]}+ : {a:.2f}M-{abs((b-5*a)):.2f}')
        else:
            axs[row][col].plot([], [], color='#003f5c', zorder=102,
                               linestyle='--', label=f'M{window_lengths[time]}+ : no data')
        axs[row][col].legend(fontsize=12)
    import matplotlib.transforms as mtransforms
    trans = mtransforms.ScaledTranslation(-20 / 72, 7 / 72, fig.dpi_scale_trans)
    axs[0][0].text(0.0, 1.0, 'a)', transform=axs[0][0].transAxes + trans,
                   fontsize='12', va='bottom')
    axs[0][1].text(0.0, 1.0, 'b)', transform=axs[0][1].transAxes + trans,
                   fontsize='12', va='bottom')
    axs[1][0].text(0.0, 1.0, 'c)', transform=axs[1][0].transAxes + trans,
                   fontsize='12', va='bottom')
    axs[1][1].text(0.0, 1.0, 'd)', transform=axs[1][1].transAxes + trans,
                   fontsize='12', va='bottom')

    axs[0][0].set_yticks([-1, 0, 1, 2], [fr'$10^{{{-1}}}$', 1, 10, fr'$10^{{{2}}}$'])
    axs[0][0].set_ylim([-1, 2])

    axs[0][1].set_yticks([-1, 0, 1, 2], [fr'$10^{{{-1}}}$', 1, 10, fr'$10^{{{2}}}$'])
    axs[0][1].set_ylim([-1, 2])

    axs[1][0].set_yticks(axs[1][0].get_yticks(), [fr'$10^{{{int(flt)}}}$' for flt in axs[1][0].get_yticks()])
    axs[1][1].set_yticks(axs[1][1].get_yticks(), [fr'$10^{{{int(flt)}}}$' for flt in axs[1][1].get_yticks()])
    axs[0][1].set_xticks([3, 4, 5, 6, 7, 8], [3, 4, 5, 6, 7, 8], zorder=110)
    axs[1][1].set_xticks([3, 4, 5, 6, 7, 8], [3, 4, 5, 6, 7, 8], zorder=110)

    # fig.suptitle(
    #     f'''
    #     {time} s window,
    #     snr = {snr}, n >= {n},
    #     distances = {min_dist}--{max_dist} km''',
    #     fontsize=14, ha = 'center')
    figure = plt.gcf()
    figure.set_size_inches(figure_sizes.a4landscape)
    figure.tight_layout()

    if save is True and path is None:
        plt.savefig(
            f'''{paths.figure_path}/two_lines_{time}_blankwindow_{blank}_snr{snr}_n{n}_dist{min_dist}_{max_dist}.pdf''')
        print('saved default')
    elif save is True and path is not None:
        plt.savefig(f'''{path}/two_lines_{time}_blankwindow_{blank}_snr{snr}_n{n}_dist{min_dist}_{max_dist}.pdf''')
        print('saved to path')
    if show is True:
        plt.show()
    return figure
