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

print('the big boys')
root = '/home/earthquakes1/homes/Rebecca/phd/data/2018_2021_global_m5/'
eq_list = os.listdir(root)
cat = obspy.read_events('/home/earthquakes1/homes/Rebecca/phd/data/2018_2021_global_m5_catalog.xml')

eq_with_data = []
cat_with_data = obspy.Catalog()  # cat.copy()
# cat_with_data.clear()
for event in cat:  # check earthquakes have data AND PICKS
    eq_name = util.catEventToFileName(event)
    if os.path.isdir(root+eq_name) and os.path.isdir(root+eq_name+'/station_xml_files') and os.path.exists(root+eq_name+'/picks.pkl'):
        eq_with_data.append(eq_name)
        cat_with_data.extend([event])
        
print("everything loaded, let's begin")
for params in parameters:
    print(params)
    WINDOW_LEN, min_filter, max_filter, blank_window, fn = params

    for i in range(0, len(eq_with_data)):
        print(parameters[-1], i)
        print('make object')
        eq = earthquake.Earthquake(eq_with_data[i], cat_with_data[i], root = '/home/earthquakes1/homes/Rebecca/phd/data/2018_2021_global_m5/')
        eq.eq_info()
        #eq.calc_iv2(window_length=WINDOW_LEN)
        #eq.calc_tc(window_length=WINDOW_LEN)
        eq.calc_tpmax(window_length=WINDOW_LEN, filter_limits=[min_filter,max_filter], blank_time = blank_window)
        del(eq.data)
        print('save object')
        if eq.data is not False:
            with open('/home/earthquakes1/homes/Rebecca/phd/data/2018_2021_global_m5/'+eq_with_data[i]+'/'+ fn +'.pkl', 'wb') as picklefile:
                pickle.dump(eq, picklefile)
        else:
            print('data problem')

print('the little guys')    
root = '/home/earthquakes1/homes/Rebecca/phd/data/2019_global_m3/'
eq_list = os.listdir(root)
cat = obspy.read_events('/home/earthquakes1/homes/Rebecca/phd/data/2019_global_m3_catalog.xml')

eq_with_data = []
cat_with_data = obspy.Catalog()  # cat.copy()
# cat_with_data.clear()
for event in cat:  # check earthquakes have data AND PICKS
    eq_name = util.catEventToFileName(event)
    if os.path.isdir(root+eq_name) and os.path.isdir(root+eq_name+'/station_xml_files') and os.path.exists(root+eq_name+'/picks.pkl'):
        eq_with_data.append(eq_name)
        cat_with_data.extend([event])
print("everything loaded, let's begin")        
for params in parameters:
    print(params)
    WINDOW_LEN, min_filter, max_filter, blank_window, fn = params
    for i in range(0, len(eq_with_data)):
        print(parameters[-1], i)
        print('make object')
        eq = earthquake.Earthquake(eq_with_data[i], cat_with_data[i], root = '/home/earthquakes1/homes/Rebecca/phd/data/2019_global_m3/')
        eq.eq_info()
        #eq.calc_iv2(window_length=WINDOW_LEN)
        #eq.calc_tc(window_length=WINDOW_LEN)
        eq.calc_tpmax(window_length=WINDOW_LEN, filter_limits=[min_filter,max_filter], blank_time = blank_window)
        del(eq.data)
        print('save object')
        if eq.data is not False:
            with open('/home/earthquakes1/homes/Rebecca/phd/data/2019_global_m3/'+eq_with_data[i]+'/'+ fn +'.pkl', 'wb') as picklefile:
                pickle.dump(eq, picklefile)
        else:
            print('data problem')
