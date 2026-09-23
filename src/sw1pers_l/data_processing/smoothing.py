from scipy.ndimage import gaussian_filter1d
import numpy as np

def sma(ts, rolling_size):
    weights = np.ones(rolling_size) / rolling_size
    ma = np.convolve(ts, weights, mode='valid')
    t_ma = np.arange(len(ma))     # adjusted time after convolution
    return t_ma, ma

def gaussian_density(ts, rolling_size, denominator=8):
    sigma = rolling_size/denominator  # adjust for desired smoothness
    return gaussian_filter1d(ts, sigma=sigma)