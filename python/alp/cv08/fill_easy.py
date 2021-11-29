"""
def vypln(deska, cisloKamene, kameny):
    #if cisloKamene == len(kameny):
        # kontrola reseni
        # if spravne reseni:
            # print a exit (kdyz tam nebude exit, tak to vypise vsechny reseni)

    # pro vsechny pozice kamene "cisloKamene":
        # zapis kamen na hraci desku
        # vypln(deska, cisloKamene + 1, kameny)
        # vymaz kameny z desky

"""
import sys


def debug_print(message, print_debug):
    if print_debug:
        print(message)


NOSOLUTION = 'NOSOLUTION'

# denotes empty cells in the board
# color of stone is guaranteed to be > 0
EMPTY_CELL_COLOR = 0

DEBUG_PRINTS = False
# indexes
STONE_COLOR = 0
STONE_CELLS = 1
# stone border length is appended in draft.cv08.hw_08_light.stone_border, so here should be -1 for index
STONE_BORDER = -1  # used for sort
SORT_STONES_BY_BORDER = 10  # used to switch sorting of stones
CELL_ROW = 0
CELL_COLUMN = 1

# exit codes
EC_SOLUTION_FOUND = 0
# all stones can't fit on board  = no solution
EC_CANNOT_FIT_ALL_STONES = 1
# all stones used but empty cell remains on board - happens after changing cell
EC_EMPTY_CELL_LEFT_ON_BOARD = 2
EC_STONES_DO_NOT_FIT_EXACTLY_ON_BOARD = 3


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
        s_c = len(stone[STONE_CELLS])
        area += s_c
        debug_print("color={}, area ={}".format(stone[STONE_COLOR], s_c), DEBUG_PRINTS)
    if area != rows * cols:
        print("Stones do not fit on board exactly")
        print(NOSOLUTION)
        sys.exit(EC_STONES_DO_NOT_FIT_EXACTLY_ON_BOARD)
    return area


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
        top = [cell[CELL_ROW] - 1, cell[CELL_COLUMN]] in cells
        bottom = [cell[CELL_ROW] + 1, cell[CELL_COLUMN]] in cells
        right = [cell[CELL_ROW], cell[CELL_COLUMN] + 1] in cells
        left = [cell[CELL_ROW], cell[CELL_COLUMN] - 1] in cells
        n += len([x for x in [top, bottom, right, left] if x is False])
    stone.append(n)
    return n


def sort_stones(stones, key=SORT_STONES_BY_BORDER):
    # key=lambda x: len(x[1]), reverse=True : sort by area
    # key=lambda x: x[STONE_BORDER] : sort by length of border
    if key == SORT_STONES_BY_BORDER:
        stones.sort(key=lambda x: x[STONE_BORDER], reverse=True)
    else:
        stones.sort(key=lambda x: len(x[1]), reverse=True)


def prepare_stones(stones):
    for stone in stones:
        debug_print("Before {}]".format(stone), DEBUG_PRINTS)
        move_to_top_left_corner(stone)
        stone_border(stone)
        debug_print("Stone {} : cells={}, border={}]"
                    .format(stone[STONE_COLOR], stone[STONE_CELLS], stone[STONE_BORDER]), DEBUG_PRINTS)
    sort_stones(stones)


def stone_fits_on_board(stone, board, row, col):
    cells = stone[STONE_CELLS]
    board_max_row_idx = len(board) - 1
    board_max_col_idx = len(board[0]) - 1
    for cell in cells:
        new_cell_col = cell[CELL_COLUMN] + col
        new_cell_row = cell[CELL_ROW] + row
        row_overflow = new_cell_row > board_max_row_idx
        col_overflow = new_cell_col > board_max_col_idx
        if col_overflow or row_overflow:
            return False
        stone_present = board[new_cell_row][new_cell_col] != EMPTY_CELL_COLOR
        if stone_present:
            return False
    return True


def fill_stone(board, stone, row, column, color):
    for cell in stone[STONE_CELLS]:
        cell_row = row + cell[CELL_ROW]
        cell_column = column + cell[CELL_COLUMN]
        board[cell_row][cell_column] = color


def fill(board, stone_no, stones):
    if stone_no == len(stones):  # all stones used
        if not any(EMPTY_CELL_COLOR in x for x in board):  # board does not contains any EMPTY_CELL_COLOR
            print(board)  # print filled board
            sys.exit(EC_SOLUTION_FOUND)
        else:
            print("All stones used but empty cell left on board")
            print(NOSOLUTION)
            sys.exit(EC_EMPTY_CELL_LEFT_ON_BOARD)

    board_rows = len(board)
    board_cols = len(board[0])
    last_stone = stones[stone_no]
    stone_color = last_stone[STONE_COLOR]
    for r in range(0, board_rows):
        for c in range(0, board_cols):
            if stone_fits_on_board(last_stone, board, r, c):
                fill_stone(board, last_stone, r, c, stone_color)
                fill(board, stone_no + 1, stones)
                fill_stone(board, last_stone, r, c, EMPTY_CELL_COLOR)
    return None


filename = sys.argv[1]
rows, cols, stones = read_stones(filename)
board = [[EMPTY_CELL_COLOR] * cols for i in range(0, rows)]
check_stone_areas(rows, cols, stones)
prepare_stones(stones)
fill(board, 0, stones)
print(NOSOLUTION)
sys.exit(EC_CANNOT_FIT_ALL_STONES)
