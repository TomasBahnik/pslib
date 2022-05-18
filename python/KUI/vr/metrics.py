import abc


class BinaryConfusionMatrix:
    """Binary confusion matrix is required for most binary classification metrics"""

    def __init__(self, true_positives=0, true_negatives=0, false_positives=0, false_negatives=0):
        self.true_positives = true_positives
        self.true_negatives = true_negatives
        self.false_positives = false_positives
        self.false_negatives = false_negatives
        self.num_samples = sum([true_positives, true_negatives, false_positives, false_negatives])

    def update(self, y_pred, y_true):
        for yp, yt in zip(y_pred, y_true):
            self.num_samples += 1
            if yp and yt:
                self.true_positives += 1
            elif yp and not yt:
                self.false_positives += 1
            elif not yp and not yt:
                self.true_negatives += 1
            else:
                self.false_negatives += 1


class Metric(abc.ABC):
    def __init__(self, cm: BinaryConfusionMatrix):
        self.cm = cm

    @abc.abstractmethod
    def get(self):
        raise NotImplementedError

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.get()}"

    def __str__(self):
        return repr(self)


class Precision(Metric):
    def get(self):
        try:
            return self.cm.true_positives / (self.cm.true_positives + self.cm.false_positives)
        except ZeroDivisionError:
            return 0.0


class Recall(Metric):
    def get(self):
        try:
            return self.cm.true_positives / (self.cm.true_positives + self.cm.false_negatives)
        except ZeroDivisionError:
            return 0.0


class TruePositiveRate(Metric):
    """Same as Recall"""

    def get(self):
        positive = GroundTruthPositive(self.cm).get()
        try:
            return self.cm.true_positives / positive
        except ZeroDivisionError:
            return 0.0


class FalsePositiveRate(Metric):
    def get(self):
        negative = GroundTruthNegative(self.cm).get()
        try:
            return self.cm.false_positives / negative
        except ZeroDivisionError:
            return 0.0


class F1(Metric):
    def __init__(self, cm: BinaryConfusionMatrix):
        super().__init__(cm)
        self.precision = Precision(self.cm)
        self.recall = Recall(self.cm)
        self.beta = 1.0

    def get(self):
        p = self.precision.get()
        r = self.recall.get()
        b2 = self.beta ** 2
        try:
            return (1 + b2) * p * r / (b2 * p + r)
        except ZeroDivisionError:
            return 0.0


class PredictionPositive(Metric):
    def get(self):
        return self.cm.true_positives + self.cm.false_positives


class PredictionNegative(Metric):
    def get(self):
        return self.cm.true_negatives + self.cm.false_negatives


class GroundTruthPositive(Metric):
    """the number of real positive cases in the data"""

    def get(self):
        return self.cm.true_positives + self.cm.false_negatives


class GroundTruthNegative(Metric):
    """the number of real negative cases in the data"""

    def get(self):
        return self.cm.true_negatives + self.cm.false_positives
