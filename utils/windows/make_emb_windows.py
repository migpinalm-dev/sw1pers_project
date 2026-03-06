from tqdm import tqdm
import numpy as np

from utils import parameter_selection
from utils import time_series

from .point_cloud_tools import mean_center, normalize, meanshift_pointcloud


def make_embedded_windows(X, window_size, window_stride):

    X = X.reshape(len(X), )

    windows = time_series.make_sliding_windows(X, window_size, window_stride)

    emb_windows=[]
    dim, delay = 1, 1
    input_dimensions = []
    input_delays = []

    print("Finding best parameters...\n")
    for i, window in enumerate(tqdm(windows)):
        ami = parameter_selection.average_mutual_information(window, bins=int(np.sqrt(len(window)))+1)
        delay = parameter_selection.compute_optimal_delay(ami, msg_bool=False)
        fnn = parameter_selection.false_nearest_neighbors(window, max_dim=10, delay=delay)
        dim = parameter_selection.compute_optimal_dim(fnn, msg_bool=False)

    print()
    print("Forming point clouds...\n")
    for i, window in enumerate(tqdm(windows)):
        input_dim = dim + 1  #max(dim, 3)      # make this (dim + 1) to not squish some cycles trivial
        input_dimensions.append(input_dim)
        input_delays.append(delay)
        emb_window = time_series.embed(window, input_dim, delay)

        emb_window = mean_center(emb_window)
        emb_window = normalize(emb_window)

        emb_window = meanshift_pointcloud(emb_window, np.pi/16)    # pi/16 is radius used in Perea's paper
        emb_window = normalize(emb_window)    # normalize again because meanshift changes this

        emb_windows.append(emb_window)

    return emb_windows, input_dimensions, input_delays