import sys

n = int(input())
x = float(input())

hint = []


def r0():
    return -1


def r1(y):
    return y


def r2(y):
    return -y ** 2


def init_hint(y):
    hint.append(r0())
    hint.append(r1(y))
    hint.append(r2(y))


def r(y, m):
    if m < len(hint):
        return hint[m]
    return 1 / m * hint[m - 1] + (-1) ** m * hint[m - 2] + (m - 1) / y * hint[m - 3]


if x == 0:
    print("error x nemuze byt".format(x))
    sys.exit(1)

init_hint(x)
print(hint)
print("r{}({}) = {}".format(n, x, r(x, n)))
