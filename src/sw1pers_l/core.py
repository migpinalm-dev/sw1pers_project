# import numpy as np
from .time_series import embed
from .windows import make_embedded_windows, make_embedded_ts
from .data_processing import moving_avg, make_spline
# from .visualize import attractor
from .diagrams import make_pers_diagrams, make_pers_diagram
from .sw1pers_scores import compute_scores, density, plot_score_landscape

def SW1PerS(values, rolling_size=1, factor=1):
    t_ma, ma = moving_avg(values, rolling_size)

    _, finer_spline = make_spline(t_ma, ma, factor*len(values))

    emb_spline, _, _ = make_embedded_ts(finer_spline)

    pers_dgm = make_pers_diagram(emb_spline)

    score = compute_scores([pers_dgm])

    return score

#---------------------------------------------------------------------

def SW1PerS_L(values, rolling_size=1, factor=1, size=1, stride=1, min_dim=3, choose_hyper_param=False, plot_bool = False):

    t_ma, ma = moving_avg(values, rolling_size)

    _, finer_spline = make_spline(t_ma, ma, factor*len(values))

    #-----------------------------------
    if choose_hyper_param:
        size = int(input("Please choose a window size: "))
        stride = int(input("Please choose a window stride: "))
        print()
        print(f"window_size = {size}")
        print(f"window_stride = {stride}")
        print()
    else:
        print()
        print(f"window_size = {size}")
        print(f"window_stride = {stride}")
        print()

    emb_windows, _, _ = make_embedded_windows(finer_spline, size, stride, min_dim)

    #-----------------------------------

    pers_dgms = make_pers_diagrams(emb_windows)

    scores = compute_scores(pers_dgms)

    #-----------------------------------

    rolling_size_scores = int(size/stride)
                          
    score_density = density(scores, rolling_size_scores)

    if plot_bool:
        plot_score_landscape(scores, score_density, finer_spline, size, stride, None, rolling_size_scores)

    return scores