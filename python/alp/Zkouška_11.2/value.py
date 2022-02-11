"""
INPUTS
0. 1. -1. 0.5
1. 0. -1. -1.5

---> 1 (idx min abs f(x,y))
     2 (idx druhe max hodnoty)
     2 (pocet kladnych hodnot)


1.
2.

---> 0
     NONE
     0

1.0 2.5
2.0

---> ERROR
"""
import sys


def f(x, y):
    return x * y


def idx_second_max(f_values):
    first_max_idx = f_values.index(max(f_values)) # vzdycky bude
    try:
        second_max_idx = f_values.index(max(f_values), first_max_idx + 1)
        print(second_max_idx)
    except ValueError as ve:
        print('NONE')  # neni uz druhy max


def test_second_max():
    v = [2, 3, 4, 5, 7.7, 8.9, 10.2, 5, 6, 8.9, 10.2, 134]
    idx_second_max(v)


def function_values(x, y):
    ret_val_abs = []
    ret_val = []
    for i in range(len(x)):
        ret_val_abs.append(abs(f(x[i], y[i])))  # absolutni hodnoty
        ret_val.append(f(x[i], y[i]))  # skutecne hodnoty
    min_idx = ret_val_abs.index(min(ret_val_abs))  # (idx min abs f(x,y))
    num_of_positive = len([x for x in ret_val if x > 0])  # pocet kladnych hodnot puvodni funkce
    print(ret_val_abs)
    print(min_idx, num_of_positive)


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
