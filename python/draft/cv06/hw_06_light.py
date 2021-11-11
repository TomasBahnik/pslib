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
"""

import sys

from draft.shared.matrices import load_char_matrix, diagonals, column, search_char_in_rows_columns, char_in_list


def test_rows_columns(matrix, words):
    print("rows ...")
    for chars in words:
        for char in chars:
            search_char_in_rows_columns(matrix, char)
    print("columns ...")
    for chars in words:
        for char in chars:
            search_char_in_rows_columns(matrix, char, row=False)


def test_diagonals(matrix, words):
    # print("diagonals right-top to left-bottom ...")
    # diagonals(matrix, 3, down=True)
    print("diagonals left-top - right-bottom...")
    # columns = len(matrix[0])
    # rows = len(column(matrix, 0))
    # r_up = range(-rows + 1, rows)
    details = diagonals(matrix, 0, down=False)
    search_in = details[0]
    for chars in words:
        for char in chars:
            char_in_list(char, search_in)


def empty_matrix(rows, columns):
    r = [0] * columns
    ret = [r] * rows
    return ret


if __name__ == '__main__':
    file_with_matrix = sys.argv[1]
    file_with_words = sys.argv[2]
    matrix = load_char_matrix(file_with_matrix)
    words = load_char_matrix(file_with_words)
    matrix_columns = len(matrix[0])
    matrix_rows = len(column(matrix, 0))
    print("matrix rows x columns = {}x{}".format(matrix_rows, matrix_columns))
    e_m = empty_matrix(matrix_rows, matrix_columns)
    # test_rows_columns(matrix, words)
    test_diagonals(matrix, words)
    sys.exit(0)
