from scipy.interpolate import CubicSpline
import numpy as np

def make_spline(x, y, instances=2000,):
    factor = round(instances/len(y))
    print(f"Factor = {factor}\n")

    t = np.arange(len(y) * factor)

    cs = CubicSpline(x, y)

    t_fine = np.linspace(x[0], x[-1], len(t))
    finer_spline = cs(t_fine)
    return t_fine, finer_spline