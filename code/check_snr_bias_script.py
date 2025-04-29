import earthquake_snr as earthquake
import os
import obspy
import util
import pickle
from multiprocessing import Pool
import setup_paths as paths
import matplotlib.pyplot as plt

# fill out this with the parameters you want to use
# window length, blank window, filename to use
parameters = [[0.3, 0, 'eq_object_03s_snr_20_blank_0'],
              [0.5, 0, 'eq_object_05s_snr_20_blank_0'],
              [1, 0, 'eq_object_1s_snr_20_blank_0'],
              [4, 0, 'eq_object_4s_snr_20_blank_0']]

root_path = '/home/earthquakes1/homes/Rebecca/phd/data/'#paths.data_path
count = 0


def find_with_data(wanted):
    """
    Find earthquakes with data and picks.

    Args:
        wanted (str): The name of the directory of interest.

    Returns:
        - eq_with_data (list): A list of earthquake names with data and picks.
        - cat_with_data (obspy.Catalog): An ObsPy Catalog object containing events with data and picks.
    """
    folder = root_path + wanted + '/'
    cat = obspy.read_events(root_path + wanted + '_catalog.xml')
    eq_with_data = []
    cat_with_data = obspy.Catalog()
    for event in cat:  # check earthquakes have data AND PICKS
        eq_name = util.catEventToFileName(event)
        if (os.path.isdir(folder + eq_name)
                and os.path.isdir(folder + eq_name + '/station_xml_files')
                and os.path.exists(folder + eq_name + '/picks.pkl')):
            eq_with_data.append(eq_name)
            cat_with_data.extend([event])
    return eq_with_data, cat_with_data


def build_list():
    """
    Build a list of earthquakes with data and picks.

    Returns:
        list_for_multi (list): A list of lists containing the earthquake name, event, folder, and parameters.
    """
    #wanted_list = paths.data_subfolders
    wanted_list = ['2005_2018_global_m5', '2018_2021_global_m5', '2019_global_m3']
    list_for_multi = []
    for wanted in wanted_list:
        eq_with_data, cat_with_data = find_with_data(wanted)
        for params in parameters:
            for eq_no in range(0, len(eq_with_data)):
                list_for_multi.append([eq_with_data[eq_no],
                                      cat_with_data[eq_no],
                                      root_path + wanted + '/',
                                      params])
    return list_for_multi


snr_list = []
mag_list = []
list_for_multi = build_list()

for i in range(0, len(list_for_multi)):
	#print(i)
	eq_with_data_name, event, folder, params = list_for_multi[i]
	WINDOW_LEN, blank_window, fn = params
	#if os.path.isfile(folder + eq_with_data_name + '/' + fn + '_reviews_snr_20.pkl') is False:
	eq = earthquake.Earthquake(eq_with_data_name, event, root=folder)
	eq.eq_info()
	eq.calc_snr(root=folder)
	if eq.data is not False:
		#print('in if')
		#print(eq.snr)
		#print(eq.__dict__)
		snr_list.append(eq.snr)
		mag_list.append(eq.event_stats['eq_mag'])
		#print('snr_list', snr_list)
		#print('mag_list', mag_list)
	else:
		pass #print('no data')
	if i==0:
		print(i)
		with open('snr_list.pkl', 'wb') as f:
			pickle.dump(snr_list, f)
		with open('mag_list.pkl', 'wb') as f:
			pickle.dump(mag_list, f)
		snr_list = []
		mag_list = []
	elif i%10 == 0:
		print(i)
		with open('snr_list.pkl', 'ab') as f:
			pickle.dump(snr_list, f)
		with open('mag_list.pkl', 'ab') as f:
			pickle.dump(mag_list, f)
		snr_list = []
		mag_list = []






