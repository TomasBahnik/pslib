import sys

from sympy import *

x, y, z, t, a = symbols('x y z t a')
p_1, p_2, p_3, p_4, p_5 = symbols('p_1 p_2 p_3 p_4 p_5')
k, m, n = symbols('k m n', integer=True)
latex_new_line = '\\'


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
    if det_a == 0:
        print("determinant = 0, can't compute inverse")
    else:
        inv = matrix.inv()
        print("mA-1={} {}".format(latex(inv), latex_new_line))
    print("\\evb={} {}".format(latex(b), latex_new_line))
    print("det(A)={}={} {}".format(latex(det_a), latex(factor(det_a)), latex_new_line))
    print("p={} {}".format(latex(particular), latex_new_line))
    print("kernel={} {}".format(latex(ker), latex_new_line))
    print("rank={} {}".format(rank, latex_new_line))
    # homogenni rovnice
    b = Matrix([0, 0, 0, 0, 0])
    homog_sol = linsolve((matrix, b), p)
    print("solution (b=0)={}".format(latex(homog_sol)))


def matrix_det(m):
    det_a = m.det()
    print("{}\ndet = {}".format(m, det_a))


def p812():
    A = Matrix([[1, 1, 1, 1, 0], [1, -1, -1, 0, 0], [1, 1, -1, -1, -1], [2, 2, 0, 0, -1], [1, 1, 5, 5, 2]])
    b = Matrix([3, 4, 5, 8, -1])
    print("\\mA={}".format(latex(A)))
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
    # print("\nCviceni 9")
    # cv9()
    # print("\nProblem 8.1.2")
    # p812()
    # cv9()
    # print(latex(p812()))
    matrix = Matrix([[3, 2, 1, 0], [1, 2, 4, 2], [0, 1, 2, 2], [3, 3, 2, 1]])
    matrix_det(matrix)
    sys.exit(0)
