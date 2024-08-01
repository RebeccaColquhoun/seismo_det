import obspy
import smtplib
import os,shutil
import copy
import datetime
import numpy as np
import waveformdb
from obspy.clients.fdsn import Client
from waveformtable import Waveform

def findneeded(session,t1,t2,stn=None,net=None,chan=None,bfr=0.,
               nsc=None,bfrd=0.):
    """
    :param    session:   handle to database or database name
    :param         t1:   start time
    :param         t2:   end time
    :param        stn:   station to consider (default: all)
    :param        net:   network to consider (default: all)
    :param       chan:   channel to consider (default: all)
    :param        bfr:   space to allow between segments
    :param        nsc:   list of networks,stations,channels 
                            overrides stn,net,chan if given
    :param       bfrd:   time buffer for selection---usually time spacing
    :return      dtsa:   list of arrays with dates
    :return       nsc:   list of networks,stations,channels 
    """

    # open database
    sessioni = session
    if isinstance(session,str):
        session=waveformdb.opendatabase(session)

    # query for relevant waveforms
    q=session.query(Waveform).yield_per(50)

    # close the database if it was open
    if isinstance(sessioni,str):
        session.close()

    # first filter by time
    q=q.filter(Waveform.starttime<=t2.timestamp)
    q=q.filter(Waveform.endtime>=t1.timestamp)

    # networks, stations, etc
    if nsc is None:
        nsc,trash,trash,trash=collectnsc(net,stn,chan)

    print('Filtering data')
    # just these networks, stations, channels
    vli=np.unique(np.array([vl[0] for vl in nsc]))
    q=q.filter(Waveform.net.in_(vli))
    vli=np.unique(np.array([vl[1] for vl in nsc]))
    q=q.filter(Waveform.sta.in_(vli))
    vli=np.unique(np.array([vl[2] for vl in nsc]))
    q=q.filter(Waveform.chan.in_(vli))

    # collect the values I care about
    vls = [[wv.net,wv.sta,wv.chan,wv.starttime,wv.endtime] for wv in q]
    nsch = np.array([vl[0:3] for vl in vls])
    tlmh = np.array([vl[3:5] for vl in vls])
    nsch = nsch.reshape([int(nsch.size/3),3])
    tlmh = tlmh.reshape([int(tlmh.size/2),2])

    # for all the times
    dtsa = []

    # repeat buffer time as necessary
    bfrd = np.atleast_1d(bfrd)
    bfrd = np.repeat(bfrd,int(np.ceil(len(nsc)/len(bfrd))))

    print('Gathering times')
    for k in range(0,len(nsc)):
        nsci = nsc[k]

        # with the right channels
        ii = np.logical_and(np.in1d(nsch[:,0],nsci[0:1]),
                            np.in1d(nsch[:,1],nsci[1:2]))
        ii = np.logical_and(ii,np.in1d(nsch[:,2],nsci[2:3]))
        ii, = np.where(ii)

        # # filter
        # qq=q.filter(Waveform.net==nsci[0])
        # qq=qq.filter(Waveform.sta==nsci[1])
        # qq=qq.filter(Waveform.chan==nsci[2])

        # print('Making list')
        # # create a list of what we have
        # tms = [[wv.starttime, wv.endtime] for wv in qq]
        # tms = np.array(tms)

        tms = tlmh[ii,:]
        tms = np.atleast_2d(tms)

        if tms.size:
            # min and max
            tms[:,0] = np.maximum(tms[:,0],t1.timestamp)
            tms[:,1] = np.minimum(tms[:,1],t2.timestamp)


            # sort and delete overlaps
            tms = sortintosegs(tms,bfr=bfr)
        
            # and then just get the portions with no data
            tms = [np.append(np.array(t1.timestamp),tms[:,1]),
                  np.append(tms[:,0],np.array(t2.timestamp))]
            tms = np.vstack(tms).transpose()

        else:
            # no data
            tms = np.array([t1,t2]).reshape([1,2])

        # and delete any repetition
        tms = sortintosegs(tms,bfr=bfrd[k])
        tms = noshortsegs(tms,bfr=bfrd[k])

        # create as dates
        dts = [obspy.UTCDateTime(tm) for tm in tms.flatten()]
        dts = np.array(dts).reshape(tms.shape)
        dts = np.atleast_2d(dts)

        # add for this channel
        dtsa.append(dts)

    return dtsa,nsc

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

def initautodrm(lbl='adrm'):
    """
    :param       lbl:  request label
    :return    fname:  file name that was started
    :return   fnamei:  name of the request label
    """

    # file to write to
    fdir=os.environ['SDATA']
    fname=datetime.datetime.now().strftime("%Y.%B.%d.%H.%M.%S.%f")
    fnamei='autodrm_'+lbl+'_'+fname

    # NCEDC doesn't like '_' in labels
    fnamei = fnamei.replace('_','.')
    
    fname = os.path.join(fdir,'REQUESTS',fnamei)

    fl = open(fname,'w')
    fl.write('BEGIN\n')
    fl.write('EMAIL jessica.hawthorne@earth.ox.ac.uk\n')
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

    
    
def sortintosegs(vls,bfr=0.):
    """
    :param    vls:   ? x 2 set of values
           to sort and delete overlaps
    :param    bfr:   how  much time to allow between segments
    :return   vls:   vls, but sorted and with overlaps deleted
    """

    # sort
    ixi = np.argsort(vls[:,0])
    vls = vls[ixi,:]
    vls = np.atleast_2d(vls)

    # identify overlaps
    ii, = np.where(vls[1:,0]<=vls[:-1,1]+bfr)
    while len(ii):
        # just one at a time
        ii = ii[0]
        vls[ii,1] = vls[ii+1,1]
        vls = np.delete(vls,ii+1,axis=0)
        
        # identify overlaps again
        ii, = np.where(vls[1:,0]<=vls[:-1,1]+bfr)

    return vls


def noshortsegs(vls,bfr=0.):
    """
    :param    vls:   ? x 2 set of values
           to sort and delete overlaps
    :param    bfr:   how  much time to allow between segments
    :return   vls:   vls, but sorted and with overlaps deleted
    """

    # sort
    ixi = np.argsort(vls[:,0])
    vls = vls[ixi,:]
    vls = np.atleast_2d(vls)

    # identify intervals with no time in them
    ii, = np.where(vls[:,1]<=vls[:,0]+bfr)
    while len(ii):
        vls = np.delete(vls,ii[0],axis=0)
        ii, = np.where(vls[:,1]<=vls[:,0]+bfr)

    return vls

def updatepbostrain(t1=None,t2=None,stn=None,usebf=True,sendreq=False):
    """
    :param         t1:   start time
    :param         t2:   end time
    :param        stn:   stations to consider (default: all)
    :param      usebf:   use breqfast for the request
    :param    sendreq:   actually send the request
    """

    # strain database
    datab = 'pbostrain'

    # network and components
    net = 'PB'
    # atm pressure, rainfall, pore pressure, T at pore pressure
    chan = ['RDO','RRO','RDD','RKD']
    chan = ['RDO']
    chan = ['RS1','RS2','RS3','RS4']+chan
    #chan = chan+['BS1','BS2','BS3','BS4']
    #chan = ['BS1','BS2','BS3','BS4']
    #chan = ['LS1','LS2','LS3','LS4']
    #chan = ['EH1','EH2','EHZ']
    if isinstance(stn,str):
        stn = [stn]
    # how much spacing to allow in seconds
    bfr = 1000.

    # default time ranges
    if t1 is None:
        t1=obspy.UTCDateTime(2007,1,1)
    if t2 is None:
        t2=obspy.UTCDateTime(datetime.datetime.now())
    
    # request and add to database
    if usebf:
        if ('BS1' in chan) or ('LS1' in chan):
            for sta in stn:
                bfreqdata(datab='pbostrain',t1=t1,t2=t2,stn=sta,
                          net=net,chan=chan,bfr=10.,clnt="IRIS",
                          sendreq=sendreq)
        else:
            bfreqdata(datab='pbostrain',t1=t1,t2=t2,stn=stn,
                      net=net,chan=chan,bfr=10.,clnt="IRIS",
                      sendreq=sendreq)

    else:
        for sta in stn:
            for ch in chan:
                print(sta+'.'+ch)
                reqdata(datab=datab,t1=t1,t2=t2,stn=sta,
                        net=net,chan=ch,bfr=bfr)



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

def getandsaveresponse(t1=None,t2=None,stn='*',net='*',
                       chan='*',clnt=None):
    """
    :param         t1:   start time
    :param         t2:   end time
    :param        stn:   station to consider (default: all)
                          can be 'byletter' to split by first letter
    :param        net:   network to consider (default: all)
    :param       chan:   channel to consider (default: all)
    :param       clnt:   client to request data from 
                           (default: based on network)
    """

    # split by the starting letter so that everything isn't done at once
    if stn == 'byletter':
        stn='ABCDEFGHIJKLMNOPRSTUVWXYZ'
        stn=[stni+'*' for stni in stn]
    

    if isinstance(stn,str):
        print('stations '+stn)
        try:
            # get the inventories
            invi=getresponse(t1=t1,t2=t2,stn=stn,net=net,chan=chan,
                             clnt=clnt)
            
            # write them
            saveresponse(invi)
        except:
            print('Request failed: possibly no data')
    else:
        for stni in stn:
            getandsaveresponse(t1=t1,t2=t2,stn=stni,net=net,
                               chan=chan,clnt=clnt)    

def getresponse(t1=None,t2=None,stn='*',net='*',chan='*',clnt=None):
    """
    :param         t1:   start time
    :param         t2:   end time
    :param        stn:   station to consider (default: all)
    :param        net:   network to consider (default: all)
    :param       chan:   channel to consider (default: all)
    :param       clnt:   client to request data from 
                           (default: based on network)
    
    """

    if t1 is None:
        t1 = obspy.UTCDateTime(1970,1,1)
    if t2 is None:
        t2 = obspy.UTCDateTime(datetime.datetime.now())
    if clnt is None:
        if net in ['BK','NC','BP']:
            clnt = 'NCEDC'
        elif net in ['CI','AZ']:
            clnt = 'SCEDC'
        else:
            clnt = 'IRIS'

    # open client to retrieve data
    client=Client(clnt)

    print(client)
    # stations?
    invi=client.get_stations(network=net,station=stn,
                             starttime=t1,endtime=t2,
                             channel=chan,level='response')
    print(invi)

    return invi

def getmarsdata(t1=None,t2=None,getresp=False):
    """
    :param        t1: beginning of time range
    :param        t2: end of time range
    :param   getresp: also download the response information
    """

    if t1 is None:
        t1=obspy.UTCDateTime(2018,11,30)
    if t2 is None:
        t2=t1+180.

    # network and client
    net='XB'
    clnt='IPGP'

    # data from final configuration
    stn='ELYSE'

    # 20 Hz velocity and pressure data
    chns=['BHW','BHV','BHU','BDO']

    # look through existing database and request the rest
    # reqdata(datab='mars',t1=t1,t2=t2,stn=stn,net=net,chan=chns,
    #         bfr=10.,clnt=clnt,breqfast=False)

    # go ahead and replace the response files,
    # as they seem to be updated frequently
    if getresp:
        t1=obspy.UTCDateTime(2019,1,1)
        t2=obspy.UTCDateTime(datetime.datetime.now())
        getandsaveresponse(t1=t1,t2=t2,stn=stn,net=net,chan='*',clnt=clnt)

def getparkfielddata(teq,usebf=True,sendreq=False,cmp=['S','B'],
                     trange=[-60,60],t1=None,t2=None):
    """
    :param       teq:  earthquake time or list of times
    :param     usebf:  use the breqfast request system
    :param   sendreq:  send the breqfast request?
    :param       cmp:  which component of HRSN 'S' (20 Hz) or 'D' (250 Hz)
    :param    trange:  time range relative to teq in seconds (default: [-60,60])
    :param        t1:  start time of interval to grab (overrides teq)
    :param        t2:  end time of interval to grab (overrides teq)
    """

    teq = np.atleast_1d(teq)
    trange = np.atleast_1d(trange)

    if t1 is None or t2 is None:
        # time range relative to earthquakes
        t1 = teq+trange[0]
        t2 = teq+trange[1]
    else:
        # the specified times are the time ranges
        t1,t2=np.atleast_1d(t1),np.atleast_1d(t2)
    print(t1)
    print(t2)


    # relative to a reference time
    tref = t1[0]

    # redefine groups as necessary, to avoid overlapping requests
    tlm = np.vstack([t1-tref,t2-tref]).transpose()
    tlm = sortintosegs(tlm)
    t1 = np.array([tref+tm for tm in tlm[:,0]])
    t2 = np.array([tref+tm for tm in tlm[:,1]])

    # time range to look for stations
    tmin=np.min(t1)
    tmax=np.max(t2)

    import pksdrops
    refloc = pksdrops.refloc()

    # for NCEDC request

    # create an empty inventory
    inventory=obspy.Inventory([],'T','T')

    #------------------BP stations-------------------------------------

    # find relevant stations
    for cmpi in cmp:
        nw,stn,chn,inventoryi=\
           findstat(tmin,tmax,stn='*',net='BP',chan=cmpi+'P*',
                    clnt="NCEDC",lon=refloc[0],lat=refloc[1],
                    rad=50.)
        inventory = inventory + inventoryi

    #------------------NC stations-------------------------------------

    print('no NC stations')

    # # find relevant stations
    # nw,stn,chn,inventoryi=\
    #     findstat(tmin,tmax,stn='*',net='NC',chan='*N*',
    #              clnt="NCEDC",lon=refloc[0],
    #              lat=refloc[1],rad=100.)
    # inventory = inventory + inventoryi

    # nw,stn,chn,inventoryi=\
    #     findstat(tmin,tmax,stn='*',net='NC',chan='EH*',
    #              clnt="NCEDC",lon=refloc[0],
    #              lat=refloc[1],rad=100.)
    # inventory = inventory + inventoryi

    # nw,stn,chn,inventoryi=\
    #     findstat(tmin,tmax,stn='*',net='NC',chan='HH*',
    #              clnt="NCEDC",lon=refloc[0],
    #              lat=refloc[1],rad=100.)
    # inventory = inventory + inventoryi

    if inventory:
        if usebf:
            bfreqdata(datab='parkfield',t1=t1,t2=t2,stn=stn,
                      net=nw,chan=chn,bfr=10.,clnt="NCEDC",
                      inventory=inventory,sendreq=sendreq)
        else:
            # request data, one earthquake at a time
            for k in range(0,len(t1)):
                print('Earthquake '+str(k)+' of '+str(len(t1)))
                # check for and request the data
                reqdata(datab='parkfield',t1=t1[k],t2=t2[k],stn=stn,
                        net=nw,chan=chn,bfr=10.,clnt="NCEDC",
                        inventory=inventory,breqfast=False)


    #------------------PB stations-------------------------------------
    # create an empty inventory for IRIS request
    inventory=obspy.Inventory([],'T','T')

    # find relevant stations
    nw,stn,chn,inventoryi=findstat(tmin,tmax,stn='*',net='PB',chan='EH*',
                                   clnt="IRIS",lon=refloc[0],lat=refloc[1],
                                   rad=50.)
    inventory = inventory + inventoryi
    #print('no PB stations')

    if inventory:
        if usebf:
            bfreqdata(datab='parkfield',t1=t1,t2=t2,stn=stn,
                      net=nw,chan=chn,bfr=10.,clnt="IRIS",
                      inventory=inventory,sendreq=sendreq)
            
        else:
            # request data, one earthquake at a time
            for k in range(0,len(t1)):
                print('Earthquake '+str(k)+' of '+str(len(t1)))
                # check for and request the data
                reqdata(datab='parkfield',t1=t1[k],t2=t2[k],stn=stn,
                        net=nw,chan=chn,bfr=10.,clnt="IRIS",
                        inventory=inventory)



def collectnsc(nw,stn,chn):
    """
    :param        nw:   networks
    :param       stn:   stations
    :param       chn:   channels
    :return      nsc:   set of network,station,channel tuples
    :return       nw:   networks
    :return      stn:   stations
    :return      chn:   channels
    """

    # want lists
    if isinstance(nw,str):
        nw = [nw]
    if isinstance(stn,str):
        stn = [stn]
    if isinstance(chn,str):
        chn = [chn]
    if not chn:
        chn=[chn]
    elif isinstance(chn[0],str):
        chn = [chn]

    # want lists, not numpy array
    nw,stn,chn=list(nw),list(stn),list(chn)

    # repeat to number of stations
    if nw:
        nmax = np.max(np.array([len(nw),len(stn),len(chn)]))
        nw = nw * int(nmax/len(nw))
        stn = stn * int(nmax/len(stn))
        chn = chn * int(nmax/len(chn))
    else:
        nmax = 0

    # collect
    nsc = []
    for k in range(0,nmax):
        for ch in chn[k]:
            nsc.append(tuple([nw[k],stn[k],ch]))

    return nsc,nw,stn,chn


def bfreqdata(datab,t1,t2,stn=None,net=None,chan=None,bfr=0.,
              clnt='IRIS',inventory=None,sendreq=False):
    """
    :param      datab:   database name
    :param         t1:   start time
    :param         t2:   end time
    :param        stn:   station to consider (default: all)
    :param        net:   network to consider (default: all)
    :param       chan:   channel to consider (default: all)
    :param        bfr:   how much spacing to allow in seconds (default: 0.)
    :param       clnt:   client to request data from (default: IRIS)
    :param  inventory:   an inventory object with the stations of interest
                          ---overrides stn,net,chan
    :param    sendreq:   make a breqfast request?
    """


    # initialize a directory to retrieve data later
    fdir=os.environ['SDATA']
    fname=datetime.datetime.now().strftime("%Y.%B.%d.%H.%M.%S.%f")
    fnamei='breqfastdata_'+fname
    fname = os.path.join(fdir,fnamei)
    os.makedirs(fname)
    fnamedir = fname

    # create a file to sort
    fnamesort = os.path.join(fnamedir,'tosort.py')
    fl = open(fnamesort,'w')
    fl.write('import waveformdb\n')
    fl.write('\n')
    fl.write('waveformdb.allsort(datab=\''+datab+'\',fdirf=\''+
             fnamedir+'\',dlist=True)\n')
    fl.close()

    # create a file to run
    fnamerun = os.path.join(fnamedir,'toretrieve')
    fl = open(fnamerun,'w')
    fl.write('\n')
    fl.write('cd '+fnamedir+'\n\n')
    fl.close()
    fnamegrab = os.path.join(fdir,'REQUESTS','grabwlabel.sh')
    shutil.copymode(fnamegrab,fnamerun)

    # make a list of labels
    lbls = []

    # initialize file for request
    fname,fnamei=initbreqfast(lbl='bfreq')    

    # keep track of number of lines
    nline = 0

    # need as arrays
    t1,t2=np.atleast_1d(t1),np.atleast_1d(t2)

    for k in range(0,len(t1)):
        # go through each event
        nreq=reqdata(datab,t1[k],t2[k],stn=stn,net=net,
                     chan=chan,bfr=bfr,clnt="ignore",
                     inventory=inventory,breqfast=fname)
        
        # if there's a large number of lines, split them
        nline=nline+nreq
        if nline>3000:
            # go ahead and send what's written
            nline = 0

            # add to list of labels
            lbls.append(fnamei)

            # to retrieve later
            fl = open(fnamerun,'a')
            fl.write(fnamegrab+' '+fnamei+' '+clnt+'\n')
            fl.close()
            
            # send if specified
            if sendreq:
                sendbreqfast(fname,clnt)

            # new file
            fname,fnamei=initbreqfast(lbl='bfreq')

    # the last group of files?
    if nline>0:
        # add to list of labels
        lbls.append(fnamei)

        # to retrieve later
        fl = open(fnamerun,'a')
        fl.write(fnamegrab+' '+fnamei+' '+clnt+'\n')
        fl.close()

        # send if specified
        if sendreq:
            sendbreqfast(fname,clnt)

    # to sort later
    fl = open(fnamerun,'a')
    fl.write('\npython3 '+fnamesort+'\n')
    fl.close()

    return lbls

def adreqdata(datab,t1,t2,stn=None,net=None,chan=None,bfr=0.,
              clnt='CNSN',inventory=None,sendreq=False):
    """
    :param      datab:   database name
    :param         t1:   start time
    :param         t2:   end time
    :param        stn:   station to consider (default: all)
    :param        net:   network to consider (default: all)
    :param       chan:   channel to consider (default: all)
    :param        bfr:   how much spacing to allow in seconds (default: 0.)
    :param       clnt:   client to request data from (default: IRIS)
    :param  inventory:   an inventory object with the stations of interest
                          ---overrides stn,net,chan
    :param    sendreq:   make a breqfast request?
    """


    # initialize a directory to retrieve data later
    fdir=os.environ['SDATA']
    fname=datetime.datetime.now().strftime("%Y.%B.%d.%H.%M.%S.%f")
    fnamei='auotdrmdata_'+fname
    fname = os.path.join(fdir,fnamei)
    os.makedirs(fname)
    fnamedir = fname

    # create a file to sort
    fnamesort = os.path.join(fnamedir,'tosort.py')
    fl = open(fnamesort,'w')
    fl.write('import waveformdb\n')
    fl.write('\n')
    fl.write('waveformdb.allsort(datab=\''+datab+'\',fdirf=\''+
             fnamedir+'\',dlist=True)\n')
    fl.close()

    # create a file to run
    fnamerun = os.path.join(fnamedir,'toretrieve')
    fl = open(fnamerun,'w')
    fl.write('\n')
    fl.write('cd '+fnamedir+'\n\n')
    fl.close()
    fnamegrab = os.path.join(fdir,'REQUESTS','grabwlabel.sh')
    shutil.copymode(fnamegrab,fnamerun)

    # make a list of labels
    lbls = []

    # initialize file for request
    fname,fnamei=initautodrm(lbl='adrm')    

    # keep track of number of lines
    nline = 0

    # need as arrays
    t1,t2=np.atleast_1d(t1),np.atleast_1d(t2)

    for k in range(0,len(t1)):
        # go through each event
        nreq=reqdata(datab,t1[k],t2[k],stn=stn,net=net,
                     chan=chan,bfr=bfr,clnt="ignore",
                     inventory=inventory,breqfast=fname)
        
        # if there's a large number of lines, split them
        nline=nline+nreq
        if nline>3000:
            # go ahead and send what's written
            nline = 0

            # add to list of labels
            lbls.append(fnamei)

            # to retrieve later
            fl = open(fnamerun,'a')
            fl.write(fnamegrab+' '+fnamei+' '+clnt+'\n')
            fl.close()
            
            # send if specified
            if sendreq:
                sendbreqfast(fname,clnt)

            # new file
            fname,fnamei=initautodrm(lbl='adrm')

    # the last group of files?
    if nline>0:
        # add to list of labels
        lbls.append(fnamei)

        # to retrieve later
        fl = open(fnamerun,'a')
        fl.write(fnamegrab+' '+fnamei+' '+clnt+'\n')
        fl.close()

        # send if specified
        if sendreq:
            sendbreqfast(fname,clnt)

    # to sort later
    fl = open(fnamerun,'a')
    fl.write('\npython3 '+fnamesort+'\n')
    fl.close()

    return lbls

def reqdata(datab,t1,t2,stn=None,net=None,chan=None,bfr=0.,
            clnt="IRIS",inventory=None,breqfast=False,sendreq=False,
            autodrm=False):
    """
    :param      datab:   database name
    :param         t1:   start time
    :param         t2:   end time
    :param        stn:   station to consider (default: all)
    :param        net:   network to consider (default: all)
    :param       chan:   channel to consider (default: all)
    :param        bfr:   how much spacing to allow in seconds (default: 0.)
    :param       clnt:   client to request data from (default: IRIS)
    :param  inventory:   an inventory object with the stations of interest
                          ---overrides stn,net,chan
    :param   breqfast:   make a breqfast request?
    :param    sendreq:   actually send the breqfast request (default: False)
    :param    autodrm:   make an autodrm request?
    :return      nreq:   number of intervals requested
    """

    # if the station given was actually an inventory
    if inventory is not None:
        inventory=inventory.select(starttime=t1,endtime=t2)
        net,stn,chan,lln=netstatfrominv(inventory)


    # collect the set of values
    nsc,nw,stn,chn = collectnsc(net,stn,chan)

    # try to get time spacing
    dtim = np.ones([len(nsc)],dtype=float)*0.01
    if inventory:  # is not None:
        for k in range(0,len(nsc)):
            nsci = nsc[k]
            invi=inventory.select(network=nsci[0],station=nsci[1],
                                  channel=nsci[2])
            dtim[k]=1.5/invi[0][0][0].sample_rate
    else:
        pass

    # go to breqfast request if desired
    if breqfast is True:
        bfreqdata(datab=datab,t1=t1,t2=t2,stn=stn,net=net,
                  chan=chn,bfr=bfr,clnt=clnt,inventory=inventory,
                  sendreq=sendreq)
        nreq=float('nan')

    else:
        if nsc:
            bulk = []
            print('Looking for existing data')
            dtsa,nsci = findneeded(datab,t1,t2,bfr=bfr,nsc=nsc,bfrd=dtim)

            for k in range(0,len(nsci)):
                # find the data needed
                dts,nsi = dtsa[k],nsci[k]
                for m in range(0,dts.shape[0]):
                    bulk.append([nsi[0],nsi[1],'*',nsi[2],
                                 dts[m,0],dts[m,1]])

            if bulk and not breqfast:
                print('Requesting data')
                
                # open client to retrieve data
                client=Client(clnt)
                
                # directory
                fdir=os.environ['SDATA']
                curdata=datetime.datetime.now().strftime("%Y.%B.%d.%H.%M.%S.%f")
                curdata='currentdata_' + curdata
                fdir = os.path.join(fdir,curdata)
                
                if not os.path.exists(fdir):
                    os.makedirs(fdir)
                    
                # may not want to get the whole thing at once
                nint=int(np.ceil(float(len(bulk))/100))
                nint=np.linspace(0.,len(bulk)+1.,nint+1).astype(int)
           
                # for each date range
                for k in range(0,len(nint)-1):
                    try:
                        # waveform
                        st=client.get_waveforms_bulk(bulk[nint[k]:nint[k+1]])
                    except:
                        # if there isn't any data, just create an empty Stream
                        st=obspy.Stream()

                    for tr in st:
                        # write each trace
                        fname=waveformdb.sacfilename(tr)
                        fname=os.path.join(fdir,fname)
                        if tr.stats.npts>1:
                            tr.write(fname,'SAC')
            
                # add the sac files
                waveformdb.allsort(datab=datab,fdirf=fdir,dlist=True)

                # delete the directory used for data storage
                os.rmdir(fdir)

            elif bulk and breqfast:
                # add these to a breqfast request
                addtobreqfast(breqfast,bulk)

            # the number of requests
            nreq = len(bulk)
        else:
            # no stations to request
            nreq = 0


    return nreq


def reqdataind(datab,t1,t2,stn=None,net=None,chan=None,bfr=0.,
               clnt="IRIS"):
    """
    :param      datab:   database name
    :param         t1:   start time
    :param         t2:   end time
    :param        stn:   station to consider (default: all)
    :param        net:   network to consider (default: all)
    :param       chan:   channel to consider (default: all)
    :param        bfr:   how much spacing to allow in seconds (default: 0.)
    :param       clnt:   client to request data from (default: IRIS)
    """

    # find the data needed
    dts = findneeded(datab,t1,t2,stn=stn,net=net,chan=chan,bfr=bfr)

    # open client to retrieve data
    client=Client(clnt)

    # directory
    fdir=os.environ['SDATA']
    curdata=datetime.datetime.now().strftime("%Y.%B.%d.%H.%M.%S.%f")
    curdata='currentdata_' + curdata
    fdir = os.path.join(fdir,curdata)

    if not os.path.exists(fdir):
        os.makedirs(fdir)
    #print((dts[:,1]-dts[:,0])/3600.)

    # for each date range
    for k in range(0,dts.shape[0]):
        t1,t2=dts[k,0],dts[k,1]

        try:
            # waveform
            st=client.get_waveforms(net,stn,'*',chan,t1,t2)
        except:
            # if there isn't any data, just create an empty Stream
            st=obspy.Stream()

        for tr in st:
            # write each trace
            fname=waveformdb.sacfilename(tr)
            fname=os.path.join(fdir,fname)
            tr.write(fname,'SAC')
        
    # add the sac files
    waveformdb.allsort(datab=datab,fdirf=fdir,dlist=True)

    # delete the directory used for data storage
    os.rmdir(fdir)



def reqdatao(dts,clts=None,sta=None,net=None,chan=None):    

    # open client
    client=Client("NCEDC")

    # time range to get
    trange=np.array([-50,100.])

    # directory
    fdir=os.environ['SDATA']

    # to check if it's in the file
    session=waveformdb.opendatabase('pksdrop')
    q=session.query(Waveform)

    eqi=0;
    for eq in eqs:
        eqi=eqi+1
        print(eq.evid)
        print(eqi)

        # time
        tm=obspy.UTCDateTime(eq.time)
        t1=tm+trange[0]
        t2=tm+trange[1]

        print(tm)

        for k in range(0,len(ns)):
            # split
            nsi,ch=ns[k],cmps[k]
            vls=nsi.split('.')

            for chi in ch:
                # saved waveforms
                qq=q.filter(Waveform.net==vls[0])
                qq=qq.filter(Waveform.sta==vls[1])
                qq=qq.filter(Waveform.chan==chi)
                qq=qq.filter(Waveform.starttime<=t2.timestamp)
                qq=qq.filter(Waveform.endtime>=t1.timestamp)

                if not qq.all():
                    try:
                        # waveform
                        st=client.get_waveforms(vls[0],vls[1],'*',chi,t1,t2)
                        
                        # write to sac file
                        fname=nsi+'.'+chi+'.'+str(eq.evid)+'.SAC'
                        fname=os.path.join(fdir,fname)
                    
                        if st:
                            st[0].write(fname,'SAC')
                    except:
                        print('No data available')
                else:
                    print('Have data')

        # close
        session.close()
        
        # add the sac files
        waveformdb.allsort(datab=['pksdrop','allseis'])
