import os
import scipy
import numpy as np
import matplotlib.pyplot as plt
import obspy
import pickle
from obspy import UTCDateTime
from obspy.clients.fdsn import Client
import pandas as pd
import math
import figure_sizes
import matplotlib
matplotlib.rcParams.update({'font.size': 20})

magnitudes = np.arange(3,7.1, 0.1)
colors = {'tp':'#7f58af', 'tc':'#e84d8a', 'iv2' : '#64c5eb', 'pgd' : '#7fb646'}
window_lengths = {'0.3':4, '0.5':4.4, '1' : 5.02, '4' : 6.22}
def sort_tp_data(df, mag_lim = 0):
    list_tp_all = list(df.tp_max)
    list_mag_all = list(df.eq_mag)
    list_mag = []
    list_tpmax = []
    count = 0
    for m in range(0, len(list_mag_all)):
        if list_mag_all[m] > mag_lim:
            list_mag.append(list_mag_all[m])
            list_tpmax.append([])
            for d in range(0, len(list_tp_all[m])):
                if list_tp_all[m][d] != None and list_tp_all[m][d]>0:
                    list_tpmax[count].append(list_tp_all[m][d])
            count += 1
    return list_mag, list_tpmax

def sort_tc_data(df, mag_lim = 0):
    list_tc_all = list(df.tc)
    list_mag_all = list(df.eq_mag)
    list_mag = []
    list_tc = []
    count = 0
    for m in range(0, len(list_mag_all)):
        if list_mag_all[m] > mag_lim:
            list_mag.append(list_mag_all[m])
            list_tc.append([])
            for d in range(0, len(list_tc_all[m])):
                if list_tc_all[m][d] != None and list_tc_all[m][d]>0:
                    list_tc[count].append(list_tc_all[m][d])
            count += 1
    return list_mag, list_tc

def sort_iv2_data(df, mag_lim = 0):
    list_iv2_all = list(df.iv2)
    list_mag_all = list(df.eq_mag)
    list_dist_Distance = list(df.iv2_distances)
    list_dist = []
    list_mag = []
    list_iv2 = []
    eq = 0
    for m in range(0, len(list_mag_all)):
        if list_mag_all[m]>mag_lim:
            someTrue = len(list_iv2_all[m])
            for d in range(0, len(list_dist_Distance[m])):
                if list_iv2_all[m][d] != None:
                    list_mag.append(list_mag_all[m])
                    list_iv2.append(list_iv2_all[m][d])
                    list_dist.append(float(str(np.array(list_dist_Distance[m][d]))[:-3]))
    return list_mag, list_iv2, list_dist
def sort_pgd_data(df, mag_lim = 0):
    list_pgd_all = list(df.pgd)
    list_mag_all = list(df.eq_mag)
    list_dist_Distance = list(df.pgd_distances)
    list_dist = []
    list_mag = []
    list_pgd = []
    eq = 0
    for m in range(0, len(list_mag_all)):
        if list_mag_all[m]>mag_lim:
            someTrue = len(list_pgd_all[m])
            for d in range(0, len(list_dist_Distance[m])):
                if list_pgd_all[m][d] != None:
                    list_mag.append(list_mag_all[m])
                    list_pgd.append(list_pgd_all[m][d])
                    list_dist.append(float(str(np.array(list_dist_Distance[m][d]))[:-3]))
                else:
                    someTrue -= 1
            if someTrue >0:
                eq += 1
    return list_mag, list_pgd, list_dist

def calc_tp_mag_lim(df, mag_lim):
    #print(mag_lim)
    list_mags, list_tpmax = sort_tp_data(df, mag_lim)
    params = []
    y_aves_tp = []
    x_aves_tp = []
    i = 0
    for i  in range(0, len(list_mags)):
        if len(list_tpmax[i])>=1:
            mean_tp = np.mean(list_tpmax[i]) 
            std_tp = np.std(list_tpmax[i]) 
            y_tp = [] 
            for j in list_tpmax[i]: 
                if j > mean_tp-2*std_tp and j < mean_tp + 2*std_tp:# and j < 100: 
                    y_tp.append(math.log(j, 10))
                elif len(list_tpmax[i])==1:
                    y_tp.append(math.log(j, 10))
            x_tp = np.zeros(len(y_tp))  
            x_tp = x_tp + list_mags[i]
            c = 0
            if math.isnan(np.median(y_tp))==False:  
                y_aves_tp.append(np.median(y_tp))
                x_aves_tp.append(list_mags[i])
    return x_aves_tp, y_aves_tp

def calc_tc_mag_lim(df, mag_lim):
    #print(mag_lim)
    list_mags, list_tc = sort_tc_data(df, mag_lim)
    params = []
    y_aves_tc = []
    x_aves_tc = []
    i = 0
    for i  in range(0, len(list_mags)):
        if len(list_tc[i])>=1:
            mean_tc = np.mean(list_tc[i]) 
            std_tc = np.std(list_tc[i]) 
            y_tc = [] 
            for j in list_tc[i]: 
                if j > mean_tc-2*std_tc and j < mean_tc + 2*std_tc:# and j < 100: 
                    y_tc.append(math.log(j, 10))
                elif len(list_tc[i])==1:
                    y_tc.append(math.log(j, 10))
            x_tc = np.zeros(len(y_tc))  
            x_tc = x_tc + list_mags[i]
            c = 0
            if math.isnan(np.median(y_tc))==False:  
                y_aves_tc.append(np.median(y_tc))
                x_aves_tc.append(list_mags[i])
    return x_aves_tc, y_aves_tc


def calc_pgd_mag_lim(df, mag_lim):
    list_mag, list_pgd, list_dist = sort_pgd_data(df, mag_lim)
    if len(list_mag)>1 and len(list_dist)>1 and len(list_pgd)>1:
        dist_corr_mult_alt = (np.array(list_dist)**1.38)*np.array(list_pgd)
        df3  = pd.DataFrame({'pgd':np.log10(dist_corr_mult_alt), 'mag':list_mag, 'dist':list_dist})
        y = np.log10(dist_corr_mult_alt)
        x = np.array(list_mag)
        mask = ~np.isnan(x) & ~np.isnan(y)
        return x[mask],y[mask]
    else:
        return [],[]

def calc_iv2_mag_lim(df, mag_lim, r_corr = '2'):
    list_mag, list_iv2, list_dist = sort_iv2_data(df, mag_lim)
    if len(list_mag)>1 and len(list_dist)>1 and len(list_iv2)>1:
        r_corr = float(r_corr)
        dist_corr_mult = (np.array(list_dist)**r_corr)*np.array(list_iv2)
        y = np.log10(dist_corr_mult)
        x = np.array(list_mag) 
        mask = ~np.isnan(x) & ~np.isnan(y)
        return x[mask],y[mask]
    else:
        return [],[]

def calc_opt(x, y, gradt, intercept, gradt_std, intercept_std, pearson, spearman, spearman_p, n_l):
    if len(y)>0:
        x_use = np.array(x) - 5
        y_use = np.array(y)

        x = x_use
        y = y_use
        x_unique = np.arange(min(x_use),max(x_use),0.1)
        df_tp = pd.DataFrame(columns = x_unique)
        
        if len(set(x))>1:
            result = scipy.stats.linregress(x,y)
            a = result.slope
            gradt.append(a)
            b = result.intercept
            intercept.append(b)
            std_a = result.stderr
            gradt_std.append(std_a)
            std_b = result.intercept_stderr
            intercept_std.append(std_b)
            #plt.scatter(x,y)
            #x_plot = np.array([-2,3])
            #plt.plot(x_plot,a*x_plot+b)
            pearson.append(result.rvalue)
            spearman.append(scipy.stats.spearmanr(x,y)[0])
            spearman_p.append(scipy.stats.spearmanr(x,y)[1])
            n_l.append(len(x))   
    return gradt, intercept, gradt_std, intercept_std, pearson, spearman, spearman_p, n_l

def name_to_time(f):
    l = f.split('_')
    time = l[2][:-1]
    if time == '1' or time == '4':
        return time
    else:
        time = time[0]+'.'+time[1]
        return time
    
def plot_spearman_subplots(f, gradt, gradt_std, spearman, spearman_p, n, var = 'tp', save = False):
    matplotlib.rcParams.update({'font.size': 20})
    time = name_to_time(f)
    fig, axs = plt.subplots(5,1, figsize = figure_sizes.a4portrait, sharex = True)
    magn = magnitudes[0:len(spearman)]
    axs[0].plot(magn,gradt, color = colors[var])
    axs[0].set_ylabel('gradient')
    axs[1].plot(magn,gradt_std, color = colors[var])
    axs[1].set_ylabel('gradient std')
    axs[2].plot(magn,spearman, color = colors[var])
    axs[2].set_ylabel('spearman r')
    axs[3].plot(magn,spearman_p, color = colors[var])
    mask = np.array(spearman_p)>0.05
    mag_mask = magn[mask]
    axs[3].plot(mag_mask,np.array(spearman_p)[mask], color = colors[var], linestyle = '', marker = 'o')
    axs[3].set_ylabel('p-value of\n  spearman \n (H0=linearly \n uncorrelated)')
    axs[3].axhspan(0, 0.05, facecolor=colors[var], alpha=0.2)
    axs[4].plot(magn, np.array(n), color = colors[var])
    axs[4].set_ylabel('n')
    axs[0].set_title(f'log$_{10}$({var}) - {time} s window')
    axs[4].set_xlabel('max mag')
    axs[3].set_xlim([3,7])
    axs[0].grid(True); axs[1].grid(True); axs[2].grid(True); axs[3].grid(True); axs[4].grid(True)
    
    if save == True:
        plt.savefig(f'/home/earthquakes1/homes/Rebecca/phd/seismo_det/figures/gradt_spearman/{var}_with_number_window_{time}.pdf', dpi=400)
    plt.show()

def plot_spearman_subplots_all_on_one(f, tp_params, pgd_params, iv2_params, tc_params, save = False):
    params = [tp_params, pgd_params, iv2_params, tc_params]#[gradt, gradt_std, spearman, spearman_p, n, var]
    time = name_to_time(f)
    fig, axs = plt.subplots(5,1, figsize = figure_sizes.a5landscape, sharex = True)
    axs[0].plot([],[],color='k',label = 'significant')
    axs[0].plot([],[],color='k',linestyle = ':', label = 'insignificant')

    for p in params:
        magn = magnitudes[0:len(p[2])]
        mask = np.array(p[3])>0.05
        res = [idx for idx, val in enumerate(p[3]) if val > 0.05]
        if len(res)>0:
            flip = res[0]
            mag_mask = magn[(flip-1):]
            mag_neg_mask = magn[:flip]  
            for i in range(0, 5):
                axs[i].plot(mag_mask,np.array(p[i])[(flip-1):], color = colors[p[5]], linestyle = ':')
                axs[i].plot(mag_neg_mask,np.array(p[i])[:flip], color = colors[p[5]], label = p[-1])
        else:
            for i in range(0, 5):
                axs[i].plot(magn,p[i], color = colors[p[5]])

        axs[3].axhspan(0, 0.05, facecolor='grey', alpha=0.2)
    for ax in axs:
        ax.vlines(window_lengths[str(time)], 0, 1, transform=ax.get_xaxis_transform(), color = 'grey', linewidth=1.5)

    axs[0].set_ylabel('gradient')
    axs[1].set_ylabel('gradient std')
    axs[2].set_ylabel('spearman r')
    axs[3].set_ylabel('p-value of\n  spearman \n (H0=linearly \n uncorrelated)')
    axs[4].set_ylabel('n')
    axs[0].set_title(f'{time} s window')
    axs[4].set_xlabel('max mag')
    axs[3].set_xlim([3,7])
    axs[0].grid(True); axs[1].grid(True); axs[2].grid(True); axs[3].grid(True); axs[4].grid(True)
    axs[0].autoscale(True, 'y'); axs[1].autoscale(True, 'y'); axs[2].autoscale(True, 'y'); axs[3].autoscale(True, 'y'); axs[4].autoscale(True, 'y')
    handles, labels = axs[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', ncol = len(labels))
    figure = plt.gcf()
    figure.set_size_inches(figure_sizes.a5landscape)
    if save == True:
        plt.savefig(f'/home/earthquakes1/homes/Rebecca/phd/seismo_det/figures/gradt_spearman/combined_with_number_window_{time}.pdf', dpi=400)
    plt.show()

def plot_spearman_subplots_all_on_one_no_n(f, tp_params, pgd_params, iv2_params, tc_params, save = False):
    params = [tp_params, pgd_params, iv2_params, tc_params]#[gradt, gradt_std, spearman, spearman_p, n, var]
    time = name_to_time(f)
    fig, axs = plt.subplots(4,1, figsize = figure_sizes.a5landscape, sharex = True)
    axs[0].plot([],[],color='k',label = 'significant')
    axs[0].plot([],[],color='k',linestyle = ':', label = 'insignificant')
    for p in params:
        magn = magnitudes[0:len(p[2])]
        mask = np.array(p[3])>0.05
        res = [idx for idx, val in enumerate(p[3]) if val > 0.05]
        if len(res)>0:
            flip = res[0]
            mag_mask = magn[(flip-1):]
            mag_neg_mask = magn[:flip]  
            for i in range(0, 4):
                axs[i].plot(mag_mask,np.array(p[i])[(flip-1):], color = colors[p[5]], linestyle = ':', linewidth=2)
                axs[i].plot(mag_neg_mask,np.array(p[i])[:flip], color = colors[p[5]], label = p[-1], linewidth=2)
        else:
            for i in range(0, 4):
                axs[i].plot(magn,p[i], color = colors[p[5]], linewidth=2)

        axs[3].axhspan(0, 0.05, facecolor='grey', alpha=0.2)
    for ax in axs:
        ax.vlines(window_lengths[str(time)], 0, 1, transform=ax.get_xaxis_transform(), color = 'grey', linewidth=1.5)

    axs[0].set_ylabel('gradient')
    axs[1].set_ylabel('gradient std')
    axs[2].set_ylabel('spearman r')
    axs[3].set_ylabel('p-value of\n  spearman \n (H0=linearly \n uncorrelated)')
    #axs[4].set_ylabel('n')
    axs[0].set_title(f'{time} s window')
    axs[3].set_xlabel('max mag')
    axs[3].set_xlim([3,7])
    axs[0].grid(True); axs[1].grid(True); axs[2].grid(True); axs[3].grid(True)
    axs[0].autoscale(True, 'y'); axs[1].autoscale(True, 'y'); axs[2].autoscale(True, 'y'); axs[3].autoscale(True, 'y')
    handles, labels = axs[0].get_legend_handles_labels()
    figure = plt.gcf()
    figure.set_size_inches(figure_sizes.a4portrait)
    fig.legend(handles, labels, loc='lower center', ncol = len(labels), bbox_to_anchor = (0.03, -0.03,1,1),bbox_transform = figure.transFigure)
    figure.tight_layout()
    if save == True:
        plt.savefig(f'/home/earthquakes1/homes/Rebecca/phd/seismo_det/figures/gradt_spearman/combined_no_number_window_{time}.pdf', dpi=400, bbox_inches='tight')
    plt.show()
    
def plot_spearman_subplots_all_on_one_no_n_shaded(f, tp_params, pgd_params, iv2_params, tc_params, save = False):
    params = [tp_params, pgd_params, iv2_params, tc_params]#[gradt, gradt_std, spearman, spearman_p, n, var]
    time = name_to_time(f)
    fig, axs = plt.subplots(3,1, figsize = figure_sizes.a4square, sharex = True, height_ratios = [2,1,1])
    axs[0].plot([],[],color='k',label = 'significant')
    axs[0].plot([],[],color='k',linestyle = ':', label = 'insignificant')
    #axs[0].fill_between([],[], [],color='k',alpha = 0.3, label = '1 s.d.')
    for p in params:
        magn = magnitudes[0:len(p[2])]
        mask = np.array(p[3])>0.05
        res = [idx for idx, val in enumerate(p[3]) if val > 0.05]
        if len(res)>0:
            flip = res[0]
            mag_mask = magn[(flip-1):]
            mag_neg_mask = magn[:flip]  
            for i in range(0, 4):
                if i == 0:
                    print('i=0')
                    axs[i].plot(mag_mask,np.array(p[i])[(flip-1):], color = colors[p[5]], linestyle = ':', linewidth=2)
                    axs[i].plot(mag_neg_mask,np.array(p[i])[:flip], color = colors[p[5]], label = p[-1], linewidth=2)
                elif i == 1:
                    print('i=1')
                    axs[0].fill_between(magn,np.array(p[1])+np.array(p[0]),np.array(p[0])-np.array(p[1]), color = colors[p[5]], alpha = 0.3)
                    #axs[1].plot(mag_neg_mask,np.array(p[i])[:flip], color = colors[p[5]], label = p[-1], linewidth=2)
                else:
                    print('in else')
                    axs[i-1].plot(mag_mask,np.array(p[i])[(flip-1):], color = colors[p[5]], linestyle = ':', linewidth=2)
                    axs[i-1].plot(mag_neg_mask,np.array(p[i])[:flip], color = colors[p[5]], label = p[-1], linewidth=2)
        else:
            for i in [0,2,3]:
                if i == 0:
                    axs[i].plot(magn,p[i], color = colors[p[5]], linewidth=2)
                elif i == 1:
                    axs[0].fill_between(magn,np.array(p[1])+np.array(p[0]),np.array(p[0])-np.array(p[1]), color = colors[p[5]], alpha = 0.3)
                    #axs[1].plot(mag_neg_mask,np.array(p[i])[:flip], color = colors[p[5]], label = p[-1], linewidth=2)
                else:
                    axs[i-1].plot(magn,p[i], color = colors[p[5]], linewidth=2)
                

        axs[2].axhspan(0, 0.05, facecolor='grey', alpha=0.05)
    for ax in axs:
        ax.vlines(window_lengths[str(time)], 0, 1, transform=ax.get_xaxis_transform(), color = 'grey', linewidth=1.5)
        ax.tick_params(axis='both', which='major', labelsize=14)
        #ax.tick_params(axis='both', which='minor', labelsize=8)
    axs[0].set_ylabel('Gradient', fontsize = 14)
    axs[1].set_ylabel('Spearman r', fontsize = 14)
    axs[2].set_ylabel('p-value of\n  spearman r', fontsize = 14)
    #axs[4].set_ylabel('n')
    axs[0].set_title(f'{time} s Window', fontsize = 14)
    axs[2].set_xlabel('Min mag', fontsize = 14)
    axs[2].set_xlim([3,7])
    axs[0].grid(True); axs[1].grid(True); axs[2].grid(True)
    axs[0].autoscale(True, 'y'); axs[1].autoscale(True, 'y'); axs[2].autoscale(True, 'y')
    matplotlib.rcParams.update({'font.size': 14})
    import matplotlib.transforms as mtransforms
    trans = mtransforms.ScaledTranslation(-20/72, 7/72, fig.dpi_scale_trans)
    axs[0].text(0.0, 1.0, 'a)', transform=axs[0].transAxes + trans,
                fontsize='14', va='bottom')
    axs[1].text(0.0, 1.0, 'b)', transform=axs[1].transAxes + trans,
                fontsize='14', va='bottom')
    axs[2].text(0.0, 1.0, 'c)', transform=axs[2].transAxes + trans,
                fontsize='14', va='bottom')

    handles, labels = axs[0].get_legend_handles_labels()
    figure = plt.gcf()
    figure.set_size_inches(figure_sizes.a4square)
    fig.legend(handles, labels, loc='lower center', ncol = 3, bbox_to_anchor = (0.03, -0.1,1,1),bbox_transform = figure.transFigure)
    figure.tight_layout()
    if save == True:
        plt.savefig(f'/home/earthquakes1/homes/Rebecca/phd/seismo_det/figures/gradt_spearman/shaded_combined_no_number_window_{time}.pdf', dpi=400, bbox_inches='tight')
    plt.show()