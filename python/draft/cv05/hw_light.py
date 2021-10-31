# Piskvorky - find where to put cross to win i.e. 5 crosses in vertical, horizontal or diagonal direction
# 1st arg is n x n array (square matrix granted by assigment)

import sys

empty = 0
cross = 1
circle = 2


def load_matrix(file):
    pole = []
    with open(file, 'r') as f:
        for line in f:
            pole.append(list(map(int, line.split())))
    return pole


def last_cross_missing(sequence):
    s = sum(sequence)
    cnt_empty = sequence.count(empty)
    cnt_cross = sequence.count(cross)
    # len must be 5 = 4 crosses (1) and 1 empty (0) and sum must be 4
    # search all sub sequences of length 5
    if s != 4: return False
    if cnt_empty == 1 and cnt_cross == 4:
        return True
    else:
        return False


def sub_seq_of_length(sequence, row, length=5):
    """ sub sequences of given length """
    l_s = len(sequence)  # sequence is modified by poping last item at the end
    if l_s <= length:  # l_s - length <= 0
        print("ERROR length of sequence < = length. Length = {}, seq length={}".format(length, l_s))
        return
    for j in range(0, l_s - length + 1):  # j <= l_s - length
        sub_seq = sequence[j:j + length]
        if last_cross_missing(sub_seq):
            print("indexes {}{} , sub seq {}".format(sub_seq.index(empty), row, sub_seq))


# TODO for transposed row <-> column and len - row
def search_rows(matrix):
    for row in range(0, len(matrix)):
        sub_seq_of_length(matrix[row], row)


def transpose_matrix(matrix):
    matrix_transposed = []
    l = len(matrix)
    for row in range(0, l):
        r_t = []
        for column in range(0, l):
            r_t += [matrix[column][row]]
        matrix_transposed += [r_t]
    return matrix_transposed


if __name__ == '__main__':
    file_with_matrix = sys.argv[1]
    matrix = load_matrix(file_with_matrix)
    t_m = transpose_matrix(matrix)
    print("Search matrix ...")
    search_rows(matrix)
    print("Search transposed matrix ...")
    search_rows(t_m)
    sys.exit(0)
