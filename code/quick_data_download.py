def initbreqfast(lbl='bfreq'):
    """
    :param       lbl:  request label
    :return    fname:  file name that was started
    :return   fnamei:  name of the request label
    """

    # file to write to
    fdir=os.environ['SDATA']
    fname=datetime.datetime.now().strftime("%Y.%B.%d.%H.%M.%S.%f")
    fnamei='breqfast_'+lbl+'_'+fname

    # NCEDC doesn't like '_' in labels
    fnamei = fnamei.replace('_','.')
    
    fname = os.path.join(fdir,'REQUESTS',fnamei)

    fl = open(fname,'w')
    fl.write('.NAME Jessica Hawthorne\n')
    fl.write('.INST University of Oxford\n')
    fl.write('.MAIL University of Oxford, Oxford, UK OX1 3AN\n')
    fl.write('.EMAIL jessica.hawthorne@earth.ox.ac.uk\n')
    fl.write('.PHONE 609 858-3784\n')
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
    me = 'jessica.hawthorne@earth.ox.ac.uk'

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
                [network,station,ignored,channel,
                 time 1, time 2]
    """
    
    fl = open(fname,'a')
    for req in bulkreq:
        t1=req[4].strftime("%Y %m %d %H %M %S.00")
        t2=(req[5]+1).strftime("%Y %m %d %H %M %S.00")
        fl.write(req[1]+' '+req[0]+' '+t1+' '+t2+' 1 '+req[3]+'\n')
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
            chn.append([])
            lln.append([])
            sta.append(sti.code)
            nw.append(nwi.code)
            for chi in sti:
                chn[-1].append(chi.code)
                lln[-1].append(chi.location_code)

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
            # stations?
            invi=client.get_stations(network=net,station=stn,
                                     starttime=t1,endtime=t2,
                                     channel=chan,level='channel')
        else:
            # stations?
            invi=client.get_stations(network=net,station=stn,
                                     starttime=t1,endtime=t2,
                                     channel=chan,level='channel',
                                     longitude=lon,latitude=lat,
                                     maxradius=rad/110.)
        # group results
        nw,sta,chn,lln=netstatfrominv(invi)

    except:
        # create an empty inventory
        invi=obspy.Inventory([],'T','T')

    return nw,sta,chn,invi

def saveresponse(invi):
    """
    :param       invi:   inventory of values to save
    """
    
    # directory
    sdir = os.environ['SDATA']

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
