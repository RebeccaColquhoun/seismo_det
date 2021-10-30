#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 19 11:44:21 2021

@author: rebecca
"""

fig, axs = plt.subplots(2,3)
for i in range(0, len(eq.data)):
    axs[int(np.floor(i/3))][i%3].plot(eq._cached_params["tau_p"][i], color='black')
    start = (eq.picks[i]-eq.data[i].stats.starttime)*eq.data[i].stats.sampling_rate
    end = start+eq.data[i].stats.sampling_rate*4
    axs[int(np.floor(i/3))][i%3].hlines([0.63], 0, 180000, color='pink')
    axs[int(np.floor(i/3))][i%3].vlines([start, end], 0, 10000, color='lightblue')
    axs[int(np.floor(i/3))][i%3].axis(xmin = start-100, xmax=end+3000, ymin=0, ymax=10)
plt.show()