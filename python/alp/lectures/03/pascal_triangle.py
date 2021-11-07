# -*- coding: utf-8 -*-


def print_2d_matrix(a):
    for i in range(len(a)):
        print(a[i])


def pascal_triangle(N):
    """ Create a Pascal's triangle 'p' with 'N' rows,
        so that p[n][k] is 'n' over 'k' """
    p = [[1]]
    for n in range(2, N + 1):
        prev = p[n - 2]  # předchozí řada
        row = [1] + [prev[k - 1] + prev[k] for k in range(1, n - 1)] + [1]
        p += [row]
    return p


print_2d_matrix(pascal_triangle(5))
