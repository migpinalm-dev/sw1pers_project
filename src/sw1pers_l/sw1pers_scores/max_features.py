import numpy as np

def select_max_features(diagrams):
    max_feature_arr = []
    for diagram in diagrams:
        if len(diagram[1])==0:
            max_feature_arr.append([0,0])
        else:
            max_feature = []
            max = 0
            for feature in diagram[1]:
                if max < feature[1] - feature[0] and not np.isinf(feature[1]):
                    max = feature[1] - feature[0]
                    max_feature = [feature[0], feature[1]]
                elif np.isinf(feature[1]) or max > np.sqrt(3):
                    max = np.sqrt(3)
                    max_feature = [feature[0], np.sqrt(3)]
            max_feature_arr.append(max_feature)
    return max_feature_arr