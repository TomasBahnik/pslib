import os
import sys
from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt
from numpy import genfromtxt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, roc_curve, roc_auc_score


def opt_clf(folder, n_samples=100, n_params=50):
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
    # accuracy is float type
    clf_alpha_acc = np.zeros((n_clf, n_params), dtype=float)
    for clf in range(n_clf):
        for param in range(n_params):
            y_pred = clf_results[clf, :, param]
            acc = accuracy(y_true, y_pred)
            clf_alpha_acc[clf, param] = acc
    max_alpha_ind = np.argmax(clf_alpha_acc, axis=1)
    accuracies = np.diagonal(clf_alpha_acc.take(max_alpha_ind, axis=1))
    acc_param = list(zip(accuracies, max_alpha_ind))
    best_y_pred = np.empty((n_clf, n_samples), dtype=int)
    for j in range(len(acc_param)):
        max_ind = acc_param[j][1]
        best_y_pred[j] = clf_results[j, :, max_ind]
    return y_true, acc_param, best_y_pred


def accuracy(y_true, y_pred):
    if isinstance(y_true, np.ndarray):
        result = (y_true == y_pred)
        correct = np.count_nonzero(result)
        acc = correct / len(result)
        # print("Correct={}, Errors={}, accuracy={}".format(correct, len(result) - correct, acc))
        return acc


def display_plots(y_true, best_clf, best_pred, roc):
    classes = (0, 1)
    for i in range(len(best_clf)):
        alpha = best_clf[i][1]
        acc = best_clf[i][0]
        y_pred = best_pred[i]
        print("{}. classifier acc = {}, alpha = {}".format(i + 1, acc, alpha))
        if roc:
            fpr, tpr, thresh = roc_curve(y_true, y_pred)
            auc = roc_auc_score(y_true, y_pred)
            label = "clf=" + str(i + 1) + ",alpha_ind=" + str(alpha) + ",auc=" + str(round(auc, 2))
            plt.plot(fpr, tpr, label=label)
            plt.title("Best ROC curves with AUC")
            plt.legend()
        else:
            cm = confusion_matrix(y_true, y_pred, labels=classes)
            disp_labels = classes
            disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=disp_labels)
            color_bar = True
            disp.plot(colorbar=color_bar)
            label = "clf=" + str(i + 1) + ",alpha_ind=" + str(alpha) + ",accuracy=" + str(round(acc, 2))
            disp.ax_.set_title(label)
            plt.show()
    plt.show()


if __name__ == "__main__":
    y_true, best_clf, best_pred = opt_clf('./classif_result_tables')
    roc = False
    display_plots(y_true, best_clf, best_pred, roc)
    sys.exit(0)
