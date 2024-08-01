def initbreqfast(lbl='bfreq'):
    """
    :param       lbl:  request label
    :return    fname:  file name that was started
    :return   fnamei:  name of the request label
    """

    # file to write to
    fdir= '/Users/rebecca/Documents/PhD/Research/Frequency/seismo_det/other/test_breqfast'
    fname=datetime.datetime.now().strftime("%Y.%B.%d.%H.%M.%S.%f")
    fnamei='breqfast_'+lbl+'_'+fname

    # NCEDC doesn't like '_' in labels
    fnamei = fnamei.replace('_','.')
    
    fname = os.path.join(fdir,'REQUESTS',fnamei)

    fl = open(fname,'w')
    fl.write('.NAME Rebecca Colquhoun\n')
    fl.write('.INST University of Oxford\n')
    fl.write('.MAIL University of Oxford, Oxford, UK OX1 3AN\n')
    fl.write('.EMAIL rebecca.colquhoun@univ.ox.ac.uk\n')
    fl.write('.PHONE 111 111-1111\n')
    fl.write('.FAX 111 111-1111\n')
    fl.write('.MEDIA: FTP\n')
    fl.write('.LABEL '+fnamei+'\n')
    fl.write('.END\n')
    fl.close()
    
    return fname,fnamei

def sendbreqfast(fname,clnt):
    """
    :param   fname:  file name to send
    :param    clnt:  client to send it to---'IRIS' or 'NCEDC'
    """

    from email.mime.text import MIMEText

    # decide where to send the file
    if clnt in ['IRIS','IPGP']:
        adrs = 'miniseed@iris.washington.edu'
        #adrs = 'DATALESS@iris.washington.edu'
        #adrs = 'breq_fast@iris.washington.edu'
    elif clnt == 'NCEDC':
        adrs = 'breq_fast@ncedc.org'
        #adrs = 'miniseed@ncedc.org'

    # from me
    me = 'rebecca.colquhoun@univ.ox.ac.uk'

    # open file to send
    fp = open(fname,'r')
    msg = MIMEText(fp.read())
    fp.close()

    # send
    msg['Subject'] = 'breqfast request'
    
    # open mail server
    s = smtplib.SMTP('localhost')
    s.sendmail(me,[adrs],msg.as_string())
    s.quit()
    
def addtobreqfast(fname,bulkreq):
    """
    :param    fname:  file name to write to
    :param  bulkreq:  a set of intervals to request,
                as in the bulk requests for obspy
                list of lists, each with 
                [network,station,channel,
                 time 1, time 2]
    """
    
    fl = open(fname,'a')
    for req in bulkreq:
        t1=req[3].strftime("%Y %m %d %H %M %S.00")
        t2=(req[4]).strftime("%Y %m %d %H %M %S.00")
        fl.write(req[1]+' '+req[0]+' '+t1+' '+t2+' 1 '+req[2]+'\n')
    fl.close()
    
def netstatfrominv(inventory):
    """
    :param       inventory:  the inventory of stations
    :return             nw:  list of networks
    :return            sta:  list of stations
    :return            chn:  list of channels
    """

    # initialize
    nw,sta,chn,lln=[],[],[],[]
    
    # go through networks
    for nwi in inventory:
        for sti in nwi:
            for chi in sti:
                sta.append(sti.code)
                nw.append(nwi.code)
                chn.append(chi.code)
                lln.append(chi.location_code)

    return nw,sta,chn,lln


def findstat(t1,t2,stn='*',net='*',chan='*',clnt="IRIS",
             lon=None,lat=None,rad=None):
    """
    :param         t1:   start time
    :param         t2:   end time
    :param        stn:   station to consider (default: all)
    :param        net:   network to consider (default: all)
    :param       chan:   channel to consider (default: all)
    :param        lon:   longitude to center 
    :param        lat:   latitude to center 
    :param        rad:   max radius from location in km
    :param       clnt:   client to request data from (default: IRIS)
    :return        nw:   list of networks
    :return       sta:   list of stations
    :return       chn:   list of channels for each station
    :return inventory:   the inventory retrieved
    """

    # open client to retrieve data
    client=Client(clnt)

    nw,sta,chn=[],[],[]
    try:
        if not rad:
            print('not rad')
            # stations?
            invi=client.get_stations(network=net,station=stn,
                                     starttime=t1,endtime=t2,
                                     channel=chan,level='channel')
        else:
            print('rad')
            # stations?
            invi=client.get_stations(network=net,station=stn,
                                     starttime=t1,endtime=t2,
                                     channel=chan,level='channel',
                                     longitude=lon,latitude=lat,
                                     maxradius=rad/110.)
        # group results
        print('group results')
        nw,sta,chn,lln=netstatfrominv(invi)

    except:
        # create an empty inventory
        print('failed')
        invi=obspy.Inventory([],'T','T')

    return nw,sta,chn,invi

def saveresponse(invi):
    """
    :param       invi:   inventory of values to save
    """
    
    # directory
    sdir = '/Users/rebecca/Documents/PhD/Research/Frequency/seismo_det/other/test_breqfast'

    for nw in invi:
        for st in nw:
            for ch in st:

                # response for this channel
                rsp = ch.response
                
                # directory to save to 
                fdir=os.path.join(sdir,nw.code,st.code,ch.code,
                                  'RESPONSE')
                if not os.path.exists(fdir):
                    os.makedirs(fdir)

                # select a portion of the inventory
                invii=invi.select(network=nw.code,station=st.code,
                                  channel=ch.code)

                # write to the file
                fname=os.path.join(fdir,'inventory.xml')
                invii.write(fname,format='STATIONXML')


for day in range(0, 3):
    fname, fnamei = initbreqfast(lbl=str(day))
    date = datetime.datetime(2019, 1, 1) + datetime.timedelta(days = day)
    day_cat = client.get_events(date, date + datetime.timedelta(days = 1), includearrivals = False, minmagnitude = 3)
    count =0
    bulkreq = []
    for earthquake in day_cat:
        print(count)
        t = earthquake.origins[0].time.datetime
        t1 = t - datetime.timedelta(minutes = 5)
        t2 = t + datetime.timedelta(minutes = 5)
        eq_lat = earthquake.origins[0].latitude
        eq_lon = earthquake.origins[0].longitude
        nw,sta,chn,invi = findstat(t1,t2,stn='*',net='*',chan='*H*',clnt="IRIS", lon=eq_lon,lat=eq_lat,rad=200)
        count += 1
        for n in nw:
            for s in sta:
                for c in chn:
                    bulkreq.append([n, s, c, t1, t2])
        #bulkreq.append([nw, sta, chn, t1, t2])
    addtobreqfast(fname,bulkreq)
    """
    :param    fname:  file name to write to
    :param  bulkreq:  a set of intervals to request,
                as in the bulk requests for obspy
                list of lists, each with
                [network,station,ignored,channel,
                 time 1, time 2]
    """
    #saveresponse(invi)
