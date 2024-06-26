import sys

from sympy import *

if __name__ == '__main__':
    x, y, z, t = symbols('x y z t')
    k, m, n = symbols('k m n', integer=True)
    init_printing()  # doctest: +SKIP
    a = Integral(x * x, x)
    pprint(a)
    print(latex(a))
    res = Eq(a, a.doit())
    print(latex(res))
    expr = (x + y) ** 5
    print(expand(expr))
    print(latex(expand(expr)))
    a = Integral(sin(x) ** 2, x)
    res = Eq(a, a.doit())
    c = Integral(expr, x)
    print(latex(res))
    res = Eq(c, c.doit())
    print(latex(res))
    sys.exit(0)
