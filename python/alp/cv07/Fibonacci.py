def fib(n):
    if reseni[n] != None:
        return reseni[n]

    if n == 0 or n == 1:
        return 1

    reseni[n] = fib(n - 2) + fib(n - 1)
    return reseni[n]


reseni = [None] * 10
print(fib(6))
# for i in range(1, 50):
#     print(fib(i) / fib(i - 1))


def fib(n):
    if n in reseni:
        return reseni[n]

    if n == 0 or n == 1:
        return 1

    reseni[n] = fib(n - 2) + fib(n - 1)
    return reseni[n]

# dictionary
reseni = {}
# reseni = [None] * 10
print(fib(10))
print(reseni)
# for i in range(1, 50):
#     print(fib(i) / fib(i - 1))
