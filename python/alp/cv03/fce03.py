# program pro generovani dokonalych cisel

def sumOfDivisors(n):
    suma = 0
    for i in range(1, n):
        if n % i == 0:
            print("zpracovavam{}, soucet={}".format(i, suma))
            suma += i
    return suma


print(sumOfDivisors(100))
