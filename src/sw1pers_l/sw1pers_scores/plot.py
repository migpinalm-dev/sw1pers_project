import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
from sw1pers_l.sw1pers_scores._density import density

def plot_score_landscape(scores, score_density, finer_spline, window_size, window_stride, dates, rolling_size_scores):

    offset = round(window_size/2)
    scale_factor = np.max(finer_spline)/(np.max(scores))
    fig, ax1 = plt.subplots(figsize=(11, 4))
    x = range(0, len(finer_spline))

    # Secondary y-axis (scores) ---------------------------------------------------
    ax2 = ax1.twinx()
    bar_y = scores
    bar_x = np.arange(offset, offset + window_stride * len(scores), window_stride)
    bar_width = window_size
    ax2.bar(bar_x, bar_y, width=bar_width, alpha=0.15, label="Periodicity Score", color = "orange")
    ax2.set_ylabel("Periodicity Score", color = "orange")
    ax2.tick_params(axis='y', labelcolor = "orange")
    ax2.set_ylim(0, np.max(bar_y)*1.05)

    # Primary y-axis (time series) ------------------------------------------------
    ax1.plot(x, finer_spline, label="Time Series Spline", color="C0", alpha=0.4)
    ax1.set_ylabel("Time Series Spline", color="C0")
    ax1.tick_params(axis='y', labelcolor='C0')
    # ax1.set_ylim(np.min(finer_spline), np.max(finer_spline))

    #Window indexing --------------------------------------------------------------
    secax = ax1.secondary_xaxis("top")
    step = 20
    tick_positions = bar_x[::step]
    tick_labels = [str(i) for i in range(0, len(bar_x), step)]
    secax.set_xticks(tick_positions)
    secax.set_xticklabels(tick_labels, rotation=45)
    secax.set_xlabel("Windows")

    # Date indexing (and primary time series) ---------------------------------------------------------------
    if dates is not None:
        n_ticks = int(len(finer_spline)/window_size/2)
        tick_positions = np.linspace(0, len(finer_spline)-1, n_ticks, dtype=int)
        tick_dates = pd.date_range(start=dates[0], end=dates[-1], periods=n_ticks)
        ax1.set_xticks(tick_positions)
        ax1.set_xticklabels(tick_dates.strftime("%Y-%m-%d"), rotation=45, ha="right")    #%Y-%m-%d [%H:%M]
        ax1.set_xlabel("Date")
        ax1.set_ylabel("Time Series Spline", color="C0")
        ax1.tick_params(axis='y', labelcolor='C0')

    # Density plot ----------------------------------------------------------------
    ma_x = bar_x[rolling_size_scores//2 : -(rolling_size_scores//2)]  # center alignment
    ma_y = score_density[rolling_size_scores//2 : -(rolling_size_scores//2)] #* scale_factor
    ax2.plot(ma_x, ma_y, color="red", linewidth=2, label="Anomaly Density (MA)", alpha=0.6)

    # Labels: combine from both axes-----------------------------------------------
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc="lower right")
    plt.tight_layout()
    plt.grid()
    plt.show()

def plot_scores_comparison(scores, secondary_scores, window_size, window_stride, dates, factor=1, score_rolling_size=1, sec_score_rolling_size=1, is_score_windowed = False, show_bars = False, label_msg = "Alternative anomaly score"):
    fig, ax1 = plt.subplots(figsize=(11, 4))
    offset = round(window_size/2)

    # Window x-axis set up -------------------------
    windows_x = np.arange(offset, offset + window_stride * len(scores), window_stride)
    
    # Secondary scores plot ----------------
    sec_score_density = density(secondary_scores, sec_score_rolling_size)
    if is_score_windowed:
        ax1.plot(windows_x, sec_score_density, color="C0", linewidth=1, label="Secondary Scores")
        ax1.set_ylabel(label_msg, color = "C0")
        ax1.tick_params(axis='y', labelcolor = 'C0')
    else:
        x = range(0, len(density(secondary_scores, sec_score_rolling_size)))
        ax1.plot(x, sec_score_density, linewidth=1, label="Secondary Score Landscape", color="C0")
        ax1.set_ylabel(label_msg, color="C0")
        ax1.tick_params(axis='y', labelcolor='C0')

    ax2 = ax1.twinx()

    #sw1pers bars plot
    if show_bars:
        windows_y = scores
        bar_width = window_size
        ax2.bar(windows_x, windows_y, width=bar_width, alpha=0.15, label="Periodicity Scores", color = "orange")
        ax2.set_ylabel("Periodicity Scores", color = "orange")
        ax2.tick_params(axis='y', labelcolor = "orange")

    # sw1pers plot -----------------
    ma_x = windows_x[-int(-score_rolling_size//2) : int(-score_rolling_size//2)]  # center alignment
    ma_y = density(scores, score_rolling_size)[-int(-score_rolling_size//2) : int(-score_rolling_size//2)]    # math.ceil(score_rolling_size//2)) also works here
    ax2.plot(ma_x, ma_y, color="orange", linewidth=1, label="Periodicity Density")
    ax2.set_ylabel("Periodicity score", color="orange")
    ax2.tick_params(axis='y', labelcolor='orange')

    #Window indexing -----------------------
    secax = ax2.secondary_xaxis("top")
    step = 20
    tick_positions = windows_x[::step]
    tick_labels = [str(i) for i in range(0, len(windows_x), step)]
    secax.set_xticks(tick_positions)
    secax.set_xticklabels(tick_labels, rotation=45)
    secax.set_xlabel("Windows")

    # Date indexing (and primary time series) ---------------------------------------------------------------
    if dates is not None:
        n_ticks = int(len(dates)*factor/(window_size))
        tick_positions = np.linspace(0, len(dates)*factor-1, n_ticks, dtype=int)
        tick_dates = pd.date_range(start=dates[0], end=dates[-1], periods=n_ticks)
        ax1.set_xticks(tick_positions)
        ax1.set_xticklabels(tick_dates.strftime("%Y-%m-%d"), rotation=45, ha="right")    #%Y-%m-%d [%H:%M]
        ax1.set_xlabel("Date")