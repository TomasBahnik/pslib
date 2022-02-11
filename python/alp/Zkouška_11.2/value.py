"""
INPUTS
0. 1. -1. 0.5
1. 0. -1. -1.5

---> 1 (idx min abs f(x,y))
     2 (idx maxminalni druhe hodnoty v ret_val, pokud neni druha tiskne NONE)
     2 (pocet kladnych hodnot)


1.
2.

---> 0
     NONE
     0

1.0 2.5
2.0

---> ERROR

BRUTE chyba:
1.95 3.45 1.0 3.05 4.35 -3.05 -0.05 -2.4 4.6 4.0 3.5 1.9 3.55 1.75 4.75 -3.1 3.7 -2.55
4.25 3.15 0.85 1.45 -2.15 4.5 2.5 1.75 3.85 1.9 -2.45 -2.9 -2.45 4.8 4.7 3.4 -1.45 -2.45
"""
import sys


def f(x, y):
    return (x - 1/2) * (1 - y) - x**x + (2 - y) * (2 - y) * (2 - y) - 10


def idx_second_max(f_values):
    first_max_idx = f_values.index(max(f_values))  # vzdycky bude
    try:
        second_max_idx = f_values.index(max(f_values), first_max_idx + 1)
        return second_max_idx
    except ValueError as ve:
        return 'NONE'  # neni uz druhy max


def test_second_max():
    v = [2, 3, 4, 5, 7.7, 8.9, 10.2, 5, 6, 8.9, 10.2]
    print(idx_second_max(v))


def function_values(x, y):
    ret_val_abs = []
    ret_val = []
    for i in range(len(x)):
        ret_val_abs.append(abs(f(x[i], y[i])))  # absolutni hodnoty
        ret_val.append(f(x[i], y[i]))  # skutecne hodnoty
    min_idx = ret_val_abs.index(min(ret_val_abs))  # (idx min abs f(x,y))
    num_of_positive = len([x for x in ret_val if x > 0])  # pocet kladnych hodnot puvodni funkce
    second_max_idx = idx_second_max(ret_val)
    # print(ret_val)
    # print(ret_val_abs)
    print(min_idx)
    print(second_max_idx)
    print(num_of_positive)


def test():
    x_s = load_input(input())
    y_s = load_input(input())
    if len(x_s) != len(y_s):
        print("ERROR")
    else:
        function_values(x_s, y_s)

def load_input(inp):
    nums = list(map(float, inp.strip().split()))
    # print(nums)
    return nums


if __name__ == '__main__':
    # load_input(input())
    test()
    sys.exit(0)
