"""
program, který řeší trojsměrku (lehčí variantu osmisměrky). Slova ve trojsměrce jsou zapsána pouze
zleva doprava, shora dolů a diagonálně zleva shora doprava dolů

Vstup:
Jména dvou souborů zadaná na příkazové řádce.
První soubor obsahuje 2D matici písmen
Druhý soubor obsahuje slova, která jsou v trojsměrce obsažena.

Výstup:
Písmena, která zbudou po vynechání všech písmen vyskytujících se v zadaných slovech
(pozor slova se mohou křížit, je důležité nalezené slovo z matice nemazat)
Písmena tiskněte zleva doprava odshora dolů

osmismerka.txt + slova.txt => odfoukali

Overit : Vynechat by se meli NE VSECHNA pismena V CELE MATICI co se vyskytnout v nalezenych slovech, ale jen
jenom ta v mistech, kde bylo nalezene slovo - ale po nalezeni slova je nutne je ponechat v matici aby zustaly slova
co se mohou krizit - tj. udelat v miste pismena jen 'pruhlednou' znacku a teprve nakonci je mozne takto oznacene
misto smazat resp. preskocit

Je celkem 4x2 = 8 moznych smeru (v dane uloze prvni 3 bez reverse)
   * left -> right  + reverse
   * top -> down + reverse
   * left-top -> right-bottom + reverse
   * left-bottom -> right-top + reverse
"""

import sys

from draft.shared.matrices import load_char_matrix, diagonals, column, load_lines_matrix

found_word_ranges = []

RANGE_TYPE_ROWS = 0
RANGE_TYPE_COLS = 1
RANGE_TYPE_DIAG = 2


# TODO search for substrings in given directions
#  and for substring start index end index or length
#  for diagonals and columns ensure the search in right direction
#  left -> right, top -> down, left-top -> right-bottom
def find_word(search_in, words, start_idx, rows=True, diagonal=False):
    # convert list to string
    search_in_str = ''.join(search_in)
    for word in words:
        lowest_idx = search_in_str.find(word)
        if lowest_idx != -1:
            # shift to right for diag to get actual start position of word
            start_idx = start_idx if not diagonal else start_idx + lowest_idx
            length_of_word = len(word)
            if diagonal:
                start_idx_row = start_idx
                start_idx_col = lowest_idx
                end_idx_row = start_idx_row + length_of_word - 1
                end_idx_col = start_idx_col + length_of_word - 1
                shift_start = start_idx_row - start_idx_col
                shift_end = end_idx_row - end_idx_col
                range_type = RANGE_TYPE_DIAG
                if shift_start != shift_end:
                    print("ERROR diag shifts {} != {}".format(shift_start, shift_end))
            elif rows:
                # valid for rows, for columns interchange
                start_idx_row = start_idx
                start_idx_col = lowest_idx
                end_idx_row = start_idx_row
                end_idx_col = lowest_idx + length_of_word - 1
                range_type = RANGE_TYPE_ROWS
                if start_idx_row != end_idx_row:
                    print("ERROR rows {} != {}".format(start_idx_row, end_idx_row))
            else:  # columns
                # valid for columns
                start_idx_row = lowest_idx
                start_idx_col = start_idx
                end_idx_row = start_idx_row + length_of_word - 1
                end_idx_col = start_idx_col
                range_type = RANGE_TYPE_COLS
                if start_idx_col != end_idx_col:
                    print("ERROR columns {} != {}".format(start_idx_col, end_idx_col))
            # TODO provide whole range as row, col pairs use list comprehension according to type
            #  easy to delete range type becomes obsolete
            idx_range = [range_type, start_idx_row, start_idx_col, end_idx_row, end_idx_col]
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


def test_rows_columns(matrix, words):
    print("\nrows ...")
    l = len(column(matrix, 0))
    for idx in range(0, l):
        search_in = matrix[idx]
        find_word(search_in, words, idx)
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
    print("\ndiagonals left-top - right-bottom, {}".format(diff_range))
    for diff in diff_range:
        details = diagonals(matrix, diff, down=False)
        search_in = details[0]  # diagonal sequence
        row_start_idx = details[1]  # diagonal start coordinates - row
        col_start_idx = details[2]  # diagonal start coordinates - col
        find_word(search_in, words, row_start_idx, diagonal=True)


if __name__ == '__main__':
    file_with_matrix = sys.argv[1]
    file_with_words = sys.argv[2]
    matrix = load_char_matrix(file_with_matrix)
    print(matrix)
    words = load_lines_matrix(file_with_words)
    matrix_columns = len(matrix[0])
    matrix_rows = len(column(matrix, 0))
    print("matrix rows x columns = {}x{}".format(matrix_rows, matrix_columns))
    test_rows_columns(matrix, words)
    test_diagonals(matrix, words)
    print(found_word_ranges)
    for found_range in found_word_ranges:
        delete_range(matrix, found_range)
    for row in matrix:
        print(''.join(row))
    sys.exit(0)
