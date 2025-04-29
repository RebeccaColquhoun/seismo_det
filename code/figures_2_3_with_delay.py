import pandas as pd
import setup_paths as paths
import data_plotting_func_min_dist as data_plotting

import matplotlib
matplotlib.rcParams.update({'font.size': 20})


filenames = ['eq_object_04s_snr_20_blank_01_reviews_snr_20_delay.pkl']
            #'eq_object_09s_snr_20_blank_neg_01_reviews_snr_20_delay.pkl']
# 'eq_object_41s_snr_20_blank_01_reviews_snr_20_delay.pkl',
#			 'eq_object_06s_snr_20_blank_01_reviews_snr_20_delay.pkl',
#			'eq_object_11s_snr_20_blank_01_reviews_snr_20_delay.pkl',		 	 ,
# 'eq_object_02s_snr_20_blank_neg_01_reviews_snr_20_delay.pkl',
#              'eq_object_04s_snr_20_blank_neg_01_reviews_snr_20_delay.pkl',
# 		 	 'eq_object_39s_snr_20_blank_neg_01_reviews_snr_20_delay.pkl']
            #  'eq_object_04s_snr_20_blank_01_reviews_snr_20_delay.pkl',
            #  'eq_object_41s_snr_20_blank_01_reviews_snr_20_delay.pkl',
			#  'eq_object_06s_snr_20_blank_01_reviews_snr_20_delay.pkl',
			#  'eq_object_11s_snr_20_blank_01_reviews_snr_20_delay.pkl']
            #  'eq_object_1s_snr_20_blank_neg_01_reviews_snr_20_delay.pkl',
		 	#  'eq_object_03s_snr_20_blank_neg_01_reviews_snr_20_delay.pkl',
			#  'eq_object_1s_snr_20_blank_01_reviews_snr_20_delay.pkl',
            #  'eq_object_03s_snr_20_blank_01_reviews_snr_20_delay.pkl',
	 		#  'eq_object_4s_snr_20_blank_neg_01_reviews_snr_20_delay.pkl',
			#  'eq_object_05s_snr_20_blank_neg_01_reviews_snr_20_delay.pkl',
			#  'eq_object_4s_snr_20_blank_01_reviews_snr_20_delay.pkl',
			#  'eq_object_05s_snr_20_blank_01_reviews_snr_20_delay.pkl']

min_dist = 0
max_dist = 200

for f in filenames:
    print(f)
    df = pd.read_pickle(paths.data_path + '/results_database_different_window_lengths_for_reviews_delay/results_' + f + '.pkl')
    # can run for multiple (minimum) n_stations and min_dist, but for now just look at all data

    for min_dist in [0]:  # np.arange(0, 51, 10):
        for n_stations in [1]:  # range(0, 6, 1):

            # prepare data
            options = {'n': n_stations, 'min_dist': min_dist, 'max_dist': max_dist}
            x_tp, y_tp = data_plotting.calc_tp_mag_lim(df, 3., **options)
            x_pgd, y_pgd = data_plotting.calc_pgd_mag_lim(df, 3., **options)
            x_tc, y_tc = data_plotting.calc_tc_mag_lim(df, 3., **options)
            x_iv2, y_iv2 = data_plotting.calc_iv2_mag_lim(df, 3., **options)

            # make scatter plots of data without best fit lines
            data_plotting.plot_data_subplots([x_tp, x_iv2, x_tc, x_pgd],
                                             [y_tp, y_iv2, y_tc, y_pgd],
                                             ['tp', 'iv2', 'tc', 'pgd'],
                                             f,
                                             n=n_stations,
                                             min_dist=min_dist, max_dist=max_dist,
                                             save=True, show=False, path = '/home/earthquakes1/homes/Rebecca/phd/seismo_det/figures/figures_with_delay/')
            data_plotting.plot_data_subplots_grey([x_tp, x_iv2, x_tc, x_pgd],
                                                  [y_tp, y_iv2, y_tc, y_pgd],
                                                  ['tp', 'iv2', 'tc', 'pgd'],
                                                  f,
                                                  n=n_stations,
                                                  min_dist=min_dist, max_dist=max_dist,
                                                  save=True, show=False,
                                                  path = '/home/earthquakes1/homes/Rebecca/phd/seismo_det/figures/figures_with_delay/')

            # predominant period
            # define empty lists to store the results
            gradt, intercept, gradt_std, intercept_std = [], [], [], []
            pearson = []
            spearman = []
            spearman_p = []
            n_l = []

            # loop over magnitudes and calculate statistical values for each. append to lists just defined.
            for mag_lim in data_plotting.magnitudes:
                x, y = data_plotting.calc_tp_mag_lim(df, mag_lim, **options)
                output = data_plotting.calc_opt(x, y,
                                                gradt,
                                                intercept,
                                                gradt_std,
                                                intercept_std,
                                                pearson,
                                                spearman,
                                                spearman_p,
                                                n_l)
                gradt, intercept, gradt_std, intercept_std, pearson, spearman, spearman_p, n = output
            tp_params = [gradt, gradt_std, intercept, intercept_std, 'tp']

            # average period
            # define empty lists to store the results
            gradt, intercept, gradt_std, intercept_std = [], [], [], []
            pearson = []
            spearman = []
            spearman_p = []
            n_l = []
            # loop over magnitudes and calculate statistical values for each. append to lists just defined.
            for mag_lim in data_plotting.magnitudes:
                x, y = data_plotting.calc_tc_mag_lim(df, mag_lim, **options)
                output = data_plotting.calc_opt(x, y,
                                                gradt,
                                                intercept,
                                                gradt_std,
                                                intercept_std,
                                                pearson,
                                                spearman,
                                                spearman_p,
                                                n_l)
                gradt, intercept, gradt_std, intercept_std, pearson, spearman, spearman_p, n = output
            tc_params = [gradt, gradt_std, intercept, intercept_std, 'tc']

            # peak ground displacement
            # define empty lists to store the results
            gradt, intercept, gradt_std, intercept_std = [], [], [], []
            pearson = []
            spearman = []
            spearman_p = []
            n_l = []

            # loop over magnitudes and calculate statistical values for each. append to lists just defined.
            for mag_lim in data_plotting.magnitudes:
                x, y = data_plotting.calc_pgd_mag_lim(df, mag_lim, **options)
                output = data_plotting.calc_opt(x, y,
                                                gradt,
                                                intercept,
                                                gradt_std,
                                                intercept_std,
                                                pearson,
                                                spearman,
                                                spearman_p,
                                                n_l)
                gradt, intercept, gradt_std, intercept_std, pearson, spearman, spearman_p, n = output
            pgd_params = [gradt, gradt_std, intercept, intercept_std, 'pgd']

            # iv2
            # define empty lists to store the results
            gradt, intercept, gradt_std, intercept_std = [], [], [], []
            pearson = []
            spearman = []
            spearman_p = []
            n_l = []
            # loop over magnitudes and calculate statistical values for each. append to lists just defined.
            for mag_lim in data_plotting.magnitudes:
                x, y = data_plotting.calc_iv2_mag_lim(df, mag_lim, **options)
                output = data_plotting.calc_opt(x, y,
                                                gradt,
                                                intercept,
                                                gradt_std,
                                                intercept_std,
                                                pearson,
                                                spearman,
                                                spearman_p,
                                                n_l)
                gradt, intercept, gradt_std, intercept_std, pearson, spearman, spearman_p, n = output
            iv2_params = [gradt, gradt_std, intercept, intercept_std, 'iv2']

            # do plotting with best-fit lines
            data_plotting.plot_data_subplots_line([x_tp, x_iv2, x_tc, x_pgd],
                                                  [y_tp, y_iv2, y_tc, y_pgd],
                                                  ['tp', 'iv2', 'tc', 'pgd'],
                                                  f,
                                                  tp_params,
                                                  iv2_params,
                                                  tc_params,
                                                  pgd_params,
                                                  n=n_stations,
                                                  min_dist=min_dist, max_dist=max_dist,
                                                  save=True, show=False, hyp=False, 
                                                  path = '/home/earthquakes1/homes/Rebecca/phd/seismo_det/figures/figures_with_delay/')
