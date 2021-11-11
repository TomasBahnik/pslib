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


def test_rows_columns(matrix):
    print("rows ...")
    print("columns ...")


def test_diagonals(matrix, down=True):
    print("diagonals ..")
    diagonals(matrix, 3, down)


if __name__ == '__main__':
    file_with_matrix = sys.argv[1]
    file_with_words = sys.argv[2]
    matrix = load_char_matrix(file_with_matrix)
    words = load_char_matrix(file_with_words)
    print("matrix indexes : {}x{}".format(len(matrix[0]) - 1, len(column(matrix, 0)) - 1))
    test_rows_columns(matrix)
    # print("diagonals down ...")
    test_diagonals(matrix, down=True)
    # print("diagonals up ...")
    test_diagonals(matrix, down=False)
    sys.exit(0)
