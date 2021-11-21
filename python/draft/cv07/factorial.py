import sys

x = int(input())


def factorial(n):
    fac = 1
    for i in range(1, n + 1):
        fac = fac * i
        if i == n:
            print(fac)


def factorial_2(n):
    if n == 0:
        return 1
    return factorial_2(n - 1) * n


print(factorial_2(x))

sys.exit(0)
