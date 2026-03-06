import numpy as np

def embed(ts, dim, delay):
    N = len(ts) - (dim - 1) * delay
    return np.array([ts[i:i + dim * delay:delay] for i in range(N)])