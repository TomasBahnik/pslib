import sys

#
# def read_value(filename):
#     f = open(filename, "r")
#     row1 = list(f.readline())  # precti 1. radek ze souboru
#     row2 = list(f.readline())  # precti 2. radek ze souboru
#     # print(row1, row2)
#     return (x, y)


# read_value(sys.argv[1])
#
# x, y = read_value(sys.argv[1])
#
# sys.exit()
"""
input :
0. 1. -1. 0.5
1. 0. -1. -1.5

input2 :
1. 2.
2. 3.

input3 :
1.0 2.5
"""

x = list(map(float, input().split()))
y = list(map(float, input().split()))


def poly(x, y):
    f = (1 / 2) * x ** 2 * (1 - y) ** 2 + (x - 2) ** 3 - 2 * y + x
    return f


if len(x) != len(y):
    print("ERROR")
    sys.exit(1)

f_values = []


def napln_fce(a, b):
    for i in range(0, len(a)):
        f_values.append(poly(a[i], b[i]))


napln_fce(x, y)
# print(f_values)

max_idx = f_values.index(max(f_values))
# prvni hodnota
# print(max_idx)

# f_values.sort()
# print(f_values)
zaporny_cisla = [x for x in f_values if x < 0]
# druha hodnota
# print(len(zaporny_cisla))


def poly_2(a, b):
    for i in range(0, len(f_values)):
        v = f_values[i] * (a[i] + 2) * (b[i] - 2)
        f_values[i] = v
    return f_values


poly_2(x, y)
# print(f_values)
min_idx = f_values.index(min(f_values))
# treti hodnota
# print(min_idx)

print(max_idx, len(zaporny_cisla), min_idx)