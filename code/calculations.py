import earthquake
import os
import obspy
import util

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

print('make object')
for i in range(0, len(eq_with_data)):
    eq = earthquake.Earthquake(eq_with_data[0], cat_with_data[0])
    eq.eq_info()
    eq.calc_iv2()
    print(eq._cached_params['iv2'])
