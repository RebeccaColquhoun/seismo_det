#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 12:07:14 2020

@author: Rebecca
"""

import matplotlib.pyplot as plt
import matplotlib
import NZfunctions
import numpy as np
import os
import datetime
import pandas as pd
from obspy import read_events
from obspy.geodetics import locations2degrees
import random
# An "interface" to matplotlib.axes.Axes.hist() method

#matplotlib.use('TkAgg')

files = os.listdir('/home/earthquakes1/homes/Rebecca/NZPaperData/attributes/')
files.sort(reverse=True)
print(len(files))
noComp = 0

eqFolders = NZfunctions.NZopenEQList()
myCat, numEQ = NZfunctions.NZmakeCat()
cat = NZfunctions.catEventsWithData(myCat, files)

dataCat = []
filesBig = []
catBig = []
eqFoldersData = []
eqFoldersBig = []
filesSml = []
catSml = []
eqFoldersSml = []

foreshocksList = []
aftershocksList = []


def makeBlankCat():
    myCat, numEQ = NZfunctions.NZmakeCat()
    cat = myCat.copy()
    cat.clear()
    return cat


def sortCatalog(division=4.0, minimumMag=0):
    '''creates a catalog which only contains events with a template AKA usable
    events also produces a catalog, list of files and list of folders with
    mag >= 4, and another mag<4.

    AFFECTS THE GLOBAL VARIABLES, so no need to return anything

    division is the line between large and small events

    folders need to be blanked at global level before use'''
    eqFolders = NZfunctions.NZopenEQList()

    dataCat = makeBlankCat()
    for j in range(0, len(eqFolders)):
        print(j)
        # print('tempates', j)
        try:
            NZfunctions.NZLoadTempl(eqFolders[j])
        except Exception:
            print('no template')
        else:
            dataCat.append(myCat[j])
            eqFoldersData.append(eqFolders[j])
            # these are equivilent to files
    # print('sizes')

    catBig = makeBlankCat()
    catSml = makeBlankCat()
    for k in range(0, len(dataCat)):
        # print('sizes', k)
        if dataCat[k].magnitudes[0].mag >= division:
            filesBig.append(files[k])
            catBig.append(dataCat[k])
            eqFoldersBig.append(eqFoldersData[k])
        elif dataCat[k].magnitudes[0].mag < division and dataCat[k].magnitudes[0].mag >= minimumMag:
            filesSml.append(files[k])
            catSml.append(dataCat[k])
            eqFoldersSml.append(eqFoldersData[k])
    with open('filesBigUntil2015.txt', 'w') as f:
        for item in filesBig:
            f.write("%s\n" % item)
    catBig.write('catBigUntil2015.ml', "QUAKEML")
    with open('eqFoldersBigUntil2015.txt', 'w') as f:
        for item in eqFoldersBig:
            f.write("%s\n" % item)
    with open('filesSmlUntil2015.txt', 'w') as f:
        for item in filesSml:
            f.write("%s\n" % item)
    catSml.write('catSmlUntil2015.ml', "QUAKEML")
    with open('eqFoldersSmlUntil2015.txt', 'w') as f:
        for item in eqFoldersSml:
            f.write("%s\n" % item)


def loadSorted():
    filesBig = [line.rstrip('\n') for line in open('filesBig.txt')]
    catBig = read_events('catBig.ml')
    eqFoldersBig = [line.rstrip('\n') for line in open('eqFoldersBig.txt')]
    filesSml = [line.rstrip('\n') for line in open('filesSml.txt')]
    catSml = read_events('catSml.ml')
    eqFoldersSml = [line.rstrip('\n') for line in open('eqFoldersSml.txt')]
    return filesBig, catBig, eqFoldersBig, filesSml, catSml, eqFoldersSml


def fsAsNumber(detections):
    '''param: detections list
       return: foreshocks
               aftershocks'''
    foreshocks = []
    aftershocks = []
    for i in detections:
        if i < 1800:
            foreshocks.append(i)
        else:
            aftershocks.append(i)
    return foreshocks, aftershocks


def plotHist(peakLocations2, peakLocations3, peakLocations4, typeOfPlot='comp', zoom=False):
    '''
    inputs:
        typeOfPlot = 'stat' or 'comp'
        zoom = True or False
        peakLocations2 = list of detections at 2 s.d.
        peakLocations3 = list of detections at 3 s.d.
        peakLocations4 = list of detections at 4 s.d.

    produces a histogram plot which is automatically showed

    returns:
        n2, n3, n4 =  the numbers in bins at 2, 3, 4 s.d. '''
    if zoom is True:
        binLimits = np.arange(1730, 1871, 1)  # for zoom
    else:
        binLimits = np.arange(0, 3600, 10)  # for complete record
    # PLOT
    n2, bins, patches = plt.hist(peakLocations2, binLimits, label='PC more than 2 s.d. above mean')
    n3, bins, patches = plt.hist(peakLocations3, binLimits, label='PC more than 3 s.d. above mean')
    n4, bins, patches = plt.hist(peakLocations4, binLimits, label='PC more than 4 s.d. above mean')

    plt.grid(axis='y')
    plt.xlabel('Time relative to mainshock arrival (s)')
    plt.ylabel('Counts')
    if typeOfPlot == 'stat':
        plt.title('Histogram of interstation phase coherence peaks', wrap=True)
    elif typeOfPlot == 'comp':
        plt.title('Histogram of intercomponent phase coherence peaks', wrap=True)
    else:
        print('pls specify stat or comp')

    if zoom is True:
        plt.xlim(1730, 1880)  # ?
        plt.xticks(np.arange(1730, 1880, 10), np.arange(-70, 80, 10))
    else:
        plt.xlim(0, 3600)
        plt.xticks(np.arange(0, 3601, 200), np.arange(-1800, 1801, 200))  # for complete record
        # for zoom
    plt.legend()
    plt.show()

    return n2, n3, n4


def findPeaks(listOfFiles):
    '''finds all peaks
        input:
            listOfFiles: a list of files to be looked at
        returns:
            peakLocations2: peaks at 2 s.d. in interstation coherence from all earthquakes with a file in list of files
            peakLocations3: peaks at 3 s.d. in interstation coherence from all earthquakes with a file in list of files
            peakLocations4: peaks at 4 s.d. in interstation coherence from all earthquakes with a file in list of files
            peakLocations2Comp: peaks at 2 s.d. in intercomponent coherence from all earthquakes with a file in list of files
            peakLocations3Comp: peaks at 3 s.d. in intercomponent coherence from all earthquakes with a file in list of files
            peakLocations4Comp: peaks at 4 s.d. in intercomponent coherence from all earthquakes with a file in list of files
            noComp: lists number of events with only an interstation coherence
    '''
    peakLocations2 = []
    peakLocations3 = []
    peakLocations4 = []
    peakLocations2Comp = []
    peakLocations3Comp = []
    peakLocations4Comp = []
    noComp = 0
    for i in range(0, len(listOfFiles)):
        att = np.load('/home/earthquakes1/homes/Rebecca/NZPaperData/attributes/'+listOfFiles[i], allow_pickle=True)
        for peak2 in att[5]:
            peakLocations2.append(peak2)
        for peak3 in att[7]:
            peakLocations3.append(peak3)
        for peak4 in att[9]:
            peakLocations4.append(peak4)
        if len(att) > 17:
            #print('comp')
            for peak2C in att[17]:
                if peak2C not in [1798, 1799, 1800, 1801, 1802]:
                    peakLocations2Comp.append(peak2C)
            for peak3C in att[19]:
                peakLocations3Comp.append(peak3C)
            for peak4C in att[21]:
                peakLocations4Comp.append(peak4C)
        else:
            #print('no comp')
            noComp += 1
    return peakLocations2, peakLocations3, peakLocations4, peakLocations2Comp, peakLocations3Comp, peakLocations4Comp, noComp

def findPeaksEachEQ(listOfFiles):
    '''finds all peaks
        input:
            listOfFiles: a list of files to be looked at
        returns:
            peakLocations2: peaks at 2 s.d. in interstation coherence from all earthquakes with a file in list of files
            peakLocations3: peaks at 3 s.d. in interstation coherence from all earthquakes with a file in list of files
            peakLocations4: peaks at 4 s.d. in interstation coherence from all earthquakes with a file in list of files
            peakLocations2Comp: peaks at 2 s.d. in intercomponent coherence from all earthquakes with a file in list of files
            peakLocations3Comp: peaks at 3 s.d. in intercomponent coherence from all earthquakes with a file in list of files
            peakLocations4Comp: peaks at 4 s.d. in intercomponent coherence from all earthquakes with a file in list of files
            noComp: lists number of events with only an interstation coherence
    '''
    #peakLocations2 = []
    #peakLocations3 = []
    #peakLocations4 = []
    peakLocations2Comp = []
    #peakLocations3Comp = []
    #peakLocations4Comp = []
    noComp = 0
    for i in range(0, len(listOfFiles)):
        det = np.load('/home/earthquakes1/homes/Rebecca/NZPaperData/detectionsAll/'+listOfFiles[i][0:17]+'detections.npy', allow_pickle=True)
        #peakLocations2.append([])
        #peakLocations3.append([])
        #peakLocations4.append([])
        peakLocations2Comp.append([])
        #peakLocations3Comp.append([])
        #peakLocations4Comp.append([])
        #for peak2 in att[5]:
        #    peakLocations2[i].append(peak2)
        #for peak3 in att[7]:
        #    peakLocations3[i].append(peak3)
        #for peak4 in att[9]:
        #    peakLocations4[i].append(peak4)
        #if len(att) > 17:
            # print('comp')
        for peak2C in det[6]:
            if peak2C not in [1798, 1799, 1800, 1801, 1802]:
                peakLocations2Comp[i].append(peak2C)
        #    for peak3C in att[19]:
        #        if peak3C not in [1798, 1799, 1800, 1801, 1802]:
        #            peakLocations3Comp[i].append(peak3C)
        #    for peak4C in att[21]:
        #        if peak4C not in [1798, 1799, 1800, 1801, 1802]:
        #            peakLocations4Comp[i].append(peak4C)
        else:
            #print('no comp')
            noComp += 1
    return peakLocations2Comp #, peakLocations3, peakLocations4, peakLocations2Comp, peakLocations3Comp, peakLocations4Comp, noComp

def findPeaksEachEQAll(listOfFiles):
    '''finds all peaks
        input:
            listOfFiles: a list of files to be looked at
        returns:
            peakLocations2: peaks at 2 s.d. in interstation coherence from all earthquakes with a file in list of files
            peakLocations3: peaks at 3 s.d. in interstation coherence from all earthquakes with a file in list of files
            peakLocations4: peaks at 4 s.d. in interstation coherence from all earthquakes with a file in list of files
            peakLocations2Comp: peaks at 2 s.d. in intercomponent coherence from all earthquakes with a file in list of files
            peakLocations3Comp: peaks at 3 s.d. in intercomponent coherence from all earthquakes with a file in list of files
            peakLocations4Comp: peaks at 4 s.d. in intercomponent coherence from all earthquakes with a file in list of files
            noComp: lists number of events with only an interstation coherence
    '''
    peakLocations2 = []
    peakLocations3 = []
    peakLocations4 = []
    peakLocations2Comp = []
    peakLocations3Comp = []
    peakLocations4Comp = []
    noComp = 0
    for i in range(0, len(listOfFiles)):
        det = np.load('/home/earthquakes1/homes/Rebecca/NZPaperData/detectionsAll/'+listOfFiles[i][0:17]+'detections.npy', allow_pickle=True)
        peakLocations2.append([])
        peakLocations3.append([])
        peakLocations4.append([])
        peakLocations2Comp.append([])
        peakLocations3Comp.append([])
        peakLocations4Comp.append([])
        for peak2 in det[0]:
            peakLocations2[i].append(peak2)
        for peak3 in det[2]:
            peakLocations3[i].append(peak3)
        for peak4 in det[4]:
            peakLocations4[i].append(peak4)
        #if len(att) > 17:
        #     print('comp')
        for peak2C in det[6]:
            #if peak2C not in [1798, 1799, 1800, 1801, 1802]:
            peakLocations2Comp[i].append(peak2C)
        for peak3C in det[8]:
            #if peak3C not in [1798, 1799, 1800, 1801, 1802]:
            peakLocations3Comp[i].append(peak3C)
        for peak4C in det[10]:
            #if peak4C not in [1798, 1799, 1800, 1801, 1802]:
            peakLocations4Comp[i].append(peak4C)
        #else:
            #print('no comp')
        #    noComp += 1
    return peakLocations2, peakLocations3, peakLocations4, peakLocations2Comp, peakLocations3Comp, peakLocations4Comp, noComp


def findPeaksOld(listOfFiles):
    '''OLD
    USES DATA IN NZDATA2
    finds all peaks
    input:
        listOfFiles: a list of files to be looked at
    returns:
        peakLocations2: peaks at 2 s.d. in interstation coherence from all earthquakes with a file in list of files
        peakLocations3: peaks at 3 s.d. in interstation coherence from all earthquakes with a file in list of files
        peakLocations4: peaks at 4 s.d. in interstation coherence from all earthquakes with a file in list of files
        peakLocations2Comp: peaks at 2 s.d. in intercomponent coherence from all earthquakes with a file in list of files
        peakLocations3Comp: peaks at 3 s.d. in intercomponent coherence from all earthquakes with a file in list of files
        peakLocations4Comp: peaks at 4 s.d. in intercomponent coherence from all earthquakes with a file in list of files
        noComp: lists number of events with only an interstation coherence'''
    peakLocations2 = []
    peakLocations3 = []
    peakLocations4 = []
    peakLocations2Comp = []
    peakLocations3Comp = []
    peakLocations4Comp = []
    noComp = 0
    for i in range(0, len(listOfFiles)):
        att = np.load('/home/earthquakes1/homes/Rebecca/NZData2/attributes5/'+listOfFiles[i], allow_pickle=True)
        for peak2 in att[5]:
            peakLocations2.append(peak2)
        for peak3 in att[7]:
            peakLocations3.append(peak3)
        for peak4 in att[9]:
            peakLocations4.append(peak4)
        if len(att) > 17:
            #print('comp')
            for peak2C in att[17]:
                if peak2C not in [1798, 1799, 1800, 1801, 1802]:
                    peakLocations2Comp.append(peak2C)
            for peak3C in att[19]:
                peakLocations3Comp.append(peak3C)
            for peak4C in att[21]:
                peakLocations4Comp.append(peak4C)
        else:
            #print('no comp')
            noComp += 1
    return peakLocations2, peakLocations3, peakLocations4, peakLocations2Comp, peakLocations3Comp, peakLocations4Comp, noComp

def findPeaksForDeclustering(listOfFiles):
    '''finds all peaks
        input:
            listOfFiles: a list of files to be looked at
        returns:
            peakLocations2: peaks at 2 s.d. in interstation coherence from all earthquakes with a file in list of files
            peakLocations3: peaks at 3 s.d. in interstation coherence from all earthquakes with a file in list of files
            peakLocations4: peaks at 4 s.d. in interstation coherence from all earthquakes with a file in list of files
            peakLocations2Comp: peaks at 2 s.d. in intercomponent coherence from all earthquakes with a file in list of files
            peakLocations3Comp: peaks at 3 s.d. in intercomponent coherence from all earthquakes with a file in list of files
            peakLocations4Comp: peaks at 4 s.d. in intercomponent coherence from all earthquakes with a file in list of files
            noComp: lists number of events with only an interstation coherence
    '''
    peakLocations2 = []
    peakLocations3 = []
    peakLocations4 = []
    peakLocations2Comp = []
    peakLocations3Comp = []
    peakLocations4Comp = []
    noComp = 0
    for i in range(0, len(listOfFiles)):
        att = np.load('/home/earthquakes1/homes/Rebecca/NZPaperData/attributes/'+listOfFiles[i], allow_pickle=True)
        peakLocations2.append([])
        peakLocations3.append([])
        peakLocations4.append([])
        peakLocations2Comp.append([])
        peakLocations3Comp.append([])
        peakLocations4Comp.append([])
        for peak2 in att[5]:
            peakLocations2[i].append(peak2)
        for peak3 in att[7]:
            peakLocations3[i].append(peak3)
        for peak4 in att[9]:
            peakLocations4[i].append(peak4)
        if len(att) > 17:
            #print('comp')
            for peak2C in att[17]:
                peakLocations2Comp[i].append(peak2C)
            for peak3C in att[19]:
                peakLocations3Comp[i].append(peak3C)
            for peak4C in att[21]:
                peakLocations4Comp[i].append(peak4C)
        else:
            #print('no comp')
            noComp += 1
    return peakLocations2, peakLocations3, peakLocations4, peakLocations2Comp, peakLocations3Comp, peakLocations4Comp, noComp


def sortCatalogExcludeMatches(matches):
    eqFolders = NZfunctions.NZopenEQList()
    for j in range(0, len(eqFolders)):
        try:
            NZfunctions.NZLoadTempl(eqFolders[j])
        except Exception:
            print('no template')
        else:
            if eqFolders[j] not in matches:
                dataCat.append(cat[j])
                eqFoldersData.append(eqFolders[j])
    for k in range(0, len(dataCat)):
        if dataCat[k].magnitudes[0].mag >= 4.0:
            filesBig.append(files[k])
            catBig.append(dataCat[k])
            eqFoldersBig.append(eqFoldersData[k])


def findTimeSpacing(cat):
    '''finds time between all events and the next event
    input: cat -- catalog to look at events in
    returns: myEvents -- list of times of all events in dataCat
    difference -- time difference between events and next event IN MINUTES??
    '''

    myEvents = []
    for i in range(0, len(cat)):
        myEvents.append((cat[i].origins[0].time).datetime)
        # bigEvents.append((catBig[i].origins[0].time).datetime)
    # compare matches to my events, find those which dont appear
    difference = []
    for i in range(0, len(myEvents)-1):
        difference.append(myEvents[i]-myEvents[i+1])

    difference = np.array(difference)
    difference = difference/timedelta(minutes=1)
    shortDiff = []
    longDiff = []

    for i in difference:
        if i < 1000:  # DIFFERENCE LESS THAN 1000 MINUTES
            shortDiff.append(i)
        else:
            longDiff.append(i)

    return myEvents, difference


def findNonClustered(difference, files, timeInterval):
    '''find events which are more than x minutes apart and make list of their files
    parameters:
        difference - array of times between event and next event in minutes
        files - list of files
        timeInterval - critical difference between events.
    returns:
        toUse - a list of files more than timeInterval away from the next event.

    '''
    toUse = [files[0]]
    for i in range(0, len(difference)):
        if difference[i] > timeInterval:
            toUse.append(files[i+1])
    return toUse


def foreshocks(detections, foreshocksList, aftershocksList, averageWindow=400):
    '''


    '''
    n, bins = np.histogram(detections, np.arange(0, 3600, 1))
    subd = n - np.average(n[0:averageWindow])
    foreshocksList.append(sum(subd[0:1798]))
    aftershocksList.append(sum(subd[1803:3600]))
    return foreshocksList, aftershocksList

def sortByDate(cat, files):
    '''
    sorts files and catalog entries into lists by year
    parameters:
        cat -- catalog of events
        files -- list of files which are each an event in cat
     returns:
         yearCat -- a list of a catalog for each year
         yearFiles -- a list of files for each year
    '''
    sortCatalog()
    yearCat = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
    yearFiles = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
    for eventNo in range(0, len(cat)):
        # print(eventNo)
        time = NZfunctions.catEventToDate(cat[eventNo])
        year = int(str(time.year)[2:4])
        yearCat[year].append(cat[eventNo])
        yearFiles[year].append(files[eventNo])
    return yearCat, yearFiles


def decluster(cluster, catFOrDeclustering, filesForDeclustering, minMag=0, maxMag=10):
    '''
    declusters events at intervals set by cluster to find biggest event in interval
    parameters:
        cluster: min interval between events not to be considered clustered
        cat: catalog of events
    returns:
        biggestEvents -- list of catalog events to use
        filesUse -- list of files to use

    '''
    print('declustering')
    biggestEvents = makeBlankCat()
    filesUse = []
    declusteringRadius = 0.3 #in degrees, radius to remove events within
    surroundingEvents = []
    surroundingEventsAll = []
    print(minMag, maxMag)
    for eventNo in range(0, len(catFOrDeclustering)):
        # print(eventNo)
        time = NZfunctions.catEventToDate(catFOrDeclustering[eventNo])
        eventMag = catFOrDeclustering[eventNo].magnitudes[0].mag
        eventLat = catFOrDeclustering[eventNo].origins[0].latitude
        eventLong = catFOrDeclustering[eventNo].origins[0].longitude
        events1HourAfter = []
        events1HourBefore = []
        diffBefore = datetime.timedelta(0)
        diffAfter = datetime.timedelta(0)
        distance = 0
        counterA = 1
        counterB = 1
        eventMagA = []
        eventMagB = []
        print(eventMag)
        if eventMag<maxMag and eventMag>minMag:
            print('eventMag within bounds')
            while abs(diffBefore) < datetime.timedelta(hours=cluster) and eventNo-counterB >= 0:
                #print('before')
                eventBeforeTime = NZfunctions.catEventToDate(catFOrDeclustering[eventNo-counterB])
                diffBefore = eventBeforeTime - time
                eventBeforeLat = catFOrDeclustering[eventNo-counterB].origins[0].latitude
                eventBeforeLong = catFOrDeclustering[eventNo-counterB].origins[0].longitude
                distance = locations2degrees(eventLat, eventLong, eventBeforeLat, eventBeforeLong)
                if abs(diffBefore) < datetime.timedelta(hours=cluster):
                    if abs(distance) > declusteringRadius:
                        events1HourBefore.append(catFOrDeclustering[eventNo-counterB])
                        eventMagB.append(catFOrDeclustering[eventNo-counterB].magnitudes[0].mag)
                counterB += 1
            while abs(diffAfter) < datetime.timedelta(hours=cluster) and eventNo+counterA < len(catFOrDeclustering):
                #print('after', eventNo+counterA)
                eventAfterTime = NZfunctions.catEventToDate(catFOrDeclustering[eventNo+counterA])
                diffAfter = eventAfterTime - time
                eventAfterLat = catFOrDeclustering[eventNo+counterA].origins[0].latitude
                eventAfterLong = catFOrDeclustering[eventNo+counterA].origins[0].longitude
                distance = locations2degrees(eventLat, eventLong, eventAfterLat, eventAfterLong)
                if abs(diffAfter) < datetime.timedelta(hours=cluster):
                    if abs(distance) > declusteringRadius:
                        events1HourAfter.append(catFOrDeclustering[eventNo+counterA])
                        eventMagA.append(catFOrDeclustering[eventNo+counterA].magnitudes[0].mag)
                counterA += 1
            print(len(events1HourBefore), len(events1HourAfter))
            surroundingEventsAll.append([eventNo, events1HourBefore, events1HourAfter])
    
            if (len(eventMagA) == 0 or eventMag > max(eventMagA)+0) and (len(eventMagB) == 0 or eventMag > max(eventMagB)+0):
                biggestEvents.append(catFOrDeclustering[eventNo])
                filesUse.append(filesForDeclustering[eventNo])
                surroundingEvents.append([eventNo, events1HourBefore, events1HourAfter])
            #import code
            #code.interact(local=locals())
    return biggestEvents, filesUse, surroundingEvents, surroundingEventsAll

# Convenience function to calculate the great circle distance between two points on a spherical Earth.

# This method uses the Vincenty formula in the special case of a spherical Earth. For more accurate values use the geodesic distance calculations of geopy 



def use(clusterInterval=100, chosenAverageWindow=400, standardDeviationLevel=2, useSml='3'):
    '''
    Args:
        clusterInterval (INT): DESCRIPTION.
        chosenAverageWindow (INT)
        standardDeviationLevel (INT)
    Returns:
        peakLocations2Comp (LIST): DESCRIPTION.
        peakLocations2CompBig (LIST): DESCRIPTION.
        peakLocations2CompBigF (LIST): DESCRIPTION.
        peakLocations2CompSml (LIST): DESCRIPTION.
        peakLocations2CompSmlF (LIST): DESCRIPTION.

    '''
    #filesBig, catBig, eqFoldersBig, filesSml, catSml, eqFoldersSml = hp.loadSorted()
# =============================================================================
#     files35 = [line.rstrip('\n') for line in open('files35Until2015.txt')]
#     cat35 = read_events('cat35Until2015.ml')
#     eqFolders35 = [line.rstrip('\n') for line in open('eqFolders35Until2015.txt')]
#     files37 = [line.rstrip('\n') for line in open('files37Until2015.txt')]
#     cat37 = read_events('cat37Until2015.ml')
#     eqFolders37 = [line.rstrip('\n') for line in open('eqFolders37Until2015.txt')]
#     filesBig = [line.rstrip('\n') for line in open('filesBigUntil2015.txt')]
#     catBig = read_events('catBigUntil2015.ml')
#     eqFoldersBig = [line.rstrip('\n') for line in open('eqFoldersBigUntil2015.txt')]
#     filesSml = [line.rstrip('\n') for line in open('filesSmlUntil2015.txt')]
#     catSml = read_events('catSmlUntil2015.ml')
#     eqFoldersSml = [line.rstrip('\n') for line in open('eqFoldersSmlUntil2015.txt')]
# 
# =============================================================================
    print('set to blank')
    peakLocations2, peakLocations3, peakLocations4, peakLocations2Comp, peakLocations3Comp, peakLocations4Comp, noComp = [], [], [], [], [], [], []
    peakLocations2Big, peakLocations3Big, peakLocations4Big, peakLocations2CompBig, peakLocations3CompBig, peakLocations4CompBig, noCompBig = [], [], [], [], [], [], []
    peakLocations2BigF, peakLocations3BigF, peakLocations4BigF, peakLocations2CompBigF, peakLocations3CompBigF, peakLocations4CompBigF, noCompBigF = [], [], [], [], [], [], []
    peakLocations2Sml, peakLocations3Sml, peakLocations4Sml, peakLocations2CompSml, peakLocations3CompSml, peakLocations4CompSml, noCompSml = [], [], [], [], [], [], []
    peakLocations2SmlF, peakLocations3SmlF, peakLocations4SmlF, peakLocations2CompSmlF, peakLocations3CompSmlF, peakLocations4CompSmlF, noCompSmlF = [], [], [], [], [], [], []
    biggestEventsBig, filesUseBig = [], []
    biggestEventsSml, filesUseSml = [], []

    foreshocksList, aftershocksList = [], []
    print('blanked')
    filesBig, catBig, eqFoldersBig, filesSml, catSml, eqFoldersSml = loadSorted()
    minimumMag = 0
    if useSml == '3.5' or useSml == '35':
        print("only M3.5+")
        filesSml = [line.rstrip('\n') for line in open('files35.txt')]
        catAllAboveMinMag = read_events('cat35.ml') + catBig
        eqFoldersSml = [line.rstrip('\n') for line in open('eqFolders35.txt')]
        minimumMag = 3.5
    elif useSml == '3.7' or useSml == '37':
        print("only M3.7+")
        filesSml = [line.rstrip('\n') for line in open('files37.txt')]
        catAllAboveMinMag = read_events('cat37.ml') +catBig
        eqFoldersSml = [line.rstrip('\n') for line in open('eqFolders37.txt')]
        minimumMag = 3.7
    else:
        catAllAboveMinMag = cat #catSml + catBig
    files = []  
    for i in catAllAboveMinMag:
        files.append(NZfunctions.catEventToFileName(i)+'attributes.npy')
    print('loaded')
    #peakLocations2, peakLocations3, peakLocations4, peakLocations2Comp, peakLocations3Comp, peakLocations4Comp, noComp = findPeaks(files)
    peakLocations2Comp = findPeaksEachEQ(files)
    peakLocations2Comp = np.concatenate(peakLocations2Comp)
    #peakLocations2Big, peakLocations3Big, peakLocations4Big, peakLocations2CompBig, peakLocations3CompBig, peakLocations4CompBig, noCompBig = findPeaks(filesBig)
    peakLocations2CompBig = findPeaksEachEQ(filesBig)
    peakLocations2CompBig = np.concatenate(peakLocations2CompBig)
    print('decluster big')
    biggestEventsBig, filesUseBig, surroundingEventsBig, surroundingEventsBigAll = decluster(clusterInterval, catBig, filesBig, minMag=4)

    #peakLocations2BigF, peakLocations3BigF, peakLocations4BigF, peakLocations2CompBigF, peakLocations3CompBigF, peakLocations4CompBigF, noCompBigF = findPeaks(filesUseBig)
    peakLocations2CompBigF= findPeaksEachEQ(filesUseBig)
    peakLocations2CompBigF = np.concatenate(peakLocations2CompBigF)
    difference = list(set(filesBig).symmetric_difference(set(filesUseBig)))
    # print(difference)
    # import code
    # code.interact(local=locals())

    #peakLocations2Sml, peakLocations3Sml, peakLocations4Sml, peakLocations2CompSml, peakLocations3CompSml, peakLocations4CompSml, noCompSml = findPeaks(filesSml)
    peakLocations2CompSml = findPeaksEachEQ(filesSml)
    peakLocations2CompSml = np.concatenate(peakLocations2CompSml)
    print('decluster sml')
    declusteredSml, filesDeclusteredSml, surroundingEventsSml, surroundingEventsSmlAll = decluster(clusterInterval, catAllAboveMinMag, files, minMag=minimumMag, maxMag=4)
    #declustered, filesDeclustered, surroundingEvents, surroundingEventsAll = decluster(clusterInterval, catAllAboveMinMag, files, minMfilag=0, maxMag=4.)
    # sort to only look at declustered events smaller than M4
    catDeclusteredSml = makeBlankCat()
    for k in range(0, len(declusteredSml)):
        #print('sizes', k)
        if declusteredSml[k].magnitudes[0].mag < 4.0 and declusteredSml[k].magnitudes[0].mag > minimumMag:
            filesUseSml.append(filesDeclusteredSml[k])
            catDeclusteredSml.append(declusteredSml[k])
    print("length of filesUseSml", len(filesUseSml))
    #peakLocations2SmlF, peakLocations3SmlF, peakLocations4SmlF, peakLocations2CompSmlF, peakLocations3CompSmlF, peakLocations4CompSmlF, noCompSmlF = findPeaks(filesUseSml)
    peakLocations2CompSmlF= findPeaksEachEQ(filesUseSml)
    peakLocations2CompSmlF = np.concatenate(peakLocations2CompSmlF)
    # import code
    # code.interact(local=locals())
    # foreshocks, aftershocks = fsAsNumber(peakLocations2Comp)
    # print(foreshocks,aftershocks)
    # foreshocksBig, aftershocksBig = fsAsNumber(peakLocations2CompBig)
    # print(foreshocksBig, aftershocksBig)
    print('foreshocks')
    # print(len(foreshocksList), len(peakLocations2Comp), len(peakLocations2CompBig))
    # for each set of detections, append number of foreshocks and aftershocks to foreshocksList and aftershocksList respectively
    foreshocksList, aftershocksList = foreshocks(peakLocations2Comp, foreshocksList, aftershocksList, chosenAverageWindow)
    foreshocksList, aftershocksList = foreshocks(peakLocations2CompBig, foreshocksList, aftershocksList, chosenAverageWindow)
    foreshocksList, aftershocksList = foreshocks(peakLocations2CompBigF, foreshocksList, aftershocksList, chosenAverageWindow)
    foreshocksList, aftershocksList = foreshocks(peakLocations2CompSml, foreshocksList, aftershocksList, chosenAverageWindow)
    foreshocksList, aftershocksList = foreshocks(peakLocations2CompSmlF, foreshocksList, aftershocksList, chosenAverageWindow)
    # print(len(foreshocksList))
    fsh = np.array(foreshocksList)
    ash = np.array(aftershocksList)
    ratio = fsh/ash
    print('table')
    if useSml != '3':
        name = np.array(['all', 'big', 'big unclustered', useSml, useSml+' unclustered'])
    else:
        name = np.array(['all', 'big', 'big unclustered', 'sml', 'sml unclustered'])
    # print(len(name), len(fsh), len(ash), len(ratio))
    print('clustering interval (hours)', clusterInterval)
    numEvents = [len(files), len(filesBig), len(biggestEventsBig), len(filesSml), len(catDeclusteredSml)]
    d = {'name': name, 'numberOfEvents': numEvents, 'foreshocks': fsh, 'aftershocks': ash, 'ratio': ratio}
    table = pd.DataFrame(d)
    print(table)
    return peakLocations2Comp, peakLocations2CompBig, peakLocations2CompBigF, peakLocations2CompSml, peakLocations2CompSmlF, foreshocksList, aftershocksList, ratio, numEvents, surroundingEventsBig, surroundingEventsSml, surroundingEventsBigAll, surroundingEventsSmlAll, catBig, catAllAboveMinMag

def useDepths(clusterInterval=100, chosenAverageWindow=400, standardDeviationLevel=2, useSml='3'):
    '''
    Args:
        clusterInterval (INT): DESCRIPTION.
        chosenAverageWindow (INT)
        standardDeviationLevel (INT)
    Returns:
        peakLocations2Comp (LIST): DESCRIPTION.
        peakLocations2CompBig (LIST): DESCRIPTION.
        peakLocations2CompBigF (LIST): DESCRIPTION.
        peakLocations2CompSml (LIST): DESCRIPTION.
        peakLocations2CompSmlF (LIST): DESCRIPTION.

    '''

    print('set to blank')
    peakLocations2, peakLocations3, peakLocations4, peakLocations2Comp, peakLocations3Comp, peakLocations4Comp, noComp = [], [], [], [], [], [], []
    peakLocations2Big, peakLocations3Big, peakLocations4Big, peakLocations2CompBig, peakLocations3CompBig, peakLocations4CompBig, noCompBig = [], [], [], [], [], [], []
    peakLocations2BigF, peakLocations3BigF, peakLocations4BigF, peakLocations2CompBigF, peakLocations3CompBigF, peakLocations4CompBigF, noCompBigF = [], [], [], [], [], [], []
    peakLocations2Sml, peakLocations3Sml, peakLocations4Sml, peakLocations2CompSml, peakLocations3CompSml, peakLocations4CompSml, noCompSml = [], [], [], [], [], [], []
    peakLocations2SmlF, peakLocations3SmlF, peakLocations4SmlF, peakLocations2CompSmlF, peakLocations3CompSmlF, peakLocations4CompSmlF, noCompSmlF = [], [], [], [], [], [], []
    biggestEventsBig, filesUseBig = [], []
    biggestEventsSml, filesUseSml = [], []

    foreshocksList, aftershocksList = [], []
    print('blanked')
    filesBig, catBig, eqFoldersBig, filesSml, catSml, eqFoldersSml = loadSorted()
    minimumMag = 0
    catAllAboveMinMag = cat
    
    files = []  
    for i in catAllAboveMinMag:
        files.append(NZfunctions.catEventToFileName(i)+'attributes.npy')
    
    declusteredCat, filesUse, surroundingEvents, surroundingEventsAll = decluster(clusterInterval, catAllAboveMinMag, files, minMag=4)
    
    shallowFiles = []
    for i in declusteredCat:
        if i.origins[0].depth <= 70000.0:
            shallowFiles.append(NZfunctions.catEventToFileName(i)+'attributes.npy')
    print('loaded')
    
    peakLocations2Comp = findPeaksEachEQ(filesUse)
    peakLocations2Comp = np.concatenate(peakLocations2Comp)
    peakLocations2CompShallow = findPeaksEachEQ(shallowFiles)
    peakLocations2CompShallow = np.concatenate(peakLocations2CompShallow)
    
    foreshocksList, aftershocksList = foreshocks(peakLocations2Comp, foreshocksList, aftershocksList, chosenAverageWindow)
    foreshocksList, aftershocksList = foreshocks(peakLocations2CompShallow, foreshocksList, aftershocksList, chosenAverageWindow)
    
    fsh = np.array(foreshocksList)
    ash = np.array(aftershocksList)
    ratio = fsh/ash
    

    name = np.array(['all', 'shallow'])
    numEvents = [len(filesUse), len(shallowFiles)]
    d = {'name': name, 'numberOfEvents': numEvents, 'foreshocks': fsh, 'aftershocks': ash, 'ratio': ratio}
    table = pd.DataFrame(d)
    print(table)
    '''peakLocations2Comp = findPeaksEachEQ(files)
    peakLocations2Comp = np.concatenate(peakLocations2Comp)
    peakLocations2CompBig = findPeaksEachEQ(filesBig)
    peakLocations2CompBig = np.concatenate(peakLocations2CompBig)
    print('decluster big')
    biggestEventsBig, filesUseBig, surroundingEventsBig, surroundingEventsBigAll = decluster(clusterInterval, catBig, filesBig, minMag=4)

    peakLocations2CompBigF= findPeaksEachEQ(filesUseBig)
    peakLocations2CompBigF = np.concatenate(peakLocations2CompBigF)
    difference = list(set(filesBig).symmetric_difference(set(filesUseBig)))

    peakLocations2CompSml = findPeaksEachEQ(filesSml)
    peakLocations2CompSml = np.concatenate(peakLocations2CompSml)
    print('decluster sml')
    declusteredSml, filesDeclusteredSml, surroundingEventsSml, surroundingEventsSmlAll = decluster(clusterInterval, catAllAboveMinMag, files, minMag=minimumMag, maxMag=4.0)
    # sort to only look at declustered events smaller than M4
    catDeclusteredSml = makeBlankCat()
    for k in range(0, len(declusteredSml)):
        #print('sizes', k)
        if declusteredSml[k].magnitudes[0].mag < 4.0 and declusteredSml[k].magnitudes[0].mag > minimumMag:
            filesUseSml.append(filesDeclusteredSml[k])
            catDeclusteredSml.append(declusteredSml[k])
    print("length of filesUseSml", len(filesUseSml))
    peakLocations2CompSmlF= findPeaksEachEQ(filesUseSml)
    peakLocations2CompSmlF = np.concatenate(peakLocations2CompSmlF)

    print('foreshocks')
    # for each set of detections, append number of foreshocks and aftershocks to foreshocksList and aftershocksList respectively
    foreshocksList, aftershocksList = foreshocks(peakLocations2Comp, foreshocksList, aftershocksList, chosenAverageWindow)
    foreshocksList, aftershocksList = foreshocks(peakLocations2CompBig, foreshocksList, aftershocksList, chosenAverageWindow)
    foreshocksList, aftershocksList = foreshocks(peakLocations2CompBigF, foreshocksList, aftershocksList, chosenAverageWindow)
    foreshocksList, aftershocksList = foreshocks(peakLocations2CompSml, foreshocksList, aftershocksList, chosenAverageWindow)
    foreshocksList, aftershocksList = foreshocks(peakLocations2CompSmlF, foreshocksList, aftershocksList, chosenAverageWindow)
    fsh = np.array(foreshocksList)
    ash = np.array(aftershocksList)
    ratio = fsh/ash
    print('table')
    if useSml != '3':
        name = np.array(['all', 'big', 'big unclustered', useSml, useSml+' unclustered'])
    else:
        name = np.array(['all', 'big', 'big unclustered', 'sml', 'sml unclustered'])
    print('clustering interval (hours)', clusterInterval)
    numEvents = [len(files), len(filesBig), len(biggestEventsBig), len(filesSml), len(catDeclusteredSml)]
    d = {'name': name, 'numberOfEvents': numEvents, 'foreshocks': fsh, 'aftershocks': ash, 'ratio': ratio}
    table = pd.DataFrame(d)
    print(table)
    return peakLocations2Comp, peakLocations2CompBig, peakLocations2CompBigF, peakLocations2CompSml, peakLocations2CompSmlF, foreshocksList, aftershocksList, ratio, numEvents, surroundingEventsBig, surroundingEventsSml, surroundingEventsBigAll, surroundingEventsSmlAll, catBig, catAllAboveMinMag'''

'''
def useBS(clusterInterval=100, chosenAverageWindow=700, standardDeviationLevel=2, useSml='3'):
    '''''''
    Args:
        clusterInterval (INT): DESCRIPTION.
        chosenAverageWindow (INT)
        standardDeviationLevel (INT)
    Returns:
        peakLocations2Comp (LIST): DESCRIPTION.
        peakLocations2CompBig (LIST): DESCRIPTION.
        peakLocations2CompBigF (LIST): DESCRIPTION.
        peakLocations2CompSml (LIST): DESCRIPTION.
        peakLocations2CompSmlF (LIST): DESCRIPTION.

    '''
'''
    print('set to blank')
    peakLocations2, peakLocations3, peakLocations4, peakLocations2Comp, peakLocations3Comp, peakLocations4Comp, noComp = [], [], [], [], [], [], []
    peakLocations2F, peakLocations3F, peakLocations4F, peakLocations2CompF, peakLocations3CompF, peakLocations4CompF, noCompF = [], [], [], [], [], [], []
    peakLocations2Big, peakLocations3Big, peakLocations4Big, peakLocations2CompBig, peakLocations3CompBig, peakLocations4CompBig, noCompBig = [], [], [], [], [], [], []
    peakLocations2BigF, peakLocations3BigF, peakLocations4BigF, peakLocations2CompBigF, peakLocations3CompBigF, peakLocations4CompBigF, noCompBigF = [], [], [], [], [], [], []
    peakLocations2Sml, peakLocations3Sml, peakLocations4Sml, peakLocations2CompSml, peakLocations3CompSml, peakLocations4CompSml, noCompSml = [], [], [], [], [], [], []
    peakLocations2SmlF, peakLocations3SmlF, peakLocations4SmlF, peakLocations2CompSmlF, peakLocations3CompSmlF, peakLocations4CompSmlF, noCompSmlF = [], [], [], [], [], [], []
    biggestEventsBig, filesUseBig = [], []
    biggestEventsSml, filesUseSml = [], []
    ratiosBS = []
    filesUseAll = []
    foreshocksList, aftershocksList = [], []
    print('blanked')
    filesBig, catBig, eqFoldersBig, filesSml, catSml, eqFoldersSml = loadSorted()
    minimumMag = 0
    if useSml == '3.5':
        print("only M3.5+")
        filesSml = [line.rstrip('\n') for line in open('files35.txt')]
        catAllAboveMinMag = read_events('cat35.ml') + catBig
        eqFoldersSml = [line.rstrip('\n') for line in open('eqFolders35.txt')]
        minimumMag = 3.5
    elif useSml == '3.7':
        print("only M3.7+")
        filesSml = [line.rstrip('\n') for line in open('files37.txt')]
        catAllAboveMinMag = read_events('cat37.ml') + catBig
        eqFoldersSml = [line.rstrip('\n') for line in open('eqFolders37.txt')]
        minimumMag = 3.7
    else:
        catAllAboveMinMag = catSml + catBig
    print('loaded')
    files = []
    for i in catAllAboveMinMag:
        files.append(NZfunctions.catEventToFileName(i)+'attributes.npy')
    peakLocations2CompInd = findPeaksEachEQ(files)

    print('decluster all')
    declusteredAll, filesDeclusteredAll, surroundingEventsAll, surroundingEventsAllAll = decluster(clusterInterval, catAllAboveMinMag, files, minMag=0, maxMag=7.0)
    # sort to only look at declustered events smaller than M4
    catDeclusteredAll = makeBlankCat()
    for k in range(0, len(declusteredAll)):
        # print('sizes', k)
        filesUseAll.append(filesDeclusteredAll[k])
        catDeclusteredAll.append(declusteredAll[k])
    print("length of filesUseAll", len(filesUseAll))

    peakLocations2CompFInd = findPeaksEachEQ(filesUseAll)

    peakLocations2CompBigInd = findPeaksEachEQ(filesBig)

    print('decluster big')
    biggestEventsBig, filesUseBig, surroundingEventsBig, surroundingEventsBigAll = decluster(clusterInterval, catBig, filesBig, minMag=4)

    peakLocations2CompBigFInd = findPeaksEachEQ(filesUseBig)
    peakLocations2CompSmlInd = findPeaksEachEQ(filesSml)

    print('decluster sml')
    declusteredSml, filesDeclusteredSml, surroundingEventsSml, surroundingEventsSmlAll = decluster(clusterInterval, catAllAboveMinMag, files, minMag=minimumMag, maxMag=4.)
    # sort to only look at declustered events smaller than M4
    catDeclusteredSml = makeBlankCat()
    for k in range(0, len(declusteredSml)):
        # print('sizes', k)
        if declusteredSml[k].magnitudes[0].mag < 4.0 and declusteredSml[k].magnitudes[0].mag > minimumMag:
            filesUseSml.append(filesDeclusteredSml[k])
            catDeclusteredSml.append(declusteredSml[k])
    print("length of filesUseSml", len(filesUseSml))

    peakLocations2CompSmlFInd = findPeaksEachEQ(filesUseSml)

    print('bootstrapping')
    for j in range(0, 10):
        foreshocksList, aftershocksList = [], []
        for i in range(0, len(peakLocations2CompInd)):
            n = random.randrange(0, len(peakLocations2CompInd))
            peakLocations2Comp.append(peakLocations2CompInd[n])
    
            peakLocations2CompFInd
        for i in range(0, len(peakLocations2CompFInd)):
            n = random.randrange(0, len(peakLocations2CompFInd))
            peakLocations2CompF.append(peakLocations2CompFInd[n])
    
        for i in range(0, len(peakLocations2CompBigInd)):
            n = random.randrange(0, len(peakLocations2CompBigInd))
            peakLocations2CompBig.append(peakLocations2CompBigInd[n])
    
        for i in range(0, len(peakLocations2CompBigFInd)):
            n = random.randrange(0, len(peakLocations2CompBigFInd))
            peakLocations2CompBigF.append(peakLocations2CompBigFInd[n])
        # difference = list(set(filesBig).symmetric_difference(set(filesUseBig)))
    
        # peakLocations2CompSml = findPeaksEachEQ(filesSml)
        # peakLocations2CompSml = np.concatenate(peakLocations2CompSml)
    
        for i in range(0, len(peakLocations2CompSmlInd)):
            n = random.randrange(0, len(peakLocations2CompSmlInd))
            peakLocations2CompSml.append(peakLocations2CompSmlInd[n])
    
        for i in range(0, len(peakLocations2CompSmlFInd)):
            n = random.randrange(0, len(peakLocations2CompSmlFInd))
            peakLocations2CompSmlF.append(peakLocations2CompSmlFInd[n])
    
        print('foreshocks')
    
        # for each set of detections, append number of foreshocks and aftershocks to foreshocksList and aftershocksList respectively
        foreshocksList, aftershocksList = foreshocks(np.concatenate(peakLocations2Comp), foreshocksList, aftershocksList, chosenAverageWindow)
        foreshocksList, aftershocksList = foreshocks(np.concatenate(peakLocations2CompF), foreshocksList, aftershocksList, chosenAverageWindow)
        foreshocksList, aftershocksList = foreshocks(np.concatenate(peakLocations2CompBig), foreshocksList, aftershocksList, chosenAverageWindow)
        foreshocksList, aftershocksList = foreshocks(np.concatenate(peakLocations2CompBigF), foreshocksList, aftershocksList, chosenAverageWindow)
        foreshocksList, aftershocksList = foreshocks(np.concatenate(peakLocations2CompSml), foreshocksList, aftershocksList, chosenAverageWindow)
        foreshocksList, aftershocksList = foreshocks(np.concatenate(peakLocations2CompSmlF), foreshocksList, aftershocksList, chosenAverageWindow)
        fsh = np.array(foreshocksList)
        ash = np.array(aftershocksList)
        ratio = fsh/ash
        print('table')
        if useSml != '3':
            name = np.array(['all', 'all unclustered', 'big', 'big unclustered', useSml, useSml+' unclustered'])
        else:
            name = np.array(['all', 'all unclustered', 'big', 'big unclustered', 'sml', 'sml unclustered'])
        print('clustering interval (hours)', clusterInterval)
        numEvents = [len(files), len(catDeclusteredAll), len(filesBig), len(biggestEventsBig), len(filesSml), len(catDeclusteredSml)]
        d = {'name': name, 'numberOfEvents': numEvents, 'foreshocks': fsh, 'aftershocks': ash, 'ratio': ratio}
        table = pd.DataFrame(d)
        print(table)
        ratiosBS.append(ratio)
    return peakLocations2Comp, peakLocations2CompBig, peakLocations2CompBigF, peakLocations2CompSml, peakLocations2CompSmlF, foreshocksList, aftershocksList, ratio, numEvents, surroundingEventsBig, surroundingEventsSml, surroundingEventsBigAll, surroundingEventsSmlAll, catBig, catAllAboveMinMag'''


def BSfiles(files):
    filesBS = []
    for i in range(0, len(files)):
        n = random.randrange(0, len(files))
        filesBS.append(files[n])
    return filesBS


def useBS(clusterInterval=100, chosenAverageWindow=800, standardDeviationLevel=2, useSml='3'):
    '''
    Args:
        clusterInterval (INT): DESCRIPTION.
        chosenAverageWindow (INT)
        standardDeviationLevel (INT)
    Returns:
        peakLocations2Comp (LIST): DESCRIPTION.
        peakLocations2CompBig (LIST): DESCRIPTION.
        peakLocations2CompBigF (LIST): DESCRIPTION.
        peakLocations2CompSml (LIST): DESCRIPTION.
        peakLocations2CompSmlF (LIST): DESCRIPTION.

    '''
    #filesBig, catBig, eqFoldersBig, filesSml, catSml, eqFoldersSml = hp.loadSorted()
# =============================================================================
#     files35 = [line.rstrip('\n') for line in open('files35Until2015.txt')]
#     cat35 = read_events('cat35Until2015.ml')
#     eqFolders35 = [line.rstrip('\n') for line in open('eqFolders35Until2015.txt')]
#     files37 = [line.rstrip('\n') for line in open('files37Until2015.txt')]
#     cat37 = read_events('cat37Until2015.ml')
#     eqFolders37 = [line.rstrip('\n') for line in open('eqFolders37Until2015.txt')]
#     filesBig = [line.rstrip('\n') for line in open('filesBigUntil2015.txt')]
#     catBig = read_events('catBigUntil2015.ml')
#     eqFoldersBig = [line.rstrip('\n') for line in open('eqFoldersBigUntil2015.txt')]
#     filesSml = [line.rstrip('\n') for line in open('filesSmlUntil2015.txt')]
#     catSml = read_events('catSmlUntil2015.ml')
#     eqFoldersSml = [line.rstrip('\n') for line in open('eqFoldersSmlUntil2015.txt')]
# 
# =============================================================================
    print('set to blank')
    peakLocations2, peakLocations3, peakLocations4, peakLocations2Comp, peakLocations3Comp, peakLocations4Comp, noComp = [], [], [], [], [], [], []
    peakLocations2Big, peakLocations3Big, peakLocations4Big, peakLocations2CompBig, peakLocations3CompBig, peakLocations4CompBig, noCompBig = [], [], [], [], [], [], []
    peakLocations2BigF, peakLocations3BigF, peakLocations4BigF, peakLocations2CompBigF, peakLocations3CompBigF, peakLocations4CompBigF, noCompBigF = [], [], [], [], [], [], []
    peakLocations2Sml, peakLocations3Sml, peakLocations4Sml, peakLocations2CompSml, peakLocations3CompSml, peakLocations4CompSml, noCompSml = [], [], [], [], [], [], []
    peakLocations2SmlF, peakLocations3SmlF, peakLocations4SmlF, peakLocations2CompSmlF, peakLocations3CompSmlF, peakLocations4CompSmlF, noCompSmlF = [], [], [], [], [], [], []
    biggestEventsBig, filesUseBig = [], []
    biggestEventsSml, filesUseSml = [], []

    foreshocksList, aftershocksList = [], []
    print('blanked')
    filesBig, catBig, eqFoldersBig, filesSml, catSml, eqFoldersSml = loadSorted()
    minimumMag = 0
    if useSml == '3.5' or useSml == '35':
        print("only M3.5+")
        filesSml = [line.rstrip('\n') for line in open('files35.txt')]
        catAllAboveMinMag = read_events('cat35.ml') + catBig
        eqFoldersSml = [line.rstrip('\n') for line in open('eqFolders35.txt')]
        minimumMag = 3.5
    elif useSml == '3.7' or useSml == '37':
        print("only M3.7+")
        filesSml = [line.rstrip('\n') for line in open('files37.txt')]
        catAllAboveMinMag = read_events('cat37.ml') +catBig
        eqFoldersSml = [line.rstrip('\n') for line in open('eqFolders37.txt')]
        minimumMag = 3.7
    else:
        catAllAboveMinMag = cat #catSml + catBig
    files = []
    for i in catAllAboveMinMag:
        files.append(NZfunctions.catEventToFileName(i)+'attributes.npy')
    
    print('loaded')
    
    filesBS = BSfiles(files)
    peakLocations2Comp = findPeaksEachEQ(filesBS)
    peakLocations2Comp = np.concatenate(peakLocations2Comp)
    
    filesBigBS = BSfiles(filesBig)
    peakLocations2CompBig = findPeaksEachEQ(filesBigBS)
    peakLocations2CompBig = np.concatenate(peakLocations2CompBig)
    
    print('decluster big')
    biggestEventsBig, filesUseBig, surroundingEventsBig, surroundingEventsBigAll = decluster(clusterInterval, catBig, filesBig, minMag=4)
    filesUseBigBS = BSfiles(filesUseBig)
    peakLocations2CompBigF= findPeaksEachEQ(filesUseBigBS)
    peakLocations2CompBigF = np.concatenate(peakLocations2CompBigF)
    difference = list(set(filesBig).symmetric_difference(set(filesUseBig)))

    filesSmlBS = BSfiles(filesSml)
    peakLocations2CompSml = findPeaksEachEQ(filesSmlBS)
    peakLocations2CompSml = np.concatenate(peakLocations2CompSml)
    
    print('decluster sml')
    declusteredSml, filesDeclusteredSml, surroundingEventsSml, surroundingEventsSmlAll = decluster(clusterInterval, catAllAboveMinMag, files, minMag=minimumMag, maxMag=4.0)
    # sort to only look at declustered events smaller than M4
    catDeclusteredSml = makeBlankCat()
    for k in range(0, len(declusteredSml)):
        #print('sizes', k)
        if declusteredSml[k].magnitudes[0].mag < 4.0 and declusteredSml[k].magnitudes[0].mag > minimumMag:
            filesUseSml.append(filesDeclusteredSml[k])
            catDeclusteredSml.append(declusteredSml[k])
    print("length of filesUseSml", len(filesUseSml))
    filesUseSmlBS = BSfiles(filesUseSml)
    #peakLocations2SmlF, peakLocations3SmlF, peakLocations4SmlF, peakLocations2CompSmlF, peakLocations3CompSmlF, peakLocations4CompSmlF, noCompSmlF = findPeaks(filesUseSml)
    peakLocations2CompSmlF= findPeaksEachEQ(filesUseSmlBS)
    peakLocations2CompSmlF = np.concatenate(peakLocations2CompSmlF)
    # import code
    # code.interact(local=locals())
    # foreshocks, aftershocks = fsAsNumber(peakLocations2Comp)
    # print(foreshocks,aftershocks)
    # foreshocksBig, aftershocksBig = fsAsNumber(peakLocations2CompBig)
    # print(foreshocksBig, aftershocksBig)
    print('foreshocks')
    # print(len(foreshocksList), len(peakLocations2Comp), len(peakLocations2CompBig))
    # for each set of detections, append number of foreshocks and aftershocks to foreshocksList and aftershocksList respectively
    foreshocksList, aftershocksList = foreshocks(peakLocations2Comp, foreshocksList, aftershocksList, chosenAverageWindow)
    foreshocksList, aftershocksList = foreshocks(peakLocations2CompBig, foreshocksList, aftershocksList, chosenAverageWindow)
    foreshocksList, aftershocksList = foreshocks(peakLocations2CompBigF, foreshocksList, aftershocksList, chosenAverageWindow)
    foreshocksList, aftershocksList = foreshocks(peakLocations2CompSml, foreshocksList, aftershocksList, chosenAverageWindow)
    foreshocksList, aftershocksList = foreshocks(peakLocations2CompSmlF, foreshocksList, aftershocksList, chosenAverageWindow)
    # print(len(foreshocksList))
    fsh = np.array(foreshocksList)
    ash = np.array(aftershocksList)
    ratio = fsh/ash
    print('table')
    if useSml != '3':
        name = np.array(['all', 'big', 'big unclustered', useSml, useSml+' unclustered'])
    else:
        name = np.array(['all', 'big', 'big unclustered', 'sml', 'sml unclustered'])
    # print(len(name), len(fsh), len(ash), len(ratio))
    print('clustering interval (hours)', clusterInterval)
    numEvents = [len(files), len(filesBig), len(biggestEventsBig), len(filesSml), len(catDeclusteredSml)]
    d = {'name': name, 'numberOfEvents': numEvents, 'foreshocks': fsh, 'aftershocks': ash, 'ratio': ratio}
    table = pd.DataFrame(d)
    print(table)
    return peakLocations2Comp, peakLocations2CompBig, peakLocations2CompBigF, peakLocations2CompSml, peakLocations2CompSmlF, foreshocksList, aftershocksList, ratio, numEvents, surroundingEventsBig, surroundingEventsSml, surroundingEventsBigAll, surroundingEventsSmlAll, catBig, catAllAboveMinMag

def useEachEQ(clusterInterval=100, chosenAverageWindow=400, standardDeviationLevel=2, useSml='3.0'):
    '''
    Args:
        clusterInterval (TYPE): DESCRIPTION.

    Returns:
        peakLocations2Comp (TYPE): DESCRIPTION.
        peakLocations2CompBig (TYPE): DESCRIPTION.
        peakLocations2CompBigF (TYPE): DESCRIPTION.
        peakLocations2CompSml (TYPE): DESCRIPTION.
        peakLocations2CompSmlF (TYPE): DESCRIPTION.

    '''
    print('set to blank')
    peakLocations2, peakLocations3, peakLocations4, peakLocations2Comp, peakLocations3Comp, peakLocations4Comp, noComp = [], [], [], [], [], [], []
    peakLocations2Big, peakLocations3Big, peakLocations4Big, peakLocations2CompBig, peakLocations3CompBig, peakLocations4CompBig, noCompBig = [], [], [], [], [], [], []
    peakLocations2BigF, peakLocations3BigF, peakLocations4BigF, peakLocations2CompBigF, peakLocations3CompBigF, peakLocations4CompBigF, noCompBigF = [], [], [], [], [], [], []
    peakLocations2Sml, peakLocations3Sml, peakLocations4Sml, peakLocations2CompSml, peakLocations3CompSml, peakLocations4CompSml, noCompSml = [], [], [], [], [], [], []
    peakLocations2SmlF, peakLocations3SmlF, peakLocations4SmlF, peakLocations2CompSmlF, peakLocations3CompSmlF, peakLocations4CompSmlF, noCompSmlF = [], [], [], [], [], [], []
    biggestEventsBig, filesUseBig = [], []
    biggestEventsSml, filesUseSml = [], []

    print('blanked')
    filesBig, catBig, eqFoldersBig, filesSml, catSml, eqFoldersSml = loadSorted()
    minimumMag = 0
    if useSml == '3.5':
        print("only M3.5+")
        filesSml = [line.rstrip('\n') for line in open('files35.txt')]
        catAllAboveMinMag = read_events('cat35.ml') + catBig
        eqFoldersSml = [line.rstrip('\n') for line in open('eqFolders35.txt')]
        minimumMag = 3.5
    elif useSml == '3.7':
        print("only M3.7+")
        filesSml = [line.rstrip('\n') for line in open('files37.txt')]
        catAllAboveMinMag = read_events('cat37.ml') +catBig
        eqFoldersSml = [line.rstrip('\n') for line in open('eqFolders37.txt')]
        minimumMag = 3.7
    else:
        catAllAboveMinMag = cat #catSml + catBig
        
    print('loaded')
    peakLocations2Comp = findPeaksEachEQ(files)

    peakLocations2CompBig = findPeaksEachEQ(filesBig)
    print('decluster big')
    biggestEventsBig, filesUseBig, surroundingEventsBig, surroundingEventsBigAll = decluster(clusterInterval, catBig, filesBig, minMag=4)

    peakLocations2CompBigF = findPeaksEachEQ(filesUseBig)

    difference = list(set(filesBig).symmetric_difference(set(filesUseBig)))
    # print(difference)
    # import code
    # code.interact(local=locals())

    peakLocations2CompSml = findPeaksEachEQ(filesSml)

    print('decluster sml')
    declusteredSml, filesDeclusteredSml, surroundingEventsSml, surroundingEventsSmlAll = decluster(clusterInterval, catAllAboveMinMag, files, minMag=minimumMag, maxMag=4.)

    # sort to only look at declustered events smaller than M4
    catDeclusteredSml = makeBlankCat()
    for k in range(0, len(declusteredSml)):
        #print('sizes', k)
        if declusteredSml[k].magnitudes[0].mag < 4. and declusteredSml[k].magnitudes[0].mag > minimumMag:
            filesUseSml.append(filesDeclusteredSml[k])
            catDeclusteredSml.append(declusteredSml[k])

    peakLocations2CompSmlF = findPeaks(filesUseSml)
    # import code
    # code.interact(local=locals())
    # foreshocks, aftershocks = fsAsNumber(peakLocations2Comp)
    # print(foreshocks,aftershocks)
    # foreshocksBig, aftershocksBig = fsAsNumber(peakLocations2CompBig)
    # print(foreshocksBig, aftershocksBig)
    print('foreshocks')
    # print(len(foreshocksList), len(peakLocations2Comp), len(peakLocations2CompBig))
    # for each set of detections, append number of foreshocks and aftershocks to foreshocksList and aftershocksList respectively
    if standardDeviationLevel == 2:
        return peakLocations2Comp, peakLocations2CompBig, peakLocations2CompBigF, peakLocations2CompSml, peakLocations2CompSmlF
    elif standardDeviationLevel == 3:
        return peakLocations3Comp, peakLocations3CompBig, peakLocations3CompBigF, peakLocations3CompSml, peakLocations3CompSmlF
    elif standardDeviationLevel == 4:
        return peakLocations4Comp, peakLocations4CompBig, peakLocations4CompBigF, peakLocations4CompSml, peakLocations4CompSmlF

def useCopyPaste(clusterInterval):
    '''
    Args:
        clusterInterval (TYPE): DESCRIPTION.

    Returns:
        peakLocations2Comp (TYPE): DESCRIPTION.
        peakLocations2CompBig (TYPE): DESCRIPTION.
        peakLocations2CompBigF (TYPE): DESCRIPTION.
        peakLocations2CompSml (TYPE): DESCRIPTION.
        peakLocations2CompSmlF (TYPE): DESCRIPTION.

    '''
    hp.loadSorted()

    peakLocations2, peakLocations3, peakLocations4, peakLocations2Comp, peakLocations3Comp, peakLocations4Comp, noComp = hp.findPeaks(hp.files)

    peakLocations2Big, peakLocations3Big, peakLocations4Big, peakLocations2CompBig, peakLocations3CompBig, peakLocations4CompBig, noCompBig = hp.findPeaks(hp.filesBig)

    biggestEventsBig, filesUseBig = hp.decluster(clusterInterval, hp.catBig)

    peakLocations2BigF, peakLocations3BigF, peakLocations4BigF, peakLocations2CompBigF, peakLocations3CompBigF, peakLocations4CompBigF, noCompBigF = hp.findPeaks(filesUseBig)

    peakLocations2Sml, peakLocations3Sml, peakLocations4Sml, peakLocations2CompSml, peakLocations3CompSml, peakLocations4CompSml, noCompSml = hp.findPeaks(hp.filesSml)

    biggestEventsSml, filesUseSml = hp.decluster(clusterInterval, hp.catSml)

    peakLocations2SmlF, peakLocations3SmlF, peakLocations4SmlF, peakLocations2CompSmlF, peakLocations3CompSmlF, peakLocations4CompSmlF, noCompSmlF = hp.findPeaks(filesUseSml)

    # foreshocks, aftershocks = fsAsNumber(peakLocations2Comp)
    # print(foreshocks,aftershocks)
    # foreshocksBig, aftershocksBig = fsAsNumber(peakLocations2CompBig)
    # print(foreshocksBig, aftershocksBig)
    hp.foreshocks(peakLocations2Comp)
    hp.foreshocks(peakLocations2CompBig)
    hp.foreshocks(peakLocations2CompBigF)
    hp.foreshocks(peakLocations2CompSml)
    hp.foreshocks(peakLocations2CompSmlF)

    fsh = np.array(foreshocksList)
    ash = np.array(aftershocksList)
    ratio = fsh/ash

    name = np.array(['all', 'big', 'big unclustered', 'small', 'small unclustered'])
    print('clustering interval (hours)', clusterInterval)
    d = {'name': name, 'foreshocks': fsh, 'aftershocks': ash, 'ratio': ratio}
    table = pd.DataFrame(d)
    print(table)
    return peakLocations2Comp, peakLocations2CompBig, peakLocations2CompBigF, peakLocations2CompSml, peakLocations2CompSmlF

'''
ratioBS = []
for i in range(0, 100):
    print('bootstrap number', i)
    peakLocations2Comp, peakLocations2CompBig, peakLocations2CompBigF, peakLocations2CompSml, peakLocations2CompSmlF, foreshocksList, aftershocksList, ratio, numEvents, surroundingEventsBig, surroundingEventsSml, surroundingEventsBigAll, surroundingEventsSmlAll, catBig, catAllAboveMinMag = useBS(clusterInterval=100, chosenAverageWindow=800, standardDeviationLevel=2, useSml='3')
    ratioBS.append(ratio)

big = []
sml = []
for i in ratioBS:
    big.append(i[2])
    sml.append(i[4])

peakLocations2Comp, peakLocations2CompBig, peakLocations2CompBigF, peakLocations2CompSml, peakLocations2CompSmlF, foreshocksList, aftershocksList, ratio, numEvents, surroundingEventsBig, surroundingEventsSml, surroundingEventsBigAll, surroundingEventsSmlAll, catBig, catAllAboveMinMag = use(clusterInterval=100, chosenAverageWindow=800, standardDeviationLevel=2, useSml='3')
bigTrue = ratio[2]
smlTrue = ratio[4]

big.sort()
sml.sort()

fig, axs = plt.subplots(1, 2, sharey=True, tight_layout=True)
bins = np.arange(-1, 1, 0.01)
axs[0].hist(big, np.arange(-0.1, 0.15, 0.01), color='#59B6D9ff')
axs[1].hist(sml, np.arange(-0.8, 0.4, 0.05), color='#59B6D9ff')
axs[0].axvline(bigTrue, color="#083763ff", label="observed")
axs[1].axvline(smlTrue, color="#083763ff", label="observed")
axs[0].set_ylabel("n")
axs[1].set_xlabel("FS/AS ratio")
axs[0].set_xlabel("FS/AS ratio")
axs[0].axvline(big[14], color='white', linestyle = ':', label="70% confidence")
axs[0].axvline(big[84], color='white', linestyle = ':', label="70% confidence")
axs[1].axvline(sml[14], color='white', linestyle = ':')
axs[1].axvline(sml[84], color='white', linestyle = ':')#, label="70% confidence")
axs[0].axvline(0.163, color='#800066ff', label="expected M1")
axs[1].axvline(0.224, color='#800066ff', label="expected M1") #sml M1
axs[0].axvline(0.17, color='#ff5599ff', label="expected M2")
axs[1].axvline(0.289, color='#ff5599ff', label="expected M2") # sml M2
axs[0].set_title("M4+")
axs[1].set_title("M3+")
axs[1].legend(facecolor='white', framealpha=1)
 #, big[84], facecolor = '', edgecolor = 'white', linewidth=100)
#axs[1].fill_betweenx([0, 20], sml[14], sml[84], color='g', alpha=0.1)
plt.savefig('/home/earthquakes1/homes/Rebecca/ratioBS_all.png')

f = open("ratioBS_37.txt", "w")
f.write([smlTrue, sml[14], sml[84], sml])

f = open("ratioBS_4.txt", "w")
f.write([bigTrue, big[14], big[84], big])


fig, axs = plt.subplots(1, 2, sharey=True, tight_layout=True)
bins = np.arange(-1, 1, 0.01)
axs[1].hist(sml, np.arange(-0.8, 0.4, 0.05), color='#59B6D9ff')
axs[1].axvline(smlTrue, color="#083763ff", label="observed")
axs[0].set_ylabel("n")
axs[0].set_xlabel("FS/AS ratio")
axs[1].axvline(sml[14], color='white', linestyle = ':')
axs[1].axvline(sml[84], color='white', linestyle = ':')#, label="70% confidence")
axs[1].axvline(0.224, color='#800066ff', label="expected M1") #sml M1
axs[1].axvline(0.289, color='#ff5599ff', label="expected M2") # sml M2
axs[1].set_title("M3.7-4")
axs[1].legend(facecolor='white', framealpha=1)'''