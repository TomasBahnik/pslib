c_r = list(map(int, input().strip().split()))
values = list(map(int, input().strip().split()))
"""sloupce"""
c = c_r[0]
"""radky"""
r = c_r[1]

if c % 8 !=0:
    print("ERROR! zadej cislo delitelne 8")
    exit(1)
if r % 8 !=0:
    print("ERROR! zadej cislo delitelne 8")
    exit(1)

"""
INPUTS:
24 24
0 0 0 0 0 0 1 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 0 0 0 1 1 0 0 0 0 0
"""


for col in range(c):
    continue
for row in range(r):
    print()
    for col in range(len(values)):
        if values[col] == 1:
            print("x", end=" ")
        else:
            print("", end=" ")
