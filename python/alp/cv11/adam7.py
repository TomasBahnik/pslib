c_r = list(map(int, input().strip().split()))
values = list(map(int, input().strip().split()))
adam7 = [[1, 6, 4, 6, 2, 6, 4, 6],
         [7, 7, 7, 7, 7, 7, 7, 7],
         [5, 6, 5, 6, 5, 6, 5, 6],
         [7, 7, 7, 7, 7, 7, 7, 7],
         [3, 6, 4, 6, 3, 6, 4, 6],
         [7, 7, 7, 7, 7, 7, 7, 7],
         [5, 6, 5, 6, 5, 6, 5, 6],
         [7, 7, 7, 7, 7, 7, 7, 7]]

"""sloupce"""
c = c_r[0]
"""radky"""
r = c_r[1]

if c % 8 != 0:
    print("ERROR! zadej cislo delitelne 8")
    exit(1)
if r % 8 != 0:
    print("ERROR! zadej cislo delitelne 8")
    exit(1)

"""
INPUTS:
24 24
0 0 0 0 0 0 1 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 0 0 0 1 1 0 0 0 0 0
"""


# for col in range(c):
#     continue
# for row in range(r):
#     print()
#     for col in range(len(values)):
#         if values[col] == 1:
#             print("x", end=" ")
#         else:
#             print("", end=" ")

def adam7_size(original, col, row):
    col_div = col // 8
    row_div = row // 8
    output = [original] * (col_div * row_div)
    # print(output)
    # print(len(output))
    return output


adam7_size(adam7, c, r)
