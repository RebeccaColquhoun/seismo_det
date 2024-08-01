#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: rebecca
"""
import os
import stationevent_to_json as to_json
from obspy import UTCDateTime
import obspy
from obspy.clients.fdsn.mass_downloader import CircularDomain, Restrictions, MassDownloader
from obspy.clients.fdsn import Client
import csv
import pickle
import json

client = Client("IRIS")

# CHANGE THIS
parent = "/home/earthquakes1/homes/Rebecca/phd/data/AK_data_eqtransformer/"


def download_data(cat):
    for event in cat:
        origin_time = event.origins[0].time
        eq_name = catEventToFileName(event)

        # Circular domain around the epicenter. This will download all data between
        # 0 and 1 degrees distance from the epicenter. This module also offers
        # rectangular and global domains. More complex domains can be defined by
        # inheriting from the Domain class.
        domain = CircularDomain(latitude=event.origins[0].latitude, longitude=event.origins[0].longitude,
                                minradius=0, maxradius=1)

        restrictions = Restrictions(
            # Get data from 5 minutes before the event to 5 minutes after the
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
            # No two stations should be closer than x km to each other. This is
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

        mseed_storage_name = ("/Users/rebecca/Documents/PhD/Research/Frequency/alaska_2020_100_km/mseed/{starttime}/{network}.{station}.{location}.{channel}.mseed")
        mdl.download(domain, restrictions, mseed_storage="/home/earthquakes1/homes/Rebecca/phd/data/AK_data_eqtransformer/"+eq_name+"/data/{station}/{network}.{station}.{location}.{channel}__{starttime}__{endtime}.mseed",
                     stationxml_storage="/home/earthquakes1/homes/Rebecca/phd/data/AK_data_eqtransformer/"+eq_name+"/station_xml_files/")


def use_eq_transformer(eq_name):
    '''
    do the eqt stuff
    :param eq_name: earthquake folder name e.g. yyyymmdd_hhmmss
    :type eq_name: string
    '''
    from EQTransformer.utils.hdf5_maker import preprocessor
    from EQTransformer.core.predictor import predictor
    # move into the earthquake folder
    os.chdir(parent+eq_name)
    # tell it where the json is saved
    json_basepath = parent+eq_name+"/json/station_list.json"
    # do preprocessing. data is stored in the data file, preprocessed things end up in preproc (it makes that folder) and hdf5s end up in data_processed_hdfs
    preprocessor(preproc_dir="preproc", mseed_dir='data', stations_json=json_basepath, overlap=0, n_processor=4)
    # do the detecting (output in detections), set model location 
    predictor(input_dir='data_processed_hdfs', input_model='/home/earthquakes1/homes/Rebecca/EQTransformer/ModelsAndSampleData/EqT_model.h5', output_dir='detections', detection_threshold=0.3, P_threshold=0.1, S_threshold=0.1, number_of_plots=100, plot_mode='time')
    # plot_data_chart('time_tracks.pkl', time_interval=10)


def catEventToFileName(catalogEntry):
    '''
    :param catalogEntry: one event in catalog
    :type catalogEntry: catalog entry
    :return fileName: yyyymmdd_hhmmss
    :rtype: string
    '''
    year = str(catalogEntry.origins[0].time.year).zfill(4)
    month = str(catalogEntry.origins[0].time.month).zfill(2)
    day = str(catalogEntry.origins[0].time.day).zfill(2)
    hour = str(catalogEntry.origins[0].time.hour).zfill(2)
    minute = str(catalogEntry.origins[0].time.minute).zfill(2)
    second = str(catalogEntry.origins[0].time.second).zfill(2)
    fileName = year+month+day+'_'+hour+minute+second
    return fileName


def inv_to_dict(eq_name, parent):
    '''
    :param eq_name: earthquake folder name e.g. yyyymmdd_hhmmss
    :type eq_name: string
    :param parent: path to parent of data file, e.g. '/home/earthquakes1/homes/Rebecca/phd/data/AK_data_eqtransformer/'
    :type parent: string, optional
    :return dictionary: dictionary of stations and their details
    :rtype: TYPE
    '''
    dictionary = {}
    files = os.listdir(parent+eq_name+"/station_xml_files")
    for station in files:
        inv = obspy.read_inventory(parent+eq_name+"/station_xml_files/"+station)
        station_name = inv[0][0].code
        if station_name in dictionary:  # 1 component at this station has already been added
            channels = dictionary[station_name]["channels"]
            for cha in inv[0][0]:
                channels.append(cha.code)
            dictionary[station_name]["channels"] = channels
        else:
            sta_dict = {}
            sta_dict["network"] = inv[0].code
            channels = []
            for cha in inv[0][0]:
                channels.append(cha.code)
            sta_dict["channels"] = channels
            sta_dict["coords"] = [inv[0][0].latitude, inv[0][0].longitude,  inv[0][0].elevation]
            dictionary[station_name] = sta_dict
    return dictionary


def save_as_json(eq_name, parent):
    '''
    :param eq_name: earthquake folder name e.g. yyyymmdd_hhmmss
    :type eq_name: string
    :param parent: parent path, e.g. '/home/earthquakes1/homes/Rebecca/phd/data/AK_data_eqtransformer/'
    :type parent: string
    '''
    # convert inventory (loaded from XML files within function) to dictionary ready for saving as a json
    dictionary = inv_to_dict(eq_name, parent)
    # see if folder called json exists in this earthquakes folder and if not make it
    if not os.path.exists(parent+eq_name+"/json/"):
        os.makedirs(parent+eq_name+"/json/")
    # save json file
    with open(parent+eq_name+"/json/station_list.json", 'w') as fp:
        json.dump(dictionary, fp)


# make a catalog of alaskan earthquakes. replace with making/loading your own catalog
cat = client.get_events(starttime=UTCDateTime("2019-06-26"), endtime=UTCDateTime("2020-06-26"), minlongitude=-179, maxlongitude=-145, minlatitude=42, maxlatitude=71, minmagnitude=5, includearrivals=True)

# downloads the data, obviously don't need this if you have already got your data
download_data(cat)

# make a list of earthquakes in the catalog which have data available
eq_with_data = []
for event in cat:
    eq_name = catEventToFileName(event)
    if os.path.isdir(parent+eq_name):  # if the earthquake doesnt have any available data, this folder isn't made
        eq_with_data.append(eq_name)

# make the json file for each earthquake with data
for eq_name in eq_with_data:
    to_json.save_as_json(eq_name, parent)

# do the EQT bit!
for eq_name in eq_with_data:
    use_eq_transformer(eq_name)

# OPTIONAL. this takes the X_prediction_results files and saves a pickled file with a dictionary of stations and picks for every earthquake.
for eq_name in eq_with_data:
    picks = {}
    stations = os.listdir(parent+eq_name+'/detections/')
    for sta in stations:
        with open(parent+eq_name+'/detections/'+sta+'/X_prediction_results.csv') as f:
            reader = csv.reader(f)
            pred_results = list(reader)
            if len(pred_results) > 1:  # the first line of the X_prediction_results file is the header, so if there are any detections length>1
                picks[pred_results[1][2]] = pred_results[1][11]
    with open(parent+'/'+eq_name+'/picks.pkl', 'wb') as f:
        pickle.dump(picks, f, pickle.HIGHEST_PROTOCOL)
