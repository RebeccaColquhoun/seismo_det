'''
earthquake class
'''

import math
import os
import pickle
import obspy
import numpy as np
import geopy.distance
from obspy import UTCDateTime

class Earthquake():

    '''
    Class for earthquake calculations

    Args required:
        * name      : Instance Name (corresponding to foldername, e.g. 20120101_102342.a)
        * catalog_object  : Obspy catalog containing 1 event
    '''

    # -------------------------------------------------------------------------------
    # Initialize class #
    def __init__(self, name, catalog_object, root = '/home/earthquakes1/homes/Rebecca/phd/data/2019_global_m3/'):  # data, inventory, picks=None, sensor_types=None):

        '''
        Initialize main variables of the class

        * name -- instance name -- strings
        * catalog object -- obspy catalog with one event in

        '''
        # print('init')
        # Save name
        isinstance(name, str), 'name argument must be a string'
        self.event_stats = dict()
        self.event_stats['name'] = name
        self.event = catalog_object
        self.data_stats = dict()
        self.load(root)
        self.calculated_params = {}
        self.calculation_info = dict()
        self.find_sensor_types()

    def load(self, root):
        """

        loads data and picks and removes response

        Alters self.data, self.inv

        """

        try:
            data = obspy.read(root+self.event_stats['name']+'/data/*/*')
            #print(data)
            with open(root+self.event_stats['name']+'/picks.pkl', 'rb') as file:
                self.data_stats['picks'] = pickle.load(file)
            self.inv = obspy.read_inventory(root+self.event_stats['name']+'/station_xml_files/*')
            data_response_removed = []
            #print(self.data_stats['picks'].keys())
            for trace in data:
                try:
                    tr_name = trace.stats.network+'.'+trace.stats.station+'.'+trace.stats.location
                    #print(trace.stats.sampling_rate)
                    #print(tr_name)
                    if trace.stats.sampling_rate == 100 and tr_name in self.data_stats['picks'].keys():
                        pick = self.data_stats['picks'][tr_name]
                        pick_samples = int(round((UTCDateTime(pick) - trace.stats.starttime)*trace.stats.sampling_rate, 0))
                        snr = max(abs(trace.data[pick_samples:500+pick_samples]))/max(abs(trace.data[pick_samples-700:pick_samples-200]))
                        #print(snr)
                        if snr > 20:
                            data_response_removed.append(trace.remove_response(self.inv))
                            self.data = obspy.Stream(traces = data_response_removed)
                    else:
                        continue#print('in else')
                except Exception:
                    continue
            if len(data_response_removed)==0:
                self.data = False
        except Exception:
            self.data = False

    def eq_info(self):
        """
        extracts info from catalog into event_stats dictionary

        """
        if self.data is not False:
            cat_entry = self.event
            self.event_stats['eq_lat'] = cat_entry.origins[0].latitude
            self.event_stats['eq_long'] = cat_entry.origins[0].longitude
            self.event_stats['eq_depth'] = cat_entry.origins[0].depth
            self.event_stats['eq_mag'] = cat_entry.magnitudes[0].mag
            self.event_stats['eq_mag_type'] = cat_entry.magnitudes[0].magnitude_type

    def find_sensor_types(self):
        """
        saves sensortypes (acc or vel) as data_stats['sensor_types']
        """
        if self.data is not False:
            data = self.data
            sensor_types = []
            for i in range(0, len(self.data)):
                proc = data[i].stats['processing'][0]
                loc = proc.find('output')
                stream = proc[loc+8:loc+11]
                sensor_types.append(stream)
            self.data_stats['sensor_types'] = sensor_types

    def calc_tpmax(self, window_length=4, start_window=0, filter_limits=[0.1,3], filter_corners=3, blank_time = 0.5):
        """


        Parameters
        ----------
        window_length : int, optional
            window over which to calculate max predominant period, defaults to 4
        start_window : int, optional
            time to start calculation, relative to p wave pick. The default is 0.
        filter_limits : [int, int], optional
            DESCRIPTION. The default is [0.1,3]. FIRST VALUE IS FOR HIGHPASS ACC-->VEL, SECOND IS FOR LOWPASS (USED IN ALL)
        filter_corners : int, optional
            Number of corners to use in lowpass filter. The default is 3.

        alters:
            calculated_params["tau_p"] -- list of calculated predominant period for all traces
            calculated_params["tau_p_max"] -- list of max predominant periods (1 value for each trace)

        """

        if self.data is not False:
            data = self.data
            picks = self.data_stats['picks']
            sensor_types = self.data_stats['sensor_types']
            tau_p_list = []
            tp_max = []
            tp_stations = []
            for i in range(0, len(data)):  # iterate through all traces
                if data[i].stats.channel[2] == 'Z':  # only use vertical components
                    trace = data[i].copy()
                    tr_name = trace.stats.network+'.'+trace.stats.station+'.'+trace.stats.location
                    if tr_name in picks.keys():
                        # load saved parameters
                        sampling_rate = trace.stats.sampling_rate
                        pick = UTCDateTime(picks[tr_name])
                        pick_samples = int(round((UTCDateTime(pick) - trace.stats.starttime)*trace.stats.sampling_rate, 0))
                        # preprocess data
                        trace.detrend()
                        if sensor_types[i][0] == 'a':
                            trace.filter('highpass', freq=filter_limits[0], corners=filter_corners)  # 0.078)#i_freq)
                            trace = trace.integrate()
                        trace.filter('highpass', freq=filter_limits[0])
                        trace.filter('lowpass', freq=filter_limits[1])
                        # tr.data[0:int((picks[i] - tr.stats.starttime)*sampling_rate)] = 0
                        alpha = 1-(1/sampling_rate)
                        x = trace.data
                        diff = (trace.differentiate()).data
                        X = np.zeros(len(x))
                        D = np.zeros(len(x))
                        start = int((pick - trace.stats.starttime)*sampling_rate)
                        end = int(start + window_length * sampling_rate)
                        for t in range(0, len(trace.data)):
                            X[t] = alpha*X[t-1]+x[t]**2
                            D[t] = alpha*D[t-1]+diff[t]**2
                        tau_p = 2 * np.pi * np.sqrt(X/D)
                        tau_p_list.append(tau_p)
                        tp_max.append(max(tau_p[int(start+blank_time*sampling_rate):int(end)]))
                        tp_stations.append(tr_name)
            self.calculated_params["tau_p"] = tau_p_list
            self.calculation_info["tau_p_stations"] = tp_stations
            self.calculated_params["tau_p_max"] = tp_max

    def calc_tc(self, window_length=4, start_window=0):
        """


        Parameters
        ----------
        window_length : int, optional
            window over which to calculate max predominant period, defaults to 4
        start_window : int, optional
            time to start calculation, relative to p wave pick. The default is 0.

        ALTERS
        ----
        self.calculated_params['tau_c']

        """
        if self.data is not False:
            picks = self.data_stats['picks']
            data = self.data
            sensor_types = self.data_stats['sensor_types']
            tc_value = []
            tc_stations = []
            count = 0
            for i in range(0, len(data)):
                if data[i].stats.channel[2] == 'Z':
                    trace = data[i].copy()
                    tr_name = trace.stats.network+'.'+trace.stats.station+'.'+trace.stats.location
                    if tr_name in picks.keys():
                        # load saved parameters
                        sampling_rate = trace.stats.sampling_rate
                        pick = UTCDateTime(picks[tr_name])
                        start = int((pick - trace.stats.starttime)*sampling_rate)
                        end = int(start + window_length * sampling_rate)
                        if sensor_types[i][0] == 'acc':  # convert acceleration to velocity
                            acc = trace
                            acc.detrend()
                            vel = acc.copy()
                            vel = vel.integrate()  # V
                        else:
                            vel = trace
                        vel_hp = vel.copy()  # V_HP
                        vel_hp.filter('highpass', freq=0.075, corners=3)
                        displ = vel_hp.copy()
                        displ = displ.integrate()  # u
                        vel_for_tc = displ.copy()
                        vel_for_tc = vel_for_tc.differentiate()  # u_dot

                        numerator = vel_for_tc[start:end+1] ** 2
                        numerator = np.trapz(numerator)  # .integrate()

                        denominator = displ[start:end+1] ** 2
                        denominator = np.trapz(denominator)  # .integrate()

                        t_c = (2 * math.pi)/(math.sqrt(numerator/denominator))
                        tc_value.append(t_c)
                        tc_stations.append(tr_name)
                        # print(t_c)
            self.calculated_params['tau_c'] = tc_value
            self.calculated_params['tau_c_stations'] = tc_stations

    def calc_distance(tr):
        """


        Parameters
        ----------
        tr : TYPE
            DESCRIPTION.

        Returns
        -------
        distance : TYPE
            DESCRIPTION.

        """
        inv = self.inv
        station = tr.stats.station
        station = station.ljust(4)
        sta_lat = inv.select(network=tr.stats.network, station=tr.stats.station)[0][0].latitude
        sta_long = inv.select(network=tr.stats.network, station=tr.stats.station)[0][0].longitude
        distance = np.sqrt(
            (self.event_stats['eq_lat'] - sta_lat)**2 +
            (self.event_stats['eq_long'] - sta_long)**2
            ) * 110
        return distance

    def calc_iv2(self, window_length=4, subtract_bkg=True, filter_limits=[0.075, 10]):
        """


        Parameters
        ----------
        window_length : TYPE, optional
            DESCRIPTION. The default is 4.
        subtract_bkg : TYPE, optional
            DESCRIPTION. The default is True.
        filter_limits : TYPE, optional
            DESCRIPTION. The default is [0.075, 10].

        Returns
        -------
        TYPE
            DESCRIPTION.

        """

        def calc_distance(tr):
            """


            Parameters
            ----------
            tr : obspy trace
                trace object.

            Returns
            -------
            distance : float
                distance from station to earthquake in km.

            """
            inv = self.inv
            station = tr.stats.station
            station = station.ljust(4)
            sta_lat = inv.select(network=tr.stats.network, station=tr.stats.station)[0][0].latitude
            sta_long = inv.select(network=tr.stats.network, station=tr.stats.station)[0][0].longitude
            distance = geopy.distance.distance((self.event_stats['eq_lat'],self.event_stats['eq_long']),(sta_lat,sta_long))
            return distance

        def actual_iv2_calculation(tr, pick, window, bkg):
            """


            Parameters
            ----------
            tr : TYPE
                DESCRIPTION.
            pick : TYPE
                DESCRIPTION.
            window : TYPE
                DESCRIPTION.
            bkg : TYPE
                DESCRIPTION.

            Returns
            -------
            iv2 : TYPE
                DESCRIPTION.

            """
            start = int((pick - tr.stats.starttime)*sampling_rate)
            end = int(start + window * sampling_rate)
            vel = tr.copy()
            v2 = vel.copy()
            if bkg is True:
                bkg = vel.data[int(start-(200+window*100)):int(start-200)] #bkg is window length seconds of velocity counting backwards from 200 samples before the pick
                bkg = bkg**2
                bkg_ave = np.mean(bkg)
            else:
                bkg = 0
            v2.data = (vel.data[start:end]**2)-bkg_ave
            iv2_this = v2.integrate()
            iv2 = iv2_this.data[-1]
            #print(iv2)
            if 1e-15 < abs(iv2) < 10 and iv2 != 0:
                return iv2
            return None

        if self.data is not False:
            list_iv2 = []
            list_iv2_distance = []
            list_iv2_stations = []
            data_interp = self.data.copy()
            data_interp.interpolate(100, 'lanczos', a=20)
            picks = self.data_stats['picks']

            for i in range(0, len(data_interp)):  # iterate through all traces
                tr_name = data_interp[i].stats.network+'.'+data_interp[i].stats.station+'.'+data_interp[i].stats.location
                if data_interp[i].stats.channel[2] == 'Z' and tr_name in picks.keys():  # only use vertical components at stations with a pick
                    trace = data_interp[i].copy()
                    distance = calc_distance(trace)
                    tr_name = trace.stats.network+'.'+trace.stats.station+'.'+trace.stats.location
                    try:
                        pick = UTCDateTime(picks[tr_name])
                        pick_samples = int(round((UTCDateTime(pick) - trace.stats.starttime)*trace.stats.sampling_rate, 0))
                        sampling_rate = trace.stats.sampling_rate
                        if distance < 100:
                            iv2 = actual_iv2_calculation(trace, pick, window_length, subtract_bkg)
                            dist = calc_distance(trace)
                            list_iv2.append(iv2)
                            list_iv2_distance.append(dist)
                            list_iv2_stations.append(tr_name)
                    except Exception:
                        continue
            self.calculated_params['iv2'] = list_iv2
            self.calculated_params['iv2_dist'] = list_iv2_distance
            self.calculation_info['iv2_stations'] = list_iv2_stations


    def calc_pgd(self, window_length = 1):
        def calc_distance(tr):
            """


            Parameters
            ----------
            tr : obspy trace
                trace object.

            Returns
            -------
            distance : float
                distance from station to earthquake in km.

            """
            inv = self.inv
            station = tr.stats.station
            station = station.ljust(4)
            sta_lat = inv.select(network=tr.stats.network, station=tr.stats.station)[0][0].latitude
            sta_long = inv.select(network=tr.stats.network, station=tr.stats.station)[0][0].longitude
            distance = geopy.distance.distance((self.event_stats['eq_lat'],self.event_stats['eq_long']),(sta_lat,sta_long))
            return distance

        def pgd_calculation(timeseries):
            pgd = [abs(timeseries[0])]
            for i in range(1, len(timeseries)):
                pgd.append(max(pgd[-1], abs(timeseries[i])))
            return pgd
        if self.data is not False:
            data = self.data
            sensor_types = self.data_stats['sensor_types']
            picks = self.data_stats['picks']
            """Absolute peak ground displacement"""
            pgd_value = []
            pgd_stations = []
            pgd_distances = []
            for i in range(0, len(data)):  # iterate through all traces
                if data[i].stats.channel[2] == 'Z':  # only use vertical components
                    trace = data[i].copy()
                    station = trace.stats.station
                    tr_name = trace.stats.network+'.'+trace.stats.station+'.'+trace.stats.location
                    if tr_name in picks.keys():
                        # load saved parameters
                        pick = UTCDateTime(picks[tr_name])
                        sampling_rate = trace.stats.sampling_rate
                        pick_samples = int(round((UTCDateTime(pick) - trace.stats.starttime)*sampling_rate, 0))
                        snr = max(abs(trace.data[pick_samples:500+pick_samples]))/max(abs(trace.data[pick_samples-700:pick_samples-200]))
                        if snr > 20:
                            trace.detrend()
                            #print(sensor_types[i][0])
                            if sensor_types[i][0].lower() == 'a':
                                trace.filter('highpass', freq=0.075, corners=4)  # 0.078)#i_freq)
                                vel = trace.integrate()
                                displ = vel.integrate()
                                #print('in if')
                            elif sensor_types[i][0].lower() == 'v':
                                trace.filter('highpass', freq=0.075, corners=4)  # 0.078)#i_freq)
                                displ= trace.integrate()
                                #print('in elif')
                            else:
                                continue
                                #print('in else')
                            pgd_timeseries = pgd_calculation(displ)
                            #print(pick_samples, pick_samples+window_length)
                            pgd_value.append(max(pgd_timeseries[int(pick_samples):int(pick_samples+window_length*sampling_rate)]))
                            pgd_distances.append(calc_distance(trace))
                            pgd_stations.append(tr_name)
                            #print(len(pgd_value), len(pgd_distances), len(pgd_stations))
            self.calculated_params['pgd'] = pgd_value
            self.calculated_params['pgd_distances'] = pgd_distances
            self.calculation_info['pgd_stations'] = pgd_stations




    def calc_delaytime(self):
        """


        Returns
        -------
        aad : TYPE
            DESCRIPTION.

        """
        if self.data is not False:
            data = self.data  # for OOP
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
                    abs_displ = abs(displ.data)  # find absolute of trace
                    sum_abs_displ = sum_abs_displ + abs_displ
                '''peaks_x = scipy.signal.find_peaks(abs_displ)[0]
                peaks_y = []
                for peak in peaks_x:
                    peaks_y.append(abs_displ[peak])'''
            aad = sum_abs_displ/n_records
            return aad
    @property
    def calc_pgv(self):
        """


        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        if self.data is not False:
            data = self.data
            """Absolute peak ground velocity"""
            if "pgv" in self.calculated_params:
                return self.calculated_params["pgv"]
            # pgv = util_funcs.calc_peak(data[0].data)
            motion = data[0].data
            pgv = max(abs(min(motion)), max(motion))
            self.calculated_params["pgv"] = pgv
            return pgv
