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

from draft.shared.matrices import load_char_matrix, diagonals, column

found_words = []


def test_rows_columns(matrix, words):
    print("rows ...")
    for word in words:
        l = len(column(matrix, 0))
        for idx in range(0, l):
            search_in = matrix[idx]
            if search_in == word:
                print("word {} found".format(word))
                found_words.append(word)
    print("columns ...")
    for word in words:
        l = len(matrix[0])
        for idx in range(0, l):
            search_in = column(matrix, idx)
            if search_in == word:
                print("word {} found".format(word))
                found_words.append(word)


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
        for word in words:
            if search_in == word:
                print("word {} found".format(word))
                found_words.append(word)


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
    test_rows_columns(matrix, words)
    test_diagonals(matrix, words)
    # print(found_words)
    for word in found_words:
        print("\n*** {}".format(word))
        for row in matrix:
            print([char for char in row if char not in word])
    sys.exit(0)
