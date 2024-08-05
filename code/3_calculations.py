import earthquake
import os
import obspy
import util
import pickle
from multiprocessing import Pool
import setup_paths as paths

# fill out this with the parameters you want to use
# window length, blank window, filename to use
parameters = [[0.3, 0, 'eq_object_03s_snr_20_blank_0'],
              [0.5, 0, 'eq_object_05s_snr_20_blank_0'],
              [1, 0, 'eq_object_1s_snr_20_blank_0'],
              [4, 0, 'eq_object_4s_snr_20_blank_0']]

root_path = paths.data_path
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


def do_calculation_new(num_proc=1):
    """
    Perform calculations on the earthquakes with data and picks.

    Args:
        num_proc (int): The number of processes to use for multiprocessing. Default
            is 1, which uses a single process.
    """
    list_for_multi = build_list()
    if num_proc == 1:
        for i in range(0, len(list_for_multi)):
            single_eq_calculation(list_for_multi[i])
    else:
        with Pool(num_proc) as p:
            p.map(single_eq_calculation, list_for_multi)


def build_list():
    """
    Build a list of earthquakes with data and picks.

    Returns:
        list_for_multi (list): A list of lists containing the earthquake name, event, folder, and parameters.
    """
    wanted_list = paths.data_subfolders
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


def single_eq_calculation(calculation_values):
    """
    Perform calculations on a single earthquake.

    Args:
        calculation_values (list): A list containing the earthquake name, event, folder, and parameters.
    """
    eq_with_data_name, event, folder, params = calculation_values
    WINDOW_LEN, blank_window, fn = params
    if os.path.isfile(folder + eq_with_data_name + '/' + fn + '_new_snr5.pkl') is False:
        eq = earthquake.Earthquake(eq_with_data_name, event, root=folder)
        eq.eq_info()
        eq.load(root=folder)
        eq.find_sensor_types()
        # print(eq.event_stats['name'] )
        if len(eq.data_stats['picks']) > 0:
            eq.calc_iv2(window_length=WINDOW_LEN)
            eq.calc_tc(window_length=WINDOW_LEN)
            eq.calc_pgd(window_length=WINDOW_LEN)
            eq.calc_tpmax(window_length=WINDOW_LEN,
                          blank_time=blank_window)
            if eq.data is not False:
                del eq.data  # don't save seismographs data in pickle file
                print(eq.event_stats['name'], fn)
                with open(folder + eq_with_data_name + '/' + fn + '_snr20.pkl', 'wb') as picklefile:
                    pickle.dump(eq, picklefile)
            else:
                print('data problem')
        else:
            print('no picks')
    else:
        print('already done')


if __name__ == '__main__':
    num_threads = paths.num_threads
    do_calculation_new(num_threads)
