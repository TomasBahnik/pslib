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
    for i in range(n, m + 1):  # row
        row = []
        for j in range(n, m + 1):  # column
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
        i = 1
        for row in table:
            print('{}. {}'.format(i, row))
            i += 1
    else:
        print('Unknown type {}'.format(type(table)))


if __name__ == '__main__':
    vstup = [2, 10]
    print(vstup)
    print_table(prepare_table(min(vstup), max(vstup)))

    vstup = [11, 10]
    print(vstup)
    print_table(prepare_table(min(vstup), max(vstup)))

    vstup = [2, 1]
    print(vstup)
    print_table(prepare_table(min(vstup), max(vstup)))
    sys.exit(0)
