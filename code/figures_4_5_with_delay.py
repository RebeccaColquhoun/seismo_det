import numpy as np
import pandas as pd
import matplotlib
import spearman_plotting_func as spearman_plotting
import setup_paths as paths

matplotlib.rcParams.update({'font.size': 14})
# 'eq_object_1s_snr_20_blank_neg_01_reviews_snr_20_delay.pkl',
# 		 	 'eq_object_03s_snr_20_blank_neg_01_reviews_snr_20_delay.pkl',
# 			 'eq_object_1s_snr_20_blank_01_reviews_snr_20_delay.pkl',
#              'eq_object_03s_snr_20_blank_01_reviews_snr_20_delay.pkl',
# 	 		 'eq_object_4s_snr_20_blank_neg_01_reviews_snr_20_delay.pkl',
# 			 'eq_object_05s_snr_20_blank_neg_01_reviews_snr_20_delay.pkl',
# 			 'eq_object_4s_snr_20_blank_01_reviews_snr_20_delay.pkl',
# 			 'eq_object_05s_snr_20_blank_01_reviews_snr_20_delay.pkl',
filenames = ['eq_object_04s_snr_20_blank_01_reviews_snr_20_delay.pkl',
            'eq_object_41s_snr_20_blank_01_reviews_snr_20_delay.pkl',
			'eq_object_06s_snr_20_blank_01_reviews_snr_20_delay.pkl',
			'eq_object_11s_snr_20_blank_01_reviews_snr_20_delay.pkl']
			# 'eq_object_02s_snr_20_blank_neg_01_reviews_snr_20_delay.pkl',
            #  'eq_object_39s_snr_20_blank_neg_01_reviews_snr_20_delay.pkl',
			#  'eq_object_04s_snr_20_blank_neg_01_reviews_snr_20_delay.pkl',
			#  'eq_object_09s_snr_20_blank_neg_01_reviews_snr_20_delay.pkl']


n_stations = 1
min_dist = 0
max_dist = 200

for f in filenames:
    print(f)
    #df = pd.read_pickle(f'{paths.data_path}results_database/{f}.pkl')
    df = pd.read_pickle(paths.data_path + '/results_database_different_window_lengths_for_reviews_delay/results_' + f + '.pkl')

    # can run for multiple (minimum) n_stations and min_dist, but for now just look at all data
    for n_stations in [1]:  # range(0,7):
        for min_dist in [0]:  # range(0, 100, 10):

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

            # do plotting
            spearman_plotting.plot_spearman_subplots_all_on_one_no_n_shaded_percent_var(f,
                                                                                        tp_params,
                                                                                        pgd_params,
                                                                                        iv2_params,
                                                                                        tc_params,
                                                                                        log=False, save=True,
																						path = '/home/earthquakes1/homes/Rebecca/phd/seismo_det/figures/figures_with_delay/',
                                                                                        **options)
