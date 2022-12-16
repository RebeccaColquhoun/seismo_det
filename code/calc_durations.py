
def calc_line_fig1(V, stressdrop, w_max, list_of_moments):
    logT = []
    for moment in list_moments:
        if moment < c*stressdrop*w_max**3:
            logT.append(1/3*np.log10(moment)-1/3*np.log10(c*stressdrop*V**3))
        else:
            logT.append(np.log10(moment)-np.log10(c*stressdrop*(w_max**2)*V))
    return np.array(logT)

def calc_durations(list_moments = None, list_mags = None):
    if list_moments == None and list_mags == None:
        #raise error
    elif list_moments == None:
        list_moments = 10**((list_mags/(2/3))+9.1)

    min_stressdrop = 0.1*mpa #mpa
    max_stressdrop = 100*mpa #mpa
    min_V = 1000 #ms-1
    max_V = 4000 #ms-1
    min_Wmax = 10*km # km
    max_Wmax = 200*km  #km

    min_logT = np.minimum(calc_line_fig1(min_V, min_stressdrop, min_Wmax, list_moments), calc_line_fig1(min_V, min_stressdrop, max_Wmax, list_moments))
    min_logT = np.minimum(min_logT, calc_line_fig1(max_V, min_stressdrop, min_Wmax, list_moments))
    min_logT = np.minimum(min_logT, calc_line_fig1(max_V, min_stressdrop, max_Wmax, list_moments))
    min_logT = np.minimum(min_logT, calc_line_fig1(min_V, max_stressdrop, min_Wmax, list_moments))
    min_logT = np.minimum(min_logT, calc_line_fig1(min_V, max_stressdrop, max_Wmax, list_moments))
    min_logT = np.minimum(min_logT, calc_line_fig1(max_V, max_stressdrop, min_Wmax, list_moments))
    min_logT = np.minimum(min_logT, calc_line_fig1(max_V, max_stressdrop, max_Wmax, list_moments))

    max_logT = np.maximum(calc_line_fig1(min_V, min_stressdrop, min_Wmax, list_moments), calc_line_fig1(min_V, min_stressdrop, max_Wmax, list_moments))
    max_logT = np.maximum(max_logT, calc_line_fig1(max_V, min_stressdrop, min_Wmax, list_moments))
    max_logT = np.maximum(max_logT, calc_line_fig1(max_V, min_stressdrop, max_Wmax, list_moments))
    max_logT = np.maximum(max_logT, calc_line_fig1(min_V, max_stressdrop, min_Wmax, list_moments))
    max_logT = np.maximum(max_logT, calc_line_fig1(min_V, max_stressdrop, max_Wmax, list_moments))
    max_logT = np.maximum(max_logT, calc_line_fig1(max_V, max_stressdrop, min_Wmax, list_moments))
    max_logT = np.maximum(max_logT, calc_line_fig1(max_V, max_stressdrop, max_Wmax, list_moments))

    return min_logT, max_logT