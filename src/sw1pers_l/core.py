# import numpy as np
from .time_series import embed
from .windows import make_embedded_windows, make_embedded_ts
from .data_processing import sma, gaussian_density, make_spline
# from .visualize import attractor
from .diagrams import make_pers_diagrams, make_pers_diagram
from .sw1pers_scores import compute_scores, plot_score_landscape

def SW1PerS(values, rolling_size=1, factor=1):
    t_ma, ma = sma(values, rolling_size)

    _, finer_spline = make_spline(t_ma, ma, factor*len(values))

    emb_spline, _, _ = make_embedded_ts(finer_spline)

    pers_dgm = make_pers_diagram(emb_spline)

    score = compute_scores([pers_dgm])

    return score

#---------------------------------------------------------------------

def SW1PerS_L(values, dates=None, rolling_size=1, factor=1, size=1, slide=1, min_dim=2, plot_bool = False):

    t_ma, ma = sma(values, rolling_size)

    size = size*factor
    slide = slide*factor

    _, finer_spline = make_spline(t_ma, ma, factor*len(values))

    emb_windows, _, _ = make_embedded_windows(finer_spline, size, slide, min_dim)

    #-----------------------------------

    pers_dgms = make_pers_diagrams(emb_windows)

    scores = compute_scores(pers_dgms)

    #-----------------------------------

    rolling_size_scores = int(size/slide)    # Resolution
                          
    score_density = gaussian_density(scores, rolling_size_scores)

    if plot_bool:
        plot_score_landscape(scores, score_density, finer_spline, size, slide, dates, rolling_size_scores)

    return scores