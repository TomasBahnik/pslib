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

from draft.shared.matrices import load_matrix


def test_rows_columns(matrix):
    print("rows ...")
    print("columns ...")


def test_diagonals(matrix, down=True):
    print("diagonals ..")


if __name__ == '__main__':
    file_with_matrix = sys.argv[1]
    matrix = load_matrix(file_with_matrix)
    test_rows_columns(matrix)
    # print("diagonals down ...")
    test_diagonals(matrix, down=True)
    # print("diagonals up ...")
    test_diagonals(matrix, down=False)
    sys.exit(0)
