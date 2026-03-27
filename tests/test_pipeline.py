
# run this test: go to root directory -> python tests/test_pipeline.py

#------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt

from sw1pers_l.core import SW1PerS, SW1PerS_L

#------------------------------------------------

x = np.arange(0, 10*2*np.pi, 0.1)
test_ts = np.cos(x)

scores = SW1PerS_L(test_ts)