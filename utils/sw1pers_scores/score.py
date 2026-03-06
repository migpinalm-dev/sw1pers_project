import numpy as np
from .max_features import select_max_features

def compute_scores(diagrams, n=2, m=2):    # n >= m
    scores = []
    max_feat = select_max_features(diagrams)
    for feat in max_feat:
        score = 1 - (feat[1]**n - feat[0]**m)/(np.sqrt(3))**n
        if score < 0:
            score = 0
        if score > 1:
            score = 1
        scores.append(score)
    return np.array(scores)