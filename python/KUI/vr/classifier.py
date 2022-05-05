import argparse
import sys
from pathlib import Path

import numpy as np
import scipy.sparse as sp
from PIL import Image
from sklearn.model_selection import train_test_split

from scikit_clf import c_m


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


def read_truth_dsv(dsv_dir, dsv_file):
    d_f = Path(dsv_dir, dsv_file)
    ret = []
    with open(d_f, 'r') as d_f:
        for line in d_f.readlines():
            stripped = line.strip()
            ret.append(stripped.split(":"))
    return ret


def read_samples(truth_data):
    # train_data = random 1/2 of indexes
    path = Path("train_data")
    for fpath in path.iterdir():
        print(fpath)


class NaiveBayes:

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

    def samples(self, labeled_data: list, folder: str):
        n_samples = len(labeled_data)
        img_file = folder + '/' + labeled_data[0][0]
        image = Image.open(img_file)
        np_img = np.array(image).flatten()
        n_features = len(np_img)
        # sample values
        X = np.empty((n_samples, n_features), dtype=int)
        # target values = classes
        y = np.empty(n_samples, dtype=int)
        s = 0
        for l_d in labeled_data:
            img_file = folder + '/' + l_d[0]
            img_label_ascii = ord(l_d[1])
            image = Image.open(img_file)
            np_img = np.array(image).flatten()
            X[s] = np_img
            y[s] = img_label_ascii
            s += 1
        return X, y

    def one_hot_enc(self, y):
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
        Y = self.one_hot_enc(y)
        n_classes = Y.shape[1]
        if self.n_classes != n_classes:
            print("Wrong one hot encoding")
        n_features = X.shape[1]
        # init count attributes
        feature_count = np.zeros((n_classes, n_features), dtype=int)
        class_count = np.zeros(n_classes, dtype=int)
        # ret = np.dot(a, b) or ret = a @ b np.matmul(a,b)
        feature_count += np.dot(Y.T, X)
        class_count += Y.sum(axis=0)
        # smoothed counts
        smoothed_fc = feature_count + self.alpha
        smoothed_cc = smoothed_fc.sum(axis=1)
        # fit model
        feature_log_prob = np.log(smoothed_fc) - np.log(smoothed_cc.reshape(-1, 1))
        self.feature_log_prob = feature_log_prob
        # TODO if/else uniform
        # class_log_prior_ = np.full(n_classes, -np.log(n_classes))
        # empirical prior
        log_class_count = np.log(class_count)
        self.log_class_count = log_class_count
        class_log_prior = log_class_count - np.log(class_count.sum())
        self.class_log_prior = class_log_prior

    def predict(self, X):
        """Calculate the posterior log probability of the samples X"""
        log_post_prob = np.dot(X, self.feature_log_prob.T) + self.class_log_prior
        predictions = self.classes[np.argmax(log_post_prob, axis=1)]
        return predictions


# TODO return
# Výsledkem klasifikátoru je soubor classification.dsv stejného formátu jako truth.dsv,
# který je umístěný v adresáři s testovacími obrázky.
def n_b(train_dir, test_dir, output_file='classification.dsv'):
    # multinomial_n_b(X_test, X_train, y_test, y_train)
    manual_n_b(train_dir, test_dir, output_file='classification.dsv')


def manual_n_b(train_dir, test_dir, output_file='classification.dsv'):
    print("Using manual nb")
    labeled = read_truth_dsv(train_dir, 'truth.dsv')
    clf = NaiveBayes()
    X, y = clf.samples(labeled, train_dir)
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
    clf.fit(X_train, y_train)
    predictions = clf.predict(X_test)
    c_m(predictions, y_test, clf.classes)


def main():
    parser = setup_arg_parser()
    args = parser.parse_args()

    print('Training data directory:', args.train_path)
    print('Testing data directory:', args.test_path)
    print('Output file:', args.o)
    if args.k is not None:
        print(f"Running k-NN classifier with k={args.k}")
        # TODO Train and test the k-NN classifier
    elif args.b:
        print("Running Naive Bayes classifier")
        n_b(args.train_path, args.test_path, output_file=args.o)


if __name__ == "__main__":
    # python classifier.py -b ./train_1000_28 ./test_data
    main()
    sys.exit(0)
