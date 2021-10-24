# krajni meze
x1 = -100
x2 = 100

# koeficienty
a5 = float(input())
a4 = float(input())
a3 = float(input())
a2 = float(input())
a1 = float(input())
a0 = float(input())


def polynom(bod):
    return a5 * bod ** 5 + a4 * bod ** 4 + a3 * bod ** 3 + a2 * bod ** 2 + a1 * bod + a0


# zaokrouhleni
z = 0.000000001
# xi = 0

while abs(x1 - x2) > z:
    xi = (x1 + x2) / 2
    #print("{}".format(xi))
    if polynom(xi) < 0:
        x1 = xi
    else:
        x2 = xi
print(xi)
