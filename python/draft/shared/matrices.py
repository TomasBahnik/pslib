def load_int_matrix(file):
    pole = []
    with open(file, 'r') as f:
        for line in f:
            pole.append(list(map(int, line.split())))
    return pole


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


def search_word_in_rows_columns(matrix, word, row=True):
    l = len(column(matrix, 0)) if row else len(matrix[0])
    for idx in range(0, l):
        search_in = matrix[idx] if row else column(matrix, idx)
        if search_in == word:
            print("word {} found".format(word))


def char_in_list(char, search_in):
    found = char in search_in
    if found:
        position = search_in.index(char)
        print("Char '{}' found in {} at index {}".format(char, search_in, position))
