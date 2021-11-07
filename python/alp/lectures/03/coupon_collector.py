# -*- coding: utf-8 -*-
# Simulace problému sběratele, 
import random
import sys

n = int(sys.argv[1])  # počet různých prvků
collectedCount = 0  # počet již vybraných různých prvků
isCollected = [False] * n  # již jsme viděli tento prvek
count = 0  # kolik prvků jsme již vybrali

while collectedCount < n:
    r = random.randrange(n)  # náhodný prvek 0..n-1
    count += 1
    if not isCollected[r]:  # nový prvek
        collectedCount += 1
        isCollected[r] = True

print("Pro n=%d bylo potřeba %d výběrů." % (n, count))
