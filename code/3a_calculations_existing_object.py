# use this if you previously did calculations for only some parameters.
# comment out completed parameters as appropriate in do_calculation_preexisting
import earthquake
import os
import obspy
import util
import pickle
import setup_paths as paths

parameters = [[0.1, 0., 'eq_object_03s_snr_20_blank_0'],
              [0.3, 0., 'eq_object_05s_snr_20_blank_0'],
              [1, 0., 'eq_object_1s_snr_20_blank_0'],
              [4, 0., 'eq_object_4s_snr_20_blank_0']]


def find_with_data(root, cat):
    """
    Find earthquakes with data and picks.

    Args:
        root (str): The root directory.
        cat (obspy.Catalog): An ObsPy Catalog object containing events.

    Returns:
        - eq_with_data (list): A list of earthquake names with data and picks.
    """
    eq_with_data = []
    cat_with_data = obspy.Catalog()  # create empty catalog
    for event in cat:  # check earthquakes have data AND PICKS
        eq_name = util.catEventToFileName(event)
        if (os.path.isdir(root + eq_name)
                and os.path.isdir(root + eq_name + '/station_xml_files')
                and os.path.exists(root + eq_name + '/picks.pkl')):
            eq_with_data.append(eq_name)
            cat_with_data.extend([event])
    return eq_with_data


def do_calculation_preexisting(eq_with_data, root):
    """
    Perform calculations on the earthquakes with data and picks.

    Args:
        eq_with_data (list): A list of earthquake names with data and picks.
        root (str): The root directory.
    """

    print("let's begin")
    for params in parameters:
        print(params)
        WINDOW_LEN, blank_window, fn = params
        for eq_no in range(0, len(eq_with_data)):
            print(params, eq_no)
            print('make object')
            if os.path.exists(root + eq_with_data[eq_no] + '/' + fn + '.pkl'):
                with open(root + eq_with_data[eq_no] + '/' + fn + '.pkl', 'rb') as picklefile:
                    eq = pickle.load(picklefile)
                eq.load(root=root)
                eq.calc_iv2(window_length=WINDOW_LEN)
                eq.calc_tc(window_length=WINDOW_LEN)
                eq.calc_pgd(window_length=WINDOW_LEN)
                eq.calc_tp(window_length=WINDOW_LEN,
                           blank_window=blank_window)
                print(eq.calculated_params['tau_c'])
                if eq.data is not False:
                    del eq.data
                    print('save object')

                    with open(root + eq_with_data[eq_no] + '/' + fn + '.pkl', 'wb') as picklefile:
                        pickle.dump(eq, picklefile)


for folder in paths.data_subfolders:
    root = f'{paths.data_path}{folder}/'
    print(root)
    cat = obspy.read_events('{paths.data_path}{folder}_catalog.xml')
    eq_with_data = find_with_data(root, cat)
    do_calculation_preexisting(eq_with_data, root)
