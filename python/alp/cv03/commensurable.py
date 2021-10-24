# vstupy
# a = int(input())
# b = int(input())
a = 2
b = 10


def r_s():
    return max(a, b) - min(a, b)


def deli(x, y):
    if x < y:
        x, y = y, x
    zb = x % y
    while zb != 0:
        x = y
        y = zb
        zb = x % y
    return y > 1


if a < 2 or b < 2 or a == b:
    print("ERROR")
else:
    for n in range(r_s() + 1):
        for m in range(r_s() + 1):
            if deli(n, m):
                print('x', end='|')
            else:
                print(' ', end='|')
        print("\n------------------")
