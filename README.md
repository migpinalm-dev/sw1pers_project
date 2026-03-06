The algorithm SW1PerS yields a scalar periodicity score for univariate time series.
The aim of this project is to make extend the algorithm in order to correspond an array of periodicity scores to univariate time series:
    The time series is divided into overlapping snippets (sub-time-series), to each of which we apply SW1PerS.
    The size of the snippet and the overlapping size are hyper-parameters (dependent on the data)

This is useful to locate periodic behaviour in general time series.
On the other hand, this is useful to locate aperiodic behaviour in periodc time series.
