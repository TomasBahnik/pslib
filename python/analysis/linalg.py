import sys

from sympy import *

x, y, z, t = symbols('x y z t')
k, m, n = symbols('k m n', integer=True)


def cv9():
    cv9_matrix = Matrix([[x, 1, 1, 1], [1, x, 1, 1], [1, 1, x, 1], [1, 1, 1, x]])
    det_cv09 = cv9_matrix.det()
    f_p = factor(det_cv09)
    print(latex(cv9_matrix))
    print(latex(det_cv09))
    print(latex(f_p))


def matrices():
    m_a = Matrix([[34, 22, 19, 12], [72, 87, 162, 122], [69, 69, 420, 89]])
    print(latex(m_a))
    m_a_transposed = m_a.T
    print(latex(m_a_transposed))


if __name__ == '__main__':
    init_printing()  # doctest: +SKIP
    # matrices()
    cv9()
    sys.exit(0)
