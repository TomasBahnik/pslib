import os
import sys
from pathlib import Path

import numpy as np
from numpy import genfromtxt

import metrics
from clf import Classifier


def load_classifiers(folder, n_samples=100, n_params=50):
    clf_files = [Path(folder, name) for name in os.listdir(folder) if os.path.isfile(Path(folder, name))
                 and name.endswith('dsv') and name.startswith('C')]

    n_clf = len(clf_files)
    clf_results = np.empty((n_clf, n_samples, n_params,), dtype=int)
    for i in range(n_clf):
        c_f = clf_files[i]
        np_c_f = genfromtxt(c_f, delimiter=',', dtype=int)
        clf_results[i] = np_c_f
    gt_file = Path(folder, 'GT.dsv')
    y_true = genfromtxt(gt_file, dtype=int)
    classifiers = []
    for clf in range(n_clf):
        for alpha in range(n_params):
            y_pred = clf_results[clf, :, alpha]
            cm = metrics.BinaryConfusionMatrix()
            classifier = Classifier(cm, alpha, y_pred, y_true)
            classifier.check_y()
            classifier.update_cm()
            classifiers.append(classifier)
    return classifiers


def evaluate_classifiers(classifiers: list[Classifier] = None):
    i = 0
    for c in classifiers:
        """Print metrics"""
        tpr = metrics.TruePositiveRate(c.cm)
        fpr = metrics.FalsePositiveRate(c.cm)
        acc = metrics.Accuracy(c.cm)
        f1 = metrics.F1(c.cm).get()
        f1 = round(f1, 2)
        a = c.alpha
        ind = (i // 50) + 1
        print(f"C{ind}.alpha={a}. {acc}, F1={f1}, {tpr}, {fpr}")
        i += 1


if __name__ == "__main__":
    clfs = load_classifiers('./classif_result_tables')
    evaluate_classifiers(clfs)
    sys.exit(0)
