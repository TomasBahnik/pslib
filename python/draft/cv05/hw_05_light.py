# Piskvorky - find where to put cross to win i.e. 5 crosses in vertical, horizontal or diagonal direction
# 1st arg is n x n array (square matrix granted by assigment)

import sys

from draft.shared.matrices import diagonals, load_int_matrix, column

empty = 0
cross = 1
circle = 2
# how many solution is enough
enough_num_of_solutions = 10
# num_of_solutions <= enough_num_of_solutions
num_of_solutions = 0


def last_cross_missing(sequence):
    s = sum(sequence)
    cnt_empty = sequence.count(empty)
    cnt_cross = sequence.count(cross)
    # len must be 5 = 4 crosses (1) and 1 empty (0) and sum must be 4
    # search all sub sequences of length 5
    if s != 4:
        return False
    if cnt_empty == 1 and cnt_cross == 4:
        return True
    return False


def sub_seq_of_length(sequence, length=5):
    """ sub sequences of given length """
    l_s = len(sequence)
    if l_s < length:  # l_s - length < 0
        # print("ERROR length of sequence < = length. Length = {}, seq length={}".format(length, l_s))
        return
    for j in range(0, l_s - length + 1):  # j <= l_s - length
        sub_seq = sequence[j:j + length]
        if last_cross_missing(sub_seq):
            # add j because we need empty idx counted from the original sequence
            empty_idx = sub_seq.index(empty) + j
            # print("{} : cross at {} in {} wins! piskvorka = {} ".format(sys.argv[1], empty_idx, sequence, sub_seq))
            return empty_idx


def print_output(row, col):
    global num_of_solutions
    if num_of_solutions < enough_num_of_solutions:
        print(row, col)
        num_of_solutions += 1
    else:
        return


def search_for_piskvorka(matrix, row=True):
    l = len(matrix)
    for idx in range(0, l):
        empty_idx = sub_seq_of_length(matrix[idx]) if row else sub_seq_of_length(column(matrix, idx))
        if empty_idx is not None:
            cross_row_idx = idx if row else empty_idx
            cross_col_idx = empty_idx if row else idx
            # print("(cross_row_idx, cross_col_idx) = {} {}".format(cross_row_idx, cross_col_idx))
            # Main output - just 2 indexes
            print_output(cross_row_idx, cross_col_idx)


def cross_diag_seq(seq_details):
    seq = seq_details[0]
    seq_row_start_idx = seq_details[1]
    seq_col_start_idx = seq_details[2]
    down = seq_details[3]
    empty_idx = sub_seq_of_length(seq)
    if empty_idx is not None:
        # print("shift={}, shift_p={}, empty_idx {}, seq_diag {}".format(shift, shift_p, empty_idx, seq))
        # there is no common solution for both diagonals
        # either row OR column can grow not both in both directions !!
        cross_row_idx = empty_idx + seq_row_start_idx
        cross_col_idx = seq_col_start_idx - empty_idx if down else seq_col_start_idx + empty_idx
        # print("(seq_row_start_idx, seq_col_start_idx) | empty_idx) = {} {} | {}"
        #       .format(seq_row_start_idx, seq_col_start_idx, empty_idx))
        # print("(cross_row_idx, cross_col_idx) = {} {}".format(cross_row_idx, cross_col_idx))
        if matrix[cross_row_idx][cross_col_idx] != 0:
            print("ERROR !!! element at [{}][{}] is not empty = {}".format(cross_row_idx, cross_col_idx, empty))
        # Main output - just 2 indexes
        print_output(cross_row_idx, cross_col_idx)


def test_diagonals(matrix, down=True):
    l = len(matrix)
    r_down = range(0, 2 * l - 1)
    r_up = range(-l + 1, l)
    # print("matrix length = {}".format(l))
    if down:
        for k in r_down:
            seq_details = diagonals(matrix, k, down)
            cross_diag_seq(seq_details)
            # print("{} : {}".format(k, seq))
    else:
        for k in r_up:
            seq_details = diagonals(matrix, k, down)
            cross_diag_seq(seq_details)
            # print("{} : {}".format(k, seq))


def test_rows_columns(matrix):
    # print("rows ...")
    search_for_piskvorka(matrix)
    # print("columns ...")
    search_for_piskvorka(matrix, row=False)


if __name__ == '__main__':
    file_with_matrix = sys.argv[1]
    matrix = load_int_matrix(file_with_matrix)
    test_rows_columns(matrix)
    # print("diagonals down ...")
    test_diagonals(matrix, down=True)
    # print("diagonals up ...")
    test_diagonals(matrix, down=False)
    sys.exit(0)
