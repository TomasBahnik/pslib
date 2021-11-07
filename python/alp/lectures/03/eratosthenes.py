# -*- coding: utf-8 -*-
# eratosthenes3.py - Vypíše prvočísla menší než zadaný limit 

import sys

n = int(sys.argv[1])

p = [True] * n  # p[i] = je 'i' prvočíslo?

for i in range(2, n):
    if p[i]:  # je to prvočíslo
        print(i, end=", ")
        j = 2 * i  # označ j=2i,3i,... < n
        while j < n:
            p[j] = False
            j = j + i

print()  # závěrečný konec řádky
