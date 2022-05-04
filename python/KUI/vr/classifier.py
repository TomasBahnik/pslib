import argparse
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import scipy.sparse as sp
from PIL import Image
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB


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


ASCII_CHARS_COUNT = 128
GREY_COUNT = 256


def samples(labeled_data: list, folder: str, img_size: int):
    n_samples = len(labeled_data)
    n_features = img_size
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


# Multinomial NB estimates likelihoods
def likelihoods(labeled_data: list, folder: str, img_size: int, grey_bits: int):
    # Initialize likelihoods
    l_h = np.zeros([ASCII_CHARS_COUNT, img_size, 2 ** grey_bits], dtype=int)
    label_count = np.zeros([ASCII_CHARS_COUNT], dtype=int)
    for l_d in labeled_data:
        img_file = folder + '/' + l_d[0]
        img_label_ascii = ord(l_d[1])
        label_count[img_label_ascii] += 1
        image = Image.open(img_file)
        np_img = np.array(image).flatten()
        for pixel in range(len(np_img)):
            grey = np_img[pixel]
            l_h[img_label_ascii][pixel][grey] += 1
    return label_count, l_h


# TODO return
# Výsledkem klasifikátoru je soubor classification.dsv stejného formátu jako truth.dsv,
# který je umístěný v adresáři s testovacími obrázky.
def n_b(img_dir, img_size):
    # TODO what about splitting to train and test labeled
    # so classification.dsv can be created from tests
    labeled = read_truth_dsv(img_dir, 'truth.dsv')
    # files = [x[0] for x in labeled]
    # targets = [x[1] for x in labeled]
    # files_train, files_test, targets_train, targets_test = train_test_split(files, targets)
    X, y = samples(labeled, img_dir, img_size)
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
    Y = one_hot_enc(y_train)
    # multinomial_n_b(X_test, X_train, y_test, y_train)
    print(Y.shape)


def multinomial_n_b(X_test, X_train, y_test, y_train):
    clf = MultinomialNB()
    clf.fit(X_train, y_train)
    predictions = clf.predict(X_test)
    cm = confusion_matrix(y_test, predictions, labels=clf.classes_)
    disp_labels = [chr(x) for x in clf.classes_]
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=disp_labels)
    disp.plot()
    plt.show()


def unique_labels(y):
    ys = set(x for x in y)
    return np.array(sorted(ys))


def one_hot_enc(y):
    classes = unique_labels(y)
    n_samples = len(y)
    n_classes = len(classes)
    classes = np.asarray(classes)
    y_in_classes = np.in1d(y, classes)
    y_seen = y[y_in_classes]
    sorted_class = np.sort(classes)
    indices = np.searchsorted(sorted_class, y_seen)
    indptr = np.hstack((0, np.cumsum(y_in_classes)))

    data = np.empty_like(indices)
    data.fill(1)
    Y = sp.csr_matrix((data, indices, indptr), shape=(n_samples, n_classes))
    return Y.toarray()


def n_b_fit(X, y):
    _, n_features = X.shape
    Y = one_hot_enc(y)
    return Y


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
        # TODO Train and test the Naive Bayes classifier


def test_1():
    # shape (28,28,4)
    img_dir = 'train_700_28'  # 28x28 = 784 32 bit
    labeled = read_truth_dsv(img_dir, 'truth.dsv')
    label_cnt, grey_cnt = likelihoods(labeled, img_dir, 28 * 28 * 4, 8)
    for lbl in label_cnt.nonzero()[0]:
        print("{}: count={}".format(chr(lbl), label_cnt[lbl]))
        # nonzero [pixel,grey]
        n_z_lbl_pix = grey_cnt[lbl].nonzero()
        nz_greys = n_z_lbl_pix[0].nonzero()


if __name__ == "__main__":
    # label_cnt, grey_cnt = likelihoods(labeled, img_dir, 10*10, 8)
    # n_b('train_1000_10', 10 * 10)  # 10x10 8 bit
    # n_b('train_1000_28', 28 * 28)  # 28x28 8 bit
    n_b('train_700_28', 28 * 28 * 4)  # 28x28 32 bit
    sys.exit(0)
