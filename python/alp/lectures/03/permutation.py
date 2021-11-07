import random


def permutation(n):
    "Create a random permutation of integers 0..n-1"
    p = list(range(n))
    for i in range(n - 1):
        r = random.randrange(i, n)
        temp = p[r]
        p[r] = p[i]
        p[i] = temp
    return (p)
