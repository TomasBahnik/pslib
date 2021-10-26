import copy

a = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
     [0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
     [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
     ]


def neighbors(m, row, col):
    alive = 0
    nrows = len(m)
    ncols = len(m[0])
    for i in range(row - 1, row + 1 + 1):
        for j in range(col - 1, col + 1 + 1):
            alive += m[i % nrows][j % ncols]
        alive -= m[row][col]
    return alive


def life(old):
    new = copy.deepcopy(old)
    for row in range(len(old)):
        for col in range(len(old[row])):
            alive = neighbors(old, row, col)
            new[row][col] = 0
            if alive == 3:
                new[row][col] = 1
            if old[row][col] == 1 and alive == 2:
                new[row][col] = 1
    return new


def pm(m):
    for row in range(len(m)):
        for col in range(len(m[row])):
            if m[row][col] == 1:
                print("*", end="")
            else:
                print(".", end="")


for i in range(40):
    pm(a)
    a = life(a)
    print()
    time.sleep(0.5)
pm(a)
