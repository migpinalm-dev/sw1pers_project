import numpy as np
from sw1pers_l.core import SW1PerS_L

def evaluate_window(series: list[float], lower_bound, upper_bound, num_div) -> int:
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