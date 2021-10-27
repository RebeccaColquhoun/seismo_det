#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 15:57:52 2021

@author: rebecca
"""


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
