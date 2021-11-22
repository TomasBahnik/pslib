def load_lines_matrix(file):
    pole = []
    with open(file, 'r') as f:
        for line in f:
            pole.append(line.rstrip())
    return pole


def load_char_matrix(file):
    pole = []
    with open(file, 'r') as f:
        for line in f:
            chars = [char for char in line.rstrip()]
            pole.append(chars)
    return pole


def column(matrix, i):
    return [row[i] for row in matrix]


# down=True means right-top to left-bottom
# down=False means left-top right-bottom used by hw_06_light.py
def diagonals(matrix, shift, down=True):
    matrix_columns = len(matrix[0])
    matrix_rows = len(column(matrix, 0))
    # matrix needs not to be square
    row_range = range(0, matrix_rows)
    col_range = range(0, matrix_columns)
    seq = []  # for each s new seq
    # initialized only once for given shift
    seq_row_start_idx = None
    seq_col_start_idx = None
    if down:
        for i in row_range:
            for j in col_range:
                if (i + j) == shift:  # sum of indexes is equal
                    print("index sum {} : [{},{}] = {}".format(shift, i, j, matrix[i][j]))
                    if seq_row_start_idx is None:
                        seq_row_start_idx = i
                    if seq_col_start_idx is None:
                        seq_col_start_idx = j
                    seq.append(matrix[i][j])
    else:
        for i in row_range:
            for j in col_range:
                if i - j == shift:  # difference of indexes is equal and can be negative zero (main diag) or positive
                    # print("index diff={} : [{},{}] = {}".format(shift, i, j, matrix[i][j]))
                    if seq_row_start_idx is None:
                        seq_row_start_idx = i
                    if seq_col_start_idx is None:
                        seq_col_start_idx = j
                    seq.append(matrix[i][j])
    return seq, seq_row_start_idx, seq_col_start_idx, down

import sys

found_word_ranges = []

RANGE_TYPE_ROWS = 0
RANGE_TYPE_COLS = 1
RANGE_TYPE_DIAG = 2

DEBUG_PRINTS = False


# TODO search for substrings in given directions
#  and for substring start index end index or length
#  for diagonals and columns ensure the search in right direction
#  left -> right, top -> down, left-top -> right-bottom
def find_word(search_in, words, row_start_idx, col_start_idx=0, rows=True, diagonal=False):
    # convert list to string
    search_in_str = ''.join(search_in)
    for word in words:
        lowest_idx = search_in_str.find(word)
        if lowest_idx != -1:
            length_of_word = len(word)
            if diagonal:
                # shift to right for diag to get actual start position of word
                start_idx_row = row_start_idx + lowest_idx
                # for diagonals started at top - > left diagonal
                start_idx_col = lowest_idx + col_start_idx
                end_idx_row = start_idx_row + length_of_word - 1
                end_idx_col = start_idx_col + length_of_word - 1
                shift_start = start_idx_row - start_idx_col
                shift_end = end_idx_row - end_idx_col
                range_type = RANGE_TYPE_DIAG
                if shift_start != shift_end:
                    print("ERROR diag shifts {} != {}".format(shift_start, shift_end))
            elif rows:
                # valid for rows, for columns interchange
                start_idx_row = row_start_idx
                start_idx_col = lowest_idx
                end_idx_row = start_idx_row
                end_idx_col = lowest_idx + length_of_word - 1
                range_type = RANGE_TYPE_ROWS
                if start_idx_row != end_idx_row:
                    print("ERROR rows {} != {}".format(start_idx_row, end_idx_row))
            else:  # columns
                # valid for columns
                start_idx_row = lowest_idx
                start_idx_col = row_start_idx
                end_idx_row = start_idx_row + length_of_word - 1
                end_idx_col = start_idx_col
                range_type = RANGE_TYPE_COLS
                if start_idx_col != end_idx_col:
                    print("ERROR columns {} != {}".format(start_idx_col, end_idx_col))
            # TODO provide whole range as (row,col) pairs use list comprehension
            #  [(x, y) for x in [1,2,3] for y in [3,1,4] if x != y] according to type (row, col, diag)
            #  row = [(r, c) for r in [0] for c in [3,1,4]]
            #  col = [(r, c) for r in [0,1,2,3] for c in [3]]
            #  how to do that for diag ??
            #  easy to delete range type becomes obsolete
            idx_range = [range_type, start_idx_row, start_idx_col, end_idx_row, end_idx_col]
            if DEBUG_PRINTS:
                print("word '{}' : range = [{},{}] - [{},{}], length={}, lowest_idx={}"
                      .format(word, start_idx_row, start_idx_col, end_idx_row, end_idx_col, length_of_word, lowest_idx))
            # found_words.append(word)
            found_word_ranges.append(idx_range)


def delete_range(matrix, idx_range):
    range_type = idx_range[0]
    start_row = idx_range[1]
    start_col = idx_range[2]
    end_row = idx_range[3]
    end_col = idx_range[4]
    if range_type == RANGE_TYPE_ROWS:
        for c in range(start_col, end_col + 1):
            matrix[start_row][c] = ''
    elif range_type == RANGE_TYPE_COLS:
        for r in range(start_row, end_row + 1):
            matrix[r][start_col] = ''
    else:
        s = end_row - start_row
        for r in range(0, s + 1):
            matrix[start_row + r][start_col + r] = ''


def test_delete(matrix):
    # moniko
    delete_range(matrix, [RANGE_TYPE_COLS, 1, 0, 6, 0])
    # brblalo
    delete_range(matrix, [RANGE_TYPE_ROWS, 0, 3, 0, 9])
    # zadu [3,1] - [6,4]
    delete_range(matrix, [RANGE_TYPE_DIAG, 3, 1, 6, 4])


def test_rows_columns(matrix, words):
    if DEBUG_PRINTS:
        print("\nrows ...")
    l = len(column(matrix, 0))
    for idx in range(0, l):
        search_in = matrix[idx]
        find_word(search_in, words, idx)
    if DEBUG_PRINTS:
        print("\ncolumns ...")
    l = len(matrix[0])
    for idx in range(0, l):
        search_in = column(matrix, idx)
        find_word(search_in, words, idx, rows=False)


def test_diagonals(matrix, words):
    # print("diagonals right-top to left-bottom ...")
    # diagonals(matrix, 3, down=True)
    columns = len(matrix[0])
    rows = len(column(matrix, 0))
    diff_range = range(-columns + 1, rows)
    if DEBUG_PRINTS:
        print("\ndiagonals left-top - right-bottom, {}".format(diff_range))
    for diff in diff_range:
        details = diagonals(matrix, diff, down=False)
        search_in = details[0]  # diagonal sequence
        row_start_idx = details[1]  # diagonal start coordinates - row
        col_start_idx = details[2]  # diagonal start coordinates - col
        find_word(search_in, words, row_start_idx, col_start_idx, diagonal=True)


if __name__ == '__main__':
    file_with_matrix = sys.argv[1]
    file_with_words = sys.argv[2]
    matrix = load_char_matrix(file_with_matrix)
    # print(matrix)
    words = load_lines_matrix(file_with_words)
    # matrix_columns = len(matrix[0])
    # matrix_rows = len(column(matrix, 0))
    # print("matrix rows x columns = {}x{}".format(matrix_rows, matrix_columns))
    test_rows_columns(matrix, words)
    test_diagonals(matrix, words)
    # print(found_word_ranges)
    for found_range in found_word_ranges:
        delete_range(matrix, found_range)
    # join individual rows and add them to list of strings using list comprehension
    result_list = [''.join(r) for r in matrix]
    if DEBUG_PRINTS:
        print("\n*** Result ***")
    # join all rows to single string
    print(''.join(result_list))
    sys.exit(0)