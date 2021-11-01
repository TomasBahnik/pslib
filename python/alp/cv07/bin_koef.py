def binom(n, k):
    if k == 0 or k == n:
        return 1
    if k == 1 or k == n - 1:
        return n
    return binom(n - 1, k) + binom(n - 1, k - 1)


binom(1, -1)
