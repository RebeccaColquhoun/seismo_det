#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 15:58:57 2021

@author: rebecca
"""
from memory_profiler import profile
import psutil
import gc
import util
import os
import stationevent_to_json as to_json
import numpy as np
from obspy import UTCDateTime
import obspy
from obspy.clients.fdsn.mass_downloader import CircularDomain, Restrictions, MassDownloader
from obspy.clients.fdsn import Client
import csv
import pickle

client = Client("IRIS")

root = "/home/earthquakes1/homes/Rebecca/phd/data/2019_global_m5/"


def download_data(cat):
    for event in cat:
        origin_time = event.origins[0].time
        eq_name = util.catEventToFileName(event)

        # Circular domain around the epicenter. This will download all data between
        # 70 and 90 degrees distance from the epicenter. This module also offers
        # rectangular and global domains. More complex domains can be defined by
        # inheriting from the Domain class.
        domain = CircularDomain(latitude=event.origins[0].latitude, longitude=event.origins[0].longitude,
                                minradius=0, maxradius=1)

        restrictions = Restrictions(
            # Get data from 5 minutes before the event to half an hour after the
            # event. This defines the temporal bounds of the waveform data.
            starttime=origin_time - 5 * 60,
            endtime=origin_time + 5 * 60,
            # You might not want to deal with gaps in the data. If this setting is
            # True, any trace with a gap/overlap will be discarded.
            reject_channels_with_gaps=True,
            # And you might only want waveforms that have data for at least 95 % of
            # the requested time span. Any trace that is shorter than 95 % of the
            # desired total duration will be discarded.
            minimum_length=0.95,
            # No two stations should be closer than 1 km to each other. This is
            # useful to for example filter out stations that are part of different
            # networks but at the same physical station. Settings this option to
            # zero or None will disable that filtering.
            minimum_interstation_distance_in_m=0,  # 10E3,
            # Only HH or BH channels. If a station has HH channels, those will be
            # downloaded, otherwise the BH. Nothing will be downloaded if it has
            # neither. You can add more/less patterns if you like.
            channel_priorities=["HH[ZNE12]", "BH[ZNE12]"],
            # Location codes are arbitrary and there is no rule as to which
            # location is best. Same logic as for the previous setting.
            location_priorities=["", "00", "10"])

        # No specified providers will result in all known ones being queried.
        mdl = MassDownloader()
        # The data will be downloaded to the ``./waveforms/`` and ``./stations/``
        # folders with automatically chosen file names.

        mdl.download(domain, restrictions, mseed_storage=root+eq_name+"/data/{station}/{network}.{station}.{location}.{channel}__{starttime}__{endtime}.mseed",
                     stationxml_storage=root+eq_name+"/station_xml_files/")


def use_eq_transformer(eq_name):
    from EQTransformer.utils.hdf5_maker import preprocessor
    from EQTransformer.core.predictor import predictor
    from EQTransformer.utils.plot import plot_data_chart
    os.chdir(root+eq_name)
    json_basepath = root+eq_name+"/json/station_list.json"
    preprocessor(preproc_dir="preproc", mseed_dir='data', stations_json=json_basepath, overlap=0, n_processor=4)
    predictor(input_dir='data_processed_hdfs', input_model='/home/earthquakes1/homes/Rebecca/EQTransformer/ModelsAndSampleData/EqT_model.h5', output_dir='detections', detection_threshold=0.3, P_threshold=0.1, S_threshold=0.1, number_of_plots=100, plot_mode='time')
    # plot_data_chart('time_tracks.pkl', time_interval=10)

def save_obj(obj, eq_name):
    with open(root+'/'+eq_name+'/picks.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(eq_name):
    with open(root+'/'+eq_name+'/picks.pkl', 'rb') as f:
        return pickle.load(f)


#@profile
def run():
    # cat = client.get_events(starttime=UTCDateTime("2019-01-01"), endtime=UTCDateTime("2020-01-01"), includearrivals=True, minmagnitude=5) #, minlongitude=-179, maxlongitude=-145, minlatitude=42, maxlatitude=71)
    cat = obspy.read_events('/home/earthquakes1/homes/Rebecca/phd/data/2019_global_m5_catalog.xml')
    # download_data(cat)
    
    eq_with_data = []
    for event in cat:
        eq_name = util.catEventToFileName(event)
        if os.path.isdir(root+eq_name) and os.path.isdir(root+eq_name+'/station_xml_files'):
            eq_with_data.append(eq_name)
            
    data = []
    xml = []
    for event in cat:
        eq_name = util.catEventToFileName(event)
        if os.path.isdir(root+eq_name):
            data.append(eq_name)
        if os.path.isdir(root+eq_name+'/station_xml_files'):
            xml.append(eq_name)
    
    # for eq_name in eq_with_data:
    #    dictionary = to_json.inv_to_dict(eq_name, root)
    #    to_json.save_as_json(dictionary, eq_name, root)
    
    eq_processed = []
    for eq_name in eq_with_data:
        if os.path.isdir(root+eq_name+"/data_processed_hdfs") and os.path.isdir(root+eq_name+"/detections"):
            eq_processed.append(eq_name)
    
    count = 0
    failed = []
    for eq_name in eq_with_data:
        if eq_name not in eq_processed:
            if count < 7:
                try:
                    #use_eq_transformer(eq_name)
                    from EQTransformer.utils.hdf5_maker import preprocessor
                    from EQTransformer.core.predictor import predictor
                    from EQTransformer.utils.plot import plot_data_chart
                    os.chdir(root+eq_name)
                    json_basepath = root+eq_name+"/json/station_list.json"
                    preprocessor(preproc_dir="preproc", mseed_dir='data', stations_json=json_basepath, overlap=0, n_processor=4)
                    predictor(input_dir='data_processed_hdfs', input_model='/home/earthquakes1/homes/Rebecca/EQTransformer/ModelsAndSampleData/EqT_model.h5', output_dir='detections', detection_threshold=0.3, P_threshold=0.1, S_threshold=0.1, number_of_plots=100, plot_mode='time')
                    eq_processed.append(eq_name)
                    #print(psutil.swap_memory())
                    print(psutil.virtual_memory().percent)
                    count += 1
                    gc.collect()
                    print(psutil.virtual_memory().percent)
                except:
                    failed.append(eq_name)
            
    
# =============================================================================
#     for eq_name in eq_with_data:
#         picks = {}
#         stations = os.listdir(root+eq_name+'/detections/')
#         for sta in stations:
#             with open(root+eq_name+'/detections/'+sta+'/X_prediction_results.csv') as f:
#                 reader = csv.reader(f)
#                 pred_results = list(reader)
#                 if len(pred_results)>1:
#                     picks[pred_results[1][2]]=pred_results[1][11]
#         save_obj(picks, eq_name)
# =============================================================================

if __name__ == '__main__':
    run()