import obspy
import numpy as np
import matplotlib.pyplot as plt


def output_to_acc(e, q = 0.99, g = 2.384185791015625e-06):
    a = np.zeros(len(e))
    for j in range(1, len(e)):
        a[j] = (((1+q)/2)*((e[j]-e[j-1])/g))+(q*a[j-1])
    return a


def acc_to_vel(a, q = 0.99):
    dt = 0.01
    v = np.zeros(len(a))
    for j in range(1, len(a)):
        v[j] = ((1+q)/2)*((a[j]+a[j-1])/2)*dt + q*v[j-1]
    return v


data_files = ["HKD1000309260450", "HKD1110309260450", "HKD1120309260450", "HKD1130309260450"]
picks = [1285, 1224, 1340, 1326]
freq_mins = [0.1, 0.1, 0.078, 0.1]
# 1198 or 1224
tp_max = []
count = 0
# for i_freq in np.arange(0.075, 0.2, 0.0001):
#     print(i)
#     print(data_files[i])
#     print(picks[i])
#     tp_max.append([])
#     for i in range(0, len(data_files)):
#         print(i_freq)
#         i_freq = freq_mins[i]  # 0.078


def run_tp(i, q=0.99, start_at_pick=True, plot=False):
    ep = obspy.read("/Users/rebecca/Documents/PhD/Research/Frequency/Tokachi-Oki/data/"+data_files[i]+"/"+data_files[i]+".UD", apply_calib=False)

    tr_acc = ep[0].copy()
    tr_acc.data = output_to_acc(ep[0].data, q)
    # tr_int = tr_acc.copy()
    tr_acc.detrend()
    # tr_acc.filter('highpass', freq=0.078)#i_freq)
    tr_int = tr_acc.copy()
    tr_int = tr_int.integrate()

    v = acc_to_vel(tr_acc.data, q)
    tr_v = tr_acc.copy()
    tr_v.data = v
    tr_v.detrend()
    tr_v.filter('lowpass', freq=3)

    tau_p_list = []
    # tp_max = []
    tr = tr_v.copy()
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
    if start_at_pick:
        start_calc = picks[i]
    else:
        start_calc = 0
    for t in range(start_calc, len(tr.data)):  # picks[i]
        X[t] = alpha*X[t-1]+x[t]**2
        D[t] = alpha*D[t-1]+diff[t]**2
    tau_p = 2 * np.pi * np.sqrt(X/D)
    tau_p_list.append(tau_p)
    print(max(tau_p[int(start+0.1*sampling_rate):int(end)]))
    tp_max.append(max(tau_p[int(start+0.1*sampling_rate):int(end)]))
    # +0.5*sampling_rate
    # plt.plot(np.arange(0.01, 0.2, 0.01), tp_max)
    #  += 1
    if plot:
        fig, axs = plt.subplots(4, 1, sharex=True)
        axs[0].plot(tr_acc.data)
        axs[1].plot(tr_v.data)
        axs[2].plot(tr_int.data)
        axs[3].plot(tau_p)
        axs[3].axvspan(1340, 1740, alpha=0.5, color='red')
        plt.xlim([1000, 2000])
        plt.show()
    return max(tau_p[int(start+0.1*sampling_rate):int(end)])


tp_true = []
tp_false = []
i = 2
for q in np.arange(0.97, 1, 0.001):
    tp_true.append(run_tp(i, q, True))
    tp_false.append(run_tp(i, q, False))
