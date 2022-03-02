from obspy import UTCDateTime
import obspy
from obspy.clients.fdsn.mass_downloader import CircularDomain, Restrictions, MassDownloader
from obspy.clients.fdsn import Client
from func_data_download import download_data

client = Client("IRIS")

root = "/home/earthquakes1/homes/Rebecca/phd/data/2019_global_m3/"

try: #catalog already exists
    cat = obspy.read_events('/home/earthquakes1/homes/Rebecca/phd/data/2019_global_m3_catalog.xml')
except: # catalog doesn't already exist
    print("catalog doesn't exist, make a new one")
    #download new data
    #cat = client.get_events(starttime=UTCDateTime("2019-01-01"), endtime=UTCDateTime("2020-02-01"), includearrivals=True, minmagnitude=3)
    dates = ["2019-01-01", "2019-02-01", "2019-03-01", "2019-04-01", "2019-05-01", "2019-06-01", "2019-07-01", "2019-08-01", "2019-09-01", "2019-10-01", "2019-11-01", "2019-12-01", "2020-01-01"]
    cat = client.get_events(starttime=UTCDateTime(dates[0]), endtime=UTCDateTime(dates[1]), includearrivals=True, minmagnitude=3)
    print(len(cat))
    for d in range(1, len(dates)-1):
        new_cat = client.get_events(starttime=UTCDateTime(dates[d]), endtime=UTCDateTime(dates[d+1]), includearrivals=True, minmagnitude=3)
        print(len(new_cat))
        for event in new_cat:
            cat.append(event)

    #cat.write('/home/earthquakes1/homes/Rebecca/phd/data/2019_global_m3_catalog.xml', format="QUAKEML") 

print('onto downloading data')
download_data(cat, root)
