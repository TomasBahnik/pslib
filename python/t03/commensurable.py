# input 2 integers
# output a < 2  or b < 2 or a = b : 'ERROR'
# table  n x m : min(a,b) <= m,n, <= max(a,b)
import sys

soudelna = 'x'
prvocisla = 'p'
mezera = ' '
separator = '|'


def prepare_table(n, m):
    table = []
    for i in range(0, n):  # row
        row = []
        for j in range(0, m):  # column
            row += [i, j]
        table += [row]
    return table


if __name__ == '__main__':
    # n x m table
    print(prepare_table(2, 4))
    sys.exit(0)
