import numpy as np
import datetime as dt
import pandas as pd
import obspy
#import STRAINPROC
import glob,os
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import matplotlib.dates as mdates
pylab.rcParams['figure.figsize']=10,6
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

class ZoomPan:   #https://stackoverflow.com/users/1629298/seadoodude
    def __init__(self):
        self.press = None
        self.cur_xlim = None
        self.cur_ylim = None
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.xpress = None
        self.ypress = None


    def zoom_factory(self, ax, base_scale = 2.):
        def zoom(event):
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()

            xdata = event.xdata # get event x location
            ydata = event.ydata # get event y location

            if event.button == 'down':
                # deal with zoom in
                scale_factor = 1 / base_scale
            elif event.button == 'up':
                # deal with zoom out
                scale_factor = base_scale
            else:
                # deal with something that should never happen
                scale_factor = 1
                print(event.button)

            new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
            new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

            relx = (cur_xlim[1] - xdata)/(cur_xlim[1] - cur_xlim[0])
            rely = (cur_ylim[1] - ydata)/(cur_ylim[1] - cur_ylim[0])

            ax.set_xlim([xdata - new_width * (1-relx), xdata + new_width * (relx)])
            ax.set_ylim([ydata - new_height * (1-rely), ydata + new_height * (rely)])
            ax.figure.canvas.draw()

        fig = ax.get_figure() # get the figure of interest
        fig.canvas.mpl_connect('scroll_event', zoom)

        return zoom

    def pan_factory(self, ax):
        def onPress(event):
            if event.inaxes != ax: return
            self.cur_xlim = ax.get_xlim()
            self.cur_ylim = ax.get_ylim()
            self.press = self.x0, self.y0, event.xdata, event.ydata
            self.x0, self.y0, self.xpress, self.ypress = self.press

        def onRelease(event):
            self.press = None
            ax.figure.canvas.draw()

        def onMotion(event):
            if self.press is None: return
            if event.inaxes != ax: return
            dx = event.xdata - self.xpress
            dy = event.ydata - self.ypress
            self.cur_xlim -= dx
            self.cur_ylim -= dy
            ax.set_xlim(self.cur_xlim)
            ax.set_ylim(self.cur_ylim)

            ax.figure.canvas.draw()

        fig = ax.get_figure() # get the figure of interest

        # attach the call back
        fig.canvas.mpl_connect('button_press_event',onPress)
        fig.canvas.mpl_connect('button_release_event',onRelease)
        fig.canvas.mpl_connect('motion_notify_event',onMotion)

        #return the function
        return onMotion
        
def timdata(tr):
    """
    :param     tr:   a waveform or trace
    :return   tim:   times
    :return  data:   data
    """
    
    if isinstance(tr,obspy.Trace):
        # all the times
        tim = tr.times("matplotlib")

        # data
        data = tr.data


    return tim,data


    
def picking_IRIS(st,interval,starttime,endtime,time1,fname):
    '''
    :param                     st: stream
    :param               interval: interval of time for plotting window
    :param              starttime: start time of windows to observe
    :param                endtime: end time of windows to observe
    :param                  time1: interpolated time record of strain
    :param                  fname: name of file to save noise to
    :return df_picks_correct_time: dataframe of picks
    '''
    
    
    #from matplotlib.dates import date2num
    import matplotlib.dates as mdates
    # initiate picks dataframe
    df_picks = pd.read_csv(fname, index_col=0)
    
    #set up number of windows to view
    no_windows = round((endtime-starttime)/dt.timedelta(days=interval/2))
    #identify noisy periods in windows
    for j in range(no_windows):
        tst = pd.to_datetime(starttime) + dt.timedelta(days = interval/2*j)
        tnd = tst+dt.timedelta(days=interval)
        tstp,tndp=mdates.date2num(tst),mdates.date2num(tnd)
                 
        
        
        #plot window
        
        tim_0,data_0=timdata(st.select(channel='G0-na')[0])
        ii_0=np.logical_and(tim_0>=tstp,tim_0<=tndp)
        tim_1,data_1=timdata(st.select(channel='G1-na')[0])
        ii_1=np.logical_and(tim_1>=tstp,tim_1<=tndp)
        tim_2,data_2=timdata(st.select(channel='G2-na')[0])
        ii_2=np.logical_and(tim_2>=tstp,tim_2<=tndp)
        tim_3,data_3=timdata(st.select(channel='G3-na')[0])
        ii_3=np.logical_and(tim_3>=tstp,tim_3<=tndp)
        
        boolarr = np.logical_and(time1>=tst,time1<=tnd)
        time_windows = time1[boolarr]
                     
        plt.close('all')
        fig=plt.figure()
        ax0 = plt.subplot(4,1,1)
        ax0.set_title('Scroll to zoom')

        scale = 1.1
        zp = ZoomPan()
        figZoom = zp.zoom_factory(ax0, base_scale = scale)
        figPan = zp.pan_factory(ax0)
        s = 1
        plt.plot_date(tim_0[ii_0],data_0[ii_0],linestyle='-',marker=None,label='G0',color='#ca0020')
        ax0.autoscale()
        ax0.set_xlim([tst,tnd]) 
        
        ax1 = plt.subplot(4,1,2, sharex = ax0)
        plt.plot_date(tim_1[ii_1],data_1[ii_1],linestyle='-',marker=None,label='G1',color='#f4a582')
        
        ax2 = plt.subplot(4,1,3, sharex = ax0)
        plt.plot_date(tim_2[ii_2],data_2[ii_2],linestyle='-',marker=None,label='G2',color='#92c5de')
        
        ax3 = plt.subplot(4,1,4, sharex = ax0)
        plt.plot_date(tim_3[ii_3],data_3[ii_3],linestyle='-',marker=None,label='G3',color='#0571b0')
        
        #click start and end point of noisy period
        figure = plt.gcf()  # get current figure
        figure.set_size_inches(16,9)
        pts = plt.ginput(2,timeout = 15)
        plt.show()
        
        #append noisy interval to dataframe
        noisy=[]
        noise_identified=[]
        for sublist in pts:
            for item in sublist:
                noisy.append(item)
        noise_identified = [noisy]
        
        if len(noisy) ==4:
            df2=pd.DataFrame(noise_identified,columns=['Start_Time','Start_offset','End_Time', 'End_offset'])
            df2.drop('Start_offset', axis='columns', inplace=True)
            df2.drop('End_offset', axis='columns', inplace=True)
            
            #Convert to datetime array
            df2.Start_Time = mdates.num2date(df2.Start_Time)
            df2.End_Time = mdates.num2date(df2.End_Time)
            
            #Round to nearest 1 mins
            s1 = df2.iloc[:,0]
            s2 = df2.iloc[:,1]

            s3 = pd.Series(s1).dt.round("10min")
            s4 = pd.Series(s2).dt.round("10min")
            df2.Start_Time = s3
            df2.End_Time = s4
            
             #make sure noisy interval starts and ends at an actual datapoint
            
            df_picks = df_picks.append(df2, ignore_index=True)
            plt.close('all')
        else:
            plt.close('all')
            
    return df_picks