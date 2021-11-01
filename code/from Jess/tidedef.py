import numpy as np
import general
#import pupygrib
import netCDF4
import os,glob
import datetime
import math
import matplotlib.pyplot as plt
from matplotlib import gridspec
import matplotlib
import graphical
import slabgeom
from scipy import signal
#import cartopy
#import cartopy.crs as ccrs
import copy
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable

class defm:
    # set up with a dictionary
    def __init__(self,dloc=None,rgn='unknown'):
        """
        :param      dloc: deformation / target locations
                             N x 3 array: N points by 
                                [lon, lat, depth] for each
        :param       rgn: which region this is (default: unknown)
        """

        # keep track of the region of interest, as we'll calculate differently
        self.region = rgn


        # deformation points
        if dloc is not None:
            self.add_dloc(dloc)

        # which loads to consider
        self.loads = []

    def add_dloc(self,dloc=None,lon=None,lat=None,depth=None):
        """
        :param      dloc: deformation / target locations
                             N x 3 array: N points by 
                                [lon, lat, depth in km] for each
                             or list of locations
                             N x 2 matrices are set to the surface
        :param       lon: longitudes in degrees, used only if dloc=None
        :param       lat: latitudes in degrees, used only if dloc=None
        :param     depth: latitudes in degrees, used only if dloc=None
                             or dloc doesn't have at third column
        """

        # make sure it's a numpy array with the appropriate size
        dloc = np.atleast_2d(dloc)


        if dloc is not None:
            # horizontal locations
            self.lon = dloc[:,0]
            self.lat = dloc[:,1]

            # identify values of interest
            cloc,depths,stk,dip,gds=slabgeom.projtoplate(np.vstack([self.lon,self.lat]).T)


            # depth
            if dloc.shape[1]>=3:
                self.depth = dloc[:,2]
            elif depth is not None:
                self.depth = depth
            else:
                self.depth = depths

        else:

            # horizontal locations
            self.lon = lon
            self.lat = lat

            # identify values of interest
            cloc,depths,stk,dip,gds=slabgeom.projtoplate(np.vstack([self.lon,self.lat]).T)

            # depth
            if depth is not None:
                self.depth = depth
            else:
                self.depth = depths

        # save strike and dip
        self.strike = stk
        self.dip = dip


    def picklocs(self,depthrange=None,spc=15,specloc=None,justgrid=[]):
        """
        find a gridded set of locations on the interface
        :param     depthrange: only look in this depth range
        :param            spc: desired spacing in km
        :param        specloc: specific lon, lat locations, if not given
        :param       justgrid: if we just want a grid of lon, lat values
                               justgrid is the width of the grid in degrees latitude
        """

        if spc is None:
            spc=15.
        justgrid=np.atleast_1d(justgrid)

        if specloc is not None:
            specloc=np.atleast_2d(specloc)
            self.lon=specloc[:,0]
            self.lat=specloc[:,1]
            self.depth=np.ones(self.lon.size,dtype=float)*30.
            self.strike=np.ones(self.lon.size,dtype=float)*0.
            self.dip=np.ones(self.lon.size,dtype=float)*20.

        elif len(justgrid):
            # ytox ratio
            ytox=justgrid[1]
            justgrid=justgrid[0]
            
            # spacing and center
            spc=spc/deg2km()
            ctr=somestressloc(self.region)
            ctr=np.median(ctr,axis=0)
            dlon=np.maximum(np.cos(np.pi/180*ctr[1]),0.05)

            # limits
            lonlim=ctr[0]+np.array([-1,1])*justgrid/2./dlon*ytox
            latlim=ctr[1]+np.array([-1,1])*justgrid/2.

            # points
            lon=np.arange(lonlim[0],lonlim[1]+spc*1e-3,spc*dlon)
            lat=np.arange(latlim[0],latlim[1]+spc*1e-3,spc)
            lon,lat=np.meshgrid(lon,lat)

            self.lon=lon.flatten()
            self.lat=lat.flatten()
            self.depth=np.ones(self.lon.size,dtype=float)*20.
            self.strike=np.ones(self.lon.size,dtype=float)*0.
            self.dip=np.ones(self.lon.size,dtype=float)*90.

        elif self.region in ['Cascadia','Shikoku']:
            self.pickspacedlocs(depthrange=depthrange,spc=spc,region=self.region)

        elif self.region=='Parkfield':
            import pklfes
            loc=pklfes.lfelocs()
            loc=np.array(list(loc.values()))
            self.lon=loc[:,0]
            self.lat=loc[:,1]
            self.depth=loc[:,2]
            
            flt=slabgeom.faultmodel(region=self.region,spc=None)
            self.strike=np.ones(self.lon.size,dtype=float)*np.median(flt.stk)
            self.strike=np.ones(self.strike.size)*135.
            self.dip=np.ones(self.lon.size,dtype=float)*np.median(flt.dip)
            self.dip=np.ones(self.lon.size,dtype=float)*90.
                        
        elif self.region=='Parkfield_shallow':
            flt=slabgeom.faultmodel(region=self.region,spc=spc)
            self.lon=flt.loc[:,0]
            self.lat=flt.loc[:,1]
            self.depth=flt.loc[:,2]
            self.strike=flt.stk
            self.dip=flt.dip
            
    def pickspacedlocs(self,region='Cascadia',depthrange=None,spc=15,
                       lonlim=None):
        """
        find a gridded set of locations on the interface
        :param         region: region of interest (default: 'Cascadia')
        :param     depthrange: only look in this depth range
        :param            spc: desired spacing in km
        :param         lonlim: a longitude limit, if desired 
                                 (default: any for cascadia, 
                                  [131.9,135] for shikoku)
        """

        # default depth ranges
        depthdef={'Cascadia':[25,55],'Shikoku':[15,70],'Ryukyu':[15,70]}
        if depthrange is None:
            depthrange=depthdef.get(region,[15,70])
        
        # read the interface
        if region in ['Cascadia']:
            lon,lat,depths,stk,dip,gds=slabgeom.readcascadia()
        elif region in ['Shikoku']:
            lon,lat,depths,stk,dip=slabgeom.read_slab2(region=region)

        if lonlim is None:
            lonlim={'Shikoku':[130,139]}
            lonlim=lonlim.get(region,[0,360])
        dflon=np.diff(lonlim)[0] % 360
        if dflon==0:
            dflon=360.

        # remove mask on locations
        if isinstance(lon,np.ma.masked_array):
            lon,lat=lon.data,lat.data
            
        # preferred spacing in each direction
        dlon=spc/(np.median(np.diff(lon))*111.*np.cos(math.pi/180*np.median(lat)))
        dlat=spc/(np.median(np.diff(lat))*111.)
        dlon,dlat=int(np.floor(dlon)),int(np.floor(dlat))

        # select from grid
        ilon=np.arange(0,lon.size,dlon)
        ilat=np.arange(0,lat.size,dlat)

        lons,lats=np.meshgrid(lon[ilon],lat[ilat])
        depths=depths[ilat,:][:,ilon]
        stk=stk[ilat,:][:,ilon]
        dip=dip[ilat,:][:,ilon]

        # only within a certain depth range
        # just to avoid an error
        if isinstance(depths,np.ma.masked_array):
            iok=~depths.mask
            depths[depths.mask]=0.
        else:
            iok=np.ones(depths.shape,dtype=bool)
        iok=np.logical_and(iok,depths>=depthrange[0])
        iok=np.logical_and(iok,depths<=depthrange[1])
        iok=np.logical_and(iok,~stk.mask)
        iok=np.logical_and(iok,~np.isnan(dip))
        iok=np.logical_and(iok,(lons-lonlim[0])%360<=dflon)
        self.lon=lons[iok]
        self.lat=lats[iok]
        self.depth=depths.data[iok]
        self.strike=stk.data[iok]
        self.dip=dip.data[iok]

    def addload(self,sload):
        """
        :param      sload: a surfload object to add to set of values
        """

        self.loads.append(sload)

class surfload:
    """
    an object to track and compute the stresses produced by atmospheric pressure
    """

    def __init__(self,defm=None,sloadi=None,load_type=None,sloads=[]):
        """
        :param          defm: a deformation object, to keep track of the points 
                               where we want to compute the deformation
        :param        sloadi: a pre-existing surfload class, in case 
                               we want to copy from it
        :param     load_type: the type of load for calculating
        :param        sloads: a list of the loads to be combined
        """

        # link the objects to each other
        self.defm=defm
        defm.addload(self)

        # note the load being considered
        self.load_type=load_type

        # any loads to add
        self.sloads=sloads

        # which region is of interest
        self.region=self.defm.region

        # default is unfiltered
        self.flm = np.array([0,float('inf')])
        self.flm_load = np.array([0,float('inf')])
        self.pmin=-float('inf')

        self.bintype='unbinned'
        self.nbins=0

        self.pick_gf_calc()

        # copy from another object if necessary
        if sloadi is not None:
            for nm in sloadi.__dict__.keys():
                self.__setattr__(nm,sloadi.__getattribute__(nm))

        # any other functions that need to be called
        self.additional_init()


    def downsample(self,tspc=3.):
        """
        :param      tspc: desired time spacing in hours
        """

        # spacing
        ospc=(self.tms[1]-self.tms[0]).total_seconds()/3600.
        nsamp=int(np.round(tspc/ospc))

        if nsamp > 1:
            # grab relevant values
            ix=np.arange(0,self.tms.size,nsamp)
            self.tms=self.tms[ix]
            self.stresstensor=self.stresstensor[:,:,ix]
            
            if 'stresstensorf' in self.__dict__.keys():
                self.stresstensorf=self.stresstensorf[:,:,ix]

            if 'meanload' in self.__dict__.keys():
                self.meanload=self.meanload[ix]
                
            # recompute timing
            self.computehourstime()
        
    def defm_f(self):
        """
        :return    defm: return the relevant deformation value
        """
        
        return self.defm

        
    def additional_init(self):
        """
        placeholder for the sub-classes
        """

        pass

    def init_load_locs(self):
        """
        the default locations
        will be overriden in each set
        :return        lons: set of longitudes, in degrees
        :return        lats: set of latitudes, in degrees
        :return        dlon: longitude spacing for each box, in degrees
        :return        dlat: latitude spacing for each box, in degrees
        :return        wgts: a weighting to assign to each point
        """

        lons=np.array([-125,-124,-123])
        lats=np.array([49,48,47])

        dlon=1.*np.ones(lons.size,dtype=float)
        dlat=1.*np.ones(lons.size,dtype=float)

        wgts=np.ones(lons.size,dtype=float)

        return lons,lats,dlon,dlat,wgts

    def computehourstime(self,tref=None):
        """
        compute time in hours relative to a reference
        :param       tref: reference time 
        """

        # reference time
        if tref is not None:
            self.tref=tref
        else:
            try:
                tref=self.tref
            except:
                self.tref=datetime.datetime(1900,1,1)

        # time in hours since then
        self.tmsh=np.array([(tm-self.tref).total_seconds()/3600.
                            for tm in self.tms])

        # note units
        self.time_units = 'hours since {:s}'.format(self.tref.strftime('%-d-%b-%Y'))
    
    def initcalc(self,dstmax=2.,iok=None,nearpoint=None,delnowgt=True,subsamp=0.1):
        """
        initialise the calculations---compute GF and find the relevant parts of the load
        :param     dstmax: only consider contributes from load up to dstmax degrees away
        :param        iok: which to read, if we already know
        :param  nearpoint: if we just want to calculate stresses for a 20-km region 
                              centered at nearpoint
        :param   delnowgt: delete the point from the calculation if it's given 
                              zero weighting
        :param    subsamp: how much to subsample the loading boxes to maintain accuracy
        """
    
        if iok is not None:
            self.dstmax=float('NaN')
        else:
            self.dstmax=dstmax

        # identify the locations of interest
        lons,lats,self.dlon,self.dlat,self.lwgts=\
                self.init_load_locs()
        
        # deformation locations
        # reset just to make sure it's not been wrapped to another value
        self.defm=self.defm_f()
        dloc=np.vstack([self.defm.lon,self.defm.lat,self.defm.depth]).T            

        if iok is None:
            # some range from the outset
            lonm=np.median(self.defm.lon)
            lonlim=general.minmax(self.defm.lon-lonm)+np.array([-1.,1])*dstmax
            latlim=general.minmax(self.defm.lat)+np.array([-1.,1])*dstmax
            iok=(lons-lonm) % 360
            iok[iok>180]=iok[iok>180]-360
            iok=np.logical_and(iok>=lonlim[0],iok<=lonlim[1])
            iok=np.logical_and(iok,lats>=latlim[0])
            iok=np.logical_and(iok,lats<=latlim[1])
            iok,=np.where(iok)
            lons,lats=lons[iok],lats[iok]
            self.dlon,self.dlat=self.dlon[iok],self.dlat[iok]
            self.lwgts=self.lwgts[iok]
            
            # grids of locations
            sloc=np.vstack([lons,lats]).T
            
            # distances between these points
            dst,az = spheredist(dloc,sloc)
            
            # and again delete any points that are always too far away
            toofar=dst>dstmax
            jok = np.sum(toofar,axis=0)<toofar.shape[0]
            iok,lons,lats=iok[jok],lons[jok],lats[jok]
            self.dlon,self.dlat=self.dlon[jok],self.dlat[jok]
            self.lwgts=self.lwgts[jok]
            toofar=toofar[:,jok]

        else:
            # already know which values to grab
            lons,lats=lons[iok],lats[iok]
            self.dlon,self.dlat=self.dlon[iok],self.dlat[iok]
            self.lwgts=self.lwgts[iok]
            toofar=np.zeros([dloc.shape[0],iok.size],dtype=bool)

        # if we just want  local section
        if nearpoint is not None:
            nearpoint=np.atleast_2d(np.array(nearpoint).flatten()[0:2])
            dst,az = spheredist(nearpoint,np.vstack([lons,lats]).T)
            jok=dst[0,:]<40/deg2km()
            iok,lons,lats=iok[jok],lons[jok],lats[jok]
            self.dlon,self.dlat=self.dlon[jok],self.dlat[jok]
            self.lwgts=self.lwgts[jok]
            toofar=toofar[:,jok]

            
        # if the weighting in zero, no point in keeping the values
        if delnowgt:
            jok=self.lwgts>0.
            iok,lons,lats=iok[jok],lons[jok],lats[jok]
            self.dlon,self.dlat=self.dlon[jok],self.dlat[jok]
            self.lwgts=self.lwgts[jok]
            toofar=toofar[:,jok]
            
        # now we have a set of points to use
        self.iuse = iok
        self.lons = lons
        self.lats = lats

        # compute the Green's functions
        sloc=np.vstack([lons,lats]).T
        #self.gf = halfspace_stress_gf(sloc,dloc)
        self.gf=calc_gf(sloc,dloc,np.vstack([self.dlon,self.dlat]).T,
                        subsamp=subsamp,gffun=self.gffun,
                        sphdist=self.sphdist,gfname=self.gfname)
        self.stresstypes=['EE','NN','ZZ','EN','EZ','NZ']

        # set any Green's functions for distant points to zero
        toofar=toofar.reshape([1]+list(toofar.shape))
        toofar=(~toofar).astype(float)
        self.gf=np.multiply(self.gf,toofar)

        # convert the GF to pressure
        self.change_gf_units()

    def pick_gf_calc(self,gftype='halfspace',sphdist=True):
        """
        :param    gftype: which type of GF to use ('halfspace' or 'depth')
        :param   sphdist: use spherical distances (default: True)
        """

        self.gftype=gftype
        self.gffun=None
        self.gfname=None
        if gftype in ['halfspace']:
            self.gffun=halfspace_stress_gf
        elif gftype in ['depth']:
            self.gffun=calc_spotl_gf
            self.gfname='depth_Amanda'

        self.sphdist=sphdist
        

    def change_gf_units(self):
        """
        change the GF units appropriately
        """

        # nothing to do here since we don't know what the load is
        self.gfunit = 'unknown'

    def check_strip(self,width=200,orientation='longitude'):
        """
        check the calculations to compare with a strip
        :param         width: strip width
        :param   orientation: along longitude or along latitude
        """

        # center of the grid
        xc=np.median(self.defm.lon)
        yc=np.median(self.defm.lat)
        dlon=np.cos(np.pi/180*yc)

        # nonzero values
        if orientation in ['longitude','vertical']:
            lm=np.array([-0.5,0.5])*width/deg2km()/dlon
            ii=general.modhalf(self.lons-xc,360)
            ii=np.logical_and(ii>=lm[0],ii<=lm[1])
            lm=lm+xc

            lm=np.array([np.min(self.lons[ii]-self.dlon[ii]/2.),
                         np.max(self.lons[ii]+self.dlon[ii]/2.)])

            lat=self.defm.lat[np.argmin(np.abs(self.defm.lat-yc))]
            jj=self.defm.lat==lat
            xvl=self.defm.lon[jj]

            scl=dlon
            
            ix=[0,2,4,1,3,5]
        elif orientation in ['latitude','horizontal']:
            lm=np.array([-0.5,0.5])*width/deg2km()+yc
            ii=np.logical_and(self.lats>=lm[0],self.lats<=lm[1])
            
            lm=np.array([np.min(self.lats[ii]-self.dlat[ii]/2.),
                         np.max(self.lats[ii]+self.dlat[ii]/2.)])

            lon=self.defm.lon[np.argmin(np.abs(self.defm.lon-yc))]
            jj=self.defm.lon==lon
            xvl=self.defm.lat[jj]

            scl=1.

            ix=[1,2,5,0,3,4]

        # sum the relevant values
        gsum=np.sum(self.gf[:,:,ii],axis=2)
        gsum=gsum[:,jj]
        
        # and for comparison, compute the strip solution
        # distance from middle of strip, in km
        dx=general.modhalf(xvl-np.mean(lm),360)*deg2km()*scl

        # distance from right side of strip, in km
        dx1=general.modhalf(xvl-lm[1],360)*deg2km()*scl

        # distance from left side of strip, in km
        dx2=general.modhalf(xvl-lm[0],360)*deg2km()*scl

        # depth
        z=self.defm.depth[jj]

        # angles
        theta1=-np.angle(dx1-1j*z)
        theta2=-np.angle(dx2-1j*z)

        # and analytical solutions
        a=np.diff(lm)[0]/2.

        tauxx=np.multiply(np.sin(theta1-theta2),np.cos(theta1+theta2))
        tauxx=-1/np.pi*((theta1-theta2)-tauxx)

        tauzz=np.multiply(np.sin(theta1-theta2),np.cos(theta1+theta2))
        tauzz=-1/np.pi*((theta1-theta2)+tauzz)

        tauxz=np.multiply(np.sin(theta1-theta2),np.sin(theta1+theta2))
        tauxz=1/np.pi*tauxz
                       

        # to plot
        plt.close()
        f = plt.figure(figsize=(10,8))
        Np = 3
        gs,p=gridspec.GridSpec(3,2),[]
        for gsi in gs:
            p.append(plt.subplot(gsi))
        p=np.array(p).reshape([3,2])
        gs.update(left=0.11,right=0.93)
        gs.update(bottom=0.08,top=0.97)
        gs.update(hspace=0.07,wspace=0.03)

        p[0,0].plot(dx,tauzz,color='b',linestyle='-')
        p[1,0].plot(dx,tauxx,color='b',linestyle='-')
        p[2,0].plot(dx,tauxz,color='b',linestyle='-')

        p[0,0].plot(dx,gsum[ix[0],:],color='r',linestyle='--')
        p[1,0].plot(dx,gsum[ix[1],:],color='r',linestyle='--')
        p[2,0].plot(dx,gsum[ix[2],:],color='r',linestyle='--')       


        p[0,1].plot(dx,gsum[ix[3],:],color='r',linestyle='--')
        p[1,1].plot(dx,gsum[ix[4],:],color='r',linestyle='--')
        p[2,1].plot(dx,gsum[ix[5],:],color='r',linestyle='--')       

        for ph in p.flatten():
            ph.set_xlim(general.minmax(dx))
            ph.set_ylim([-1.05,1.05])
        
    def calcstress(self):
        """
        multiply the Green's functions by the loads to get the stresses
        """

        # EE, NN, ZZ, EN, EZ, NZ
        self.stresstensor = np.dot(self.gf,self.prs)

        # also calculate the mean load through time
        self.meanload = np.ma.median(self.prs,axis=0)

    def calcstress_throughtime(self,trange,twin=30.,usesaved=False,tspc=3.):
        """
        consider a range of time windows, load the surface information, calculate the stress
        :param    trange: time range to consider
        :param      twin: max length of time window in days (default: 20)
        :param  usesaved: use saved values where available? (default: False)
        :param      tspc: preferred time sampling in hours (default: 3)
        """

        # default time window
        if twin is None:
            twin=40.

        # initialize the calculations
        #self.initcalc(dstmax=2.)

        if usesaved:
            self.read_stresses(trange=trange)

        else:
            # find the time windows
            tlm=(trange[1]-trange[0]).total_seconds()
            nwin=int(np.ceil(tlm/(twin*86400)))
            tlm=np.linspace(0,tlm,nwin+1)
            tlm=[trange[0]+datetime.timedelta(seconds=tm) for tm in tlm]
            
            for k in range(0,nwin):
                tlmi=tlm[k:k+2]
                tm=tlmi[0].strftime('%b %d, %Y')+' -  '+tlmi[1].strftime('%b %d, %Y')
                print('Computing stresses for '+tm)

                # read for this window
                self.read_total_load(trange=tlmi)
                
                # calculate the stresses
                self.calcstress()
                
                # add to set
                if k==0:
                    tmss=self.tms.copy()
                    stresstensors=self.stresstensor.copy()
                    meanload=self.meanload.copy()
                else:
                    tmss=np.append(tmss,self.tms)
                    meanload=np.append(meanload,self.meanload)
                    stresstensors=np.append(stresstensors,self.stresstensor,axis=2)

            # replace the values
            self.tms=tmss
            self.stresstensor=stresstensors
            self.meanload=meanload
            self.computehourstime()

        # downsample if needed
        self.downsample(tspc=tspc)

    def calcmeanload_throughtime(self,trange,loccent=None,dsts=[1.],
                                 twin=30.,tspc=3.,inclwgt=False):
        """
        consider a range of time windows, load the surface information, calculate the stress
        :param    trange: time range to consider
        :param   loccent: central location of interest
        :param      dsts: distances in degrees
        :param      twin: max length of time window in days (default: 20)
        :param      tspc: preferred time sampling in hours (default: 3)
        :param   inclwgt: include the land-ocean weighting
        """

        # default time window
        if twin is None:
            twin=40.

        # location
        if loccent is None:
            loccent=somestressloc(region=self.region)
            loccent=np.median(loccent,axis=0)
        loccent=np.atleast_1d(loccent)[0:2]

        # distances for each point
        dst,az=spheredist(np.vstack([self.lons,self.lats]).T,
                          loccent.reshape([1,2]))
        dsts=np.atleast_1d(dsts)
        dsts=dsts.reshape([1,dsts.size])
        wgts=(dsts<=dst).astype(float)
        if inclwgt:
            wgts=np.multiply(wgts,self.lwgts.reshape([self.lwgts.size,1]))
        wgts=np.divide(wgts,np.sum(wgts,axis=0)).T

        # initialize the calculations
        #self.initcalc(dstmax=2.)

        # find the time windows
        tlm=(trange[1]-trange[0]).total_seconds()
        nwin=int(np.ceil(tlm/(twin*86400)))
        tlm=np.linspace(0,tlm,nwin+1)
        tlm=[trange[0]+datetime.timedelta(seconds=tm) for tm in tlm]
        
        for k in range(0,nwin):
            tlmi=tlm[k:k+2]
            tm=tlmi[0].strftime('%b %d, %Y')+' -  '+tlmi[1].strftime('%b %d, %Y')
            print('Computing mean load for '+tm)

            # read for this window
            self.read_total_load(trange=tlmi)
            
            # add to set
            if k==0:
                tmss=self.tms.copy()
                meanload=np.dot(wgts,self.prs)
            else:
                tmss=np.append(tmss,self.tms)
                meanload=np.append(meanload,np.dot(wgts,self.prs),
                                   axis=1)

        # replace the values
        self.tms=tmss
        self.meanloads=meanload
        self.loadcents=loccent
        self.loaddsts=dsts.flatten()
        self.computehourstime()

        # file name
        fdir=os.path.join(os.environ['DATA'],'TREMORMOD','SAVEDSTRESSES')
        fname=self.load_label()[2]+'_mean_'+self.defm_f().region+'_'

        # go through and save
        for k in range(0,len(self.loaddsts)):
            fnamei=fname+'{:0.2f}'.format(self.loaddsts[k])
            fnamei=fnamei.replace('.','p')
            fnamei=os.path.join(fdir,fnamei)
            fnamej=fnamei+'_time'

            np.save(fnamei,self.meanloads[k,:])
            np.save(fnamej,self.tms)


    def read_meanload(self,drange=1.):
        """
        read the mean load and interpolate to the desired times
        :param    drange: distance range in degrees
        """

        # file name
        fdir=os.path.join(os.environ['DATA'],'TREMORMOD','SAVEDSTRESSES')
        fname=self.load_label()[2]+'_mean_'+self.defm_f().region+'_'
        fnamei=fname+'{:0.2f}'.format(drange)
        fnamei=fnamei.replace('.','p')
        fnamei=os.path.join(fdir,fnamei)
        fnamej=fnamei+'_time'

        # read
        meanload=np.load(fnamei+'.npy')
        tms=np.load(fnamej+'.npy')

        # interpolate
        tref=tms[0]
        thave=np.array([(tm-tref).total_seconds() for tm in tms])
        tdes=np.array([(tm-tref).total_seconds() for tm in self.tms])
        self.meanload=np.interp(tdes,thave,meanload)
        self.meanloadrange=drange

    def pickloadlocs(self,locdes=None):
        """
        :param    locdes: desired locations, if you know which ones are wanted
        :return     locs: locations of some stations
        :return    igrab: indices of those stations
        """

        # preferred locations
        if locdes is None:
            if self.load_type is 'pressure':
                locdes=someloadloc(self.region)
            elif self.load_type in ['groundwater','snow']:
                locdes=someloadloc_land(self.region)
        locdes=np.atleast_2d(locdes)

        # find the nearest locations
        igrab=findnearest(locdes[:,0],locdes[:,1],self.lons,self.lats)
        locs=np.vstack([self.lons[igrab],self.lats[igrab]]).T

        # for ease of plotting
        locs[:,0]=general.modhalf(locs[:,0],360)

        return locs,igrab


    def plotstress_time(self,usefiltered=True,stressloc=None,loadloc=None,icmp=2,
                        trange=None,demean=True,prt=True):
        """
        assign phases between 0 and 360 to the times of each part of the signal
        :param    usefiltered: use stresstensorf instead of stresstensor
        (default: True)
        :param      stressloc: locations of the stresses to plot
        :param        loadloc: locations of the loads to plot
        :param           icmp: which components of stress to plot
        :param         trange: time range to plot
        :param         demean: remove the means
        """

        # which stresses to use
        icmp=np.atleast_1d(icmp).astype(int)
        if usefiltered:
            stress = self.stresstensorf[icmp,:,:]
        else:
            stress = self.stresstensor[icmp,:,:]

        #---------------grab values for the stress------------------------------

        # find which points to plot for stress
        if stressloc is None:
            stressloc=somestressloc(self.region)
        stressloc=np.atleast_2d(stressloc)
        istress=findnearest(stressloc[:,0],stressloc[:,1],self.defm.lon,self.defm.lat)
        stress=stress[:,istress,:]

        # label the locations
        slons,slats=self.defm.lon[istress],self.defm.lat[istress]
        slbls=['{:0.1f} W, {:0.1f} N'.format(slons[k],slats[k])
               for k in range(0,len(istress))]

        
        # only some times?
        if trange is not None:
            ii=np.logical_and(self.tms>=trange[0],self.tms<=trange[1])
            stress=stress[:,:,ii]
            tms=self.tms[ii]
        else:
            tms=self.tms
            trange=general.minmax(tms)

        if demean:
            mns=np.ma.mean(stress,axis=2)
            mns=mns.reshape([mns.shape[0],mns.shape[1],1])
            stress=stress-mns
            
        # times
        tms=np.array([matplotlib.dates.date2num(tm) for tm in tms])
        tranger=np.array([matplotlib.dates.date2num(tm) for tm in trange])

        # coloring
        scols=graphical.colors(len(istress))
        lsty=graphical.linestyles(len(icmp))
        
        #----------------grab values for the load---------------------------

        # find which points to plot for the load
        loadloc,iload=self.pickloadlocs(loadloc)

        # get the loads and the times
        ld,ltms=self.return_load()

        # only some locations?
        ld=ld[iload,:]
        
        # only some times?
        if trange is not None:
            ii=np.logical_and(ltms>=trange[0],ltms<=trange[1])
            ld,ltms=ld[:,ii],ltms[ii]
        else:
            trange=general.minmax(ltms)

        if demean:
            mns=np.ma.mean(ld,axis=1)
            mns=mns.reshape([mns.shape[0],1])
            ld=ld-mns

            
        # times
        ltms=np.array([matplotlib.dates.date2num(tm) for tm in ltms])
        tranger=np.array([matplotlib.dates.date2num(tm) for tm in trange])

        # coloring
        lcols=graphical.colors(len(iload),lgt=True)

        # label the locations
        #llons,llats=general.modhalf(self.lons[iload],360),self.lats[iload]
        llons,llats=general.modhalf(loadloc[:,0],360),loadloc[:,1]
        llbls=['{:0.1f} W, {:0.1f} N'.format(llons[k],llats[k])
               for k in range(0,len(iload))]

        #-----------------------------------------------------------------------
        
        plt.close()
        f = plt.figure(figsize=(12,8))
        Np = 2
        gs,p=gridspec.GridSpec(2,1),[]
        for gsi in gs:
            p.append(plt.subplot(gsi))
        pm=np.array(p).reshape([2,1])
        gs.update(left=0.11,right=0.93)
        gs.update(bottom=0.08,top=0.97)
        gs.update(hspace=0.07,wspace=0.03)
        p=pm.flatten()

        gs.update(left=0.42)
        gs2=gridspec.GridSpec(1,1)
        gs2.update(left=0.02,right=0.34)
        gs2.update(bottom=0.08,top=0.97)
        pmap=plt.subplot(gs2[0])


        # plot the stresses
        h=[]
        for kc in range(0,len(icmp)):
            for k in range(0,len(istress)):
                hh,=p[0].plot_date(tms,stress[kc,k,:]/1000,color=scols[k],
                                   linestyle=lsty[kc],label=slbls[k],marker=None,
                                   xdate=True)
                h.append(hh)
        h=np.array(h).reshape([len(icmp),len(istress)])
        p[0].set_ylabel('stress (kPa)')
        p[0].set_xlim(tranger)

        if len(icmp)>1:
            lgc=p[0].legend(h[:,0],np.array(self.stresstypes)[icmp])
        else:
            p[0].set_ylabel(self.stresstypes[icmp[0]]+' stress (kPa)')

        # plot the loads
        hl=[]
        if ld.size:
            ylm=general.minmax(ld/self.load_label()[1])
        else:
            ylm=np.array([0.,0.])
        for k in range(0,len(iload)):
            hh,=p[1].plot_date(ltms,ld[k,:]/self.load_label()[1],color=lcols[k],
                               linestyle='-',label=llbls[k],marker=None,xdate=True)
            hl.append(hh)
        p[1].set_ylabel(self.load_label()[0])
        if np.diff(ylm)[0]>0:
            ylm=general.minmax(ylm,1.1)
        else:
            ylm=np.array([0.,1.])
        p[1].set_ylim(ylm)
        p[1].set_xlim(tranger)
        f.autofmt_xdate()
        p[0].set_xticklabels([])

        if self.load_type in ['snow','groundwater','oceanheight']:
            nax=p[1].twinx()
            nax.set_ylim(ylm*(1000*10/1000))
            nax.set_ylabel('pressure equivalent (kPa)')
        
        

        pmap,tform = startmap(pmap,region=self.region)
        for k in range(0,len(istress)):
            hsloc,=pmap.plot(slons[k],slats[k],marker='*',transform=ccrs.Geodetic(),
                             color=scols[k],markersize=6,linestyle='none')

        for k in range(0,len(iload)):
            hsloc,=pmap.plot(llons[k],llats[k],marker='s',transform=ccrs.Geodetic(),
                             color=lcols[k],markersize=6,linestyle='none')

        if prt:
            fname=trange[0].strftime('%Y-%b-%d')+'_'+trange[1].strftime('%Y-%b-%d')
            fname='stress_with_'+self.load_label()[2]+'_'+fname
            if usefiltered:
                flmi='{:0.2f}-{:0.2f}'.format(self.flm[0],self.flm[1])
                fname=fname+'_'+flmi.replace('.','p')
            graphical.printfigure(fname,f)

    def plot_example_load(self,icmp=6,redostress=True,tloc=[]):
        """
        :param          icmp: which components to plot
        :param    redostress: do the load read-in and stress calculation too
        :param          tloc: any tremor locations to plot
        """

        icmp=np.atleast_1d(icmp)
        Np=len(icmp)
        
        plt.close()
        f = plt.figure(figsize=(4,6))
        gs,p=gridspec.GridSpec(Np,1),[]
        for gsi in gs:
            p.append(plt.subplot(gsi))
        pm=np.array(p).reshape([Np,1])
        gs.update(left=0.08,right=0.85)
        gs.update(bottom=0.08,top=0.97)
        gs.update(hspace=0.17,wspace=0.03)
        p=pm.flatten()
        fs='medium'


        if redostress:
            trange=datetime.datetime(2011,8,1)
            trange=[trange,trange+datetime.timedelta(days=1)]
            self.read_load(trange=trange)
            mprs=89547
            self.prs=self.prs-mprs
            self.calcstress()
            self.rotatetointerface()

        # meanload=np.dot(self.lwgts,self.prs)/np.sum(self.lwgts)
        # print('meanload is {:0.0f}'.format(meanload))

        if len(tloc)>0:
            tloc=np.unique(tloc,axis=0)
        
        lonlim,latlim=[-126,-122],[47,50]
        for k in range(0,Np):
            p2,tform = startmap(p[k],region=self.region,
                                  lonlim=lonlim,latlim=latlim)

            stress=self.stresstensor[icmp[k],:,0]/1000.
            ylm=np.median(np.abs(stress))*3.
            
            h=p2.scatter(self.defm.lon,self.defm.lat,c=stress,
                         vmin=-ylm,vmax=ylm,transform=ccrs.Geodetic(),
                         cmap='seismic')

            if len(tloc)>0:
                ht=p2.scatter(tloc[:,0],tloc[:,1],c='k',
                              transform=ccrs.Geodetic(),marker='*',
                              s=12)


            
        ps=p2.get_position()
        psc=[ps.x1+0.02,0.3,0.04,0.5]
        cbs = f.add_axes(psc)
        cb = f.colorbar(h,cax=cbs,orientation='vertical',
                        ticklocation='right')
        cbs.tick_params(axis='y',labelsize=9)
        cb.set_label(self.stresstypes[icmp[0]]+' stress (kPa)',fontsize=fs)

        fname='AM_example_load_'+self.stresstypes[icmp[0]]
        graphical.printfigure(fname,f)
            
    def plot_simple_load(self,icmp=[6,7]):
        """
        :param        icmp: which components to plot
        """

        Nc=len(icmp)
        Np=len(icmp)+1

        plt.close()
        f = plt.figure(figsize=(4,12))
        gs,p=gridspec.GridSpec(Np,1),[]
        for gsi in gs:
            p.append(plt.subplot(gsi))
        pm=np.array(p).reshape([Np,1])
        gs.update(left=0.08,right=0.85)
        gs.update(bottom=0.08,top=0.97)
        gs.update(hspace=0.17,wspace=0.03)
        p=pm.flatten()

        trange=datetime.datetime(2011,8,1)
        trange=[trange,trange+datetime.timedelta(days=1)]
        self.read_load(trange=trange)
        #pload.prs[:,:]=1.
        mprs=90000.
        prs=self.prs[:,0]-mprs
        meanload=np.dot(self.lwgts,prs)/np.sum(self.lwgts)

        pgrd,plon,plat=general.tomatrix(np.vstack([self.lons,self.lats]).T,prs)
        pgrd=pgrd[:,:,0]
        plon=general.modhalf(plon,360)

        
        lonlim,latlim=[-127,-120],[45,54]
        for k in range(0,Np):
            p[k],tform = startmap(p[k],region=self.region,
                                  lonlim=lonlim,latlim=latlim)

        p[0].scatter(self.lons,self.lats,c=prs,transform=tform,cmap='bone')
        p[0].pcolormesh(plon,plat,pgrd,transform=tform,
                        cmap='bone')
        
        import code
        code.interact(local=locals())

    def plotload_time(self,iplt=None,p=None,trange=None):
        """
        plot pressure with time
        :param     iplt: which points to plot (default: all, or up to 20)
        :param        p: the axis to plot to  (default: created)
        :param   trange: the time range to plot  (default: all available)
        """

        
        if iplt is None:
            iplt=np.arange(0,np.minimum(self.prs.shape[0],10))
        iplt=np.atleast_1d(iplt)
        N=len(iplt)

        # get the loads and the times
        ld,tms=self.return_load()

        # only some locations?
        ld=ld[iplt,:]
        
        # only some times?
        if trange is not None:
            ii=np.logical_and(tms>=trange[0],tms<=trange[1])
            ld=ld[:,ii]
        else:
            trange=general.minmax(tms)
            
        # times
        tms=np.array([matplotlib.dates.date2num(tm) for tm in tms])
        tranger=np.array([matplotlib.dates.date2num(tm) for tm in trange])

        # coloring
        cols=graphical.colors(N)

        # create the plots
        if p is None:
            plt.close()
            f = plt.figure(figsize=(8,5))
            gs,p=gridspec.GridSpec(1,1),[]
            for gsi in gs:
                p.append(plt.subplot(gsi))
            pm=np.array(p).reshape([1,1])
            gs.update(left=0.08,right=0.85)
            gs.update(bottom=0.08,top=0.97)
            gs.update(hspace=0.17,wspace=0.03)
            p=pm.flatten()[0]

        # label the locations
        lbls=['{:0.1f} W, {:0.1f} N'.format(self.lons[iplt[k]],self.lats[iplt[k]])
              for k in range(0,N)]
        
        # go ahead and plot
        h=[]
        for k in range(0,N):
            hh,=p.plot_date(tms,ld[k,:]/self.load_label()[1],
                            color=cols[k],
                            marker=None,linestyle='-',label=lbls[k])
            h.append(hh)
        p.set_ylabel(self.load_label()[0])
        p.set_xlim(tranger)

        # make a legend
        lg=p.legend(h,lbls)

        # return in case it will be used elsewhere
        return p,h,lg


    def load_label(self):
        """
        :return        llab: a label for the load in question
        :return        lscl: a scaling factor to divide by
        :return        slab: a short label
        """

        lscl=1.
        
        if self.load_type is 'pressure':
            llab = 'surface pressure (kPa)'
            lscl = 1000.
        elif self.load_type is 'groundwater':
            llab = 'column groundwater (m water equivalent)'
        elif self.load_type is 'snow':
            llab = 'snow depth (m water equivalent)'
        elif self.load_type is 'waves':
            llab = 'wave height (m)'
        elif self.load_type is 'oceanheight':
            llab = 'ocean height (m)'
        else:
            llab = 'combined surface pressure (kPa)'

        # the short name
        if isinstance(self.load_type,str):
            slab=self.load_type
        else:
            slab='combined'
            
        return llab,lscl,slab

    def plotload_space(self,iplt=0):
        """
        plot the pressure distribution used
        :param      iplt: which of the times to use for calculation
        """

        # the values
        lon,ilon=np.unique(self.lons,return_inverse=True)
        lat,ilat=np.unique(self.lats,return_inverse=True)
        
        # plot some values
        iplt=np.atleast_1d(iplt)
        plt.close()
        f = plt.figure(figsize=(8,iplt.size*5))
        gs,p=gridspec.GridSpec(iplt.size,1),[]
        for gsi in gs:
            p.append(plt.subplot(gsi))
        pm=np.array(p).reshape([iplt.size,1])
        gs.update(left=0.08,right=0.85)
        gs.update(bottom=0.08,top=0.97)
        gs.update(hspace=0.17,wspace=0.03)
        p=pm.flatten()

        clm=(general.minmax(self.prs[:,iplt])-1e5)/1e3

        # set these values
        for k in range(0,iplt.size):
            vls=np.zeros(lon.size*lat.size)
            vls[ilon+ilat*lon.size]=(self.prs[:,iplt[k]]-1e5)/1e3
            vls=vls.reshape([lat.size,lon.size])

            h=p[k].pcolormesh(lon,lat,vls,vmin=clm[0],vmax=clm[1])

        ps=p[0].get_position()
        psc=[ps.x1+0.02,0.2,0.04,0.6]

        cbs = f.add_axes(psc)
        cb = f.colorbar(h,cax=cbs,orientation='vertical',
                        ticklocation='right')
        cbs.tick_params(axis='y',labelsize=9)
        cb.set_label('surface pressure difference (kPa)',fontsize=9)


    def plotgf(self,iplt=0,icmp=2):
        """
        plot the pressure distribution used
        :param      iplt: which of the times to use for calculation
        """


        # the values
        lon,ilon=np.unique(self.lons,return_inverse=True)
        lat,ilat=np.unique(self.lats,return_inverse=True)
        
        # plot some values
        iplt=np.atleast_1d(iplt)
        icmp=np.atleast_1d(icmp)
        plt.close()
        f = plt.figure(figsize=(6*icmp.size,iplt.size*5))
        gs,p=gridspec.GridSpec(iplt.size,icmp.size),[]
        for gsi in gs:
            p.append(plt.subplot(gsi))
        pm=np.array(p).reshape([iplt.size,icmp.size])
        gs.update(left=0.08,right=0.75)
        gs.update(bottom=0.08,top=0.97)
        gs.update(hspace=0.17,wspace=0.03)
        p=pm.flatten()

        clm=[general.minmax(self.gf[ii,:,:][iplt,:]) for ii in icmp]

        # set these values
        for k in range(0,iplt.size):
            for kc in range(0,icmp.size):
                vls=np.zeros(lon.size*lat.size)
                vls[ilon+ilat*lon.size]=self.gf[icmp[kc],iplt[k],:]
                vls=vls.reshape([lat.size,lon.size])

                sm = np.sum(vls)

                
                h=pm[k,kc].pcolormesh(lon,lat,vls,vmin=clm[kc][0],vmax=clm[kc][1])

        ps=p[0].get_position()
        psc=[ps.x1+0.02,0.2,0.04,0.6]

        cbs = f.add_axes(psc)
        cb = f.colorbar(h,cax=cbs,orientation='vertical',
                        ticklocation='right')
        cbs.tick_params(axis='y',labelsize=9)
        cb.set_label('stress per pressure change (kPa)',fontsize=9)

    def rotatetointerface(self):
        """
        rotate to compute shear (updip positive), normal (tension positive), 
        and volumetric (average pressure, tension positive)
        for each point on the interface
        """    

        # want the amount rotated counterclockwise and updip
        self.defm = self.defm_f()
        theta = -self.defm.strike.reshape([self.defm.strike.size,1])
        phi = -self.defm.dip.reshape([self.defm.dip.size,1])

        # rotate to get new stresses
        strs = rotatestresses(self.stresstensor[0:6,:,:],theta,phi)

        # grab the correct stresses
        if self.region =='Parkfield':
            shear = -strs[5:6,:,:]
            # was shear = -strs[4:5,:,:]
        else:
            shear = -strs[4:5,:,:]
            # was shear = -strs[5:6,:,:]
        normal = strs[2:3,:,:]
        volum = np.sum(strs[0:3,:,:],axis=0).reshape(shear.shape)

        # collect
        self.stresstensor=np.vstack([self.stresstensor[0:6,:,:],shear,normal,volum])
        self.stresstypes=['EE','NN','ZZ','EN','EZ','NZ','shear','normal','volumetric']

        # filtered too, if applicable
        if 'stresstensorf' in list(self.__dict__.keys()):
            # rotate to get new stresses
            strs = rotatestresses(self.stresstensorf[0:6,:,:],theta,phi)
            
            # grab the correct stresses
            if self.region =='Parkfield':
                shear = -strs[5:6,:,:]
            else:
                shear = -strs[4:5,:,:]
            normal = strs[2:3,:,:]
            volum = np.sum(strs[0:3,:,:],axis=0).reshape(shear.shape)
        
            # collect
            self.stresstensorf=np.vstack([self.stresstensorf[0:6,:,:],shear,normal,volum])

    def differential_shear(self):
        """

        """

        # where to save new stresses
        idiff,ipred=9,10
        ndiff,npred=11,12
        nmax=np.max([ipred,idiff,ndiff,npred])+1

        # which stresses to calculate for
        stresses=[]
        if 'stresstensor' in self.__dict__.keys():
            if self.stresstensor.shape[0]>=8:
                if self.stresstensor.shape[0]<nmax:
                    sz=list(self.stresstensor.shape)
                    self.stresstensor=np.append(self.stresstensor,
                                                np.ndarray([nmax-sz[0]]+sz[1:],dtype=float),
                                                axis=0)
                stresses.append(self.stresstensor)
        if 'stresstensorf' in self.__dict__.keys():
            if self.stresstensorf.shape[0]>=8:
                if self.stresstensorf.shape[0]<nmax:
                    sz=list(self.stresstensorf.shape)
                    self.stresstensorf=np.append(self.stresstensorf,
                                                 np.ndarray([nmax-sz[0]]+sz[1:],dtype=float),
                                                 axis=0)
                stresses.append(self.stresstensorf)

        # the indices of the components
        if len(stresses):
            ishear=np.where(np.array(self.stresstypes)=='shear')[0][0]
            inorm=np.where(np.array(self.stresstypes)=='normal')[0][0]

        for stress in stresses:
            # values
            shear=stress[ishear,:,:]
            normal=stress[inorm,:,:]
            nloc,nvl=shear.shape[0],shear.shape[1]
            
            # demean
            shear=shear-np.ma.mean(shear,axis=1).reshape([nloc,1])
            normal=normal-np.ma.mean(normal,axis=1).reshape([nloc,1])

            # to get ratio
            rts=np.ma.sum(np.multiply(shear,normal),axis=1)
            # normal to shear
            rtn=np.divide(rts,np.ma.sum(np.power(shear,2),axis=1))
            self.normalratio=rtn
            # shear to normal
            rts=np.divide(rts,np.ma.sum(np.power(normal,2),axis=1))
            self.shearratio=rts

            # and compute predictions
            shear,normal=shear.reshape([1,nloc,nvl]),normal.reshape([1,nloc,nvl])
            rts,rtn=np.maximum(rts,0.),np.maximum(rtn,0.)
            rts=rts.reshape([1,nloc,1])
            rtn=rtn.reshape([1,nloc,1])

            stress[ipred,:,:]=np.multiply(rts,normal)
            stress[idiff,:,:]=stress[ishear:ishear+1,:,:]-stress[ipred:ipred+1,:,:]
            stress[npred,:,:]=np.multiply(rtn,shear)
            stress[ndiff,:,:]=stress[inorm:inorm+1,:,:]-stress[npred:npred+1,:,:]

        if len(self.stresstypes)<nmax:
            self.stresstypes=list(self.stresstypes)+['unknown']*(nmax-len(self.stresstypes))
            self.stresstypes[ipred]='shear from normal'
            self.stresstypes[idiff]='independent shear'
            self.stresstypes[npred]='normal from shear'
            self.stresstypes[ndiff]='independent normal'

    def remove_pressure_correlated(self):
        """
        remove the signals that have nonzero correlation with atmospheric 
        pressure
        """

        # note time range and spacing
        trange=general.minmax(self.tms)
        trange[0]=trange[0]-datetime.timedelta(days=10)
        trange[1]=trange[1]+datetime.timedelta(days=10)
        tspc=np.diff(self.tms[0:2])[0].total_seconds()/3600.

        # read the averages atm pressure        
        mprs,ptms=median_atm_pressure(rgn=self.region,trange=trange,tspc=tspc)
                                      
        # and remove the correlated component
        self.remove_correlated(xcsig=mprs,txc=ptms)
            
    def remove_correlated(self,xcsig,txc=None):
        """
        calculate the shear and normal stresses that differ 
        from the multiplication of some other signal
        :param         xcsig: the other signal
        :param           txc: times of the other signals 
                      (default: assumed to be the same)
        """

        # note time in hours
        if txc is None:
            txc=self.tmsh.copy()
        txc=np.array([(tm-self.tref).total_seconds()/3600
                      for tm in txc])
        
        
        # where to save new stresses
        idiffs,idiffn=13,14
        nmax=np.max([idiffs,idiffn])+1

        # which stresses to calculate for
        stresses=[]
        if 'stresstensor' in self.__dict__.keys():
            if self.stresstensor.shape[0]>=8:
                if self.stresstensor.shape[0]<nmax:
                    sz=list(self.stresstensor.shape)
                    self.stresstensor=np.append(self.stresstensor,
                                                np.ndarray([nmax-sz[0]]+sz[1:],dtype=float),
                                                axis=0)
                stresses.append(self.stresstensor)
        if 'stresstensorf' in self.__dict__.keys():
            if self.stresstensorf.shape[0]>=8:
                if self.stresstensorf.shape[0]<nmax:
                    sz=list(self.stresstensorf.shape)
                    self.stresstensorf=np.append(self.stresstensorf,
                                                 np.ndarray([nmax-sz[0]]+sz[1:],dtype=float),
                                                 axis=0)
                stresses.append(self.stresstensorf)

            # if there's a filtered version, filter it too
            tmsf,fxcsig=filtertimeseries(txc,xcsig,self.flm/24)
            fxcsig=fxcsig.flatten()
        else:
            # if it's unfiltered, just copy
            fxcsig=xcsig.copy()

        # interpolate to the desired times
        fxcsig=np.interp(self.tmsh,txc,fxcsig)
        nml=np.ma.sum(np.power(fxcsig,2))
        fxcsig=fxcsig.reshape([1,fxcsig.size])
        xcsig=np.interp(self.tmsh,txc,xcsig)
        
        # the indices of the components
        if len(stresses):
            ishear=np.where(np.array(self.stresstypes)=='shear')[0][0]
            inorm=np.where(np.array(self.stresstypes)=='normal')[0][0]

            # compute the x-c with the last value (should be the filtered version)
            stress=stresses[-1]

            # values
            shear=stress[ishear,:,:]
            normal=stress[inorm,:,:]
            nloc,nvl=shear.shape[0],shear.shape[1]
            
            # demean
            shear=shear-np.ma.mean(shear,axis=1).reshape([nloc,1])
            normal=normal-np.ma.mean(normal,axis=1).reshape([nloc,1])
                        
            # to get ratios
            rts=np.ma.sum(np.multiply(shear,fxcsig),axis=1)/nml
            rtn=np.ma.sum(np.multiply(normal,fxcsig),axis=1)/nml
            self.normalxc=rtn
            self.shearxc=rtn

            # and compute predictions: here for the filtered version
            shear,normal=shear.reshape([1,nloc,nvl]),normal.reshape([1,nloc,nvl])
            rts=rts.reshape([1,nloc,1])
            rtn=rtn.reshape([1,nloc,1])
            fxcsig=fxcsig.reshape([1,1,nvl])

            stress[idiffs,:,:]=shear-np.multiply(rts,fxcsig)
            stress[idiffn,:,:]=normal-np.multiply(rtn,fxcsig)

            # and for the unfiltered version, using the same scaling
            stress=stresses[0]
            xcsig=xcsig.reshape([1,1,nvl])
            shear=stress[ishear:ishear+1,:,:]
            normal=stress[inorm:inorm+1,:,:]

            stress[idiffs,:,:]=shear-np.multiply(rts,xcsig)
            stress[idiffn,:,:]=normal-np.multiply(rtn,xcsig)
            
        if len(self.stresstypes)<nmax:
            self.stresstypes=list(self.stresstypes)+['unknown']*(nmax-len(self.stresstypes))
            self.stresstypes[idiffn]='uncorrelated normal'
            self.stresstypes[idiffs]='uncorrelated shear'


            
    def binbyshearratio(self,bnlm_s2n=None,bnlm_n2s=None):
        """
        bin the locations by their shear to normal scaling factor
        :param  bnlm_s2n: the bin limits desired for shear to normal factor (default: created)
        :param  bnlm_n2s: the bin limits desired for normal to shear factor (default: created)
        """

        # default bin limits
        if bnlm_s2n is None:
            bnlm_s2n=np.array([-10.,-.1,.1,10.])

        if bnlm_n2s is None:
            bnlm_n2s=np.array([-100.,-1,1,100.])

        # bin
        irat=np.searchsorted(bnlm_s2n,self.shearratio)
        msk=np.logical_or(irat==0,irat==len(bnlm_s2n))
        self.is2n=np.ma.masked_array(irat-1,mask=msk)
        self.bnlm_s2n=bnlm_s2n

        irat=np.searchsorted(bnlm_n2s,self.normalratio)
        msk=np.logical_or(irat==0,irat==len(bnlm_n2s))
        self.in2s=np.ma.masked_array(irat-1,mask=msk)
        self.bnlm_n2s=bnlm_n2s


    def plotshearratio(self,justsign=False,prt=True,plotn2s=True):
        """
        plots the scaling factor to get from normal to shear
        :param    justsign: just plot the sign (default: False)
        :param         prt: print to a figure (default: True)
        :param     plotn2s: also plot the normal to shear ratio
        :return          p: handle to the plots
        """
        

        plt.close()
        if plotn2s:
            Np=2
        else:
            Np=1
        f = plt.figure(figsize=(4.+3.*Np,7))
        gs,p=gridspec.GridSpec(2,Np,height_ratios=[1,0.05]),[]
        for gsi in gs:
            p.append(plt.subplot(gsi))
        pm=np.array(p).reshape([2,Np])
        cax=pm[1,:]
        p=pm[0,:]
        gs.update(left=0.08,right=0.97)
        gs.update(bottom=0.08,top=0.97)
        gs.update(hspace=0.17,wspace=0.03)

        for k in range(0,Np):
            p[k],tform = startmap(p[k],region=self.region)
        lon,lat=general.modhalf(self.defm.lon,360),self.defm.lat
        rts=self.shearratio
        rtn=self.normalratio
        if justsign:
            rts=np.sign(rts)
            rtn=np.sign(rtn)
            
        clm=general.minmax(rts)
        clm=np.max(np.abs(rts))*np.array([-1.,1])

        clmn=general.minmax(rtn)
        clmn=np.max(np.abs(rtn))*np.array([-1.,1])

        self.binbyshearratio()

        hh=p[0].scatter(lon,lat,marker='^',transform=ccrs.Geodetic(),
                        c=rts,s=6,vmin=clm[0],vmax=clm[1],cmap='RdYlBu')
        cb=plt.colorbar(hh,cax=cax[0],orientation='horizontal')
        for xvl in (self.bnlm_s2n-clm[0])/(clm[1]-clm[0]):
            cax[0].annotate("",xy=(xvl,-0.1),xycoords='axes fraction',
                            xytext=(xvl,1.1),textcoords='axes fraction',
                            arrowprops=dict(arrowstyle='-'))
        if justsign:
            cb.set_label('sign of shear to normal factor')
        else:
            cb.set_label('shear to normal factor')

            
        if plotn2s:
            mks=graphical.markers(len(self.bnlm_n2s)-1)
            for k in range(0,len(self.bnlm_n2s)-1):
                ii=self.in2s==k
                hh=p[1].scatter(lon[ii],lat[ii],marker=mks[k],transform=ccrs.Geodetic(),
                                c=rtn[ii],s=6,vmin=clmn[0],vmax=clmn[1],cmap='RdYlBu')
            cb=plt.colorbar(hh,cax=cax[1],orientation='horizontal')
            for xvl in (self.bnlm_n2s-clmn[0])/(clmn[1]-clmn[0]):
                cax[1].annotate("",xy=(xvl,-0.1),xycoords='axes fraction',
                                xytext=(xvl,1.1),textcoords='axes fraction',
                                arrowprops=dict(arrowstyle='-'))
            if justsign:
                cb.set_label('sign of normal to shear factor')
            else:
                cb.set_label('normal to shear factor')


        if prt:
            fname='shear2normal_'+self.load_label()[2]
            graphical.printfigure(fname,f)

        return p.flatten()

    def plot_stress_amps(self,prt=True,icmp=[6,7],usefiltered=True):
        """
        plots the amplitudes of the stresses
        :param         prt: print to a figure (default: True)
        :param        icmp: which components of stress
        :param usefiltered: use the filtered stresses?
        """
        

        plt.close()
        fs=12
        Np=len(icmp)
        f = plt.figure(figsize=(4.+3.*Np,7))
        gs,p=gridspec.GridSpec(2,Np,height_ratios=[1,0.05]),[]
        for gsi in gs:
            p.append(plt.subplot(gsi))
        pm=np.array(p).reshape([2,Np])
        cax=pm[1,:]
        p=pm[0,:]
        gs.update(left=0.08,right=0.97)
        gs.update(bottom=0.08,top=0.97)
        gs.update(hspace=0.17,wspace=0.03)

        for k in range(0,Np):
            p[k],tform = startmap(p[k],region=self.region)
        lon,lat=general.modhalf(self.defm.lon,360),self.defm.lat

        icmp=np.atleast_1d(icmp).astype(int)
        if usefiltered:
            stress=self.stresstensorf
        else:
            stress=self.stresstensor
        stress=np.ma.std(stress[icmp,:,:],axis=2)

        cmap='RdYlBu'
        cmap='gist_rainbow_r'
        for k in range(0,Np):
            vl=stress[k,:]/1000.
            clm=general.minmax(vl)
            clm=[0.,4.]
            hh=p[k].scatter(lon,lat,marker='^',transform=ccrs.Geodetic(),
                            c=vl,s=6,vmin=clm[0],vmax=clm[1],cmap=cmap)
            cb=plt.colorbar(hh,cax=cax[k],orientation='horizontal')
            cb.set_label(self.stresstypes[icmp[k]]+' stress (kPa)',fontsize=fs)
            p[k].tick_params(axis='y',labelsize=9)
            
        if prt:
            fname='stress_amps_'+self.region+'_'+self.load_label()[2]
            if usefiltered:
                fname=fname+'_{:0.1f}-{:0.1f}'.format(self.flm[0],self.flm[1])
            fname=fname.replace('.','p')
            graphical.printfigure(fname,f)

    def filterstresses(self,flm=[0.,float('inf')]):
        """
        :param      flm: frequency limits in day^-1
        """

        # save filter info
        self.flm=np.array(flm)

        if flm[0]==0 and np.isinf(flm[1]):
            self.stresstensorf = self.stresstensor.copy()
        else:
            # time spacing in days
            dtim=np.diff(self.tms[0:2])[0].total_seconds()/86400
            # Nyquist frequency
            nfreq=0.5/dtim
            # frequencies as a fraction of Nyquist
            flm=np.array(flm)/nfreq

            # create filter
            if flm[0]==0:
                b,a=signal.butter(N=5,Wn=flm[1],btype='lowpass')
            elif flm[1]>0.95:
                b,a=signal.butter(N=5,Wn=flm[0],btype='highpass')
            else:
                b,a=signal.butter(N=5,Wn=flm,btype='bandpass')
                
            # remove the mean
            stress=self.stresstensor
            mns=np.mean(stress,axis=2)
            mns=mns.reshape(list(mns.shape)+[1])

            # apply filter
            npad=int(30/dtim)
            self.stresstensorf=signal.filtfilt(b,a,stress-mns,padlen=npad)

    def assignphases(self,usefiltered=True):
        """
        assign phases between 0 and 360 to the times of each part of the signal
        :param    usefiltered: use stresstensorf instead of stresstensor
        (default: True)
        """

        # which stresses to use
        if usefiltered:
            stress = self.stresstensorf
            self.phasefiltered=True
        else:
            stress = self.stresstensor
            self.phasefiltered=False
            
        # initialize
        iperi=np.arange(0,stress.shape[2])
        self.phases=np.ma.masked_array(np.ndarray(stress.shape,dtype=float),
                                      mask=False)
        
        # just loop through
        for kc in range(0,stress.shape[0]):
            for kl in range(0,stress.shape[1]):
                
                # increasing or decreasing?
                idf=stress[kc,kl,1:]>stress[kc,kl,0:-1]
                
                # find the minima and maxima
                imax=np.logical_and(idf[0:-1],~idf[1:])
                imin=np.logical_and(~idf[0:-1],idf[1:])

                imin=np.where(imin)[0]+1
                imax=np.where(imax)[0]+1
                
                # make a list of the extrema
                if imin.size:
                    if imin[0]<imax[0]:
                        iex=np.insert(imax,np.arange(0,imin.size),imin)
                    else:
                        iex=np.insert(imax,np.arange(1,imin.size+1),imin)
                else:
                    iex=imax.copy()

                # shift each point for a more accurate peak
                shf=(stress[kc,kl,iex+1]-stress[kc,kl,iex-1])/2.
                denom=stress[kc,kl,iex+1]+stress[kc,kl,iex-1]-2*stress[kc,kl,iex]
                denom[denom==0.]=float('inf')
                shf=np.divide(shf,denom)
                iex=iex+shf

                # decide which cycle each point is in
                # one cycle is 2 integers
                icycle=np.searchsorted(iex,np.arange(0,stress.shape[2]))
                
                # the start of the half-periods
                hstar=np.hstack([0,iex])
                
                # the half-periods of interest
                hper=np.hstack([-1,np.diff(iex),-1])

                if imin.size and imax.size:

                    # if the last value was a minimum
                    if np.min(imin)<np.min(imax):
                        ishf=(np.arange(0,hper.size)-0) % 2
                    else:
                        ishf=(np.arange(0,hper.size)-1) % 2 
                        
                    # where we are in the half period
                    iper = (np.divide(iperi-hstar[icycle],hper[icycle]) 
                            - ishf[icycle])*180


                    # add mask if necessary
                    iper=np.ma.masked_array(iper, \
                          mask=np.logical_or(icycle==0,icycle==hper.size-1))

                    # add to set
                    self.phases[kc,kl,:]=iper

                else:
                    # if no minima or maxima were found
                    self.phases.mask[kc,kl,:]=True

        # go ahead and bin the phases
        self.binphases()
        
    def binphases(self,nbin=10,btype='stress',usefiltered=True):
        """
        :param          nbin: number of bins
        :param         btype: how to bin---by 'stress' or 'phases'
        :param   usefiltered: use filtered value, for stress
        """

        # save the number of bins
        self.nbins=nbin
        
        if btype in ['phase','phases']:
            # binning
            self.phasebins=np.linspace(-180,180,int(np.round(nbin+1)))
            
            # separate
            self.iphases=np.ma.masked_array(np.searchsorted(self.phasebins[1:],self.phases),
                                            mask=self.phases.mask,side='left')

            # note the phase type
            self.bintype='phase'
            
        elif btype in ['stress','stresses']:

            if usefiltered:
                stress = self.stresstensorf
            else:
                stress = self.stresstensor
                
            # select a different bin for each stress type
            bns=np.ma.std(stress,axis=2)
            bns.mask=np.logical_or(bns.mask,bns==0)
            bns=np.ma.median(bns,axis=1)
            bns=bns.reshape([1,bns.size])

            # relative to std
            nbin=int(np.round(nbin+1))
            self.nstressbins=np.linspace(-3,3,nbin)
            self.nstressbins=np.logspace(np.log10(.1),np.log10(3),int(nbin/2))
            self.nstressbins=np.append(self.nstressbins,-self.nstressbins)
            self.nstressbins.sort()
            
            self.stressbins=self.nstressbins.reshape([nbin,1])
            self.stressbins=np.multiply(self.stressbins,bns)
            Ns=self.stressbins.shape[1]
            
            # mask below and above bins
            llm=self.stressbins[0,:].reshape([Ns,1,1])
            ulm=self.stressbins[-1,:].reshape([Ns,1,1])
            msk=np.logical_or(stress<llm,stress>ulm)
            msk=np.logical_or(msk,stress==0.)
            self.iphases=np.ndarray(msk.shape,dtype=int)
            
            # for each stress type
            for k in  range(0,Ns):
                self.iphases[k,:,:]=np.searchsorted(self.stressbins[1:,k],
                                                    stress[k:k+1,:,:])
            self.iphases=np.ma.masked_array(self.iphases,mask=msk)

            # note the phase type
            self.bintype='stress'
            
    def masklowpressure(self,ptime=None,prs=None,flm=[0.,float('inf')],pmin=-300):
        """
        :param     ptime: pressure times
        :param       prs: pressure values
        :param       flm: a frequency to filter to
        :param      pmin: minimum pressure to leave unmasked
        """

        if ptime is None or prs is None:
            ptime=self.tms
            prs=self.meanload

        # pressure times in seconds
        tref=np.min(ptime)
        ptms=np.array([(tm-tref).total_seconds() for tm in ptime])

        # filter
        prs=prs-np.ma.mean(prs)
        if flm[0]>0 or flm[1]<1e8:
            ptms,prs=filtertimeseries(ptms,prs,np.array(flm)/86400)
            prs=prs.flatten()

        # interpolate to the times of interest
        tms=np.array([(tm-tref).total_seconds() for tm in ptime])
        msk=np.interp(tms,ptms,prs)<pmin

        # apply mask
        msk=msk.reshape([1,1,msk.size])
        self.iphases.mask=np.logical_or(self.iphases.mask,msk)
        #self.phases.mask=np.logical_or(self.phases.mask,msk)

        self.pmin=pmin
        
    def displayphases(self,tdur=None,icmp=None):
        """
        to show an example of the phase interval
        """

        # pick a duration
        if tdur is None:
            if self.flm[0]>0 or not np.isinf(self.flm[1]):
                tdur=self.flm[np.logical_and(self.flm>0,~np.isinf(self.flm))]
                tdur=3./np.mean(tdur)
            else:
                tdur=5.

        # number of points
        tspc=np.diff(self.tms)[0].total_seconds()/86400.
        npts=int(tdur/tspc)

        # pick a component
        if icmp is None:
            if self.phases.shape[0]>=6:
                icmp=6
            else:
                icmp=2

        # a location
        iloc = np.random.choice(self.phases.shape[1],1)[0]

        # find an acceptable time interval
        phs= np.ma.masked_array([0.,],mask=True)
        while np.sum(phs.mask):
            ist=np.random.choice(self.phases.shape[2]-npts-1,1)[0]
            ii=np.arange(ist,ist+npts)
            phs=self.phases[icmp,iloc,ii]

        # the stresses
        if self.phasefiltered:
            stress=self.stresstensorf[icmp,iloc,ii]/1000
        else:
            stress=self.stresstensor[icmp,iloc,ii]/1000

            
        plt.close()
        f = plt.figure(figsize=(8,5))
        gs,p=gridspec.GridSpec(2,1),[]
        for gsi in gs:
            p.append(plt.subplot(gsi))
        pm=np.array(p).reshape([2,1])
        gs.update(left=0.11,right=0.98)
        gs.update(bottom=0.08,top=0.97)
        gs.update(hspace=0.05,wspace=0.03)
        p=pm.flatten()

        
        # timing
        tms=np.arange(0,npts)*tspc
        tms=np.array([matplotlib.dates.date2num(tm) for tm in self.tms[ii]])

        # limint
        ylm = general.minmax(stress,1.05)



        # identify zeros and 180
        phs = phs % 360.

        imin=phs>180
        imin=np.where(np.logical_and(~imin[0:-1],imin[1:]))[0]

        imax=modhalf(phs,360) > 0
        imax=np.where(np.logical_and(~imax[0:-1],imax[1:]))[0]

        use360=False
        if use360:
            plm=[0,360]
            
            tmsp=np.insert(tms,imax+1,np.float('nan'))
            phsp=np.insert(phs,imax+1,np.float('nan'))
            p[0].plot_date(general.minmax(tms),[180,18],color='k',linestyle='-.',
                           marker=None,linewidth=0.4)
        else:
            plm=[-180,180]
            phs=modhalf(phs,360)
            tmsp=np.insert(tms,imin+1,np.float('nan'))
            phsp=np.insert(phs,imin+1,np.float('nan'))
            p[0].plot_date(general.minmax(tms),[0,0],color='k',linestyle='-.',
                           marker=None,linewidth=0.4)


        lwi=0.6
        dtim=tms[1]-tms[0]
        for ix in imin:
            shf=general.modhalf(phs[ix:ix+2]-180,360)
            shf=(shf[0]/np.sum(shf)-0.5)*dtim/2.
            shf=0.
            hmin,=p[0].plot_date(np.ones(2)*(shf+np.mean(tms[ix:ix+2])),plm,
                                 color='k',linestyle=':',marker=None,
                                 linewidth=lwi)
            hmin,=p[1].plot_date(np.ones(2)*(shf+np.mean(tms[ix:ix+2])),ylm,
                                 color='k',linestyle=':',marker=None,
                                 linewidth=lwi)

        for ix in imax:
            shf=general.modhalf(phs[ix:ix+2]-0,360)
            shf=(shf[0]/np.sum(shf)-0.5)*dtim/2.
            shf=0.
            hmax,=p[0].plot_date(np.ones(2)*np.mean(tms[ix:ix+2]+shf),plm,
                                 color='k',linestyle='--',marker=None,
                                 linewidth=lwi)
            hmax,=p[1].plot_date(np.ones(2)*np.mean(tms[ix:ix+2]+shf),ylm,
                                 color='k',linestyle='--',marker=None, 
                                 linewidth=lwi)


        hphs,=p[0].plot_date(tmsp,phsp,color='k',marker=None,linestyle='-',
                             linewidth=2)

        hst,=p[1].plot_date(tms,stress,color='k',marker=None,linestyle='-', 
                            linewidth=2.)

        for ph in p:
            ph.set_xlim(general.minmax(tms))
            
        graphical.delticklabels(pm)

        p[0].set_ylim(plm)
        p[1].set_ylim(ylm)
        p[0].set_yticks(np.arange(plm[0],plm[1]+0.01,90))
        p[0].set_ylabel('phase (degrees)')
        p[1].set_ylabel(self.stresstypes[icmp]+' stress (kPa)')
        fmt=matplotlib.dates.DateFormatter('%d %b')
        p[1].xaxis.set_major_formatter(fmt)

        graphical.printfigure('phase_illustration',f)

    def save_stresses(self,fnameadd=''):
        """
        save the stresses to a text file so they can be read in
        :param        fnameadd: a string to add to the default file name
        """

        # file name
        fdir=os.path.join(os.environ['DATA'],'TREMORMOD','SAVEDSTRESSES')
        fname=self.load_label()[2]+'_'+self.defm_f().region+fnameadd
        #fname=fname+'_'+self.tms[0].strftime('%Y-%b-%d')
        #fname=fname+'_'+self.tms[-1].strftime('%Y-%b-%d')
        fname=os.path.join(fdir,fname)
        fname2=fname+'_data.npy'
        fname3=fname+'_meanload.npy'

        fl=open(fname,'w')
        # write all the locations
        fl.write(','.join(['{:0.5f}'.format(vl) for vl in self.defm.lon])+'\n')
        fl.write(','.join(['{:0.5f}'.format(vl) for vl in self.defm.lat])+'\n')

        # note the components used
        icmp=np.arange(0,6)
        fl.write(','.join(['{:s}'.format(self.stresstypes[ix]) for ix in icmp]))
        fl.write('\n')

        # write the times
        fmt='%Y-%b-%d-%H-%M-%S'
        fl.write(','.join([tm.strftime(fmt) for tm in self.tms]))
        fl.close()

        # write the stresses
        stress=self.stresstensor[icmp,:,:]
        if isinstance(stress,np.ma.masked_array):
            stress.data[stress.mask]=999999
            stress=stress.data
        np.save(fname2,stress)

        # write the mean load
        stress=self.meanload.copy()
        if isinstance(stress,np.ma.masked_array):
            stress.data[stress.mask]=999999
            stress=stress.data
        np.save(fname3,stress)

        
    def read_stresses(self,fnameadd='',trange=None):
        """
        save the stresses to a text file so they can be read in
        :param        fnameadd: a string to add to the default file name
        :param          trange: a time range to read in (default: all)
        """

        # file name
        fdir=os.path.join(os.environ['DATA'],'TREMORMOD','SAVEDSTRESSES')
        fname=self.load_label()[2]+'_'+self.defm_f().region+fnameadd
        #fname=fname+'_'+self.tms[0].strftime('%Y-%b-%d')
        #fname=fname+'_'+self.tms[-1].strftime('%Y-%b-%d')
        fname=os.path.join(fdir,fname)
        fname2=fname+'_data.npy'
        fname3=fname+'_meanload.npy'

        # read the locations, components, times
        fl = open(fname,'r')
        lon=np.array(fl.readline().split(',')).astype(float)
        lat=np.array(fl.readline().split(',')).astype(float)
        cmps=fl.readline().split(',')
        cmps=[cmp.strip() for cmp in cmps]
        fmt='%Y-%b-%d-%H-%M-%S'
        tms=fl.readline().split(',')
        tms=np.array([datetime.datetime.strptime(tm.strip(),fmt) for tm in tms])
        fl.close()

        # find the closest points
        igrab=findnearest(self.defm.lon,self.defm.lat,lon,lat)
        
        # compute the distances
        dst=np.multiply(general.modhalf(lon[igrab]-self.defm.lon,360),
                        np.cos(self.defm.lat*np.pi/180))
        dst=np.power(dst,2)+np.power(lat[igrab]-self.defm.lat,2)
        dst=np.power(dst,0.5) * deg2km()
        print('Maximum distance from desired points: {:0.1f} km'.format(np.max(dst)))

        # and read the rest
        stress=np.load(fname2)

        # if there were masked values
        msk=stress==999999
        if np.sum(msk):
            stress=np.ma.masked_array(stress,mask=msk)

        # and read the mean load
        meanload=np.load(fname3)

        # if there were masked values
        msk=meanload==999999
        if np.sum(msk):
            meanload=np.ma.masked_array(meanload,mask=msk)

        if trange is not None:
            ii=np.logical_and(tms>=trange[0],tms<=trange[1])
            stress=stress[:,:,ii]
            tms=tms[ii]
            meanload=meanload[ii]
        
        # save these values 
        self.stresstensor=stress[:,igrab,:]
        self.tms=tms
        self.meanload=meanload
        self.stresstypes=cmps
        self.computehourstime(tref=None)
        if 'stresstensorf' in self.__dict__.keys():
            self.__delattr__('stresstensorf')
            

#-------------START OF COMBINED LOADS CLASS--------------------------------------

class combinedload(surfload):

    def additional_init(self):

        # make a list of load types
        self.load_type=[sl.load_type for sl in self.sloads]

        # make sure the deformation points are the same for all
        for sload in self.sloads:
            sload.defm_f=self.defm_f


    def calcstress(self):
        """
        multiply the Green's functions by the loads to get the stresses
        """

        # just compute for each load
        for sload in self.sloads:
            sload.calcstress()


    def calcstress_throughtime(self,trange,twin=None,usesaved=False,tspc=3.):
        """
        consider a range of time windows, load the surface information, calculate the stress
        :param    trange: time range to consider
        :param      twin: max length of time window in days (default: None, picked in sloads)
        :param  usesaved: use saved values where available? (default: False)
        :param      tspc: time sampling desired in hours (default: 3)
        """

        # just compute for each load
        for sload in self.sloads:
            sload.calcstress_throughtime(trange=trange,twin=twin,usesaved=usesaved,tspc=tspc)

        # sum the stresses
        self.sum_stresses()


    def sum_stresses(self):
        """
        sum the stresses produced by the various loads
        """

        # the various times, in hours since 1900
        tref=datetime.datetime(1900,1,1)
        tms=[[(tm-tref).total_seconds()/3600 for tm in sload.tms]
             for sload in self.sloads]

        # get the range of dates
        t1=np.max([tm[0] for tm in tms]).round()
        t2=np.min([tm[-1] for tm in tms]).round()
        tspc=np.max([np.median(np.diff(tm)) for tm in tms]).round()
        tdes=np.arange(t1,t2+tspc*1e-4,tspc)

        # set these times
        self.tref = tref
        self.tmsh=tdes
        self.tms=np.array([tref+datetime.timedelta(hours=tm) for tm in tdes])

        # initialize stress tensor to zero
        nloc=self.defm.lon.size
        self.stresstensor=np.zeros([6,nloc,self.tms.size],dtype=float)

        # add contributions from each set
        for k in range(0,len(self.sloads)):
            ix=general.closest(tms[k],self.tmsh)
            self.stresstensor=self.stresstensor+self.sloads[k].stresstensor[0:6,:,ix]

        # note the types of stresses
        self.stresstypes=self.sloads[0].stresstypes[0:6]

        # just copy one of the loads
        self.meanload = self.sloads[0].meanload.copy()

        
        
#------START OF ECMWF (ATMOSPHERIC PRESSURE AND GROUNDWATER/SNOW) LOAD CLASS------

class ecmwfload(surfload):

    def additional_init(self):
        """
        placeholder for the sub-classes
        """

        # set the function to read data
        self.pick_load_to_read(load_type=self.load_type)

        # the folders that contain the data
        self.pressure_dir = os.path.join(os.environ['DATA'],'ECMWF','PRESSURE')
        self.snow_dir = os.path.join(os.environ['DATA'],'ECMWF','SNOW')
        self.water_dir = os.path.join(os.environ['DATA'],'ECMWF','WATER')
        self.wave_dir = os.path.join(os.environ['DATA'],'ECMWF','WAVES')
        self.wind_dir = os.path.join(os.environ['DATA'],'ECMWF','WIND')
        self.pick_data_directory()

    def pick_data_directory(self):
        """
        note the directory with data
        """
        
        if self.load_type is 'pressure':
            self.dir_with_files=self.pressure_dir
        if self.load_type is 'snow':
            self.dir_with_files=self.snow_dir
        elif self.load_type in 'groundwater':
            self.dir_with_files=self.water_dir
        elif self.load_type in 'waves':
            self.dir_with_files=self.wave_dir
        elif self.load_type in 'wind':
            self.dir_with_files=self.wind_dir
    
    def init_load_locs(self):
        """
        the default locations
        will be overriden in each set
        :return        lons: set of longitudes, in degrees
        :return        lats: set of latitudes, in degrees
        :return        dlon: longitude spacing for each box, in degrees
        :return        dlat: latitude spacing for each box, in degrees
        :return        wgts: a weighting to assign to each point
        """

        # read pressures just to get a grid
        prs,lons,lats,tms=self.read_load_fun(fname=None,justone=True) 
        dlon=np.abs(np.median(np.diff(lons[0,:])))
        dlat=np.abs(np.median(np.diff(lats[:,0])))
        lons,lats=lons.flatten(),lats.flatten()

        # since I want one box size per point
        dlon=dlon*np.ones(lons.size,dtype=float)
        dlat=dlat*np.ones(lons.size,dtype=float)

        if self.load_type in ['snow','groundwater','pressure']:
            # but for values that are only on land,
            # weight by fraction of each point that's on land
            wgts=slabgeom.frac_land(lons,lats,dlon,dlat,10,10)
        elif self.load_type in ['waves']:
            # but for values that are only on water,
            # weight by fraction of each point that's on water
            wgts=1.-slabgeom.frac_land(lons,lats,dlon,dlat,10,10)
        else: #self.load_type is 'pressure': # includes 'wind'
            # default weighting is one per box, values everywhere
            wgts=np.ones(lons.size,dtype=float)

        return lons,lats,dlon,dlat,wgts

    def readpressurepoints(self,loc=None,trange=None):
        """
        read the pressure time series for certain points
        note this deletes previously used Green's functions and other data
        :param      loc: locations of interest
        :param   trange: time range of interest
        """

        # read pressures just to get a grid
        fname='pressure_2011-08-01_2011-09-01.nc'
        prs,lons,lats,tms=read_surface_pressure(fname,justone=True) 
        lons,lats=lons.flatten(),lats.flatten()

        # find the closest values to each point
        loc = np.atleast_2d(loc)
        iuse=[]
        for k in range(0,loc.shape[0]):
            dst=np.power(modhalf(lons-loc[k,0],360),2)*np.cos(math.pi/180*loc[k,1]) \
                 +np.power(lats-loc[k,1],2)
            iuse.append(np.argmin(dst))

        # initialize calculations
        self.initcalc(iok=np.array(iuse))

        # and read the data
        self.read_total_load(trange=trange)

    def unsphere_gf_units(self):
        """
        remove the spherical components of the area coefficients
        """
        
        scl = np.divide(np.cos(math.pi/180*np.median(self.lats)),
                        np.cos(math.pi/180*self.lats))
        scl = scl.reshape([1,1,scl.size])

        self.gf = np.multiply(self.gf,scl)

    def change_gf_units(self):
        """
        convert the GF for N to GF for pressure given the grid spacing
        """

        # compute area of each cell in m^2, 
        # assuming 1 degree longitude = 1 degree latitude
        d2k = deg2km()
        area = np.multiply(self.dlon,self.dlat) * d2k**2 * 1e6
        
        # adjust areas by the appropriate reduction in longitude size
        areas = np.multiply(np.cos(math.pi/180*self.lats),area)

        # multiply by fraction of box in the ocean
        areas = np.multiply(areas,self.lwgts)

        # and multiply to get pressure GF
        self.gf = np.multiply(self.gf,areas.reshape([1,1,areas.size]))
        
        if self.load_type is 'pressure':
            # turns out to be unitless
            # Pa stress on intervals for Pa stress on surface
            self.gfunit='Pa / Pa'
        elif self.load_type in ['groundwater','snow','waves']:
            # groundwater and snow are read in equivalent water depth in m
            # multiply by density and gravitational acceleration
            self.gf = self.gf * (1000*9.8)
            self.gfunit = 'Pa / m'
        elif self.load_type in ['wind']:
            # can compute loads for wind, but doesn't make sense
            self.gfunit = 'nonsense'
        elif not isinstance(self.load_type,str):
            # if it's a combined load, all the loads will have been converted to pressure
            self.gfunit='Pa / Pa'

    def pick_load_to_read(self,load_type='pressure'):
        """
        choose the function to read in the surface load
        :param    load_type: which load---'pressure' (default), 
                                 'groundwater', or 'snow'
        """

        if load_type is 'pressure':
            self.read_load_fun = read_surface_pressure
        elif load_type is 'snow':
            self.read_load_fun = read_snow_depth
        elif load_type is 'groundwater':
            self.read_load_fun = read_groundwater
        elif load_type in ['wave','waves']:
            self.read_load_fun = read_wave_height
        elif load_type in ['wind']:
            self.read_load_fun = read_wind_speed
        elif not isinstance(self.load_type,str):
            self.read_load_fun = read_surface_pressure
        else:
            print('No reading function available for '+load_type)
            print('Possible loads are pressure, snow, waves, wind, and groundwater')

    def read_total_load(self,trange=None):
        """
        :param     trange: the time range to read
        """

        if isinstance(self.load_type,str):
            # if there's only one load to read, just read it
            self.read_load(trange=trange)
        else:
            # but if there are several, need to read them and convert to pressure
            load_types=copy.copy(self.load_type)

            # will collect all the values before combining
            tms,prs=[],[]

            for loadt in load_types:
                # change the function to read the load
                self.load_type=loadt
                self.pick_load_to_read(load_type=loadt)

                # and note where the data are
                self.pick_data_directory()

                # actually read the values
                self.read_load(trange=trange)

                # convert to pressure if needed
                if loadt in ['groundwater','snow']:
                    self.prs=self.prs*(1000*9.8)

                # add to set
                tms.append(self.tms.copy())
                prs.append(self.prs.copy())

            # combine the loads
            import code
            code.interact(local=locals())
                
            # reset descriptions
            self.load_type=load_types
            self.load_units='Pa'
            
    def read_load(self,trange=None):
        """
        :param     trange: the time range to read
        """

        # identify the available times
        fls=glob.glob(os.path.join(self.dir_with_files,'*.nc'))
        trng=np.array([os.path.split(fname)[1].split('.')[0].split('_') for fname in fls]) 
        t1=np.array([t.split('-') for t in trng[:,1]]).astype(int)
        t1=np.array([datetime.datetime(t1[k,0],t1[k,1],t1[k,2]) 
                     for k in range(0,t1.shape[0])])
        t2=np.array([t.split('-') for t in trng[:,2]]).astype(int)
        t2=np.array([datetime.datetime(t2[k,0],t2[k,1],t2[k,2]) 
                     for k in range(0,t2.shape[0])])

        if trange is None:
            # use a wide range if not given
            trange= [np.min(t1),np.max(t2)]
        self.trange=trange

        # make sure the files are in order
        ix=np.argsort(t1)
        t1,t2,fls=t1[ix],t2[ix],np.array(fls)[ix]

        # which files
        ifls=np.logical_and(t1<=trange[1],t2>trange[0])
        fls=np.array(fls)[ifls]

        # initialize
        self.prs=np.ndarray([self.iuse.size,0])
        self.tms=np.array([])
        self.ltms=np.array([])
        
        for fname in fls:
            
            # read this section
            prs,lons,lats,tms=self.read_load_fun(fname,ikp=self.iuse,
                                                 trange=self.trange)   
            self.prs=np.append(self.prs,prs,axis=1)
            self.tms=np.append(self.tms,tms)
            self.ltms=np.append(self.ltms,tms)

        # avoid duplicates
        self.tms,ix=np.unique(self.tms,return_index=True)
        self.prs=self.prs[:,ix]
        self.ltms=self.ltms[ix]

        # note units
        self.time_units = 'hours since 1900-Jan-01'
        if self.load_type is 'pressure':
            self.load_units='Pa'
        elif self.load_type in ['groundwater','snow','waves']:
            self.load_units='m'
        elif self.load_type in ['wind']:
            self.load_units='m/s'

        # waves---mask if needed
        if self.load_type in ['waves']:
            self.prs=np.ma.masked_array(self.prs,mask=self.prs<=0.)

    def return_load(self):
        """
        :return     ld: the load [# of locations by # of times]
        :return   ltms: the load times
        """

        if 'ltms' in self.__dict__.keys():
            ltms=self.ltms
        else:
            ltms=np.arange(0,100).astype(float)
            ltms=np.array([datetime.datetime(2010,1,1)+datetime.timedelta(hours=tm)
                           for tm in ltms])

        if 'prs' in self.__dict__.keys():
            ld=self.prs
        else:
            ld=np.ndarray([len(self.lons),len(ltms)],dtype=float)
            ld=np.ma.masked_array(ld,mask=np.ones(ld.size,dtype=bool))
            
            
        return ld,ltms
        



#-------------------END OF ATM LOAD CLASS--------------------------------------

#----------------START OF OCEAN HEIGHT LOAD CLASS--------------------------

class oceanload(surfload):

    def additional_init(self):
        """
        additional info to save on initialization
        """

        self.load_type='oceanheight'
        
    
    def read_tidegage(self,trange=None):
        """
        read all the tide gage data
        :param      trange: time range to read (default: 2008-2019)
        """

        # select some stations
        stats,trash,trash,trash=tidegage_stationlist(region=self.region)
        statdel=irrelevant_stations()
        stats=np.array(list(set(stats)-set(statdel)))

        # read
        tdes,trefi,self.wlev,self.statinfo,self.stats = \
            read_tidegage_all(datades='original',stats=stats,trange=trange)
        self.load_units='m'

        # make two copies so that one remains unfiltered
        self.wlev_original=self.wlev.copy()

        # frequency limits
        self.flm_load=np.array([0.,float('inf')])
        
        # pick a reference time and change to hours since 1900
        self.tref=datetime.datetime(1900,1,1)
        self.ltmsh=((trefi-self.tref).total_seconds()+tdes)/3600.
        self.time_units = 'hours since 1900-Jan-01'
        self.ltms=np.array([self.tref+datetime.timedelta(hours=tm)
                            for tm in self.ltmsh])


    def remove_tides(self):
        """
        remove the tides from the tide gage records
        """

        # compute the fit and corrections
        flm=[0.5,6]
        cfs,pers,tref,prd,self.wlev=remove_tides(self.ltms,self.wlev,flm=flm)
        
    def filter_tidegage(self,flm=[0.1,0.5]):
        """
        :param      flm: frequency limits in day^-1
        """
        
        # frequency limits
        flm=np.array(flm)
        self.flm_load=flm

        # filter and save
        self.ltmsh,self.wlev=filtertimeseries(self.ltmsh,self.wlev_original,flm=flm/24.)

        # new times
        self.ltms=np.array([self.tref+datetime.timedelta(hours=tm) 
                            for tm in self.ltmsh])

    def stations(self,prnt=True):
        """
        :return    statnum: a list of the station numbers in order
        :return   statname: a list of the station names in order
        :return       lons: a list of the station longitudes in order
        :return       lats: a list of the station latitudes in order
        """

        stats = np.array(list(self.statinfo.keys()))
        stats = self.stats

        statname=np.array([self.statinfo[stat]['statname'] for stat in stats])
        statnum=np.array([self.statinfo[stat]['statnum'] for stat in stats])
        lons=np.array([self.statinfo[stat]['longitude'] for stat in stats])
        lats=np.array([self.statinfo[stat]['latitude'] for stat in stats])

        if prnt:
            fmt='{:>2d}: {:7d}, {:37s} {:3.2f} W, {:2.2f} N'
            for k in range(0,len(stats)):
                print(fmt.format(k,statnum[k],statname[k],-lons[k],lats[k]))

        return statnum,statname,lons,lats

    def pickloadlocs(self,locdes=None):
        """
        :param    locdes: desired locations, if you know which ones are wanted
        :return     locs: locations of some stations
        :return    igrab: indices of those stations
        """

        # preferred locations
        if locdes is None:
            locdes=someloadloc_water(self.region)
        locdes=np.atleast_2d(locdes)

        # nearby tide gages
        statnum,statname,lons,lats=self.stations(prnt=False)

        # find the nearest stations
        igrab=findnearest(locdes[:,0],locdes[:,1],lons,lats)
        locs=np.vstack([lons[igrab],lats[igrab]]).T

        # for ease of plotting
        locs[:,0]=general.modhalf(locs[:,0],360)
        
        return locs,igrab
        
        
    def plot_tidegage(self,iplt=None,filtered=True,dur=100,plotmean=True,
                      plotdiff=True,plotmap=True,trange=None):
        """
        :param      iplt: which of the stations to plot (default: 3 random)
        :param  filtered: plot the filtered data? (default: True)
        :param       dur: duration to plot in days (default: 100)
        :param  plotmean: also plot the mean over stations (default: True)
        :param  plotdiff: plot differences from the mean (default: True)
        :param   plotmap: also plot a map of the stations? (default: True)
        """

        # which stations to plot
        nstat=self.wlev.shape[1]
        if iplt is None:
            iplt = np.random.choice(nstat,3,replace=False)
            iplt=np.array(iplt)
        iplt=np.atleast_1d(iplt)
        N=len(iplt)
        
        # coloring
        cols=graphical.colors(N)

        # which portion to plot
        dtim=np.ma.median(np.diff(self.ltmsh))/24.
        nvl=int(np.ceil(dur/dtim))
        if trange is not None:
            ii=general.closest(self.ltms,np.array(trange))
            ii=np.arange(ii[0],ii[1]+1)
        else:
            ii = nvl*2+np.random.choice(self.ltmsh.size-nvl*3-nvl*2,1)[0]
            ii = np.arange(ii,ii+nvl)

        # times
        tms=np.array([matplotlib.dates.date2num(tm) for tm in self.ltms[ii]])
        

        plt.close()
        if plotdiff:
            f = plt.figure(figsize=(12,10))
            Np = 2
        else:
            f = plt.figure(figsize=(12,5))
            Np = 1
        gs,p=gridspec.GridSpec(2,1),[]
        for gsi in gs:
            p.append(plt.subplot(gsi))
        pm=np.array(p).reshape([2,1])
        gs.update(left=0.11,right=0.97)
        gs.update(bottom=0.08,top=0.97)
        gs.update(hspace=0.17,wspace=0.03)
        p=pm.flatten()

        if plotmap:
            gs.update(left=0.4)
            gs2=gridspec.GridSpec(1,1)
            gs2.update(left=0.11,right=0.35)
            gs2.update(bottom=0.08,top=0.97)
            pmap=plt.subplot(gs2[0])

        # which stations, sort by latitude
        statname=self.stats
        lons=np.array([self.statinfo[statname[k]]['longitude'] for k in iplt])
        lats=np.array([self.statinfo[statname[k]]['latitude'] for k in iplt])
        ix=np.flipud(np.argsort(lats))
        iplt,lons,lats=iplt[ix],lons[ix],lats[ix]
        statname=[statname[k] for k in iplt]

        # labels
        lbls=[]
        for stat in statname:
            stati=self.statinfo[stat]
            lon,lat=stati['longitude'],stati['latitude']
            if lon<0:
                lbls.append('{:>6s}, '.format(str(stat))+'{:0.1f} W, {:0.1f} N'.format(-lon,lat))
            else:
                lbls.append('{:>6s}, '.format(str(stat))+'{:0.1f} E, {:0.1f} N'.format(lon,lat))
            lbls[-1]=lbls[-1]+' '+stati['statname']

        # which data to plot
        if filtered:
            data=self.wlev[ii,:]
        else:
            data=self.wlev_original[ii,:]
        data = data[:,iplt]

        # plot
        h=[]
        for k in range(0,N):
            hh,=p[0].plot_date(tms,data[:,k],color=cols[k],linewidth=2,
                               marker=None,linestyle='-',label=lbls[k])
            h.append(hh)

        if plotmean:
            hm,=p[0].plot_date(tms,self.wlev_mean[ii],color='gray',linewidth=3,
                               marker=None,linestyle='--',label='mean')


        if plotdiff:
            datadf=data-self.wlev_mean[ii].reshape([data.shape[0],1])
            for k in range(0,N):
                hh,=p[1].plot_date(tms,datadf[:,k],
                                   color=cols[k],linewidth=2,
                                   marker=None,linestyle='-',label=lbls[k])
            p[1].set_ylim(np.max(np.abs(datadf.flatten()))*1.05*np.array([-1,1]))

        if plotmean or plotdiff:
            datadf=data-self.wlev_mean[ii].reshape([data.shape[0],1])
            vr = np.var(data,axis=0)
            vrdf = np.var(datadf,axis=0)
            for k in range(0,len(lbls)):
                lbls[k]=lbls[k]+', '+'{:>3.0f}%'.format((1-vrdf[k]/vr[k])*100)

        if filtered:
            flb='{:g} - {:g}'.format(1/self.flm_load[1],1/self.flm_load[0])
            flb='water height, filtered to '+flb+' days (m)'
        else:
            flb='water height (m)'
        for ph in p:
            ph.set_ylabel(flb)
            ph.set_xlim(general.minmax(tms))
        if plotdiff:
            p[1].set_ylabel('residual '+flb)
        p[0].set_ylim(np.max(np.abs(data.flatten()))*1.05*np.array([-1,1]))

        lg=p[0].legend(h+[hm],lbls+['mean'])

        # map
        if plotmap:
            pmap,tform = startmap(pmap,region=self.region)
            statnumi,statnamei,lonsi,latsi=self.stations(prnt=False)
            pmap.plot(lonsi,latsi,marker='^',transform=ccrs.Geodetic(),
                      color='gray',markersize=6,linestyle='none')
            for k in range(0,len(statname)):
                pmap.plot(lons[k],lats[k],marker='^',transform=ccrs.Geodetic(),
                          color=cols[k],markersize=10)
                pmap.text(lons[k]+0.5,lats[k],str(statname[k]),
                          transform=ccrs.Geodetic(),
                          color=cols[k])


    def meanoceanheight(self,tweight=20):
        """
        compute a mean ocean height from all the stations
        :param    tweight: time to allow smoothing in in days (default: 20)
        """

        # weight by distance from a data edge according to a cosine function
        dtim=np.median(np.diff(self.ltmsh))
        nwgt=int(np.round(tweight*24/dtim))
        wgt=(np.arange(0,nwgt+1)/nwgt-1.)*np.pi
        wgt=(np.cos(wgt)+1)/2.
        
        # number of stations
        nstat=self.wlev.shape[1]

        # some weights
        wgts = np.ones(self.wlev.shape,dtype=float)
        igrd = np.arange(0,self.wlev.shape[0])
        for k in range(0,nstat):
            # find out how far each point is from a masked point
            imsk=np.where(self.wlev.mask[:,k])[0]
            if imsk.size:
                idf=general.closest(imsk,igrd)
                idf=(np.abs(imsk[idf]-igrd)).astype(int)
                idf=np.minimum(idf,wgt.size-1)
                wgts[:,k]=wgt[idf]

        # multiply and average
        self.wlev_mean=np.sum(np.multiply(self.wlev,wgts),axis=1)
        self.wlev_mean=np.divide(self.wlev_mean,np.sum(wgts,axis=1))

        # throw away if more than half the stations are missing
        if isinstance(self.wlev,np.ma.masked_array):
            self.wlev_mean.mask=np.sum(self.wlev.mask,axis=1)>nstat/2.

        # calculate percentage of variance accounted for
        vr = np.ma.var(self.wlev,axis=0)
        vrdf = np.ma.var(self.wlev-self.wlev_mean.reshape([self.wlev_mean.size,1]),axis=0)
        self.varmean = 1-np.divide(vrdf,vr)
        


    def init_load_locs(self,dstmax=None,dspcmax=20.,dspcmin=2.):
        """
        :param       dstmax: maximum distance in degrees to consider 
                                 from the deformation points
        :param         dspc: grid spacing in km 
        :return        lons: set of longitudes, in degrees
        :return        lats: set of latitudes, in degrees
        :return        dlon: longitude spacing for each box, in degrees
        :return        dlat: latitude spacing for each box, in degrees
        :return        wgts: a weighting to assign to each point
        """


        # default max distance
        if dstmax is None:
            dstmax=self.dstmax

        # make sure we're referring to the right deformation object
        self.defm=self.defm_f()
            
        # latitude limits
        latlim=general.minmax(self.defm.lat)+np.array([-1,1])*dstmax

        # longitude limits
        lonrt=math.cos(np.max(self.defm.lat)*np.pi/180.)
        lonlim=np.minimum(180,dstmax/lonrt)
        lonlim=general.minmax(self.defm.lon)+np.array([-1,1])

        # values
        lonrt=np.maximum(lonrt,0.1)

        # change spacing to degrees
        dspcmax=dspcmax/deg2km()
        dspcmin=dspcmin/deg2km()

        # make a list of edges
        lon=int(np.ceil(np.diff(lonlim)/(dspcmax*lonrt)))+1
        lon=np.linspace(lonlim[0],lonlim[1],lon)
        dlon=np.diff(lon)[0]
        lat=int(np.ceil(np.diff(latlim)/dspcmax))+1
        lat=np.linspace(latlim[0],latlim[1],lat)
        dlat=np.diff(lat)[0]

        # and a grid
        lon,lat=np.meshgrid(lon,lat)
        lon,lat=lon.flatten(),lat.flatten()

        # initialize
        lons,lats=np.array([],dtype=float),np.array([],dtype=float)
        dlons,dlats=np.array([],dtype=float),np.array([],dtype=float)

        # shifts to divide as a fraction of dlon or dlat
        xdiv,ydiv=2,2
        xnew=np.linspace(-0.5,0.5,xdiv+1)
        xnew=(xnew[0:-1]+xnew[1:])/2.
        ynew=np.linspace(-0.5,0.5,ydiv+1)
        ynew=(ynew[0:-1]+ynew[1:])/2.
        xnew,ynew=np.meshgrid(xnew,ynew)
        xnew,ynew=xnew.flatten(),ynew.flatten()
    
        import global_land_mask

        # keep going until get to minimum grid size
        while (dlat>dspcmin or dlon*lonrt>dspcmin) and lon.size:
            # check what's on the ocean
            isoc=global_land_mask.is_ocean(lat,lon)

            # try shifting up or down---is the result still on land or sea?
            frc_land=slabgeom.frac_land(lon,lat,dlon,dlat,xdiv=10,ydiv=10)
                
            # could be added to set now, if they're in the ocean
            iadd=np.logical_and(frc_land==0.,isoc)
            lons=np.append(lons,lon[iadd])
            lats=np.append(lats,lat[iadd])
            dlons=np.append(dlons,dlon*np.ones(np.sum(iadd),dtype=float))
            dlats=np.append(dlats,dlat*np.ones(np.sum(iadd),dtype=float))

            # continue on with those that need to be split
            inow=np.logical_and(~iadd,frc_land<1.)
            lon,lat=lon[inow],lat[inow]
            lon=lon.reshape([lon.size,1])+(dlon*xnew).reshape([1,xnew.size])
            lat=lat.reshape([lat.size,1])+(dlat*ynew).reshape([1,ynew.size])
            lon,lat=lon.flatten(),lat.flatten()
            dlon,dlat=dlon/xdiv,dlat/ydiv

        # add anything that's left
        lons=np.append(lons,lon)
        lats=np.append(lats,lat)
        dlons=np.append(dlons,dlon*np.ones(lon.size,dtype=float))
        dlats=np.append(dlats,dlat*np.ones(lon.size,dtype=float))

        # also compute a weight for each one
        wgts=1.-slabgeom.frac_land(lons,lats,dlons,dlats,xdiv=10,ydiv=10)

        return lons,lats,dlons,dlats,wgts

    def checkboxes(self,lonlim=np.array([-128,-123]),latlim=np.array([46,52])):

        # initial map
        pmap,tform = startmap(lonlim=lonlim,latlim=latlim)
        
        # left and right edges
        x0=self.lons-self.dlon/2.
        x1=self.lons+self.dlon/2.

        # bottom and top
        y0=self.lats-self.dlat/2.
        y1=self.lats+self.dlat/2.

        # only some
        ii=np.logical_and(x1>=lonlim[0],x0<lonlim[1])
        ii=np.logical_and(ii,y1>=latlim[0])
        ii=np.logical_and(ii,y0<=latlim[1])
        x0,x1,y0,y1=x0[ii],x1[ii],y0[ii],y1[ii]

        # the sets of values
        xvl=np.vstack([x0,x1,x1,x0,x0])
        yvl=np.vstack([y0,y0,y1,y1,y0])


        pmap.plot(xvl,yvl,marker=None,transform=ccrs.Geodetic(),
                  linestyle='-')

    def change_gf_units(self):
        """
        convert the GF for N to GF for ocean load given the grid spacing
        """

        # compute area of each cell in m^2, 
        # assuming 1 degree longitude = 1 degree latitude
        d2k = deg2km()
        area = np.multiply(self.dlon,self.dlat) * d2k**2 * 1e6
        
        # adjust areas by the appropriate reduction in longitude size
        areas = np.multiply(np.cos(math.pi/180*self.lats),area)

        # multiply by fraction of box in the ocean
        areas = np.multiply(areas,self.lwgts)
        
        # and multiply to get pressure GF
        self.gf = np.multiply(self.gf,areas.reshape([1,1,areas.size]))

        # but here we'd prefer the stress change per change in ocean height in m
        # density * g
        pres_per_meter = 1000. * 9.8
        self.gf = self.gf * pres_per_meter

        
        # Pa stress on intervals for m change in ocean height
        self.gfunit='Pa / m'

        
        
    def set_load_mean(self):
        """
        set the load to compute to be the mean ocean height,
        with a weighting of 1 for each point
        """

        # how it varies with time
        self.load_with_time=self.wlev_mean.reshape([self.wlev_mean.size,1])

        # and with space
        self.load_with_space=np.ones([self.lons.size,1])

    
    def calcstress(self):
        """
        calculate the stress at each point on the fault for all available times
        """

        # calculate the stresses for each load
        # EE, NN, ZZ, EN, EZ, NZ
        stress_per_load = np.dot(self.gf,self.load_with_space)

        # save the mean load
        self.meanload = self.wlev_mean.copy()
        
        # and multiply by time to sum
        self.stresstensor = np.dot(stress_per_load,self.load_with_time.T)

        # copy a set of time values
        self.tms=self.ltms.copy()
        
    def calcstress_throughtime(self,trange=None,twin=None,usesaved=False,tspc=3.):
        """
        read the relevant data and calculate the stresses
        :param         trange: time range to calculate for
        :param           twin: for a time spacing (will be ignored)
        :param  usesaved: use saved values where available? (default: False)
        :param      tspc: preferred time sampling in hours (default: 3)
        """

        # read the data
        self.read_tidegage(trange=trange)

        # remove the tides
        #self.remove_tides()

        # unless we're doing PCA, don't need to worry about filtering here

        # get the mean ocean height from all the stations
        self.meanoceanheight()

        # divide the loads
        self.set_load_mean()

        if usesaved:
            # read the stresses?
            self.read_stresses(trange=trange)
        else:
            # and calculate the stresses
            self.calcstress()

        # downsample if needed
        self.downsample(tspc=tspc)

        
    def return_load(self,ltype='stations'):
        """
        :param     ltype: which load you want
                         'stations': actually return the values from stations of interest 
                         'usedload': values used in the calculations
        :return       ld: the load [# of locations by # of times]
        :return     ltms: the load times
        """

        if ltype is 'stations':
            # station values
            ld=self.wlev.T
        elif ltype is 'trueload':
            # the values used, repeated per station
            ld=np.repeat(self.load_with_time,len(self.stats),axis=1).T

        return ld,self.ltms
        
        


        
#----------------END OF OCEAN HEIGHT LOAD CLASS--------------------------


#----------------START OF CODES FOR STRESS CALCULATION---------------------

def calc_gf(sloc,dloc,spc,subsamp=0.2,gffun=None,sphdist=True,gfname=None):
    """
    :param       sloc: surface loading location, Nsx2 [lon, lat]
    :param       dloc: location of deformation / induced stresses
                          Ndx3 [lon in deg, lat in deg, depth in km]
    :param        spc: size of the patches Nx2 [dlon in deg, dlat in deg]
    :param    subsamp: sub-sample to get to this fraction of the distance
    :param      gffun: function to actually calculate the GF
    :param    sphdist: use spherical distances (default: True)
    :param     gfname: a GF name, if needed
    :return     gfmat: Green's function matrix [6 x Nd x Ns]
                        unit (Pa / N)
    """

    # make an array
    sloc=np.atleast_2d(sloc)
    dloc=np.atleast_2d(dloc)

    # distances and azimuths
    if sphdist:
        x,az = spheredist(dloc,sloc)
    else:
        x,az = flatdist(dloc,sloc)

    # to min dimensions in degrees
    ddeg=np.maximum(np.cos(np.pi/180*sloc[:,1]),0.05)
    ddeg=np.multiply(ddeg,spc[:,0])
    ddeg=np.minimum(ddeg,spc[:,1])
    ddeg=ddeg.reshape([1,ddeg.size])

    # which ones need to be calculated more precisely
    inew=ddeg>np.maximum(x*subsamp,0.02)
    iid=np.sum(inew,axis=1)>0
    iis=np.sum(inew,axis=0)>0
    jjs=np.where(iis)[0]

    # try some shifts
    N=2
    xshf,yshf=np.linspace(-.5,.5,N+1),np.linspace(-.5,.5,N+1)
    xshf,yshf=(xshf[0:-1]+xshf[1:])/2.,(yshf[0:-1]+yshf[1:])/2.
    xshf,yshf=np.meshgrid(xshf,yshf)
    xshf,yshf=xshf.flatten(),yshf.flatten()
    wgt=1./len(xshf)

    # initialize and compute those with acceptable spacing
    gfmat=np.zeros([6,dloc.shape[0],sloc.shape[0]],dtype=float)
    if np.sum(~iis):
        gfi=gffun(sloc[~iis,:],dloc,sphdist=sphdist,gfname=gfname)
        gfmat[:,:,~iis]=gfi
    if np.sum(~iid):
        gfi=gffun(sloc,dloc[~iid,:],sphdist=sphdist,gfname=gfname)
        gfmat[:,~iid,:]=gfi

    # to compute the average over unresolved locations
    if np.sum(iid) or np.sum(iis):
        gftemp=np.zeros([6,np.sum(iid),np.sum(iis)],dtype=float)
        for k in range(0,len(xshf)):
            # shift by some amount and recompute
            shf=np.vstack([xshf[k]*spc[iis,0],yshf[k]*spc[iis,1]]).T
            gfi=calc_gf(sloc[iis,:]+shf,dloc[iid,:],spc[iis,:]/N,
                        subsamp=subsamp,sphdist=sphdist,gffun=gffun,
                        gfname=gfname)
            gftemp=gftemp+gfi*wgt

        # copy to output
        for k in range(0,len(jjs)):
            gfmat[:,iid,jjs[k]]=gftemp[:,:,k]

    return gfmat

def halfspace_stress_gf(sloc,dloc,sphdist=True,gfname=None):
    """
    :param       sloc: surface loading location, Nsx2 [lon, lat]
    :param       dloc: location of deformation / induced stresses
                            Ndx3 [lon in deg, lat in deg, depth in km]
    :param    sphdist: use spherical distances for computation
                           (default: True)
    :param     gfname: an option for the GF name (not used)
    :return     gfmat: Green's function matrix [6 x Nd x Ns]
                        unit (Pa / N)
    """

    # make an array
    sloc=np.atleast_2d(sloc)
    dloc=np.atleast_2d(dloc)

    # Poisson's ratio
    nu = 0.25
    #print('poissons ratio: {:0.2f}'.format(nu))
    mnu = 1.-2.*nu
    #print('1- 2*poissons ratio: {:0.2f}'.format(mnu))

    # distances and azimuths
    if sphdist:
        x,az = spheredist(dloc,sloc)
    else:
        x,az = flatdist(dloc,sloc)
    az = az + 180

    # azimuth is now the direction from the surface load to the tremor location

    # distances between the points, in meters
    x = x*deg2km()*1000.

    # follow Jaeger et al, page, 409
    # let x/theta be distance along the line from the load to the deformation point
    # changed sign of tauzz, taull, and tautt to make tension positive
    # also changed sign of tautz because Jaeger et al 
    # use positive-negative sign convention

    # depths
    z = (dloc[:,2]*1000.).reshape([dloc.shape[0],1])

    # 3-d distance
    r = np.power(np.power(x,2)+np.power(z,2),0.5)

    # save some normalized values
    xor = np.divide(x,r)
    zor = np.divide(z,r)

    # theta-theta
    tautt=3*np.divide(np.multiply(np.power(xor,2),zor),np.power(r,2))
    tautt=tautt+mnu*np.divide(np.power(zor,2),np.multiply(r,z+r))
    tautt=tautt-mnu*np.divide(zor,np.power(r,2))
    tautt=tautt-mnu*np.divide(np.power(xor,2),np.power(z+r,2))
    tautt=tautt/(-2*math.pi)

    # lambda-lambda
    taull=mnu*np.divide(np.power(xor,2)+np.power(zor,2),np.multiply(r,z+r))
    taull=taull-mnu*np.divide(zor,np.power(r,2))
    taull=taull/(-2*math.pi)

    # z-z
    tauzz=1/(-2*math.pi)*np.divide(3*np.power(zor,3),np.power(r,2))

    # theta-z
    tautz=1/(2*math.pi)*np.divide(3*np.multiply(xor,np.power(zor,2)),np.power(r,2))

    # reshape
    sz=[1]+list(tautt.shape)
    tautt=tautt.reshape(sz)
    taull=taull.reshape(sz)
    tauzz=tauzz.reshape(sz)
    tautz=tautz.reshape(sz)
    az=az.reshape(sz)

    # rotate to allow for azimuths
    # want azr to be the counterclockwise rotation of the axes in radians
    azr=(90-az)*(-math.pi/180)
    cs,sn=np.cos(azr),np.sin(azr)

    # rotate shear on vertical planes
    tauxz=np.multiply(tautz,cs)
    tauyz=np.multiply(tautz,-sn)

    # and now need xx, yy, xy
    # stresses on vertical planes don't matter

    # so only need to rotate tautt and taull
    tauxx = np.multiply(tautt,np.power(cs,2)) + \
            np.multiply(taull,np.power(sn,2))
    tauyy = np.multiply(tautt,np.power(sn,2)) + \
            np.multiply(taull,np.power(cs,2)) 

    tauxy = np.multiply(taull-tautt,np.multiply(sn,cs))

    # create a tensor
    gfmat=np.vstack([tauxx,tauyy,tauzz,tauxy,tauxz,tauyz])

    return gfmat

def rotate_stress(tautt,taull,tauzz,tautz,az):
    """
    :param    tautt: extensional stress along azimuth
    :param    taull: extensional stress perpendicular to azimuth
    :param    tauzz: extensional vertical stress
    :param    tautz: shear stress in azimuth direction on horizontal plane
    :param       az: direction from surface load to tremor location in degrees
    :return  stress: an [6 x Ntremorloc x Nloadloac] array, 
                      where the first dimension indexes
                      xx (EE), yy (NN), zz (vertical), xy, xz, and yz stresses
    """

    # reshape
    sz=[1]+list(tautt.shape)
    tautt=tautt.reshape(sz)
    taull=taull.reshape(sz)
    tauzz=tauzz.reshape(sz)
    tautz=tautz.reshape(sz)
    az=az.reshape(sz)

    # rotate to allow for azimuths
    # want azr to be the counterclockwise rotation of the axes in radians
    azr=(90-az)*(-math.pi/180)
    cs,sn=np.cos(azr),np.sin(azr)

    # rotate shear on vertical planes
    tauxz=np.multiply(tautz,cs)
    tauyz=np.multiply(tautz,-sn)

    # and now need xx, yy, xy
    # stresses on vertical planes don't matter

    # so only need to rotate tautt and taull
    tauxx = np.multiply(tautt,np.power(cs,2)) + \
            np.multiply(taull,np.power(sn,2))
    tauyy = np.multiply(tautt,np.power(sn,2)) + \
            np.multiply(taull,np.power(cs,2)) 

    tauxy = np.multiply(taull-tautt,np.multiply(sn,cs))

    # create a tensor
    stress=np.vstack([tauxx,tauyy,tauzz,tauxy,tauxz,tauyz])

    return stress


def calc_spotl_gf(sloc,dloc,gfname='depth_Amanda',sphdist=True):
    """
    :param       sloc: surface loading location, Nsx2 [lon, lat]
    :param       dloc: location of deformation / induced stresses
                            Ndx3 [lon in deg, lat in deg, depth in km]
    :param    gfname: which GF file to get
    :param   sphdist: use spherical distances (default: True)
    :return    gfmat: Green's function values
    """

    # make an array
    sloc=np.atleast_2d(sloc)
    dloc=np.atleast_2d(dloc)

    # distances and azimuths
    if sphdist:
        x,az = spheredist(dloc,sloc)
    else:
        x,az = flatdist(dloc,sloc)
    az = az + 180
    # azimuth is now the direction from the surface load to the tremor location

    # note distances between the points is in degrees

    # depths in meters
    z = (dloc[:,2]*1000.).reshape([dloc.shape[0],1])

    # read a slice
    sdst,gf,gftyp=read_spotl_gf_slice(gfname=gfname)
    

    # convert strain to stress
    stressxx,stressyy,stresszz=\
        strain_to_stress_surface(gf[:,4],gf[:,5],gf[:,6],
                                 shmod=3e10,pr=0.25)

    # interpolate
    stressxx=np.interp(x.flatten(),sdst,stressxx)
    stressyy=np.interp(x.flatten(),sdst,stressyy)
    stresszz=np.interp(x.flatten(),sdst,stresszz)
    stressxx=stressxx.reshape(az.shape)
    stressyy=stressyy.reshape(az.shape)
    stresszz=stresszz.reshape(az.shape)

    # and rotate
    gfmat=rotate_stress(stressxx,stressyy,stresszz,
                        np.zeros(stressxx.shape),az)

    return gfmat


def read_spotl_gf_slice(gfname='depth_Amanda'):
    """
    :param    gfname: which GF file to get
    :param   sphdist
    :return     dsts: distances
    :return       gf: Green's function values, in values / Pa
    :return    gftyp: types of values returned
    """

    # identify file
    nm=gfname
    fdir=os.path.join(os.environ['DATA'],'SURFACE','GREENFUN')
    if nm.lower() == 'depth_amanda':
        fname='green.contap.sph25'
    fname=os.path.join(fdir,fname)
    # vls=np.loadtxt(nm,skiprows=2,dtype=float)

    # to get started
    fl = open(fname,'r')
    trash = fl.readline()
    ln = fl.readline()
    ln = ln.split()

    # initialize Green's functions
    ngf = int(ln[0])
    gf=np.zeros([0,ngf],dtype=float)
    dsts=np.zeros(0,dtype=float)

    # earth radius in m
    erad=6371000.


    while len(ln):
        # identify centre points of each distance bin
        dst1,dst2,nh=float(ln[4]),float(ln[5]),int(ln[3])
        dsti=np.linspace(dst1,dst2,nh)
        dsts=np.append(dsts,dsti)

        # to normalize to response to 1 N load

        # ring width
        nml=float(ln[6])/360*erad

        # multiply by ring circumference to get right area in m^2
        nml=nml*np.multiply(dsti/360*erad,np.sin(dsti*np.pi/180))
        #nml=np.ones(dsti.size)*nml

        # since the values are the mass response, multiply by gravitational
        # acceleration
        nml=nml * 9.8
        
        # get these values
        for k in range(0,nh):
            vls=np.array(fl.readline().split()).astype(float).reshape([1,ngf])
            gf=np.append(gf,vls/nml[k],axis=0)
            

        # another set?
        ln = fl.readline().split()

    fl.close()

    gftyp=['vertical displacement','radial displacement','acceleration',
           'radial tilt','strain t-t','strain l-l',
           'strain z-z','strain t-z','strain l-z']
    gftyp=gftyp[0:ngf]

    return dsts,gf,gftyp   


def strain_to_stress(strainxx,strainyy,strainzz,shmod=3e10,pr=0.25):
    """
    :param   strainxx: x-x extensional strain values
    :param   strainyy: y-y extensional strain values
    :param   strainzz: z-z extensional strain values
    :param      shmod: shear modulus in Pa
    :param         pr: Poisson's ratio
    :return  stressxx: x-x extensional stress values
    :return  stressyy: y-y extensional stress values
    :return  stresszz: z-z extensional stress values
    """

    lambd=shmod*2*pr/(1-2*pr)

    avstrain=strainxx+strainyy+strainzz
    stressxx = strainxx*2*shmod+avstrain*lambd
    stressyy = strainyy*2*shmod+avstrain*lambd
    stresszz = strainzz*2*shmod+avstrain*lambd

    return stressxx,stressyy,stresszz

def strain_to_stress_surface(strainxx,strainyy,strainzz,shmod=3e10,pr=0.25):
    """
    :param   strainxx: x-x extensional strain values
    :param   strainyy: y-y extensional strain values
    :param   strainzz: z-z extensional strain values
    :param      shmod: shear modulus in Pa
    :param         pr: Poisson's ratio
    :return  stressxx: x-x extensional stress values
    :return  stressyy: y-y extensional stress values
    :return  stresszz: z-z extensional stress values
    """

    lambd=shmod*2*pr/(1-2*pr)

    strainzz=-lambd/(2*shmod+lambd)*(strainxx+strainyy)
    avstrain=strainxx+strainyy+strainzz
    stressxx = strainxx*2*shmod+avstrain*lambd
    stressyy = strainyy*2*shmod+avstrain*lambd
    stresszz = strainzz*2*shmod+avstrain*lambd
    #stresszz = np.zeros(stressxx.shape,dtype=float)

    return stressxx,stressyy,stresszz

def spheredist(loc1,loc2):
    """
    :param     loc1: [lon1,lat1] or Nx2 array of locations
    :param     loc2: [lon2,lat2] or Nx2 array of locations
    :return    dsts: distances in degrees [# of loc1 by # of loc2]
    :return      az: azimuths from location 1 to location 2
    """

    # make them a 2-d grid
    loc1=np.atleast_2d(loc1)
    loc2=np.atleast_2d(loc2)

    # latitude in radians
    phi1=loc1[:,1]*(math.pi/180)
    phi2=loc2[:,1]*(math.pi/180)

    # longitude 
    thet1=loc1[:,0]
    thet2=loc2[:,0]

    # to correct dimensions
    phi1=phi1.reshape([phi1.size,1])
    thet1=thet1.reshape([thet1.size,1])
    phi2=phi2.reshape([1,phi2.size])
    thet2=thet2.reshape([1,thet2.size])

    # longitude difference in radians
    thet2=(thet2-thet1)*(math.pi/180)
    
    # to distances
    dsts=np.multiply(np.cos(phi1),np.cos(phi2))
    dsts=np.multiply(dsts,np.cos(thet2))
    dsts=dsts+np.multiply(np.sin(phi1),np.sin(phi2))
    dsts=np.arccos(np.minimum(dsts,1.))

    # to azimuths
    az=np.multiply(np.cos(phi1),np.tan(phi2))
    az=az-np.multiply(np.sin(phi1),np.cos(thet2))
    az=np.divide(np.sin(thet2),az)
    az=np.arctan(az)

    # there's an azimuthal ambiguity of 180 degrees, 
    # so let's check the law of sines for each azimuth
    df1=np.multiply(np.sin(az),np.sin(dsts)) - \
        np.multiply(np.sin(thet2),np.sin(math.pi/2-phi2))
    df2=np.multiply(np.sin(az+math.pi),np.sin(dsts)) - \
        np.multiply(np.sin(thet2),np.sin(math.pi/2-phi2))
    sw=np.abs(df2)<np.abs(df1)
    az[sw]=az[sw]+math.pi

    # and still one ambiguity---when they're along a line of longitude
    sw=np.logical_or(az==0.,az==math.pi)
    if len(sw):
        phi1=phi1-np.zeros(phi2.shape)
        phi2=phi2-np.zeros(phi1.shape)
        sw0=(math.pi/2.-phi2[sw].flatten())+(math.pi/2.-phi1[sw].flatten())<=math.pi

        shp=az.shape
        az=az.flatten()
        sw=np.where(sw.flatten())[0]
        az[sw[sw0]]=0.
        az[sw[~sw0]]=math.pi
        az=az.reshape(shp)

    # back to degrees
    az=az*(180/math.pi) % 360
    dsts=dsts*(180/math.pi)
    
    return dsts,az

def flatdist(loc1,loc2):
    """
    distances and azimuths on a flat plane, assuming 
    longitude and latitude spacing are the same
    :param     loc1: [lon1,lat1] or Nx2 array of locations
    :param     loc2: [lon2,lat2] or Nx2 array of locations
    :return    dsts: distances in degrees [# of loc1 by # of loc2]
    :return      az: azimuths from location 1 to location 2
    """

    # make them a 2-d grid
    loc1=np.atleast_2d(loc1)
    loc2=np.atleast_2d(loc2)

    # dx + i dy
    dsts=general.modhalf(loc2[:,0:1].T-loc1[:,0:1],360)
    dsts=dsts*np.cos(np.pi/180*np.median(loc2[:,1]))
    dsts=dsts+1j*(loc2[:,1:2].T-loc1[:,1:2])

    # azimuths
    az=(90-180/np.pi*np.angle(dsts)) % 360.

    # distances
    dsts=np.abs(dsts)

    return dsts,az

def findnearest(londes,latdes,lonhave,lathave):
    """
    :param      londes:  the desired longitudes
    :param      latdes:  the desired latitudes
    :param     lonhave:  the longitudes we have
    :param     lathave:  the latitudes we have
    :return      igrab:  indices of the locations to grab from lon/lathave
    """

    # just compute stupidly for now
    # reshape for subtraction
    lonhave,lathave=lonhave.reshape([lonhave.size,1]),lathave.reshape([lonhave.size,1])
    londes,latdes=londes.reshape([1,londes.size]),latdes.reshape([1,londes.size])

    
    # compute distance
    dst=general.modhalf(londes-lonhave,360)
    dst=np.multiply(dst,np.cos(londes*np.pi/180))
    dst=np.power(dst,2)+np.power(lathave-latdes,2)

    # find minima
    igrab=np.argmin(dst,axis=0)

    return igrab

        
def rotatestresses(X,theta,phi):
    """
    :param        X: the initial stress field, where the first dimension indexes
                         xx,yy,zz,xy,xz,yz
    :param    theta: rotation angle in the horizontal plane, so that
                         the new axis is the old axis roted theta degrees counterclockwise
                         theta = negative of the trend azimuth
    :param      phi: rotation angle in the vertical plane, so that
                         the new x axis is the old x axis roted phi degrees counterclockwise
                         around the y axis---toward the z axis
                         phi = negative of the dip magnitude
    :return       X: the rotated stress tensor
                         x-x: along-dip tension
                         y-y: along-strike tension
                         z-z: fault-perpendicular tension
                          xy: shear stress on plane perpendicular to fault plane
                          xz: shear stress on fault plane, along dip
                          yz: shear stress on fault plane, along strike, 
                                  90 degrees counterclockwise from dip
    """
    
    # organize the axes
    X = np.atleast_1d(X)
    sz = list(X.shape)
    if X.ndim==1:
        X = X.reshape([6,1])
    elif X.ndim>2:
        X = X.reshape([6,np.prod(sz[1:])])

    # first the horizontal rotation
    # if we assume that original +x=E, +y=N, +z=up, then
    # here we are rotating the dip direction to have azimuth -theta

    if not isinstance(theta,float) and not isinstance(theta,int):
        # repeat theta if needed
        theta=np.atleast_1d(theta)*(math.pi/180)
        cs,sn=np.cos(theta),np.sin(theta)
        cs,sn=np.atleast_1d(cs),np.atleast_1d(sn)
        sdes=[1]+list(cs.shape)+[1]*(len(sz)-cs.ndim-1)
        cs,sn=cs.reshape(sdes),sn.reshape(sdes)
        nrep=np.divide(np.array([1]+sz[1:]),np.array(list(cs.shape))).astype(int)
        cs,sn=np.tile(cs,nrep),np.tile(sn,nrep)
        cs,sn=cs.reshape([1,np.prod(sz[1:])]),sn.reshape([1,np.prod(sz[1:])])
    else:
        # or if it's a scalar
        cs,sn=np.cos(theta*math.pi/180),np.sin(theta*math.pi/180)


    # x-x
    tauxxi = np.multiply(X[0,:],np.power(cs,2)) + \
             2*np.multiply(X[3,:],np.multiply(sn,cs)) + \
             np.multiply(X[1,:],np.power(sn,2))

    # y-y
    tauyy = np.multiply(X[0,:],np.power(sn,2)) - \
            2*np.multiply(X[3,:],np.multiply(sn,cs)) + \
            np.multiply(X[1,:],np.power(cs,2))

    # x-y
    tauxyi = np.multiply(X[1,:]-X[0,:],np.multiply(sn,cs)) + \
             np.multiply(X[3,:],np.power(cs,2)-np.power(sn,2))

    # x-z
    tauxzi = np.multiply(X[4,:],cs) + np.multiply(X[5,:],sn)

    # y-z
    tauyzi = np.multiply(X[5,:],cs) - np.multiply(X[4,:],sn)


    # now the vertical rotation
    # we are rotating the +x direction from the horizontal direction to the
    # down-dip direction, which is an angle -phi downward

    if not isinstance(phi,float) and not isinstance(phi,int):
        # repeat theta if needed
        phi=np.atleast_1d(phi)*(math.pi/180)
        cs,sn=np.cos(phi),np.sin(phi)
        cs,sn=np.atleast_1d(cs),np.atleast_1d(sn)
        sdes=[1]+list(cs.shape)+[1]*(len(sz)-cs.ndim-1)
        cs,sn=cs.reshape(sdes),sn.reshape(sdes)
        nrep=np.divide(np.array([1]+sz[1:]),np.array(list(cs.shape))).astype(int)
        cs,sn=np.tile(cs,nrep),np.tile(sn,nrep)
        cs,sn=cs.reshape([1,np.prod(sz[1:])]),sn.reshape([1,np.prod(sz[1:])])
    else:
        # or if it's a scalar
        cs,sn=np.cos(phi*math.pi/180),np.sin(phi*math.pi/180)


    # x-x
    tauxx = np.multiply(tauxxi,np.power(cs,2)) + \
            2*np.multiply(tauxzi,np.multiply(sn,cs)) + \
            np.multiply(X[2,:],np.power(sn,2))

    # z-z
    tauzz = np.multiply(tauxxi,np.power(sn,2)) - \
            2*np.multiply(tauxzi,np.multiply(sn,cs)) + \
            np.multiply(X[2,:],np.power(cs,2))

    # x-z
    tauxz = np.multiply(X[2,:]-tauxxi,np.multiply(sn,cs)) + \
            np.multiply(tauxzi,np.power(cs,2)-np.power(sn,2))

    # x-y
    tauxy = np.multiply(tauxyi,cs) + np.multiply(tauyzi,sn)

    # y-z
    tauyz = np.multiply(tauyzi,cs) - np.multiply(tauxyi,sn)


    # collect for output
    X = np.vstack([tauxx,tauyy,tauzz,tauxy,tauxz,tauyz])

    # back to original shape
    X = X.reshape(sz)

    return X


#----------------END OF CODES FOR STRESS CALCULATION---------------------

#----------------START OF CODES FOR ECMWF READING---------------------------

def read_surface_pressure(fname=None,fdir=os.path.join(os.environ['DATA'],'ECMWF','PRESSURE'),
                          ikp=None,trange=None,justone=False):
    """
    reads snow depth from an ECMWF netcdf file
    :param       fname: the file name to read
    :param        fdir: directory containing file (default: $DATA/ECMWF)
    :param         ikp: if only a subset of the values are desired, get these
    :param      trange: time range of interest, in datetime units
    :param     justone: just read one time range, to get the grid set up
    :return        tms: an array of times
    :return        prs: atmospheric pressure pressure in Pa
    :return       lons: longitudes on a grid, or a list if ikp given
    :return       lats: latitudes on a grid, or a list if ikp given
    """

    # files if not given
    if fname is None:
        fls,t1,t2=ecmwf_files(datatype='pressure',trange=trange)
        # just use the first one for now
        fname=fls[0]

    
    # use general format
    prs,lons,lats,tms=read_ecmwf(fname,fdir=fdir,ikp=ikp,trange=trange,justone=justone)
    
    return prs,lons,lats,tms

def read_wave_height(fname=None,fdir=os.path.join(os.environ['DATA'],'ECMWF',
                                                  'WAVES'),
                          ikp=None,trange=None,justone=False):
    """
    reads snow depth from an ECMWF netcdf file
    :param       fname: the file name to read
    :param        fdir: directory containing file (default: $DATA/ECMWF)
    :param         ikp: if only a subset of the values are desired, get these
    :param      trange: time range of interest, in datetime units
    :param     justone: just read one time range, to get the grid set up
    :return        tms: an array of times
    :return        prs: atmospheric pressure pressure in Pa
    :return       lons: longitudes on a grid, or a list if ikp given
    :return       lats: latitudes on a grid, or a list if ikp given
    """

    # files if not given
    if fname is None:
        fls,t1,t2=ecmwf_files(datatype='waves',trange=trange)
        # just use the first one for now
        fname=fls[0]

    
    # use general format
    wheight,lons,lats,tms=read_ecmwf(fname,dtype='shww',
                                     fdir=fdir,ikp=ikp,trange=trange,justone=justone)

    # mask
    wheight=np.ma.masked_array(wheight,mask=wheight<=0.)

    return wheight,lons,lats,tms

def read_wind_speed(fname=None,fdir=os.path.join(os.environ['DATA'],'ECMWF',
                                                 'WIND'),
                          ikp=None,trange=None,justone=False):
    """
    reads wind speeds from an ECMWF netcdf file
    :param       fname: the file name to read
    :param        fdir: directory containing file (default: $DATA/ECMWF)
    :param         ikp: if only a subset of the values are desired, get these
    :param      trange: time range of interest, in datetime units
    :param     justone: just read one time range, to get the grid set up
    :return        tms: an array of times
    :return        prs: atmospheric pressure pressure in Pa
    :return       lons: longitudes on a grid, or a list if ikp given
    :return       lats: latitudes on a grid, or a list if ikp given
    """

    # files if not given
    if fname is None:
        fls,t1,t2=ecmwf_files(datatype='wind',trange=trange)
        # just use the first one for now
        fname=fls[0]

    
    # use general format to read E and N components
    wspeedu,lons,lats,tms=read_ecmwf(fname,dtype='u10',
                                     fdir=fdir,ikp=ikp,trange=trange,
                                     justone=justone)
    wspeed,lons,lats,tms=read_ecmwf(fname,dtype='v10',
                                     fdir=fdir,ikp=ikp,trange=trange,
                                     justone=justone)

    # combine to get amplitude
    wspeed=np.power(np.power(wspeed,2)+np.power(wspeedu,2),0.5)

    # mask
    #wspeed=np.ma.masked_array(wspeed,mask=wspeed<=0.)

    return wspeed,lons,lats,tms


def read_snow_depth(fname=None,
                    fdir=os.path.join(os.environ['DATA'],'ECMWF','WATER'),
                    ikp=None,trange=None,justone=False):
    """
    reads snow depth from an ECMWF netcdf file
    :param       fname: the file name to read
    :param        fdir: directory containing file (default: $DATA/ECMWF)
    :param         ikp: if only a subset of the values are desired, get these
    :param      trange: time range of interest, in datetime units
    :param     justone: just read one time range, to get the grid set up
    :return        tms: an array of times
    :return     sdepth: snow depth
    :return       lons: longitudes on a grid, or a list if ikp given
    :return       lats: latitudes on a grid, or a list if ikp given
    """

    # files if not given
    if fname is None:
        fls,t1,t2=ecmwf_files(datatype='snow',trange=trange)
        # just use the first one for now
        fname=fls[0]

    
    # use general format
    sdepth,lons,lats,tms=\
            read_ecmwf(fname,dtype='sd',fdir=fdir,ikp=ikp,trange=trange,
                       justone=justone)
    
    return sdepth,lons,lats,tms

def read_groundwater(fname=None,
                     fdir=os.path.join(os.environ['DATA'],'ECMWF','WATER'),
                     ikp=None,trange=None,justone=False):
    """
    reads groundwater values from an ECMWF netcdf file
    :param       fname: the file name to read
    :param        fdir: directory containing file (default: $DATA/ECMWF)
    :param         ikp: if only a subset of the values are desired, get these
    :param      trange: time range of interest, in datetime units
    :param     justone: just read one time range, to get the grid set up
    :return        tms: an array of times
    :return     wequiv: equivalent water height in m due to moisture in the 4 layers
    :return       lons: longitudes on a grid, or a list if ikp given
    :return       lats: latitudes on a grid, or a list if ikp given
    """
    
    # volumetric soil moisture is given in m^3/m^3 in four layers
    # want to convert to an equivalent water depth in meters

    # files if not given
    if fname is None:
        fls,t1,t2=ecmwf_files(datatype='groundwater',trange=trange)
        # just use the first one for now
        fname=fls[0]

    # read and sum each one
    wequiv=0.
    
    #Layer 1: 0 -7cm
    dens,lons,lats,tms=\
            read_ecmwf(fname,dtype='swvl1',fdir=fdir,ikp=ikp,trange=trange,justone=justone)
    wequiv=dens*0.07

    #Layer 2: 7 -21cm
    dens,lons,lats,tms=\
            read_ecmwf(fname,dtype='swvl2',fdir=fdir,ikp=ikp,trange=trange,justone=justone)
    wequiv=wequiv+dens*(0.21-0.07)

    #Layer 3: 21-72cm
    dens,lons,lats,tms=\
            read_ecmwf(fname,dtype='swvl3',fdir=fdir,ikp=ikp,trange=trange,justone=justone)
    wequiv=wequiv+dens*(0.72-0.21)

    #Layer 4: 72-189cm
    dens,lons,lats,tms=\
            read_ecmwf(fname,dtype='swvl4',fdir=fdir,ikp=ikp,trange=trange,justone=justone)
    wequiv=wequiv+dens*(1.89-0.72)
    
    return wequiv,lons,lats,tms


def ecmwf_files(fdir=None,datatype='pressure',trange=None):
    """
    :param        fdir: directory with files, if known (default: chosen given datatype)
    :param    datatype: data type to use, to pick fdir if not given (default: 'pressure')
    :param      trange: time range (default: all)
    :return        fls: an array of the file names
    :return         t1: file start times
    :return         t2: file end times
    """

    if fdir is None:
        if datatype is 'pressure':
            fdir=os.path.join(os.environ['DATA'],'ECMWF','PRESSURE')
        elif datatype is 'groundwater':
            fdir=os.path.join(os.environ['DATA'],'ECMWF','WATER')
        elif datatype is 'snow':
            fdir=os.path.join(os.environ['DATA'],'ECMWF','SNOW')
        elif datatype is 'waves':
            fdir=os.path.join(os.environ['DATA'],'ECMWF','WAVES')
        elif datatype is 'wind':
            fdir=os.path.join(os.environ['DATA'],'ECMWF','WIND')

    # all the files
    fls=glob.glob(os.path.join(fdir,'*.nc'))
    fls=np.array(fls)

    # identify the available times
    trng=np.array([os.path.split(fname)[1].split('.')[0].split('_') for fname in fls]) 
    t1=np.array([t.split('-') for t in trng[:,1]]).astype(int)
    t1=np.array([datetime.datetime(t1[k,0],t1[k,1],t1[k,2]) 
                 for k in range(0,t1.shape[0])])
    t2=np.array([t.split('-') for t in trng[:,2]]).astype(int)
    t2=np.array([datetime.datetime(t2[k,0],t2[k,1],t2[k,2]) 
                 for k in range(0,t2.shape[0])])

    if trange is not None:
        # use a wide range if not given
        ix=np.logical_and(t2>=trange[0],t1<=trange[1])
        t1,t2,fls=t1[ix],t2[ix],np.array(fls)[ix]

    # make sure the files are in order
    ix=np.argsort(t1)
    t1,t2,fls=t1[ix],t2[ix],np.array(fls)[ix]

    return fls,t1,t2

def read_ecmwf(fname,dtype='sp',
               fdir=os.path.join(os.environ['DATA'],'ECMWF','PRESSURE'),
               ikp=None,trange=None,justone=False):
    """
    reads values from an ECMWF netcdf file
    :param       fname: the file name to read
    :param       dtype: data type to read (default: 'sp'--surface pressure)
    :param        fdir: directory containing file (default: $DATA/ECMWF)
    :param         ikp: if only a subset of the values are desired, get these
    :param      trange: time range of interest, in datetime units
    :param     justone: just read one time range, to get the grid set up
    :return        prs: set of values on a grid, or a list if ikp given
    :return       lons: longitudes on a grid, or a list if ikp given
    :return       lats: latitudes on a grid, or a list if ikp given
    :return        tms: an array of times
    """
    
    # full file name
    fname=os.path.join(fdir,fname)

    # read one message
    dataset = netCDF4.Dataset(fname,'r')
    vrs = dataset.variables

    # coordinates
    lons=vrs['longitude'][:]
    lats=vrs['latitude'][:]
    lons,lats=np.meshgrid(lons,lats)
        
    if ikp is not None:
        ikp=np.atleast_1d(ikp)
        lons,lats=lons.flatten()[ikp],lats.flatten()[ikp]

    # the times, in hours since 1900
    tms = vrs['time'][:]

    # time range in these units
    tref=datetime.datetime(1900,1,1)
    if justone:
        itim=np.array([0],dtype=int)
    elif trange is None:
        itim = np.arange(0,tms.size,dtype=int)
    else:
        t1=(trange[0]-tref).total_seconds()/3600
        t2=(trange[1]-tref).total_seconds()/3600
        itim,=np.where(np.logical_and(tms>=t1,tms<t2))

    # the variable name of interest
    vname = dtype

    if ikp is None:
        # just grab the values---they're already organized
        prs=vrs[vname][itim,:,:]
    
        # except I want the time dimension last
        prs=prs.transpose([1,2,0])

    else:
        # we'll just get some of the locations
        if len(itim):
            prs=np.vstack([vrs[vname][k,:,:].flatten()[ikp] for k in itim]).T
        else:
            prs=np.ndarray([ikp.size,0],dtype=float)

    # for the times
    tms=np.array([tref+datetime.timedelta(hours=float(tms[k])) for k in itim])

    # trash the masks
    if isinstance(prs,np.ma.masked_array):
        prs=prs.data
    if isinstance(lons,np.ma.masked_array):
        lons=lons.data
    if isinstance(lats,np.ma.masked_array):
        lats=lats.data

    return prs,lons,lats,tms


def read_surface_pressure_grib(fname,fdir=os.path.join(os.environ['DATA'],'ECMWF'),
                               ikp=None):
    """
    reads surface pressure from a grib file
    :param       fname: the file name to read
    :param        fdir: directory containing file (default: $DATA/ECMWF)
    :param         ikp: if only a subset of the values are desired, get these
    :return        prs: set of pressure values on a grid, or a list if ikp given
    :return       lons: longitudes on a grid, or a list if ikp given
    :return       lats: latitudes on a grid, or a list if ikp given
    :return        tms: an array of times
    """
    
    # full file name
    fname=os.path.join(fdir,fname)

    # read one message
    with open(fname,'rb') as stream:
        msg = pupygrib._try_read_message(stream)
    

    # coordinates
    lons,lats=msg.get_coordinates()
    
    if ikp is not None:
        ikp=np.atleast_1d(ikp)
        lons,lats=lons.flatten()[ikp],lats.flatten()[ikp]

    # for one time
    prs=np.ndarray(list(lons.shape)+[1],dtype=float)

    # to get the date
    sc1 = msg._get_section1()
    yr=100*(sc1.centuryOfReferenceTimeOfData-1)+sc1.yearOfCentury
    tm=datetime.datetime(yr,sc1.month,sc1.day,sc1.hour,sc1.minute)
    tms=np.array([tm])

    # the values
    vls = msg.get_values()
    if ikp is None:
        prs[:,:,0] = vls
    else: 
        prs[:,0]=vls.flatten()[ikp]

    return prs,lons,lats,tms

    
def rename_ecmwf(fls,fstart='pressure_'):
    """
    :param      fls: files to rename, or folder if the first file doesn't end with .nc
    :param   fstart: start of file name (default: 'pressure_')
    """


    if isinstance(fls,str):
        if fls[-3:] == '.nc':
            # make a list if needed
            fls = [fls]
        else:
            # or find relevant files
            fls=glob.glob(os.path.join(fls,'*.nc'))

    for fname in fls:
        dataset = netCDF4.Dataset(fname,'r')

        # grab times
        time = dataset.variables['time']

        # time limits
        tlm = general.minmax(time)

        # add average spacing
        tlm[1]=tlm[1]+np.median(np.diff(time))
        t1=datetime.datetime(1900,1,1)+datetime.timedelta(hours=float(tlm[0]))
        t2=t1+datetime.timedelta(hours=float(np.diff(tlm)[0]))
        
        # new file name
        fdir,fnamei = os.path.split(fname)
        fnamei='{:04d}-{:02d}-{:02d}_{:04d}-{:02d}-{:02d}.nc'.format(\
                       t1.year,t1.month,t1.day,t2.year,t2.month,t2.day)
        fnamei=fstart+fnamei
        
        # rename
        os.rename(fname,os.path.join(fdir,fnamei))
    
 

#-------------------END OF CODES FOR ECMWF READING--------------------------------


#---------START OF MISCELLANEOUS FILTERING, DEGREE CALCULATIONS-----------------

def deg2km():
    """
    :return     X: number of km per degree
    """

    X = 111.

    return X

def modhalf(a,b):
    """
    :param   a:  numerator
    :param   b:  denominator
    :return  x:  a % b, but always between -b/2 and b/2
    """

    if isinstance(a,list):
        a = np.atleast_1d(a)

    x = a % b
    x[x>b/2.]=x[x>b/2.]-b

    return x

def filtertimeseries(tms,data,flm=np.array([.1,.5])/86400.):
    """
    :param       tms: times
    :param      data: data to filter
    :param       flm: frequencies to filter to, in units of 1/tms
    :return     tmsf: filtered times
    :return    fdata: filtered time series
    """

    # create a 2-d array
    sz=data.shape
    if data.ndim==1:
        data=data.reshape([data.size,1])

    # time spacing in days
    dtim=np.ma.median(np.diff(tms))
    # Nyquist frequency
    nfreq=0.5/dtim
    # frequencies as a fraction of Nyquist
    flm=np.array(flm)/nfreq

    # remove the mean
    mn=np.ma.mean(data,axis=0)
    mn=mn.reshape([1]+list(data.shape)[1:])
    fdata = data-mn

    # fill masked values
    if isinstance(fdata,np.ma.masked_array):
        msk=fdata.mask
        for k in range(0,data.shape[1]):
            datai=fdata[:,k]
            if np.sum(datai.mask) and np.sum(~datai.mask)>100:
                datai.data[datai.mask]=np.interp(np.where(datai.mask)[0],
                                                 np.where(~datai.mask)[0],
                                                 datai.data[~datai.mask],
                                                 left=0.,right=0.)
                fdata.data[:,k]=datai.data
        fdata=fdata.data
    else:
        msk=np.arrray([])

    # decimate if needed
    tmsf=tms.copy()
    while flm[1]<0.01:
        ndec=10
        tmsf=tmsf[np.arange(0,tmsf.size,ndec)]
        fdata=signal.decimate(fdata,ndec,zero_phase=True,axis=0)
        flm,dtim=flm*ndec,dtim*ndec

    # create filter
    if flm[0]==0:
        b,a=signal.butter(N=5,Wn=flm[1],btype='lowpass')
        npad=int(2/flm[1])
    elif flm[1]>0.95:
        b,a=signal.butter(N=5,Wn=flm[0],btype='highpass')
        npad=int(2/flm[1])
    else:
        b,a=signal.butter(N=5,Wn=flm,btype='bandpass')
        npad=int(2/flm[0])

    # apply filter
    fdata=signal.filtfilt(b,a,fdata,padlen=npad,axis=0)

    # re-apply mask
    if msk.size:
        fdata=np.ma.masked_array(fdata,mask=msk)

    return tmsf,fdata

#---------START OF MISCELLANEOUS FILTERING, DEGREE CALCULATIONS-----------------

#----------START OF TIDE GAGE READING CODES----------------------------


def read_stations_japan():
    """
    :return     statinfo: dictionary of the information, including
              statnum: station number
              statname: station name
              longitude: longitude in degrees
              latitude: latitude info
              type: type of tide gauge
              plane: tidal datum plane (m)
              fixed_height: height of the fixed point (m)
              start_date: date of establishment
    """

    fdir=os.path.join(os.environ['DATA'],'SURFACE','TIDEGAGE','GSIJ')
    fname=os.path.join(fdir,'station_summary.txt')

    fl=open(fname,'r')
    hdr=fl.readline().split(',')
    hdr=[vl.strip() for vl in hdr]
    fl.close()

    vls=np.loadtxt(fname,skiprows=1,dtype=str)
    statinfo={}
    statinfo['statnum']=vls[:,0].astype(int)
    statinfo['statname']=vls[:,1]

    statinfo['longitude']=np.array([vl.strip().replace('-','.').replace('E','')
                                    for vl in vls[:,3]]).astype(float)
    statinfo['latitude']=np.array([vl.strip().replace('-','.').replace('N','')
                                   for vl in vls[:,2]]).astype(float)

    statinfo['type']=vls[:,4]

    statinfo['plane']=np.array([vl.strip().replace('m','')
                                for vl in vls[:,5]]).astype(float)
    statinfo['fixed_height']=np.array([vl.strip().replace('m','')
                                       for vl in vls[:,6]]).astype(float)

    statinfo['start_date']=np.array([datetime.datetime.strptime(vl,'%b.%Y')
                                     for vl in vls[:,7]])

    return statinfo


def read_tidegage_gsij(statnum=9,trange=None):
    """
    :param    statnum: station number
    :param     trange: desired time range (default: all)
    :return       tms: times in seconds since tref
    :return      tref: reference time
    :return      wlev: water level in meters
    :return  statinfo: information about the station
    """

    # identify files
    statname='{:02d}'.format(statnum)
    fdir=os.path.join(os.environ['DATA'],'SURFACE','TIDEGAGE','*')
    fname=os.path.join(fdir,statname+'*.txt')
    fls=glob.glob(fname)

    # initialize
    tms=np.array([],dtype=float)
    wlev=np.array([],dtype=float)
    tref=datetime.datetime(2000,1,1)
    
    # read data for each one
    for fnm in fls:
        # check to find time zone
        ln = ''
        fl=open(fnm,'r')
        while not 'TimeZone' in ln:
            ln=fl.readline()
        fl.close()
        tz=ln.split()[1].split('(')[0]
        tz=datetime.datetime.strptime(tz,'+%H:%M') - \
            datetime.datetime.strptime('','')
        tz=tz.total_seconds()

        # read all the data
        vls=np.loadtxt(fnm,comments='#',dtype=str)

        # and the timing
        tmsi=np.array([(datetime.datetime.strptime(tm,'%Y/%m/%d')-tref).total_seconds()
                       for tm in vls[:,1]])
        tmsi=tmsi+vls[:,2].astype(float)*3600.-tz
        tms=np.append(tms,tmsi)
        
        wlev=np.append(wlev,vls[:,3].astype(float))

    # sorted through time
    ix=np.argsort(tms)
    tms,wlev=tms[ix],wlev[ix]

    # check for nans
    wlev=np.ma.masked_array(wlev/1000.,mask=wlev==-999.)

    # read the values
    statinfos=read_stations_japan()
    ix=np.argmin(np.abs(statinfos['statnum']-statnum))
    statinfo={}
    for hdr in statinfos.keys():
        statinfo[hdr]=statinfos[hdr][ix]
    
    return tms,tref,wlev,statinfo


def read_tidegage_noaa(statname='lapush',datades='tideremoved',trange=None):
    """
    :param    statname: station name (default: 'lapush')
    :param     datades: which data type is desired 
                        'original': quality-controlled record
                        'modelled': the modelled tidal variation
                        'tideremoved': the data after removing tides (default)
    :param       range: desired time range (default: all)
    :return        tms: times in seconds since tref
    :return       tref: reference time
    :return       wlev: water level in meters
    :return   statinfo: information about the station
    """

    # identify file
    statname=str(statname)
    fdir=os.path.join(os.environ['DATA'],'SURFACE','TIDEGAGE','NOAA')
    fname=os.path.join(fdir,statname+'*.nc')
    fname=glob.glob(fname)[0]

    # read
    dataset = netCDF4.Dataset(fname,'r') 

    # station information
    statinfo = {'latitude':dataset.variables['lat'][:][0],
                'longitude':dataset.variables['lon'][:][0]}
    name=dataset.variables['platform_info'].long_name
    statinfo['statname']=(','.join(name.split(',')[1:])).strip().title()
    statinfo['statnum']=int(name.split(',')[0].split(' ')[-1])

    # time 
    # given in seconds since 1970
    trefi = datetime.datetime(1970,1,1)
    tms = dataset.variables['time'][:]

    # output in seconds since 2000,1,1
    tref = datetime.datetime(2000,1,1)
    tms = tms + (trefi-tref).total_seconds()
    #tms = np.array([tref+datetime.timedelta(seconds=tm) for tm in tms])

    # water level
    if datades == 'original':
        wlev = dataset.variables['waterlevel_quality_controlled'][:].flatten()
    elif datades == 'tidemodel':
        wlev = dataset.variables['waterlevel_modelled'][:].flatten()
    elif datades == 'tideremoved':
        wlev = dataset.variables['waterlevel_residual'][:].flatten()
    else:
        error('Data requested was '+datades+', but there is no such option')

    # throw away masked values since we'll grab from the rest
    iok=~np.isnan(wlev)
    if isinstance(wlev,np.ma.masked_array):
        iok=np.logical_and(iok,~wlev.mask)
    tms,wlev=tms[iok],wlev[iok]
    
    # want a steady sampling
    tdiff = np.diff(tms)
    tdiff = np.min(tdiff[tdiff>0])
    tdes=np.arange(tms[0],tms[-1]+tdiff*1e-4,tdiff)

    # if we only want part of it
    if trange is not None:
        t1,t2=(trange[0]-tref).total_seconds(),(trange[1]-tref).total_seconds()
        tdes=tdes[np.logical_and(tdes>=t1,tdes<=t2)]

    # get closest times
    ix=general.closest(tms,tdes)
    df=np.abs(tms[ix]-tdes)/tdiff
    wlev=np.ma.masked_array(wlev[ix],mask=df>0.05)
    
    return tdes,tref,wlev,statinfo

def read_tidegage_foc(statname=8615,trange=None):
    """
    :param    statname: station number (default: 8615)
    :param      trange: time range to retrieve (default: all)
    :return        tms: times in seconds since tref
    :return       tref: reference time
    :return       wlev: water level in meters
    :return   statinfo: information about the station
    """

    # identify file
    statname=int(statname)
    fdir=os.path.join(os.environ['DATA'],'SURFACE','TIDEGAGE','FOC')
    fls=glob.glob(os.path.join(fdir,'{:d}'.format(statname)+'*.csv'))


    # initialize
    tms = np.array([],dtype=float)
    wlev = np.array([],dtype=float)
    tref=datetime.datetime(2000,1,1)

    statinfo = {}
    nskip = 0
    for fname in fls:
        fl = open(fname,'r')
        ln = fl.readline().split(',')
        nskip += 1
        statinfo['statname']=(','.join(ln[1:])).strip()
        
        ln = fl.readline().split(',')
        nskip += 1
        statinfo['statnum']=int(ln[1])

        ln = fl.readline().split(',')
        nskip += 1
        statinfo['latitude']=float(ln[1])

        ln = fl.readline().split(',')
        nskip += 1
        statinfo['longitude']=-float(ln[1])
        
        ln = fl.readline().split(',')
        nskip += 1
        statinfo['datum']=ln[1].strip()

        ln = fl.readline().split(',')
        nskip += 1
        statinfo['time_zone']=ln[1].strip()
        if statinfo['time_zone'] != 'UTC':
            print('NOT IN UTC TIME ZONE!')

        while ln[0:8] != 'Obs_date':
            ln = fl.readline()
            nskip += 1

        fl.close()

        # read the data
        vls = np.loadtxt(fname,dtype=str,delimiter=',',skiprows=nskip)

        # add the water level
        wlev = np.append(wlev,vls[:,1].astype(float))

        # the timing
        tmsi=np.array([(datetime.datetime.strptime(tm,'%Y/%m/%d %H:%M') - 
                        tref).total_seconds() for tm in vls[:,0]])
        tms = np.append(tms,tmsi)


    # order and avoid duplicates
    tms,ix=np.unique(tms,return_index=True)
    wlev=wlev[ix]

    # if we only want part of it
    if trange is not None:
        t1,t2=(trange[0]-tref).total_seconds(),(trange[1]-tref).total_seconds()
        ii=np.logical_and(tms>=t1,tms<=t2)
        tms,wlev=tms[ii],wlev[ii]
    
    return tms,tref,wlev,statinfo

def tidegage_stationlist(region='all'):
    """
    :param       region: region of interest (default: 'Cascadia')
    :return       stats: list of all stations
    :return       cstat: list of available FOC stations
    :return       ustat: list of available NOAA stations
    """

    cstat,ustat,jstat=[],[],[]
    if region=='Cascadia':
        cstat=[7120,7277,7654,7735,7795,8074,8408,8545,8615,8735]
        ustat=[9416841,9440569,9418767,9440581,9419750,9440910,9431647,9441102,
               9432780,9442396,9435380,9443090,9437540,9444090,9439011,9444900,
               9439040,9446484,9439099,9447130,9439201,9449424,9440083,9449880,
               9440422]
    elif region=='Shikoku':
        jstat=[2,13,5,9]
    elif region=='Parkfield':
        ustat=[9410660,9410840,9411340,9411406,9412110,9413450]
    elif region=='all':
        ustat=[9410660,9410840,9411340,9411406,9412110,9413450,
               9416841,9440569,9418767,9440581,9419750,9440910,9431647,9441102,
               9432780,9442396,9435380,9443090,9437540,9444090,9439011,9444900,
               9439040,9446484,9439099,9447130,9439201,9449424,9440083,9449880,
               9440422]
        cstat=[7120,7277,7654,7735,7795,8074,8408,8545,8615,8735]
        jstat=[2,13,5,9]
        
    stats=cstat+ustat+jstat

    return stats,cstat,ustat,jstat


def read_tidegage_all(stats=None,tspc=3600,trange=None,datades='tideremoved'):
    """
    read the data from all tide gage
    :param         stats: desired stations
    :param          tspc: desired time spacing in seconds (default: 3600)
    :param        trange: time range in datetime  
                            (default: 2008-01-01 to 2019-05-01)
    :param     datades: which data type is desired 
                        'original': quality-controlled record
                        'modelled': the modelled tidal variation
                        'tideremoved': the data after removing tides (default)
    :return         tdes: times in seconds since tref
    :return         tref: reference time
    :return         wlev: water levels in meters, [# time x # stations] array
    :return     statinfo: information about each station
    """

    # define desired time spacing
    if trange is None:
        trange=[datetime.datetime(2008,1,1),datetime.datetime(2019,5,1)]
    tref=datetime.datetime(2000,1,1)
    tdes=[(trange[0]-tref).total_seconds(),(trange[1]-tref).total_seconds()]
    tdes=np.arange(tdes[0],tdes[1]+tspc*1e-6,tspc)

    # buffer time range slightly for reading data
    tranger=datetime.timedelta(seconds=tspc*100)
    tranger=[trange[0]-tranger,trange[1]+tranger]

    # desired stations
    trash,cstat,ustat,jstat=tidegage_stationlist()
    if stats is not None:
        cstat=np.intersect1d(cstat,stats)
        ustat=np.intersect1d(ustat,stats)
        jstat=np.intersect1d(jstat,stats)
    stats=np.hstack([cstat,ustat,jstat])
    stattype=['C']*len(cstat)+['U']*len(ustat)+['J']*len(jstat)
    statinfo = {}

    # initialize
    wlev=np.ndarray([tdes.size,len(stats)],dtype=float)
    wlev=np.ma.masked_array(wlev,mask=False)

    ctr=0
    for k in range(0,len(stats)):
        # for each station
        stat=stats[k]

        # read data
        if stattype[k]=='U':
            # US stations
            tmsi,trefi,wlevi,statinfoi=read_tidegage_noaa(stat,datades=datades,trange=tranger)
            
        elif stattype[k]=='C':
            # Canadian stations
            tmsi,trefi,wlevi,statinfoi=read_tidegage_foc(stat,trange=tranger)
            
        elif stattype[k]=='J':
            # Japanese stations
            tmsi,trefi,wlevi,statinfoi=read_tidegage_gsij(stat,trange=tranger)

        # station info
        statinfo[stat]=statinfoi

        # check how many points there are
        npts=wlevi.size
        if npts and isinstance(wlevi,np.ma.masked_array):
            npts=np.sum(~wlevi.mask)
        
        if npts>100:
            # timing info
            tshf=(trefi-tref).total_seconds()
            
            # add masked values at beginning and end
            dtim=np.median(np.diff(tmsi))
            nadd=int(tspc*100/dtim)
            if not isinstance(wlevi,np.ma.masked_array):
                wlevi=np.ma.masked_array(wlevi,mask=False)
            if wlevi.mask is False:
                wlevi.mask = np.zeros(wlevi.size,dtype=bool)
            tadd=np.arange(0,nadd)*dtim
            nadd=np.ma.masked_array(np.ndarray([nadd],dtype=float),mask=True)
            msk=np.hstack([nadd.mask,wlevi.mask,nadd.mask])
            wlevi=np.hstack([nadd.data,wlevi.data,nadd.data])
            wlevi=np.ma.masked_array(wlevi,mask=msk)
            tmsi=np.hstack([tadd+(tmsi[0]-dtim-tadd[-1]),tmsi,
                            tadd+(tmsi[-1]+dtim-tadd[0])])
        
            # remove masked samples
            if isinstance(wlevi,np.ma.masked_array):
                msk=wlevi.mask
                wlevi.data[msk]=np.interp(np.where(msk)[0],np.where(~msk)[0],wlevi[~msk])
                wlevi=wlevi.data
                msk=msk.astype(float)
            else:
                msk=np.zeros(wlevi.size,dtype=float)
                
            # decimate if needed
            dtim = np.median(np.diff(tmsi))
            while dtim<0.1*tspc:
                ndec=5

                msk=np.cumsum(msk)[np.arange(0,tmsi.size,ndec)]
                msk=np.diff(np.append([0.],msk))/ndec
                
                tmsi=tmsi[np.arange(0,tmsi.size,ndec)]
                
                wlevi=signal.decimate(wlevi,ndec,zero_phase=True,axis=0)
                dtim=dtim*ndec

            # low-pass filter if necessary
            flm=(0.9*0.5/tspc)/(0.5/dtim)
            if dtim<tspc:
                # create filter
                b,a=signal.butter(N=1,Wn=flm,btype='lowpass')
                npad=int(tspc*5/dtim)
                
                # apply filter
                wlevi=signal.filtfilt(b,a,wlevi,padlen=npad,axis=0)
                msk=signal.filtfilt(b,a,msk,padlen=npad,axis=0)
                
            # and interpolate
            wlev[:,ctr]=np.interp(tdes,tmsi+tshf,wlevi)
            msk=np.interp(tdes,tmsi+tshf,msk)

            # add mask
            wlev.mask[:,ctr]=np.abs(msk)>0.01

        else:
            # if there's no data
            wlev.mask[:,ctr]=True

        # on to next station
        ctr += 1
            
    # order with north at the top
    lats=np.array([statinfo[stat]['latitude'] for stat in stats])
    ix=np.flipud(np.argsort(lats))
    wlev=wlev[:,ix]
    stats=[stats[k] for k in ix]
    
    return tdes,tref,wlev,statinfo,stats

def irrelevant_stations():
    """
    :return        stat_irrel: stations that aren't useful for the mean calculation
    """

    # some are in the Columbia River
    stat_irrel=np.array([9438772,9439040,9440569,9439099,9440422,
                         9439201,9440083])

    # don't use the oil platform station, as it started late and has a funny offset
    stat_irrel=np.append(stat_irrel,[9411406])

    # some are farther south
    # these stations actually seem fine and appear to have roughly the
    # same timing as those farther north, but the
    # amplitude is smaller, so the variance reduction is funny
    # ignore for now
    stat_south=np.array([9432780, 9431647, 9419750, 9418767, 9416841])
    stat_irrel=np.append(stat_irrel,stat_south)

    return stat_irrel

def remove_tides(tms,wlev,flm=[0.5,10],pers=None):
    """
    :param    tms: times in timedate
    :param   wlev: water levels
    :param    flm: filter to apply before fitting, in 1/day
    :param   pers: periods to use, in days (default: chosen based on CTE)
    :return   cfs: tidal coefficients (cosine + i * sine)
    :return  pers: periods used, in days
    :return  tref: reference time
    :return   prd: predicted data from tides
    :return wlevr: water level with prediction removed
    """

    if pers is None:
        # if no periods are given, we'll start with a few and extrapolate
        # from the expected amplitudes
        from Strain import tides
        tdvl=tides.readcte()
        ipers=np.argsort(np.abs(tdvl['amp']))
        ipers=ipers[tdvl['freqs'][ipers]>0][-20:]
        pers=np.power(tdvl['freqs'][ipers],-1)
        pers=pers[pers<2.]
        newpers=True
    else:
        newpers=False

    # times in days relative to a reference
    tref=datetime.datetime(2000,1,1)
    tms=np.array([(tm-tref).total_seconds()/86400 for tm in tms])

    # create an array
    M=np.vstack([np.vstack([np.cos(tms*(2*np.pi/peri)),
                            np.sin(tms*(2*np.pi/peri))])
                 for peri in pers]).T

    # for both
    ndim=wlev.ndim
    if ndim==1:
        wlev=wlev.reshape([wlev.size,1])

    # normalize filter by Nyquist
    dtim=np.ma.median(np.diff(tms))
    flm=np.array(flm)/(0.5/dtim)

    # filter if necessary
    npad=int(np.round(5./dtim))
    if flm[0]>0 or not np.isinf(flm[1]):
        if flm[0]==0:
            b,a=signal.butter(N=5,Wn=flm[1],btype='lowpass')
        elif flm[1]>0.95:
            b,a=signal.butter(N=5,Wn=flm[0],btype='highpass')
        else:
            b,a=signal.butter(N=5,Wn=flm,btype='bandpass')

        # apply filter
        mn=np.ma.mean(wlev,axis=0).reshape([1,wlev.shape[1]])
        wlevf=signal.filtfilt(b,a,wlev-mn,padlen=npad,axis=0)
        mn=np.ma.mean(M,axis=0).reshape([1,M.shape[1]])
        Mf=signal.filtfilt(b,a,M-mn,padlen=npad,axis=0)

        # also copy the mask
        if isinstance(wlev,np.ma.masked_array):
            wlevf=np.ma.masked_array(wlevf,mask=wlev.mask)
        
    else:
        # just copy the data
        wlevf,Mf=wlev,M

    Np=len(pers)
    Ns=wlevf.shape[1]
    if newpers:
        # only use some of the frequencies
        iuse=[np.arange(0,Mf.shape[1])]*Ns
        istill=np.arange(0,Ns,dtype=int)

        # intervals to bootstrap
        nsplit=500
        iboot=np.linspace(0,wlev.shape[0],nsplit+1)[1:-1].astype(int)
        iboot=np.cumsum(np.bincount(iboot,minlength=wlev.shape[0]))
        
        # create bootstrap intervals
        Nb=50
        btpk=np.ndarray([wlev.shape[0],Nb],dtype=bool)
        for kb in range(0,Nb):
            tok=np.random.choice(nsplit,int(nsplit*0.75),replace=False)
            tok=np.bincount(tok,minlength=nsplit).astype(bool)
            btpk[:,kb]=tok[iboot]

        # create arrays
        X=np.ma.masked_array(np.ndarray([Np*2,Ns]),
                             mask=np.zeros([Np*2,Ns],dtype=bool))
        Xb=np.ndarray([Np*2,Ns,Nb])
        while len(istill):
            for ks in istill:
                # compute coefficients for this time series
                ix=iuse[ks]
                Mfi=Mf[:,ix]
                X[ix,ks],rsd,rank,s=np.linalg.lstsq(Mf[:,ix],wlevf[:,ks],rcond=None)
                for kb in range(0,Nb):
                    # with various bootstrap sets
                    iok=btpk[:,kb]
                    Xb[ix,ks,kb],rsd,rank,s=np.linalg.lstsq(Mfi[iok,:],wlevf[iok,ks],rcond=None)

            # re-arrange coefficients and get uncertainty
            ii=np.arange(0,X.shape[0],2)
            Xu=np.var(Xb,axis=2)
            Xu=np.power(Xu[ii,:]+Xu[ii,:],0.5)
            Xh=X[ii,:]+1j*X[ii+1,:]

            # identify values without data
            istill=np.where(np.min(np.divide(np.abs(Xh),Xu),axis=0)<1.)[0]
            for ks in istill:
                # delete the worst-constrained value
                idel=np.argmin(np.divide(np.abs(Xh[:,ks]),Xu[:,ks]))
                iuse[ks]=np.array(list(set(iuse[ks])-set([idel*2,idel*2+1])))
                X[idel*2:idel*2+2,ks]=0.
                X.mask[idel*2:idel*2+2,ks]=True

    else:
        # compute coefficients
        X,rsd,rank,s=np.linalg.lstsq(Mf,wlevf,rcond=None)

        
    # prediction, without filtering
    prd=np.dot(M,X)
    wlevr=wlev-prd

    # re-arrange coefficients
    ii=np.arange(0,X.shape[0],2)
    cfs=X[ii,:]+1j*X[ii+1,:]

    return cfs,pers,tref,prd,wlevr

#----------END OF TIDE GAGE READING CODES----------------------------

#--------START OF CODES FOR PLOTTING------------------------------------

def somestressloc(region='Cascadia'):
    """
    :param        region: region of interest (default: 'Cascadia')
    :return      stressloc: some reasonable stress locations
    """

    if region=='Parkfield':
        stressloc=[[239.17-360,36.29],[239.5048-360,35.9462],[239.89-360,35.57]]
    elif region=='Cascadia':
        stressloc=[[-124,48.8],[-123.3,47.6],[-122.2,49.2],[-125.1,47.9],[-122.9,44.8]]
    elif region=='Shikoku':
        stressloc=[[132.6,33.5],[133.6,34.1],[136.3,34.4],[133.6,32.1]]
    else:
        stressloc=[[-124,48.8],[-123.3,47.6],[-122.2,49.2],[-125.1,47.9],[-122.9,44.8]]
    stressloc = np.atleast_2d(stressloc)

    return stressloc

def someloadloc(region='Cascadia'):
    """
    :param        region: region of interest (default: 'Cascadia')
    :return      loadloc: some reasonable load locations
    """

    loadloc=np.append(someloadloc_water(region),someloadloc_land(region),axis=0)

    ix=np.argsort(loadloc[:,1])
    loadloc=loadloc[ix,:]

    return loadloc


def someloadloc_water(region='Cascadia'):
    """
    :param        region: region of interest (default: 'Cascadia')
    :return      loadloc: some reasonable load locations
    """

    if region=='Cascadia':
        loadloc = [[-124.3,45.4],[-125.3,48.5],[-122.9,48.8]]
    elif region=='Parkfield':
        loadloc=[[-121.9,36.6],[-120.8,35.2],[-119.7,34.4]]
    elif region=='Shikoku':
        loadloc=[[132.5,33.8],[132.2,33],[133.8,33.3],[135,34],[134.1,34.6]]
    else:
        loadloc = [[-124.3,45.4],[-125.3,48.5],[-122.9,48.8]]
    loadloc = np.atleast_2d(loadloc)

    ix=np.argsort(loadloc[:,1])
    loadloc=loadloc[ix,:]


    return loadloc

def someloadloc_land(region='Cascadia'):
    """
    :param        region: region of interest (default: 'Cascadia')
    :return      loadloc: some reasonable load locations
    """

    if region=='Cascadia':
        loadloc = [[-123.4,44.8],[-121.85,44.8],[-123.6,47.7],[-124.2,48],
                   [-124.5,48.9],[-122.9,49.7]]
    elif region=='Parkfield':
        loadloc = [[-119.7,36.3],[-120.8,36.2],[-119.0,34.5],[-118.8,36.9],
                   [-119.1,35.0]]
    elif region=='Shikoku':
        loadloc=[[132.9,33.4],[133.1,33.9],[134.3,34],[132.9,34.5]]
    else:
        loadloc = [[-123.4,44.8],[-121.85,44.8],[-123.6,47.7],[-124.2,48],
                   [-124.5,48.9],[-122.9,49.7]]
    loadloc = np.atleast_2d(loadloc)

    ix=np.argsort(loadloc[:,1])
    loadloc=loadloc[ix,:]


    return loadloc


def startmap(p=None,region='Cascadia',lonlim=None,latlim=None):
    """
    create the beginning of a map
    :param            p: an original axis (will be deleted but position kept)
    :param       lonlim: longitude limits
    :param       latlim: latitude limits
    :return           p: handle to the axis plotted
    :param        tform: transform used for projection
    """

    if region=='Cascadia':
        londef,latdef=np.array([-130,-120]),np.array([40,52])
    elif region=='Parkfield':
        londef,latdef=np.array([-125,-115]),np.array([32,38])
    elif region=='Shikoku':
        londef,latdef=np.array([130,139]),np.array([29,37])
        
    if lonlim is None:
        lonlim=londef
    if latlim is None:
        latlim=latdef
    
    if p is not None:
        ps = p.get_position()
        ps = tuple([ps.x0,ps.y0,ps.width,ps.height])
        p.remove()
    else:
        ps = None
        
    extent=tuple(np.append(lonlim,latlim))
    tform = ccrs.LambertConformal(np.mean(lonlim))
    p = plt.axes(ps,projection=ccrs.LambertConformal(np.mean(lonlim)),
                 extent=extent)
    #tform = ccrs.PlateCarree(np.mean(lonlim))
    # p = plt.axes(ps,projection=tform, #ccrs.PlateCarree(np.mean(lonlim)),
    #              extent=extent)
    p.coastlines()
    # p.add_feature(cartopy.feature.OCEAN)
    # p.add_feature(cartopy.feature.LAND)

    # grids
    xsp = general.roundsigfigs(np.diff(lonlim)/4,1)
    lontk = np.arange(round(lonlim[0]-5,1),round(lonlim[1]+5,1),xsp)

    ysp = general.roundsigfigs(np.diff(latlim)/4,1)
    lattk = np.arange(round(latlim[0],1),round(latlim[1],1),ysp)

    lontk=np.unique(np.append(lontk,lonlim+np.array([-1,1])*30))
    lattk=np.unique(np.append(lattk,latlim+np.array([-1,1])*30))
    p.gridlines(xlocs=lontk,ylocs=lattk)

    return p,tform

def junk():

    m = Basemap(llcrnrlon=lonlim[0],llcrnrlat=latlim[0],
                urcrnrlon=lonlim[1],urcrnrlat=latlim[1],
                projection='lcc',resolution='l',
                lat_0=latlim.mean(),lon_0=lonlim.mean(),
                suppress_ticks=True)

    m.drawlsmask(land_color='whitesmoke',ocean_color='aliceblue',lakes=True,
                 grid=1.25)
    #m.shadedrelief()
    m.drawcoastlines()

    m.drawmeridians(lontk,labels=[0,0,0,1])

    m.drawparallels(lattk,labels=[0,1,0,0])

    m.drawstates()
    m.drawcountries()


#---------END OF CODES FOR PLOTTING--------------------------------------


#----------START OF MISCELLANEOUS CODES FOR READING----------------------

def median_wave_height(rgn='Cascadia',trange=None,tspc=3.):
    """
    :param      rgn: region of interest
    :param   trange: time range of interest
    :param     tspc: time spacing in hours
    :return    whgt: wave height in meters
    :return    wtms: times for these wave heights
    """

    # a reference location
    locref=somestressloc(rgn)
    dfm=defm(rgn=rgn)
    dfm.picklocs(specloc=np.median(locref,axis=0))

    # initialize object for the wave info
    dsts={'Cascadia':2,'Shikoku':3.,'Parkfield':6}
    dstmax=dsts.get(rgn,2.)
    wvs=ecmwfload(defm=dfm,load_type='waves')
    wvs.initcalc(dstmax=dstmax)

    # get the values through time
    wvs.calcstress_throughtime(trange=trange,usesaved=True,tspc=tspc)

    # extract the relevant values
    whgt=wvs.meanload
    wtms=wvs.tms

    return whgt,wtms


def median_wind_speed(rgn='Cascadia',trange=None,tspc=3.):
    """
    :param      rgn: region of interest
    :param   trange: time range of interest
    :param     tspc: time spacing in hours
    :return    wspd: wind speed in m / s
    :return    wtms: times for these wind speeds
    """

    # a reference location
    locref=somestressloc(rgn)
    dfm=defm(rgn=rgn)
    dfm.picklocs(specloc=np.median(locref,axis=0))

    # initialize object for the wave info
    dsts={'Cascadia':2,'Shikoku':3.,'Parkfield':6}
    dstmax=dsts.get(rgn,2.)
    wvs=ecmwfload(defm=dfm,load_type='wind')
    wvs.initcalc(dstmax=dstmax)

    # get the values through time
    wvs.calcstress_throughtime(trange=trange,usesaved=True,tspc=tspc)

    # extract the relevant values
    wspd=wvs.meanload
    wtms=wvs.tms

    return wspd,wtms


def median_atm_pressure(rgn='Cascadia',trange=None,tspc=3.,drange=1.,
                        withstress=False):
    """
    :param      rgn: region of interest
    :param   trange: time range of interest
    :param     tspc: time spacing in hours
    :param   drange: distance range in degrees
    :param  withstress: use the pressure means calculated with the stress
                             (default: False)
    :return    wspd: wind speed in m / s
    :return    wtms: times for these wind speeds
    """

    # a reference location
    locref=somestressloc(rgn)
    dfm=defm(rgn=rgn)
    dfm.picklocs(specloc=np.median(locref,axis=0))

    # initialize object for the wave info
    dsts={'Cascadia':2,'Shikoku':3.,'Parkfield':6}
    dstmax=dsts.get(rgn,2.)
    wvs=ecmwfload(defm=dfm,load_type='pressure')

    if withstress:
        # get the values through time
        wvs.initcalc(dstmax=drange)
        wvs.calcstress_throughtime(trange=trange,usesaved=True,tspc=tspc)

        # extract the relevant values
        mprs=wvs.meanload
        ptms=wvs.tms
        
    else:
        # specify the times
        t1,t2=trange[0],trange[1]+datetime.timedelta(hours=tspc)
        t1=datetime.datetime(t1.year,t1.month,t1.day)
        wvs.tms=np.arange(0,(t2-t1).total_seconds(),tspc*3600)
        wvs.tms=np.array([t1+datetime.timedelta(seconds=tm)
                          for tm in wvs.tms])
        ii=np.logical_and(wvs.tms>=trange[0],wvs.tms<=trange[1])
        wvs.tms=wvs.tms[ii]

        # read the relevant portion
        wvs.read_meanload(drange=drange)

        # extract the relevant values
        mprs=wvs.meanload
        ptms=wvs.tms

    return mprs,ptms

def compare_pressure(region='Parkfield',drange=[0.5,1,2,3,4,5],
                     trange=None,tms=None,prs=None,delmean=True,
                     addlocal=True,lbls=None):
    """
    :param     region: region of interest
    :param     drange: distance ranges to compare in degrees
    :param     trange: time range of interest
    :param        tms: a list of the times
    :param        prs: a list of the pressures
    :param       lbls: labels of interest
    :return       tms: a list of the times
    :return       prs: a list of the pressures
    :return      lbls: labels of interest
    """

    if trange is None:
        trange=[datetime.datetime(2005,1,1),
                datetime.datetime(2005,4,1)]
    elif trange == 'all':
        trange=[datetime.datetime(2000,1,1),
                datetime.datetime(2019,7,1)]

    if prs is None or tms is None:
        tms,prs=[],[]
        for k in range(0,len(drange)):
            mprs,ptms=median_atm_pressure(trange=trange,drange=drange[k],
                                          rgn=region,withstress=False)
            
            prs.append(mprs)
            tms.append(ptms)

        lbls=['{:g}'.format(dr) for dr in drange]

        if addlocal:
            lbls=lbls+['local']
            ptms,mprs=read_local_pressure(station='Bakersfield')
            prs.append(mprs)
            tms.append(ptms)

    plt.close()
    p = plt.axes()
    cols=graphical.colors(len(lbls))
    h=[]

    for k in range(0,len(lbls)):
        ii=np.logical_and(tms[k]>=trange[0],tms[k]<=trange[1])
        tmsi=np.array([matplotlib.dates.date2num(tm) 
                       for tm in tms[k][ii]])
        prsi=prs[k][ii]
        if delmean:
            prsi=prsi-np.ma.mean(prsi)
        hh,=p.plot_date(tmsi,prsi,color=cols[k],linestyle='-',
                        marker=None)
        h.append(hh)
    p.set_xlim([matplotlib.dates.date2num(trange[0]),
                matplotlib.dates.date2num(trange[1])])

    lg=p.legend(h,lbls)

    return tms,prs,lbls

def read_local_pressure(station='Bakersfield'):
    """
    :param          station: station  of interest
    :return             tms: times of the data
    :return             prs: pressures in Pa
    :return              tr: the times listed as a sac file
    """

    # identify file to read
    fdir=os.path.join(os.environ['DATA'],'SURFACE','LOCAL_WEATHER')
    fname=os.path.join(fdir,station)
    
    # read header data
    fl=open(fname,'r')
    hdr=fl.readline().split(',')


    # relevant indice
    idate=np.where(['DATE' in hdri for hdri in hdr])[0][0]
    iprs=np.where(['HourlySeaLevelPressure' in hdri for hdri in hdr])[0][0]

    # read the data
    vls=np.loadtxt(fname,skiprows=1,delimiter=',',dtype=str)

    # pressures
    prs=vls[:,iprs]

    iok=np.where(np.array([len(vl) for vl in prs])>0)[0]
    prs=prs[iok]

    jok=np.where(~np.array(['s' in vl for vl in prs]))[0]
    prs,iok=prs[jok],iok[jok]

    prs=prs.astype(float)*3386.39

    # read    
    fmt='%Y-%m-%dT%H:%M:%S'
    tms=np.array([datetime.datetime.strptime(tm[0:-1],fmt) for tm in vls[iok,0]])

    return tms,prs


#----------END OF MISCELLANEOUS CODES FOR READING----------------------
