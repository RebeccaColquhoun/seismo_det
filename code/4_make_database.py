import pickle
import os
import geopy

import pandas as pd
import numpy as np

import setup_paths as paths

root_path = paths.data_path

subfolders = paths.data_subfolders

list_base_folders = []

for folder in subfolders:
    list_base_folders.append(os.path.join(root_path, folder) + '/')

filenames = ['eq_object_03s_snr_20_blank_0_snr20',
             'eq_object_05s_snr_20_blank_0_snr20',
             'eq_object_1s_snr_20_blank_0_snr20',
             'eq_object_4s_snr_20_blank_0_snr20']


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
                        'distance_dict': [make_distance_dict(eq)]})
    return df2


for fn in filenames:
    print(fn)
    for base_folder in list_base_folders:
        print(base_folder)
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
                                   'distance_dict'])
        print(len(folders))
        for eq_no in range(0, len(folders) - 1):
            print(eq_no)
            print(base_folder + folders[eq_no] + '/' + fn + '.pkl')
            if os.path.exists(base_folder + folders[eq_no] + '/' + fn + '.pkl'):
                print('in')
                with open(base_folder + folders[eq_no] + '/' + fn + '.pkl', 'rb') as picklefile:
                    eq = pickle.load(picklefile)
                    print(eq)
                    df2 = make_dataframe(eq)
                    print(df2)
                    df = pd.concat([df, df2])
        df = df.reset_index()
        isExist = os.path.exists(base_folder + 'results_database/')
        if not isExist:
            # Create a new directory because it does not exist
            os.makedirs(base_folder + 'results_database/')
        df.to_pickle(base_folder + 'results_database/results_' + fn + '.pkl')

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

    if not os.path.exists(paths.data_path + '/results_database_combined/'):
        os.makedirs(paths.data_path + '/results_database_combined')
    df.to_pickle(paths.data_path + '/results_database_combined/results_' + fn + '.pkl')
