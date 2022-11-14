import earthquake
import os
import obspy
import util
import pickle

parameters = [
[1,0.1,19,0,'eq_object_1s_bandpass_01_19_snr_20_blank_0'],
[1,0.1,19,0.05,'eq_object_1s_bandpass_01_19_snr_20_blank_005'],
[1,0.1,19,0.1,'eq_object_1s_bandpass_01_19_snr_20_blank_01'],
[1,0.1,19,0.25,'eq_object_1s_bandpass_01_19_snr_20_blank_025'],
[1,0.1,19,0.5,'eq_object_1s_bandpass_01_19_snr_20_blank_05'],
[4,0.1,19,0,'eq_object_4s_bandpass_01_19_snr_20_blank_0'],
[4,0.1,19,0.05,'eq_object_4s_bandpass_01_19_snr_20_blank_005'],
[4,0.1,19,0.1,'eq_object_4s_bandpass_01_19_snr_20_blank_01'],
[4,0.1,19,0.25,'eq_object_4s_bandpass_01_19_snr_20_blank_025'],
[4,0.1,19,0.5,'eq_object_4s_bandpass_01_19_snr_20_blank_05']]

root_path = '/home/earthquakes1/homes/Rebecca/phd/data/'

def find_with_data(wanted):
    folder = root_path+wanted+'/'
    print(folder)
    cat = obspy.read_events(root_path+wanted+'_catalog.xml')
    print(len(cat))
    eq_with_data = []
    cat_with_data = obspy.Catalog()
    for event in cat:  # check earthquakes have data AND PICKS
        eq_name = util.catEventToFileName(event)
        if os.path.isdir(folder+eq_name) and os.path.isdir(folder+eq_name+'/station_xml_files') and os.path.exists(folder+eq_name+'/picks.pkl'):
            eq_with_data.append(eq_name)
            cat_with_data.extend([event])
    return eq_with_data, cat_with_data

def do_calculation_new(eq_with_data, cat_with_data, wanted, params):
    folder = root_path+wanted+'/'
    for eq_no in range(0, 1):#len(eq_with_data)):
        print(params[-1], eq_no)
        single_eq_calculation(eq_with_data[eq_no],cat_with_data[eq_no], folder, params)

def single_eq_calculation(eq_with_data_item, event, folder, params):
    WINDOW_LEN, min_filter, max_filter, blank_window, fn = params
    eq = earthquake.Earthquake(eq_with_data_item, event, root = folder)
    eq.eq_info()
    eq.load(root=folder)
    eq.calc_iv2(window_length=WINDOW_LEN)
    eq.calc_tc(window_length=WINDOW_LEN)
    eq.calc_tpmax(window_length=WINDOW_LEN, filter_limits=[min_filter,max_filter], blank_time = blank_window)
    if eq.data is not False:
        del(eq.data)
        with open(folder+eq_with_data_item+'/test/'+ fn +'.pkl', 'wb') as picklefile:
            pickle.dump(eq, picklefile)
    else:
        print('data problem:', wanted, str(eq_no))

wanted = '2018_2021_global_m5'
eq_with_data, cat_with_data = find_with_data(wanted)
print(len(eq_with_data), len(cat_with_data))
do_calculation_new(eq_with_data, cat_with_data, wanted, parameters[0])
