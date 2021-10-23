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
    for row in table:
        print(row)


if __name__ == '__main__':
    i = 1
    for row in prepare_table(2, 10):
        print('{}. {}'.format(i, row))
        i += 1
    sys.exit(0)
