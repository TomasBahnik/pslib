import sys

import numpy as np
from matplotlib import pyplot as plt
from sklearn import metrics
from sklearn.metrics import roc_auc_score


def roc_curve():
    # y = np.array([1, 1, 2, 2])
    y = np.array([1, 1, 0, 0])
    scores = np.array([1, 0, 1, 1])
    fpr, tpr, thresholds = metrics.roc_curve(y, scores, pos_label=2)
    auc = roc_auc_score(y, scores)
    label = "auc=" + str(round(auc, 2))
    plt.plot(fpr, tpr, label=label)
    plt.title("Best ROC curves with AUC")
    plt.legend()
    plt.show()
    return fpr, tpr, thresholds


if __name__ == "__main__":
    roc_curve()
    sys.exit(0)
