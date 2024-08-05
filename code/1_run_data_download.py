from obspy import UTCDateTime
import obspy
from obspy.clients.fdsn import Client
from func_data_download import download_data
import setup_paths as paths

client = Client("IRIS")

root = paths.data_path
print(root)
min_mag = 5
min_year = 2018
max_year = 2018
wanted = f'{str(min_year)}_{str(max_year)}_global_m{str(min_mag)}'

# first, need a catalog of events

try:  # if catalog already exists, just load in
    print('catalog exists')
    cat = obspy.read_events(paths.data_path + wanted + '_catalog.xml')
    print('catalog loaded')
except Exception:  # if catalog doesn't already exist, download it
    print("catalog doesn't exist, make a new one")
    # download new data
    dates = []
    for year in range(min_year, max_year + 1):
        for month in range(1, 12 + 1):
            dates.append(str(year) + "-" + str(month).zfill(2) + "-01")
    cat = client.get_events(starttime=UTCDateTime(dates[0]),
                            endtime=UTCDateTime(dates[1]),
                            includearrivals=True,
                            minmagnitude=min_mag)
    print(len(cat))
    for d in range(1, len(dates) - 1):
        new_cat = client.get_events(starttime=UTCDateTime(dates[d]),
                                    endtime=UTCDateTime(dates[d + 1]),
                                    includearrivals=True,
                                    minmagnitude=min_mag)
        print(len(new_cat))
        for event in new_cat:
            cat.append(event)
    cat.write(paths.data_path + wanted + '_catalog.xml', format="QUAKEML")

print('onto downloading data')
# actually do the downloading
download_data(cat, paths.data_path + wanted + '/')
