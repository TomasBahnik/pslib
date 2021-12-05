import sys

from sympy import *

x, y, z, t = symbols('x y z t')
k, m, n = symbols('k m n', integer=True)


def factor_poly():
    return factor(x ** 4 - 6 * x ** 2 + 8 * x - 3)


if __name__ == '__main__':
    init_printing()  # doctest: +SKIP
    A = Matrix([[34, 22, 19, 12], [72, 87, 162, 122], [69, 69, 420, 89]])
    print(latex(A))
    AT = A.T
    print(latex(AT))
    cv9_matrix = Matrix([[x, 1, 1, 1], [1, x, 1, 1], [1, 1, x, 1], [1, 1, 1, x]])
    print(latex(cv9_matrix))
    det_cv09 = cv9_matrix.det()
    print(latex(det_cv09))
    print(latex(factor_poly()))

    sys.exit(0)
