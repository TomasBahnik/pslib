import sys

files = ['maze1.txt', 'maze2.txt', 'maze3.txt']

reseni = ['', '', '', ]


def load_matrix(file):
    pole = []
    with open(file, 'r') as f:
        for line in f:
            pole.append(list(map(int, line.split())))
    return pole


def test_maze(file):
    print(file)
    board = load_matrix(file)
    print(board)


def all_test():
    for f in files:
        test_maze(f)


if __name__ == '__main__':
    all_test()
    sys.exit(0)

