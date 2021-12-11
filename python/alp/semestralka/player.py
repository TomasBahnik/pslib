import alp.semestralka.base as base

from alp.semestralka.draw import Drawer

from draft.cv08.hw_08_light import move_to_top_left_corner, rotate_stone_counter_clockwise_90, CELL_COLUMN, \
    CELL_ROW, EMPTY_CELL_COLOR


class Player(base.BasePlayer):
    def __init__(self, name, board, marks, stones, player):
        """ constructor of Player. Place you variables here with prefix 'self' -> e.g. 'self.myVariable' """

        base.BasePlayer.__init__(self, name, board, marks, stones, player)  # do not change this line!!
        self.algorithm = "my great method"  # name of your method. Will be used in tournament mode

    def moveStone(self, stone, row_col):
        # stone = [[row1, col1], ... [rown, coln]]
        # row, col = int
        # create new stone, place it to row, col
        newStone = []
        for cell in stone:
            rowCell, colCell = cell
            newRow = rowCell + row_col[0]
            newCol = colCell + row_col[1]
            newStone.append([newRow, newCol])
        return newStone

    def canBePlaced(self, stone, stoneColor):
        # stone = [[row, col], ... [row, col]]
        # true if all [row, cal] inside board and all row, col are free i.e. the cell contains 0
        for cell in stone:
            row, col = cell
            if self.inBoard(row, col) and self.board[row][col] == 0:
                pass
            else:
                return False
        if not self.has_correct_side(stone, stoneColor):
            return False
        return True

    def move(self):
        """ return [ stoneIdx, [ stonePosition] ]
            stoneIdx .. integer .. index of stone to self.freeStones
            [stonePosition] = [ [row1,col1] ... [rown, coln] ] .. position into board where stone is placed

            if no stone can be placed:
            return []
        """
        try:
            stoneIdx = self.freeStones.index(True)
            stoneColor, stone = self.stones[stoneIdx]
        except ValueError as ve:
            return []

        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                moveStone = self.moveStone(stone, [row, col])
                if self.canBePlaced(moveStone, stoneColor):
                    return [stoneIdx, moveStone]

        return []

    # nově položený kamen se musí dotýkat alespoň jednou hranou některého z již položených kamenů
    # kameny stejné barvy se nikdy nesmějí dotýkat hranou (kameny různých barev se mohou dotýkat)
    # nesmi vzniknout zcela pokryta bunka 2x2
    # color > 0 we can divide
    def has_correct_side(self, stone, color):
        same_color_cnt = 0  # must be zero
        empty_color_cnt = 0  # no limit but can used for existence of 2x2 cells
        diff_color_cnt = 0  # must be >= 1
        for cell in stone:
            # colors > 0 or EMPTY_CELL_COLOR = 0. test ratio might be less than 1
            row = cell[CELL_ROW] - 1
            col = cell[CELL_COLUMN]
            t_c = self.board[row][col] if self.inBoard(row, col) else None
            top = t_c / color if t_c is not None else None

            row = cell[CELL_ROW] + 1
            col = cell[CELL_COLUMN]
            b_c = self.board[row][col] if self.inBoard(row, col) else None
            bottom = b_c / color if b_c is not None else None

            row = cell[CELL_ROW]
            col = cell[CELL_COLUMN] + 1
            r_c = self.board[row][col] if self.inBoard(row, col) else None
            right = r_c / color if r_c is not None else None

            row = cell[CELL_ROW]
            col = cell[CELL_COLUMN] - 1
            l_c = self.board[row][col] if self.inBoard(row, col) else None
            left = l_c / color if l_c is not None else None

            same_color_cnt += len([x for x in [top, bottom, right, left] if x is not None and x == 1])
            diff_color_cnt += len([x for x in [top, bottom, right, left] if x is not None and x != 1])
            empty_color_cnt += len([x for x in [top, bottom, right, left] if x is not None and x == EMPTY_CELL_COLOR])
        return same_color_cnt == 0  # only one condition


# kameny nesmí přečnívat z desky, nebo zakrývat (ani částečně) již položené kameny
def is_move_valid(player, move):
    # use player board to check
    # player_sign = player.player
    # player_board = player.board
    # any(player_sign in x for x in player_board)
    return len(move) != 0


def shift_stones(stones):
    for s in stones:
        move_to_top_left_corner(s)


def rotate_stones(stones):
    for s in stones:
        rotate_stone_counter_clockwise_90(s)


if __name__ == "__main__":

    # load stones from file
    stones = base.loadStones("stones.txt")
    print("stones are", stones)
    shift_stones(stones)
    rotate_stones(stones)
    shift_stones(stones)

    # prepare board and marks
    board, marks = base.makeBoard10()

    # create both players
    p1 = Player("pepa", board, marks, stones, 1)
    p2 = Player("franta", board, marks, stones, -1)

    # not necessary, only if you want to draw board to png files
    d = Drawer()
    d.draw(p1.board, p1.marks, "init.png")

    moveidx = 0
    while True:
        p1play = True
        p2play = True

        move_ret_val = p1.move()  # first player, we assume that a corrent output is returned

        # the following if/else is simplified. On Brute, we will check if return value
        # from move() is valid ...
        if not is_move_valid(p1, move_ret_val):
            p1play = False
        else:
            stoneIdx, stone = move_ret_val
            stoneColor = stones[stoneIdx][0]
            base.writeBoard(p1.board, stone, stoneColor)  # write stone to player1's board
            base.writeBoard(p2.board, stone, stoneColor)  # write stone to player2's board
            p1.freeStones[stoneIdx] = False  # tell player1 which stone is used
            p2.freeStones[stoneIdx] = False  # tell player2 which stone is used

        d.draw(p2.board, p2.marks, "move-{:02d}a.png".format(moveidx))  # draw to png

        # now we call player2 and update boards/freeStones of both players
        move_ret_val = p2.move()
        if not is_move_valid(p2, move_ret_val):
            p2play = False
        else:
            stoneIdx, stone = move_ret_val
            stoneColor = stones[stoneIdx][0]
            base.writeBoard(p1.board, stone, stoneColor)
            base.writeBoard(p2.board, stone, stoneColor)
            p1.freeStones[stoneIdx] = False
            p2.freeStones[stoneIdx] = False

        d.draw(p1.board, p1.marks, "move-{:02d}b.png".format(moveidx))

        # if both players return [] from move, the game ends
        if p1play is False and p2play is False:
            print("end of game")
            break

        moveidx += 1
        print(" -- end of move ", moveidx, " score is ", p1.score(p1.player), p1.score(-p1.player))
