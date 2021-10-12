# Napište program root.py který metodou půlení intervalu spočítá kořen polynomu 5-tého stupně
# -100 < koren < 100 zadani
import sys


def f(x):
    y = a5 * x ** 5 + a4 * x ** 4 + a3 * x ** 3 + a2 * x ** 2 + a1 * x + a0
    return y


# a5 = float(input())
# a4 = float(input())
# a3 = float(input())
# a2 = float(input())
# a1 = float(input())
# a0 = float(input())

# # root = 100 (upper bound - zadna iterace)
a0 = -700
a1 = 8
a2 = 0
a3 = 0
a4 = 0
a5 = 0

# 3 odmocnina a3 * x ** 3 + a0 = 0
# x**3 - 27 = 0
# a0 = -44565
# a1 = 0
# a2 = 0
# a3 = 1
# a4 = 0
# a5 = 0

# podle zadani
x1 = -100
x2 = 100

eps = 0.00000001
xp = 0
step = 0
# TODO muzu pouzit abs ??
while abs(x1 - x2) >= eps:
    xp = (x1 + x2) / 2
    # step += 1 # step = step + 1
    # acc = abs(x1 - x2)
    # print("{} : {}, eps {}".format(step, acc, eps))
    if f(xp) < 0:
        x1 = xp
    else:  # tady uz je f(xp) >= 0
        x2 = xp

# print("f({}) = {}".format(xp, f(xp)))
print(xp)
sys.exit(0)
