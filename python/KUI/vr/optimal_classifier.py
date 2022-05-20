import os
import sys
from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt
from numpy import genfromtxt

import metrics
from clf import Classifier, ClassifierTest


def load_classifiers(folder, n_samples=100, n_params=50):
    clf_files = sorted([Path(folder, name) for name in os.listdir(folder) if os.path.isfile(Path(folder, name))
                        and name.endswith('dsv') and name.startswith('C')])
    n_clf = len(clf_files)
    clf_results = np.empty((n_clf, n_samples, n_params,), dtype=int)
    for i in range(n_clf):
        c_f = clf_files[i]
        np_c_f = genfromtxt(c_f, delimiter=',', dtype=int)
        clf_results[i] = np_c_f
    gt_file = Path(folder, 'GT.dsv')
    y_true = genfromtxt(gt_file, dtype=int)
    classifiers: list[Classifier] = []
    for clf in range(n_clf):
        classifier = Classifier(y_true)
        classifiers.append(classifier)
        for alpha in range(n_params):
            y_pred = clf_results[clf, :, alpha]
            cm = metrics.BinaryConfusionMatrix()
            classifier_test = ClassifierTest(cm, y_pred=y_pred, alpha=alpha)
            classifier.check_y(y_pred)
            classifier_test.update_cm(y_true=y_true)
            classifier.update_ct(classifier_test)
    return classifiers


def evaluate_classifiers(classifiers: list[Classifier] = None):
    i = 0
    for c in classifiers:
        i += 1
        x = []
        y = []
        accuracies = np.asarray([ct.metrics()[2] for ct in c.cts])
        max_acc = max(accuracies)
        max_acc_ind = accuracies.argmax()
        for ct in c.cts:
            tpr, fpr, acc, f1 = ct.metrics()
            x.append(fpr)
            y.append(tpr)
            a = ct.alpha
            print(f"C{i} : alpha={a}, {acc}, {tpr}, {fpr}")
        label = f"C{i}: alpha={max_acc_ind}, max_acc={max_acc}"
        plt.plot(x, y, label=label)
        plt.title("ROC curves for alphas")
        plt.legend()
    plt.show()


if __name__ == "__main__":
    clfs = load_classifiers('./classif_result_tables')
    evaluate_classifiers(clfs)
    sys.exit(0)
