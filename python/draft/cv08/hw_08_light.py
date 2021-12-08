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
    """
    According to assignment all stones must be used and fully fill the whole board.
    Calculate area of stone as sum of cells i.e. each cell has area=1
    :param rows: number of board rows
    :param cols: number of board columns
    :param stones: stones
    :return: area of board and stones if equal or exists with exit code and message
    """
    area = 0
    for stone in stones:
        s_c = len(stone[STONE_CELLS])
        area += s_c
        debug_print("color={}, area ={}".format(stone[0], s_c), DEBUG_PRINTS)
    if area != rows * cols:
        print("Stones do not fit on board exactly")
        print(NOSOLUTION)
        sys.exit(EC_STONES_DO_NOT_FIT_EXACTLY_ON_BOARD)
    return area


def move_to_top_left_corner(stone):
    """
    Relabels in place stone cells as if it sits at top left corner
    by shift all cells so that min row = 0 and min column = 0
    i.e. subtract min_row from all row positions and
    min_col from all columns positions
    :param stone: stone
    :return: relabeled stone cells
    """
    stone_cells = stone[STONE_CELLS]
    min_row = min([cell[CELL_ROW] for cell in stone_cells])
    min_col = min([cell[CELL_COLUMN] for cell in stone_cells])
    for cell in stone_cells:
        cell[CELL_ROW] -= min_row
        cell[CELL_COLUMN] -= min_col
    return stone_cells


# 90 is [[0,-1],[1,0]]
def rotate_stone_counter_clockwise_90(stone):
    stone_cells = stone[STONE_CELLS]
    for cell in stone_cells:
        r = cell[CELL_ROW]
        c = cell[CELL_COLUMN]
        cell[CELL_ROW] = -c
        cell[CELL_COLUMN] = r
    return stone_cells


def stone_border(stone):
    """
    Calculates border length of stone as number of missing neighbours.
    The length of border is appended to the stone definition and thus can accessed
    at index -1 (last element)
    :param stone: stone
    :return: length of stone border
    """
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
    """
    Sort stones in place either by area or length of border in descending order.
    :param stones:
    :param key: Key used for sorting. Default value is by length of boarder
    :return: None
    """
    # key=lambda x: len(x[1]), reverse=True : sort by area
    # key=lambda x: x[STONE_BORDER] : sort by length of border
    if key == SORT_STONES_BY_BORDER:
        stones.sort(key=lambda x: x[STONE_BORDER], reverse=True)
    else:
        stones.sort(key=lambda x: len(x[1]), reverse=True)


def prepare_stones(stones):
    """
    Relabels and sorts the stones in place
    :param stones:
    :return: None
    """
    for stone in stones:
        debug_print("Before {}]".format(stone), DEBUG_PRINTS)
        move_to_top_left_corner(stone)
        stone_border(stone)
        debug_print("Stone {} : cells={}, border={}]"
                    .format(stone[STONE_COLOR], stone[STONE_CELLS], stone[STONE_BORDER]), DEBUG_PRINTS)
    sort_stones(stones)


def stone_fits_on_board(stone, board, row, col):
    """
    Check if the stone can be placed on board starting at board [row,col] position
    Stone cannot be placed if it
       * overflows board boarder
       * overlays already placed stone
    :param stone:
    :param board:
    :param row: row where stone starts
    :param col: col where stone starts
    :return: True/False
    """
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
# puts = 0
# deletes = 0

def fill_stone(board, stone, row, column, color):
    """
    Prints/deletes the stone (color) on/from board at given position.
    Stone is deleted from board by setting the color of the position to EMPTY_CELL_COLOR.
    EMPTY_CELL_COLOR is used initialized the board and no stone can have this color
    :param board:
    :param stone:
    :param row:
    :param column:
    :param color:
    :return:
    """
    for cell in stone[STONE_CELLS]:
        cell_row = row + cell[CELL_ROW]
        cell_column = column + cell[CELL_COLUMN]
        board[cell_row][cell_column] = color


def fill(board, stone_no, stones):
    """
    recursively puts stones on the board
    :param board:
    :param stone_no:
    :param stones:
    :return:
    """
    # global puts, deletes
    if stone_no == len(stones):  # all stones used
        if not any(EMPTY_CELL_COLOR in x for x in board):  # board does not contains any EMPTY_CELL_COLOR
            # debug_print("Puts {},  deletes {}".format(puts, deletes), DEBUG_PRINTS)
            print(board)  # print filled board
            sys.exit(EC_SOLUTION_FOUND)
        # all stones are used but there is EMPTY_CELL_COLOR
        # e.g two identical cells 2 6 4 7 4 7 4 instead of 2 6 4 7 4 7 3
        else:
            print("All stones used but empty cell left on board")
            print(NOSOLUTION)
            # print(board)
            sys.exit(EC_EMPTY_CELL_LEFT_ON_BOARD)

    board_rows = len(board)
    board_cols = len(board[0])
    last_stone = stones[stone_no]
    stone_color = last_stone[STONE_COLOR]
    for r in range(0, board_rows):
        for c in range(0, board_cols):
            if stone_fits_on_board(last_stone, board, r, c):
                # puts += 1
                # put the stone color on board starting at [r,c]
                fill_stone(board, last_stone, r, c, stone_color)
                # try to put next stone
                fill(board, stone_no + 1, stones)
                # the stone_no + 1 does not fit on the board (stone_fits_on_board returns False)
                # previous call returns (there is no else after last if!)
                # AND continues at the point where it forked new fill function i.e. HERE
                # => deletes the stones it has created
                # deletes += 1
                # delete means put EMPTY_CELL_COLOR on the board instead of stone color
                fill_stone(board, last_stone, r, c, EMPTY_CELL_COLOR)
    # there is implicit return at the end of the function block
    # here the function returns when outer for loop finishes without recursively calling next fill function
    # i.e. when the stone does not fit for any position in board
    # this makes the return explicit
    return None


if __name__ == '__main__':
    filename = sys.argv[1]
    rows, cols, stones = read_stones(filename)
    board = [[EMPTY_CELL_COLOR] * cols for i in range(0, rows)]
    check_stone_areas(rows, cols, stones)
    prepare_stones(stones)
    fill(board, 0, stones)
    print(NOSOLUTION)
    sys.exit(EC_CANNOT_FIT_ALL_STONES)
