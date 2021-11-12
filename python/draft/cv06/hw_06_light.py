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

found_words = []


# TODO search for substrings in given directions
#  and for substring start index end index or length
#  for diagonals and columns ensure the search in right direction
#  left -> right, top -> down, left-top -> right-bottom
def find_word(search_in, words, start_idx, diagonal=False):
    # TODO no need to use list for rows, only for columns and diagonals
    search_in_str = ''.join(search_in)
    for word in words:
        lowest_idx = search_in_str.find(word)
        if lowest_idx != -1:
            # shift to right for diag to get actual start position of word
            start_idx = start_idx if not diagonal else start_idx + lowest_idx
            print("word '{}' : lowest_idx = {},  start at = [{},{}]"
                  .format(word, lowest_idx, start_idx, lowest_idx))
            found_words.append(word)


def test_rows_columns(matrix, words):
    print("rows ...")
    l = len(column(matrix, 0))
    for idx in range(0, l):
        search_in = matrix[idx]
        find_word(search_in, words, idx)
    print("columns ...")
    l = len(matrix[0])
    for idx in range(0, l):
        search_in = column(matrix, idx)
        find_word(search_in, words, idx)


def test_diagonals(matrix, words):
    # print("diagonals right-top to left-bottom ...")
    # diagonals(matrix, 3, down=True)
    columns = len(matrix[0])
    rows = len(column(matrix, 0))
    diff_range = range(-columns + 1, rows)
    print("diagonals left-top - right-bottom, {}".format(diff_range))
    for diff in diff_range:
        details = diagonals(matrix, diff, down=False)
        search_in = details[0]  # diagonal sequence
        row_start_idx = details[1]  # diagonal start coordinates - row
        col_start_idx = details[2]  # diagonal start coordinates - col
        find_word(search_in, words, row_start_idx, diagonal=True)


def empty_matrix(rows, columns):
    r = [0] * columns
    ret = [r] * rows
    return ret


def remove_words(m, f_w):
    for word in f_w:
        print("\n*** {}".format(word))
        for i in range(0, len(m)):
            m[i] = ([char for char in m[i] if char not in word])
    return m


if __name__ == '__main__':
    file_with_matrix = sys.argv[1]
    file_with_words = sys.argv[2]
    matrix = load_char_matrix(file_with_matrix)
    # TODO keep words as list of strings
    words = load_lines_matrix(file_with_words)
    matrix_columns = len(matrix[0])
    matrix_rows = len(column(matrix, 0))
    print("matrix rows x columns = {}x{}".format(matrix_rows, matrix_columns))
    test_rows_columns(matrix, words)
    test_diagonals(matrix, words)
    print(found_words)
    sys.exit(0)
