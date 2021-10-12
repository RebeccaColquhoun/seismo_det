import obspy
def load_data_and_remove_response(event_file):
    event_id = 3031111
    rootpath = '/Users/rebecca/Documents/PhD/Research/Frequency/Olsen and Allen/data/'
    event_file = '1992-06-28T11:57:34.130000Z'
    data = obspy.read(rootpath+event_file+'/mseed/*')
    
    for tr in data:
        inv=obspy.read_inventory(rootpath+event_file+'/stations/'+str(tr.stats.network)+"."+str(tr.stats.station)+'.xml')
        tr.remove_response(inventory=inv)
    data.plot()
    return data

def load_data(pathToEQ, subfolder):
    ''' 
    Loads seismograms for 1 EQ from memory discarding any which are not channel HH*. 
    args: 
        pathToEQ - takes one item in EQ folders
        subfolder = data source to load from e.g. sac, raw
    Returns:
        data: obspy Stream with all seismograms with HH channel of that eq
        cat: EQ catalog between t1 and t2
    '''

    path = rootPath + pathToEQ + '/'+subfolder+'/*'
    st = obspy.read(path)
    data = obspy.Stream() 
    for i in range(0,len(st)): 
        if st[i].stats['channel'][0:2]=='HH' and st[i].stats['network']=='NZ':
            tr = st[i] 
            if hasattr(tr.data,'mask')==False:
                data = data + tr
                        
    return data

def plottogpicks(st,pk='t0',tlm=None,tscl=None,rscl=True,fname=None):
    # INPUT
    # after Jess
    # st          a list of waveform sets
    # rscl        rescale the amplitudes

    if isinstance(st,obspy.Stream):
        st=[st]

    if tlm is None:
        tlm = np.array([-1.,3])

    if tscl is None:
        tscl = tlm

    # set of stations and components
    lbls,lblss=[],[]
    for sti in st:
        for tr in sti:
            wid=tr.stats.network+'.'+tr.stats.station+'.'+\
                tr.stats.channel
            #wid=tr.get_id()
            lbls.append(wid.strip())
            #wid=tr.stats.station
            lblss.append(wid.strip())

    lbls,ix=np.unique(np.array(lbls),return_index=True)
    lblss=np.array(lblss)[ix]
    
    # number of stations
    N = len(lbls)

    # initialize plots
    plt.close()
    f = plt.figure(figsize=(8,12))
    gs,p=gridspec.GridSpec(N,1),[]
    for k in range(0,N):
        p.append(plt.subplot(gs[k]))

    cls = ['blue','red','green','black','yellow','orange']
    M = len(st)

    for k in range(0,N):
        for m in range(0,M):
            nw,stn,chn=lbls[k].split('.')
            tr = st[m].select(network=nw,station=stn,channel=chn)

            #wid=tr.stats.network+'.'+tr.stats.station+'.'+\
            #    tr.stats.channel

            # find the relevant values
            #            tr = st[m].select(id=lbls[k])

            if tr:
                tr = tr[0]
                # the reference time
                tsec,tpk=resolvepick(tr,pk=pk,mkset=None)

                # for scaling
                if rscl:
                    scl = tr.copy().trim(starttime=tpk+tscl[0],
                                         endtime=tpk+tscl[1])
                    if scl.data.any():
                        scl = np.max(np.abs(scl.data))
                    else:
                        scl = float('nan')
                else:
                    scl = 1.

                # for plotting
                data = tr.copy().trim(starttime=tpk+tlm[0],
                                      endtime=tpk+tlm[1])
                tm = data.times()+(data.stats.starttime-tpk)
                data = data.data / scl

                # plot
                p[k].plot(tm,data,color=cls[m])

        p[k].set_ylabel(lblss[k])
        p[k].set_xlim(tlm)
        if rscl:
            p[k].set_ylim(np.array([-1.,1.])*1.1)
        if k<N-1:
            p[k].set_xticklabels([])

    if fname:
        import graphical
        graphical.printfigure(fname,f)
    else:
        plt.show()

    return p
