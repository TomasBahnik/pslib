import argparse
import sys

import numpy as np
from PIL import Image


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
    i1 = 'train_1000_10/img_1112.png'
    i2 = 'train_1000_10/img_1112.png'
    image_distance(i1, i2)
    sys.exit(0)
