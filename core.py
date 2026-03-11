import numpy as np
from utils import time_series as ts
from utils import windows as w
from utils import data_processing
from utils import visualize
from utils import diagrams
from utils import sw1pers_scores

def SW1PerS(values):
    # values = np.array([p.value for p in series])
    # timestamps = np.array([p.time_stamp for p in series])

    t_ma, ma = data_processing.moving_avg(values)

    t_fine, finer_spline = data_processing.make_spline(t_ma, ma, 2*len(values))

    #-----------------------------------

    size = len(finer_spline)//8
    stride = size//4

    emb_windows, dims, delays = w.make_embedded_windows(finer_spline, size, stride)

    #----------------------------------

    pers_dgms = diagrams.make_pers_diagrams(emb_windows)

    scores = sw1pers_scores.compute_scores(pers_dgms)

    rolling_size_scores = int(size/stride)
                          
    score_density = sw1pers_scores.density(scores, rolling_size_scores)

    sw1pers_scores.plot_scores(scores, score_density, finer_spline, size, stride, None, rolling_size_scores)

    return scores