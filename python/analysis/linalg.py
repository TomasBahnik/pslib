import sys

from sympy import *

x, y, z, t, a = symbols('x y z t a')
p_1, p_2, p_3, p_4, p_5 = symbols('p_1 p_2 p_3 p_4 p_5')
k, m, n = symbols('k m n', integer=True)


def lin_equations():
    A = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 10]])
    b = Matrix([3, 6, 9])
    linsolve((A, b), [p_1, p_2, p_3])


def p812():
    A = Matrix([[1, 1, 1, 1, 0], [1, -1, -1, 0, 0], [1, 1, -1, -1, -1], [2, 2, 0, 0, -1], [1, 1, 5, 5, 2]])
    b = Matrix([3, 4, 5, 8, -1])
    return linsolve((A, b), [p_1, p_2, p_3, p_4, p_5])


def cv9():
    m_a = Matrix([[a, 1, 1, 1], [1, a, 1, 1], [1, 1, a, 1], [1, 1, 1, a]])
    b = Matrix([1, 1, 1, 1])
    det_a = m_a.det()
    p_s = linsolve((m_a, b), [p_1, p_2, p_3, p_4])
    print("\\mA={} \\\\".format(latex(m_a)))
    print("det(A)={}={} \\\\".format(latex(det_a), latex(factor(det_a))))
    print("p={}".format(latex(p_s)))


def matrices():
    m_a = Matrix([[34, 22, 19, 12], [72, 87, 162, 122], [69, 69, 420, 89]])
    print(latex(m_a))
    m_a_transposed = m_a.T
    print(latex(m_a_transposed))


if __name__ == '__main__':
    init_printing()  # doctest: +SKIP
    # matrices()
    cv9()
    # print(p812())
    sys.exit(0)
