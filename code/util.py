#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 15:57:52 2021

@author: rebecca
"""
import obspy
from obspy.geodetics import degrees2kilometers
import numpy as np
import math

def calc_peak(motion):
    """Calculates the peak absolute response"""
    peak = max(abs(min(motion)), max(motion))
    return peak

def catEventToFileName(catalogEntry):
    year = str(catalogEntry.origins[0].time.year).zfill(4)
    month = str(catalogEntry.origins[0].time.month).zfill(2)
    day = str(catalogEntry.origins[0].time.day).zfill(2)
    hour = str(catalogEntry.origins[0].time.hour).zfill(2)
    minute = str(catalogEntry.origins[0].time.minute).zfill(2)
    second = str(catalogEntry.origins[0].time.second).zfill(2)
    fileName = year+month+day+'_'+hour+minute+second+'.a'
    return fileName


def dateToFileName(date):
    year = date[0:4]
    month = date[5:7]
    day = date[8:10]
    hour = date[11:13]
    minute =date[14:16]
    second = date[17:19]
    fileName = year+month+day+'_'+hour+minute+second+'.a'
    return fileName

def filenameToDate(filename):
    import datetime
    year = int(filename[0:4])
    month = int(filename[4:6])
    day = int(filename[6:8])
    hour = int(filename[9:11])
    minute = int(filename[11:13])
    second = int(filename[13:15])
    date = datetime.datetime(year, month, day, hour, minute, second)
    return date

def catEventToDate(catalogEntry):
    year = catalogEntry.origins[0].time.year
    month = catalogEntry.origins[0].time.month
    day = catalogEntry.origins[0].time.day
    hour = catalogEntry.origins[0].time.hour
    minute = catalogEntry.origins[0].time.minute
    second = catalogEntry.origins[0].time.second
    # date = {'year':year,'month':month,'day':day,'hour':hour,'minute':minute,'second':second}
    date = datetime.datetime(year, month, day, hour, minute, second)
    return date
    # append fileName to list catFiles
    # run [k for k,v in Counter(catFiles).items() if v>1]  to find duplicate
    # go to catalog.ml to remove

def spheredist(loc1,loc2): # FROM JESS
    """
    :param     loc1: [lon1,lat1,depth1] or Nx2 array of locations
    :param     loc2: [lon2,lat2,depth2] or Nx2 array of locations
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

def flatdist(loc1,loc2): # FROM JESS
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

def findnearest(londes,latdes,lonhave,lathave): # FROM JESS
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

def find_nearby_data(data, inv, event, max_radius =100000, min_radius = 0): # atm only 2d

    ev_lat = event.origins[0].latitude
    ev_lon = event.origins[0].longitude
    ev_depth = event.origins[0].depth
    data_use = obspy.Stream()
    for tr in data:
        sta_name = tr.stats.network+'.'+tr.stats.station+'.'+tr.stats.location+'.'+tr.stats.channel
        sta_loc = inv.get_coordinates(sta_name)
        sta_lat = sta_loc['latitude']
        sta_lon = sta_loc['longitude']
        sta_depth = -sta_loc['elevation']
        degrees_dist, azimuth = spheredist([ev_lat, ev_lon], [sta_lat, sta_lon])
        dist = degrees2kilometers(degrees_dist) # assumes perfectly spherical earth
        if dist<max_radius and dist>min_radius:
            data_use.append(tr)
    return data_use

def calc_hypo_dist(event, tr, inv): # atm only 2d

    ev_lat = event.origins[0].latitude
    ev_lon = event.origins[0].longitude
    ev_depth = event.origins[0].depth

    sta_name = tr.stats.network+'.'+tr.stats.station+'.'+tr.stats.location+'.'+tr.stats.channel
    sta_loc = inv.get_coordinates(sta_name)
    sta_lat = sta_loc['latitude']
    sta_lon = sta_loc['longitude']
    sta_depth = -sta_loc['elevation']

    degrees_dist, azimuth = spheredist([ev_lat, ev_lon], [sta_lat, sta_lon])
    epi_dist = degrees2kilometers(degrees_dist) # assumes perfectly spherical earth

    depth = abs(ev_depth/1000 - sta_depth/1000)
    hyp_dist = math.sqrt(epi_dist **2 + depth**2)
    return hyp_dist