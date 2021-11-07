# -*- coding: utf-8 -*-
import random

h = [0] * 13  # četnost výskytu součtu h[s]
n = 100000

# Simulace n dvojic hodů
for i in range(n):
    x = random.randrange(1, 7)
    y = random.randrange(1, 7)
    s = x + y
    h[s] += 1

# Tisk výsledných pravděpodobností
for s in range(2, 13):
    anal = (6 - abs(s - 7)) / 36
    simul = h[s] / n
    print("s=%2d  P(s)=analyticky %0.3f    simulace %0.3f    chyba %6.3f" %
          (s, anal, simul, anal - simul))
