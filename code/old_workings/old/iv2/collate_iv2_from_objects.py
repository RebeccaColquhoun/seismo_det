'''
uses objects to calculate iv2 and then puts those into dataframe and list
'''
import os
import pickle
import pandas as pd
import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt
import obspy
import earthquake
import util

iv2 = pd.DataFrame({'3.0': [[], [], [], [], [], [], [], []],
                      '3.1': [[], [], [], [], [], [], [], []],
                      '3.2': [[], [], [], [], [], [], [], []],
                      '3.3': [[], [], [], [], [], [], [], []],
                      '3.4': [[], [], [], [], [], [], [], []],
                      '3.5': [[], [], [], [], [], [], [], []],
                      '3.6': [[], [], [], [], [], [], [], []],
                      '3.7': [[], [], [], [], [], [], [], []],
                      '3.8': [[], [], [], [], [], [], [], []],
                      '3.9': [[], [], [], [], [], [], [], []],
                      '4.0': [[], [], [], [], [], [], [], []],
                      '4.1': [[], [], [], [], [], [], [], []],
                      '4.2': [[], [], [], [], [], [], [], []],
                      '4.3': [[], [], [], [], [], [], [], []],
                      '4.4': [[], [], [], [], [], [], [], []],
                      '4.5': [[], [], [], [], [], [], [], []],
                      '4.6': [[], [], [], [], [], [], [], []],
                      '4.7': [[], [], [], [], [], [], [], []],
                      '4.8': [[], [], [], [], [], [], [], []],
                      '4.9': [[], [], [], [], [], [], [], []],
                      '5.0': [[], [], [], [], [], [], [], []],
                      '5.1': [[], [], [], [], [], [], [], []],
                      '5.2': [[], [], [], [], [], [], [], []],
                      '5.3': [[], [], [], [], [], [], [], []],
                      '5.4': [[], [], [], [], [], [], [], []],
                      '5.5': [[], [], [], [], [], [], [], []],
                      '5.6': [[], [], [], [], [], [], [], []],
                      '5.7': [[], [], [], [], [], [], [], []],
                      '5.8': [[], [], [], [], [], [], [], []],
                      '5.9': [[], [], [], [], [], [], [], []],
                      '6.0': [[], [], [], [], [], [], [], []],
                      '6.1': [[], [], [], [], [], [], [], []],
                      '6.2': [[], [], [], [], [], [], [], []],
                      '6.3': [[], [], [], [], [], [], [], []],
                      '6.4': [[], [], [], [], [], [], [], []],
                      '6.5': [[], [], [], [], [], [], [], []],
                      '6.6': [[], [], [], [], [], [], [], []],
                      '6.7': [[], [], [], [], [], [], [], []],
                      '6.8': [[], [], [], [], [], [], [], []],
                      '6.9': [[], [], [], [], [], [], [], []],
                      '7.0': [[], [], [], [], [], [], [], []]})
list_mag = []
list_dist = []
list_iv2 = []
list_mag_types = []

ROOT = '/home/earthquakes1/homes/Rebecca/phd/data/2019_global_m3/'
eq_list = os.listdir(ROOT)
cat = obspy.read_events('/home/earthquakes1/homes/Rebecca/phd/data/2019_global_m3_catalog.xml')

eq_with_data = []
cat_with_data = obspy.Catalog()  # cat.copy()
# cat_with_data.clear()
for event in cat:  # check earthquakes have data AND PICKS
    eq_name = util.catEventToFileName(event)
    if (os.path.isdir(ROOT+eq_name) and
            os.path.isdir(ROOT+eq_name+'/station_xml_files') and
            os.path.exists(ROOT+eq_name+'/picks.pkl')):
        eq_with_data.append(eq_name)
        cat_with_data.extend([event])

# print('make object')
WINDOW_LENGTH = 4
for eq_no in range(0, len(eq_with_data)):
    print(eq_no)
    try:
        with open('/home/earthquakes1/homes/Rebecca/phd/data/2019_global_m3/'+eq_with_data[eq_no]+'/eq_object.pkl', 'rb') as picklefile:
            eq = pickle.load(picklefile)
    # print(eq.calculated_params['iv2'])

        for num_iv2 in range(len(eq.calculated_params['iv2'])):
            distance = eq.calculated_params['iv2'][num_iv2][1]
            current = iv2[str(np.round(eq.event_stats['eq_mag'], 1))][int(distance//25)]
            current.append(eq.calculated_params['iv2'][num_iv2][0])
            iv2[str(np.round(eq.event_stats['eq_mag'], 1))][int(distance//25)] = current
            list_iv2.append(eq.calculated_params['iv2'][num_iv2][0])
            list_mag.append(eq.event_stats['eq_mag'])
            list_dist.append(distance)
            list_mag_types.append(eq.event_stats['eq_mag_type'])
    except Exception:
        continue
    # with open(root+eq_with_data[eq_no]+'/eq_object', )

    if eq_no % 100 == 0:
        iv2.to_pickle(ROOT+'iv2_dataframe_bkg_window4.pkl')
        with open(ROOT+'list_iv2_bkg_window4', "wb") as fp:
            pickle.dump(list_iv2, fp)
        with open(ROOT+'list_mag_bkg_window4', "wb") as fp:
            pickle.dump(list_mag, fp)
        with open(ROOT+'list_mag_types_bkg_window4', "wb") as fp:
            pickle.dump(list_mag_types, fp)
        with open(ROOT+'list_dist_bkg_window4', "wb") as fp:
            pickle.dump(list_dist, fp)
        #iv2_2.to_pickle(ROOT+'iv2_dataframe_bkg_window2.pkl')
        #with open(ROOT+'list_iv2_bkg_window2', "wb") as fp:
        #    pickle.dump(list_iv2_2, fp)
        #with open(ROOT+'list_mag_bkg_window2', "wb") as fp:
        #    pickle.dump(list_mag_2, fp)
        #with open(ROOT+'list_dist_bkg_window2', "wb") as fp:
        #    pickle.dump(list_dist_2, fp)

        # counts[str(eq.event_stats['eq_mag'])][int(distance//25)] =
        # counts[str(eq.event_stats['eq_mag'])][int(distance//25)] + 1

'''iv2.to_pickle(ROOT+'iv2_dataframe_bkg_window4.pkl')
with open(ROOT+'list_iv2_bkg_window4', "rb") as fp:
    pickle.dump(list_iv2, fp)
with open(ROOT+'list_mag_bkg_window4', "rb") as fp:
    pickle.dump(list_mag, fp)
with open(ROOT+'list_dist_bkg_window4', "rb") as fp:
    pickle.dump(list_dist, fp)'''
def obj(to_opt):
    '''optimisation function'''
    a_opt=to_opt[0]
    b_opt=to_opt[1]
    #importance = np.array(n)
    y_real= np.log10(dist_corr_mult)
    x_list = np.array(mag_plot)
    y_guess = (a_opt*x_list+b_opt)
    print(y_guess)
    return sum(abs(y_guess-y_real))


dist_plot = []
iv2_plot = []
mag_plot = []
mag_type = []
#to_plot = pd.DataFrame({'iv2': [], 'dist':[], 'mag'=[], 'mag_type' = []})
to_plot_list = []
for i, iv2_entry in enumerate(list_iv2):
    if (
            iv2_entry is not None
            and list_dist[i] is not None
            and list_mag[i] is not None
            and iv2_entry>0):
        # iv2_plot.append(iv2_entry)
        # dist_plot.append(list_dist[i])
        # mag_plot.append(list_mag[i])
        # mag_type.append(list_mag_types[i][0:2].lower())
        to_plot_list.append([iv2_entry, list_dist[i], list_mag[i], list_mag_types[i][0:2].lower()])
to_plot=pd.DataFrame(to_plot_list, columns = ['iv2', 'dist', 'mag', 'mag_type'])
#dist_corr_mult_ext = (np.array(dist_plot)**2)*np.array(iv2_plot)
dist_corr_mult = to_plot.iv2/to_plot.dist
mag_plot = to_plot.mag
iv2_in_mag_bins =  [[] for _ in range(int((max(list_mag)-min(list_mag))*10)+1)]
for i, mag in enumerate(mag_plot):  # in range(0, len(list_mag_4)):
    iv2_in_mag_bins[int((mag-min(list_mag))*10)].append(dist_corr_mult[i])

mag_bin_medians = []
for l in iv2_in_mag_bins:
    mag_bin_medians.append(np.median(l))
#+++++++PLOTTING++++++++++
# LINE_BY_MAG_TYPE = True
# COLOR_BY_MAG_TYPE = True
def plot(line_by_mag_type=True, color_by_mag_type=True):
    fig,axs = plt.subplots()
    dist_corr_mult = to_plot.iv2/to_plot.dist
    mag_plot = to_plot.mag
    # dist_corr_mult = to_plot.iv2/to_plot.dist
    # mag_plot = to_plot.mag
    initial_guess = (1.4,0)
    res = optimize.minimize(obj, initial_guess, method = 'Nelder-mead')

    x = np.arange(min(mag_plot), max(mag_plot), 0.1)
    y = res.x[0] * x + res.x[1]

    axs.plot(x,y, label = str(res.x[0]) + '*x+'+ str(res.x[1]), color = 'k', linestyle = ':')

    if line_by_mag_type is False:
        colors = {'ml':"#ddc000", 'mw':"#79ad41", 'mb':"#34b6c6", 'md':"#4063a3"}
        if color_by_mag_type is False:
            pcm = axs.scatter(
                to_plot.mag,
                np.log10(dist_corr_mult),
                c = to_plot.dist,
                cmap = 'inferno',
                alpha = 1)
            fig.colorbar(pcm, label = 'distance (km)')
        else:
            axs.scatter(mag_plot, np.log10(dist_corr_mult),
                       c = list(to_plot.mag_type.map(colors)),
                       alpha = 1)
        plt.scatter(np.arange(min(to_plot.mag), max(to_plot.mag)+0.1, 0.1),
                    np.log10(mag_bin_medians),
                    marker='x',
                    color='silver',
                    label='median in mag bins')
    else:  # plot each group individually
        colors = ["#88a0dc", "#381a61", "#7c4b73", "#ed968c", "#ab3329", "#e78429", "#f9d14a"]
        # [ "#ddc000", "#79ad41", "#34b6c6", "#4063a3"]
        groups = to_plot.groupby(['mag_type'])
        for  j,(k,v) in enumerate(groups):
            axs.scatter(v.mag, np.log10(v.iv2/v.dist),
                       color = colors[j],
                       alpha = 0.5,
                       marker = 'x',
                       label = k + ',' + str(len(v.mag_type)))
            dist_corr_mult = v.iv2/v.dist
            mag_plot = v.mag
            initial_guess = (1.4,0)
            res = optimize.minimize(obj, initial_guess, method = 'Nelder-mead')
            x = np.arange(min(mag_plot), max(mag_plot), 0.1)
            y = res.x[0] * x + res.x[1]
            axs.plot(x,y, label = str(res.x[0]) + '*x+'+ str(res.x[1]), color = colors[j])

    plt.title('''log10(iv2) referenced to 1km by multiplying by distance^2.
              window length = '''+str(WINDOW_LENGTH))
    plt.ylabel('log10(iv2)')
    plt.xlabel('magntitude')
    plt.legend()
    plt.show()

def plot_heatmap():
    dist_corr_mult = to_plot.iv2/to_plot.dist
    mag_plot = to_plot.mag
    plt.figure(figsize=(20,10))
    y_limits = np.logspace(-20, 2, 100)
    x_limits = np.linspace(3, 7, 41)
    H, xedges, yedges = np.histogram2d(list(mag_plot), list(dist_corr_mult),  bins=[x_limits, y_limits])
    H = H.T

    plt.imshow(np.log(H), interpolation='nearest', origin='lower', extent=[xedges[0], xedges[-1], np.log10(yedges[0]), np.log10(yedges[-1])], aspect = 0.5, cmap = 'inferno', vmin = np.log10(0.5))
    plt.colorbar(label = 'log10(histogram amplitude)')

    plt.ylabel('log10(iv2)')
    plt.xlabel('magntitude')
    plt.ylim([-20,2])

    initial_guess = (1.4,0)
    res = optimize.minimize(obj, initial_guess, method = 'Nelder-mead')
    x = np.linspace(min(mag_plot), max(mag_plot), 20)
    y = res.x[0] * x + res.x[1]
    plt.plot(x,y, label = str(res.x[0]) + '*x+'+ str(res.x[1]))
    plt.scatter(np.arange(3, 6.8, 0.1), np.log10(mag_bin_medians), marker = 'x', color = 'silver')
    
    plt.show()
plot_heatmap()