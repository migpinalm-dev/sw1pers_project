from scipy.ndimage import gaussian_filter1d

def density(scores, rolling_size_scores):
    sigma = rolling_size_scores/8  # adjust for desired smoothness
    return gaussian_filter1d(scores, sigma=sigma)