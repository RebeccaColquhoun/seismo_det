import pickle
import os
import numpy as np


folders_big = os.listdir('/home/earthquakes1/homes/Rebecca/phd/data/2018_2021_global_m5/')
def del_data_big(eq_no):
    print(eq_no)
    difference = 0
    try:
        for file in os.listdir('/home/earthquakes1/homes/Rebecca/phd/data/2018_2021_global_m5/'+folders_big[eq_no]):
            start = os.path.getsize('/home/earthquakes1/homes/Rebecca/phd/data/2018_2021_global_m5/'+folders_big[eq_no]+'/'+file)
            if file.endswith(".pkl") and file.startswith('eq_object'):
                with open('/home/earthquakes1/homes/Rebecca/phd/data/2018_2021_global_m5/'+folders_big[eq_no]+'/'+file, 'rb') as picklefile:
                    eq = pickle.load(picklefile)
                del(eq.data)
                with open('/home/earthquakes1/homes/Rebecca/phd/data/2018_2021_global_m5/'+folders_big[eq_no]+'/'+file, 'wb') as picklefile:
                    pickle.dump(eq, picklefile)

                end = os.path.getsize('/home/earthquakes1/homes/Rebecca/phd/data/2018_2021_global_m5/'+folders_big[eq_no]+'/'+file)
                difference = difference + abs(start-end)
        return difference
    except Exception:
        print('except')
        return 0

space_saved = 0
for eq_no in range(0, len(folders_big)):
    deleted = del_data_big(eq_no)
    space_saved = space_saved + deleted
    if eq_no%100 == 0:
        print(space_saved)
print('final: '+str(space_saved))
'''
        
print(os.path.getsize('/home/earthquakes1/homes/Rebecca/phd/data/2019_global_m3/'+folders[eq_no]) )
try:
    for file in os.listdir('/home/earthquakes1/homes/Rebecca/phd/data/2019_global_m3/'+folders[eq_no]):
        if file.endswith(".pkl") and file.startswith('eq_object'):
            print(file)
            print(os.path.getsize('/home/earthquakes1/homes/Rebecca/phd/data/2019_global_m3/'+folders[eq_no]+'/'+file))
            with open('/home/earthquakes1/homes/Rebecca/phd/data/2019_global_m3/'+folders[eq_no]+'/'+file, 'rb') as picklefile:
                eq = pickle.load(picklefile)
            print(len(eq.data))
            del(eq.data)
            with open('/home/earthquakes1/homes/Rebecca/phd/data/2019_global_m3/'+folders[eq_no]+'/'+file, 'wb') as picklefile:
                pickle.dump(eq, picklefile)
            print(os.path.getsize('/home/earthquakes1/homes/Rebecca/phd/data/2019_global_m3/'+folders[eq_no]+'/'+file))
except Exception:
    print('except')
    pass
'''