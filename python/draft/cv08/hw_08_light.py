# 1. kameny zcela vyplni matici
# 2. jsou použity všechny kameny
# 3. každý zcela leží uvnitř matice
# 4. žadné políčko matice není prázdné
# 5. barva kamene je vždy větší než 0
# pokud existuje více řešení, vypište libovolné z nich
import sys

from draft.shared.general import debug_print

DEBUG_PRINTS = True
# indexes
STONE_COLOR = 0
STONE_CELLS = 1
STONE_BORDER = 2  # used for sort
CELL_ROW = 0
CELL_COLUMN = 1


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


# see 1 and 2
# all stones must be used and fill the whole matrix
def check_stone_areas(rows, cols, stones):
    area = 0
    for stone in stones:
        s_c = len(stone[STONE_CELLS])
        area += s_c
        print("color={}, area ={}".format(stone[0], s_c))
    if area != rows * cols:
        print('NOSOLUTION')
        return -1
    return area


# relabel stone cells as if it is at
# top left corner, shift all cells so that
# min row = 0 and min column = 0
def move_to_top_left_corner(stone):
    stone_cells = stone[STONE_CELLS]
    min_row = min([cell[CELL_ROW] for cell in stone_cells])
    min_col = min([cell[CELL_COLUMN] for cell in stone_cells])
    for cell in stone_cells:
        cell[CELL_ROW] -= min_row
        cell[CELL_COLUMN] -= min_col
    return stone_cells


def stone_border(stone):
    n = 0
    cells = stone[STONE_CELLS]
    for cell in cells:
        l = [cell[CELL_ROW] - 1, cell[CELL_COLUMN]] in cells
        r = [cell[CELL_ROW] + 1, cell[CELL_COLUMN]] in cells
        b = [cell[CELL_ROW], cell[CELL_COLUMN] + 1] in cells
        t = [cell[CELL_ROW], cell[CELL_COLUMN] - 1] in cells
        n += len([x for x in [l, r, b, t] if x is False])
    stone.append(n)
    return n


if __name__ == '__main__':
    filename = sys.argv[1]
    M, N, stones = read_stones(filename)
    for stone in stones:
        # debug_print("Before {}]".format(stone), DEBUG_PRINTS)
        moved_cells = move_to_top_left_corner(stone)
        boarder = stone_border(stone)
        debug_print("Stone {} : cells={}, border={}]"
                    .format(stone[STONE_COLOR], stone[STONE_CELLS], stone[STONE_BORDER]), DEBUG_PRINTS)

    print("matrix {}x{}".format(M, N))
    check_stone_areas(M, N, stones)
