import pickle
import pandas as pd
root = '/home/earthquakes1/homes/Rebecca/phd/data/2019_global_m3/'
with open(root+'list_iv2_0075_10', "rb") as fp:   #Pickling
    list_iv2 = pickle.load(fp)
with open(root+'list_mag_0075_10', "rb") as fp:   #Pickling
    list_mag = pickle.load(fp)
with open(root+'list_dist_0075_10', "rb") as fp:   #Pickling
    list_dist = pickle.load(fp) 
iv2_in_mag_bins =  [[] for _ in range(int((max(list_mag)-min(list_mag))*10))]
for i in range(0, len(list_mag)):
    iv2_in_mag_bins[int((list_mag[i]-min(list_mag))*10)].append(list_iv2[i])
with open(root+'iv2_in_mag_bins', "wb") as fp:   #Pickling
    pickle.dump(iv2_in_mag_bins, fp)