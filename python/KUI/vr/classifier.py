import argparse
import os
import sys
from pathlib import Path

import numpy as np
import scipy.sparse as sp
from PIL import Image
from scipy import stats
from scipy.spatial.distance import cdist


def setup_arg_parser():
    parser = argparse.ArgumentParser(description='Learn and classify image data.')
    parser.add_argument('train_path', type=str, help='path to the training data directory')
    parser.add_argument('test_path', type=str, help='path to the testing data directory')
    mutex_group = parser.add_mutually_exclusive_group(required=True)
    mutex_group.add_argument('-k', type=int,
                             help='run k-NN classifier (if k is 0 the code may decide about proper K by itself')
    mutex_group.add_argument("-b",
                             help="run Naive Bayes classifier", action="store_true")
    parser.add_argument("-o", metavar='filepath',
                        default='classification.dsv',
                        help="path (including the filename) of the output .dsv file with the results")
    return parser


#  Uvedením dtype=np.uint16 vyhradíme pro výsledky více bitů, takže se
#  kvadráty do datového typu vejdou.
def image_distance(path_img_1, path_img_2):
    image_1 = Image.open(path_img_1)
    image_2 = Image.open(path_img_2)
    im1 = np.array(image_1).flatten()
    im2 = np.array(image_2).flatten()

    diff = im1 - im2
    d1 = np.sqrt(np.sum(np.square(diff, dtype=np.uint16)))
    d2 = np.linalg.norm(diff)
    return d1, d2


def read_truth_dsv(train_dir):
    d_f = Path(train_dir, 'truth.dsv')
    file_name_label = []
    with open(d_f, 'r') as d_f:
        for line in d_f.readlines():
            stripped = line.strip()
            stripped_split = stripped.split(":")
            p = Path(train_dir, stripped_split[0])
            # unicode int code
            target = ord(stripped_split[1])
            file_name_label.append((p, target))
    return file_name_label


def init_np_arrays(img_files):
    n_samples = len(img_files)
    image = Image.open(img_files[0][0])
    np_img = np.array(image).flatten()
    n_features = len(np_img)
    X = np.empty((n_samples, n_features), dtype=int)
    y = np.empty(n_samples, dtype=int)
    return X, y


def read_test_data(folder):
    img_files = [Path(folder, name) for name in os.listdir(folder) if os.path.isfile(Path(folder, name))
                 and name.endswith('png')]
    targets = [0] * len(img_files)  # no targets for test data
    X, y = init_np_arrays(list(zip(img_files, targets)))
    s = 0
    for f in img_files:
        X[s] = np.array(Image.open(f)).flatten()
        s += 1
    # no target
    return X, None, img_files


def read_train_data(folder):
    labeled_data = read_truth_dsv(folder)
    X, y = init_np_arrays(labeled_data)
    img_files = []
    s = 0
    for l_d in labeled_data:
        img_path = l_d[0]
        img_class = l_d[1]
        img_files.append(img_path)
        np_img = np.array(Image.open(img_path)).flatten()
        X[s] = np_img
        y[s] = img_class
        s += 1
    return X, y, img_files


def samples(folder: str, truth_file=True):
    """
    Read features (X) and targets (y) from parsed truth.dsv
    Targets are converted to their ASCII codes
    Also img file names are loaded for expected output classification.dsv
    """
    if truth_file:
        return read_train_data(folder)

    return read_test_data(folder)


def write_output_dsv(predictions, file_names, dsv_dir, output_file):
    output_dsv_f = Path(output_file)
    # full path to file
    if not output_dsv_f.is_absolute():
        output_dsv_f = Path(dsv_dir, output_file)
    if len(predictions) == len(file_names):
        dsv = list(zip(file_names, predictions))
        # in case of comparison with labeled data use
        # diff -y --suppress-common-lines classification.dsv class_truth.dsv | wc -l gives success rate
        dsv.sort(key=lambda d: d[0])
    else:
        print("ERROR : unequal length of predictions and image file names: {} != {}".
              format(predictions, file_names))
        return
    with open(output_dsv_f, 'w') as output_dsv_f:
        for item in dsv:
            file_name = item[0].name if isinstance(item[0], Path) else item[0]
            pred_class = chr(item[1])
            output_dsv_f.write(file_name + ":" + pred_class + "\n")


class NaiveBayes:
    """
    Multinomial naive Bayes with likelihood p(x_i | y) estimated by
    p_hat(x_i | y) = (N_{y i} + alpha) / (N_y + n_features * alpha)
    where
    N_{y i} = sum_x (x_i) for given y : (n_classes,n_features) array
    N_y = sum_i (N_{y i}) : (n_classes,)
    see https://scikit-learn.org/stable/modules/naive_bayes.html
    """

    def __init__(self, alpha=1.0, fit_prior=True):
        # additive smoothing parameter
        self.alpha = alpha
        # prior class probability - uniform or empirical
        self.fit_prior = fit_prior
        self.classes = None
        self.n_classes = None
        self.n_samples = None
        self.class_log_prior = None
        self.feature_log_prob = None
        self.log_class_count = None

    def one_hot_enc(self, y):
        """one-hot or 1-of-K encoding of targets y - needed for likelihood p(x_i { y ) multinomial estimation
        requires scipy library
        :param y: targets
        :return: one hot encoding of targets
        """
        classes = np.array(sorted(set(y)))
        self.classes = classes
        self.n_samples = len(y)
        self.n_classes = len(classes)
        y_in_classes = np.in1d(y, classes)
        y_seen = y[y_in_classes]
        sorted_class = np.sort(classes)
        indices = np.searchsorted(sorted_class, y_seen)
        indptr = np.hstack((0, np.cumsum(y_in_classes)))

        data = np.empty_like(indices)
        data.fill(1)
        Y = sp.csr_matrix((data, indices, indptr), shape=(self.n_samples, self.n_classes))
        Y = Y.toarray()
        return Y

    def fit(self, X, y):
        """Estimate the log priors of classes (y) and log likelihoods of features X given class variable y
        in the samples X,y"""
        Y = self.one_hot_enc(y)
        n_classes = Y.shape[1]
        if self.n_classes != n_classes:
            print("Wrong one hot encoding")
        n_features = X.shape[1]
        # init counts for features (N_{y i}) and classes (N_y)
        feature_count = np.zeros((n_classes, n_features), dtype=int)
        class_count = np.zeros(n_classes, dtype=int)
        # for matrix multiplication ret = np.dot(a, b) or ret = a @ b np.matmul(a,b) might be used
        # N_{y i} = sum_x (x_i) for given y
        feature_count += np.dot(Y.T, X)
        # N_y = sum_i (N_{y i})
        class_count += Y.sum(axis=0)
        # smoothed counts
        smoothed_fc = feature_count + self.alpha
        smoothed_cc = smoothed_fc.sum(axis=1)
        # multinomial log likelihood estimation - stability
        feature_log_prob = np.log(smoothed_fc) - np.log(smoothed_cc.reshape(-1, 1))
        self.feature_log_prob = feature_log_prob
        # TODO if/else uniform
        # class_log_prior_ = np.full(n_classes, -np.log(n_classes))
        # empirical prior
        log_class_count = np.log(class_count)
        self.log_class_count = log_class_count
        # class log prior probabilities
        class_log_prior = log_class_count - np.log(class_count.sum())
        self.class_log_prior = class_log_prior

    def predict(self, X):
        """Calculate the posterior log probability of the samples X from Bayes rule"""
        log_post_prob = np.dot(X, self.feature_log_prob.T) + self.class_log_prior
        predictions = self.classes[np.argmax(log_post_prob, axis=1)]
        return predictions


class KNearestNeighbors:
    def __init__(self, n_neighbors):
        self._y = None
        self.classes = None
        self.n_neighbors = n_neighbors
        self.fit_X = None
        self.fit_y = None
        self.n_samples_fit = None

    def fit(self, X, y):
        self.fit_X = X
        self.fit_y = y
        # _y indices of the unique array that reconstruct the input array
        self._y = np.empty(y.shape, dtype=int)
        classes, self._y = np.unique(y, return_inverse=True)
        self.classes = classes
        self.n_samples_fit = X.shape[0]

    def kneighbors(self, X):
        distances = cdist(self.fit_X, X, 'euclidean')  # n_train x n_test matrix
        indices = np.argsort(distances, 0)
        distances = np.sort(distances, 0)
        neigh_ind = indices[0:self.n_neighbors, :]
        neigh_dist = distances[0:self.n_neighbors, :]
        return neigh_dist.T, neigh_ind.T

    def predict(self, X):
        neigh_dist, neigh_ind = self.kneighbors(X)
        # _y from row to column
        _y = self._y.reshape((-1, 1))
        classes = self.classes
        mode, _ = stats.mode(_y[neigh_ind, 0], axis=1)
        y_pred = classes.take(mode)
        y_pred = y_pred.ravel()
        return y_pred


def n_b(train_dir, test_dir, output_file, test_accuracy=False):
    clf = NaiveBayes()
    # f_name_train is used to write class_truth.dsv file - can be compared
    # with actual truth file
    X_train, y_train, f_name_train = samples(train_dir, truth_file=True)
    clf.fit(X_train, y_train)

    # y_test is generally not available, only when  truth_file is provided
    X_test, y_test, f_name_test = samples(test_dir, truth_file=False)
    predictions = clf.predict(X_test)
    write_output_dsv(predictions, f_name_test, test_dir, output_file=output_file)
    if test_accuracy:
        report_accuracy(f_name_train, predictions, test_dir, y_test, y_train)


def k_nn(train_dir, test_dir, n_neighbors, output_file, test_accuracy=False):
    X_train, y_train, f_name_train = samples(train_dir, truth_file=True)
    # knn = KNeighborsClassifier(algorithm='brute', n_neighbors=n_neighbors, metric='euclidean')
    knn = KNearestNeighbors(n_neighbors=n_neighbors)
    knn.fit(X_train, y_train)
    X_test, y_test, f_name_test = samples(test_dir, truth_file=True)
    predictions = knn.predict(X_test)
    write_output_dsv(predictions, f_name_test, test_dir, output_file=output_file)
    if test_accuracy:
        # print(knn.score(X_test, y_test))
        report_accuracy(f_name_train, predictions, test_dir, y_test, y_train)


def report_accuracy(f_name_train, predictions, test_dir, y_test, y_train):
    if isinstance(y_test, np.ndarray):
        result = (y_test == predictions)
        correct = np.count_nonzero(result)
        print("Correct={}, Errors={}, Success={} %".format(correct, len(result) - correct, 100 * correct / len(result)))
        # classes = np.array(sorted(set(y_train)))
        # confusion matrix
        # c_m(predictions, y_test, classes)
    write_output_dsv(y_train, f_name_train, test_dir, output_file='class_truth.dsv')


def main(test_accuracy=False):
    parser = setup_arg_parser()
    args = parser.parse_args()

    print('Training data directory:', args.train_path)
    print('Testing data directory:', args.test_path)
    print('Output file:', args.o)
    if args.k is not None:
        k = int(args.k) if int(args.k) > 0 else 3
        print(f"Running k-NN classifier with k={k}")
        k_nn(args.train_path, args.test_path, k, output_file=args.o, test_accuracy=test_accuracy)
    elif args.b:
        print("Running Naive Bayes classifier")
        n_b(args.train_path, args.test_path, output_file=args.o, test_accuracy=test_accuracy)


if __name__ == "__main__":
    main(True)
    sys.exit(0)
