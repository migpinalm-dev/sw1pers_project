from sklearn.metrics import mutual_info_score
import numpy as np

def average_mutual_information(ts, max_lag=100, bins=64, plot=False):
    max_lag = len(ts)//2
    if ts.shape == (ts.shape[0], 1):
        ts = ts.squeeze(1)

    if np.max(ts) == np.min(ts):
        return np.zeros(max_lag)

    ts = (ts - np.min(ts)) / (np.max(ts) - np.min(ts))  # normalize
    ami = []
    for lag in range(1, max_lag + 1):
        x = ts[:-lag]
        y = ts[lag:]
        # histogram binning
        c_xy = np.histogram2d(x, y, bins)[0]
        c_xy = c_xy[c_xy.sum(axis=1) > 0][:, c_xy.sum(axis=0) > 0]

        if c_xy.size == 0:
            ami.append(0.0)
        else:
            ami.append(mutual_info_score(None, None, contingency=c_xy))
    # if plot:
    #     plt.plot(range(1, max_lag+1), ami)
    #     plt.xlabel("Lag")
    #     plt.ylabel("AMI")
    #     plt.title("Average Mutual Information")
    #     plt.show()
    return ami

def compute_optimal_delay(ami, msg_bool=False):
    ami = np.asarray(ami)

    for i in range(1, len(ami) - 1):
        if ami[i] < ami[i - 1] and ami[i] <= ami[i + 1]:
            if msg_bool:
                print(f"Optimal delay found at τ = {i+1}")
            return i + 1
    if msg_bool:
        print("No local minimum found, using delay = 1")
    return 1