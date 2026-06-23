
# run this test: go to root directory -> python tests/test_pipeline.py

#------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt

from sw1pers_l.core import SW1PerS, SW1PerS_L

import kagglehub, os
import pandas as pd

#------------------------------------------------
# DATA
# x = np.arange(0, 10*2*np.pi, 0.1)
# test_ts = np.cos(x)

key = "energy_consumption"

FILE = "tetuan-city-power-consumption"

path = kagglehub.dataset_download(f"gmkeshav/{FILE}")

print("Path to dataset files:", path)

files = os.listdir(path)
print("Downloaded files:", files)
df = pd.read_csv(os.path.join(path, files[0]))
df.info()

period = 144
L = 10
instances = period*L    # S = 144 * L
column = 'Zone 1 Power Consumption'
dates_energy = df["DateTime"].values[0:instances]
energy_consumption = df[column].values[0:instances]

test_ts = energy_consumption
dates = dates_energy

#------------------------------------------------

# scores = SW1PerS_L(test_ts, size=160, stride=32)
# print(scores)

# candidate_ws = np.unique(np.logspace(np.log10(len(test_ts)//10), np.log10(len(test_ts)//3), 25).astype(int))

candidate_ws = np.linspace(152, 180, 10).astype(int)
threshold_ratio = 0.2

y_metric = []
best_ws = candidate_ws[-1]   # fallback

prev_metric = None
prev_drop = None

for ws in candidate_ws:
    wstrd = ws // 10
    scores = SW1PerS_L(test_ts, size=ws, stride=wstrd)
    metric = scores.mean() + 0.5 * scores.var()
    y_metric.append(metric)
    print(metric, ws)
    if prev_metric is not None:
        curr_drop = prev_metric - metric   # how much we improved
        if prev_drop is not None:
            # if improvement has become much smaller, we're at the elbow
            if np.abs(curr_drop) < np.abs(threshold_ratio * prev_drop):
                best_ws = ws #prev_ws
                break
        prev_drop = curr_drop
        prev_ws = ws    # optional
    prev_metric = metric

plt.plot(candidate_ws[:len(y_metric)], y_metric)
plt.show()
print(f"BEST WINDOW SIZE = {best_ws}")
