import earthquake
import os
import obspy
import util
import pickle
from multiprocessing import Pool

parameters = [[1, 0.1, 19, 0.25, 'eq_object_1s_bandpass_01_19_snr_20_blank_025']]

root_path = '/home/earthquakes1/homes/Rebecca/phd/data/'
count = 0

def find_with_data(wanted):
    folder = root_path+wanted+'/'
    print(folder)
    cat = obspy.read_events(root_path+wanted+'_catalog.xml')
    print(len(cat))
    eq_with_data = []
    cat_with_data = obspy.Catalog()
    for event in cat:  # check earthquakes have data AND PICKS
        eq_name = util.catEventToFileName(event)
        if (os.path.isdir(folder+eq_name) and
                os.path.isdir(folder+eq_name+'/station_xml_files') and
                os.path.exists(folder+eq_name+'/picks.pkl')):
            eq_with_data.append(eq_name)
            cat_with_data.extend([event])
    return eq_with_data, cat_with_data


def do_calculation_new(num_proc=0):
    list_for_multi = build_list()
    if num_proc == 0:
        for i in range(0, len(list_for_multi)):
            single_eq_calculation(list_for_multi[i])
    else:
        with Pool(num_proc) as p:
            print(p.map(single_eq_calculation, list_for_multi))


def build_list():
    wanted_list = ['2005_2018_global_m5']
    list_for_multi = []
    for wanted in wanted_list:
        eq_with_data, cat_with_data = find_with_data(wanted)
        for params in parameters:
            for eq_no in range(0, len(eq_with_data)):
                list_for_multi.append([eq_with_data[eq_no],
                                      cat_with_data[eq_no],
                                      root_path+wanted+'/',
                                      params])
    return list_for_multi


def single_eq_calculation(calculation_values):
    eq_with_data_item, event, folder, params = calculation_values
    WINDOW_LEN, min_filter, max_filter, blank_window, fn = params
    eq = earthquake.Earthquake(eq_with_data_item, event, root=folder)
    eq.eq_info()
    eq.load(root=folder)
    eq.find_sensor_types()
    print(eq.event_stats['name'] )
    if len(eq.data_stats['picks'])>0:
        eq.calc_pgd(window_length=WINDOW_LEN)
    else:
        print('no picks')



# export OMP_NUM_THREADS = 1
# python calculations.py
if '__name__'=='__main__':
    list_for_multi = build_list()
    for i in range(0, len(list_for_multi)):
        single_eq_calculation(list_for_multi[i])
list_for_multi = build_list()
for i in range(0, len(list_for_multi)):
    #print(i)
    calculation_values = list_for_multi[i]
    eq_with_data_item, event, folder, params = calculation_values
    WINDOW_LEN, min_filter, max_filter, blank_window, fn = params
    eq = earthquake.Earthquake(eq_with_data_item, event, root=folder)
    eq.eq_info()
    eq.find_sensor_types()
    eq.calc_tc(window_length=WINDOW_LEN)
    eq.calc_tpmax(window_length=WINDOW_LEN,
                  filter_limits=[min_filter, max_filter],
                  blank_time=blank_window)
    print(i, len(eq.calculated_params))
    if len(eq.calculated_params)>0:
        if len(eq.calculated_params["tau_p_max"])!=len(eq.calculated_params["tau_c"]):
            print('different')