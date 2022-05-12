import os
import sys
from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt
from numpy import genfromtxt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, roc_curve, RocCurveDisplay
from sklearn.naive_bayes import MultinomialNB, ComplementNB
from sklearn.neighbors import NeighborhoodComponentsAnalysis, KNeighborsClassifier
from sklearn.pipeline import Pipeline

from classifier import samples, write_output_dsv, report_accuracy


def multinomial_n_b(X_test, X_train, y_test, y_train):
    print("Using scikit multinomial nb")
    clf = MultinomialNB()
    clf.fit(X_train, y_train)
    predictions = clf.predict(X_test)
    c_m(y_test, predictions, clf.classes_, n_b_type=1)


def complement_n_b(X_test, X_train, y_true, y_train):
    print("Using scikit complement nb")
    clf = ComplementNB()
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    c_m(y_true, y_pred, clf.classes_, n_b_type=1)


def c_m(y_true, y_pred, classes, n_b_type=0):
    cm = confusion_matrix(y_true, y_pred, labels=classes)
    roc = roc_curve(y_true, y_pred)
    # disp_labels = [chr(x) for x in classes]
    disp_labels = classes
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=disp_labels)
    # roc_disp = RocCurveDisplay.from_predictions(y_true, y_pred)
    # color_bar = False if n_b_type == 0 else True
    color_bar = True
    disp.plot(colorbar=color_bar)
    plt.show()


def k_nn(train_dir, test_dir, n_neighbors, output_file, test_accuracy=False):
    X_train, y_train, f_name_train = samples(train_dir, truth_file=True)
    nca = NeighborhoodComponentsAnalysis(random_state=42)
    knn = KNeighborsClassifier(n_neighbors=n_neighbors)
    nca_pipe = Pipeline([('nca', nca), ('knn', knn)])
    nca_pipe.fit(X_train, y_train)
    X_test, y_test, f_name_test = samples(test_dir, truth_file=False)
    predictions = nca_pipe.predict(X_test)
    write_output_dsv(predictions, f_name_test, test_dir, output_file=output_file)
    if test_accuracy:
        print(nca_pipe.score(X_test, y_test))
        report_accuracy(f_name_train, predictions, test_dir, y_test, y_train)


def opt_clf(folder, n_samples=100, n_params=50):
    clf_files = [Path(folder, name) for name in os.listdir(folder) if os.path.isfile(Path(folder, name))
                 and name.endswith('dsv') and name.startswith('C')]

    n_clf = len(clf_files)
    clf_results = np.empty((n_clf, n_samples, n_params,), dtype=int)
    for i in range(n_clf):
        c_f = clf_files[i]
        np_c_f = genfromtxt(c_f, delimiter=',')
        clf_results[i] = np_c_f
    gt_file = Path(folder, 'GT.dsv')
    y_true = genfromtxt(gt_file, delimiter=',')
    classes = [0, 1]
    clf_alpha_acc = np.zeros((n_clf, n_params), dtype=float)
    for clf in range(n_clf):
        for param in range(n_params):
            y_pred = clf_results[clf, :, param]
            acc = accuracy(y_true, y_pred)
            clf_alpha_acc[clf, param] = acc
            # print("Score : clf={}, alpha={}: accuracy={}".format(clf, param, acc))
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


def sample_data():
    rng = np.random.RandomState(1)
    X = rng.randint(5, size=(7, 10))
    y = np.array([1, 1, 2, 3, 4, 5, 6])
    return X, y


if __name__ == "__main__":
    y_true, best_clf, best_pred = opt_clf('./classif_result_tables')
    for i in range(len(best_clf)):
        print("{}. classifier acc = {}, alpha = {}".format(i + 1, best_clf[i][0], best_clf[i][1]))
        y_pred = best_pred[i]
        c_m(y_true, y_pred, (0, 1))
    sys.exit(0)
