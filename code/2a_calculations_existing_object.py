import earthquake
import os
import obspy
import util
import pickle

parameters = [
[1,0.1,19,0.25,'eq_object_1s_bandpass_01_19_snr_20_blank_025'],
[2,0.1,19,0.25,'eq_object_2s_bandpass_01_19_snr_20_blank_025'],
[3,0.1,19,0.25,'eq_object_3s_bandpass_01_19_snr_20_blank_025'],
[4,0.1,19,0.25,'eq_object_4s_bandpass_01_19_snr_20_blank_025']]

def find_with_data(root, cat):
    eq_with_data = []
    cat_with_data = obspy.Catalog()  # cat.copy()
    # cat_with_data.clear()
    for event in cat:  # check earthquakes have data AND PICKS
        eq_name = util.catEventToFileName(event)
        if os.path.isdir(root+eq_name) and os.path.isdir(root+eq_name+'/station_xml_files') and os.path.exists(root+eq_name+'/picks.pkl'):
            eq_with_data.append(eq_name)
            cat_with_data.extend([event])
    return eq_with_data
            
def do_calculation_preexisting(eq_with_data, root):        
    print("let's begin")
    for params in parameters:
        print(params)
        WINDOW_LEN, min_filter, max_filter, blank_window, fn = params
        for eq_no in range(0, len(eq_with_data)):
            print(params, eq_no)
            print('make object')
            if os.path.exists(root+eq_with_data[eq_no]+'/'+fn+'.pkl'):
                with open(root+eq_with_data[eq_no]+'/'+fn+'.pkl', 'rb') as picklefile:
                    eq = pickle.load(picklefile)
                eq.load(root=root)
                eq.calc_iv2(window_length=WINDOW_LEN)
                eq.calc_tc(window_length=WINDOW_LEN)
                print(eq.calculated_params['tau_c'])
                #eq.calc_tpmax(window_length=WINDOW_LEN, filter_limits=[min_filter,max_filter], blank_time = blank_window)
                del(eq.data)
                print('save object')
                #if eq.data is not False:
                with open(root+eq_with_data[eq_no]+'/'+ fn +'.pkl', 'wb') as picklefile:
                    pickle.dump(eq, picklefile)
                    
print('the big boys')
root = '/home/earthquakes1/homes/Rebecca/phd/data/2018_2021_global_m5/'
cat = obspy.read_events('/home/earthquakes1/homes/Rebecca/phd/data/2018_2021_global_m5_catalog.xml')
eq_with_data = find_with_data(root,cat)
do_calculation_preexisting(eq_with_data, root)


print('the little guys')    
root = '/home/earthquakes1/homes/Rebecca/phd/data/2019_global_m3/'
cat = obspy.read_events('/home/earthquakes1/homes/Rebecca/phd/data/2019_global_m3_catalog.xml')
eq_with_data = find_with_data(root,cat)
do_calculation_preexisting(eq_with_data, root)