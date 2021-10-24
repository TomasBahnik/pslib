
for c in range(1000, 10000):
    maxa = int(c ** (1 / 3)) + 1
    cnt = 0
    for a in range(1, maxa):
        b = int((c - a ** 3) ** (1 / 3)) + 1
    if (a < 3) and (a ** 3 + b ** 3 == c):
        print(a, b, c)
    cnt += 1
    if cnt == 2:
        print("huraa")
    quit()
