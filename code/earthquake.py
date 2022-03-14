#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import obspy
import numpy as np
import math

class earthquake(object):

    '''
    Class implementing the phase coherence method

    Args required:
        * name      : Instance Name
        * template  : Obspy stream for templates

    Args optional:
        * data      : Obspy stream of data set to search (default: st1)
        * lat0      : Origin latitude (for plot, default=0)
        * lon0      : Origin longitude (for plot, default=0)
    '''

    # -------------------------------------------------------------------------------
    # Initialize class #
    def __init__(self, name, catalog_object, data, picks={}, sensor_types=[]):
        '''
        Initialize main variables of the class

        * name -- instance name -- string
        * time -- earthquake time -- time
        * data -- obspy stream
        * picks -- defaults to empty list, otherwise is a list of time variables
        '''
        # print('init')
        # Save name
        assert(type(name) is str), 'name argument must be a string'
        self.name = name
        self.event = catalog_object[0]
        # Copy data and template with copuy.deepcopy() to avoid changing original data
        # Save template
        assert(type(data) is obspy.core.stream.Stream), 'must be an obspy stream'
        self.data = data.copy()
        self._cached_params = {}
        self.data_stats = {}
        self.data_stats['picks'] = picks
        self.stalta = []
        self.find_sensor_types()
    
    def find_sensor_types(self):
        data = self.data
        sensor_types = []
        for i in range(0, len(self.data)):
            proc = data[i].stats['processing'][0]
            loc = proc.find('output')
            st = proc[loc+8:loc+11]
            sensor_types.append(st)
        self.data_stats['sensor_types'] = sensor_types
        
    def calc_Tpmax(self, window_length=4, start_window=0, freq_cut_off = 0.1, filter_corners = 3):
        """

        :param window: window over which to calculate max predominant period, defaults to 4
        :type window: int, optional
        :param window: window over which to calculate max predominant period, defaults to 4
        :type window: int, optional

        alters:
            _cached_params["tau_p"] -- list of calculated predominant period for all traces
            _cached_params["tau_p_max"] -- list of max predominant periods (1 value for each trace)

        """
        from obspy import UTCDateTime
        data = self.data
        picks = self.data_stats['picks']
        sensor_types = self.data_stats['sensor_types']
        tau_p_list = []
        tp_max = []
        for i in range(0, len(data)):  # iterate through all traces
            if data[i].stats.channel[2] == 'Z':  # only use vertical components
                tr = data[i].copy()
                station = tr.stats.station
                #station = station.ljust(4)
                tr_name = tr.stats.network+'.'+tr.stats.station+'.'+tr.stats.location
                if tr_name in picks.keys():
                    # load saved parameters
                    sampling_rate = tr.stats.sampling_rate
                    pick = UTCDateTime(picks[tr_name])
                    #preprocess data
                    tr.detrend()
                    if sensor_types[i][0] == 'a':
                        tr.filter('highpass', freq=freq_cut_off, corners=filter_corners)  # 0.078)#i_freq)
                        tr = tr.integrate()
                    #tr.filter('highpass', freq=0.075)
                    tr.filter('lowpass', freq=3)
                    # tr.data[0:int((picks[i] - tr.stats.starttime)*sampling_rate)] = 0
                    alpha = 1-(1/sampling_rate)
                    x = tr.data
                    diff = (tr.differentiate()).data
                    X = np.zeros(len(x))
                    D = np.zeros(len(x))
                    start = int((pick - tr.stats.starttime)*sampling_rate)
                    end = int(start + 4 * sampling_rate)
                    for t in range(0, len(tr.data)):
                        X[t] = alpha*X[t-1]+x[t]**2
                        D[t] = alpha*D[t-1]+diff[t]**2
                    tau_p = 2 * np.pi * np.sqrt(X/D)
                    tau_p_list.append(tau_p)
                    # print(max(tau_p[int(start+0.5*sampling_rate):int(end)]))
                    tp_max.append(max(tau_p[int(start+0.5*sampling_rate):int(end)]))
        self._cached_params["tau_p"] = tau_p_list
        self._cached_params["tau_p_max"] = tp_max

    @property
    def calc_pgv(self):
        data = self.data
        """Absolute peak ground velocity"""
        if "pgv" in self._cached_params:
            return self._cached_params["pgv"]
        else:
            # pgv = util_funcs.calc_peak(data[0].data)
            motion = data[0].data
            pgv = max(abs(min(motion)), max(motion))
            self._cached_params["pgv"] = pgv
            return pgv

    def calc_stalta(self):
        from obspy.signal.trigger import classic_sta_lta
        from datetime import timedelta
        data = self.data
        stalta = self.stalta
        picks = []
        for i in range(0, len(data)):# , 3):  # stations
            k=0
            #for k in range(0, 3):  # components
            tr = data[i+k]
            # cft = classic_sta_lta(trace.data, int(5 * df), int(10 * df))
            # trigger[j][int(i/3)].append([])
            df = tr.stats.sampling_rate
            cft = classic_sta_lta(tr.data, int(1 * df), int(10 * df))
            for j in range(0, len(cft)):
                if cft[j] > 6 and len(stalta) <= (i+k):
                    stalta.append(j)
                    picks.append(time+timedelta(seconds=(j)/df))
        self.stalta = stalta
        if self.picks == []:
            self.picks = picks

    def calc_Tc(self, window_length=4, start_window=0):
        from obspy import UTCDateTime
        picks = self.data_stats['picks']
        data = self.data
        sensor_types = self.data_stats['sensor_types']
        tc_value = []
        count = 0
        #for i_freq in [0.1, 0.075]:  # np.arange(0.001, 0.2, 0.001):
         #   for corners in [1,2,3,4,5]:
                #tc_value.append([])
        for i in range(0, len(data)):
            if data[i].stats.channel[2] == 'Z':
            #acceleration_data = obspy.read("/Users/rebecca/Documents/PhD/Research/Frequency/Tokachi-Oki/data/"+data_files[i]+"/"+data_files[i]+".UD", apply_calib=True)
                tr = data[i]
                station = tr.stats.station
                station = station.ljust(4)
                tr_name = tr.stats.network+'.'+tr.stats.station+'.'+tr.stats.location
                if tr_name in picks.keys():
                    # load saved parameters
                    sampling_rate = tr.stats.sampling_rate
                    pick = UTCDateTime(picks[tr_name])

                    start = int((pick - tr.stats.starttime)*sampling_rate)
                    end = int(start + 3 * sampling_rate)

                    if sensor_types[i]=='acc': # convert acceleration to velocity
                        acc = tr
                        acc.detrend()
                        #acc = data[i].copy()
                        vel = acc.copy()
                        vel = vel.integrate() # V
                    else:
                        vel = tr

                    vel_HP = vel.copy() # V_HP
                    vel_HP.filter('highpass', freq=0.075, corners = 3)
                    displ = vel_HP.copy()
                    displ = displ.integrate() # u
                    vel_for_tc = displ.copy()
                    vel_for_tc = vel_for_tc.differentiate() # u_dot


                    numerator = vel_for_tc[start:end+1] ** 2
                    numerator = np.trapz(numerator) # .integrate()

                    denominator = displ[start:end+1] ** 2
                    denominator = np.trapz(denominator) # .integrate()

                    t_c = (2 * math.pi)/(math.sqrt(numerator/denominator))
                    tc_value.append(t_c)
                    # print(t_c)
        self._cached_params['tau_c'] = tc_value

    def calc_IV2(self, window_length=4, start_window=0):
        from obspy import UTCDateTime
        picks = self.data_stats['picks']
        data = self.data
        sensor_types = self.data_stats['sensor_types']
        IV2 = []
        count = 0
        for i in range(0, len(data)):
            if data[i].stats.channel[2] == 'Z':
                tr = data[i]
                station = tr.stats.station
                station = station.ljust(4)
                tr_name = tr.stats.network+'.'+tr.stats.station+'.'+tr.stats.location
                if tr_name in picks.keys():
                    # load saved parameters
                    sampling_rate = tr.stats.sampling_rate
                    pick = UTCDateTime(picks[tr_name])

                    start = int((pick - tr.stats.starttime)*sampling_rate)
                    end = int(start + 3 * sampling_rate)

                    if sensor_types[i]=='acc': # convert acceleration to velocity
                        acc = tr
                        acc.detrend()
                        #acc = data[i].copy()
                        vel = acc.copy()
                        vel = vel.integrate() # V
                    else:
                        vel = tr

                    vel_HP = vel.copy() # V_HP
                    vel_HP.filter('bandpass', minfreq=0.1, maxfreq = 10, corners = 3)
                    #IV2 = 
                    #IV2.append(t_c)
                    # print(t_c)
        self._cached_params['tau_c'] = tc_value
        
        
        
        
        

    def calc_delaytime(self):
        # data = self.data for OOP
        root = '/home/earthquakes1/homes/Rebecca/phd/data/AK_data_eqtransformer/'
        eq_list = os.listdir(root)
        eq_name = eq_list[0]
        data = obspy.read(root+eq_name+'/data/*/*')
        # sensor_types = self.data_stats['sensor_types'] for automated OOP
        for i in range(0, len(data)):  # iterate through all traces
            if data[i].stats.channel[2] == 'Z':  # only use vertical components
                tr = data[i].copy()
                n_records += 1
                '''if sensor_types[i][0] == 'a':
                    tr.filter('highpass', freq=0.1, corners=3)  # 0.078)#i_freq)
                    tr = tr.integrate()
                    displ = tr.integrate()
                elif sensor_types[i][0] == 'v':'''
                tr.filter('highpass', freq=0.1, corners=3)  # 0.078)#i_freq)
                displ = tr.integrate()
                abs_displ = abs(displ.data) # find absolute of trace
                sum_abs_displ = sum_abs_displ + abs_displ
            '''peaks_x = scipy.signal.find_peaks(abs_displ)[0]
            peaks_y = []
            for peak in peaks_x:
                peaks_y.append(abs_displ[peak])'''
        aad = sum_abs_displ/n_records
