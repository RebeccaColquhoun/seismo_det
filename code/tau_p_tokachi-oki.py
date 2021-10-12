import obspy
import numpy as np
import matplotlib.pyplot as plt


def output_to_acc(e):
    q = 0.998
    g = 2.384185791015625e-06
    a = np.zeros(len(e))
    for j in range(1, len(e)):
        a[j] = (((1+q)/2)*((e[j]-e[j-1])/g))+(q*a[j-1])
    return a


def acc_to_vel(a):
    q = 0.998
    dt = 0.01
    v = np.zeros(len(a))
    for j in range(1, len(a)):
        v[j] = ((1+q)/2)*((a[j]+a[j-1])/2)*dt + q*v[j-1]
    return v


data_files = ["HKD1000309260450", "HKD1110309260450", "HKD1120309260450", "HKD1130309260450"]
picks = [1285, 1224, 1350, 1326]
freq_mins = [0.1, 0.1, 0.078, 0.1]
# 1198 or 1224
tp_max = []
count = 0

# print(i)
# print(data_files[i])
# print(picks[i])

filter_types = []
for i_freq in [0.1, 0.075]:  # np.arange(0.001, 0.2, 0.001):
    for corners in [1,2,3,4,5]:
        tp_max.append([])
        for i in range(0, len(data_files)):
            # print(i_freq)
            # i_freq = freq_mins[i]  # 0.078
            acc = obspy.read("/Users/rebecca/Documents/PhD/Research/Frequency/Tokachi-Oki/data/"+data_files[i]+"/"+data_files[i]+".UD", apply_calib=True)
    
            tr_acc = acc[0].copy()
    
            tr_int = tr_acc.copy()
            tr_acc.detrend()
            tr_acc.filter('highpass', freq=i_freq, corners=corners)  # 0.078)#i_freq)
            tr_int = tr_acc.copy()
            tr_int = tr_int.integrate()
    
            v = acc_to_vel(tr_acc.data)
            tr_v = tr_acc.copy()
            tr_v.data = v
            tr_v.detrend()
            tr_v.filter('lowpass', freq=3)
    
            tau_p_list = []
            # tp_max = []
            tr = tr_int.copy()
            #tr.filter('highpass', freq=0.1, corners=3)  # 0.078)#i_freq)
            tr.filter('lowpass', freq=3)
            sampling_rate = tr.stats.sampling_rate
            if sampling_rate == 100:
                alpha = 0.99
            elif sampling_rate == 20:
                alpha = 0.95
            x = tr.data
            diff = (tr.differentiate()).data
            X = np.zeros(len(x))
            D = np.zeros(len(x))
            start = picks[i]  # int((picks[i] - tr.stats.starttime)*sampling_rate)
            end = picks[i]+400  # int(start + 4 * sampling_rate)
            for t in range(0, len(tr.data)):  # picks[i]
                X[t] = alpha*X[t-1]+x[t]**2
                D[t] = alpha*D[t-1]+diff[t]**2
            tau_p = 2 * np.pi * np.sqrt(X/D)
            tau_p_list.append(tau_p)
            print(max(tau_p[int(start+0.05*sampling_rate):int(end)]))
            tp_max[count].append(max(tau_p[int(start+0.05*sampling_rate):int(end)]))
            # +0.5*sampling_rate
            # plt.plot(np.arange(0.01, 0.2, 0.01), tp_max)
            #  += 1
            '''fig, axs = plt.subplots(3, 1, sharex=True)
            axs[0].plot(tr_acc.data)
            axs[0].vlines(1350, min(tr_acc.data), max(tr_acc.data), color='black')
            axs[1].plot(tr_v.data)
            axs[1].vlines(1350, min(tr_v.data), max(tr_v.data), color='black')
            #axs[2].plot(tr_int.data)
            axs[2].plot(tau_p)
            axs[2].vlines(1350, 0, 10, color='black')
            #axs[2].ylim
            #axs[2].axvspan(1340, 1740, alpha=0.5, color='red')
            plt.xlim([1000, 2000])
            plt.show()'''
        count += 1


y = [[],[],[],[]]
for i in tp_max:
    y[0].append(i[0])
    y[1].append(i[1])
    y[2].append(i[2])
    y[3].append(i[3])
plt.plot(np.arange(0.001, 0.2, 0.001), y[0])
plt.plot(np.arange(0.001, 0.2, 0.001), y[1])
plt.plot(np.arange(0.001, 0.2, 0.001), y[2])
plt.plot(np.arange(0.001, 0.2, 0.001), y[3])

plt.ylabel("max predominant period")
plt.xlabel("highpass filter (Hz)")
#plt.title("corners = 2")
#plt.vlines(0.1, 0, max(tp_max[0]), color='black')
plt.show()

tp_max_0 = np.array(tp_max[0])
tp_max_1 = np.array(tp_max[1])
tp_max_2 = np.array(tp_max[2])
tp_max_3 = np.array(tp_max[3])

plt.plot(np.arange(0.075, 0.2, 0.0001), (tp_max_0+tp_max_1+tp_max_2+tp_max_3)/4)
plt.ylabel("average max predominant period")
plt.xlabel("highpass filter (Hz)")
plt.title("corners = 2")
plt.vlines(0.1, 0, 2.75, color='black')
plt.show()

