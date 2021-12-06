import sys

from sympy import *

latex_new_line = "\\\\"

x, y, z, t, a = symbols('x y z t a')
p_1, p_2, p_3, p_4, p_5 = symbols('p_1 p_2 p_3 p_4 p_5')
k, m, n = symbols('k m n', integer=True)


def lin_equations():
    A = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 10]])
    b = Matrix([3, 6, 9])
    linsolve((A, b), [p_1, p_2, p_3])


def matrix_properties(matrix, b, p):
    det_a = matrix.det()
    rank = matrix.rank()
    ker = matrix.nullspace()
    particular = linsolve((matrix, b), p)
    print("\\mA={} {}".format(latex(matrix), latex_new_line))
    print("det(A)={}={} {}".format(latex(det_a), latex(factor(det_a)), latex_new_line))
    print("p={} {}".format(latex(particular), latex_new_line))
    print("kernel={} {}".format(latex(ker), latex_new_line))
    print("rank={} {}".format(rank, latex_new_line))
    # homogenni rovnice
    b = Matrix([0, 0, 0, 0, 0])
    homog_sol = linsolve((matrix, b), p)
    print("solution (b=0)={}".format(latex(homog_sol)))


matrix_p812 = Matrix([[1, 1, 1, 1, 0], [1, -1, -1, 0, 0], [1, 1, -1, -1, -1], [2, 2, 0, 0, -1], [1, 1, 5, 5, 2]])
b_p812 = Matrix([3, 4, 5, 8, -1])
symbols_p812 = [p_1, p_2, p_3, p_4, p_5]


def p812():
    matrix_properties(matrix_p812, b_p812, symbols_p812)


matrix_cv9 = Matrix([[a, 1, 1, 1], [1, a, 1, 1], [1, 1, a, 1], [1, 1, 1, a]])
b_cv9 = Matrix([1, 1, 1, 1])
symbols_cv9 = [p_1, p_2, p_3, p_4]


def cv9():
    matrix_properties(matrix_cv9, b_cv9, symbols_cv9)


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
