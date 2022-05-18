import numpy as np

from metrics import BinaryConfusionMatrix, TruePositiveRate, FalsePositiveRate, Accuracy, F1


class ClassifierTest:
    """Individual pairs of predictions for give parameter"""

    def __init__(self, cm: BinaryConfusionMatrix, y_pred: np.ndarray, alpha: int = -1):
        self.cm = cm
        self.alpha = alpha
        self.y_pred = y_pred

    def update_cm(self, y_true):
        self.cm.update(self.y_pred, y_true)

    def metrics(self):
        tpr = TruePositiveRate(self.cm).get()
        fpr = FalsePositiveRate(self.cm).get()
        acc = Accuracy(self.cm).get()
        f1 = F1(self.cm).get()
        f1 = round(f1, 2)
        return tpr, fpr, acc, f1


class Classifier:
    """Classifier prediction for given parameters"""

    def __init__(self, y_true=None):
        self.cts: list[ClassifierTest] = []
        self.y_true = y_true
        self.num_samples = None

    def check_y(self, y_pred):
        assert isinstance(self.y_true, np.ndarray)
        assert isinstance(y_pred, np.ndarray)
        if len(self.y_true) == len(y_pred):
            self.num_samples = len(self.y_true)
        else:
            raise AssertionError

    def update_ct(self, ct: ClassifierTest):
        self.cts.append(ct)
