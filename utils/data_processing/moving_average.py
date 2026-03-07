import numpy as np

def moving_avg(ts, rolling_size=1):
    ma = np.convolve(ts, np.ones(rolling_size)/rolling_size, mode='valid')
    t_ma = np.arange(len(ma))  # adjusted time after convolution
    return t_ma, ma
