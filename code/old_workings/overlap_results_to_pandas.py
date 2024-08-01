import os
import pandas as pd

normal_all = os.listdir('/Users/rebecca/Documents/PhD/Research/Frequency/seismo_det/figures/overlaps/hypocentral')
reversed_all = os.listdir('/Users/rebecca/Documents/PhD/Research/Frequency/seismo_det/figures/overlaps_reversed/hypocentral')
normal = []
for fn in normal_all:
    if fn[:2]=='eq':
        normal.append(fn)
normal.sort()

reverse = []
for fn in reversed_all:
    if fn[:2]=='eq':
        reverse.append(fn)
reverse.sort()

df = pd.DataFrame(columns = ['window', 'blank', 'nstations', 'mindist','tp_1sd', 'tp_2sd', 'tc_1sd', 'tc_2sd', 'iv2_1sd', 'iv2_2sd', 'pgd_1sd', 'pgd_2sd'])

for fn in normal:
    #eq_object_03s_bandpass_01_19_snr_20_blank_005_new_snr20_nstations_0_mindist_70_overlap_
    if 'always' in fn: #fn[-19] not in ['0','1']:
        cut = fn.rindex('always')
        fn = fn[:cut+3]
    name = fn[:-19]
    window = fn[fn.rindex('eq_object')+10:fn.rindex('bandpass')-2]
    if window in ['03','05']:
        window = window[0] + '.' + window[1]
    window = float(window)
    blank = fn[fn.rindex('blank')+6:fn.rindex('new')-1]
    blank = blank[0] + '.' + blank[1:]
    blank = float(blank)
    nstations = int(fn[fn.rindex('nstations')+10:fn.rindex('mindist')-1])
    mindist  = int(fn[fn.rindex('mindist')+8:fn.rindex('overlap')-1])
    print(window, blank, nstations, mindist)
    print(fn)
    print(fn[-19], fn[-17], fn[-15], fn[-13], fn[-11], fn[-9], fn[-7], fn[-5])
    df.loc[name] = [window, blank, nstations, mindist, bool(int(fn[-19])), bool(int(fn[-17])), bool(int(fn[-15])), bool(int(fn[-13])), bool(int(fn[-11])), bool(int(fn[-9])), bool(int(fn[-7])), bool(int(fn[-5]))]
#print(df)
#print(df.sum())

df_r = pd.DataFrame(columns = ['window', 'blank', 'nstations', 'mindist','tp_1sd_r', 'tp_2sd_r', 'tc_1sd_r', 'tc_2sd_r', 'iv2_1sd_r', 'iv2_2sd_r', 'pgd_1sd_r', 'pgd_2sd_r'])

for fn in reverse:
    #eq_object_03s_bandpass_01_19_snr_20_blank_005_new_snr20_nstations_0_mindist_70_overlap_
    if 'always' in fn: #fn[-19] not in ['0','1']:
        cut = fn.rindex('always')
        fn = fn[:cut+3]
    name = fn[:-19]
    window = fn[fn.rindex('eq_object')+10:fn.rindex('bandpass')-2]
    if window in ['03','05']:
        window = window[0] + '.' + window[1]
    window = float(window)
    blank = fn[fn.rindex('blank')+6:fn.rindex('new')-1]
    blank = blank[0] + '.' + blank[1:]
    blank = float(blank)
    nstations = int(fn[fn.rindex('nstations')+10:fn.rindex('mindist')-1])
    mindist  = int(fn[fn.rindex('mindist')+8:fn.rindex('overlap')-1])
    print(window, blank, nstations, mindist)
    print(fn)
    print(fn[-19], fn[-17], fn[-15], fn[-13], fn[-11], fn[-9], fn[-7], fn[-5])
    df_r.loc[name] = [window, blank, nstations, mindist, bool(int(fn[-19])), bool(int(fn[-17])), bool(int(fn[-15])), bool(int(fn[-13])), bool(int(fn[-11])), bool(int(fn[-9])), bool(int(fn[-7])), bool(int(fn[-5]))]

#print(df[df["tp_1sd"] | df["tp_2sd"] | df["tc_1sd"] | df["tc_2sd"] | df["iv2_1sd"] | df["iv2_2sd"] | df["pgd_1sd"] | df["pgd_2sd"]])


df_all = pd.merge(df, df_r)
df_all.to_excel('/Users/rebecca/Documents/PhD/Research/Frequency/seismo_det/figures/overlaps_all.xlsx')
print(df_all)
print(df_all.columns)