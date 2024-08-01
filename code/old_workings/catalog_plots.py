from obspy import UTCDateTime
import obspy
from obspy.clients.fdsn.mass_downloader import CircularDomain, Restrictions, MassDownloader
from obspy.clients.fdsn import Client
# from func_data_download import download_data

'''clients = ['BGR', 'EMSC', 'ETH', 'GEONET', 'GFZ', 'ICGC', 'INGV', 'IPGP', 'IRIS', 'ISC', 'KNMI', 'KOERI', 'LMU', 'NCEDC', 'NIEP', 'NOA', 'ODC', 'ORFEUS', 'RASPISHAKE', 'RESIF', 'SCEDC', 'TEXNET', 'USGS', 'USP']
fig, axs = plt.subplots(3,3)
count = 0
for c in range(0, len(clients)):
    try:
        print(clients[c])
        client = Client(clients[c])
        dates = ["2019-01-01", "2019-02-01", "2019-03-01", "2019-04-01", "2019-05-01", "2019-06-01", "2019-07-01", "2019-08-01", "2019-09-01", "2019-10-01", "2019-11-01", "2019-12-01"]
        cat = client.get_events(starttime=UTCDateTime(dates[0]), endtime=UTCDateTime(dates[1]), includearrivals=False, minmagnitude=3)
   
        mags = []
        for e in cat:
            mags.append(e.magnitudes[0].mag)
        row = count//3
        column = count%3
        axs[row][column].hist(mags, np.arange(3, 8, 0.1), histtype='step', label = clients[c])
        axs[row][column].set_yscale('log')
        axs[row][column].set_title(clients[c])
        count += 1
    except:
        print('failed')
        continue
'''
clients = ['IRIS', 'ISC']
count = 0


client = Client("IRIS")
dates = ["2019-01-01", "2019-02-01", "2019-03-01", "2019-04-01", "2019-05-01", "2019-06-01", "2019-07-01", "2019-08-01", "2019-09-01", "2019-10-01", "2019-11-01", "2019-12-01"]
cat_IRIS= client.get_events(starttime=UTCDateTime(dates[0]), endtime=UTCDateTime(dates[1]), includearrivals=False, minmagnitude=3)

mags = []
for e in cat_IRIS:
    mags.append(e.magnitudes[0].mag)
plt.hist(mags, np.arange(3, 8, 0.1), histtype='stepfilled', alpha=0.2, label = "IRIS")

client = Client("ISC")
dates = ["2019-01-01", "2019-02-01", "2019-03-01", "2019-04-01", "2019-05-01", "2019-06-01", "2019-07-01", "2019-08-01", "2019-09-01", "2019-10-01", "2019-11-01", "2019-12-01"]
cat_ISC = client.get_events(starttime=UTCDateTime(dates[0]), endtime=UTCDateTime(dates[1]), includearrivals=False, minmagnitude=3)

mags = []
for e in cat_ISC:
    mags.append(e.magnitudes[0].mag)
plt.hist(mags, np.arange(3, 8, 0.1), histtype='stepfilled', alpha=0.2, label = "ISC")

plt.yscale('log')
plt.legend()

cat_sml = cat.filter(magnitude<4)
cat_sml.plot()

client = Client("ISC")
dates = ["2019-01-01", "2019-02-01", "2019-03-01", "2019-04-01", "2019-05-01", "2019-06-01", "2019-07-01", "2019-08-01", "2019-09-01", "2019-10-01", "2019-11-01", "2019-12-01", "2020-01-01"]
cat = client.get_events(starttime=UTCDateTime(dates[0]), endtime=UTCDateTime(dates[1]), includearrivals=True, minmagnitude=3)
print(len(cat))
for d in range(1, len(dates)-1):
    new_cat = client.get_events(starttime=UTCDateTime(dates[d]), endtime=UTCDateTime(dates[d+1]), includearrivals=False, minmagnitude=3)
    print(len(new_cat))
    for event in new_cat:
        cat.append(event)
        
new_cat = client.get_events(starttime=UTCDateTime("2019-12-01"), endtime=UTCDateTime("2020-01-01"), includearrivals=False, minmagnitude=3)
print(len(new_cat))
for event in new_cat:
    cat.append(event)
