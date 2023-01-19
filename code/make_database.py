#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
#import modin.pandas as pd
import pickle
import os
#from distributed import Client
#client = Client()


# In[2]:


list_base_folders = ['/home/earthquakes1/homes/Rebecca/phd/data/2005_2018_global_m5/','/home/earthquakes1/homes/Rebecca/phd/data/2018_2021_global_m5/','/home/earthquakes1/homes/Rebecca/phd/data/2019_global_m3/']


# In[3]:

filenames = ['eq_object_03s_bandpass_01_19_snr_20_blank_0_new',
              'eq_object_03s_bandpass_01_19_snr_20_blank_005_new',
              'eq_object_03s_bandpass_01_19_snr_20_blank_01_new']
'''filenames = ['eq_object_05s_bandpass_01_19_snr_20_blank_0_new',
             'eq_object_05s_bandpass_01_19_snr_20_blank_005_new', 
             'eq_object_05s_bandpass_01_19_snr_20_blank_01_new',
             'eq_object_05s_bandpass_01_19_snr_20_blank_025_new',
             'eq_object_1s_bandpass_01_19_snr_20_blank_0_new', 
             'eq_object_1s_bandpass_01_19_snr_20_blank_005_new',
             'eq_object_1s_bandpass_01_19_snr_20_blank_01_new',
             'eq_object_1s_bandpass_01_19_snr_20_blank_025_new',
             'eq_object_1s_bandpass_01_19_snr_20_blank_05_new',
              'eq_object_4s_bandpass_01_19_snr_20_blank_0_new',
              'eq_object_4s_bandpass_01_19_snr_20_blank_005_new',
              'eq_object_4s_bandpass_01_19_snr_20_blank_01_new',
              'eq_object_4s_bandpass_01_19_snr_20_blank_025_new',
              'eq_object_4s_bandpass_01_19_snr_20_blank_05_new']'''


# In[4]:


fn = 'eq_object_1s_bandpass_01_19_snr_20_blank_025_new'


# In[5]:


for fn in filenames:
    print(fn)
    for base_folder in list_base_folders:
        print(base_folder)
        folders = os.listdir(base_folder)
        df = pd.DataFrame(columns = [
        'eq_id',
        'eq_mag',
        'eq_mag_type',
        'eq_time',
        'eq_loc',
        'tp_max',
        'tp_max_stations',
        'tc',
        'tc_stations',
        'iv2',
        'iv2_distances',
        'iv2_stations',
        'pgd',
        'pgd_distances',
        'pgd_stations'])
        print(len(folders))
        for eq_no in range(0, len(folders)):
            #start = time.perf_counter()
            if os.path.exists(base_folder+folders[eq_no]+'/'+fn+'.pkl'):
                with open(base_folder+folders[eq_no]+'/'+fn+'.pkl', 'rb') as picklefile:
                    eq = pickle.load(picklefile)
                    df2 = pd.DataFrame({'eq_id':[str(eq.event.resource_id).split('=')[1]],
                           'eq_mag':[eq.event_stats['eq_mag']],
                            'eq_mag_type':[eq.event_stats['eq_mag_type']],
                            'eq_time':[eq.event_stats['name'][:-2]],
                           'eq_loc':[(eq.event_stats['eq_lat'], eq.event_stats['eq_long'], eq.event_stats['eq_depth']/1000)],
                            'tp_max':[eq.calculated_params['tau_p_max']],
                            'tp_max_stations':[eq.calculation_info["tau_p_stations"]],
                            'tc':[eq.calculated_params['tau_c']],
                            'tc_stations':[eq.calculated_params['tau_c_stations']],
                            'iv2':[eq.calculated_params['iv2']],
                            'iv2_distances':[eq.calculated_params['iv2_dist']],
                            'iv2_stations':[eq.calculation_info['iv2_stations']],
                            'pgd': [eq.calculated_params['pgd']],
                            'pgd_distances':[eq.calculated_params['pgd_distances']],
                            'pgd_stations':[eq.calculation_info['pgd_stations']]})
                    #print(df2)
                    df = pd.concat([df,df2])
        df = df.reset_index()
        isExist = os.path.exists(base_folder+'results_database/')
        if not isExist:
            # Create a new directory because it does not exist
            os.makedirs(base_folder+'results_database/')
        df.to_pickle(base_folder+'results_database/'+fn)



# In[47]:


for fn in filenames:
    df = pd.read_pickle('/home/earthquakes1/homes/Rebecca/phd/data/2005_2018_global_m5/results_database/'+fn)
    df2 = pd.read_pickle('/home/earthquakes1/homes/Rebecca/phd/data/2018_2021_global_m5/results_database/'+fn)
    df3 = pd.read_pickle('/home/earthquakes1/homes/Rebecca/phd/data/2019_global_m3/results_database/'+fn)
    df = pd.concat([df,df2])
    df = pd.concat([df,df3])
    df = df.reset_index()
    df.to_pickle('/home/earthquakes1/homes/Rebecca/phd/data/results_database/'+fn)


# In[48]:


df = pd.read_pickle('/home/earthquakes1/homes/Rebecca/phd/data/results_database/eq_object_1s_bandpass_01_19_snr_20_blank_025_new')

