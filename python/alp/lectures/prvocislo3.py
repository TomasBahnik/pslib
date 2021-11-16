# prvocislo3.py - Vypíše prvočísla menší než zadaný limit
import sys

m = int(sys.argv[1])
for n in range(2, m):  # cyklus 2..m-1
    p = 2  # začátek testu
    while p * p <= n:
        if n % p == 0:
            break
        p += 1
    if p * p > n:  # n je prvočíslo
        print(n, end=", ")
print()  # závěrečný konec řádky
