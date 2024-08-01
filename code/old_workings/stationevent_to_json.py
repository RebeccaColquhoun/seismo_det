'''functions to go from stationevent file (created by obspyDMT) to json (for use with EQtransformer)'''
import json
import os
import obspy

def load_stationevent(event="20191018_130859.a"):
    '''
    split stationevent file into nested lists (one inner list for each eq)

    :param event: event name as a string ("yearmonthday_hourminutesecond.a"), defaults to "20191018_130859.a"
    :type event: STRING
    :return: split_lists, nested lists (one inner list for each eq)
    :rtype: LIST

    '''
    f = open("/Users/rebecca/Documents/PhD/Research/Frequency/AK_data_2019_2020/"+event+"/info/station_event", 'r')
    list_of_stations = f.read().splitlines()
    split_lists = []
    for i in range(0, len(list_of_stations)):
        split_lists.append(list_of_stations[i].split(","))
    return split_lists


def make_dicts(list_to_use):
    '''

    :param list_to_use: nested list (created by load_stationevent), one inner list for each eq
    :type list_to_use: LIST
    :return: dictionary, nested dictionary of events and info
    :rtype: DICT

    '''
    dictionary = {}
    for list_single_channel in list_to_use:
        station_name = list_single_channel[1]
        if station_name in dictionary:  # 1 component at this station has already been added
            channels = dictionary[station_name]["channels"]
            channels.append(list_single_channel[3])
            dictionary[station_name]["channels"] = channels
        else:
            sta_dict = {}
            sta_dict["network"] = list_single_channel[0]
            sta_dict["channels"] = [list_single_channel[3]]
            sta_dict["coords"] = [list_single_channel[4], list_single_channel[5], list_single_channel[6]]
            dictionary[station_name] = sta_dict
    return dictionary


def inv_to_dict(eq_name, root = '/home/earthquakes1/homes/Rebecca/phd/data/AK_data_eqtransformer/'):
    '''
    
    :param eq_name: DESCRIPTION
    :type eq_name: string
    :param root: path to parent of data file, defaults to '/home/earthquakes1/homes/Rebecca/phd/data/AK_data_eqtransformer/'
    :type root: TYPE, optional
    :return: DESCRIPTION
    :rtype: TYPE

    '''
    dictionary = {}
    files = os.listdir(root+eq_name+"/station_xml_files")
    for station in files:
        inv = obspy.read_inventory(root+eq_name+"/station_xml_files/"+station)
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


def save_as_json(dictionary, eq_name, root='/home/earthquakes1/homes/Rebecca/phd/data/AK_data_eqtransformer/'):
    if not os.path.exists(root+eq_name+"/json/"):
        os.makedirs(root+eq_name+"/json/")
    with open(root+eq_name+"/json/station_list.json", 'w') as fp:
        json.dump(dictionary, fp)
