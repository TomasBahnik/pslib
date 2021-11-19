import sys


def read_stones(filename):
    stones = []  # vystup funkce - seznam nactenych kamenu
    f = open(filename, "r")
    num_rows = int(f.readline().strip())  # precti 1. radek ze souboru
    num_cols = int(f.readline().strip())  # precti 2. radek ze souboru
    for line in f:
        numbers = list(map(int, line.strip().split()))  # precti vsechna cisla na dalsich radcich
        color = numbers[0]  # prvni z nich je barva kamene
        coords = numbers[1:]  # zbyle jsou souradnice r1 c1 ... rn cn
        cells = []  # prevedeme [r1,c1 ... rn,cn] na pole cells = [[r1,c1], ... [rn,cn]]
        for i in range(len(coords) // 2):
            cells.append([coords[2 * i + 0], coords[2 * i + 1]])
        stones.append([color, cells])
    f.close()
    return num_rows, num_cols, stones


def check_stone_areas(rows, cols, stones):
    area = 0
    for stone in stones:
        s_a = len(stone[1])
        area += s_a
        print("color={}, area ={}".format(stone[0], s_a))
    if area != rows * cols:
        print('NOSOLUTION')
        return -1
    return area


filename = sys.argv[1]

M, N, stones = read_stones(filename)
print("matrix {}x{}".format(M, N))
check_stone_areas(M, N, stones)

# n-ty kamen je stones[n]
# jeho barva je stones[n][0], jeho bunky jsou stones[n][1]

# vypis pozic n-teho kamene:
n = 5  # napriklad chceme 0.kamen
print("color={}".format(stones[n][0]))

for cellindex in range(len(stones[n][1])):
    row, col = stones[n][1][cellindex]
    print(row, col)
