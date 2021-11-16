# n = int(input())
import sys

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


def r3(y):
    return 1 / 3 * r2(y) + (-1) ** 3 * r1(y) + 2 / y * r0()


if x == 0:
    print("error x nemuze byt".format(x))
    sys.exit(1)

init_hint(x)
print(hint)
print(r3(x))
