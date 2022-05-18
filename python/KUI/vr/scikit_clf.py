import sys

import numpy as np
from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, roc_curve
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


def sample_data():
    rng = np.random.RandomState(1)
    X = rng.randint(5, size=(7, 10))
    y = np.array([1, 1, 2, 3, 4, 5, 6])
    return X, y


if __name__ == "__main__":
    sys.exit(0)
