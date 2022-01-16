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
"""
INPUTS:
24 8
0 0 0 0 0 0 1 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 0 0 0 1 1 0 0 0 0 0
"""


# def size(col, row):
#     play_size = []
#     for i in range(col):
#         continue
#     for j in range(row):
#         print()
#         for i in range(col):
#             play_size.append("")
#             print(play_size)
# size(c,r)
def adam7_size(original, col, row):
    col_div = col // 8
    row_div = row // 8
    col_row = col_div * row_div
    output = [original] * (col_row)
    # print(output)
    # print(len(output))
    return output


# print(adam7_size(adam7,c,r))
big_list = adam7_size(adam7, c, r)
# for i in range(0,9):
#     for j in range(0,8):
#         for k in range(0,8):
#             print(big_list[i][j][k])

big_values = []
x = 0
y = 8
col_div = c // 8
row_div = r // 8
col_row = col_div * row_div
while len(big_values) != col_row * len(adam7):
    big_values.append(values[x:y])
    x += 8
    y += 8


def dopln_pole(pole, delka):
    return pole + [0] * (delka - len(pole))


# for j in range(0, col_row * len(adam7)):
for i in range(len(big_values)):
    for k in range(0, 8):
        if i > 0 and len(big_values[i]) == 0:
            big_values[i] = big_values[i - 1]
        if k <= len(big_values[i]) and big_values[i][k] != 0 and big_values[i][k] != 1:
            big_values[i][k] = big_values[i][k - 1]
        else:
            continue

print(big_values)

# def nwm(adam7):
#     for i in range(len(adam7)):
#         count2 = adam7[i].count(7)
#         print(count2, end="")
#     return count2
# nwm(adam7)
