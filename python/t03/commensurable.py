# input 2 integers
# output a < 2  or b < 2 or a = b : 'ERROR'
# table  n x m : min(a,b) <= m,n, <= max(a,b)
import sys

from common.functions import prime, gcd2

soudelna_symbol = 'x'
prvocisla_symbol = 'p'
mezera = ' '
separator = '|'


def soudelna(a, b):
    if gcd2(a, b) > 1:
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


def array_to_string(array, print_line=True):
    line = ''
    for i in range(0, 2 * len(array) - 1):
        line += '-'
    a0 = str(array)
    a1 = a0.replace('[', '').replace(']', '')
    a2 = a1.replace(',', '|').replace('| ', '|')
    a3 = a2.replace("'", '')
    print_table(a3)
    if print_line:
        print(line)


def print_table(table):
    if type(table) is str:
        print(table)
    elif type(table) is list:
        num_rows = len(table)
        for i in range(0, num_rows):
            if i < num_rows - 1:
                array_to_string(table[i], print_line=True)
            else:  # do not print last line
                array_to_string(table[i], print_line=False)

    else:
        print('Unknown type {}'.format(type(table)))


def test(vstup):
    print('\nInput {}'.format(vstup))
    print_table(prepare_table(min(vstup), max(vstup)))


if __name__ == '__main__':
    test([2, 10])
    test([11, 10])
    test([2, 1])
    test([2, 23])
    sys.exit(0)
