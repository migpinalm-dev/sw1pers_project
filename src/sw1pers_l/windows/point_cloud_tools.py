import numpy as np

def mean_center(X):
    return X - np.mean(X, axis = 0)

def normalize(X):
    return X/np.linalg.norm(X, axis = 1, keepdims=True)

# def mean_center_normalize(X):
#     return normalize(mean_center(X))


from sklearn.metrics.pairwise import pairwise_distances

def meanshift_pointcloud(SW_cloud, epsilon, metric='cosine'):

    D = pairwise_distances(SW_cloud, metric=metric)
    n_points, dim = SW_cloud.shape

    threshhold = 1 - np.cos(epsilon)

    cloud_denoised = np.zeros_like(SW_cloud)

    for k in range(n_points):
        mask = D[k] <= threshhold
        cloud_denoised[k] = SW_cloud[mask].mean(axis=0)

    return cloud_denoised