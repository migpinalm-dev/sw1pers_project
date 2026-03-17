from core import SW1PerS

import numpy as np
import matplotlib.pyplot as plt

#------------------------------------------------

x = np.arange(0, 10*2*np.pi, 0.2)
test_ts = np.cos(x)

#------------------------------------------------

# t_ma, ma = data_processing.moving_avg(test_ts)
# plt.plot(t_ma, ma)

# t_fine, finer_spline = data_processing.make_spline(t_ma, ma, 2500)
# plt.plot(t_fine, finer_spline)

# #------------------------------------------------

# test_emb_ts = ts.embed(test_ts, 3, 10)

# # visualize.attractor(test_emb_ts)

# #------------------------------------------------
# size = 10
# stride = 4

# test_emb_windows, dims, delays = w.make_embedded_windows(test_ts, size, stride)

# pers_dgms = diagrams.make_pers_diagrams(test_emb_windows)

# scores = sw1pers_scores.compute_scores(pers_dgms)

# print(scores)

# #-----------------------------------------------
# rolling_size_scores = int(size/stride)
                          
# score_density = sw1pers_scores.density(scores, rolling_size_scores)

# sw1pers_scores.plot_scores(scores, score_density, test_ts, size, stride, None, rolling_size_scores)


scores = SW1PerS(test_ts)