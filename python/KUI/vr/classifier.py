import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image
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


def n_b_sample():
    rng = np.random.RandomState(1)
    X = rng.randint(5, size=(6, 100))
    y = np.array([1, 2, 3, 4, 5, 6])
    clf = MultinomialNB()
    clf.fit(X, y)
    MultinomialNB()
    print(clf.predict(X[2:3]))


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


if __name__ == "__main__":
    # main()
    i1 = 'train_700_28/img_0000.png'
    i2 = 'train_700_28/img_0001.png'
    # image_distance(i1, i2)
    # sys.exit(1)
    # img_dir = 'train_1000_10'  # 10x10 8 bit
    # labeled = read_truth_dsv(img_dir, 'truth.dsv')
    # label_cnt, grey_cnt = likelihoods(labeled, img_dir, 10*10, 8)

    # shape (28,28,4)
    img_dir = 'train_700_28'  # 28x28 = 784 32 bit
    labeled = read_truth_dsv(img_dir, 'truth.dsv')
    label_cnt, grey_cnt = likelihoods(labeled, img_dir, 28*28*4, 8)
    for lbl in label_cnt.nonzero()[0]:
        print("{}: count={}".format(chr(lbl), label_cnt[lbl]))
        # nonzero [pixel,grey]
        n_z_lbl_pix = grey_cnt[lbl].nonzero()
        nz_greys = n_z_lbl_pix[0].nonzero()
    sys.exit(0)
