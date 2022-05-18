import numpy as np

from metrics import BinaryConfusionMatrix


class Classifier:
    """Classifier prediction for given parameters"""

    def __init__(self, cm: BinaryConfusionMatrix, alpha=0, y_pred=None, y_true=None):
        self.alpha = alpha
        self.y_pred = y_pred
        self.y_true = y_true
        self.cm = cm
        self.num_samples = None

    def check_y(self):
        assert isinstance(self.y_true, np.ndarray)
        assert isinstance(self.y_pred, np.ndarray)
        if len(self.y_pred) == len(self.y_true):
            self.num_samples = len(self.y_true)
        else:
            raise AssertionError

    def update_cm(self):
        self.cm.update(self.y_pred, self.y_true)
