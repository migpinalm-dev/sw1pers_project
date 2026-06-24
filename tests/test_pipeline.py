
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
cache_file = f"{FILE}.parquet"

if not os.path.exists(cache_file):
    path = kagglehub.dataset_download(f"gmkeshav/{FILE}")

    print("Path to dataset files:", path)

    files = os.listdir(path)
    print("Downloaded files:", files)

    df = pd.read_csv(os.path.join(path, files[0]))
    df.info()

    df.to_parquet(cache_file)
else:
    print("--------READING FROM CACHE--------")
    df = pd.read_parquet(cache_file)

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

#------------------------------------------------

candidate_ws = np.unique(np.logspace(np.log10(len(test_ts)//11), np.log10(len(test_ts)//5), 20).astype(int))

# candidate_ws = np.linspace(152, 180, 10).astype(int)

y_metric = []

factor = 1

threshold_ratio = 0.3
patience = 3
small_count = 0
max_drop = 0

best_ws = candidate_ws[-1]   # fallback

for i, ws in enumerate(candidate_ws):
    wstrd = ws // 10
    scores = SW1PerS_L(test_ts, factor=factor, size=ws*factor, stride=wstrd*factor, plot_bool=False)    # no score plotting
    metric = scores.mean() + 0.5 * scores.var()
    y_metric.append(metric)

    if i==0:
        continue    # skip to next iteration

    curr_drop = y_metric[i-1] - y_metric[i]
    max_drop = max(max_drop, curr_drop)

    if np.abs(curr_drop) < threshold_ratio * max_drop:
        small_count += 1
    else:
        small_count = 0

    if small_count >= patience:
        best_ws = candidate_ws[i-patience+1]
        break

print(f"BEST WINDOW SIZE = {best_ws}")

plt.plot(candidate_ws[:len(y_metric)], y_metric)
plt.show()
