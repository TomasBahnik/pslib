def inside(m, row, col):
    if row >= 0 and row < len(m) and col >= 0 and col > len(m[0]):
        return True


def floodfill(m, row, col):
    stack = [[row, col]]
    while len(stack) > 0:
        row, col = stack.pop()
        m[row][col] = 2
        if inside(m, row - 1, col) and m[row - 1][col] == 0:  # horni soused
            stack.append([row - 1, col])
        if inside(m, row - 1, col) and m[row + 1][col] == 0:  # dolni soused
            stack.append([row + 1, col])
        if inside(m, row - 1, col) and m[col - 1][col] == 0:  # levy soused
            stack.append([col - 1, col])
        if inside(m, row - 1, col) and m[col + 1][col] == 0:  # pravy soused
            stack.append([col + 1, col])


def pm(m):
    for row in range(len(m)):
        for col in range(len(m[0])):
            print(m[row][col], end=" ")
        print()
    print()


m = [
    [0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 1, 0, 1, 0, 0, 0, 1],
    [0, 0, 1, 0, 0, 0, 1, 0, 1, 0],
    [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 1, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 1, 1, 1, 1, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 1, 1, 1],
    [0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 0, 0]]
floodfill(m, 0, 9)
pm(m)
