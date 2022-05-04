import earthquake
import os
import obspy
import util
import pickle

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
WINDOW_LEN = 4
for i in range(0, 1000):# len(eq_with_data)):
    print(i)
    print('make object')
    eq = earthquake.Earthquake(eq_with_data[i], cat_with_data[i])
    eq.eq_info()
    eq.calc_iv2(window_length=WINDOW_LEN)
    eq.calc_tc(window_length=WINDOW_LEN)
    eq.calc_tpmax(window_length=WINDOW_LEN)
    print('save object')
    if eq.data is not False:
        with open('/home/earthquakes1/homes/Rebecca/phd/data/2019_global_m3/'+eq_with_data[i]+'/eq_object_4s_bandpass.pkl', 'wb') as picklefile:
            pickle.dump(eq, picklefile)
    else:
        print('data problem')
'''
        
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
WINDOW_LEN = 1
for i in range(0, 1000):#len(eq_with_data)):
    print(i)
    print('make object')
    eq = earthquake.Earthquake(eq_with_data[i], cat_with_data[i])
    eq.eq_info()
    eq.calc_iv2(window_length=WINDOW_LEN)
    eq.calc_tc(window_length=WINDOW_LEN)
    eq.calc_tpmax(window_length=WINDOW_LEN)
    print('save object')
    if eq.data is not False:
        with open('/home/earthquakes1/homes/Rebecca/phd/data/2018_2021_global_m5/'+eq_with_data[i]+'/eq_object_1s_bandpass.pkl', 'wb') as picklefile:
            pickle.dump(eq, picklefile)
    else:
        print('data problem')
'''