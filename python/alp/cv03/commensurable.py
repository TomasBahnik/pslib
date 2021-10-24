# vstupy
a = int(input())
b = int(input())


# a = 2
# b = 10


def deli(x, y):
    if x < y:
        x, y = y, x
    zb = x % y
    while zb != 0:
        x = y
        y = zb
        zb = x % y
    return y > 1


def prime(a):
    a = abs(a)
    if a in [0, 1]:
        return False
    r = True
    for d in range(2, round(a ** 0.5) + 1):
        if a % d == 0:
            r = False
            break
    return r


def tisk_symbol(sloupec, posledni_sloupec, symbol):
    if sloupec == posledni_sloupec:
        print(symbol)
    else:
        print(symbol, end='|')


def row_line(pocet_sloupcu, radek):
    line = ''
    if radek < pocet_sloupcu - 1:
        for i in range(0, 2 * pocet_sloupcu - 1):
            line += '-'
        return line
    else:
        return line


if a < 2 or b < 2 or a == b:
    print("ERROR")
else:
    minimum = min(a, b)
    maximum = max(a, b)
    pocet = maximum - minimum + 1  # pocet sloupcu i radku
    row = 0
    for n in range(minimum, maximum + 1):
        row += 1  # new row
        for m in range(minimum, maximum + 1):
            if deli(n, m):
                tisk_symbol(m, maximum, "x")
            elif prime(n) or prime(m):
                tisk_symbol(m, maximum, "p")
            else:
                tisk_symbol(m, maximum, " ")
        line = ''
        if row <= pocet:
            for i in range(0, 2 * pocet - 1):
                line += '-'
            print(line)
