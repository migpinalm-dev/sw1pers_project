import numpy as np
from sw1pers_l.core import SW1PerS_L

def calibrate(series: list[float], lower_bound, upper_bound, num_div) -> int:
    candidate_ws = np.unique(
        np.logspace(
            np.log10(lower_bound),
            np.log10(upper_bound),
            num_div
        ).astype(int)
    )

    y_metric = []

    factor = 1
    threshold_ratio = 0.4
    patience = 3
    small_count = 0
    max_drop = 0

    best_ws = candidate_ws[-1]   # fallback

    for i, ws in enumerate(candidate_ws):
        wstrd = max(1, ws // 10)    # set window stride

        scores = SW1PerS_L(
            series,
            factor=factor,
            size=ws * factor,
            stride=wstrd * factor,
            min_dim=3,
            plot_bool=False
        )

        # Main metric ----------------------------
        scores = np.array(scores)
        metric = scores.mean() + 0.5 * scores.var()

        y_metric.append(metric)

        if i == 0:
            continue

        curr_drop = y_metric[i-1] - y_metric[i]
        max_drop = max(max_drop, np.abs(curr_drop))

        if abs(curr_drop) < threshold_ratio * max_drop:
            small_count += 1
        else:
            small_count = 0

        if small_count >= patience:
            best_ws = candidate_ws[i - patience + 1]
            break

    return int(best_ws)

# -------------------------------------------------------------------

from scipy.stats import kendalltau

def jtk_cycle_score(x, time=None, periods=np.arange(16, 36), n_phases=24):
    x = np.asarray(x)

    if time is None:
        time = np.arange(len(x))
    else:
        time = np.asarray(time)

    best_score = -np.inf     # compare abs(tau)
    best_tau = None
    best_period = None
    best_phase = None

    for P in periods:
        phases = np.linspace(0, P, n_phases, endpoint=False)

        for phi in phases:
            ref = np.cos((2*np.pi/P) * (time - phi))

            tau, _ = kendalltau(x, ref, nan_policy='omit')

            # Skip invalid tau
            if tau is None or np.isnan(tau):
                continue

            score = np.abs(tau)
            if score > best_score:
                best_score = score
                best_tau = tau
                best_period = P
                best_phase = phi

    return best_tau, best_period, best_phase

def calibrate_via_jtk(ts, period_interval, n_phases=10):
    y_axis = ts
    x_axis = np.arange(len(ts))
    tau, period, phase = jtk_cycle_score(y_axis, x_axis, periods = np.arange(period_interval[0], period_interval[1]), n_phases=2)
    return tau, period, phase