#program na generovani sexi cisel

def isPrime(n):
    for i in range(2, int(n ** (1 / 2)) + 1):
        if n % i == 0:
            return False
        return True


for i in range(2, 993):
    if isPrime(i) and isPrime(i + 6):
        print(i, i + 6)
