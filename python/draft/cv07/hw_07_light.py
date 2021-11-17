import sys
from timeit import default_timer as timer

n = int(input())
x = float(input())
DEBUG_PRINTS = True


def debug_print(message):
    if DEBUG_PRINTS:
        print(message)


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


def r(m, y):
    l = len(hint)
    if m < l:
        return hint[m]
    else:
        r(m - 1, y)  # recursion
        r_m = (1 / m) * hint[m - 1] + (-1) ** m * (m / (m + 1)) * hint[m - 2] + (m - 1) / y * hint[m - 3]
        hint.append(r_m)
        return r_m


# 8 decimals
# n=5, x=1.5  : -3.2468055555555555 expected -3.246805555555556
# n=20, x=-1.5, : -212609.03633822594 expected -212609.036338226
if __name__ == '__main__':
    if x == 0:
        print("error x nemuze byt".format(x))
        sys.exit(1)

    init_hint(x)
    debug_print("Initial values of function={}".format(hint))
    start = timer()
    result = r(n, x)
    end = timer()
    debug_print('Elapsed time = {} sec'.format(end - start))
    debug_print("R_{}({}) = {}".format(n, x, result))
    debug_print("Rounded to 8 decimals : %.8f" % result)
    print(result)
