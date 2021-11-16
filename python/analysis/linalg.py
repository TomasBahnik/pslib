import sys

from sympy import *

if __name__ == '__main__':
    x, y, z, t = symbols('x y z t')
    k, m, n = symbols('k m n', integer=True)
    init_printing()  # doctest: +SKIP
    A = Matrix([ [34,22,19,12], [72,87,162,122], [69,69,420,89] ])
    print(latex(A))
    AT = A.T
    print(latex(AT))
    sys.exit(0)