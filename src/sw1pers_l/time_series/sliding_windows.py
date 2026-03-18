import numpy as np

def make_sliding_windows(ts, size, stride):
    return np.array([ts[i:i+size] for i in range(0, len(ts) - size + 1, stride)])