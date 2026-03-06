from scipy.spatial.distance import cdist
import numpy as np

def false_nearest_neighbors(ts, max_dim, delay, R_thresh=10, A_thresh=2, plot=False):
    if ts.shape == (ts.shape[0], 1):
        ts = ts.squeeze(1)
    # N = len(ts) - max_dim * delay
    fnn_percentages = []
    eps = 1e-10  # small value to avoid divide-by-zero

    d = 1
    N = len(ts) - (d) * delay
    while d < max_dim+1 and N > len(ts)/3:    # ensure N is larger than one third the window size
        embedded = np.array([ts[i:i + d * delay:delay] for i in range(N)])
        dists = cdist(embedded, embedded)
        np.fill_diagonal(dists, np.inf)
        nearest_idx = np.argmin(dists, axis=1)
        next_vals = ts[delay * d:N + delay * d]
        next_vals_nn = ts[nearest_idx + delay * d]
        dist_increase = np.abs(next_vals - next_vals_nn)
        R = np.std(ts)
        denom = dists[np.arange(N), nearest_idx] + eps
        false_neighbors = ((dist_increase / denom) > R_thresh) | ((dist_increase / R) > A_thresh)
        fnn_percentages.append(np.mean(false_neighbors) * 100)
        d += 1
        N = len(ts) - d * delay

    # if plot:
    #     plt.plot(range(1, d+1), fnn_percentages)
    #     plt.xlabel("Embedding Dimension")
    #     plt.ylabel("False Nearest Neighbors (%)")
    #     plt.title("FNN vs Embedding Dimension")
    #     plt.show()

    return fnn_percentages

def compute_optimal_dim(fnn, msg_bool = True):
    optimal_dim = 0
    threshhold = 3    # 5% by default
    while optimal_dim==0:
        for i, value in enumerate(fnn):
            if value < threshhold:
                optimal_dim = i + 1
                if msg_bool:
                    print(f"Found optimal dimension: {optimal_dim}\n")
                break
        threshhold += 1    # increase threshhold by 1% if no fnn value satisfies condition
    return optimal_dim