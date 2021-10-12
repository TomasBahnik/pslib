# Napište program root.py který metodou půlení intervalu spočítá kořen polynomu 5-tého stupně
# -100 < koren < 100 zadani
import sys

a0 = 23
a1 = -12.456
a2 = 5
a3 = 0.456
a4 = 3.14
a5 = 34.678

# # root = 100 (upper bound - zadna iterace)
# a0 = -800
# a1 = 8
# a2 = 0
# a3 = 0
# a4 = 0
# a5 = 0

# podle zadani
x1 = -100
x2 = 100


def f(x):
    y = a5 * x ** 5 + a4 * x ** 4 + a3 * x ** 3 + a2 * x ** 2 + a1 * x + a0
    return y


def check_root(a):
    if f(a) == 0:
        print("Root = {}".format(a))
        return True
    return False


# co kdyby nebyl potreba zadny vypocet
if check_root(x1):
    sys.exit(0)
if check_root(x2):
    sys.exit(0)

eps = 0.000000001
xp = 0
step = 0
while abs(x1 - x2) >= eps:
    xp = (x1 + x2) / 2
    step += 1
    acc = abs(x1 - x2)
    print("{} : {}, eps {}".format(step, acc, eps))
    acc = abs(x1 - x2)
    if check_root(xp):  # resi f(xp) = 0
        break
    if f(xp) < 0:
        x1 = xp
    else:  # f(xp) > 0
        x2 = xp

print("f({}) = {}".format(xp, f(xp)))
sys.exit(0)
