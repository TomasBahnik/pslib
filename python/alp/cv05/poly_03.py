def f(poly, x):
    res = 0
    for i in range(len(poly)):
        res += poly[i] * (x ** i)
    return res

#rychlejsi metoda 
def f2(poly, x):
    prev = poly[-1]
    for i in range(len(poly) - 2, -1, -1):
        act = poly[i] + prev * x
        prev = act
    return prev


a = [10, 0, 3, 1]
b = [1, 2]
print(f(a, 10))
print(f2(a, 10))
