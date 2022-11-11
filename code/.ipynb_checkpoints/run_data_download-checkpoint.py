from obspy import UTCDateTime
import obspy
from obspy.clients.fdsn.mass_downloader import CircularDomain, Restrictions, MassDownloader
from obspy.clients.fdsn import Client
from func_data_download import download_data

client = Client("IRIS")

wanted = '2019_global_m3'
root = "/home/earthquakes1/homes/Rebecca/phd/data/"
min_mag = 5
min_year = 2005
max_year = 2018

try: #catalog already exists
    cat = obspy.read_events('/home/earthquakes1/homes/Rebecca/phd/data/'+wanted+'catalog.xml')
except: # catalog doesn't already exist
    print("catalog doesn't exist, make a new one")
    #download new data
    dates = []
    for year in range(min_year, max_year+1):
        for month in range(1, 12+1):
            dates.append(str(year)+"-"+str(month).zfill(2)+"-01")
    cat = client.get_events(starttime=UTCDateTime(dates[0]), endtime=UTCDateTime(dates[1]), includearrivals=True, minmagnitude=min_mag)
    print(len(cat))
    for d in range(1, len(dates)-1):
        new_cat = client.get_events(starttime=UTCDateTime(dates[d]), endtime=UTCDateTime(dates[d+1]), includearrivals=True, minmagnitude=min_mag)
        print(len(new_cat))
        for event in new_cat:
            cat.append(event)
	cat.write('/home/earthquakes1/homes/Rebecca/phd/data/'+wanted+'_catalog.xml', format="QUAKEML") 

print('onto downloading data')
download_data(cat, root+wanted)
