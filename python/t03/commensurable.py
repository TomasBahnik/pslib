# input 2 integers
# output a < 2  or b < 2 or a = b : 'ERROR'
# table  n x m : min(a,b) <= m,n, <= max(a,b)
import sys

from common.functions import gcd_euclid, prime

soudelna_symbol = 'x'
prvocisla_symbol = 'p'
mezera = ' '
separator = '|'


def soudelna(a, b):
    if gcd_euclid(a, b) > 1:
        return True
    return False


def prepare_table(n, m):
    if n < 2 or m < 2 or n == m:
        return 'ERROR'
    table = []
    for i in range(n, m + 1):  # row <n,m> i.e m inclusive
        row = []  # new row
        for j in range(n, m + 1):  # add letter to table[i,j] position according to type
            if soudelna(i, j):
                row += [soudelna_symbol]
            elif prime(i) or prime(j):
                row += [prvocisla_symbol]
            else:
                row += [mezera]
        table += [row]
    return table


def print_table(table):
    if type(table) is str:
        print(table)
    elif type(table) is list:
        for row in table:
            print(row)
    else:
        print('Unknown type {}'.format(type(table)))


def test(vstup):
    print('\nInput {}'.format(vstup))
    print_table(prepare_table(min(vstup), max(vstup)))


if __name__ == '__main__':
    test([2, 10])
    test([11, 10])
    test([2, 1])
    sys.exit(0)
