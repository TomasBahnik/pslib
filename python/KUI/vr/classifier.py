import argparse
import os
import sys
from pathlib import Path

import numpy as np
import scipy.sparse as sp
from PIL import Image

CLASSIFICATION_DSV = 'classification.dsv'


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
                        default=CLASSIFICATION_DSV,
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


def read_test_data(folder):
    png_files = [Path(folder, name) for name in os.listdir(folder)
                 if os.path.isfile(Path(folder, name)) and name.endswith('png')]
    n_samples = len(png_files)
    image = Image.open(png_files[0])
    np_img = np.array(image).flatten()
    n_features = len(np_img)
    X = np.empty((n_samples, n_features), dtype=int)
    s = 0
    for f in png_files:
        i = Image.open(f)
        X[s] = np.array(i).flatten()
        s += 1
    # no target
    return X, None, png_files


def read_truth_dsv(dsv_dir, truth_file=True):
    if truth_file:
        d_f = Path(dsv_dir, 'truth.dsv')
        ret = []
        with open(d_f, 'r') as d_f:
            for line in d_f.readlines():
                stripped = line.strip()
                ret.append(stripped.split(":"))
        return ret
    else:
        return read_test_data(dsv_dir)


def write_output_dsv(predictions, file_names, dsv_dir, output_file=CLASSIFICATION_DSV):
    d_f = Path(dsv_dir, output_file)
    if len(predictions) == len(file_names):
        dsv = list(zip(file_names, predictions))
        # sort by file name to compare with case without truth file - might be removed or truth.dsv=False/True
        # but in reality truth.dsv is never available for test
        dsv.sort(key=lambda d: d[0])
    else:
        print("ERROR : unequal length of predictions and image file names: {} != {}".
              format(predictions, file_names))
        return
    with open(d_f, 'w') as d_f:
        for item in dsv:
            file_name = item[0].name if isinstance(item[0], Path) else item[0]
            pred_class = chr(item[1])
            d_f.write(file_name + ":" + pred_class + "\n")


def samples(folder: str, truth_file=True):
    """
    Read features (X) and targets (y) from parsed truth.dsv
    Targets are converted to their ASCII codes
    Also img file names are loaded for expected output classification.dsv
    """
    labeled_data = read_truth_dsv(folder, truth_file)
    if not truth_file:
        return labeled_data
    n_samples = len(labeled_data)
    img_file = folder + '/' + labeled_data[0][0]
    image = Image.open(img_file)
    np_img = np.array(image).flatten()
    n_features = len(np_img)
    # sample values
    X = np.empty((n_samples, n_features), dtype=int)
    file_names = []
    # target values = classes
    y = np.empty(n_samples, dtype=int)
    s = 0
    for l_d in labeled_data:
        file_name = l_d[0]
        file_class = l_d[1]
        img_file = Path(folder, file_name)
        file_names.append(file_name)
        # unicode int code
        class_code = ord(file_class)
        image = Image.open(img_file)
        np_img = np.array(image).flatten()
        X[s] = np_img
        y[s] = class_code
        s += 1
    return X, y, file_names


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


# Výsledkem klasifikátoru je soubor classification.dsv stejného formátu jako truth.dsv,
# který je umístěný v adresáři s testovacími obrázky.
def n_b(train_dir, test_dir, output_file=CLASSIFICATION_DSV):
    # multinomial_n_b(X_test, X_train, y_test, y_train)
    clf = NaiveBayes()
    X_train, y_train, f_name_train = samples(train_dir)
    # X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
    clf.fit(X_train, y_train)

    # TODO there is no truth.dsv for test data => y_test = None
    X_test, y_test, f_name_test = samples(test_dir, truth_file=True)
    predictions = clf.predict(X_test)
    if isinstance(y_test, np.ndarray):
        result = (y_test == predictions)
        correct = np.count_nonzero(result)
        print("Success {} %".format(100 * correct / len(result)))
    write_output_dsv(predictions, f_name_test, test_dir, output_file=output_file)
    # c_m(predictions, y_test, clf.classes)


def main():
    parser = setup_arg_parser()
    args = parser.parse_args()

    print('Training data directory:', args.train_path)
    print('Testing data directory:', args.test_path)
    print('Output file:', args.o)
    if args.k is not None:
        print(f"Running k-NN classifier with k={args.k}")
        # TODO Train and test the k-NN classifier
        # temporary use NB to check availability of scipy
        n_b(args.train_path, args.test_path, output_file=args.o)
    elif args.b:
        print("Running Naive Bayes classifier")
        n_b(args.train_path, args.test_path, output_file=args.o)


if __name__ == "__main__":
    # python classifier.py -b ./train_1000_28 ./test_data
    main()
    sys.exit(0)
