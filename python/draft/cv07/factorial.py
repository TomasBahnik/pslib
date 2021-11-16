x = int(input())


def factorial(n):
    fac = 1
    for i in range(1, n + 1):
        fac = fac * i
        if i == n:
            print(fac)


factorial(x)
