import sys

import numpy as np
from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.naive_bayes import MultinomialNB, ComplementNB


def multinomial_n_b(X_test, X_train, y_test, y_train):
    print("Using scikit multinomial nb")
    clf = MultinomialNB()
    clf.fit(X_train, y_train)
    predictions = clf.predict(X_test)
    c_m(predictions, y_test, clf.classes_, n_b_type=1)


def complement_n_b(X_test, X_train, y_test, y_train):
    print("Using scikit complement nb")
    clf = ComplementNB()
    clf.fit(X_train, y_train)
    predictions = clf.predict(X_test)
    c_m(predictions, y_test, clf.classes_, n_b_type=1)


def c_m(predictions, y_test, classes, n_b_type=0):
    cm = confusion_matrix(y_test, predictions, labels=classes)
    disp_labels = [chr(x) for x in classes]
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=disp_labels)
    color_bar = False if n_b_type == 0 else True
    disp.plot(colorbar=color_bar)
    plt.show()


def sample_data():
    rng = np.random.RandomState(1)
    X = rng.randint(5, size=(7, 10))
    y = np.array([1, 1, 2, 3, 4, 5, 6])
    return X, y


if __name__ == "__main__":
    sample_data()
    sys.exit(0)
