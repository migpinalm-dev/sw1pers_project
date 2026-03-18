import numpy as np
from .time_series import embed
from .windows import make_embedded_windows
from .data_processing import moving_avg, make_spline
from .visualize import attractor
from .diagrams import make_pers_diagrams
from .sw1pers_scores import compute_scores, density, plot_scores

def SW1PerS(values):
    # values = np.array([p.value for p in series])
    # timestamps = np.array([p.time_stamp for p in series])

    t_ma, ma = moving_avg(values)

    t_fine, finer_spline = make_spline(t_ma, ma, 2*len(values))

    #-----------------------------------

    size = len(finer_spline)//8
    stride = size//4

    emb_windows, dims, delays = make_embedded_windows(finer_spline, size, stride)

    #----------------------------------

    pers_dgms = make_pers_diagrams(emb_windows)

    scores = compute_scores(pers_dgms)

    rolling_size_scores = int(size/stride)
                          
    score_density = density(scores, rolling_size_scores)

    plot_scores(scores, score_density, finer_spline, size, stride, None, rolling_size_scores)

    return scores