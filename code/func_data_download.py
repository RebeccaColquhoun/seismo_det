import util
import os
from obspy.clients.fdsn.mass_downloader import CircularDomain, Restrictions, MassDownloader
from obspy.clients.fdsn import Client

client = Client("IRIS")


def download_data(cat, root="../data/2018_global_m5/"):
    cat_to_do = check_if_done(cat, root)
    for event in cat_to_do:
        origin_time = event.origins[0].time
        eq_name = util.catEventToFileName(event)
        print(eq_name)
        # Circular domain around the epicenter. This will download all data between
        # 70 and 90 degrees distance from the epicenter. This module also offers
        # rectangular and global domains. More complex domains can be defined by
        # inheriting from the Domain class.
        domain = CircularDomain(latitude=event.origins[0].latitude,
                                longitude=event.origins[0].longitude,
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
            minimum_length=0.75,
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

        mdl.download(domain, restrictions,
                     mseed_storage=root + eq_name + "/data/{station}/{network}.{station}.{location}.{channel}__{starttime}__{endtime}.mseed",
                     stationxml_storage=root + eq_name + "/station_xml_files/")


def check_if_done(cat, root="../data/2019_global_m3/"):
    last_event = 0
    for i in range(0, len(cat)):
        event = cat[i]
        fn = util.catEventToFileName(event)
        if os.path.isdir(root + fn):
            last_event = i
    cat_to_do = cat[last_event:]
    return cat_to_do

