import pickle
import os
import geopy

import pandas as pd
import numpy as np
import math

import setup_paths as paths

root_path = paths.data_path

list_base_folders = ['/home/earthquakes1/homes/Rebecca/phd/data/2005_2018_global_m5/',
					 '/home/earthquakes1/homes/Rebecca/phd/data/2018_2021_global_m5/',
					 '/home/earthquakes1/homes/Rebecca/phd/data/2019_global_m3/']

# list_base_folders = []

# for folder in subfolders:
#     list_base_folders.append(os.path.join(root_path, folder) + '/')

# parameters = [[0.3, 0.1, 'eq_object_03s_snr_20_blank_01'],
#               [0.5, 0.1, 'eq_object_05s_snr_20_blank_01'],
#               [1, 0.1, 'eq_object_1s_snr_20_blank_01'],
#               [4, 0.1, 'eq_object_4s_snr_20_blank_01'],
#               [0.3, -0.1, 'eq_object_03s_snr_20_blank_neg_01'],
#               [0.5, -0.1, 'eq_object_05s_snr_20_blank_neg_01'],
#               [1, -0.1, 'eq_object_1s_snr_20_blank_neg_01'],
#               [4, -0.1, 'eq_object_4s_snr_20_blank_neg_01'],
#               [0.4, 0.1, 'eq_object_04s_snr_20_blank_neg_01'],
#               [0.6, 0.1, 'eq_object_06s_snr_20_blank_neg_01'],
#               [1.1, 0.1, 'eq_object_11s_snr_20_blank_neg_01'],
#               [4.1, 0.1, 'eq_object_41s_snr_20_blank_neg_01']]
# filenames = ['eq_object_03s_snr_20_blank_01_reviews_snr_20_delay.pkl',
# 	 		 'eq_object_4s_snr_20_blank_neg_01_reviews_snr_20_delay.pkl',
# 			 'eq_object_05s_snr_20_blank_neg_01_reviews_snr_20_delay.pkl',
# 			 'eq_object_4s_snr_20_blank_01_reviews_snr_20_delay.pkl',
# 			 'eq_object_05s_snr_20_blank_01_reviews_snr_20_delay.pkl',
# 			 'eq_object_04s_snr_20_blank_neg_01_reviews_snr_20_delay.pkl',
# 			 'eq_object_1s_snr_20_blank_neg_01_reviews_snr_20_delay.pkl',
# 		 	 'eq_object_03s_snr_20_blank_neg_01_reviews_snr_20_delay.pkl',
# 			 'eq_object_1s_snr_20_blank_01_reviews_snr_20_delay.pkl',
# 			 'eq_object_41s_snr_20_blank_neg_01_reviews_snr_20_delay.pkl',
# 			 'eq_object_06s_snr_20_blank_neg_01_reviews_snr_20_delay.pkl',
# 			 'eq_object_11s_snr_20_blank_neg_01_reviews_snr_20_delay.pkl']

filenames = ["eq_object_04s_snr_20_blank_neg_01_reviews_snr_20_delay.pkl",
			 "eq_object_09s_snr_20_blank_neg_01_reviews_snr_20_delay.pkl",
			 "eq_object_39s_snr_20_blank_neg_01_reviews_snr_20_delay.pkl",
			 "eq_object_02s_snr_20_blank_neg_01_reviews_snr_20_delay.pkl"]

# filenames = ['eq_object_03s_snr_20_blank_0_reviews_snr_20.pkl',
# 			 'eq_object_05s_snr_20_blank_0_reviews_snr_20.pkl',
# 			 'eq_object_1s_snr_20_blank_0_reviews_snr_20.pkl',
# 			 'eq_object_4s_snr_20_blank_0_reviews_snr_20.pkl']

# filenames = ['eq_object_03s_bandpass_01_19_snr_20_blank_0_new.pkl',
# 			 'eq_object_05s_bandpass_01_19_snr_20_blank_0_new.pkl',
# 			 'eq_object_1s_bandpass_01_19_snr_20_blank_0_new.pkl',
# 			 'eq_object_4s_bandpass_01_19_snr_20_blank_0_new.pkl']


def get_hypocenter(eq):
	'''
	This function takes an eq object and returns the latitude, longitude and
	depth of the hypocenter. If the hypocenter is not defined, it returns the
	latitude, longitude and depth of the first origin in the event.

	Parameters:
	eq: A earthquake class object containing, amongst other things:
		- an obspy event object

	Returns:
	tuple: A tuple containing hypocenter:
			- latitude
			- longitude
			- depth
	'''
	location = None
	for origin in eq.event.origins:
		if origin.origin_type == 'hypocenter':
			location = origin
			break
	if location is None:
		location = eq.event.origins[0]
	return (location.latitude, location.longitude, location.depth / 1000)


def make_distance_dict(eq):
	'''
	This function takes an eq object and returns a dictionary containing the
	distance between the hypocenter and each station in the inventory.

	Parameters:
	eq: A earthquake class object containing, amongst other things:
		- an obspy event object
		- an obspy inventory object

	Returns:
	dict: A dictionary containing the distance between the hypocenter and each
	station in the inventory.
	'''
	distances = {}
	inv = eq.inv
	eq_lat, eq_long, eq_depth = get_hypocenter(eq)
	for net in inv:
		for sta in net:
			for loc in sta:
				sta_lat = loc.latitude
				sta_long = loc.longitude
				distance = geopy.distance.distance((eq_lat, eq_long),
												   (sta_lat, sta_long))
				distance = np.sqrt(distance.km**2 + (eq_depth - loc.elevation / 1000)**2)
				distances[f"{net.code}.{sta.code}.{loc.location_code}"] = distance
	return distances

def get_bearing(lat1, long1, lat2, long2):
	dLon = (long2 - long1)
	x = math.cos(math.radians(lat2)) * math.sin(math.radians(dLon))
	y = math.cos(math.radians(lat1)) * math.sin(math.radians(lat2)) - math.sin(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(math.radians(dLon))
	brng = np.arctan2(x,y)
	brng = np.degrees(brng)

	return brng

def make_azimuth_dict(eq):
	'''
	This function takes an eq object and returns a dictionary containing the
	distance between the hypocenter and each station in the inventory.

	Parameters:
	eq: A earthquake class object containing, amongst other things:
		- an obspy event object
		- an obspy inventory object

	Returns:
	dict: A dictionary containing the distance between the hypocenter and each
	station in the inventory.
	'''
	azimuths = {}
	inv = eq.inv
	eq_lat, eq_long, eq_depth = get_hypocenter(eq)
	for net in inv:
		for sta in net:
			for loc in sta:
				sta_lat = loc.latitude
				sta_long = loc.longitude

				azimuth = get_bearing(eq_lat, eq_long, sta_lat, sta_long)
				azimuths[f"{net.code}.{sta.code}.{loc.location_code}"] = azimuth
	return azimuths


def make_dataframe(eq):
	'''
	This function takes an eq object and returns a dataframe containing the
	following information:
		- eq_id: The event id
		- eq_mag: The event magnitude
		- eq_mag_type: The event magnitude type
		- eq_time: The event time
		- eq_loc: The event location
		- tp_max: The maximum value of tau_p
		- tp_max_stations: The stations used to calculate tp_max
		- tc: The value of tau_c
		- tc_stations: The stations used to calculate tc
		- iv2: The value of iv2
		- iv2_distances: The distances between the hypocenter and each station
		- iv2_stations: The stations used to calculate iv2
		- iv2_stations_distances: The distances between the hypocenter and each
									station used to calculate iv2
		- pgd: The peak ground displacement
		- pgd_stations: The stations used to calculate pgd
		- pgd_stations_distances: The distances between the hypocenter and each
									station used to calculate pgd
		- distance_dict: A dictionary containing the distance between the
							hypocenter and each station in the inventory

	Parameters:
	eq: A earthquake class object

	Returns:
	dataframe: A dataframe containing the information listed above
	'''
	df2 = pd.DataFrame({'eq_id': [str(eq.event.resource_id).split('=')[1]],
						'eq_mag': [eq.event_stats['eq_mag']],
						'eq_mag_type': [eq.event_stats['eq_mag_type']],
						'eq_time': [eq.event_stats['name'][:-2]],
						'eq_loc': [(eq.event_stats['eq_lat'],
									eq.event_stats['eq_long'],
									eq.event_stats['eq_depth'] / 1000)],
						'tp_max': [eq.calculated_params['tau_p_max']],
						'tp_max_stations': [eq.calculation_info["tau_p_stations"]],
						'tc': [eq.calculated_params['tau_c']],
						'tc_stations': [eq.calculated_params['tau_c_stations']],
						'iv2': [eq.calculated_params['iv2']],
						'iv2_distances': [eq.calculated_params['iv2_dist']],
						'iv2_stations': [eq.calculation_info['iv2_stations']],
						'pgd': [eq.calculated_params['pgd']],
						'pgd_distances': [eq.calculated_params['pgd_distances']],
						'pgd_stations': [eq.calculation_info['pgd_stations']],
						'distance_dict': [make_distance_dict(eq)],
						'azimuth_dict': [make_azimuth_dict(eq)]})
	return df2


for fn in filenames:
	print(fn)
	#print(os.listdir(list_base_folders[0]))
	for base_folder in list_base_folders:
		#print(base_folder)
		folders = os.listdir(base_folder)
		df = pd.DataFrame(columns=['eq_id',
								   'eq_mag',
								   'eq_mag_type',
								   'eq_time',
								   'eq_loc',
								   'tp_max',
								   'tp_max_stations',
								   'tc',
								   'tc_stations',
								   'iv2',
								   'iv2_distances',
								   'iv2_stations',
								   'pgd',
								   'pgd_distances',
								   'pgd_stations',
								   'distance_dict',
								   'azimuth_dict'])
		#print(len(folders))
		for eq_no in range(0, len(folders) - 1):
			#print(folders[eq_no])
			#print(eq_no)
			if folders[eq_no][0] not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
				print(folders[eq_no])
				print('continue')
				continue

			#print(os.listdir(base_folder + folders[eq_no]))
			#print(base_folder + folders[eq_no] + '/' + fn + '.pkl')
			if os.path.exists(base_folder + folders[eq_no] + '/' + fn):
				#print('in')
				print(eq_no)
				with open(base_folder + folders[eq_no] + '/' + fn, 'rb') as picklefile:
					eq = pickle.load(picklefile)
					# print(eq.name)
					# print(eq)
					df2 = make_dataframe(eq)
					#print(df2)
					df = pd.concat([df, df2])
					#print(len(df))
			else:
				#print('not in')
				continue
				
		df = df.reset_index()
		isExist = os.path.exists(base_folder + 'results_database/')
		if not isExist:
			# Create a new directory because it does not exist
			os.makedirs(base_folder + 'results_database/')
		df.to_pickle(base_folder + 'results_database/results_' + fn + '.pkl')
		print(df)
		print(base_folder + 'results_database/results_' + fn + '.pkl')

	# now combine all the dataframes for this window/calculation setup into one,
	# even if the earthquake data is in several folders
	df_list = []
	for base_folder in list_base_folders:
		df_list.append(pd.read_pickle(base_folder + 'results_database/results_' + fn + '.pkl'))
		# df.to_pickle(paths.data_path + '/results_database_hypo/' + fn)
	if len(df_list) > 1:
		df = df_list[0]
		for i in range(1, len(df_list)):
			df = pd.concat([df, df_list[i]])
		df = df.reset_index()
	else:
		df = df_list[0]

	if not os.path.exists(paths.data_path + '/results_database_different_window_lengths_for_reviews_delay/'):
		os.makedirs(paths.data_path + '/results_database_different_window_lengths_for_reviews_delay')
	df.to_pickle(paths.data_path + '/results_database_different_window_lengths_for_reviews_delay/results_' + fn + '.pkl')
