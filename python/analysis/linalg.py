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
    matrix = Matrix([[1, 1, 1, 1, 0], [1, -1, -1, 0, 0], [1, 1, -1, -1, -1], [2, 2, 0, 0, -1], [1, 1, 5, 5, 2]])
    b = Matrix([3, 4, 5, 8, -1])
    det_a = matrix.det()
    particular = linsolve((matrix, b), [p_1, p_2, p_3, p_4, p_5])
    print("\\mA={} \\\\".format(latex(matrix)))
    print("det(A)={}={} \\\\".format(latex(det_a), latex(factor(det_a))))
    print("p={}".format(latex(particular)))
    # kernel
    b = Matrix([0, 0, 0, 0, 0])
    kernel = linsolve((matrix, b), [p_1, p_2, p_3, p_4, p_5])
    print("ker={}".format(latex(kernel)))


def cv9():
    matrix = Matrix([[a, 1, 1, 1], [1, a, 1, 1], [1, 1, a, 1], [1, 1, 1, a]])
    b = Matrix([1, 1, 1, 1])
    det_a = matrix.det()
    particular = linsolve((matrix, b), [p_1, p_2, p_3, p_4])
    print("\\mA={} \\\\".format(latex(matrix)))
    print("det(A)={}={} \\\\".format(latex(det_a), latex(factor(det_a))))
    print("p={}".format(latex(particular)))
    # kernel
    b = Matrix([0, 0, 0, 0])
    kernel = linsolve((matrix, b), [p_1, p_2, p_3, p_4])
    print("ker={}".format(latex(kernel)))


def matrices():
    m_a = Matrix([[34, 22, 19, 12], [72, 87, 162, 122], [69, 69, 420, 89]])
    print(latex(m_a))
    m_a_transposed = m_a.T
    print(latex(m_a_transposed))


if __name__ == '__main__':
    init_printing()  # doctest: +SKIP
    # matrices()
    print("\nCviceni 9")
    cv9()
    print("\nProblem 8.1.2")
    p812()
    sys.exit(0)
