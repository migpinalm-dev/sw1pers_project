from tqdm import tqdm
import numpy as np

from sw1pers_l import parameter_selection
from sw1pers_l import time_series

from .point_cloud_tools import mean_center, normalize, meanshift_pointcloud

def make_embedded_ts(X):

    X = X.reshape(len(X), )

    ami = parameter_selection.average_mutual_information(X, bins=int(np.sqrt(len(X)))+1)
    delay = parameter_selection.compute_optimal_delay(ami, msg_bool=False)
    fnn = parameter_selection.false_nearest_neighbors(X, max_dim=10, delay=delay)
    dim = parameter_selection.compute_optimal_dim(fnn, msg_bool=False)

    emb_cloud = time_series.embed(X, dim, delay)

    emb_cloud = mean_center(emb_cloud)
    emb_cloud = normalize(emb_cloud)

    emb_cloud = meanshift_pointcloud(emb_cloud, np.pi/16)    # pi/16 is radius used in Perea's paper
    emb_cloud = normalize(emb_cloud)

    return emb_cloud, dim, delay