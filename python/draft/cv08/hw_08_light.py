# 1. kameny zcela vyplni matici
# 2. jsou použity všechny kameny
# 3. každý zcela leží uvnitř matice
# 4. žadné políčko matice není prázdné
# 5. barva kamene je vždy větší než 0
# pokud existuje více řešení, vypište libovolné z nich
import sys

from draft.shared.general import debug_print

# denotes empty cells in the board
# color of stone is guaranteed to be > 0
NOSOLUTION = 'NOSOLUTION'
EMPTY_CELL_COLOR = 0

DEBUG_PRINTS = False
# indexes
STONE_COLOR = 0
STONE_CELLS = 1
# stone border length is appended in draft.cv08.hw_08_light.stone_border, so here should be -1 for index
STONE_BORDER = -1  # used for sort
STONE_SORT_BORDER = 10  # used to switch sorting of stones
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
        debug_print("color={}, area ={}".format(stone[0], s_c), DEBUG_PRINTS)
    if area != rows * cols:
        print("Areas do not fit :" + NOSOLUTION)
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


def sort_stones(stones, key=STONE_SORT_BORDER):
    # key=lambda x: len(x[1]), reverse=True : sort by area
    # key=lambda x: x[STONE_BORDER] : sort by length of border
    if key == STONE_SORT_BORDER:
        stones.sort(key=lambda x: x[STONE_BORDER], reverse=True)
    else:
        stones.sort(key=lambda x: len(x[1]), reverse=True)


def prepare_stones(stones):
    for stone in stones:
        # debug_print("Before {}]".format(stone), DEBUG_PRINTS)
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
        # right and bottom board border overflow
        # only top right and top bottom cells can used
        #     max_row = max([cell[CELL_ROW] for cell in cells])
        #     max_col = max([cell[CELL_COLUMN] for cell in cells])
        # but for checking if stone is present all cells need to be tested
        row_overflow = new_cell_row > board_max_row_idx
        col_overflow = new_cell_col > board_max_col_idx
        # do not ask for stone present at [new_cell_row, new_cell_col] because it could be
        # out of range in case of overflow
        if col_overflow or row_overflow:
            return False
        # another stone already present
        stone_present = board[new_cell_row][new_cell_col] != EMPTY_CELL_COLOR
        if stone_present:
            return False
    return True


# count puts and deletes of stones = compare order of stones by area or by boarder
puts = 0
deletes = 0


def fill(board, stone_no, stones):
    global puts, deletes
    if stone_no == len(stones):  # all stones used
        if not any(EMPTY_CELL_COLOR in x for x in board):
            debug_print("Puts {},  deletes {}".format(puts, deletes), DEBUG_PRINTS)
            print(board)
            sys.exit(0)

    board_rows = len(board)
    board_cols = len(board[0])
    last_stone = stones[stone_no]
    stone_color = last_stone[STONE_COLOR]
    for r in range(0, board_rows):
        for c in range(0, board_cols):
            if stone_fits_on_board(last_stone, board, r, c):
                puts += 1
                # put the stone color on board starting at [r,c]
                fill_stone(board, last_stone, r, c, stone_color)
                # try to put next stone
                fill(board, stone_no + 1, stones)
                # the last_stone does not fit on the board => delete *the last successfully* placed stone
                # *the last successfully* placed last_stone and r and c are still available
                deletes += 1
                # delete means put EMPTY_CELL_COLOR on the board instead of stone color
                fill_stone(board, last_stone, r, c, EMPTY_CELL_COLOR)


def fill_stone(board, stone, row, column, color):
    for cell in stone[STONE_CELLS]:
        cell_row = row + cell[CELL_ROW]
        cell_column = column + cell[CELL_COLUMN]
        board[cell_row][cell_column] = color


if __name__ == '__main__':
    filename = sys.argv[1]
    rows, cols, stones = read_stones(filename)
    board = [[EMPTY_CELL_COLOR] * cols for i in range(0, rows)]
    check_stone_areas(rows, cols, stones)
    prepare_stones(stones)
    fill(board, 0, stones)
    print(NOSOLUTION)
    sys.exit(0)
