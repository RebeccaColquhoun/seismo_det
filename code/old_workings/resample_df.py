import numpy as np
import pandas as pd
import random

def pick_event_of_mag(df, mag):
    mag_events = df.loc[round(df['eq_mag'],1) == mag]
    #print(len(mag_events))
    rand_n = random.randint(0, len(mag_events)-1)
    #print(rand_n)
    mag_events = mag_events.reset_index(drop=True)
    return mag_events.loc[rand_n].to_frame()
     
def n_gr(m):
    return 10**(3-1*m)

def generate_mag_dist(N_eq):
    mag_dist = []
    for m in (np.arange(3,8,0.1)):
        n = (n_gr(m)-n_gr(m+0.1))*N_eq
        for _ in range(int(n)):
            mag_dist.append(round(m,1))
    return mag_dist

def make_subset_df(df, N_eq=None):
    if N_eq == None:
        N_eq = len(df)
    mag_dist = generate_mag_dist(N_eq)
    
    event = pick_event_of_mag(df, mag_dist[0])
    df1 = event#.to_frame()
    #print(df1)
    for mag in mag_dist[1:]:
        event = pick_event_of_mag(df, mag)
        df2 = event#.to_frame()
        df1 = pd.merge(df1, df2, left_index=True, right_index=True)
    df1 = df1.transpose()
    df1 = df1.reset_index(drop=True)
    return df1
    