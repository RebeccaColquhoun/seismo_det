#!/usr/bin/env python
# coding: utf-8

# ## Imports

# In[1]:


import os
import math
import obspy
import pickle
import datetime
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.pyplot import figure
from scipy.optimize import curve_fit
from datetime import timedelta
from obspy import UTCDateTime
from obspy.clients.fdsn import Client

from earthquake import earthquake
import util


# ## Get set up
# Set path to data, and read eq_list (all folders in root folder)

# In[2]:


root = '/home/earthquakes1/homes/Rebecca/phd/data/2019_global_m5/'

eq_list = os.listdir(root)


# Open catalog of events

# In[89]:


client = Client("IRIS")
# cat = client.get_events(starttime=UTCDateTime("2019-01-01"), endtime=UTCDateTime("2020-01-01"), minmagnitude=5, includearrivals=True)
cat = obspy.read_events('/home/earthquakes1/homes/Rebecca/phd/data/2019_global_m5_catalog.xml')


# Not all events had suitable data, look through all events and make a list of ones which have data (eq_with_data)

# In[91]:


eq_with_data = []
cat_with_data = cat.copy()
cat_with_data.clear()
for event in cat:
    eq_name = util.catEventToFileName(event)
    if os.path.isdir(root+eq_name) and os.path.isdir(root+eq_name+'/station_xml_files'):
        eq_with_data.append(eq_name)
        cat_with_data.extend([event])


# In[92]:


len(cat_with_data)


# In[85]:


cat.plot()


# In[93]:


cat_with_data.plot()


# In[107]:


cat[0].magnitudes[0].mag
mags = []
mags_d = []
for e in cat:
    mags.append(e.magnitudes[0].mag)
for e in cat_with_data:
    mags_d.append(e.magnitudes[0].mag)    
plt.hist(mags, np.arange(5, 8, 0.1))
plt.hist(mags_d, np.arange(5, 8, 0.1))
plt.yscale('log')


# ## the action!!
# For all events with data, load the data and then create an earthquake object. work out tp_max and tc, and add to lists (for plotting)

# In[5]:


list_tpmax = []
list_mags = []
list_tc= []
eqs = {}
count = 0
for eq_name in eq_with_data:
    
    d = util.filenameToDate(eq_name)
    
    filter_start = str(UTCDateTime(d-timedelta(seconds=1)))
    filter_stop = str(UTCDateTime(d+timedelta(seconds=1)))
    
    event = cat.filter('time > ' + filter_start, 'time < ' + filter_stop)
    # print(event)
    data = obspy.read(root+eq_name+'/data/*/*')
    inv = obspy.read_inventory(root+eq_name+'/station_xml_files/*')
    try:
        data.remove_response(inv)
    except:
        continue
    with open(root+eq_name+'/picks.pkl', 'rb') as f:
        picks = pickle.load(f)
    obj_name = eq_name[0:-2]
    
    eqs[obj_name] = earthquake(eq_name, event, data, picks, sensor_types = [])
    eqs[obj_name].calc_Tpmax()
    eqs[obj_name].calc_Tc()
    list_tpmax.append(eqs[obj_name]._cached_params["tau_p_max"])
    list_tc.append(eqs[obj_name]._cached_params["tau_c"])
    list_mags.append(eqs[obj_name].event.magnitudes[0].mag)
    print('earthquake number ' + str(count) + ' of '+ str(len(eq_with_data)) + ' done. It was ' + eq_name)
    count += 1


# ## plotting
# ### tp and tc subplots
# exclude points more than 1 std from the mean at each station. plot individual stations and the median of each station. 
# 
# make plot log-log

# set up function for scipy line fitting

# In[135]:


def model_function(x_data, a, b):
    return 10**(a*x_data + b)


# 

# In[161]:


get_ipython().run_cell_magic('capture', '', 'cs = [\'#00a1c1\']\nfig, axs = plt.subplots(1,2, figsize=(12.8,9.6))\ny_aves_tp = []\ny_aves_tc = []\nx_aves = []\n\nfor i  in range(0, len(list_mags)):  \n    mean_tp = np.mean(list_tpmax[i]) \n    std_tp = np.std(list_tpmax[i]) \n    y_tp = [] \n    for j in list_tpmax[i]: \n        if j > mean_tp-std_tp and j < mean_tp + std_tp and j < 10: \n            y_tp.append(j) \n    x_tp = np.zeros(len(y_tp))  \n    x_tp = x_tp + list_mags[i]  \n\n    mean_tc = np.mean(list_tc[i]) \n    std_tc = np.std(list_tc[i]) \n    y_tc = [] \n    for k in list_tc[i]: \n        if k > mean_tc-std_tc and k < mean_tc + std_tc and k < 10: \n            y_tc.append(k) \n    x_tc = np.zeros(len(y_tc))  \n    x_tc = x_tc + list_mags[i]\n    c = 0\n    if len(x_tp)>0 or len(x_tc)>0:\n        axs[0].scatter(x_tp, y_tp, s = 15, alpha = 0.3, c = cs[c], marker = \'^\', zorder =3) \n        #axs[0].scatter(list_mags[i], np.mean(y_tp), s = 50, c = cs[c], marker = \'o\')\n        axs[0].scatter(list_mags[i], np.median(y_tp), s = 50, c = cs[c], marker = \'^\', zorder =4)\n        axs[1].scatter(x_tc, y_tc, s = 15, alpha = 0.3, c = cs[c], marker = \'^\', zorder =3) \n        axs[1].scatter(list_mags[i], np.median(y_tc), s = 50, c = cs[c], marker = \'^\', zorder =4)\n        #axs[1].scatter(list_mags[i], np.mean(y_tc), s = 50, c = cs[c], marker = \'o\')\n        #FOR CURVE FITTING\n        if math.isnan(np.median(y_tp))==False:\n            y_aves_tp.append(np.median(y_tp))\n            x_aves.append(list_mags[i])\n        if math.isnan(np.median(y_tc))==False:\n            y_aves_tc.append(np.median(y_tc))\n\naxs[0].set_yscale(\'log\')\naxs[1].set_yscale(\'log\')\naxs[0].set_xlabel("magnitude") \naxs[1].set_xlabel("magnitude") \naxs[0].set_ylabel("tp_max") \naxs[1].set_ylabel("tc")\naxs[0].set_title("tp_max") \naxs[1].set_title("tc") \nfig.suptitle("median = triangle")')


# add line of best fit from olsen and allen 2005, with 2x absolute deviation band

# In[162]:


get_ipython().run_cell_magic('capture', '', "#plot line of best fit from olsen and allen 2005\nx = np.arange(5, 7.2, 0.1)\nx_lower = x - 0.54*2\nx_upper =  x + 0.54*2\ny = 10**(0.14*x-0.83)\ny_lower = 10**(0.14*x_lower-0.83)\ny_upper = 10**(0.14*x_upper-0.83)\naxs[0].plot(x, y, color = '#2a83ab', zorder =2)\naxs[0].fill_between(x, y_lower, y_upper, alpha = 0.3, color='coral', zorder =1)\naxs[0].plot(x, y_lower, color = '#2a83ab', linestyle = '--', zorder =2)\naxs[0].plot(x, y_upper, color = '#2a83ab', linestyle = '--', zorder =2)\nfig")


# use scipy curve_fit to add my own line of best fit

# In[163]:


get_ipython().run_cell_magic('capture', '', "# plot my own line of best fit\npopt, pcov = curve_fit(model_function, x_aves, y_aves_tp)\naxs[0].plot(np.array(x_aves), model_function(np.array(x_aves), *popt), color='#003f5c', zorder =2)\n\n# add 2 * std banding\n\nperr = np.sqrt(np.diag(pcov))\nx_me = np.arange(5, 7.2, 0.1)\nx_lower_me = x_me - 0.2642707*2\nx_upper_me =  x_me + 0.2642707*2\ny_me = 10**(0.14*x-0.83)\ny_lower_me = 10**(0.14*x_lower-0.83)\ny_upper_me = 10**(0.14*x_upper-0.83)\n#axs[0].plot(x, y_me, color = '')\naxs[0].fill_between(x, model_function(np.array(x_lower_me), *popt), model_function(np.array(x_upper_me), *popt), color = '#8adfff', alpha = 0.52, zorder =1)\naxs[0].plot(x, model_function(np.array(x_lower_me), *popt), color = '#003f5c', linestyle = '--', zorder =2)\naxs[0].plot(x, model_function(np.array(x_upper_me), *popt), color = '#003f5c', linestyle = '--', zorder =2)\n\nfig # show updated figure")


# In[164]:


# plot my own line of best fit for tc
popt_tc, pcov_tc = curve_fit(model_function, x_aves, y_aves_tc)
axs[1].plot(np.array(x_aves), model_function(np.array(x_aves), *popt_tc), color='#003f5c', zorder =2)

# add 2 * std banding

perr = np.sqrt(np.diag(pcov_tc))
x_me_tc = np.arange(5, 7.2, 0.1)
x_lower_me_tc = x_me_tc - 0.2642707*2
x_upper_me_tc =  x_me_tc + 0.2642707*2
#y_me_tc = 10**(0.14*x-0.83)
#y_lower_me_tc = 10**(0.14*x_lower-0.83)
#y_upper_me_tc = 10**(0.14*x_upper-0.83)
#axs[0].plot(x, y_me, color = '')
axs[1].fill_between(x, model_function(np.array(x_lower_me_tc), *popt_tc), model_function(np.array(x_upper_me_tc), *popt_tc), color = '#8adfff', alpha = 0.52, zorder =1)
axs[1].plot(x, model_function(np.array(x_lower_me_tc), *popt_tc), color = '#003f5c', linestyle = '--', zorder =2)
axs[1].plot(x, model_function(np.array(x_upper_me_tc), *popt_tc), color = '#003f5c', linestyle = '--', zorder =2)

fig # show updated figure


# In[ ]:


fig.savefig('/home/earthquakes1/homes/Rebecca/phd/seismo_det/figures/tp_and_tc/2019_m5_plus_REMOVED_INSTRUMENT_RESPONSE_tp_tc_olsen_fit.png', transparent=True)


# Now I'll plot tpmax and tc on the same graph because the slopes seem very similar so want to check they are a bit different...

# In[165]:


get_ipython().run_cell_magic('capture', '', 'cs = [\'#00a1c1\']\nfig, axs = plt.subplots(1,1, figsize=(12.8,9.6))\ny_aves_tp = []\ny_aves_tc = []\nx_aves = []\nx_aves_tc = []\n\nfor i  in range(0, len(list_mags)):  \n    mean_tp = np.mean(list_tpmax[i]) \n    std_tp = np.std(list_tpmax[i]) \n    y_tp = [] \n    for j in list_tpmax[i]: \n        if j > mean_tp-std_tp and j < mean_tp + std_tp and j < 10: \n            y_tp.append(j) \n    x_tp = np.zeros(len(y_tp))  \n    x_tp = x_tp + list_mags[i]  \n\n    mean_tc = np.mean(list_tc[i]) \n    std_tc = np.std(list_tc[i]) \n    y_tc = [] \n    for k in list_tc[i]: \n        if k > mean_tc-std_tc and k < mean_tc + std_tc and k < 10: \n            y_tc.append(k) \n    x_tc = np.zeros(len(y_tc))  \n    x_tc = x_tc + list_mags[i]\n    c = 0\n    if len(x_tp)>0 or len(x_tc)>0:\n        axs.scatter(x_tp, y_tp, s = 15, alpha = 0.3, c = cs[c], marker = \'^\', zorder =3) \n        #axs[0].scatter(list_mags[i], np.mean(y_tp), s = 50, c = cs[c], marker = \'o\')\n        axs.scatter(list_mags[i], np.median(y_tp), s = 50, c = cs[c], marker = \'^\', zorder =4)\n        axs.scatter(x_tc, y_tc, s = 15, alpha = 0.3, c = \'coral\', marker = \'*\', zorder =3) \n        axs.scatter(list_mags[i], np.median(y_tc), s = 50, c = \'coral\', marker = \'*\', zorder =4)\n        #axs[1].scatter(list_mags[i], np.mean(y_tc), s = 50, c = cs[c], marker = \'o\')\n        #FOR CURVE FITTING\n        if math.isnan(np.median(y_tp))==False:\n            y_aves_tp.append(np.median(y_tp))\n            x_aves.append(list_mags[i])\n        if math.isnan(np.median(y_tc))==False:\n            y_aves_tc.append(np.median(y_tc))\n            x_aves_tc.append(list_mags[i])\n\naxs.set_yscale(\'log\')\naxs.set_xlabel("magnitude") \naxs.set_ylabel("tp_max (^), tc (*)") \nfig.suptitle("median = triangle")')


# In[166]:


get_ipython().run_cell_magic('capture', '', "# plot my own line of best fit\npopt, pcov = curve_fit(model_function, x_aves, y_aves_tp)\naxs.plot(np.array(x_aves), model_function(np.array(x_aves), *popt), color='#008bad', zorder =2)\n\n# add 2 * std banding\n\nperr = np.sqrt(np.diag(pcov))\nx_me = np.arange(5, 7.2, 0.1)\nx_lower_me = x_me - 0.2642707*2\nx_upper_me =  x_me + 0.2642707*2\ny_me = 10**(0.14*x-0.83)\ny_lower_me = 10**(0.14*x_lower-0.83)\ny_upper_me = 10**(0.14*x_upper-0.83)\n#axs[0].plot(x, y_me, color = '')\n#axs.fill_between(x, model_function(np.array(x_lower_me), *popt), model_function(np.array(x_upper_me), *popt), color = '#8adfff', alpha = 0.52, zorder =1)\naxs.plot(x, model_function(np.array(x_lower_me), *popt), color = '#008bad', linestyle = '--', zorder =2)\naxs.plot(x, model_function(np.array(x_upper_me), *popt), color = '#008bad', linestyle = '--', zorder =2)\n\n# fig # show updated figure")


# In[167]:


# plot my own line of best fit for tc
popt_tc, pcov_tc = curve_fit(model_function, x_aves_tc, y_aves_tc)
axs.plot(np.array(x_aves), model_function(np.array(x_aves), *popt_tc), color='coral', zorder =2)

# add 2 * std banding

perr = np.sqrt(np.diag(pcov_tc))
x_me_tc = np.arange(5, 7.2, 0.1)
x_lower_me_tc = x_me_tc - 0.2642707*2
x_upper_me_tc =  x_me_tc + 0.2642707*2
#y_me_tc = 10**(0.14*x-0.83)
#y_lower_me_tc = 10**(0.14*x_lower-0.83)
#y_upper_me_tc = 10**(0.14*x_upper-0.83)
#axs[0].plot(x, y_me, color = '')
#axs.fill_between(x, model_function(np.array(x_lower_me_tc), *popt_tc), model_function(np.array(x_upper_me_tc), *popt_tc), color = '#8adfff', alpha = 0.52, zorder =1)
axs.plot(x, model_function(np.array(x_lower_me_tc), *popt_tc), color = 'coral', linestyle = '--', zorder =2)
axs.plot(x, model_function(np.array(x_upper_me_tc), *popt_tc), color = 'coral', linestyle = '--', zorder =2)

fig # show updated figure


# They are different, yay! 
# 

# In[83]:


get_ipython().run_cell_magic('script', 'false --no-raise-error', "fig.savefig('/home/earthquakes1/homes/Rebecca/phd/seismo_det/figures/tp_and_tc/2019_m5_plus_REMOVED_INSTRUMENT_RESPONSE_tp_and_tc_with_me_and_olsen_fit_shading_transparent.png', transparent=True)")


# ### importance of filtering
# turns out i only highpass filter if have acceleration data, so don't need this...

# In[10]:


get_ipython().run_cell_magic('script', 'false --no-raise-error', 'list_tpmax_2 = []\nlist_mags_2 = []\nlist_tc_2= []\neqs_2 = {}\ncount = 0\nfor eq_name in eq_with_data:\n    \n    d = util.filenameToDate(eq_name)\n    \n    filter_start = str(UTCDateTime(d-timedelta(seconds=1)))\n    filter_stop = str(UTCDateTime(d+timedelta(seconds=1)))\n    \n    event = cat.filter(\'time > \' + filter_start, \'time < \' + filter_stop)\n    # print(event)\n    data = obspy.read(root+eq_name+\'/data/*/*\')\n    with open(root+eq_name+\'/picks.pkl\', \'rb\') as f:\n        picks = pickle.load(f)\n    obj_name = eq_name[0:-2]\n    eqs_2[obj_name] = earthquake(eq_name, event, data, picks, sensor_types = [])\n    eqs_2[obj_name].calc_Tpmax(freq_cut_off=0.01, filter_corners = 4)\n    eqs_2[obj_name].calc_Tc()\n    list_tpmax_2.append(eqs[obj_name]._cached_params["tau_p_max"])\n    list_tc_2.append(eqs[obj_name]._cached_params["tau_c"])\n    list_mags_2.append(eqs[obj_name].event.magnitudes[0].mag)\n    print(\'earthquake number \' + str(count) + \' done. It was \' + eq_name)\n    count += 1')


# In[11]:


get_ipython().run_cell_magic('script', 'false --no-raise-error', 'cs = [\'#000000\']\nfig, axs = plt.subplots(1,2, figsize=(12.8,9.6))\ny_aves = []\nx_aves = []\ny_aves_2 = []\nx_aves_2 = []\nfor i  in range(0, len(list_mags)):  \n    mean_tp = np.mean(list_tpmax[i]) \n    std_tp = np.std(list_tpmax[i]) \n    y_tp = [] \n    for j in list_tpmax[i]: \n        if j > mean_tp-std_tp and j < mean_tp + std_tp and j < 10: \n            y_tp.append(j) \n    x_tp = np.zeros(len(y_tp))  \n    x_tp = x_tp + list_mags[i]  \n\n    mean_tp_2 = np.mean(list_tpmax_2[i]) \n    std_tp_2 = np.std(list_tpmax_2[i]) \n    y_tp_2 = [] \n    for j in list_tpmax_2[i]: \n        if j > mean_tp_2-std_tp_2 and j < mean_tp_2 + std_tp_2 and j < 10: \n            y_tp_2.append(j) \n    x_tp_2 = np.zeros(len(y_tp))  \n    x_tp_2 = x_tp_2 + list_mags_2[i] \n    c = 0\n    if len(x_tp)>0 or len(x_tp_2)>0:\n        axs[0].scatter(x_tp, y_tp, s = 15, alpha = 0.2, c = cs[c], marker = \'^\') \n        #axs[0].scatter(list_mags[i], np.mean(y_tp), s = 50, c = cs[c], marker = \'o\')\n        axs[0].scatter(list_mags[i], np.median(y_tp), s = 50, c = cs[c], marker = \'^\')\n        axs[1].scatter(x_tp_2, y_tp_2, s = 15, alpha = 0.2, c = cs[c], marker = \'^\') \n        axs[1].scatter(list_mags_2[i], np.median(y_tp_2), s = 50, c = cs[c], marker = \'^\')\n        #axs[1].scatter(list_mags[i], np.mean(y_tc), s = 50, c = cs[c], marker = \'o\')\n        #FOR CURVE FITTING\n        if math.isnan(np.median(y_tp))==False:\n            y_aves.append(np.median(y_tp))\n            x_aves.append(list_mags[i])\n        if math.isnan(np.median(y_tp_2))==False:\n            y_aves_2.append(np.median(y_tp_2))\n            x_aves_2.append(list_mags_2[i])\n\naxs[0].set_yscale(\'log\')\naxs[1].set_yscale(\'log\')\naxs[0].set_xlabel("magnitude") \naxs[1].set_xlabel("magnitude") \naxs[0].set_ylabel("tp_max") \naxs[1].set_ylabel("tc")\naxs[0].set_title("tp_max") \naxs[1].set_title("tc") \nfig.suptitle("median = triangle")')


# In[ ]:





# add line of best fit from olsen and allen 2005, with 2x absolute deviation band

# In[12]:


get_ipython().run_cell_magic('script', 'false --no-raise-error', "#plot line of best fit from olsen and allen 2005\nx = np.arange(5, 7.2, 0.1)\nx_lower = x - 0.54*2\nx_upper =  x + 0.54*2\ny = 10**(0.14*x-0.83)\ny_lower = 10**(0.14*x_lower-0.83)\ny_upper = 10**(0.14*x_upper-0.83)\naxs[0].plot(x, y, color = 'red')\naxs[0].plot(x, y_lower, color = 'red', linestyle = '--')\naxs[0].plot(x, y_upper, color = 'red', linestyle = '--')\nfig")


# use scipy curve_fit to add my own line of best fit

# In[13]:


get_ipython().run_cell_magic('script', 'false --no-raise-error', "# plot my own line of best fit\npopt, pcov = curve_fit(model_function, x_aves, y_aves)\naxs[0].plot(np.array(x_aves), model_function(np.array(x_aves), *popt), color='blue')\n\n# add 2 * std banding\n\nperr = np.sqrt(np.diag(pcov))\nx_me = np.arange(5, 7.2, 0.1)\nx_lower_me = x_me - 0.2642707*2\nx_upper_me =  x_me + 0.2642707*2\ny_me = 10**(0.14*x-0.83)\ny_lower_me = 10**(0.14*x_lower-0.83)\ny_upper_me = 10**(0.14*x_upper-0.83)\naxs[0].plot(x, y_me, color = 'red')\naxs[0].plot(x, model_function(np.array(x_lower_me), *popt), color = 'blue', linestyle = '--')\naxs[0].plot(x, model_function(np.array(x_upper_me), *popt), color = 'blue', linestyle = '--')\n\nfig # show updated figure")


# In[14]:


get_ipython().run_cell_magic('script', 'false --no-raise-error', "# plot my own line of best fit\npopt_2, pcov_2 = curve_fit(model_function, x_aves_2, y_aves_2)\naxs[1].plot(np.array(x_aves_2), model_function(np.array(x_aves_2), *popt_2), color='green')\n\n# add 2 * std banding\n\nperr_2 = np.sqrt(np.diag(pcov_2))\nx_me_2 = np.arange(5, 7.2, 0.1)\nx_lower_me_2 = x_me_2 - 0.2642707*2\nx_upper_me_2 =  x_me_2 + 0.2642707*2\ny_me_2 = 10**(0.14*x-0.83)\ny_lower_me_2 = 10**(0.14*x_lower-0.83)\ny_upper_me_2 = 10**(0.14*x_upper-0.83)\naxs[1].plot(x_me_2, y_me_2, color = 'red')\naxs[1].plot(x_me_2, model_function(np.array(x_lower_me_2), *popt_2), color = 'green', linestyle = '--')\naxs[1].plot(x_me_2, model_function(np.array(x_upper_me_2), *popt_2), color = 'green', linestyle = '--')\n\nfig # show updated figure")


# In[ ]:




